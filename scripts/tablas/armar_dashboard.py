# -*- coding: utf-8 -*-
"""Prepara JSON/GeoJSON limpios para el dashboard (web/data/).

Lee:
  - data/tablas/crs04_modelo.parquet          ENARES CRS04
  - data/CEM Regulares (2025).geojson
  - data/CUADRO DE VIOLENCIA FAMILIAR(SALUD).csv
  - data/ESTADISTICA2026(MP).csv
  - data/INEI(Sheet1).csv                     solo metadato: no entra al perfil

Uso:
    python scripts/tablas/procesar_crs04.py
    python scripts/tablas/armar_dashboard.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_MODELO, ROOT, WEB_DATA

CRUDOS_EXTRA = ROOT / "data"
CEM_GEO = CRUDOS_EXTRA / "CEM Regulares (2025).geojson"
SALUD_CSV = CRUDOS_EXTRA / "CUADRO DE VIOLENCIA FAMILIAR(SALUD).csv"
MP_CSV = CRUDOS_EXTRA / "ESTADISTICA2026(MP).csv"
INEI_CSV = CRUDOS_EXTRA / "INEI(Sheet1).csv"

X_CTX = [
    "toma_en_cuenta",
    "peleas_casa",
    "se_queda_sola",
    "se_siente_mal",
    "act_padres_golpear",
    "act_deje_colegio",
    "falta_colegio",
]

X_LABELS = {
    "toma_en_cuenta": "La toman en cuenta",
    "peleas_casa": "Peleas en casa",
    "se_queda_sola": "Se queda sola",
    "se_siente_mal": "Se siente mal en el colegio",
    "act_padres_golpear": "Actitud: padres pueden golpear",
    "act_deje_colegio": "Actitud: deje el colegio",
    "falta_colegio": "Falta al colegio para ayudar",
}

DEPTOS = [
    ("01", "AMAZONAS", "Amazonas"),
    ("02", "ANCASH", "Ancash"),
    ("03", "APURIMAC", "Apurimac"),
    ("04", "AREQUIPA", "Arequipa"),
    ("05", "AYACUCHO", "Ayacucho"),
    ("06", "CAJAMARCA", "Cajamarca"),
    ("07", "CALLAO", "Callao"),
    ("08", "CUSCO", "Cusco"),
    ("09", "HUANCAVELICA", "Huancavelica"),
    ("10", "HUANUCO", "Huanuco"),
    ("11", "ICA", "Ica"),
    ("12", "JUNIN", "Junin"),
    ("13", "LA LIBERTAD", "La Libertad"),
    ("14", "LAMBAYEQUE", "Lambayeque"),
    ("15", "LIMA", "Lima"),
    ("16", "LORETO", "Loreto"),
    ("17", "MADRE DE DIOS", "Madre de Dios"),
    ("18", "MOQUEGUA", "Moquegua"),
    ("19", "PASCO", "Pasco"),
    ("20", "PIURA", "Piura"),
    ("21", "PUNO", "Puno"),
    ("22", "SAN MARTIN", "San Martin"),
    ("23", "TACNA", "Tacna"),
    ("24", "TUMBES", "Tumbes"),
    ("25", "UCAYALI", "Ucayali"),
]

LABEL_UI = {
    "ancash": "\u00c1ncash",
    "apurimac": "Apur\u00edmac",
    "huanuco": "Hu\u00e1nuco",
    "junin": "Jun\u00edn",
    "san_martin": "San Mart\u00edn",
}


def slug(text: str) -> str:
    t = unicodedata.normalize("NFD", str(text))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")


def wmean(s: pd.Series, w: pd.Series) -> float | None:
    m = s.notna() & w.notna()
    if not m.any():
        return None
    ww = w[m]
    if ww.sum() <= 0:
        return None
    return float((s[m] * ww).sum() / ww.sum())


def bloque(df: pd.DataFrame) -> dict:
    w = df["w"]
    n = int(len(df))
    N = float(w.sum()) if n else 0.0
    out = {
        "n": n,
        "N": round(N, 1),
        "psic": wmean(df["viol_psicologica_12m"], w),
        "fis": wmean(df["viol_fisica_12m"], w),
        "sex": wmean(df["viol_sexual_12m"], w),
        "alguna": wmean(
            (
                (df["viol_psicologica_12m"] == 1)
                | (df["viol_fisica_12m"] == 1)
                | (df["viol_sexual_12m"] == 1)
            ).astype(float),
            w,
        ),
        "x": {k: wmean(df[k], w) for k in X_CTX if k in df.columns},
    }
    return out


def enares() -> tuple[dict, dict]:
    if not CRS04_MODELO.exists():
        raise FileNotFoundError(
            f"Falta {CRS04_MODELO}. Corre: python scripts/tablas/procesar_crs04.py"
        )
    cols = [
        "DEPARTAMENTO",
        "edad",
        "w",
        "car",
        "viol_psicologica_12m",
        "viol_fisica_12m",
        "viol_sexual_12m",
        *X_CTX,
    ]
    df = pd.read_parquet(CRS04_MODELO, columns=cols)
    df = df.loc[df["car"] != 1].copy()
    df["key"] = df["DEPARTAMENTO"].map(slug)

    nacional = {
        "todas": bloque(df),
        "12_14": bloque(df.loc[df["edad"].between(12, 14)]),
        "15_17": bloque(df.loc[df["edad"].between(15, 17)]),
    }
    por = {}
    for key, sub in df.groupby("key"):
        por[key] = {
            "todas": bloque(sub),
            "12_14": bloque(sub.loc[sub["edad"].between(12, 14)]),
            "15_17": bloque(sub.loc[sub["edad"].between(15, 17)]),
        }
    return nacional, por


def cem() -> tuple[dict, list[dict]]:
    raw = json.loads(CEM_GEO.read_text(encoding="utf-8"))
    features = []
    by: dict[str, list[dict]] = {}
    for feat in raw.get("features", []):
        p = feat.get("properties") or {}
        g = feat.get("geometry") or {}
        coords = g.get("coordinates") or [None, None]
        lon, lat = coords[0], coords[1]
        code = str(p.get("COD_DPTO") or "").zfill(2)
        key = next((slug(ena) for c, ena, _ in DEPTOS if c == code), slug(p.get("NOM_DPTO") or ""))
        row = {
            "id": p.get("COD_CA"),
            "nombre": p.get("NOM_CA"),
            "departamento": p.get("NOM_DPTO"),
            "provincia": p.get("NOM_PROV"),
            "distrito": p.get("NOM_DIST"),
            "ubigeo": p.get("COD_DIST"),
            "direccion": p.get("DIRECCION"),
            "tipo": p.get("TIPO_CEM"),
            "anio": p.get("ANIO"),
            "periodo": p.get("PERIODO"),
            "fecha": p.get("FECHA_DATO"),
            "casos": {
                "total": p.get("CAC_TOTAL"),
                "mujer": p.get("CAC_MUJER"),
                "hombre": p.get("CAC_HOMBRE"),
                "fisica": p.get("CAC_FISICA"),
                "psico": p.get("CAC_PSICO"),
                "sexual": p.get("CAC_SEXUAL"),
                "economica": p.get("CAC_ECONO"),
            },
            "lat": lat,
            "lon": lon,
            "key": key,
        }
        features.append(row)
        by.setdefault(key, []).append(row)
    return by, features


def parse_salud() -> dict:
    text = SALUD_CSV.read_text(encoding="latin-1")
    rows = []
    for line in text.splitlines():
        if line.startswith("N") or line.strip().startswith("N"):
            parts = [c.strip() for c in line.split(";")]
            if len(parts) >= 4 and parts[0]:
                rows.append(
                    {
                        "indicador": parts[0].strip(),
                        "mujer": _num(parts[1]) if len(parts) > 1 else None,
                        "hombre": _num(parts[2]) if len(parts) > 2 else None,
                        "total": _num(parts[3]) if len(parts) > 3 else None,
                    }
                )
    return {
        "fuente": "MINSA: cuadro de violencia familiar (archivo adjunto)",
        "ambito": "Sin ubicacion de servicio en las filas; no se pega a un departamento.",
        "nota": "La fila de casos (143 mujeres + 306 hombres) no cuadra con el total 1 449. Se muestra tal cual.",
        "filas": rows,
    }


def parse_mp() -> dict:
    text = MP_CSV.read_text(encoding="latin-1")
    rows = []
    for line in text.splitlines():
        if "N" in line[:3] or line.strip().startswith("N"):
            parts = [c.strip() for c in line.split(";")]
            if len(parts) >= 4 and parts[0]:
                lugar = [p for p in parts[14:] if p]
                rows.append(
                    {
                        "indicador": parts[0],
                        "mujer": _num(parts[1]) if len(parts) > 1 else None,
                        "hombre": _num(parts[2]) if len(parts) > 2 else None,
                        "lugar": " | ".join(lugar[:3]) if lugar else None,
                    }
                )
    return {
        "fuente": "Ministerio Publico 2026 (archivo adjunto)",
        "ambito": "Varias filas ubican el servicio en Lima / Canete. No es cobertura nacional.",
        "nota": "No se suma a las prevalencias ENARES. Unidad: denuncias/expedientes, no victimizacion 12m.",
        "filas": rows,
    }


def _num(x: str | None) -> float | None:
    if x is None or x == "":
        return None
    try:
        return float(str(x).replace(",", "").replace(" ", ""))
    except ValueError:
        return None


def main() -> None:
    WEB_DATA.mkdir(parents=True, exist_ok=True)
    nacional, por = enares()
    cem_by, cem_rows = cem()

    catalogo = []
    for code, ena, label in DEPTOS:
        key = slug(ena)
        pts = cem_by.get(key, [])
        lats = [c["lat"] for c in pts if c["lat"] is not None]
        lons = [c["lon"] for c in pts if c["lon"] is not None]
        catalogo.append(
            {
                "key": key,
                "code": code,
                "enares": ena,
                "label": LABEL_UI.get(key, label),
                "n_cem": len(pts),
                "centro": {
                    "lat": round(sum(lats) / len(lats), 5) if lats else None,
                    "lon": round(sum(lons) / len(lons), 5) if lons else None,
                },
            }
        )

    geo = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
                "properties": {
                    "id": r["id"],
                    "nombre": r["nombre"],
                    "key": r["key"],
                    "provincia": r["provincia"],
                    "distrito": r["distrito"],
                    "direccion": r["direccion"],
                    "casos_total": r["casos"]["total"],
                    "casos_sexual": r["casos"]["sexual"],
                    "casos_fisica": r["casos"]["fisica"],
                    "casos_psico": r["casos"]["psico"],
                },
            }
            for r in cem_rows
            if r["lat"] is not None and r["lon"] is not None
        ],
    }

    meta = {
        "universo": "Alumnas 12-17, cuestionario CRS.04, SEXO=1. Departamento = de la IE, no de la casa.",
        "encuesta": "ENARES 2024",
        "cem": {
            "archivo": "CEM Regulares (2025).geojson",
            "n": len(cem_rows),
            "tipo": "REGULAR",
            "periodo": "ENE-FEB 2025",
            "fecha": "2025-04-07",
            "nota": "175 centros. Sin horarios ni otras modalidades. Sin registro no implica sin servicio.",
        },
        "x_labels": X_LABELS,
        "fuentes_fuera": {
            "inei_its": "INEI(Sheet1).csv parece conocimiento de ITS, sin anio ni territorio. No entra al perfil.",
        },
    }

    (WEB_DATA / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "departamentos.json").write_text(
        json.dumps(catalogo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "enares.json").write_text(
        json.dumps({"nacional": nacional, "por": por}, ensure_ascii=False),
        encoding="utf-8",
    )
    (WEB_DATA / "cem.json").write_text(
        json.dumps(cem_by, ensure_ascii=False), encoding="utf-8"
    )
    (WEB_DATA / "cem.geojson").write_text(
        json.dumps(geo, ensure_ascii=False), encoding="utf-8"
    )
    (WEB_DATA / "salud.json").write_text(
        json.dumps(parse_salud(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "mp.json").write_text(
        json.dumps(parse_mp(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"wrote {WEB_DATA}  cem={len(cem_rows)} dptos={len(catalogo)}")


if __name__ == "__main__":
    main()
