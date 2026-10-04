import { DATA_BASE } from "./config.js";

async function load(name) {
  const res = await fetch(new URL(name, DATA_BASE));
  if (!res.ok) throw new Error(`No se pudo leer ${name} (${res.status})`);
  return res.json();
}

export async function loadAll() {
  const [meta, departamentos, enares, cem, salud, mp, perfiles] = await Promise.all([
    load("meta.json"),
    load("departamentos.json"),
    load("enares.json"),
    load("cem.json"),
    load("salud.json"),
    load("mp.json"),
    load("perfiles.json"),
  ]);
  return { meta, departamentos, enares, cem, salud, mp, perfiles };
}

export function sliceEnares(enares, key, age) {
  const dpto = enares.por[key] || null;
  return {
    local: dpto ? dpto[age] : null,
    nacional: enares.nacional[age],
  };
}
