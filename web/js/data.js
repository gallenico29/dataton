import { CACHE, DATA_BASE } from "./config.js";

async function load(name) {
  const url = new URL(name, DATA_BASE);
  url.searchParams.set("v", CACHE);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`No se pudo leer ${name} (${res.status})`);
  return res.json();
}

export async function loadAll() {
  const packed = globalThis.__DASHBOARD__;
  if (packed?.enares) return packed;
  const [meta, departamentos, enares, cem, perfiles, vivienda] = await Promise.all([
    load("meta.json"),
    load("departamentos.json"),
    load("enares.json"),
    load("cem.json"),
    load("perfiles.json"),
    load("vivienda.json"),
  ]);
  return { meta, departamentos, enares, cem, perfiles, vivienda };
}

export function sliceVivienda(vivienda, key) {
  const nacional = vivienda?.nacional || null;
  if (!key || key === "peru") {
    return { local: nacional, nacional };
  }
  return { local: vivienda?.por?.[key] || nacional, nacional };
}

export function sliceEnares(enares, key, age) {
  const dpto = enares.por[key] || null;
  return {
    local: dpto ? dpto[age] : null,
    nacional: enares.nacional[age],
  };
}
