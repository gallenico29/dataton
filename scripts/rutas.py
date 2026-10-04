"""Rutas del repo. Un solo lugar: crudos vs tablas vs informes.

datos_dev/              crudos INEI (CSV/PDF, no se tocan)
data/tablas/            productos (duckdb, parquet, csv de trabajo)
docs/descriptivos/      cómo se ve la muestra y el diccionario
docs/metodologia/       decisiones (universo, diseño, recodes)
docs/resultados/        lo que salió de LASSO / k-medias / CART
docs/img/               figuras de todos los informes
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CRUDOS = ROOT / "datos_dev"
TABLAS = ROOT / "data" / "tablas"

WEB = ROOT / "web"
WEB_DATA = WEB / "data"

DOCS = ROOT / "docs"
DOC_DESC = DOCS / "descriptivos"
DOC_MET = DOCS / "metodologia"
DOC_RES = DOCS / "resultados"
IMG = DOCS / "img"
IMG_MD = "../img"

DB = TABLAS / "enares.duckdb"

CRS04_MODELO = TABLAS / "crs04_modelo.parquet"
CRS04_MODELO_CSV = TABLAS / "crs04_modelo.csv"
CRS04_FILTRO = TABLAS / "crs04_filtro_violencia.parquet"
CRS04_FILTRO_CSV = TABLAS / "crs04_filtro_violencia.csv"
KMEANS_ASIG = TABLAS / "perfiles_kmeans_asig.csv"
LASSO_COEF = TABLAS / "lasso_crs04_coef.csv"
INV_CRS04_CSV = TABLAS / "inventario_crs04.csv"
INV_CRS01_CSV = TABLAS / "inventario_crs01.csv"


def asegurar_tablas() -> Path:
    TABLAS.mkdir(parents=True, exist_ok=True)
    return TABLAS


def asegurar_docs() -> None:
    for p in (DOC_DESC, DOC_MET, DOC_RES, IMG):
        p.mkdir(parents=True, exist_ok=True)


def ficha(*, que_es: str, que_no: str, tipo: str, script: str | None = None) -> str:
    """Recuadro al inicio de cada informe: para qué sirve y qué no es."""
    lineas = [
        f"> **Qué es este informe.** {que_es}",
        f"> **Qué no es.** {que_no}",
        f"> **Tipo.** {tipo}.",
    ]
    if script:
        lineas.append(
            f"> **Lo escribe.** `{script}` (Python → markdown; no es Rmd)."
        )
    else:
        lineas.append("> **Lo escribe.** Texto a mano (no sale de un script).")
    return "\n".join(lineas) + "\n\n"
