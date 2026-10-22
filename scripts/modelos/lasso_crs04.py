"""LASSO logístico sobre la matriz de procesar_crs04.py.

Un modelo por target. Peso = FACTOR_ALUMNOS. Estándar: edad y pers.
Sigue docs/metodologia/metodologia.md: sin circulares, sin DEPARTAMENTO en X.

Uso:
    uv run python scripts/tablas/procesar_crs04.py
    uv run python scripts/modelos/lasso_crs04.py

Escribe docs/resultados/lasso_crs04.md y data/tablas/lasso_crs04_coef.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_MODELO, DOC_RES, LASSO_COEF, asegurar_docs, ficha

SRC = CRS04_MODELO
DOC = DOC_RES / "lasso_crs04.md"
COEF = LASSO_COEF

TARGETS = {
    "viol_psicologica_12m": "Violencia psicológica 12m",
    "viol_fisica_12m": "Violencia física 12m",
    "viol_sexual_12m": "Violencia sexual 12m",
}

CONTINUAS = ["edad", "pers"]

BINARIAS = [
    "alguna_discapacidad",
    "toma_en_cuenta",
    "act_trabajar",
    "act_deje_colegio",
    "act_padres_golpear",
    "tiene_mama",
    "tiene_papa",
    "vive_madrastra",
    "vive_padrastro",
    "vive_hermana",
    "vive_hermano",
    "vive_abuela",
    "vive_abuelo",
    "vive_tia",
    "vive_tio",
    "vive_prima",
    "vive_primo",
    "vive_otros_parientes",
    "vive_otra_persona",
    "duerme_sola_cuarto",
    "se_queda_sola",
    "sin_comer",
    "falta_colegio",
    "peleas_casa",
    "rural",
    "ie_mujeres",
    "turno_tarde",
    "se_siente_mal",
    "jalo_curso",
    "repitio",
    "amigos_colegio",
]

DUMMIES = [
    "etnia_quechua",
    "etnia_afroperuana",
    "etnia_blanca",
    "etnia_no_sabe",
    "etnia_otra_indigena_otro",
    "idioma_quechua",
    "idioma_otro",
    "cuidador_padre",
    "cuidador_abuelos",
    "cuidador_hermanos",
    "cuidador_otros",
]

X_COLS = CONTINUAS + BINARIAS + DUMMIES


def load() -> pd.DataFrame:
    if not SRC.exists():
        raise FileNotFoundError(f"Falta {SRC}. Corre: uv run python scripts/tablas/procesar_crs04.py")
    df = pd.read_parquet(SRC)
    # CAR: no imputar el flujo de casa como 0
    return df.loc[df["car"] != 1].copy()


def fit_one(df: pd.DataFrame, ycol: str) -> tuple[pd.DataFrame, float, int]:
    work = df[X_COLS + [ycol, "w"]].dropna(subset=X_COLS + [ycol])
    X = work[X_COLS]
    y = work[ycol].astype(int)
    w = work["w"].to_numpy(dtype=float)
    w = w / w.mean()

    pre = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imp", SimpleImputer(strategy="median")),
                        ("esc", StandardScaler()),
                    ]
                ),
                CONTINUAS,
            ),
            ("bin", "passthrough", BINARIAS + DUMMIES),
        ]
    )
    clf = LogisticRegressionCV(
        Cs=25,
        cv=5,
        penalty="l1",
        solver="saga",
        scoring="roc_auc",
        max_iter=8000,
        n_jobs=1,
        random_state=2024,
    )
    pipe = Pipeline([("pre", pre), ("lasso", clf)])
    pipe.fit(X, y, lasso__sample_weight=w)

    model = pipe.named_steps["lasso"]
    auc = float(np.max(model.scores_[1].mean(axis=0)))
    names = CONTINUAS + BINARIAS + DUMMIES
    coefs = model.coef_.ravel()
    tab = pd.DataFrame({"variable": names, "coef": coefs, "target": ycol})
    tab["abs"] = tab["coef"].abs()
    tab = tab.sort_values("abs", ascending=False).drop(columns="abs")
    return tab, auc, len(work)


LABELS = {
    "edad": "Edad (lineal)",
    "pers": "Tamaño del hogar",
    "alguna_discapacidad": "Alguna discapacidad",
    "toma_en_cuenta": "Toman en cuenta su opinión",
    "act_trabajar": "Actitud: debe trabajar si falta plata",
    "act_deje_colegio": "Actitud: padres deciden que deje el colegio",
    "act_padres_golpear": "Actitud: padres tienen derecho a golpear",
    "tiene_mama": "Tiene mamá",
    "tiene_papa": "Tiene papá",
    "vive_madrastra": "Vive con madrastra",
    "vive_padrastro": "Vive con padrastro",
    "vive_hermana": "Vive con hermana/s",
    "vive_hermano": "Vive con hermano/s",
    "vive_abuela": "Vive con abuela",
    "vive_abuelo": "Vive con abuelo",
    "vive_tia": "Vive con tía",
    "vive_tio": "Vive con tío",
    "vive_prima": "Vive con prima",
    "vive_primo": "Vive con primo",
    "vive_otros_parientes": "Vive con otros parientes",
    "vive_otra_persona": "Vive con otra persona",
    "duerme_sola_cuarto": "Duerme sola en el cuarto",
    "se_queda_sola": "Se queda sola sin adulto",
    "sin_comer": "La dejaron sin comer",
    "falta_colegio": "Falta al colegio para ayudar",
    "peleas_casa": "Peleas en casa",
    "rural": "IE rural",
    "ie_mujeres": "IE de mujeres",
    "turno_tarde": "Turno tarde",
    "se_siente_mal": "Se siente mal/muy mal en el colegio",
    "jalo_curso": "Jaló un curso (2023)",
    "repitio": "Repitió de grado",
    "amigos_colegio": "Mejores amigos en este colegio",
    "etnia_quechua": "Etnia: quechua (ref. mestiza)",
    "etnia_afroperuana": "Etnia: afroperuana",
    "etnia_blanca": "Etnia: blanca",
    "etnia_no_sabe": "Etnia: no sabe",
    "etnia_otra_indigena_otro": "Etnia: otra indígena / otro",
    "idioma_quechua": "Idioma: quechua (ref. castellano)",
    "idioma_otro": "Idioma: otro",
    "cuidador_padre": "Cuidador: padre (ref. madre)",
    "cuidador_abuelos": "Cuidador: abuelos",
    "cuidador_hermanos": "Cuidador: hermanos",
    "cuidador_otros": "Cuidador: otros",
}


EPS = 1e-8


def fmt_coef(coef: float) -> str:
    if abs(coef) < EPS:
        return "0"
    return f"{coef:.4f}"


def fmt_or(coef: float) -> str:
    if abs(coef) < EPS:
        return "1"
    return f"{float(np.exp(coef)):.3f}"


def selection_table(all_coef: pd.DataFrame) -> str:
    wide = all_coef.pivot(index="variable", columns="target", values="coef")
    wide = wide.reindex(X_COLS)
    lines = [
        "| Variable | Qué es | Psic. (logit) | Fís. (logit) | Sexual (logit) | En los 3 |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for var in X_COLS:
        p = float(wide.loc[var, "viol_psicologica_12m"])
        f = float(wide.loc[var, "viol_fisica_12m"])
        s = float(wide.loc[var, "viol_sexual_12m"])
        n_ok = sum(abs(x) > EPS for x in (p, f, s))
        lines.append(
            f"| `{var}` | {LABELS.get(var, var)} | {fmt_coef(p)} | {fmt_coef(f)} | {fmt_coef(s)} | {n_ok}/3 |"
        )
    return "\n".join(lines)


def md_table(tab: pd.DataFrame) -> str:
    tab = tab.copy()
    tab["queda"] = tab["coef"].abs() > EPS
    tab["_abs"] = tab["coef"].abs()
    tab = tab.sort_values(["queda", "_abs"], ascending=[False, False])
    n_ok = int(tab["queda"].sum())
    lines = [
        "| Variable | Qué es | Coef. (logit) | OR |",
        "| --- | --- | ---: | ---: |",
    ]
    for _, row in tab.iterrows():
        var = row["variable"]
        c = float(row["coef"])
        lines.append(
            f"| `{var}` | {LABELS.get(var, var)} | {fmt_coef(c)} | {fmt_or(c)} |"
        )
    lines.append("")
    lines.append(f"Distintas de cero: {n_ok} de {len(tab)}.")
    return "\n".join(lines)


def main() -> None:
    df = load()
    pieces = []
    bloques = []
    for ycol, title in TARGETS.items():
        tab, auc, n = fit_one(df, ycol)
        pieces.append(tab)
        n_sel = int((tab["coef"].abs() > 1e-8).sum())
        bloques.append(
            f"### {title}\n\n"
            f"n completa = {n:,} · AUC-CV = {auc:.3f} · "
            f"variables distintas de cero = {n_sel}.\n\n"
            f"{md_table(tab)}\n\n"
        )
        print(f"{ycol}: n={n} auc={auc:.3f} nz={n_sel}")

    all_coef = pd.concat(pieces, ignore_index=True)
    all_coef["or"] = np.exp(all_coef["coef"])
    all_coef.loc[all_coef["coef"].abs() < EPS, "or"] = 1.0
    asegurar_docs()
    COEF.parent.mkdir(parents=True, exist_ok=True)
    with COEF.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# Coeficientes LASSO CRS04. Lo leen k-medias y CART.\n")
        all_coef.to_csv(fh, index=False)

    md = f"""# LASSO CRS04 (alumnas)

{ficha(
    "Coeficiente y OR del L1 en cada violencia a 12 meses.",
    script="scripts/modelos/lasso_crs04.py",
)}
Logístico L1 (`sklearn.linear_model.LogisticRegressionCV`, `penalty='l1'`, 5-fold, `roc_auc`).
Peso `FACTOR_ALUMNOS` (reescalado a media 1). `edad` y `pers` estandarizadas.
Referencias de dummy: etnia = mestiza, idioma = castellano, cuidador = madre.

Universo: `data/tablas/crs04_modelo.parquet`, se excluyen 18 CAR (no se imputa el flujo de casa).
Especificación: [../metodologia/metodologia.md](../metodologia/metodologia.md).

El peso entra al ajuste. La validación cruzada no incorpora el conglomerado. Lectura de los OR: [../metodologia/metodologia.md](../metodologia/metodologia.md).

## Fuera de X

Servicios de vivienda de CRS01: otra muestra. En el tablero van por departamento.

Tampoco entran el nombre del departamento, `C3P222`, `C3P301_2`, `_4` y `_6`, expulsión, `C3P127`, `C3P124`, ni los bloques de ayuda, agresor y autolesión (`C3P209`–`215`, `216A`, `236`–`247`, `C4P248A/B`, ítems madre).

## Coeficientes

Las 44 variables que entraron al L1. `0` es coeficiente apagado. “En los 3” cuenta en cuántos indicadores queda distinta de cero. Edad y tamaño del hogar están estandarizados.

{selection_table(all_coef)}

---

## Coeficientes por target

{"".join(bloques)}
---

Coeficientes: `data/tablas/lasso_crs04_coef.csv` (los leen k-medias y CART).
"""
    DOC.write_text(md, encoding="utf-8")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
