import { loadAll } from "./data.js";
import { bindDiscover, renderPanel } from "./panel.js";
import { bindFilters, bindRegionList, syncFilters } from "./filters.js";
import { initMap } from "./map.js";
import { subscribe } from "./state.js";

async function boot() {
  const bundle = await loadAll();
  bindFilters(bundle.departamentos);
  const paintRegions = bindRegionList(bundle.departamentos);
  bindDiscover();
  const paintMap = await initMap(bundle.departamentos, bundle.enares);

  const paint = () => {
    syncFilters();
    paintRegions();
    renderPanel(bundle);
    paintMap();
  };
  subscribe(paint);
  paint();
}

boot().catch((err) => {
  document.getElementById("title").textContent = "No se pudieron cargar los datos";
  document.getElementById("story").textContent =
    `${err.message}. Abre tablero.html o corre python web/serve.py.`;
});
