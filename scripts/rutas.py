"""Rutas del repo.

datos_dev/          crudos INEI
data/               CEM fuente + tablas de trabajo
docs/               informes
web/data/           JSON del tablero
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CRUDOS = ROOT / "datos_dev"
TABLAS = ROOT / "data" / "tablas"

WEB = ROOT / "web"
WEB_DATA = WEB / "data"
TABLERO = WEB / "tablero.html"

DOCS = ROOT / "docs"
DOC_DESC = DOCS / "descriptivos"
DOC_MET = DOCS / "metodologia"
DOC_RES = DOCS / "resultados"
IMG = DOCS / "img"
IMG_MD = "../img"

DB = TABLAS / "enares.duckdb"

CEM_GEO = ROOT / "data" / "cem_regulares_2025.geojson"

CRS04_MODELO = TABLAS / "crs04_modelo.parquet"
CRS04_FILTRO = TABLAS / "crs04_filtro_violencia.parquet"
KMEANS_ASIG = TABLAS / "perfiles_kmeans_asig.csv"
LASSO_COEF = TABLAS / "lasso_crs04_coef.csv"


def asegurar_tablas() -> Path:
    TABLAS.mkdir(parents=True, exist_ok=True)
    return TABLAS


def asegurar_docs() -> None:
    for p in (DOC_DESC, DOC_MET, DOC_RES, IMG):
        p.mkdir(parents=True, exist_ok=True)


def ficha(texto: str, script: str | None = None) -> str:
    if script:
        return f"> {texto} (`{script}`)\n\n"
    return f"> {texto}\n\n"
