import { ENTITIES, IRC, NAMES, PERU, TAG_HELP, TAG_LABEL, VIOLENCE, factorLabel, isNational, pct, serviceSnapshot, yKey } from "./config.js";
import { sliceEnares, sliceVivienda } from "./data.js";
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

function personName(depto, departamentos) {
  if (isNational(depto)) return NAMES[0];
  const ix = departamentos.findIndex((d) => d.key === depto);
  return NAMES[(ix < 0 ? 0 : ix) % NAMES.length];
}

function personAge(age, profile) {
  if (age === "15_17") return 16;
  if (age === "12_14") return 14;
  if (profile?.edad) return Math.round(profile.edad);
  return 14;
}

function ageRange(age) {
  if (age === "12_14") return "12-14";
  if (age === "15_17") return "15-17";
  return "12-17";
}

function placeName(info, national) {
  return national ? "el Per\u00fa" : info.label;
}

function fnStar() {
  return `<a class="fn" href="#nota-metodologica" title="Nota metodol\u00f3gica: estas cifras son del m\u00f3dulo de mujeres de 18 a\u00f1os o m\u00e1s">*</a>`;
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function cleanProfileText(text) {
  return String(text || "")
    .replace(/\bn\s*=\s*[\d.,]+[:.]?/gi, "")
    .replace(/\bN\s*[~\u2248]?\s*[\d.,]+\s*(mil)?/gi, "")
    .replace(/\bcaj[o\u00f3]n chico[,.]?/gi, "")
    .replace(/No lo leas como un tipo de casa\.?/gi, "El algoritmo las junt\u00f3 por el tipo de escuela, no porque se parezcan en la casa.")
    .replace(/no un tipo de casa mixto\.?/gi, "no un perfil de hogar m\u00e1s amplio.")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([.,;:])/g, "$1")
    .trim();
}

function otherViolences(g, violence) {
  if (violence === "alguna") {
    return `En los \u00faltimos 12 meses reportaron violencia psicol\u00f3gica ${pct(g.psic)}, f\u00edsica ${pct(g.fis)} y sexual ${pct(g.sex)}.`;
  }
  const items = [];
  if (violence !== "psic") items.push(`psicol\u00f3gica ${pct(g.psic)}`);
  if (violence !== "fis") items.push(`f\u00edsica ${pct(g.fis)}`);
  if (violence !== "sex") items.push(`sexual ${pct(g.sex)}`);
  return `Adem\u00e1s, en los \u00faltimos 12 meses reportaron violencia ${items.join(" y ")}.`;
}

function bandLabel(band) {
  if (band === "alta") return "Presi\u00f3n alta sobre la oferta";
  if (band === "baja") return "Presi\u00f3n baja sobre la oferta";
  if (band === "media") return "Presi\u00f3n media sobre la oferta";
  return "Oferta nacional";
}

function bandHelp(band) {
  if (band === "alta") {
    return "Junta la prevalencia de esta violencia y cu\u00e1ntos CEM hay por 100 mil alumnas. Alta: este departamento queda en el tercio m\u00e1s tensionado (m\u00e1s violencia y/o menos centros que el resto).";
  }
  if (band === "baja") {
    return "Junta la prevalencia de esta violencia y cu\u00e1ntos CEM hay por 100 mil alumnas. Baja: este departamento queda en el tercio m\u00e1s holgado (menos violencia y/o m\u00e1s centros que el resto).";
  }
  if (band === "media") {
    return "Junta la prevalencia de esta violencia y cu\u00e1ntos CEM hay por 100 mil alumnas. Media: queda a mitad de tabla, ni de los m\u00e1s holgados ni de los m\u00e1s tensionados.";
  }
  return "Vista nacional. Elige un departamento para ver si su oferta CEM est\u00e1 holgada o tensionada frente al resto del pa\u00eds.";
}

function barWidth(v) {
  if (v == null || Number.isNaN(v)) return 0;
  return Math.max(0, Math.min(100, v * 100));
}

function barRow(label, value) {
  return `<div class="barrow">
    <span class="barlab">${escapeHtml(label)}</span>
    <div class="bartrack" aria-hidden="true"><i style="width:${barWidth(value).toFixed(1)}%"></i></div>
    <span class="barval">${pct(value)}</span>
  </div>`;
}

function pairRow(label, todas, subgrupo, labTodas, labSub) {
  return `<div class="cmp">
    <span class="barlab">${escapeHtml(label)}</span>
    <div class="cmpline">
      <em>${escapeHtml(labTodas)}</em>
      <div class="bartrack"><i class="t" style="width:${barWidth(todas).toFixed(1)}%"></i></div>
      <b>${pct(todas)}</b>
    </div>
    <div class="cmpline">
      <em>${escapeHtml(labSub)}</em>
      <div class="bartrack"><i class="y" style="width:${barWidth(subgrupo).toFixed(1)}%"></i></div>
      <b>${pct(subgrupo)}</b>
    </div>
  </div>`;
}

function ppVs(si, all) {
  if (si == null || all == null || Number.isNaN(si) || Number.isNaN(all)) return "";
  const d = (si - all) * 100;
  if (Math.abs(d) < 0.8) return "casi igual que el conjunto";
  return `${d > 0 ? "+" : ""}${d.toFixed(1)} pp vs el conjunto`;
}

function renderTag(name) {
  const shown = TAG_LABEL[name] || name;
  const help = TAG_HELP[name] || TAG_HELP[shown];
  if (!help) return `<span class="tag">${escapeHtml(shown)}</span>`;
  return `<span class="tag" tabindex="0">
    ${escapeHtml(shown)}
    <span class="tip" role="tooltip">${escapeHtml(help)}</span>
  </span>`;
}

export function renderPanel(bundle) {
  const { meta, departamentos, enares, cem, vivienda } = bundle;
  const { depto, age, violence } = getState();
  const info = infoDepto(departamentos, depto);
  const { local: sliceLocal, nacional } = sliceEnares(enares, depto, age);
  const local = isNational(depto) ? nacional : sliceLocal;
  const centers = isNational(depto)
    ? Object.values(cem).filter(Array.isArray).flat()
    : cem[depto] || [];
  const y = yKey(violence);
  const vMeta = VIOLENCE.find((v) => v.id === violence);
  const vlab = vMeta?.noun || "";
  const vTitle = vMeta?.label || "";
  const ageLab = ageRange(age);
  const groups = bundle.perfiles?.por?.[violence] || [];
  const top = groups[0];
  const name = personName(depto, departamentos);
  const years = personAge(age, top);
  const national = isNational(depto);
  const x = local?.x || {};
  const xSi = local?.x_si?.[violence] || {};
  const locY = local?.[y];
  const labAll18 = "Todas las mujeres 18+";
  const labSub18 = "Subgrupo: violencia de pareja";
  const labAllAlu = "Todas las alumnas";
  const labSubAlu = `Las que reportaron ${vlab}`;

  const lugar = placeName(info, national);
  document.getElementById("title").textContent = `Conoce a ${name}`;
  const asideTitle = document.querySelector("aside.card > h2");
  if (asideTitle) asideTitle.textContent = info?.label || depto;

  document.getElementById("story").innerHTML = `
    <strong>${name} tiene ${years} a\u00f1os y estudia en ${lugar}.</strong>
    En su hogar hay discusiones y siente que su opini\u00f3n pocas veces es escuchada.
    Tambi\u00e9n pasa parte del d\u00eda sin compa\u00f1\u00eda adulta.
    <br><br>
    El perfil sale de alumnas de ${ageLab} a\u00f1os en ENARES que m\u00e1s concentran <strong>${vlab}</strong>,
    no de la violencia reportada por mujeres de 18 a\u00f1os o m\u00e1s.
    Esa encuesta solo describe el territorio (luz, agua, desag\u00fce).
    <span class="fiction">${name} es ilustrativa, no una alumna identificada.</span>
  `;

  const svc = serviceSnapshot(departamentos, enares, age, y, depto);
  const locSvc = svc.local || {};
  const densTxt = locSvc.per100k != null ? locSvc.per100k.toFixed(1) : "\u2014";
  const viv = sliceVivienda(vivienda, depto).local || {};
  const vivAll = viv.todas || {};
  const vivY = viv.con_violencia || {};

  document.getElementById("stats").innerHTML = `
    <div class="stat">
      <b>${pct(locY)}</b>
      <span>${vTitle}</span>
      <span>Adolescentes ${ageLab} a\u00f1os \u00b7 ${info.label}</span>
    </div>
    <div class="stat">
      <b>${pct(vivAll.elec)}</b>
      <span>Electricidad ${fnStar()}</span>
      <span>Mujeres 18 a\u00f1os o m\u00e1s \u00b7 ${info.label}</span>
    </div>
    <div class="stat">
      <b>${pct(vivAll.agua)}</b>
      <span>Agua de red ${fnStar()}</span>
      <span>Mujeres 18 a\u00f1os o m\u00e1s \u00b7 ${info.label}</span>
    </div>
  `;

  const dNet = vivY.internet != null && vivAll.internet != null
    ? (vivY.internet - vivAll.internet) * 100
    : null;
  const leadCom =
    dNet != null && Math.abs(dNet) >= 0.8
      ? `Las mujeres con violencia de pareja tienen ${Math.abs(dNet).toFixed(1)} pp ${dNet < 0 ? "menos" : "m\u00e1s"} internet que el conjunto del departamento.`
      : "";
  const leadRel = xSi.se_queda_sola != null
    ? `De las adolescentes que reportaron ${vlab}, ${pct(xSi.se_queda_sola)} se queda sola (${ppVs(xSi.se_queda_sola, x.se_queda_sola)}) y ${pct(xSi.peleas_casa)} vive peleas en casa (${ppVs(xSi.peleas_casa, x.peleas_casa)}).`
    : "";
  const leadInd = xSi.act_padres_golpear != null
    ? `De las que reportaron ${vlab}, ${pct(xSi.act_padres_golpear)} cree que los padres pueden golpear (${ppVs(xSi.act_padres_golpear, x.act_padres_golpear)}).`
    : "";

  document.getElementById("ecological").innerHTML = `
    <div class="areas-head">
      <strong>Indicadores por nivel ecol\u00f3gico</strong>
      <p class="muted">En cada bloque se ve el conjunto y el subgrupo con violencia. Comunitario: mujeres 18+. Relacional e individual: adolescentes ${ageLab} a\u00f1os.</p>
    </div>
    <div class="areas">
      <div class="area servicios">
        <strong>Comunitario <small>Servicios de vivienda ${fnStar()}</small></strong>
        <p class="pop">Mujeres de 18 a\u00f1os o m\u00e1s en ${info.label}</p>
        ${leadCom ? `<p class="lead">${leadCom}</p>` : ""}
        ${pairRow("Electricidad", vivAll.elec, vivY.elec, labAll18, labSub18)}
        ${pairRow("Agua de red", vivAll.agua, vivY.agua, labAll18, labSub18)}
        ${pairRow("Desag\u00fce", vivAll.desague, vivY.desague, labAll18, labSub18)}
        ${pairRow("Internet", vivAll.internet, vivY.internet, labAll18, labSub18)}
        <div class="cembox">
          <div><b>${centers.length || 0}</b><span>CEM</span></div>
          <div><b>${densTxt}</b><span>por 100 mil</span></div>
        </div>
        <span class="badge ${locSvc.band || "pais"}" tabindex="0">${bandLabel(locSvc.band)}<span class="tip" role="tooltip">${bandHelp(locSvc.band)}</span></span>
        <p class="note">Dos poblaciones, no un desglose: todas las mujeres del departamento y el subgrupo que report\u00f3 violencia de pareja. Luz, agua, desag\u00fce e internet no suman 100%.${fnStar()}</p>
      </div>
      <div class="area barreras">
        <strong>Relacional <small>Hogar y escuela</small></strong>
        <p class="pop">Adolescentes ${ageLab} a\u00f1os en ${info.label}</p>
        ${leadRel ? `<p class="lead">${leadRel}</p>` : ""}
        ${pairRow("Peleas en casa", x.peleas_casa, xSi.peleas_casa, labAllAlu, labSubAlu)}
        ${pairRow("Se queda sola", x.se_queda_sola, xSi.se_queda_sola, labAllAlu, labSubAlu)}
        ${pairRow("Falta al colegio", x.falta_colegio, xSi.falta_colegio, labAllAlu, labSubAlu)}
        ${pairRow("Se siente mal", x.se_siente_mal, xSi.se_siente_mal, labAllAlu, labSubAlu)}
        <p class="note">La barra de arriba es el conjunto de alumnas. La de abajo es solo las que reportaron ${vlab}. Los \u00edtems no suman 100%.</p>
      </div>
      <div class="area creencias">
        <strong>Individual <small>Creencias</small></strong>
        <p class="pop">Adolescentes ${ageLab} a\u00f1os en ${info.label}</p>
        ${leadInd ? `<p class="lead">${leadInd}</p>` : ""}
        ${pairRow("Cree que los padres pueden golpear", x.act_padres_golpear, xSi.act_padres_golpear, labAllAlu, labSubAlu)}
        ${pairRow("Cree que puede dejar el colegio", x.act_deje_colegio, xSi.act_deje_colegio, labAllAlu, labSubAlu)}
        <p class="note">Misma lectura: conjunto vs las que reportaron ${vlab}. Una alumna puede coincidir en las dos creencias.</p>
      </div>
    </div>
  `;

  const profileTitle = document.getElementById("profiletitle");
  const profileLead = document.getElementById("profilelead");
  if (profileTitle) profileTitle.textContent = `Perfiles de ${vlab}`;
  if (profileLead) {
    profileLead.textContent =
      `Tres grupos de alumnas que s\u00ed reportaron ${vlab}. El #1 junta m\u00e1s factores de riesgo. Pasa el cursor sobre una etiqueta para ver qu\u00e9 pregunta es.`;
  }

  document.getElementById("profiles").innerHTML = groups
    .map((g, i) => {
      const aviso =
        g.chico && !/grupo peque/i.test(g.texto || "")
          ? " Este grupo es peque\u00f1o: no alcanza para armar una pol\u00edtica."
          : "";
      const titulo = String(g.titulo || "").replace(/\s*\(n chico\)/i, " (grupo peque\u00f1o)");
      return `<article class="profile${g.chico ? " chico" : ""}">
      <span class="rank">#${i + 1}</span>
      <div>
        <h3>${escapeHtml(titulo)}</h3>
        <p>Adolescentes mujeres de ${ageLab} a\u00f1os en ${info.label}.${aviso} ${escapeHtml(cleanProfileText(g.texto))}</p>
        <div class="tags">${(g.tags || []).map(renderTag).join("")}</div>
        <div class="detail">
          Edad media: ${g.edad.toFixed(1)} a\u00f1os.<br>
          ${otherViolences(g, violence)}
        </div>
      </div>
    </article>`;
    })
    .join("");

  const xLabels = meta.x_labels || {};
  const keys = Object.keys(nacional?.x || {});
  const factorBox = document.getElementById("factors");
  const hint = document.getElementById("factorhint");
  const rows = keys
    .map((k) => {
      const here = local?.x?.[k] ?? 0;
      const pais = nacional?.x?.[k] ?? 0;
      return { k, here, pais, d: here - pais };
    })
    .sort((a, b) => (national ? b.here - a.here : Math.abs(b.d) - Math.abs(a.d)));
  if (hint) {
    hint.textContent = national
      ? "En la vista nacional no hay contra qui\u00e9n comparar. Las barras muestran qu\u00e9 tan frecuente es cada factor en el pa\u00eds."
      : "Barras en la misma escala (0 a 100). Arriba van los que m\u00e1s se alejan del promedio nacional.";
  }
  if (factorBox) {
    factorBox.innerHTML =
      rows
        .map((r) => {
          const lab = escapeHtml(factorLabel(r.k, xLabels));
          if (national) {
            return `<div class="gaprow">
              <div class="gaphead"><span>${lab}</span></div>
              <div class="gline">
                <em>Pa\u00eds</em>
                <div class="track"><i style="width:${barWidth(r.here).toFixed(1)}%"></i></div>
                <b>${pct(r.here)}</b>
              </div>
            </div>`;
          }
          const cls = r.d > 0.008 ? "up" : r.d < -0.008 ? "down" : "same";
          const gap =
            cls === "same"
              ? "Igual al pa\u00eds"
              : `${r.d > 0 ? "+" : ""}${(r.d * 100).toFixed(1)} pp vs pa\u00eds`;
          return `<div class="gaprow">
            <div class="gaphead">
              <span>${lab}</span>
              <span class="gap ${cls}">${gap}</span>
            </div>
            <div class="gline">
              <em>Aqu\u00ed</em>
              <div class="track"><i style="width:${barWidth(r.here).toFixed(1)}%"></i></div>
              <b>${pct(r.here)}</b>
            </div>
            <div class="gline nat">
              <em>Pa\u00eds</em>
              <div class="track"><i style="width:${barWidth(r.pais).toFixed(1)}%"></i></div>
              <b>${pct(r.pais)}</b>
            </div>
          </div>`;
        })
        .join("") || "<p class='muted'>No hay factores para comparar aqu\u00ed.</p>";
  }

  const listado = national
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
    <p>${centers.length ? `${centers.length} centros en el archivo 2025.` : "Sin registros en esta base."}
    Per\u00edodo ${meta.cem.periodo}. No incluye horarios ni otras modalidades.</p>
    ${listado}
  `;

  document.getElementById("nextstep").innerHTML = `
    Para ${info.label}: MIMP con familias y escuela con convivencia.
    La <a href="${IRC}" target="_blank" rel="noopener">Instancia Regional de Concertaci\u00f3n</a>
    puede acordar responsables.
  `;
  document.getElementById("entities").innerHTML = ENTITIES.map(
    ([n, t, u]) =>
      `<div class="entity"><b>${n}</b><span>${t}</span><div class="contact"><a href="${u}" target="_blank" rel="noopener">Ver contacto institucional</a></div></div>`
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
