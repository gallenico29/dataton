"""k-medias CRS04: filtro sí/no alguna violencia, después cluster.

X = las que el LASSO dejó vivas en los 3 targets. Y no entra al fit.

Uso:
    uv run python scripts/tablas/procesar_crs04.py
    uv run python scripts/tablas/armar_filtro_violencia.py
    uv run python scripts/modelos/lasso_crs04.py
    uv run python scripts/modelos/perfiles_kmeans_crs04.py

Escribe docs/resultados/perfiles_kmeans_crs04.md y docs/img/perfiles_*.svg / *.png.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRS04_FILTRO, CRS04_MODELO, DOC_RES, IMG, IMG_MD, KMEANS_ASIG, LASSO_COEF, asegurar_docs, ficha

from lasso_crs04 import EPS, LABELS, X_COLS

COEF = LASSO_COEF
SRC = CRS04_MODELO
DOC = DOC_RES / "perfiles_kmeans_crs04.md"
ASIG = KMEANS_ASIG

K = 3
YCOLS = [
    "viol_psicologica_12m",
    "viol_fisica_12m",
    "viol_sexual_12m",
]
INK = "#1c1917"
MUTED = "#78716c"
GRID = "#e7e5e4"
BG = "#fafaf9"
C1 = "#0369a1"
C2 = "#c2410c"
C3 = "#7c3aed"
PSIC = "#b45309"
FIS = "#c2410c"
SEX = "#7c3aed"
COLS_K = [C1, C2, C3]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_n(x: float) -> str:
    return f"{int(round(x)):,}"


def fmt_pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def wmean(s: pd.Series, w: pd.Series) -> float:
    ww = w.to_numpy(dtype=float)
    xx = s.to_numpy(dtype=float)
    if ww.sum() <= 0:
        return float("nan")
    return float(np.average(xx, weights=ww))


def nucleo_lasso() -> tuple[list[str], pd.DataFrame]:
    if not COEF.exists():
                raise FileNotFoundError(f"Falta {COEF}. Corre: uv run python scripts/modelos/lasso_crs04.py")
    coef = pd.read_csv(COEF, comment="#")
    wide = coef.pivot(index="variable", columns="target", values="coef")
    wide = wide.reindex(X_COLS)
    n_ok = (wide.abs() > EPS).sum(axis=1)
    keep = [v for v in X_COLS if int(n_ok.get(v, 0)) == 3]
    meta = pd.DataFrame(
        {
            "variable": X_COLS,
            "label": [LABELS.get(v, v) for v in X_COLS],
            "n_targets": [int(n_ok.get(v, 0)) for v in X_COLS],
            "en_kmeans": [v in keep for v in X_COLS],
        }
    )
    return keep, meta


def load() -> pd.DataFrame:
    if not SRC.exists():
        raise FileNotFoundError(f"Falta {SRC}. Corre: uv run python scripts/tablas/procesar_crs04.py")
    if not CRS04_FILTRO.exists():
        raise FileNotFoundError(
            f"Falta {CRS04_FILTRO}. Corre: uv run python scripts/tablas/armar_filtro_violencia.py"
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


def write_svg(name: str, body: str) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / name).write_text(body, encoding="utf-8")


def grouped_h(
    name: str,
    categories: list[str],
    series: list[tuple[str, list[float], str]],
    caption: str,
    width: int = 960,
    xmax: float = 100.0,
    suffix: str = "%",
) -> None:
    left, right, top, row_h, gap = 220, 28, 36, 48, 10
    bar_w = width - left - right
    height = top + len(categories) * (row_h + gap) + 36
    n_s = len(series)
    one = (row_h - 4) / n_s
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f"<title>{esc(caption)}</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="18" fill="{MUTED}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(caption)}</text>',
    ]
    y = top
    for i, cat in enumerate(categories):
        parts.append(
            f'<text x="{left - 8}" y="{y + 28}" text-anchor="end" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(cat)}</text>'
        )
        for j, (_lab, vals, color) in enumerate(series):
            w = bar_w * (vals[i] / xmax if xmax else 0)
            yy = y + j * one
            parts.append(
                f'<rect x="{left}" y="{yy:.1f}" width="{max(w, 1):.1f}" height="{one - 2:.1f}" '
                f'fill="{color}" rx="2"/>'
            )
            parts.append(
                f'<text x="{left + w + 4:.1f}" y="{yy + one - 5:.1f}" fill="{INK}" font-size="10" '
                f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{vals[i]:.1f}{suffix}</text>'
            )
        y += row_h + gap
    lx = left
    for lab, _vals, color in series:
        parts += [
            f'<rect x="{lx}" y="{height - 18}" width="10" height="10" fill="{color}" rx="2"/>',
            f'<text x="{lx + 14}" y="{height - 9}" fill="{INK}" font-size="11" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(lab)}</text>',
        ]
        lx += 160
    parts.append("</svg>")
    write_svg(name, "\n".join(parts))


def bar_simple(name: str, rows: list[tuple[str, float, str]], caption: str, suffix: str) -> None:
    left, right, top, row_h, gap = 160, 72, 28, 28, 10
    width = 720
    bar_w = width - left - right
    height = top + len(rows) * (row_h + gap) + 16
    xmax = max((v for _, v, _ in rows), default=1) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f"<title>{esc(caption)}</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="18" fill="{MUTED}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(caption)}</text>',
    ]
    y = top + 4
    for label, value, color in rows:
        w = bar_w * value / xmax
        parts += [
            f'<text x="{left - 8}" y="{y + 19}" text-anchor="end" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(label)}</text>',
            f'<rect x="{left}" y="{y}" width="{max(w, 1):.1f}" height="{row_h}" fill="{color}" rx="3"/>',
            f'<text x="{left + w + 6:.1f}" y="{y + 19}" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{value:.1f}{suffix}</text>',
        ]
        y += row_h + gap
    parts.append("</svg>")
    write_svg(name, "\n".join(parts))


def fit_kmeans(work: pd.DataFrame, nucleo: list[str], k: int) -> tuple[np.ndarray, float]:
    Xs = StandardScaler().fit_transform(work[nucleo])
    km = KMeans(n_clusters=k, random_state=2024, n_init=10)
    lab = km.fit_predict(Xs)
    sil = float(silhouette_score(Xs, lab)) if len(set(lab)) > 1 else float("nan")
    return lab, sil


def sil_table(work: pd.DataFrame, nucleo: list[str]) -> str:
    Xs = StandardScaler().fit_transform(work[nucleo])
    lines = ["| k | Silueta (sin peso) |", "| ---: | ---: |"]
    for k in (2, 3, 4):
        lab = KMeans(n_clusters=k, random_state=2024, n_init=10).fit_predict(Xs)
        s = float(silhouette_score(Xs, lab))
        mark = " ← usado" if k == K else ""
        lines.append(f"| {k} | {s:.3f}{mark} |")
    return "\n".join(lines)


def describe(
    work: pd.DataFrame,
    nucleo: list[str],
    labs: np.ndarray,
    prefijo: str,
    ycol: str,
) -> pd.DataFrame:
    out = work.copy()
    out["_lab"] = labs
    rows = []
    for raw in sorted(out["_lab"].unique()):
        sl = out.loc[out["_lab"] == raw]
        rec = {
            "cluster_raw": int(raw),
            "n": int(len(sl)),
            "N": float(sl["w"].sum()),
        }
        for y in YCOLS + ["alguna_violencia"]:
            rec[y] = wmean(sl[y], sl["w"])
        for v in nucleo:
            rec[v] = wmean(sl[v], sl["w"])
        otros = [y for y in YCOLS if y != ycol]
        rec["score"] = sum(rec[y] for y in otros) + (
            rec.get("peleas_casa", 0)
            + rec.get("se_siente_mal", 0)
            + rec.get("falta_colegio", 0)
            - rec.get("toma_en_cuenta", 0)
        )
        rows.append(rec)
    tab = pd.DataFrame(rows).sort_values("score", ascending=False)
    tab["cluster"] = [f"{prefijo}{i}" for i in range(1, len(tab) + 1)]
    return tab.reset_index(drop=True)


def remap_labels(raw: np.ndarray, tab: pd.DataFrame) -> np.ndarray:
    orden = tab.sort_values("cluster")["cluster_raw"].tolist()
    mp = {old: i + 1 for i, old in enumerate(orden)}
    return np.array([mp[int(x)] for x in raw])


def md_means(tab: pd.DataFrame, nucleo: list[str], con_y: bool) -> str:
    heads = ["Cluster", "n", "N"]
    if con_y:
        heads += ["% psic.", "% fís.", "% sexual"]
    for v in nucleo:
        heads.append(LABELS.get(v, v))
    lines = [
        "| " + " | ".join(heads) + " |",
        "| " + " | ".join(["---"] * 3 + (["---:"] * (len(heads) - 3))) + " |",
    ]
    for _, r in tab.iterrows():
        cells = [f"`{r['cluster']}`", f"{r['n']:,}", fmt_n(r["N"])]
        if con_y:
            cells += [
                fmt_pct(r["viol_psicologica_12m"]),
                fmt_pct(r["viol_fisica_12m"]),
                fmt_pct(r["viol_sexual_12m"]),
            ]
        for v in nucleo:
            if v == "edad":
                cells.append(f"{r[v]:.2f}")
            else:
                cells.append(fmt_pct(r[v]))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def charts_lado(tab: pd.DataFrame, nucleo: list[str], tag: str, titulo: str) -> list[str]:
    nombres = tab["cluster"].tolist()
    series = []
    for i, cl in enumerate(nombres):
        r = tab.loc[tab["cluster"] == cl].iloc[0]
        bins = [v for v in nucleo if v != "edad"]
        series.append(
            (cl, [100.0 * float(r[v]) for v in bins], COLS_K[i % 3])
        )
    cats = [LABELS.get(v, v) for v in nucleo if v != "edad"]
    fname_x = f"perfiles_{tag}_x.svg"
    grouped_h(
        fname_x,
        cats,
        series,
        f"{titulo}: % ponderado de cada X (0/1) por cluster",
    )
    fname_e = f"perfiles_{tag}_edad.svg"
    bar_simple(
        fname_e,
        [
            (cl, float(tab.loc[tab["cluster"] == cl, "edad"].iloc[0]), COLS_K[i % 3])
            for i, cl in enumerate(nombres)
        ],
        f"{titulo}: edad media ponderada",
        " años",
    )
    fname_y = f"perfiles_{tag}_violencia.svg"
    grouped_h(
        fname_y,
        ["Psicológica", "Física", "Sexual"],
        [
            (
                cl,
                [
                    100.0 * float(tab.loc[tab["cluster"] == cl, y].iloc[0])
                    for y in YCOLS
                ],
                COLS_K[i % 3],
            )
            for i, cl in enumerate(nombres)
        ],
        f"{titulo}: % de cada tipo de violencia 12m (ponderado)",
    )
    return [fname_x, fname_e, fname_y]


SHORT = {
    "edad": "edad",
    "toma_en_cuenta": "la toman en cuenta",
    "act_trabajar": "debe trabajar",
    "act_deje_colegio": "deje colegio",
    "act_padres_golpear": "padres golpear",
    "vive_hermana": "vive hermana",
    "vive_tio": "vive tío",
    "se_queda_sola": "se queda sola",
    "falta_colegio": "falta colegio",
    "peleas_casa": "peleas casa",
    "ie_mujeres": "IE mujeres",
    "se_siente_mal": "se siente mal",
    "jalo_curso": "jaló curso",
}


def _color_map(nombres: list[str]) -> dict[str, str]:
    return {cl: COLS_K[i % 3] for i, cl in enumerate(nombres)}


def plot_pca_map(
    X: pd.DataFrame,
    cluster: pd.Series,
    nombres: list[str],
    titulo: str,
    fname: str,
) -> tuple[str, PCA, np.ndarray]:
    Xs = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2, random_state=2024)
    Z = pca.fit_transform(Xs)
    cmap = _color_map(nombres)
    cents = np.vstack([Z[cluster.to_numpy() == cl].mean(axis=0) for cl in nombres])

    pad = 0.8
    x_min, x_max = Z[:, 0].min() - pad, Z[:, 0].max() + pad
    y_min, y_max = Z[:, 1].min() - pad, Z[:, 1].max() + pad
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 400),
        np.linspace(y_min, y_max, 400),
    )
    grid = np.c_[xx.ravel(), yy.ravel()]
    d = ((grid[:, None, :] - cents[None, :, :]) ** 2).sum(axis=2)
    reg = d.argmin(axis=1).reshape(xx.shape)
    region_colors = [cmap[cl] for cl in nombres]
    from matplotlib.colors import ListedColormap

    fig, ax = plt.subplots(figsize=(8.2, 6.4), facecolor="white")
    ax.imshow(
        reg,
        interpolation="nearest",
        extent=(x_min, x_max, y_min, y_max),
        origin="lower",
        cmap=ListedColormap(region_colors),
        alpha=0.22,
        aspect="auto",
    )
    rng = np.random.default_rng(2024)
    # jitter mínimo para que las binarias no se apilen en el mismo punto
    jitter = 0.04 * rng.normal(size=Z.shape)
    for cl in nombres:
        m = cluster.to_numpy() == cl
        ax.scatter(
            Z[m, 0] + jitter[m, 0],
            Z[m, 1] + jitter[m, 1],
            s=10,
            c=cmap[cl],
            alpha=0.45,
            linewidths=0,
            label=cl,
            zorder=2,
        )
    ax.scatter(
        cents[:, 0],
        cents[:, 1],
        marker="x",
        s=180,
        c="white",
        linewidths=2.6,
        zorder=4,
    )
    ax.scatter(
        cents[:, 0],
        cents[:, 1],
        marker="x",
        s=120,
        c="#111827",
        linewidths=1.4,
        zorder=5,
    )
    v1, v2 = 100 * pca.explained_variance_ratio_
    ax.set_xlabel(f"PC1 ({v1:.1f} % de la varianza de las 13 X)")
    ax.set_ylabel(f"PC2 ({v2:.1f} %)")
    ax.set_title(titulo, loc="left", fontsize=11)
    ax.legend(frameon=False, loc="upper right")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.axhline(0, color="#d6d3d1", lw=0.6)
    ax.axvline(0, color="#d6d3d1", lw=0.6)
    fig.tight_layout()
    IMG.mkdir(parents=True, exist_ok=True)
    path = IMG / fname
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return fname, pca, Xs


def plot_biplot(pca: PCA, nucleo: list[str], titulo: str, fname: str) -> str:
    load = pca.components_.T
    fig, ax = plt.subplots(figsize=(8.2, 6.4), facecolor="white")
    ax.axhline(0, color="#d6d3d1", lw=0.6)
    ax.axvline(0, color="#d6d3d1", lw=0.6)
    for i, var in enumerate(nucleo):
        ax.arrow(
            0,
            0,
            load[i, 0],
            load[i, 1],
            color="#0369a1",
            head_width=0.02,
            length_includes_head=True,
            alpha=0.85,
        )
        ax.text(
            load[i, 0] * 1.08,
            load[i, 1] * 1.08,
            SHORT.get(var, var),
            fontsize=8,
            color="#1c1917",
            ha="center",
            va="center",
        )
    v1, v2 = 100 * pca.explained_variance_ratio_
    ax.set_xlabel(f"PC1 ({v1:.1f} %)")
    ax.set_ylabel(f"PC2 ({v2:.1f} %)")
    ax.set_title(titulo, loc="left", fontsize=11)
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)
    return fname


def plot_var_panels(
    df: pd.DataFrame,
    nucleo: list[str],
    nombres: list[str],
    titulo: str,
    fname: str,
) -> str:
    cmap = _color_map(nombres)
    n = len(nucleo)
    ncols = 4
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(11.2, 2.5 * nrows), facecolor="white")
    axes = np.atleast_1d(axes).ravel()
    for i, var in enumerate(nucleo):
        ax = axes[i]
        if var == "edad":
            data = [df.loc[df["cluster"] == cl, var].to_numpy() for cl in nombres]
            bp = ax.boxplot(
                data,
                tick_labels=nombres,
                patch_artist=True,
                showfliers=False,
                medianprops={"color": "#111827"},
            )
            for patch, cl in zip(bp["boxes"], nombres):
                patch.set_facecolor(cmap[cl])
                patch.set_alpha(0.7)
            ax.set_ylabel("años")
        else:
            vals = [
                100.0 * float(df.loc[df["cluster"] == cl, var].mean()) for cl in nombres
            ]
            ax.bar(nombres, vals, color=[cmap[cl] for cl in nombres], width=0.7)
            ax.set_ylim(0, 100)
            ax.set_ylabel("%")
        ax.set_title(SHORT.get(var, var), fontsize=10, loc="left")
        ax.tick_params(axis="x", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    for j in range(n, len(axes)):
        axes[j].axis("off")
    fig.suptitle(titulo, fontsize=12, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(IMG / fname, dpi=140)
    plt.close(fig)
    return fname


FILTROS = [
    ("alguna", "alguna_violencia", "Alguna violencia (psic o fís o sexual)"),
    ("psic", "viol_psicologica_12m", "Violencia psicológica 12m"),
    ("fis", "viol_fisica_12m", "Violencia física 12m"),
    ("sex", "viol_sexual_12m", "Violencia sexual 12m"),
]


def top_range(tab: pd.DataFrame, nucleo: list[str], n: int = 4) -> list[tuple[str, float, str, str]]:
    out = []
    for v in nucleo:
        a = float(tab[v].max())
        b = float(tab[v].min())
        hi = str(tab.loc[tab[v].idxmax(), "cluster"])
        lo = str(tab.loc[tab[v].idxmin(), "cluster"])
        out.append((v, a - b, hi, lo))
    out.sort(key=lambda t: t[1], reverse=True)
    return out[:n]


def fmt_val(var: str, x: float) -> str:
    if var == "edad":
        return f"{x:.1f} años"
    return fmt_pct(x)


def pc_lados(pca: PCA, nucleo: list[str], eje: int, n: int = 3):
    load = pca.components_[eje]
    ranked = sorted(
        [(abs(load[i]), nucleo[i], float(load[i])) for i in range(len(nucleo))],
        reverse=True,
    )[:n]
    pos = [SHORT.get(v, v) for _, v, s in ranked if s > 0]
    neg = [SHORT.get(v, v) for _, v, s in ranked if s < 0]
    return ranked, pos, neg


def interpret_filtro(n_si: int, N_si: float, n_no: int, N_no: float, N_all: float, nombre: str) -> str:
    return (
        f"Esta barra parte la muestra *antes* del k-medias. "
        f"Sí = reportó `{nombre}`; no = no la reportó.\n\n"
        f"El {fmt_pct(N_si / N_all)} de la N (n={n_si:,}) entra al "
        f"cluster de las que sí; el {fmt_pct(N_no / N_all)} (n={n_no:,}) al de las que no. "
        "Esta Y no entra al agrupamiento: solo las 13 X. "
        "Si el filtro es un tipo (p. ej. física), las del “no” igual pueden tener psicológica o sexual."
    )


def interpret_pca(tab: pd.DataFrame, pca: PCA, nucleo: list[str]) -> str:
    v1, v2 = 100 * pca.explained_variance_ratio_
    _, pos1, neg1 = pc_lados(pca, nucleo, 0)
    _, pos2, neg2 = pc_lados(pca, nucleo, 1)
    grande = tab.loc[tab["n"].idxmax()]
    chico = tab.loc[tab["n"].idxmin()]
    flaco = (
        f" `{chico['cluster']}` tiene n={int(chico['n']):,}: es un cajón chico, no un perfil para armar política."
        if chico["n"] < 250
        else ""
    )
    der = ", ".join(pos1) if pos1 else "esas X de la derecha del biplot"
    izq = ", ".join(neg1) if neg1 else "esas X de la izquierda"
    return (
        f"Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. "
        "Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. "
        "PC = componente principal = un eje resumen (un combo de las 13 X). "
        "No es violencia: es un resumen de casa / actitudes / colegio.\n\n"
        f"**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas "
        f"({v1:.0f} % de toda la variación de las 13 X). "
        f"A la **derecha** tiende a haber más: {der}. "
        f"A la **izquierda**, más: {izq}.\n\n"
        f"**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero "
        f"({v2:.0f} %). "
        f"Arriba: {', '.join(pos2) if pos2 else '—'}. "
        f"Abajo: {', '.join(neg2) if neg2 else '—'}.\n\n"
        f"PC1+PC2 solo muestran {v1 + v2:.0f} % de cómo se distinguen las X. "
        f"El otro {100 - (v1 + v2):.0f} % no cabe en el plano: por eso los colores se mezclan. "
        "No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. "
        "La cruz blanca es el centro de cada tipo. "
        f"`{grande['cluster']}` es el más grande (n={int(grande['n']):,})."
        f"{flaco}"
    )


def interpret_biplot(pca: PCA, nucleo: list[str]) -> str:
    r1, pos1, neg1 = pc_lados(pca, nucleo, 0)
    r2, pos2, neg2 = pc_lados(pca, nucleo, 1)
    det1 = ", ".join(
        f"{SHORT.get(v, v)} ({'suma' if s > 0 else 'resta'} al PC1)"
        for _, v, s in r1
    )
    det2 = ", ".join(
        f"{SHORT.get(v, v)} ({'suma' if s > 0 else 'resta'} al PC2)"
        for _, v, s in r2
    )
    return (
        "Cada flecha es **una** de las 13 X. "
        "Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. "
        "Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.\n\n"
        f"PC1: un eje “{', '.join(pos1) if pos1 else '—'} vs "
        f"{', '.join(neg1) if neg1 else '—'}”. "
        f"Las que más pesan: {det1}. "
        "Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, "
        "tener voz en casa y vivir peleas no tiran para el mismo lado.\n\n"
        f"PC2: un segundo eje “{', '.join(pos2) if pos2 else '—'} vs "
        f"{', '.join(neg2) if neg2 else '—'}”. "
        f"Pesan: {det2}."
    )


def interpret_vars(tab: pd.DataFrame, nucleo: list[str]) -> str:
    tops = top_range(tab, nucleo, 4)
    bits = []
    for v, rng, hi, lo in tops:
        hv = float(tab.loc[tab["cluster"] == hi, v].iloc[0])
        lv = float(tab.loc[tab["cluster"] == lo, v].iloc[0])
        bits.append(
            f"**{SHORT.get(v, v)}:** `{hi}` tiene {fmt_val(v, hv)} y `{lo}` {fmt_val(v, lv)}. "
            "El k-medias usó esta X para apartar esos dos tipos."
        )
    extra = []
    for _, r in tab.iterrows():
        if r.get("ie_mujeres", 0) > 0.95:
            extra.append(
                f"`{r['cluster']}` es casi 100 % colegio de mujeres: el grupo se separa por el tipo de escuela."
            )
        if r.get("falta_colegio", 0) > 0.95:
            extra.append(
                f"`{r['cluster']}` es casi 100 % “falta al colegio”: grupo flaco definido por una sola X."
            )
        if r.get("act_padres_golpear", 0) > 0.95:
            extra.append(
                f"`{r['cluster']}` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto."
            )
        if r.get("vive_tio", 0) > 0.95:
            extra.append(
                f"`{r['cluster']}` es casi 100 % “vive con tío”."
            )
        if r.get("act_trabajar", 0) > 0.95:
            extra.append(
                f"`{r['cluster']}` es casi 100 % “debe trabajar si falta plata”."
            )
    tail = ("\n\n" + " ".join(extra)) if extra else ""
    return (
        "Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.\n\n"
        + "\n\n".join(bits)
        + tail
    )


def interpret_y(tab: pd.DataFrame, ycol: str, lado: str) -> str:
    bits = []
    for _, r in tab.iterrows():
        bits.append(
            f"`{r['cluster']}` (n={int(r['n']):,}): psicológica {fmt_pct(r['viol_psicologica_12m'])}, "
            f"física {fmt_pct(r['viol_fisica_12m'])}, "
            f"sexual {fmt_pct(r['viol_sexual_12m'])}."
        )
    if lado == "si":
        nota = (
            f"Aquí **todas** ya tienen `{ycol}` = 1 (por el filtro). "
            "Si un grupo tiene más física o más sexual que otro, ese tipo de casa/actitud "
            "se junta más con violencia **superpuesta**, no con “descubrir” el filtro."
        )
    else:
        nota = (
            f"Aquí `{ycol}` = 0 para todas. "
            "Un % > 0 de psicológica/física/sexual es **otra** violencia, no la del filtro. "
            "Si los tres % son 0, este lado es “no reportó ninguna” (solo pasa con el filtro *alguna*)."
        )
    return (
        "Violencia 12m **después** de armar el grupo. No se usó para clusterizar.\n\n"
        + "\n".join(bits)
        + "\n\n"
        + nota
    )


def interpret_edad(tab: pd.DataFrame) -> str:
    hi = tab.loc[tab["edad"].idxmax()]
    lo = tab.loc[tab["edad"].idxmin()]
    d = float(hi["edad"] - lo["edad"])
    impl = (
        "La edad no es lo que parte estos tipos."
        if d < 0.4
        else (
            f"`{lo['cluster']}` es un poco más joven. "
            "Eso no se lee como más violencia: mira el gráfico de las tres Y."
        )
    )
    return (
        "Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).\n\n"
        f"`{lo['cluster']}` = {lo['edad']:.2f} años; `{hi['cluster']}` = {hi['edad']:.2f} "
        f"(brecha {d:.2f}). {impl}"
    )


def run_lado(
    work: pd.DataFrame,
    nucleo: list[str],
    tag: str,
    titulo: str,
    ycol: str,
) -> dict:
    lab, sil = fit_kmeans(work, nucleo, K)
    tab = describe(work, nucleo, lab, f"{tag}-", ycol)
    df = work.copy()
    df["cluster"] = [f"{tag}-{i}" for i in remap_labels(lab, tab)]
    tab["cluster"] = [f"{tag}-{i}" for i in range(1, K + 1)]
    nombres = tab["cluster"].tolist()
    figs = charts_lado(tab, nucleo, tag, titulo)
    pca_f, pca, _ = plot_pca_map(
        df[nucleo],
        df["cluster"],
        nombres,
        f"{titulo} — k-medias, 13 X LASSO (PCA 2D). Cruces = centros.",
        f"perfiles_{tag}_pca.png",
    )
    bi = plot_biplot(
        pca,
        nucleo,
        f"{titulo} — cada X en el plano PCA",
        f"perfiles_{tag}_biplot.png",
    )
    pan = plot_var_panels(
        df,
        nucleo,
        nombres,
        f"{titulo} — cada una de las 13 X",
        f"perfiles_{tag}_vars.png",
    )
    return {
        "df": df,
        "tab": tab,
        "sil": sil,
        "pca": pca,
        "pca_f": pca_f,
        "bi": bi,
        "pan": pan,
        "figs": figs,
        "n": len(df),
        "N": float(df["w"].sum()),
    }


def bloque_lado(res: dict, nucleo: list[str], ycol: str, lado: str, titulo: str) -> str:
    tab = res["tab"]
    return f"""### {titulo}

n = {res['n']:,} · N = {fmt_n(res['N'])} · silueta k={K}: **{res['sil']:.3f}**

{sil_table(res['df'], nucleo)}

{md_means(tab, nucleo, con_y=True)}

#### Mapa PCA

![{res['pca_f']}]({IMG_MD}/{res['pca_f']})

{interpret_pca(tab, res['pca'], nucleo)}

#### Biplot (cada variable)

![{res['bi']}]({IMG_MD}/{res['bi']})

{interpret_biplot(res['pca'], nucleo)}

#### Una barra por variable

![{res['pan']}]({IMG_MD}/{res['pan']})

{interpret_vars(tab, nucleo)}

#### Barras de las 13 X juntas

![{res['figs'][0]}]({IMG_MD}/{res['figs'][0]})

{interpret_vars(tab, nucleo)}

#### Edad

![{res['figs'][1]}]({IMG_MD}/{res['figs'][1]})

{interpret_edad(tab)}

#### Cruce con los tres tipos de violencia

![{res['figs'][2]}]({IMG_MD}/{res['figs'][2]})

{interpret_y(tab, ycol, lado)}
"""


def guia_no_tecnica(n_all: int, N_all: float) -> str:
    return f"""## Cómo está armado

Agrupa alumnas parecidas en casa, actitudes y colegio (las 13 X que el LASSO dejó en los tres targets). La violencia no entra al agrupamiento; se cuenta después.

n = {n_all:,} alumnas en estas tablas. N = {fmt_n(N_all)} (peso `FACTOR_ALUMNOS`). Se parte en sí y no, y dentro de cada lado se piden 3 grupos. k = 3 es un recorte. Silueta cerca de 0.1–0.15: los grupos se parecen.

Si el filtro es física = no, esa alumna puede tener psicológica o sexual. Las tres Y se muestran siempre. Solo con *alguna violencia = no* las tres quedan en 0 %.

El mapa PCA muestra cerca del 20 % de las diferencias entre las 13 preguntas. El nombre del grupo sale de qué barras están más altas, no del mapa. Un grupo con n chico no se lee como si fuera un tercio del país.

Reglas SI–ENTONCES: [perfiles_cart_crs04.md](perfiles_cart_crs04.md). Las 13 variables: [lasso_crs04.md](lasso_crs04.md).
"""


def main() -> None:
    nucleo, meta = nucleo_lasso()
    df = load()
    work = df.dropna(subset=nucleo + YCOLS + ["alguna_violencia", "w"]).copy()
    n_all, N_all = len(work), float(work["w"].sum())

    usadas = meta.loc[meta["en_kmeans"]]
    fuera = meta.loc[~meta["en_kmeans"]]

    def lista_vars(tabv: pd.DataFrame) -> str:
        lines = [
            "| Variable | Qué es | En cuántos LASSO | ¿Entra al k-medias? |",
            "| --- | --- | ---: | --- |",
        ]
        for _, r in tabv.iterrows():
            entra = "sí (3/3)" if r["en_kmeans"] else "no"
            lines.append(
                f"| `{r['variable']}` | {r['label']} | {r['n_targets']}/3 | {entra} |"
            )
        return "\n".join(lines)

    piezas = []
    asig_parts = []
    for key, ycol, nombre in FILTROS:
        si = work.loc[work[ycol] == 1].copy()
        no = work.loc[work[ycol] == 0].copy()
        bar_simple(
            f"perfiles_{key}_filtro.svg",
            [
                (f"Sí {key}", 100.0 * float(si["w"].sum()) / N_all, C2),
                (f"No {key}", 100.0 * float(no["w"].sum()) / N_all, C1),
            ],
            f"Filtro (antes del k-medias): {nombre}",
            "%",
        )
        res_si = run_lado(si, nucleo, f"{key}_si", f"Sí {nombre}", ycol)
        res_no = run_lado(no, nucleo, f"{key}_no", f"No {nombre}", ycol)
        asig_parts.append(
            res_si["df"][
                ["ID", "COLEGIAL_ID", "w", "alguna_violencia", *YCOLS, "cluster"]
            ].assign(filtro=key, universo="si")
        )
        asig_parts.append(
            res_no["df"][
                ["ID", "COLEGIAL_ID", "w", "alguna_violencia", *YCOLS, "cluster"]
            ].assign(filtro=key, universo="no")
        )
        piezas.append(
            f"## {nombre}\n\n"
            f"{interpret_filtro(res_si['n'], res_si['N'], res_no['n'], res_no['N'], N_all, ycol)}\n\n"
            f"![Filtro {key}]({IMG_MD}/perfiles_{key}_filtro.svg)\n\n"
            f"{bloque_lado(res_si, nucleo, ycol, 'si', f'Las que sí — {nombre}')}\n"
            f"{bloque_lado(res_no, nucleo, ycol, 'no', f'Las que no — {nombre}')}\n"
        )
        print(f"{key}: si n={res_si['n']} sil={res_si['sil']:.3f} | no n={res_no['n']} sil={res_no['sil']:.3f}")

    ASIG.parent.mkdir(parents=True, exist_ok=True)
    with ASIG.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# Cluster por alumna (filtro, universo, cluster). Sale de perfiles_kmeans_crs04.py.\n")
        pd.concat(asig_parts, ignore_index=True).to_csv(fh, index=False)

    md = f"""# k-medias CRS04 por tipo de violencia

{ficha(
    "Tipos de alumna **dentro** de las que sí reportaron una violencia y **dentro** de las que no. Primero se filtra; después se agrupa. X = las 13 del LASSO 3/3.",
    script="scripts/modelos/perfiles_kmeans_crs04.py",
)}
{guia_no_tecnica(n_all, N_all)}

Selección de X: [lasso_crs04.md](lasso_crs04.md). Coeficientes: `data/tablas/lasso_crs04_coef.csv`.

## Qué X usó (primer filtro LASSO)

Coef ≠ 0 en los tres targets. Son {len(nucleo)}: {", ".join(f"`{v}`" for v in nucleo)}.

### Entran ({len(nucleo)})

{lista_vars(usadas)}

### No entran

{lista_vars(fuera)}

---

{"".join(piezas)}
Asignación: `data/tablas/perfiles_kmeans_asig.csv` (columnas `filtro`, `universo`, `cluster`).
"""
    asegurar_docs()
    DOC.write_text(md, encoding="utf-8")
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
