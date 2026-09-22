"""Descriptivos de controles CRS04 (alumnas) y CRS01 (vivienda).

Uso:
    python scripts/descriptivos/descriptivos_controles.py

Escribe docs/descriptivos/descriptivos_controles.md y docs/img/controles_*.svg
"""

from __future__ import annotations

from pathlib import Path

import duckdb

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import DB, DOC_DESC, IMG, IMG_MD, asegurar_docs, ficha

DOC = DOC_DESC / "descriptivos_controles.md"

YES = "#c2410c"
INK = "#1c1917"
MUTED = "#78716c"
GRID = "#e7e5e4"
BG = "#fafaf9"
BAR = "#0369a1"
PSIC = "#b45309"
FIS = "#c2410c"
SEX = "#7c3aed"


def inventory_appendix() -> str:
    return (
        "\n\n---\n\n"
        "## Dónde está el resto\n\n"
        "Diccionario de preguntas: [inventario_crs04.md](inventario_crs04.md) y "
        "[inventario_crs01.md](inventario_crs01.md).\n\n"
        "Qué se pregunta a ambas (y qué no): "
        "[descriptivos_crs01_vs_crs04.md](descriptivos_crs01_vs_crs04.md).\n\n"
        "Qué recode entra al modelo: "
        "[../metodologia/metodologia.md](../metodologia/metodologia.md).\n"
    )


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_n(x: float | int | None) -> str:
    if x is None:
        return "0"
    return f"{int(round(x)):,}"


def fmt_pct(part: float, total: float) -> str:
    if not total:
        return "—"
    return f"{100.0 * part / total:.1f}%"


def write_svg(name: str, body: str) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / name).write_text(body, encoding="utf-8")


def bar_h(name: str, rows: list[tuple[str, float]], caption: str, width: int = 920) -> None:
    left, right, top, row_h, gap = 200, 56, 28, 28, 10
    bar_w = width - left - right
    height = top + len(rows) * (row_h + gap) + 20
    xmax = max((v for _, v in rows), default=1) or 1
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f"<title>{esc(caption)}</title>",
        f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        f'<text x="{left}" y="18" fill="{MUTED}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(caption)}</text>',
    ]
    y = top + 4
    for label, value in rows:
        w = bar_w * value / xmax
        parts += [
            f'<text x="{left - 8}" y="{y + 19}" text-anchor="end" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(label)}</text>',
            f'<rect x="{left}" y="{y}" width="{max(w, 1):.1f}" height="{row_h}" fill="{BAR}" rx="3"/>',
            f'<text x="{left + w + 6:.1f}" y="{y + 19}" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{value:.1f}%</text>',
        ]
        y += row_h + gap
    parts.append("</svg>")
    write_svg(name, "\n".join(parts))


def grouped_h(
    name: str,
    categories: list[str],
    series: list[tuple[str, list[float], str]],
    caption: str,
    width: int = 920,
) -> None:
    left, right, top, row_h, gap = 168, 24, 36, 46, 12
    bar_w = width - left - right
    height = top + len(categories) * (row_h + gap) + 36
    n_s = len(series)
    inner = 10
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
            w = bar_w * vals[i] / 100.0
            yy = y + j * one
            parts.append(
                f'<rect x="{left}" y="{yy:.1f}" width="{max(w, 1):.1f}" height="{one - 2:.1f}" '
                f'fill="{color}" rx="2"/>'
            )
            parts.append(
                f'<text x="{left + w + 4:.1f}" y="{yy + one - 5:.1f}" fill="{INK}" font-size="10" '
                f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{vals[i]:.1f}</text>'
            )
        y += row_h + gap
    lx = left
    for lab, _vals, color in series:
        parts += [
            f'<rect x="{lx}" y="{height - 18}" width="10" height="10" fill="{color}" rx="2"/>',
            f'<text x="{lx + 14}" y="{height - 9}" fill="{INK}" font-size="11" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(lab)}</text>',
        ]
        lx += 140
    parts.append("</svg>")
    write_svg(name, "\n".join(parts))


def md_table(headers: list[str], rows: list[list[str]], right: set[int] | None = None) -> str:
    right = right or set()
    align = []
    for i, _h in enumerate(headers):
        align.append("---:" if i in right else "---")
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(align) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def any_eq(cols: list[str], value: int = 1) -> str:
    return "(" + " OR ".join(f"{c} = {value}" for c in cols) + ")"


def build_crs04(con: duckdb.DuckDBPyConnection) -> None:
    psic_h = [f"C3P201_{i}" for i in range(1, 12)]
    fis_h = [f"C3P205_{i}" for i in range(1, 8)]
    psic_c = [f"C3P223_{i}" for i in range(1, 15)]
    fis_c = [f"C3P227_{i}" for i in range(1, 11)]
    sex = [f"(C4P248_{i} = 1 AND C4P248C_{i} = 1)" for i in range(1, 17)]
    disc = [f"C4P130_{i} = 1" for i in range(1, 7)]
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE alumna AS
        SELECT
            *,
            FACTOR_ALUMNOS AS w,
            CASE AREA WHEN 1 THEN 'Urbano' WHEN 2 THEN 'Rural' END AS area_lab,
            CASE
                WHEN C3P105 = 2 THEN 'CAR'
                WHEN C3P114_VS = 1 THEN 'vive sola'
                WHEN C3P115_3 = 1 OR C3P115_4 = 1 THEN 'padrastro/madrastra'
                WHEN C3P115_1 = 1 AND C3P115_2 = 1 THEN 'ambos padres'
                WHEN C3P115_1 = 1 THEN 'solo madre'
                WHEN C3P115_2 = 1 THEN 'solo padre'
                WHEN C3P115_1 IS NULL THEN 'missing'
                ELSE 'otros'
            END AS composicion,
            CASE
                WHEN C3P105 = 2 OR C3P114_PERS IS NULL THEN 'missing/CAR'
                WHEN C3P114_VS = 1 OR C3P114_PERS <= 1 THEN '1'
                WHEN C3P114_PERS BETWEEN 2 AND 3 THEN '2-3'
                WHEN C3P114_PERS BETWEEN 4 AND 5 THEN '4-5'
                ELSE '6+'
            END AS tamano,
            CASE
                WHEN C3P120 IS NULL THEN 'missing'
                WHEN C3P120 = 1 THEN 'madre'
                WHEN C3P120 = 2 THEN 'padre'
                WHEN C3P120 IN (5, 6) THEN 'hermanos'
                WHEN C3P120 IN (7, 8) THEN 'abuelos'
                ELSE 'otros'
            END AS cuidador,
            CASE
                WHEN C3P128 IS NULL THEN 'missing'
                WHEN C3P128 = 1 THEN 'castellano'
                WHEN C3P128 = 2 THEN 'quechua'
                WHEN C3P128 = 3 THEN 'aimara'
                WHEN C3P128 = 6 THEN 'no sabe'
                ELSE 'otra'
            END AS idioma,
            CASE
                WHEN C3P302_4 = 2 THEN 'madre'
                WHEN C3P302_4 = 3 THEN 'padre'
                WHEN C3P302_4 = 1 THEN 'ella'
                WHEN C3P302_4 IN (4, 5) THEN 'hermanos'
                ELSE 'otros'
            END AS quien_dinero,
            CASE
                WHEN C4P129 = 1 THEN 'quechua'
                WHEN C4P129 = 2 THEN 'aimara'
                WHEN C4P129 IN (3, 4) THEN 'amazonia/otro pueblo'
                WHEN C4P129 = 5 THEN 'afroperuana'
                WHEN C4P129 = 6 THEN 'blanca'
                WHEN C4P129 = 7 THEN 'mestiza'
                WHEN C4P129 = 8 THEN 'otro'
                ELSE 'no sabe'
            END AS etnia,
            ({any_eq(psic_h)} AND C3P203 = 1) AS psic_hogar_12m,
            ({any_eq(fis_h)} AND C3P207 = 1) AS fis_hogar_12m,
            ({any_eq(psic_c)} AND C3P225 = 1) AS psic_col_12m,
            ({any_eq(fis_c)} AND C3P229 = 1) AS fis_col_12m,
            ({" OR ".join(sex)}) AS sexual_12m,
            (({any_eq(psic_h)} AND C3P203 = 1) OR ({any_eq(psic_c)} AND C3P225 = 1)) AS viol_psicologica_12m,
            (({any_eq(fis_h)} AND C3P207 = 1) OR ({any_eq(fis_c)} AND C3P229 = 1)) AS viol_fisica_12m,
            ({" OR ".join(sex)}) AS viol_sexual_12m,
            ({" OR ".join(disc)}) AS discapacidad
        FROM analisis.crs04_adolescentes
        WHERE SEXO = 1
        """
    )


def weighted_levels(con: duckdb.DuckDBPyConnection, col: str, order: str | None = None) -> list[tuple]:
    extra = f"ORDER BY {order}" if order else f"ORDER BY {col}"
    return con.execute(
        f"""
        SELECT {col}, COUNT(*) AS n, SUM(w) AS Nexp
        FROM alumna
        GROUP BY 1
        {extra}
        """
    ).fetchall()


def dist_rows(rows: list[tuple], total_n: float, total_N: float) -> list[list[str]]:
    out = []
    for lab, n, nexp in rows:
        out.append(
            [
                str(lab),
                fmt_n(n),
                fmt_pct(n, total_n),
                fmt_n(nexp),
                fmt_pct(nexp, total_N),
            ]
        )
    return out


def cross_outcome(con: duckdb.DuckDBPyConnection, col: str) -> list[tuple]:
    return con.execute(
        f"""
        SELECT
            {col},
            COUNT(*) AS n,
            SUM(w) AS Nexp,
            SUM(w * CAST(viol_psicologica_12m AS INT)) / SUM(w) AS p_psic,
            SUM(w * CAST(viol_fisica_12m AS INT)) / SUM(w) AS p_fis,
            SUM(w * CAST(viol_sexual_12m AS INT)) / SUM(w) AS p_sex
        FROM alumna
        GROUP BY 1
        ORDER BY 1
        """
    ).fetchall()


def main() -> None:
    con = duckdb.connect(str(DB), read_only=True)
    build_crs04(con)

    n_m, n_exp = con.execute("SELECT COUNT(*), SUM(w) FROM alumna").fetchone()
    overlap = con.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT ID FROM raw.crs01_cap100
            INTERSECT
            SELECT ID FROM raw.crs04_cap100
        )
        """
    ).fetchone()[0]

    area = weighted_levels(con, "area_lab", "CASE area_lab WHEN 'Urbano' THEN 1 ELSE 2 END")
    edad = weighted_levels(con, "EDAD", "EDAD")
    tamano = weighted_levels(con, "tamano", "CASE tamano WHEN '1' THEN 1 WHEN '2-3' THEN 2 WHEN '4-5' THEN 3 WHEN '6+' THEN 4 ELSE 5 END")
    comp = weighted_levels(
        con,
        "composicion",
        """CASE composicion
            WHEN 'ambos padres' THEN 1 WHEN 'solo madre' THEN 2 WHEN 'solo padre' THEN 3
            WHEN 'padrastro/madrastra' THEN 4 WHEN 'otros' THEN 5 WHEN 'vive sola' THEN 6
            WHEN 'CAR' THEN 7 ELSE 8 END""",
    )
    cuidador = weighted_levels(
        con,
        "cuidador",
        """CASE cuidador WHEN 'madre' THEN 1 WHEN 'padre' THEN 2 WHEN 'abuelos' THEN 3
            WHEN 'hermanos' THEN 4 WHEN 'otros' THEN 5 ELSE 6 END""",
    )
    idioma = weighted_levels(
        con,
        "idioma",
        """CASE idioma WHEN 'castellano' THEN 1 WHEN 'quechua' THEN 2 WHEN 'aimara' THEN 3
            WHEN 'otra' THEN 4 WHEN 'no sabe' THEN 5 ELSE 6 END""",
    )
    etnia = weighted_levels(con, "etnia", "Nexp DESC")
    dinero = weighted_levels(
        con,
        "quien_dinero",
        """CASE quien_dinero WHEN 'madre' THEN 1 WHEN 'padre' THEN 2 WHEN 'ella' THEN 3
            WHEN 'hermanos' THEN 4 ELSE 5 END""",
    )
    depto = weighted_levels(con, "DEPARTAMENTO", "Nexp DESC")
    vive_dist = weighted_levels(con, "C3P104", "C3P104")
    mig5 = weighted_levels(con, "C4P104B", "C4P104B")
    madre_nacio = weighted_levels(con, "C4P104D", "C4P104D")
    ined = weighted_levels(con, "INED", "INED")
    turno = weighted_levels(con, "TURNO", "TURNO")
    anio = weighted_levels(con, "C3ANIO", "C3ANIO")
    nied = weighted_levels(con, "NIED", "NIED")
    tiedba = weighted_levels(con, "TIEDBA", "TIEDBA")
    casa = weighted_levels(con, "C3P105", "C3P105")
    mama = weighted_levels(con, "C3P106", "C3P106")
    papa = weighted_levels(con, "C3P110", "C3P110")
    sola_cuarto = weighted_levels(con, "C3P118_12", "C3P118_12")
    sola_cama = weighted_levels(con, "C3P119_12", "C3P119_12")
    cuida_trabaja = weighted_levels(con, "C3P120A", "C3P120A")
    queda_sola = weighted_levels(con, "C3P120B", "C3P120B")
    sin_comer = weighted_levels(con, "C3P121", "C3P121")
    no_colegio = weighted_levels(con, "C3P122", "C3P122")
    peleas = weighted_levels(con, "C3P123", "C3P123")
    opinan = weighted_levels(con, "C3P126", "C3P126")
    disc = weighted_levels(con, "discapacidad", "discapacidad")
    pers_stats = con.execute(
        """
        SELECT
            MIN(C3P114_PERS) FILTER (WHERE C3P114_PERS IS NOT NULL),
            MAX(C3P114_PERS) FILTER (WHERE C3P114_PERS IS NOT NULL),
            SUM(w * C3P114_PERS) / SUM(w) FILTER (WHERE C3P114_PERS IS NOT NULL),
            SUM(CASE WHEN C3P114_PERS IS NULL THEN 1 ELSE 0 END)
        FROM alumna
        """
    ).fetchone()

    x_area = cross_outcome(con, "area_lab")
    x_edad = cross_outcome(con, "EDAD")
    x_tam = cross_outcome(con, "tamano")
    x_cuid = cross_outcome(con, "cuidador")
    x_idio = cross_outcome(con, "idioma")
    x_121 = cross_outcome(con, "C3P121")
    x_123 = cross_outcome(con, "C3P123")

    # CRS01 vivienda
    n_viv, n_viv_exp = con.execute(
        "SELECT COUNT(*), SUM(FACTOR_VIV) FROM raw.crs01_cap100"
    ).fetchone()
    activos = [
        (1, "Refrigeradora/congeladora"),
        (2, "Lavadora"),
        (3, "Computadora/laptop/tablet"),
        (4, "Internet"),
        (5, "TV cable/satelital"),
        (6, "Teléfono fijo"),
        (7, "Celular"),
        (8, "Microondas"),
        (9, "Servicio doméstico"),
        (10, "Equipo de sonido"),
        (11, "Televisor a color"),
        (12, "Cocina a gas"),
        (13, "Licuadora"),
        (14, "Plancha eléctrica"),
        (15, "Auto/camioneta particular"),
        (16, "Bicicleta"),
        (17, "Motocicleta"),
        (18, "Triciclo"),
        (19, "Mototaxi"),
        (20, "Camión"),
        (21, "Otro"),
    ]
    asset_rows = []
    for i, lab in activos:
        n_si, nexp_si = con.execute(
            f"""
            SELECT
                SUM(CASE WHEN C1P110_{i} = 1 THEN 1 ELSE 0 END),
                SUM(CASE WHEN C1P110_{i} = 1 THEN FACTOR_VIV ELSE 0 END)
            FROM raw.crs01_cap100
            """
        ).fetchone()
        asset_rows.append((lab, n_si, nexp_si, nexp_si / n_viv_exp))

    serv = con.execute(
        """
        SELECT
            AREA,
            COUNT(*) AS n,
            SUM(FACTOR_VIV) AS Nexp,
            SUM(FACTOR_VIV * CAST(C1P105 = 1 AS INT)) / SUM(FACTOR_VIV) AS elec,
            SUM(FACTOR_VIV * CAST(C1P106 = 1 AS INT)) / SUM(FACTOR_VIV) AS agua,
            SUM(FACTOR_VIV * CAST(C1P107 IN (1, 2) AS INT)) / SUM(FACTOR_VIV) AS desague,
            SUM(FACTOR_VIV * (
                CAST(C1P110_1=1 AS INT)+CAST(C1P110_2=1 AS INT)+CAST(C1P110_3=1 AS INT)+
                CAST(C1P110_4=1 AS INT)+CAST(C1P110_5=1 AS INT)+CAST(C1P110_6=1 AS INT)+
                CAST(C1P110_7=1 AS INT)+CAST(C1P110_8=1 AS INT)+CAST(C1P110_9=1 AS INT)+
                CAST(C1P110_10=1 AS INT)+CAST(C1P110_11=1 AS INT)+CAST(C1P110_12=1 AS INT)+
                CAST(C1P110_13=1 AS INT)+CAST(C1P110_14=1 AS INT)+CAST(C1P110_15=1 AS INT)+
                CAST(C1P110_16=1 AS INT)+CAST(C1P110_17=1 AS INT)+CAST(C1P110_18=1 AS INT)+
                CAST(C1P110_19=1 AS INT)+CAST(C1P110_20=1 AS INT)
            )) / SUM(FACTOR_VIV) AS idx
        FROM raw.crs01_cap100
        GROUP BY 1
        ORDER BY 1
        """
    ).fetchall()

    depto_viv = con.execute(
        """
        SELECT DEPARTAMENTO, COUNT(*), SUM(FACTOR_VIV),
            SUM(FACTOR_VIV * CAST(C1P105 = 1 AS INT)) / SUM(FACTOR_VIV) AS elec,
            SUM(FACTOR_VIV * CAST(C1P106 = 1 AS INT)) / SUM(FACTOR_VIV) AS agua,
            SUM(FACTOR_VIV * CAST(C1P107 IN (1, 2) AS INT)) / SUM(FACTOR_VIV) AS desague,
            SUM(FACTOR_VIV * (
                CAST(C1P110_1=1 AS INT)+CAST(C1P110_2=1 AS INT)+CAST(C1P110_3=1 AS INT)+
                CAST(C1P110_4=1 AS INT)+CAST(C1P110_5=1 AS INT)+CAST(C1P110_6=1 AS INT)+
                CAST(C1P110_7=1 AS INT)+CAST(C1P110_8=1 AS INT)+CAST(C1P110_9=1 AS INT)+
                CAST(C1P110_10=1 AS INT)+CAST(C1P110_11=1 AS INT)+CAST(C1P110_12=1 AS INT)+
                CAST(C1P110_13=1 AS INT)+CAST(C1P110_14=1 AS INT)+CAST(C1P110_15=1 AS INT)+
                CAST(C1P110_16=1 AS INT)+CAST(C1P110_17=1 AS INT)+CAST(C1P110_18=1 AS INT)+
                CAST(C1P110_19=1 AS INT)+CAST(C1P110_20=1 AS INT)
            )) / SUM(FACTOR_VIV) AS idx
        FROM raw.crs01_cap100
        GROUP BY 1
        ORDER BY 3 DESC
        LIMIT 6
        """
    ).fetchall()

    tipo_viv = con.execute(
        """
        SELECT C1P101, COUNT(*), SUM(FACTOR_VIV)
        FROM raw.crs01_cap100 GROUP BY 1 ORDER BY 1
        """
    ).fetchall()
    tipo_lab = {
        1: "Casa independiente",
        2: "Departamento",
        3: "Quinta",
        4: "Casa de vecindad",
        5: "Choza o cabaña",
        6: "Improvisada",
        7: "Local no habitacional",
        8: "Otro",
    }
    hab = con.execute(
        """
        SELECT
            SUM(FACTOR_VIV * C1P108) / SUM(FACTOR_VIV),
            SUM(FACTOR_VIV * C1P109) / SUM(FACTOR_VIV),
            SUM(CASE WHEN C1P108 IS NULL THEN 1 ELSE 0 END),
            SUM(CASE WHEN C1P109 IS NULL THEN 1 ELSE 0 END)
        FROM raw.crs01_cap100
        """
    ).fetchone()

    # charts
    bar_h(
        "controles_crs04_area.svg",
        [(lab, 100 * nexp / n_exp) for lab, _n, nexp in area],
        "Área de la IE · alumnas SEXO=1 · FACTOR_ALUMNOS",
    )
    bar_h(
        "controles_crs04_edad.svg",
        [(str(int(e)), 100 * nexp / n_exp) for e, _n, nexp in edad],
        "Edad · alumnas · FACTOR_ALUMNOS",
    )
    bar_h(
        "controles_crs04_tamano.svg",
        [(lab, 100 * nexp / n_exp) for lab, _n, nexp in tamano],
        "Personas en el hogar (C3P114_PERS) · tramos",
    )
    bar_h(
        "controles_crs04_composicion.svg",
        [(lab, 100 * nexp / n_exp) for lab, _n, nexp in comp],
        "Con quién vive (recode C3P105 / C3P115)",
    )
    bar_h(
        "controles_crs04_cuidador.svg",
        [(lab, 100 * nexp / n_exp) for lab, _n, nexp in cuidador],
        "Quién cuida la mayor parte del tiempo (C3P120 recode)",
    )
    bar_h(
        "controles_crs04_idioma.svg",
        [(lab, 100 * nexp / n_exp) for lab, _n, nexp in idioma],
        "Idioma en el hogar (C3P128 recode)",
    )
    bar_h(
        "controles_crs01_activos.svg",
        [(lab, 100 * p) for lab, _n, _ne, p in asset_rows if lab != "Otro"],
        "% hogares con el activo (C1P110) · FACTOR_VIV · CRS01",
        width=920,
    )

    def series_from(cross: list[tuple], order: list) -> tuple[list[str], list[list[float]]]:
        mp = {row[0]: row for row in cross}
        cats, psic, fis, sexv = [], [], [], []
        for key in order:
            if key not in mp:
                continue
            row = mp[key]
            cats.append(str(key))
            psic.append(100 * row[3])
            fis.append(100 * row[4])
            sexv.append(100 * row[5])
        return cats, [psic, fis, sexv]

    c_area, s_area = series_from(x_area, ["Urbano", "Rural"])
    grouped_h(
        "controles_crs04_cruce_area.svg",
        c_area,
        [("Psicológica 12m", s_area[0], PSIC), ("Física 12m", s_area[1], FIS), ("Sexual 12m", s_area[2], SEX)],
        "% sí 12m por área de la IE · ponderado",
    )
    c_ed, s_ed = series_from(x_edad, [12, 13, 14, 15, 16, 17])
    grouped_h(
        "controles_crs04_cruce_edad.svg",
        [f"{c} años" for c in c_ed],
        [("Psicológica 12m", s_ed[0], PSIC), ("Física 12m", s_ed[1], FIS), ("Sexual 12m", s_ed[2], SEX)],
        "% sí 12m por edad · ponderado (mira no-linealidad)",
    )
    c_t, s_t = series_from(x_tam, ["1", "2-3", "4-5", "6+", "missing/CAR"])
    grouped_h(
        "controles_crs04_cruce_tamano.svg",
        c_t,
        [("Psicológica 12m", s_t[0], PSIC), ("Física 12m", s_t[1], FIS), ("Sexual 12m", s_t[2], SEX)],
        "% sí 12m por tamaño del hogar · ponderado",
    )

    serv_rows = []
    for area_i, _n, nexp, elec, agua, desague, idx in serv:
        lab = "Urbano" if area_i == 1 else "Rural"
        serv_rows.append((lab, 100 * elec, 100 * agua, 100 * desague, idx))
    grouped_h(
        "controles_crs01_servicios.svg",
        [r[0] for r in serv_rows],
        [
            ("Electricidad", [r[1] for r in serv_rows], BAR),
            ("Agua red dentro", [r[2] for r in serv_rows], "#0f766e"),
            ("Desagüe red", [r[3] for r in serv_rows], "#a16207"),
        ],
        "Servicios adecuados · hogares CRS01 · FACTOR_VIV",
    )

    def cross_md(cross: list[tuple], labeler=str) -> str:
        rows = []
        for lab, n, nexp, p_psic, p_fis, p_sex in cross:
            rows.append(
                [
                    labeler(lab),
                    fmt_n(n),
                    fmt_n(nexp),
                    f"{100 * p_psic:.1f}%",
                    f"{100 * p_fis:.1f}%",
                    f"{100 * p_sex:.1f}%",
                ]
            )
        return md_table(
            ["Grupo", "n", "N exp.", "% psic 12m", "% fís 12m", "% sexual 12m"],
            rows,
            {1, 2, 3, 4, 5},
        )

    lab_104 = {1: "Sí, vive en el distrito de la IE", 2: "No"}
    lab_mig = {1: "Sí", 2: "No", 3: "No sabe / no recuerda"}
    lab_ined = {1: "IE de mujeres", 2: "IE de hombres", 3: "Mixto"}
    lab_turno = {1: "Mañana", 2: "Tarde", 3: "Noche"}
    lab_si = {1: "Sí", 2: "No", None: "missing/skip (CAR)"}
    lab_120a = {1: "Sí trabaja", 2: "No", 3: "No sabe", None: "missing/skip"}
    lab_105 = {1: "Casa", 2: "CAR / albergue"}
    lab_118 = {0: "Comparte cuarto", 1: "Duerme sola en el cuarto", None: "skip (CAR)"}
    lab_119 = {0: "Comparte cama", 1: "Duerme sola en la cama", None: "skip (CAR o cuarto sola)"}
    lab_bool = {True: "Sí", False: "No", "true": "Sí", "false": "No"}

    inv = md_table(
        ["Variable", "Tipo", "Niveles / recode", "Missing", "En LASSO", "Prioridad"],
        [
            ["`AREA` (IE)", "dummy 2", "Urbano / rural", "0", "Dummy", "Alta"],
            ["`DEPARTAMENTO` (IE)", "categórica 25", "nombre", "0", "Group lasso o no meter individual", "Media (agregación)"],
            ["`C3P104` vive en distrito IE", "dummy", "sí / no", "0", "Dummy", "Media"],
            ["`C4P104B` vivía aquí hace 5 años", "dummy", "sí / no / NS", "0", "Dummy (común con C1)", "Media"],
            ["`C4P104D` madre vivía aquí al nacer", "dummy", "sí / no / NS", "0", "Dummy (común con C1)", "Baja"],
            ["`EDAD`", "continua 12–17", "igual a `C3P103EDAD`", "0", "Lineal; probar `edad^2`", "Alta"],
            ["`NIED` / `TIEDBA`", "constante", "todas secundaria regular", "0", "No: no varía", "Nula"],
            ["`INED`", "dummy", "mujeres / mixto (no hay solo hombres)", "0", "Dummy", "Baja"],
            ["`TURNO`", "dummy", "mañana / tarde (noche=0)", "0", "Dummy", "Baja"],
            ["`C3ANIO`", "ordinal 1–5", "año de estudio", "0", "Numérica o dummies", "Media"],
            ["`C3P105` casa vs CAR", "dummy", "casa / albergue", "0; CAR n=18", "Dummy o excluir CAR", "Baja (n chico)"],
            ["`composicion`", "categórica 7", "ambos / solo madre / solo padre / padrastro / otros / sola / CAR", "0 (recode cubre skip)", "Dummies; group lasso", "Alta"],
            ["`C3P114_PERS`", "continua 0–20", "personas en el hogar", "18 = CAR", "Lineal; probar `pers^2`", "Alta"],
            ["`C3P118_12` cuarto sola", "dummy", "0/1", "18 CAR", "Dummy", "Media (hacinamiento)"],
            ["`C3P119_12` cama sola", "dummy", "0/1", "skip si cuarto sola", "Cuidado: skip ≠ missing", "Baja"],
            ["`cuidador` (`C3P120`)", "categórica 5", "madre / padre / abuelos / hermanos / otros", "22 ≈ CAR+", "Dummies; group lasso", "Alta"],
            ["`C3P120A` cuidador trabaja", "dummy", "sí / no / NS", "22", "Dummy", "Media"],
            ["`C3P120B` se queda sola", "dummy", "sí / no", "22", "Dummy", "Alta"],
            ["`C3P121` sin comer", "dummy", "sí / no", "22", "Dummy", "Alta (privación)"],
            ["`C3P122` no va al colegio para ayudar", "dummy", "sí / no", "22", "Dummy", "Alta"],
            ["`C3P123` peleas en casa", "dummy", "sí / no", "22", "Dummy (clima, no SES)", "Alta"],
            ["`C3P126` toman en cuenta su opinión", "dummy", "sí / no", "22", "Dummy", "Media"],
            ["`idioma` (`C3P128`)", "categórica 5", "castellano / quechua / aimara / otra / NS", "22", "Dummies; group lasso", "Alta"],
            ["`etnia` (`C4P129`)", "categórica 8", "mestiza / quechua / NS / afro / …", "0", "Group lasso o recode corto", "Media"],
            ["`discapacidad` (`C4P130_*`)", "dummy", "algún sí permanente", "0", "Dummy", "Media"],
            ["`quien_dinero` (`C3P302_4`)", "categórica 5", "quién da el dinero del hogar", "0", "Dummies", "Media (SES blando)"],
            ["`C4P248A_*` tipo agresor", "post-hoc", "solo si sexual=1", "skip", "No entra al modelo de riesgo", "Fuera"],
            ["`C1P101`–`C1P110` vivienda CRS01", "otra muestra", "agua, luz, activos", "0 en CRS01", "No se pega a CRS04", "Fuera del LASSO de alumnas"],
        ],
        {3},
    )

    def simple_dist(rows, labels=None) -> str:
        mapped = []
        for lab, n, nexp in rows:
            name = labels.get(lab, str(lab)) if labels else str(lab)
            mapped.append((name, n, nexp))
        return md_table(
            ["Nivel", "n", "% n", "N exp.", "% N"],
            dist_rows(mapped, n_m, n_exp),
            {1, 2, 3, 4},
        )

    urbano_n = next((nexp for lab, _n, nexp in area if lab == "Urbano"), 0)
    ined_txt = ", ".join(f"{lab_ined.get(int(a), a)} {fmt_pct(c, n_exp)}" for a, _b, c in ined)
    turno_txt = ", ".join(f"{lab_turno.get(int(a), a)} {fmt_pct(c, n_exp)}" for a, _b, c in turno)
    vive_txt = ", ".join(f"{lab_104.get(int(a), a)} {fmt_pct(c, n_exp)}" for a, _b, c in vive_dist)
    t_depto = md_table(["Departamento", "n", "% n", "N exp.", "% N"], dist_rows(depto[:8], n_m, n_exp), {1, 2, 3, 4})
    t_tipo = md_table(
        ["Tipo", "n", "% n", "N exp.", "% N"],
        dist_rows([(tipo_lab.get(int(a), str(a)), b, c) for a, b, c in tipo_viv], n_viv, n_viv_exp),
        {1, 2, 3, 4},
    )
    t_serv = md_table(
        ["Área", "n", "N exp.", "% electricidad", "% agua red dentro", "% desagüe red", "Índice activos (0–20)"],
        [
            [
                "Urbano" if a == 1 else "Rural",
                fmt_n(n),
                fmt_n(nexp),
                f"{100 * elec:.1f}%",
                f"{100 * agua:.1f}%",
                f"{100 * des:.1f}%",
                f"{idx:.1f}",
            ]
            for a, n, nexp, elec, agua, des, idx in serv
        ],
        {1, 2, 3, 4, 5, 6},
    )
    t_depto_viv = md_table(
        ["Departamento", "n", "N exp.", "% electricidad", "% agua red", "% desagüe red", "Índice"],
        [
            [d, fmt_n(n), fmt_n(nexp), f"{100 * e:.1f}%", f"{100 * a:.1f}%", f"{100 * ds:.1f}%", f"{idx:.1f}"]
            for d, n, nexp, e, a, ds, idx in depto_viv
        ],
        {1, 2, 3, 4, 5, 6},
    )
    t_activos = md_table(
        ["Activo", "n sí", "N sí", "% N"],
        [[lab, fmt_n(n), fmt_n(ne), f"{100 * p:.1f}%"] for lab, n, ne, p in asset_rows],
        {1, 2, 3},
    )
    disc_rows = [(lab_bool.get(a, str(a)), b, c) for a, b, c in disc]
    x_edad_md = cross_md(x_edad, lambda x: f"{int(x)} años")
    miss_hogar = (
        "18 CAR (skip del flujo de casa), no no-respuesta. "
        "Otras 4 filas missing en 115/120 son `vive sola` o residual."
    )
    t_comun = md_table(
        ["Dominio", "CRS04 (12–17) · en este doc", "CRS01 (18+)", "¿Idéntica?"],
        [
            ["Área urbano/rural", "`AREA` (de la IE)", "`AREA` (de la vivienda)", "Mismo código. Distinto objeto."],
            ["Departamento / UBIGEO", "`DEPARTAMENTO`, `CCDD`, `CCPP`, `CCDI`", "Mismos campos", "Mismo. IE vs hogar."],
            ["Edad", "`EDAD` / `C3P103EDAD`", "`C1P208_A`", "Sí. Años cumplidos."],
            ["Sexo", "`SEXO`", "`C1P207`", "Sí. En C1 la seleccionada es mujer."],
            ["¿Vive en este distrito?", "`C3P104` (+ `C4P104A_*` si no)", "Implícito: vive en la vivienda encuestada", "Parecido, no calcado."],
            ["¿Vivía aquí hace 5 años?", "`C4P104B` + `C4P104C_*`", "`C1P306_A` + `C1P306B_*`", "Sí. Casi calcado."],
            ["¿Dónde vivía su madre al nacer?", "`C4P104D` + `C4P104E_*`", "`C1P306C` + `C1P306D_*`", "Sí. Casi calcado."],
            ["Autoidentificación étnica", "`C4P129`", "`C1P306_E`", "Sí. Mismas 9 categorías."],
            ["Lengua", "`C3P128` idioma **del hogar**", "`C1P306_F` lengua **materna** de ella", "No. No comparar crudo."],
            ["Discapacidad (6 ítems)", "`C4P130_1`…`_6`", "`C1P209_A_1`…`_6` (padrón)", "Sí. Mismo listado."],
            ["Tamaño del hogar", "`C3P114_PERS`", "Conteo padrón `C1P204=1`", "Mismo concepto. Otra fuente."],
            ["Con quién vive", "`C3P115_*` / `composicion`", "`C1P203` parentesco al jefe", "Mismo concepto. Otra óptica."],
            ["Quién hace las tareas", "`C3P302_1`…`_10`", "`C1P316_1`…`_9`", "Parecido. Códigos distintos."],
            ["Quién mantiene económicamente", "`C3P302_4` / `quien_dinero`", "`C1P316_7`", "Mismo concepto."],
            ["Educación", "`C3ANIO` año actual", "`C1P210` último nivel", "No comparable 1 a 1."],
            ["Trabajo", "`C3P120A` el **cuidador**", "`C1P307` **ella**", "No. Distinto sujeto."],
            ["Resultado de encuesta", "`RFINAL`", "`RFINAL`", "Existe en ambos. Códigos distintos."],
            ["Agresión / victimización", "`C3P201`, `205`, `223`, `227`, `C4P248`", "`C1P402`, `C1P411`, `CAP441A`", "No. Ver tabla abajo."],
        ],
    )

    md = f"""# Descriptivos de controles: CRS04 + CRS01 (mujeres 18+)

{ficha(
    que_es="Cómo se ve la muestra: edad, área, cuidador, hogar, idioma, y cruces livianos con las 3 Y. También vivienda CRS01 (servicios y activos), que **no** se pega a la alumna.",
    que_no="No decide recodes (eso es descriptivos_predictores_crs04). No es el LASSO ni los perfiles. No es el diccionario de preguntas.",
    tipo="Descriptivo",
    script="scripts/descriptivos/descriptivos_controles.py",
)}
**Sí: CRS01 es el grupo de 18+.** Cuestionario CRS.01, mujeres de 18 y más en vivienda. CRS04 es adolescentes 12–17 en IE; aquí el recorte es mujeres (`SEXO = 1`).

Universo CRS04: mujeres (`SEXO = 1`) · n = {fmt_n(n_m)} · N = {fmt_n(n_exp)} con `FACTOR_ALUMNOS` · ENARES 2024.

Universo CRS01 (mujeres 18+): n = {fmt_n(n_viv)} · N = {fmt_n(n_viv_exp)} con `FACTOR_VIV` (hogar) / `FACTOR_MUJ` (mujer).

Targets 12m: [violencia_crs04_si_no_missing.md](violencia_crs04_si_no_missing.md). Recodes: [../metodologia/metodologia.md](../metodologia/metodologia.md).

---

## CRS01 y CRS04 no se unen

Son muestras distintas. `ID` no es llave común ({overlap} IDs coinciden: ruido de numeración). Electrodomésticos, agua, desagüe y material de la vivienda **no se pueden pegar a la adolescente**.

```mermaid
flowchart LR
  crs04["CRS04 alumna 12-17"] --> proxies["Proxies en CAP100/300"]
  crs01["CRS01 vivienda mujeres 18+"] --> wealth["Servicios y C1P110"]
  crs04 --> geo["AREA y departamento de la IE"]
  crs01 --> geoHogar["AREA y departamento del hogar"]
  geo -.->|"solo agregado territorial"| geoHogar
```

En CRS04, `AREA` y `DEPARTAMENTO` son de la **institución educativa**, no del hogar. Residencia: `C3P104` + `C4P104A_*`. `analisis.ubigeo` sirve para cruces agregados, no para SES individual.

---

## CRS04 — inventario de candidatos

{inv}

{miss_hogar}

---

## Distribuciones CRS04

### Territorio y escuela

`AREA` / `DEPARTAMENTO` = de la IE. {fmt_pct(urbano_n, n_exp)} de la N expandida está en IE urbana.

![Área de la IE]({IMG_MD}/controles_crs04_area.svg)

{simple_dist(area)}

`NIED` es constante (todas secundaria) y `TIEDBA` es constante (todas regular). No sirven como control.

| Variable | Qué es | Distribución ponderada |
|---|---|---|
| `INED` | Tipo de IE | {ined_txt} |
| `TURNO` | Turno de la alumna | {turno_txt} |
| `C3P104` | Vive en el distrito de la IE | {vive_txt} |

Hace 5 años, ¿vivía en este distrito? (`C4P104B`, misma pregunta que `C1P306_A`):

{simple_dist(mig5, lab_mig)}

Cuando nació, ¿vivía su madre en este distrito? (`C4P104D`, misma pregunta que `C1P306C`):

{simple_dist(madre_nacio, lab_mig)}

Año de estudio (`C3ANIO`):

{simple_dist(anio)}

Departamentos con más N expandida (la cola es larga: group lasso o no meter 25 dummies sueltas):

{t_depto}

### Edad

`EDAD` = `C3P103EDAD` en las {fmt_n(n_m)} alumnas (cero discordancias). Rango 12–17, sin missing. Candidata a término cuadrático si el cruce no es plano.

![Edad]({IMG_MD}/controles_crs04_edad.svg)

{simple_dist(edad)}

### Tamaño y composición del hogar

`C3P114_PERS`: mín {pers_stats[0]}, máx {pers_stats[1]}, media ponderada {pers_stats[2]:.2f}. Missing n = {pers_stats[3]} (CAR). Solo 4 casos “vivo sola” (`C3P114_VS = 1`).

![Tamaño del hogar]({IMG_MD}/controles_crs04_tamano.svg)

{simple_dist(tamano)}

![Composición]({IMG_MD}/controles_crs04_composicion.svg)

{simple_dist(comp)}

Casa vs CAR:

{simple_dist(casa, lab_105)}

Tiene mamá (`C3P106`):

{simple_dist(mama, lab_si)}

Tiene papá (`C3P110`):

{simple_dist(papa, lab_si)}

Cuarto / cama (proxies de hacinamiento; no hay habitaciones en CRS04):

{simple_dist(sola_cuarto, lab_118)}

{simple_dist(sola_cama, lab_119)}

`C3P119_12` NULL = skip si duerme sola en el cuarto (o CAR), no missing de calidad.

### Cuidado, privación y clima

![Cuidador]({IMG_MD}/controles_crs04_cuidador.svg)

{simple_dist(cuidador)}

Cuidador trabaja (`C3P120A`):

{simple_dist(cuida_trabaja, lab_120a)}

Se queda sola sin adulto (`C3P120B`):

{simple_dist(queda_sola, lab_si)}

Sin comer un día o más (`C3P121`):

{simple_dist(sin_comer, lab_si)}

Le piden no ir al colegio para ayudar (`C3P122`):

{simple_dist(no_colegio, lab_si)}

Peleas o discusiones en casa (`C3P123`):

{simple_dist(peleas, lab_si)}

Toman en cuenta lo que dice (`C3P126`):

{simple_dist(opinan, lab_si)}

Quién da el dinero (`C3P302_4` recode):

{simple_dist(dinero)}

### Idioma, etnia, discapacidad

![Idioma]({IMG_MD}/controles_crs04_idioma.svg)

{simple_dist(idioma)}

Autoidentificación (`C4P129` recode):

{simple_dist(etnia)}

Alguna limitación permanente (`C4P130_1`…`_6` = 1):

{simple_dist(disc_rows)}

---

## Cruce liviano con violencia 12m

Misma construcción que el QC: ámbitos con OR, NULL del filtro 12m = 0. Ponderado `FACTOR_ALUMNOS`. Sirve para ver **señal**, no para causalidad.

![Prevalencia por área]({IMG_MD}/controles_crs04_cruce_area.svg)

{cross_md(x_area)}

![Prevalencia por edad]({IMG_MD}/controles_crs04_cruce_edad.svg)

{x_edad_md}

Si sexual (u otro target) no es monótono en la edad, `edad^2` tiene sentido de probar. Si es casi lineal, no hace falta.

![Prevalencia por tamaño del hogar]({IMG_MD}/controles_crs04_cruce_tamano.svg)

{cross_md(x_tam)}

Cuidador:

{cross_md(x_cuid)}

Idioma:

{cross_md(x_idio)}

Sin comer (`C3P121`):

{cross_md(x_121, lambda x: lab_si.get(x, str(x)))}

Peleas en casa (`C3P123`):

{cross_md(x_123, lambda x: lab_si.get(x, str(x)))}

---

## CRS01 — servicios y activos (no se pegan a CRS04)

Missing en `C1P101`–`C1P110_*` = 0. Peso: `FACTOR_VIV`.

Promedio ponderado de habitaciones (`C1P108`) = {hab[0]:.2f}; dormitorios (`C1P109`) = {hab[1]:.2f}. Missing habitaciones = {hab[2]}; dormitorios = {hab[3]}.

Tipo de vivienda (`C1P101`):

{t_tipo}

### Servicios por área

Adecuado = electricidad (`C1P105=1`), agua red dentro (`C1P106=1`), desagüe red dentro o en la edificación (`C1P107 IN (1,2)`). Índice de activos = suma de `C1P110_1`…`_20` (sí=1), media ponderada.

![Servicios CRS01]({IMG_MD}/controles_crs01_servicios.svg)

{t_serv}

Departamentos con más N de hogares (muestra el gradiente territorial; no lo copies al LASSO de alumnas):

{t_depto_viv}

### Activos del hogar (`C1P110`)

![Activos CRS01]({IMG_MD}/controles_crs01_activos.svg)

{t_activos}

Estas variables **no existen en CRS04**. No las metas como dummies del LASSO de adolescentes.

### Cómo pegar contexto regional (sí se puede)

Los 25 departamentos están en CRS01 y CRS04. Calculas en CRS01, con `FACTOR_VIV`, promedios por `DEPARTAMENTO × AREA` (electricidad, agua red dentro, desagüe red, índice de activos 0–20) y se los pegas a la alumna por el departamento y área **de su IE**.

Eso es un rasgo del **lugar**, no de su casa. El 12.7% no vive en el distrito de la IE: distrito es frágil; departamento × área aguanta. No le asignes “tiene refrigeradora” a una fila.
"""

    asegurar_docs()
    DOC.write_text(md + inventory_appendix(), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"svgs in {IMG}")


if __name__ == "__main__":
    main()
