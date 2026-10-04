import { AGES, PERU, VIOLENCE } from "./config.js";
import { getState, setState } from "./state.js";

export function bindFilters(departamentos) {
  const $v = document.getElementById("violence");
  const $a = document.getElementById("age");
  const $d = document.getElementById("department");
  const state = getState();

  $v.innerHTML = VIOLENCE.map(
    (x) => `<option value="${x.id}" ${x.id === state.violence ? "selected" : ""}>${x.label}</option>`
  ).join("");
  $a.innerHTML = AGES.map(
    (x) => `<option value="${x.id}" ${x.id === state.age ? "selected" : ""}>${x.label}</option>`
  ).join("");
  $d.innerHTML = [
    `<option value="${PERU.key}" ${state.depto === PERU.key ? "selected" : ""}>${PERU.label}</option>`,
    ...departamentos.map(
      (x) =>
        `<option value="${x.key}" ${x.key === state.depto ? "selected" : ""}>${x.label}</option>`
    ),
  ].join("");

  $v.addEventListener("change", () => setState({ violence: $v.value }));
  $a.addEventListener("change", () => setState({ age: $a.value }));
  $d.addEventListener("change", () => setState({ depto: $d.value }));
}

export function syncFilters() {
  const s = getState();
  const $v = document.getElementById("violence");
  const $a = document.getElementById("age");
  const $d = document.getElementById("department");
  if ($v) $v.value = s.violence;
  if ($a) $a.value = s.age;
  if ($d) $d.value = s.depto;
}

export function bindRegionList(departamentos) {
  const box = document.getElementById("allregions");
  const paint = () => {
    const { depto } = getState();
    const chips = [
      { key: PERU.key, label: PERU.label },
      ...departamentos,
    ];
    box.innerHTML = chips
      .map(
        (x) =>
          `<button type="button" class="${x.key === depto ? "active" : ""}" data-key="${x.key}" aria-pressed="${x.key === depto}">${x.label}</button>`
      )
      .join("");
  };
  box.addEventListener("click", (ev) => {
    const btn = ev.target.closest("button[data-key]");
    if (btn) setState({ depto: btn.dataset.key });
  });
  return paint;
}
