export const DATA_BASE = new URL("../data/", import.meta.url);
export const CACHE = "20261021";

export const VIOLENCE = [
  { id: "sex", label: "Violencia sexual", noun: "violencia sexual" },
  { id: "fis", label: "Violencia f\u00edsica", noun: "violencia f\u00edsica" },
  { id: "psic", label: "Violencia psicol\u00f3gica", noun: "violencia psicol\u00f3gica" },
  {
    id: "alguna",
    label: "Al menos una violencia (f\u00edsica, psicol\u00f3gica o sexual)",
    noun: "al menos una violencia (f\u00edsica, psicol\u00f3gica o sexual)",
  },
];

export const NAMES = ["Luc\u00eda", "Camila", "Valeria", "Mariana", "Daniela"];

export const TAG_HELP = {
  Actitudes:
    "Creencias de la alumna: si los padres pueden golpear, si ella debe trabajar o dejar el colegio.",
  Hogar: "Situaci\u00f3n en casa: peleas, si la escuchan y si se queda sola.",
  Trabajo: "Si acepta que, cuando falta plata, ella debe trabajar.",
  Escuela: "Malestar en el colegio o tipo de instituci\u00f3n educativa.",
  "IE mujeres": "La escuela es un colegio solo de mujeres.",
  "Colegio de mujeres": "La escuela es un colegio solo de mujeres.",
  Participaci\u00f3n: "Si la toman en cuenta en las decisiones del hogar.",
  Composici\u00f3n: "Con qui\u00e9n vive (por ejemplo, con un t\u00edo).",
  Castigo: "Si acepta que los padres tienen derecho a golpear.",
};

export const AGES = [
  { id: "todas", label: "Todas: 12-17 a\u00f1os" },
  { id: "12_14", label: "Rango 1: 12-14 a\u00f1os" },
  { id: "15_17", label: "Rango 2: 15-17 a\u00f1os" },
];

export const ENTITIES = [
  [
    "MIMP / Warmi \u00d1an",
    "Articular prevenci\u00f3n con familias y revisar las rutas hacia los CEM del territorio.",
    "https://www.gob.pe/institucion/warmi%C3%B1an/contacto-y-numeros-de-emergencias",
  ],
  [
    "MIMP / DGCVG y DGNNA",
    "Coordinar prevenci\u00f3n y protecci\u00f3n con los factores familiares y las actitudes medidas.",
    "https://www.gob.pe/institucion/mimp/funcionarios",
  ],
  [
    "MINEDU / DRE / UGEL",
    "Trabajar convivencia, continuidad educativa y redes de apoyo con las escuelas.",
    "https://www.gob.pe/institucion/minedu/contacto-y-numeros-de-emergencias",
  ],
  [
    "MINSA / red de salud",
    "Coordinar atenci\u00f3n integral y derivaci\u00f3n.",
    "https://www.gob.pe/institucion/minsa/contacto-y-numeros-de-emergencias",
  ],
];

export const IRC =
  "https://observatorioviolencia.pe/sistema-nacional/irc/";

export const PERU = {
  key: "peru",
  label: "Per\u00fa",
};

export function yKey(violence) {
  if (violence === "psic") return "psic";
  if (violence === "fis") return "fis";
  if (violence === "sex") return "sex";
  return "alguna";
}

export function pct(x) {
  if (x == null || Number.isNaN(x)) return "\u2014";
  return `${(100 * x).toFixed(1)} %`;
}

export function slugDepto(text) {
  return String(text || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "");
}

export function isNational(depto) {
  return !depto || depto === "peru";
}

export const X_LABELS = {
  toma_en_cuenta: "La toman en cuenta",
  peleas_casa: "Peleas en casa",
  se_queda_sola: "Se queda sola",
  se_siente_mal: "Se siente mal en el colegio",
  act_padres_golpear: "Cree que los padres pueden golpear",
  act_deje_colegio: "Cree que puede dejar el colegio",
  falta_colegio: "Falta al colegio para ayudar",
};

export const TAG_LABEL = {
  "IE mujeres": "Colegio de mujeres",
};

export function factorLabel(key, extra) {
  return (extra && extra[key]) || X_LABELS[key] || "Este factor";
}

function norm01(v, lo, hi) {
  if (hi === lo) return 0.5;
  return (v - lo) / (hi - lo);
}

export function serviceSnapshot(departamentos, enares, age, y, deptoKey) {
  const nat = enares.nacional[age] || {};
  const natCem = departamentos.reduce((s, d) => s + (d.n_cem || 0), 0);
  const natN = nat.N || 0;
  const natPer100k = natN > 0 ? (100000 * natCem) / natN : 0;

  const rows = departamentos.map((d) => {
    const sl = enares.por[d.key]?.[age] || {};
    const N = sl.N || 0;
    const prev = sl[y];
    const cem = d.n_cem || 0;
    const per100k = N > 0 ? (100000 * cem) / N : 0;
    return { key: d.key, prev, per100k };
  });

  const prevs = rows.map((r) => r.prev).filter((v) => v != null);
  const minP = Math.min(...prevs);
  const maxP = Math.max(...prevs);
  const minD = Math.min(...rows.map((r) => r.per100k));
  const maxD = Math.max(...rows.map((r) => r.per100k));
  for (const r of rows) {
    const np = r.prev == null ? 0.5 : norm01(r.prev, minP, maxP);
    const nd = 1 - norm01(r.per100k, minD, maxD);
    r.pressure = 0.5 * np + 0.5 * nd;
  }
  const ranked = [...rows].sort((a, b) => a.pressure - b.pressure);
  const bandOf = (key) => {
    const i = ranked.findIndex((r) => r.key === key);
    if (i < 0) return "media";
    if (i < ranked.length / 3) return "baja";
    if (i < (2 * ranked.length) / 3) return "media";
    return "alta";
  };

  const national = !deptoKey || deptoKey === "peru";
  return {
    local: national
      ? { per100k: natPer100k, band: null }
      : { ...rows.find((r) => r.key === deptoKey), band: bandOf(deptoKey) },
  };
}
