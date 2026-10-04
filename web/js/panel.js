import { ENTITIES, IRC, PERU, VIOLENCE, fmtN, isNational, pct, yKey } from "./config.js";
import { sliceEnares } from "./data.js";
import { getState } from "./state.js";

function infoDepto(departamentos, depto) {
  if (isNational(depto)) {
    return {
      key: PERU.key,
      label: PERU.label,
      n_cem: departamentos.reduce((n, d) => n + (d.n_cem || 0), 0),
    };
  }
  return departamentos.find((d) => d.key === depto);
}

export function renderPanel(bundle) {
  const { meta, departamentos, enares, cem } = bundle;
  const { depto, age, violence } = getState();
  const info = infoDepto(departamentos, depto);
  const { local: sliceLocal, nacional } = sliceEnares(enares, depto, age);
  const local = isNational(depto) ? nacional : sliceLocal;
  const centers = isNational(depto)
    ? Object.values(cem).flat()
    : cem[depto] || [];
  const y = yKey(violence);
  const vlab = VIOLENCE.find((v) => v.id === violence)?.noun || "";
  const ageLab = age === "12_14" ? "12-14" : age === "15_17" ? "15-17" : "12-17";

  document.getElementById("context").textContent =
    `${info?.label || depto} \u00b7 ${vlab} \u00b7 ${ageLab} a\u00f1os \u00b7 ENARES 2024`;
  document.getElementById("title").textContent = info?.label || depto;
  const asideTitle = document.querySelector("aside.card > h2");
  if (asideTitle) asideTitle.textContent = info?.label || depto;

  const locY = local?.[y];
  const natY = nacional?.[y];
  const delta =
    !isNational(depto) && locY != null && natY != null ? (locY - natY) * 100 : null;
  const deltaTxt =
    delta == null
      ? isNational(depto)
        ? "Lectura nacional: todas las alumnas CRS.04 del recorte."
        : ""
      : delta > 0
        ? `${delta.toFixed(1)} puntos por encima del nacional`
        : `${Math.abs(delta).toFixed(1)} puntos por debajo del nacional`;

  const cemTxt = isNational(depto)
    ? `El archivo CEM regulares 2025 registra <strong>${centers.length} centros en el pa\u00eds</strong> (ENE-FEB, solo REGULAR).`
    : centers.length
      ? `El archivo CEM regulares 2025 registra <strong>${centers.length} centros en ${info.label}</strong> (ENE-FEB, solo REGULAR).`
      : `Para <strong>${info.label}</strong> este archivo no trae CEM regulares. No implica ausencia de servicio.`;

  const donde = isNational(depto)
    ? `Alumnas de ${ageLab} a\u00f1os en instituciones educativas de todo el Per\u00fa.`
    : `Alumnas de ${ageLab} a\u00f1os cuya IE est\u00e1 en ${info.label}.`;

  document.getElementById("story").innerHTML = `
    <strong>${donde}</strong>
    El ${pct(locY)} report\u00f3 ${vlab} en los \u00faltimos 12 meses
    (n = ${fmtN(local?.n)}, N = ${fmtN(local?.N)}).
    ${isNational(depto) ? "" : `Nacional: ${pct(natY)}. `}${deltaTxt}
    <br><br>
    El departamento es el de la <strong>instituci\u00f3n educativa</strong>, no de la casa.
    ${cemTxt}
    <span class="fiction">Cifras ponderadas con FACTOR_ALUMNOS. No es predicci\u00f3n individual ni ranking de colegios.</span>
  `;

  document.getElementById("stats").innerHTML = `
    <div class="stat"><b>${pct(locY)}</b><span>${vlab} \u00b7 ${info.label}</span></div>
    <div class="stat"><b>${isNational(depto) ? fmtN(local?.N) : pct(natY)}</b><span>${isNational(depto) ? "Alumnas representadas" : "Nacional \u00b7 misma edad"}</span></div>
    <div class="stat"><b>${centers.length ? `${centers.length} CEM` : "Sin CEM"}</b><span>${meta.cem.periodo} \u00b7 regulares</span></div>
  `;

  const xLabels = meta.x_labels || {};
  const keys = Object.keys(nacional?.x || {});
  document.getElementById("ecological").innerHTML = `
    <div class="eco">
      ${keys
        .map((k) => {
          const a = local?.x?.[k];
          const b = nacional?.x?.[k];
          return `<div><strong>${xLabels[k] || k}</strong>
            <p>${info.label}: ${pct(a)}</p>
            ${isNational(depto) ? "" : `<p>Nacional: ${pct(b)}</p>`}</div>`;
        })
        .join("")}
    </div>
  `;

  const groups = bundle.perfiles?.por?.[violence] || [];
  document.getElementById("profiles").innerHTML = groups
    .map((g, i) => {
      const aviso = g.chico
        ? " Caj\u00f3n chico: no alcanza para un discurso p\u00fablico."
        : "";
      return `<article class="profile${g.chico ? " chico" : ""}">
      <span class="rank">#${i + 1}</span>
      <div>
        <h3>${g.titulo}</h3>
        <p>Adolescentes mujeres de ${ageLab} a\u00f1os. Tipos nacionales; en ${info.label} se leen como hip\u00f3tesis.${aviso} ${g.texto}</p>
        <div class="tags">${(g.tags || []).map((t) => `<span class="tag">${t}</span>`).join("")}</div>
        <div class="detail">
          <b>${g.id}</b> \u00b7 n = ${fmtN(g.n)} \u00b7 N = ${fmtN(g.N)} \u00b7 ${g.edad.toFixed(1)} a\u00f1os<br>
          Superposici\u00f3n 12m: psicol\u00f3gica ${pct(g.psic)} \u00b7 f\u00edsica ${pct(g.fis)} \u00b7 sexual ${pct(g.sex)}
        </div>
      </div>
    </article>`;
    })
    .join("");

  const factorBox = document.getElementById("factors");
  const rows = keys.map((k) => {
    const a = local?.x?.[k] ?? 0;
    const b = nacional?.x?.[k] ?? 0;
    const w = Math.max(a, b, 0.01);
    return `<div class="comparow">
      <button type="button">${xLabels[k] || k}</button>
      <div class="track"><i style="width:${(100 * a) / w}%"></i></div>
      <b>${pct(a)}</b>
    </div>
    ${
      isNational(depto)
        ? ""
        : `<div class="comparow muted-row">
      <span>Nacional</span>
      <div class="track"><i class="nat" style="width:${(100 * b) / w}%"></i></div>
      <b>${pct(b)}</b>
    </div>`
    }`;
  });
  if (factorBox) {
    factorBox.innerHTML = rows.join("") || "<p class='muted'>Sin X en esta celda.</p>";
  }

  const listado = isNational(depto)
    ? "<p>Elige un departamento en el mapa para ver centros y direcci\u00f3n.</p>"
    : centers.length
      ? `<details><summary>Ver centros y direcci\u00f3n</summary><div class="cemlist">${centers
          .map(
            (c) =>
              `<p><b>${c.nombre}</b><br>${c.provincia} \u00b7 ${c.distrito}<br>${c.direccion || ""}</p>`
          )
          .join("")}</div></details>`
      : "";

  document.getElementById("cemterritory").innerHTML = `
    <b>CEM regulares en ${info.label}</b>
    <p>${centers.length ? `${centers.length} centros en el GeoJSON 2025.` : "Sin registros en esta base."}
    Periodo ${meta.cem.periodo}. No incluye horarios ni otras modalidades.</p>
    ${listado}
  `;

  document.getElementById("nextstep").innerHTML = `
    <b>Una respuesta posible para ${info.label}:</b>
    contrastar esta lectura (ENARES + oferta CEM) en la
    <a href="${IRC}" target="_blank" rel="noopener">Instancia Regional de Concertaci\u00f3n</a>,
    sin tratar el porcentaje ${isNational(depto) ? "nacional" : "departamental"} como meta de un colegio.
  `;
  document.getElementById("entities").innerHTML = ENTITIES.map(
    ([n, t, u]) =>
      `<div class="entity"><b>${n}</b><span>${t}<div class="contact"><a href="${u}" target="_blank" rel="noopener">Ver contacto institucional</a></div></span></div>`
  ).join("");
}

export function bindDiscover() {
  const btn = document.getElementById("discover");
  const list = document.getElementById("profilelist");
  btn.addEventListener("click", () => {
    list.hidden = !list.hidden;
    btn.setAttribute("aria-expanded", String(!list.hidden));
    btn.textContent = list.hidden
      ? "Descubrir m\u00e1s perfiles \u2192"
      : "Ocultar perfiles \u2191";
  });
}
