"""Limpieza y recodes CRS04 → matriz lista para el LASSO.

Sigue docs/metodologia/metodologia.md §4–6. No incluye variables circulares.

Uso:
    python scripts/tablas/procesar_crs04.py

Escribe data/tablas/crs04_modelo.parquet (y .csv).
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_MODELO, CRS04_MODELO_CSV, DB, asegurar_tablas

PSIC_H = " OR ".join(f"C3P201_{i} = 1" for i in range(1, 12))
FIS_H = " OR ".join(f"C3P205_{i} = 1" for i in range(1, 8))
PSIC_C = " OR ".join(f"C3P223_{i} = 1" for i in range(1, 15))
FIS_C = " OR ".join(f"C3P227_{i} = 1" for i in range(1, 11))
SEX = " OR ".join(f"(C4P248_{i} = 1 AND C4P248C_{i} = 1)" for i in range(1, 17))
DISC = " OR ".join(f"C4P130_{i} = 1" for i in range(1, 7))
CONVIVE = ", ".join(
    f"CASE WHEN car = 1 THEN NULL WHEN C3P115_{i} = 1 THEN 1 ELSE 0 END AS vive_{name}"
    for i, name in [
        (3, "madrastra"),
        (4, "padrastro"),
        (5, "hermana"),
        (6, "hermano"),
        (7, "abuela"),
        (8, "abuelo"),
        (9, "tia"),
        (10, "tio"),
        (11, "prima"),
        (12, "primo"),
        (13, "otros_parientes"),
        (14, "otra_persona"),
    ]
)


def yes01(col: str) -> str:
    """1→1, 2→0, resto NULL. En flujo de casa, CAR → NULL."""
    return f"CASE WHEN car = 1 THEN NULL WHEN {col} = 1 THEN 1 WHEN {col} = 2 THEN 0 END"


def agree01(col: str) -> str:
    """C3P301: 1 de acuerdo → 1, 2 no → 0, 3 NS → 0 (documentado)."""
    return f"CASE WHEN {col} = 1 THEN 1 WHEN {col} IN (2, 3) THEN 0 END"


def build_sql() -> str:
    return f"""
    SELECT
        ID,
        COLEGIAL_ID,
        C3SECC,
        DEPARTAMENTO,
        AREA,
        FACTOR_ALUMNOS AS w,
        CAST(C3P105 = 2 AS INT) AS car,

        -- targets (NULL del filtro 12m = 0)
        CAST((({PSIC_H}) AND C3P203 = 1) OR (({PSIC_C}) AND C3P225 = 1) AS INT)
            AS viol_psicologica_12m,
        CAST((({FIS_H}) AND C3P207 = 1) OR (({FIS_C}) AND C3P229 = 1) AS INT)
            AS viol_fisica_12m,
        CAST(({SEX}) AS INT) AS viol_sexual_12m,

        -- individual
        EDAD AS edad,
        CASE C4P129
            WHEN 7 THEN 'mestiza'
            WHEN 1 THEN 'quechua'
            WHEN 5 THEN 'afroperuana'
            WHEN 6 THEN 'blanca'
            WHEN 9 THEN 'no_sabe'
            ELSE 'otra_indigena_otro'
        END AS etnia,
        CASE
            WHEN C3P128 IS NULL THEN NULL
            WHEN C3P128 = 1 THEN 'castellano'
            WHEN C3P128 = 2 THEN 'quechua'
            ELSE 'otro_idioma'
        END AS idioma,
        CAST(({DISC}) AS INT) AS alguna_discapacidad,
        {yes01("C3P126")} AS toma_en_cuenta,
        {agree01("C3P301_1")} AS act_trabajar,
        {agree01("C3P301_2")} AS act_hablar,
        {agree01("C3P301_3")} AS act_deje_colegio,
        {agree01("C3P301_4")} AS act_profe_golpear,
        {agree01("C3P301_5")} AS act_padres_golpear,
        {agree01("C3P301_6")} AS act_denunciar,

        -- relacional
        {yes01("C3P106")} AS tiene_mama,
        {yes01("C3P110")} AS tiene_papa,
        CASE WHEN C3P105 = 2 THEN NULL ELSE C3P114_PERS END AS pers,
        {CONVIVE},
        CASE WHEN C3P105 = 2 THEN NULL WHEN C3P118_12 = 1 THEN 1 ELSE 0 END
            AS duerme_sola_cuarto,
        CASE
            WHEN C3P120 IS NULL OR C3P105 = 2 THEN NULL
            WHEN C3P120 = 1 THEN 'madre'
            WHEN C3P120 = 2 THEN 'padre'
            WHEN C3P120 IN (7, 8) THEN 'abuelos'
            WHEN C3P120 IN (5, 6) THEN 'hermanos'
            ELSE 'otros'
        END AS cuidador,
        {yes01("C3P120B")} AS se_queda_sola,
        {yes01("C3P121")} AS sin_comer,
        {yes01("C3P122")} AS falta_colegio,
        {yes01("C3P123")} AS peleas_casa,

        -- comunitario / IE
        CAST(AREA = 2 AS INT) AS rural,
        CAST(INED = 1 AS INT) AS ie_mujeres,
        CAST(TURNO = 2 AS INT) AS turno_tarde,
        CASE WHEN C3P217 IN (3, 4) THEN 1 WHEN C3P217 IN (1, 2) THEN 0 END
            AS se_siente_mal,
        CAST(C3P218 = 1 AS INT) AS jalo_curso,
        CAST(C3P219 = 1 AS INT) AS repitio,
        CAST(C3P220 = 1 AS INT) AS expulsion,
        CAST(C3P221 = 1 AS INT) AS amigos_colegio
    FROM (
        SELECT *, CAST(C3P105 = 2 AS INT) AS car
        FROM analisis.crs04_adolescentes
        WHERE SEXO = 1
    )
    """


def add_dummies(df: pd.DataFrame) -> pd.DataFrame:
    etnia = pd.get_dummies(df["etnia"], prefix="etnia", dtype="int8")
    for col in (
        "etnia_quechua",
        "etnia_afroperuana",
        "etnia_blanca",
        "etnia_no_sabe",
        "etnia_otra_indigena_otro",
    ):
        if col not in etnia:
            etnia[col] = 0
    etnia = etnia.drop(columns=["etnia_mestiza"], errors="ignore")

    idioma = pd.get_dummies(df["idioma"], prefix="idioma", dtype="int8")
    for col in ("idioma_quechua", "idioma_otro_idioma"):
        if col not in idioma:
            idioma[col] = 0
    idioma = idioma.drop(columns=["idioma_castellano"], errors="ignore")
    if "idioma_otro_idioma" in idioma.columns:
        idioma = idioma.rename(columns={"idioma_otro_idioma": "idioma_otro"})

    cuid = pd.get_dummies(df["cuidador"], prefix="cuidador", dtype="int8")
    for col in (
        "cuidador_padre",
        "cuidador_abuelos",
        "cuidador_hermanos",
        "cuidador_otros",
    ):
        if col not in cuid:
            cuid[col] = 0
    cuid = cuid.drop(columns=["cuidador_madre"], errors="ignore")

    # missing de idioma/cuidador (CAR): dummies en 0; el LASSO tira esas filas
    out = pd.concat([df, etnia, idioma, cuid], axis=1)
    return out


def main() -> None:
    con = duckdb.connect(str(DB), read_only=True)
    df = con.execute(build_sql()).df()
    con.close()
    df = add_dummies(df)

    asegurar_tablas()
    df.to_parquet(CRS04_MODELO, index=False)
    df.to_csv(CRS04_MODELO_CSV, index=False)

    n = len(df)
    n_car = int(df["car"].sum())
    print(f"n={n:,}  CAR={n_car}  cols={df.shape[1]}")
    print(f"etnia: {df['etnia'].value_counts(dropna=False).to_dict()}")
    print(f"idioma: {df['idioma'].value_counts(dropna=False).to_dict()}")
    print(f"cuidador: {df['cuidador'].value_counts(dropna=False).to_dict()}")
    for y in ("viol_psicologica_12m", "viol_fisica_12m", "viol_sexual_12m"):
        print(f"  {y}: {df[y].mean():.3f} (n sí={int(df[y].sum()):,})")
    print(f"wrote {CRS04_MODELO}")
    print(f"wrote {CRS04_MODELO_CSV}")


if __name__ == "__main__":
    main()
