"""Tabla de filtro sí/no violencia CRS04.

Se corre DESPUÉS de procesar_crs04.py. No recalcula ítems: solo arma
las banderas que el k-medias usa para partir la muestra.

Uso:
    python scripts/tablas/procesar_crs04.py
    python scripts/tablas/armar_filtro_violencia.py

Escribe data/tablas/crs04_filtro_violencia.parquet
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_FILTRO, CRS04_FILTRO_CSV, CRS04_MODELO, asegurar_tablas

YCOLS = [
    "viol_psicologica_12m",
    "viol_fisica_12m",
    "viol_sexual_12m",
]
KEYS = ["ID", "COLEGIAL_ID", "car", "w"]


def main() -> None:
    if not CRS04_MODELO.exists():
        raise FileNotFoundError(
            f"Falta {CRS04_MODELO}. Corre: python scripts/tablas/procesar_crs04.py"
        )
    df = pd.read_parquet(CRS04_MODELO, columns=KEYS + YCOLS)
    df = df.loc[df["car"] != 1].copy()
    df["alguna_violencia"] = (
        (df["viol_psicologica_12m"] == 1)
        | (df["viol_fisica_12m"] == 1)
        | (df["viol_sexual_12m"] == 1)
    ).astype(int)
    asegurar_tablas()
    df.to_parquet(CRS04_FILTRO, index=False)
    df.to_csv(CRS04_FILTRO_CSV, index=False)
    n = len(df)
    n_si = int(df["alguna_violencia"].sum())
    print(f"n={n:,}  alguna=sí {n_si:,}  no {n - n_si:,}")
    for y in YCOLS:
        print(f"  {y}: sí={int(df[y].sum()):,}")
    print(f"wrote {CRS04_FILTRO}")


if __name__ == "__main__":
    main()
