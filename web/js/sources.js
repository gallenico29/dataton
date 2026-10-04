import { fmtN } from "./config.js";

export function renderSources({ salud, mp, meta }) {
  const box = document.getElementById("admin-tables");
  const row = (r) =>
    `<tr><td>${r.indicador}</td><td>${fmtN(r.mujer)}</td><td>${fmtN(r.hombre)}</td><td>${fmtN(r.total ?? r.lugar)}</td></tr>`;

  box.innerHTML = `
    <details>
      <summary>MINSA (cuadro adjunto) \u2014 no tiene territorio</summary>
      <p>${salud.ambito} ${salud.nota}</p>
      <div class="tablewrap"><table>
        <thead><tr><th>Indicador</th><th>Mujer</th><th>Hombre</th><th>Total</th></tr></thead>
        <tbody>${(salud.filas || []).map(row).join("")}</tbody>
      </table></div>
    </details>
    <details>
      <summary>Ministerio P\u00fablico 2026 \u2014 varias filas en Ca\u00f1ete</summary>
      <p>${mp.ambito} ${mp.nota}</p>
      <div class="tablewrap"><table>
        <thead><tr><th>Indicador</th><th>Mujer</th><th>Hombre</th><th>Lugar / total</th></tr></thead>
        <tbody>${(mp.filas || [])
          .map(
            (r) =>
              `<tr><td>${r.indicador}</td><td>${fmtN(r.mujer)}</td><td>${fmtN(r.hombre)}</td><td>${r.lugar || "\u2014"}</td></tr>`
          )
          .join("")}</tbody>
      </table></div>
    </details>
    <details>
      <summary>INEI Sheet1 \u2014 no entra al perfil</summary>
      <p>${meta.fuentes_fuera?.inei_its || ""}</p>
    </details>
  `;
}
