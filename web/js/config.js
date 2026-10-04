export const DATA_BASE = new URL("../data/", import.meta.url);

export const VIOLENCE = [
  { id: "alguna", label: "Todas las violencias", noun: "alguna de las tres formas de violencia" },
  { id: "psic", label: "Violencia psicol\u00f3gica", noun: "violencia psicol\u00f3gica" },
  { id: "fis", label: "Violencia f\u00edsica", noun: "violencia f\u00edsica" },
  { id: "sex", label: "Violencia sexual", noun: "violencia sexual" },
];

export const AGES = [
  { id: "todas", label: "12-17 a\u00f1os" },
  { id: "12_14", label: "12-14 a\u00f1os" },
  { id: "15_17", label: "15-17 a\u00f1os" },
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
    "Coordinar atenci\u00f3n integral y derivaci\u00f3n. El cuadro MINSA adjunto no tiene territorio.",
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

export function fmtN(x) {
  if (x == null) return "\u2014";
  return Math.round(x).toLocaleString("es-PE");
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
