# -*- coding: utf-8 -*-
"""Prepara JSON/GeoJSON limpios para el dashboard (web/data/).

Lee:
  - data/tablas/crs04_modelo.parquet
  - data/tablas/enares.duckdb
  - data/cem_regulares_2025.geojson

Uso:
    uv run python scripts/tablas/procesar_crs04.py
    uv run python scripts/tablas/armar_dashboard.py
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CEM_GEO, CRS04_MODELO, DB, WEB_DATA

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


def y_mask(df: pd.DataFrame, y: str) -> pd.Series:
    psic = df["viol_psicologica_12m"] == 1
    fis = df["viol_fisica_12m"] == 1
    sex = df["viol_sexual_12m"] == 1
    if y == "psic":
        return psic
    if y == "fis":
        return fis
    if y == "sex":
        return sex
    return psic | fis | sex


def x_dict(df: pd.DataFrame) -> dict:
    w = df["w"]
    return {k: wmean(df[k], w) for k in X_CTX if k in df.columns}


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
        "x": x_dict(df),
        "x_si": {},
        "n_si": {},
    }
    for y in ("alguna", "psic", "fis", "sex"):
        sub = df.loc[y_mask(df, y)]
        out["x_si"][y] = x_dict(sub)
        out["n_si"][y] = int(len(sub))
    return out


def enares() -> tuple[dict, dict]:
    if not CRS04_MODELO.exists():
        raise FileNotFoundError(
            f"Falta {CRS04_MODELO}. Corre: uv run python scripts/tablas/procesar_crs04.py"
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


def _item_cols(con: duckdb.DuckDBPyConnection, table: str, prefixes: list[str]) -> list[str]:
    cols = [r[0] for r in con.execute(f"DESCRIBE {table}").fetchall()]
    out: list[str] = []
    for pref in prefixes:
        out.extend(
            c
            for c in cols
            if c.startswith(pref) and not c.endswith("_O") and "A_" not in c and "B_" not in c
        )
    return out


def _any_eq1(alias: str, cols: list[str]) -> str:
    return " OR ".join(f"COALESCE({alias}.{c}, 0) = 1" for c in cols)


def _pack_serv(row: dict) -> dict:
    def f(key: str) -> float | None:
        v = row.get(key)
        if v is None or pd.isna(v):
            return None
        return round(float(v), 4)

    return {
        "elec": f("elec"),
        "agua": f("agua"),
        "desague": f("desague"),
        "internet": f("internet"),
        "urbano": f("urbano"),
    }


def vivienda_crs01() -> dict:
    """Servicios de vivienda CRS01 por departamento. No se une a CRS04."""
    if not DB.exists():
        raise FileNotFoundError(f"Falta {DB}. Corre: uv run python scripts/tablas/build_db.py")
    con = duckdb.connect(str(DB), read_only=True)
    items = _item_cols(
        con,
        "analisis.crs01_cap402",
        ["C1P404_", "C1P414_", "C1P421_", "C1P431_", "C1P438_"],
    )
    y_sql = _any_eq1("c", items)
    base = f"""
        SELECT
            m.DEPARTAMENTO AS depto,
            COUNT(*) AS n,
            SUM(m.FACTOR_MUJ) AS n_exp,
            SUM(CASE WHEN ({y_sql}) THEN 1 ELSE 0 END) AS n_y,
            SUM(m.FACTOR_MUJ * CAST(m.C1P105 = 1 AS INT)) / SUM(m.FACTOR_MUJ) AS elec,
            SUM(m.FACTOR_MUJ * CAST(m.C1P106 = 1 AS INT)) / SUM(m.FACTOR_MUJ) AS agua,
            SUM(m.FACTOR_MUJ * CAST(m.C1P107 IN (1, 2) AS INT)) / SUM(m.FACTOR_MUJ) AS desague,
            SUM(m.FACTOR_MUJ * CAST(m.C1P110_4 = 1 AS INT)) / SUM(m.FACTOR_MUJ) AS internet,
            SUM(m.FACTOR_MUJ * CAST(m.AREA = 1 AS INT)) / SUM(m.FACTOR_MUJ) AS urbano,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END) AS n_exp_y,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ * CAST(m.C1P105 = 1 AS INT) ELSE 0 END)
                / NULLIF(SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END), 0) AS elec_y,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ * CAST(m.C1P106 = 1 AS INT) ELSE 0 END)
                / NULLIF(SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END), 0) AS agua_y,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ * CAST(m.C1P107 IN (1, 2) AS INT) ELSE 0 END)
                / NULLIF(SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END), 0) AS desague_y,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ * CAST(m.C1P110_4 = 1 AS INT) ELSE 0 END)
                / NULLIF(SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END), 0) AS internet_y,
            SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ * CAST(m.AREA = 1 AS INT) ELSE 0 END)
                / NULLIF(SUM(CASE WHEN ({y_sql}) THEN m.FACTOR_MUJ ELSE 0 END), 0) AS urbano_y
        FROM analisis.crs01_mujeres m
        LEFT JOIN analisis.crs01_cap402 c ON m.ID = c.ID
    """
    nat = dict(
        con.execute(base.replace("m.DEPARTAMENTO AS depto,", "").split("GROUP BY")[0]).fetchdf().iloc[0]
    )
    rows = con.execute(base + " GROUP BY 1").fetchdf()
    con.close()

    def bloque(r: dict) -> dict:
        r = {str(k).lower(): v for k, v in r.items()}
        return {
            "n": int(r["n"]),
            "N": round(float(r["n_exp"]), 1),
            "n_y": int(r["n_y"]),
            "todas": _pack_serv(r),
            "con_violencia": _pack_serv(
                {
                    "elec": r.get("elec_y"),
                    "agua": r.get("agua_y"),
                    "desague": r.get("desague_y"),
                    "internet": r.get("internet_y"),
                    "urbano": r.get("urbano_y"),
                }
            ),
        }

    por = {}
    for rec in rows.to_dict(orient="records"):
        por[slug(rec["depto"])] = bloque(rec)
    return {
        "fuente": "ENARES 2024, CRS.01 mujeres 18+ en vivienda",
        "peso": "FACTOR_MUJ",
        "y": "Alguna violencia fisica o sexual de pareja (actual, ultima o noviazgo), alguna vez",
        "nota": "Describe el lugar. No se une a la alumna. El departamento es el del hogar.",
        "nacional": bloque(nat),
        "por": por,
    }


def main() -> None:
    WEB_DATA.mkdir(parents=True, exist_ok=True)
    nacional, por = enares()
    vivienda = vivienda_crs01()
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
        "que": "CEM regulares 2025, puntos del mapa.",
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
            "archivo": "cem_regulares_2025.geojson",
            "n": len(cem_rows),
            "tipo": "REGULAR",
            "periodo": "ENE-FEB 2025",
            "fecha": "2025-04-07",
            "nota": "175 centros. Sin horarios ni otras modalidades. Sin registro no implica sin servicio.",
        },
        "x_labels": X_LABELS,
        "vivienda": {
            "fuente": vivienda["fuente"],
            "nota": vivienda["nota"],
        },
    }

    (WEB_DATA / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "departamentos.json").write_text(
        json.dumps(catalogo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "enares.json").write_text(
        json.dumps(
            {
                "que": "Prevalencias y factores CRS.04 por departamento y edad. x = todas las alumnas; x_si = solo las que reportaron cada violencia. Peso FACTOR_ALUMNOS.",
                "nacional": nacional,
                "por": por,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (WEB_DATA / "vivienda.json").write_text(
        json.dumps(vivienda, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (WEB_DATA / "cem.json").write_text(
        json.dumps(
            {"que": "CEM regulares 2025 por departamento (lista del panel).", **cem_by},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (WEB_DATA / "cem.geojson").write_text(
        json.dumps(geo, ensure_ascii=False), encoding="utf-8"
    )
    print(f"wrote {WEB_DATA}  cem={len(cem_rows)} dptos={len(catalogo)} vivienda={len(vivienda['por'])}")


if __name__ == "__main__":
    main()
