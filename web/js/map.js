import { DATA_BASE, PERU, isNational, pct, slugDepto, yKey } from "./config.js";
import { getState, setState } from "./state.js";

let map;
let cemLayer;
let deptoLayer;
let labelLayer;
let geo;
let lastDepto = null;
let hoverTip;
let legendScale;

function colorRamp(t) {
  const stops = [
    [0, 232, 241, 244],
    [0.25, 168, 206, 214],
    [0.5, 86, 163, 179],
    [0.75, 28, 110, 132],
    [1, 12, 58, 78],
  ];
  const x = Math.min(1, Math.max(0, t));
  let a = stops[0];
  let b = stops[stops.length - 1];
  for (let i = 0; i < stops.length - 1; i += 1) {
    if (x >= stops[i][0] && x <= stops[i + 1][0]) {
      a = stops[i];
      b = stops[i + 1];
      break;
    }
  }
  const u = (x - a[0]) / (b[0] - a[0] || 1);
  const rgb = [1, 2, 3].map((i) => Math.round(a[i] + (b[i] - a[i]) * u));
  return `rgb(${rgb.join(",")})`;
}

function deptoKey(props, departamentos) {
  const code = String(props.FIRST_IDDP || "").padStart(2, "0");
  const hit = departamentos.find((d) => d.code === code);
  if (hit) return hit.key;
  return slugDepto(props.NOMBDEP);
}

function rangeVals(departamentos, enares) {
  const { age, violence } = getState();
  const y = yKey(violence);
  const vals = departamentos
    .map((d) => enares.por[d.key]?.[age]?.[y])
    .filter((v) => v != null);
  const lo = vals.length ? Math.min(...vals) : 0;
  const hi = vals.length ? Math.max(...vals) : 1;
  return { lo, hi, y };
}

function labelOffset(key, latlng) {
  if (key === "callao") return L.latLng(latlng.lat - 0.18, latlng.lng - 0.55);
  if (key === "lima") return L.latLng(latlng.lat + 0.35, latlng.lng - 0.15);
  return latlng;
}

export async function initMap(departamentos, enares) {
  const el = document.getElementById("leaflet");
  map = L.map(el, {
    scrollWheelZoom: true,
    zoomControl: false,
    minZoom: 5,
    maxZoom: 12,
    attributionControl: false,
    zoomSnap: 0.25,
  }).setView([-9.25, -74.9], 5.35);

  map.createPane("deptos");
  map.getPane("deptos").style.zIndex = 350;
  map.createPane("cem");
  map.getPane("cem").style.zIndex = 450;
  map.createPane("labels");
  map.getPane("labels").style.zIndex = 460;
  map.getPane("labels").style.pointerEvents = "none";

  L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
    { maxZoom: 16, opacity: 0.72 }
  ).addTo(map);

  hoverTip = L.tooltip({ sticky: true, className: "map-tip", opacity: 1 });

  const [deptoRes, cemRes] = await Promise.all([
    fetch(new URL("peru_departamentos.geojson", DATA_BASE)),
    fetch(new URL("cem.geojson", DATA_BASE)),
  ]);
  const deptoGeo = await deptoRes.json();
  geo = await cemRes.json();

  deptoLayer = L.geoJSON(deptoGeo, {
    pane: "deptos",
    style: () => ({
      color: "#f7fbfc",
      weight: 1.1,
      fillColor: "#d5e6eb",
      fillOpacity: 0.88,
    }),
    onEachFeature: (feat, layer) => {
      const key = deptoKey(feat.properties, departamentos);
      layer.on("click", () => setState({ depto: key }));
      layer.on("mouseover", (ev) => {
        if (getState().depto !== key) {
          layer.setStyle({ weight: 2, color: "#163d52", fillOpacity: 0.95 });
        }
        layer.bringToFront();
        const info = departamentos.find((d) => d.key === key);
        const { age, violence } = getState();
        const val = enares.por[key]?.[age]?.[yKey(violence)];
        hoverTip
          .setLatLng(ev.latlng)
          .setContent(
            `<b>${info?.label || feat.properties.NOMBDEP}</b><br>${pct(val)} \u00b7 ${info?.n_cem ?? 0} CEM`
          )
          .addTo(map);
      });
      layer.on("mousemove", (ev) => hoverTip.setLatLng(ev.latlng));
      layer.on("mouseout", () => {
        hoverTip.remove();
        paintDeptos(departamentos, enares);
      });
    },
  }).addTo(map);

  labelLayer = L.layerGroup().addTo(map);
  deptoLayer.eachLayer((layer) => {
    const key = deptoKey(layer.feature.properties, departamentos);
    const info = departamentos.find((d) => d.key === key);
    const center = labelOffset(key, layer.getBounds().getCenter());
    const marker = L.marker(center, {
      pane: "labels",
      interactive: false,
      keyboard: false,
      icon: L.divIcon({
        className: "depto-label",
        html: `<span>${info?.label || layer.feature.properties.NOMBDEP}</span>`,
        iconSize: [92, 16],
        iconAnchor: [46, 8],
      }),
    });
    labelLayer.addLayer(marker);
  });

  cemLayer = L.geoJSON(geo, {
    pane: "cem",
    pointToLayer: (_f, latlng) =>
      L.circleMarker(latlng, {
        radius: 3.4,
        color: "#142d49",
        weight: 1,
        fillColor: "#efba57",
        fillOpacity: 0.95,
      }),
    onEachFeature: (feat, layer) => {
      const p = feat.properties;
      layer.bindPopup(
        `<div class="cem-pop"><b>${p.nombre}</b><br>${p.provincia} \u00b7 ${p.distrito}<br><small>${p.direccion || ""}</small></div>`
      );
      layer.on("click", () => {
        if (p.key) setState({ depto: p.key });
      });
    },
  }).addTo(map);

  const legend = L.control({ position: "bottomleft" });
  legend.onAdd = () => {
    const box = L.DomUtil.create("div", "map-legend");
    box.innerHTML = `
      <div class="lg-title">Prevalencia ENARES</div>
      <div class="lg-bar"></div>
      <div class="lg-scale"><span>menor</span><span>mayor</span></div>
      <div class="lg-row"><i class="dot"></i> CEM regular 2025</div>
    `;
    legendScale = box.querySelector(".lg-scale");
    return box;
  };
  legend.addTo(map);

  L.control.zoom({ position: "topright" }).addTo(map);
  const reset = L.control({ position: "topright" });
  reset.onAdd = () => {
    const btn = L.DomUtil.create("button", "map-reset");
    btn.type = "button";
    btn.textContent = PERU.label;
    btn.title = "Ver todo el pa\u00eds";
    btn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      setState({ depto: PERU.key });
    });
    return btn;
  };
  reset.addTo(map);

  map.on("zoomend", () => {
    const z = map.getZoom();
    if (labelLayer) {
      labelLayer.eachLayer((m) => {
        const el = m.getElement();
        if (el) el.classList.toggle("is-hidden", z >= 8.2);
      });
    }
  });

  requestAnimationFrame(() => map.invalidateSize());
  paintDeptos(departamentos, enares);
  return () => focusMap(departamentos, enares);
}

function paintDeptos(departamentos, enares) {
  if (!deptoLayer) return;
  const { depto } = getState();
  const { lo, hi, y } = rangeVals(departamentos, enares);
  const { age } = getState();
  if (legendScale) {
    legendScale.innerHTML = `<span>${pct(lo)}</span><span>${pct(hi)}</span>`;
  }

  deptoLayer.eachLayer((layer) => {
    const key = deptoKey(layer.feature.properties, departamentos);
    const val = enares.por[key]?.[age]?.[y];
    const t = val == null || hi === lo ? 0.15 : (val - lo) / (hi - lo);
    const selected = !isNational(depto) && key === depto;
    layer.setStyle({
      fillColor: colorRamp(t),
      fillOpacity: selected ? 0.97 : isNational(depto) ? 0.82 : 0.62,
      color: selected ? "#c2410c" : "#f4f8fa",
      weight: selected ? 2.6 : 1.05,
    });
    if (selected) layer.bringToFront();
  });
}

function fitPeru(animate) {
  if (!deptoLayer) return;
  map.invalidateSize();
  map.fitBounds(deptoLayer.getBounds().pad(0.12), { animate: !!animate, duration: 0.55 });
}

export function focusMap(departamentos, enares) {
  if (!map || !geo) return;
  paintDeptos(departamentos, enares);
  const { depto } = getState();
  const national = isNational(depto);
  const info = departamentos.find((d) => d.key === depto);

  cemLayer.eachLayer((layer) => {
    const k = layer.feature?.properties?.key;
    const on = !national && k === depto;
    layer.setStyle({
      fillColor: on ? "#c2410c" : "#efba57",
      color: on ? "#7f1d1d" : "#142d49",
      radius: on ? 6.2 : national ? 3.5 : 3,
      fillOpacity: on ? 1 : national ? 0.9 : 0.45,
      weight: on ? 1.4 : 1,
    });
    if (on) layer.bringToFront();
  });

  if (lastDepto === depto) return;
  const first = lastDepto == null;
  lastDepto = depto;

  if (national) {
    fitPeru(!first);
    return;
  }
  const layer = deptoLayer
    .getLayers()
    .find((l) => deptoKey(l.feature.properties, departamentos) === depto);
  if (layer) {
    map.fitBounds(layer.getBounds().pad(0.14), { maxZoom: 8, animate: true, duration: 0.55 });
    return;
  }
  if (info?.centro?.lat != null) map.setView([info.centro.lat, info.centro.lon], 7);
}
