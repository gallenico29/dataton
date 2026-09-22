"""CART CRS04: reglas SI–ENTONCES sobre las X que el LASSO dejó vivas.

No filtra. Un árbol por Y. Distinto del k-medias (ese agrupa personas; esto corta riesgo).

Uso:
    python scripts/tablas/procesar_crs04.py
    python scripts/tablas/armar_filtro_violencia.py
    python scripts/modelos/lasso_crs04.py
    python scripts/modelos/perfiles_cart_crs04.py

Escribe docs/resultados/perfiles_cart_crs04.md y docs/img/cart_*.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_FILTRO, CRS04_MODELO, DOC_RES, IMG, IMG_MD, LASSO_COEF, asegurar_docs, ficha

from lasso_crs04 import CONTINUAS, EPS, LABELS, X_COLS

COEF = LASSO_COEF
SRC = CRS04_MODELO
DOC = DOC_RES / "perfiles_cart_crs04.md"

TARGETS = [
    ("alguna_violencia", "Alguna violencia (psic o fís o sexual)"),
    ("viol_fisica_12m", "Violencia física 12m"),
    ("viol_sexual_12m", "Violencia sexual 12m"),
]

SHORT = {
    "edad": "edad",
    "pers": "tamaño hogar",
    "alguna_discapacidad": "alguna discapacidad",
    "toma_en_cuenta": "la toman en cuenta",
    "act_trabajar": "debe trabajar",
    "act_deje_colegio": "deje el colegio",
    "act_padres_golpear": "padres pueden golpear",
    "vive_hermana": "vive hermana",
    "vive_hermano": "vive hermano",
    "vive_tio": "vive tío",
    "vive_abuela": "vive abuela",
    "vive_otra_persona": "vive otra persona",
    "duerme_sola_cuarto": "duerme sola en el cuarto",
    "se_queda_sola": "se queda sola",
    "sin_comer": "la dejaron sin comer",
    "falta_colegio": "falta al colegio",
    "peleas_casa": "peleas en casa",
    "rural": "IE rural",
    "ie_mujeres": "IE de mujeres",
    "se_siente_mal": "se siente mal en el colegio",
    "jalo_curso": "jaló un curso",
    "repitio": "repitió",
    "amigos_colegio": "amigos en este colegio",
    "etnia_quechua": "etnia quechua",
    "etnia_afroperuana": "etnia afroperuana",
    "etnia_blanca": "etnia blanca",
    "etnia_no_sabe": "etnia no sabe",
    "cuidador_padre": "cuidador: padre",
    "cuidador_hermanos": "cuidador: hermanos",
    "cuidador_otros": "cuidador: otros",
    "vive_padrastro": "vive padrastro",
    "vive_abuelo": "vive abuelo",
    "vive_tia": "vive tía",
    "vive_prima": "vive prima",
    "turno_tarde": "turno tarde",
}


def lab(var: str) -> str:
    return SHORT.get(var, LABELS.get(var, var))


def x_lasso() -> list[str]:
    if not COEF.exists():
        raise FileNotFoundError(f"Falta {COEF}. Corre: python scripts/modelos/lasso_crs04.py")
    coef = pd.read_csv(COEF)
    wide = coef.pivot(index="variable", columns="target", values="coef")
    wide = wide.reindex(X_COLS)
    n_ok = (wide.abs() > EPS).sum(axis=1)
    return [v for v in X_COLS if int(n_ok.get(v, 0)) >= 1]


def load() -> pd.DataFrame:
    if not SRC.exists():
        raise FileNotFoundError(f"Falta {SRC}. Corre: python scripts/tablas/procesar_crs04.py")
    if not CRS04_FILTRO.exists():
        raise FileNotFoundError(
            f"Falta {CRS04_FILTRO}. Corre: python scripts/tablas/armar_filtro_violencia.py"
        )
    x = pd.read_parquet(SRC)
    y = pd.read_parquet(CRS04_FILTRO)
    flags = [
        "alguna_violencia",
        "viol_psicologica_12m",
        "viol_fisica_12m",
        "viol_sexual_12m",
        "w",
        "car",
    ]
    x = x.drop(columns=[c for c in flags if c in x.columns], errors="ignore")
    df = x.merge(y, on=["ID", "COLEGIAL_ID"], how="inner")
    return df.loc[df["car"] != 1].copy()


def cond_texto(var: str, thr: float, ir_izq: bool) -> str:
    if var in CONTINUAS:
        if ir_izq:
            return f"{lab(var)} ≤ {thr:.1f}"
        return f"{lab(var)} > {thr:.1f}"
    if ir_izq:
        return f"NO {lab(var)}"
    return f"SÍ {lab(var)}"


def hojas(clf: DecisionTreeClassifier, names: list[str], work: pd.DataFrame, ycol: str) -> pd.DataFrame:
    tree = clf.tree_

    def rec(node: int, conds: list[str]) -> list[dict]:
        left = tree.children_left[node]
        if left == -1:
            return [{"nodo": node, "regla": " y ".join(conds) if conds else "(todas)", "conds": conds}]
        var = names[tree.feature[node]]
        thr = float(tree.threshold[node])
        return rec(left, conds + [cond_texto(var, thr, True)]) + rec(
            tree.children_right[node], conds + [cond_texto(var, thr, False)]
        )

    rows = rec(0, [])
    leaf_id = clf.apply(work[names])
    out = []
    for r in rows:
        sl = work.loc[leaf_id == r["nodo"]]
        if sl.empty:
            continue
        w = sl["w"].to_numpy(dtype=float)
        y = sl[ycol].to_numpy(dtype=float)
        out.append(
            {
                "nodo": r["nodo"],
                "regla": r["regla"],
                "n": int(len(sl)),
                "N": float(w.sum()),
                "pct_y": float(np.average(y, weights=w)),
                "psic": float(np.average(sl["viol_psicologica_12m"], weights=w)),
                "fis": float(np.average(sl["viol_fisica_12m"], weights=w)),
                "sex": float(np.average(sl["viol_sexual_12m"], weights=w)),
            }
        )
    tab = pd.DataFrame(out).sort_values("pct_y", ascending=False)
    tab["hoja"] = [f"H{i}" for i in range(1, len(tab) + 1)]
    return tab.reset_index(drop=True)


def plot_arbol(clf: DecisionTreeClassifier, names: list[str], titulo: str, fname: str) -> None:
    fig, ax = plt.subplots(figsize=(16, 8), facecolor="white")
    plot_tree(
        clf,
        feature_names=[lab(v) for v in names],
        class_names=["no", "sí"],
        filled=True,
        rounded=True,
        impurity=False,
        proportion=True,
        fontsize=8,
        ax=ax,
    )
    ax.set_title(titulo, loc="left", fontsize=12)
    fig.tight_layout()
    IMG.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)


def plot_hojas(tab: pd.DataFrame, base: float, titulo: str, fname: str) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 0.7 * len(tab) + 1.8), facecolor="white")
    y = np.arange(len(tab))
    vals = 100 * tab["pct_y"].to_numpy()
    colores = ["#c2410c" if v >= 100 * base else "#0369a1" for v in vals]
    ax.barh(y, vals, color=colores, height=0.62)
    ax.axvline(100 * base, color="#111827", ls="--", lw=1.1, label=f"promedio de esta Y ({100 * base:.1f} %)")
    ax.set_yticks(y)
    ax.set_yticklabels([f"{h}  {r}" for h, r in zip(tab["hoja"], tab["regla"])], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("% que reporta esta violencia (ponderado)")
    ax.set_xlim(0, 100)
    ax.set_title(titulo, loc="left", fontsize=11)
    ax.legend(frameon=False, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)


def plot_importancia(clf: DecisionTreeClassifier, names: list[str], titulo: str, fname: str) -> None:
    imp = pd.Series(clf.feature_importances_, index=names)
    imp = imp[imp > 1e-8].sort_values()
    if imp.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 0.38 * len(imp) + 1.4), facecolor="white")
    ax.barh([lab(v) for v in imp.index], imp.values, color="#0369a1")
    ax.set_xlabel("Importancia en el árbol (suma 1)")
    ax.set_title(titulo, loc="left", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)


def plot_camino(tab: pd.DataFrame, titulo: str, fname: str) -> None:
    """Cajas SI–ENTONCES: la hoja más alta y la más baja."""
    if len(tab) < 2:
        return
    hi = tab.iloc[0]
    lo = tab.iloc[-1]
    fig, ax = plt.subplots(figsize=(11, 4.2), facecolor="white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title(titulo, loc="left", fontsize=11)

    def caja(x, y, w, h, texto, color):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.08,rounding_size=0.15",
                facecolor=color,
                edgecolor="#292524",
                lw=0.8,
            )
        )
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=8, wrap=True)

    caja(0.2, 2.3, 4.4, 1.4, f"Más riesgo  {hi['hoja']}\n{hi['regla']}\n{100 * hi['pct_y']:.1f} %  ·  n={hi['n']:,}", "#fecaca")
    caja(5.4, 2.3, 4.4, 1.4, f"Menos riesgo  {lo['hoja']}\n{lo['regla']}\n{100 * lo['pct_y']:.1f} %  ·  n={lo['n']:,}", "#bae6fd")
    ax.text(
        5,
        0.9,
        "Así se lee el CART: una frase (combinación de las X del LASSO) y un % de violencia.\n"
        "No es un tipo de alumna; es un camino. Dos chicas distintas pueden caer en la misma hoja.",
        ha="center",
        va="center",
        fontsize=9,
        color="#44403c",
    )
    fig.tight_layout()
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)


def md_hojas(tab: pd.DataFrame, base: float) -> str:
    lines = [
        "| Hoja | Regla (SI…) | n | N | % esta Y | % psic. | % fís. | % sexual | vs promedio |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for _, r in tab.iterrows():
        delta = 100 * (r["pct_y"] - base)
        signo = f"+{delta:.1f} pp" if delta >= 0 else f"{delta:.1f} pp"
        lines.append(
            f"| `{r['hoja']}` | {r['regla']} | {r['n']:,} | {r['N']:,.0f} | "
            f"{100 * r['pct_y']:.1f}% | {100 * r['psic']:.1f}% | {100 * r['fis']:.1f}% | "
            f"{100 * r['sex']:.1f}% | {signo} |"
        )
    return "\n".join(lines)


def guia() -> str:
    return """## Cómo se lee (sin jerga)

El CART no junta alumnas “parecidas”. **Corta** la muestra con preguntas sí/no hasta separar, lo más que puede, a las que reportaron violencia de las que no.

Cada camino es una frase: *si hay peleas en casa y no la toman en cuenta → 78 % reporta esta violencia*. Eso es el perfil-regla. No es un “tipo de persona” (eso era el k-medias).

**X que usa:** todas las que el LASSO dejó vivas en **al menos un** target (unión), no solo las 13 del 3/3. La violencia **sí entra**: es lo que el árbol trata de separar. El peso de la encuesta entra al fit.

**Por qué tres árboles.** “Alguna” la empuja la psicológica (~60 %): el primer corte suele ser el de esa Y tan frecuente. Física y sexual son más raras; las reglas cambian.

### Qué vas a ver en cada árbol

1. **El árbol dibujado.** Arriba la primera pregunta (la que más parte). Izquierda = no / menor; derecha = sí / mayor. Las cajas de abajo son las **hojas**: ahí ya no corta. El color más rojo = más % de violencia en esa hoja.
2. **Barras de las hojas.** Cada barra es un camino. La línea punteada es el % promedio de esa violencia en todas las alumnas. Naranja = por encima del promedio; azul = por debajo. Esa es la visualización que más se lee: “esta combinación queda 15 puntos por encima”.
3. **Las dos cajas (más vs menos riesgo).** La hoja más alta y la más baja, en una frase.
4. **Importancia.** Qué preguntas usó más el árbol. Si una X del LASSO no aparece, el árbol no la necesitó con profundidad 3.

**n** = alumnas en la encuesta. **N** = chicas del país (peso). **pp** = puntos porcentuales contra el promedio.

No es causal. Una hoja chica (n bajo) no se cuenta como hallazgo robusto.
"""


def fit_one(work: pd.DataFrame, cols: list[str], ycol: str) -> DecisionTreeClassifier:
    w = work["w"].to_numpy(dtype=float)
    w = w / w.mean()
    clf = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=max(80, len(work) // 40),
        random_state=2024,
    )
    clf.fit(work[cols], work[ycol].astype(int), sample_weight=w)
    return clf


def main() -> None:
    cols = x_lasso()
    df = load()
    need = cols + [
        "viol_psicologica_12m",
        "viol_fisica_12m",
        "viol_sexual_12m",
        "alguna_violencia",
        "w",
    ]
    work = df.dropna(subset=need).copy()
    n, N = len(work), float(work["w"].sum())

    bloques = []
    for ycol, titulo in TARGETS:
        clf = fit_one(work, cols, ycol)
        tab = hojas(clf, cols, work, ycol)
        base = float(np.average(work[ycol], weights=work["w"]))
        tag = ycol.replace("viol_", "").replace("_12m", "")
        plot_arbol(clf, cols, f"{titulo} — árbol (profundidad 3)", f"cart_{tag}_arbol.png")
        plot_hojas(tab, base, f"{titulo} — cada hoja es una regla", f"cart_{tag}_hojas.png")
        plot_camino(tab, f"{titulo} — el camino más alto y el más bajo", f"cart_{tag}_camino.png")
        plot_importancia(clf, cols, f"{titulo} — qué X usó el árbol", f"cart_{tag}_imp.png")
        usadas = sorted(
            {cols[i] for i in clf.tree_.feature if i >= 0},
            key=lambda v: cols.index(v),
        )
        bloques.append(
            f"## {titulo}\n\n"
            f"Promedio ponderado de esta Y: **{100 * base:.1f} %**. "
            f"Hojas = {len(tab)}. X que el árbol llegó a usar: "
            + ", ".join(f"`{v}`" for v in usadas)
            + ".\n\n"
            f"### Árbol\n\n"
            f"![árbol {tag}]({IMG_MD}/cart_{tag}_arbol.png)\n\n"
            f"Primera pregunta = la que más parte. Izquierda ≈ no / menor; derecha ≈ sí / mayor. "
            f"Cajas de abajo = hojas. Más rojo = más % de esta violencia.\n\n"
            f"### Hojas (la visualización principal)\n\n"
            f"![hojas {tag}]({IMG_MD}/cart_{tag}_hojas.png)\n\n"
            f"Naranja = por encima del {100 * base:.1f} % promedio. Azul = por debajo. "
            f"Cada etiqueta es el SI–ENTONCES completo.\n\n"
            f"{md_hojas(tab, base)}\n\n"
            f"### Más riesgo vs menos riesgo\n\n"
            f"![camino {tag}]({IMG_MD}/cart_{tag}_camino.png)\n\n"
            f"### Qué X pesaron\n\n"
            f"![imp {tag}]({IMG_MD}/cart_{tag}_imp.png)\n\n"
        )
        print(f"{ycol}: base={base:.3f} hojas={len(tab)} usadas={usadas}")

    md = f"""# CART CRS04 (reglas de riesgo)

{ficha(
    que_es="Reglas SI–ENTONCES: combinación de X → % de violencia. Un árbol por Y (alguna, física, sexual). No se filtra; entran todas.",
    que_no="No arma tipos de persona (eso es k-medias). No es el LASSO: usa la unión de X que el L1 dejó vivas.",
    tipo="Resultado del modelo",
    script="scripts/modelos/perfiles_cart_crs04.py",
)}
El k-medias ([perfiles_kmeans_crs04.md](perfiles_kmeans_crs04.md)) arma **tipos de alumna**. Este CART arma **reglas**.

No se filtra. Entran todas (sin 18 CAR). n = {n:,} · N = {N:,.0f}.
Profundidad 3, hojas gordas (`min_samples_leaf` ≈ n/40), peso `FACTOR_ALUMNOS`.

**X:** unión de las que el LASSO no apagó en los 3 a la vez ({len(cols)} variables), no el núcleo 3/3.
{', '.join(f'`{v}`' for v in cols)}.

{guia()}

---

{''.join(bloques)}
No mezclar `H1` de este doc con `si-1` del k-medias: no son lo mismo.
"""
    asegurar_docs()
    DOC.write_text(md, encoding="utf-8")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
