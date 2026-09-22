"""Dos informes: diseño muestral (CRS04+CRS01) y descriptivos de predictores CRS04.

Uso:
    python scripts/descriptivos/informe_muestral_predictores.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import DB, DOC_DESC, DOC_MET, IMG, IMG_MD, asegurar_docs, ficha

YES = "#c2410c"
INK = "#1c1917"
MUTED = "#78716c"
GRID = "#e7e5e4"
BG = "#fafaf9"
BAR = "#0369a1"
PSIC = "#b45309"
FIS = "#c2410c"
SEX = "#7c3aed"

ETNIA = {
    1: "Quechua",
    2: "Aimara",
    3: "Nativo/indígena Amazonía",
    4: "Otro pueblo indígena",
    5: "Afroperuana",
    6: "Blanca",
    7: "Mestiza",
    8: "Otro",
    9: "No sabe / no responde",
}
IDIOMA = {
    1: "Castellano",
    2: "Quechua",
    3: "Aimara",
    4: "Otra lengua nativa",
    5: "Idioma extranjero",
    6: "No sabe",
}
CUIDADOR = {
    1: "Madre",
    2: "Padre",
    3: "Madrastra",
    4: "Padrastro",
    5: "Hermana/s",
    6: "Hermano/s",
    7: "Abuela",
    8: "Abuelo",
    9: "Tía",
    10: "Tío",
    11: "Prima",
    12: "Primo",
    13: "Otro pariente",
    14: "Otra persona",
    15: "Hija/o del padrastro",
    16: "Hija/o de la madrastra",
    17: "Trabajadora del hogar",
}
CONVIVE = {
    1: "Madre",
    2: "Padre",
    3: "Madrastra",
    4: "Padrastro",
    5: "Hermana/s",
    6: "Hermano/s",
    7: "Abuela/s",
    8: "Abuelo/s",
    9: "Tía/s",
    10: "Tío/s",
    11: "Prima/s",
    12: "Primo/s",
    13: "Otros parientes",
    14: "Otra persona",
    15: "Hija/o del padrastro",
    16: "Hija/o de la madrastra",
    17: "Trabajadora del hogar",
}
CUARTO = {
    1: "Madre",
    2: "Padre",
    3: "Madrastra",
    4: "Padrastro",
    5: "Hermana/s",
    6: "Hermano/s",
    7: "Abuela",
    8: "Abuelo",
    9: "Tía",
    10: "Tío",
    11: "Otra persona",
    12: "Nadie (duerme sola)",
    13: "Hija/o del padrastro",
    14: "Hija/o de la madrastra",
    15: "Trabajadora del hogar",
}
DISC = {
    1: "Moverse / caminar",
    2: "Ver (aun con anteojos)",
    3: "Hablar / comunicarse",
    4: "Oír (aun con audífonos)",
    5: "Entender / aprender",
    6: "Relacionarse",
}
ACTITUD = {
    1: "Debe trabajar si falta plata",
    2: "Puede hablar lo que piensa",
    3: "Padres pueden decidir que deje el colegio",
    4: "Profesores tienen derecho a golpear",
    5: "Padres tienen derecho a golpear",
    6: "Puede denunciar a quien la maltrata",
}
SIENTE = {
    1: "Muy bien",
    2: "Bien",
    3: "Mal",
    4: "Muy mal",
    5: "No sabe",
}


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


def write_svg(name: str, body: str) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / name).write_text(body, encoding="utf-8")


def bar_h(name: str, rows: list[tuple[str, float]], caption: str, width: int = 920) -> None:
    left, right, top, row_h, gap = 220, 56, 28, 26, 8
    bar_w = width - left - right
    height = top + len(rows) * (row_h + gap) + 16
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
            f'<text x="{left - 8}" y="{y + 18}" text-anchor="end" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{esc(label)}</text>',
            f'<rect x="{left}" y="{y}" width="{max(w, 1):.1f}" height="{row_h}" fill="{BAR}" rx="3"/>',
            f'<text x="{left + w + 6:.1f}" y="{y + 18}" fill="{INK}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{value:.1f}%</text>',
        ]
        y += row_h + gap
    parts.append("</svg>")
    write_svg(name, "\n".join(parts))


def make_alumna(con: duckdb.DuckDBPyConnection) -> None:
    psic_h = " OR ".join(f"C3P201_{i}=1" for i in range(1, 12))
    fis_h = " OR ".join(f"C3P205_{i}=1" for i in range(1, 8))
    psic_c = " OR ".join(f"C3P223_{i}=1" for i in range(1, 15))
    fis_c = " OR ".join(f"C3P227_{i}=1" for i in range(1, 11))
    sex = " OR ".join(f"(C4P248_{i}=1 AND C4P248C_{i}=1)" for i in range(1, 17))
    disc = " OR ".join(f"C4P130_{i}=1" for i in range(1, 7))
    con.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE alumna AS
        SELECT
            *,
            FACTOR_ALUMNOS AS w,
            (({psic_h}) AND C3P203 = 1) OR (({psic_c}) AND C3P225 = 1) AS psic,
            (({fis_h}) AND C3P207 = 1) OR (({fis_c}) AND C3P229 = 1) AS fis,
            ({sex}) AS sexual,
            ({disc}) AS disc_alguna
        FROM analisis.crs04_adolescentes
        WHERE SEXO = 1
        """
    )


def dist(con, expr: str, labels: dict | None = None, order: str = "1") -> list[tuple]:
    rows = con.execute(
        f"""
        SELECT {expr} AS lab, COUNT(*) n, SUM(w) Nexp
        FROM alumna GROUP BY 1 ORDER BY {order}
        """
    ).fetchall()
    out = []
    for lab, n, nexp in rows:
        name = labels.get(lab, "missing" if lab is None else str(lab)) if labels else (
            "missing" if lab is None else str(lab)
        )
        out.append((name, n, nexp))
    return out


def dist_md(rows: list[tuple], n: int, nexp: float) -> str:
    body = []
    for name, ni, ni_exp in rows:
        body.append(
            [name, fmt_n(ni), fmt_pct(ni, n), fmt_n(ni_exp), fmt_pct(ni_exp, nexp)]
        )
    return md_table(["Nivel", "n", "% n", "N exp.", "% N"], body, {1, 2, 3, 4})


def yes_items(con, cols: list[str], labels: dict, nexp: float) -> str:
    bits = []
    for i, col in enumerate(cols, 1):
        lab = labels.get(i, col)
        n_yes, nexp_yes, n_null = con.execute(
            f"""
            SELECT
              SUM(CASE WHEN {col} = 1 THEN 1 ELSE 0 END),
              SUM(CASE WHEN {col} = 1 THEN w ELSE 0 END),
              SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END)
            FROM alumna
            """
        ).fetchone()
        bits.append(
            [
                f"`{col}`",
                lab,
                fmt_n(n_yes),
                fmt_pct(nexp_yes or 0, nexp),
                fmt_n(n_null),
            ]
        )
    return md_table(["Variable", "Ítem", "n sí", "% N sí", "n null"], bits, {2, 3, 4})


def cross(con, expr: str, labels: dict | None = None) -> str:
    rows = con.execute(
        f"""
        SELECT {expr} AS lab, COUNT(*) n, SUM(w) Nexp,
               100.0 * SUM(CASE WHEN psic THEN w ELSE 0 END) / SUM(w) AS p,
               100.0 * SUM(CASE WHEN fis THEN w ELSE 0 END) / SUM(w) AS f,
               100.0 * SUM(CASE WHEN sexual THEN w ELSE 0 END) / SUM(w) AS s
        FROM alumna GROUP BY 1 ORDER BY 1
        """
    ).fetchall()
    body = []
    for lab, ni, ni_exp, p, f, s in rows:
        name = labels.get(lab, "missing" if lab is None else str(lab)) if labels else (
            "missing" if lab is None else str(lab)
        )
        body.append(
            [name, fmt_n(ni), fmt_n(ni_exp), f"{p:.1f}%", f"{f:.1f}%", f"{s:.1f}%"]
        )
    return md_table(
        ["Grupo", "n", "N exp.", "% psic 12m", "% fís 12m", "% sexual 12m"],
        body,
        {1, 2, 3, 4, 5},
    )


def skip_block(con, col: str, n: int) -> tuple[int, float, float | None]:
    n_null, n_yes, n_asked = con.execute(
        f"""
        SELECT
          SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END),
          SUM(CASE WHEN {col} = 1 THEN 1 ELSE 0 END),
          SUM(CASE WHEN {col} IS NOT NULL THEN 1 ELSE 0 END)
        FROM alumna
        """
    ).fetchone()
    pct_skip = 100.0 * (n_null or 0) / n
    pct_yes_asked = 100.0 * (n_yes or 0) / n_asked if n_asked else None
    return n_null or 0, pct_skip, pct_yes_asked


def write_diseno(con, n4: int, nexp4: float) -> None:
    ies, secc, deptos, estratos, wmin, wmax = con.execute(
        """
        SELECT COUNT(DISTINCT ID),
               COUNT(DISTINCT ID || '-' || CAST(C3SECC AS VARCHAR)),
               COUNT(DISTINCT DEPARTAMENTO),
               COUNT(DISTINCT CCDD || '-' || CAST(AREA AS VARCHAR)),
               MIN(FACTOR_ALUMNOS), MAX(FACTOR_ALUMNOS)
        FROM analisis.crs04_adolescentes WHERE SEXO = 1
        """
    ).fetchone()
    ie_size = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k), AVG(k)
        FROM (SELECT ID, COUNT(*) k FROM analisis.crs04_adolescentes WHERE SEXO=1 GROUP BY ID)
        """
    ).fetchone()
    secc_ie = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k), AVG(k)
        FROM (
          SELECT ID, COUNT(DISTINCT C3SECC) k
          FROM analisis.crs04_adolescentes WHERE SEXO=1 GROUP BY ID
        )
        """
    ).fetchone()
    alum_secc = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k), AVG(k)
        FROM (
          SELECT ID, C3SECC, COUNT(*) k
          FROM analisis.crs04_adolescentes WHERE SEXO=1 GROUP BY 1,2
        )
        """
    ).fetchone()
    psu_str = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k),
               SUM(CASE WHEN k < 2 THEN 1 ELSE 0 END),
               SUM(CASE WHEN k = 2 THEN 1 ELSE 0 END),
               COUNT(*)
        FROM (
          SELECT DEPARTAMENTO, AREA, COUNT(DISTINCT ID) k
          FROM analisis.crs04_adolescentes WHERE SEXO=1 GROUP BY 1,2
        )
        """
    ).fetchone()
    thin4 = con.execute(
        """
        SELECT DEPARTAMENTO, AREA, COUNT(DISTINCT ID), COUNT(*)
        FROM analisis.crs04_adolescentes WHERE SEXO=1
        GROUP BY 1,2 HAVING COUNT(DISTINCT ID) <= 4
        ORDER BY 3, 1
        """
    ).fetchall()

    n1, hog, cong, est1, wmuj_min, wmuj_max, nexp_muj, wviv_min, wviv_max, nexp_viv = con.execute(
        """
        SELECT COUNT(*), COUNT(DISTINCT ID), COUNT(DISTINCT CONGLOME),
               COUNT(DISTINCT CCDD || '-' || CAST(AREA AS VARCHAR)),
               MIN(FACTOR_MUJ), MAX(FACTOR_MUJ), SUM(FACTOR_MUJ),
               MIN(FACTOR_VIV), MAX(FACTOR_VIV), SUM(FACTOR_VIV)
        FROM analisis.crs01_mujeres
        """
    ).fetchone()
    cong_size = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k), AVG(k)
        FROM (SELECT CONGLOME, COUNT(*) k FROM analisis.crs01_mujeres GROUP BY 1)
        """
    ).fetchone()
    psu1 = con.execute(
        """
        SELECT MIN(k), quantile_cont(k, 0.5), MAX(k),
               SUM(CASE WHEN k < 2 THEN 1 ELSE 0 END),
               SUM(CASE WHEN k = 2 THEN 1 ELSE 0 END),
               COUNT(*)
        FROM (
          SELECT DEPARTAMENTO, AREA, COUNT(DISTINCT CONGLOME) k
          FROM analisis.crs01_mujeres GROUP BY 1,2
        )
        """
    ).fetchone()
    thin1 = con.execute(
        """
        SELECT DEPARTAMENTO, AREA, COUNT(DISTINCT CONGLOME), COUNT(*)
        FROM analisis.crs01_mujeres
        GROUP BY 1,2 HAVING COUNT(DISTINCT CONGLOME) <= 4
        ORDER BY 3, 1
        """
    ).fetchall()
    has_cong4 = con.execute(
        """
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema='analisis' AND table_name='crs04_adolescentes'
          AND column_name='CONGLOME'
        """
    ).fetchone()[0]

    area_lab = {1: "Urbano", 2: "Rural"}
    thin4_md = md_table(
        ["Departamento", "Área", "IE (PSU)", "n alumnas"],
        [[d, area_lab[a], str(ie), fmt_n(ni)] for d, a, ie, ni in thin4],
        {2, 3},
    )
    thin1_md = md_table(
        ["Departamento", "Área", "CONGLOME (PSU)", "n mujeres"],
        [[d, area_lab[a], str(c), fmt_n(ni)] for d, a, c, ni in thin1],
        {2, 3},
    )

    md = f"""# Diseño muestral: CRS04 (12–17) y CRS01 (mujeres 18+)

{ficha(
    que_es="Números del diseño: qué es el PSU, el estrato, el peso, y qué tan flacos quedan los estratos. Sirve para `svydesign` y para no tratar a las alumnas como independientes.",
    que_no="No es la matriz X ni los recodes (eso es metodologia.md). No es el LASSO. No es un descriptivo de las preguntas.",
    tipo="Metodológico",
    script="scripts/descriptivos/informe_muestral_predictores.py",
)}
ENARES 2024. Este doc fija **estrato, conglomerado y peso** de las dos encuestas. Las dos muestras **no se unen** a nivel persona (`ID` no es llave común).

Universo de trabajo CRS04: `analisis.crs04_adolescentes`, `SEXO = 1` · n = {fmt_n(n4)} · N = {fmt_n(nexp4)} (`FACTOR_ALUMNOS`).

Universo CRS01: `analisis.crs01_mujeres` · n = {fmt_n(n1)} · N mujer = {fmt_n(nexp_muj)} (`FACTOR_MUJ`) · N hogar = {fmt_n(nexp_viv)} (`FACTOR_VIV`).

---

## Qué es cada cosa (las dos encuestas)

| Pieza | CRS04 alumnas 12–17 | CRS01 mujeres 18+ |
| --- | --- | --- |
| Marco | Institución educativa (secundaria regular) | Vivienda / hogar |
| Fila | Alumna | Mujer seleccionada (1 por hogar) |
| Llave de la fila | `ID` + `COLEGIAL_ID` | `ID` (= hogar) · `PERSONA_ID` de la seleccionada |
| **PSU / conglomerado** | **`ID` = la IE**. No existe `CONGLOME` ({has_cong4} columnas con ese nombre). | **`CONGLOME`** (sí viene explícito). Varios hogares por conglomerado. |
| SSU (opcional) | `C3SECC` (sección dentro de la IE) | No hace falta: 1 mujer por `ID` |
| **Estrato** | `AREA` × `DEPARTAMENTO` de la **IE** (49 celdas; Callao no tiene rural) | `AREA` × `DEPARTAMENTO` del **hogar** (también 49; Callao solo urbano) |
| Peso | `FACTOR_ALUMNOS` (mín {wmin:.2f}, máx {fmt_n(wmax)}) | `FACTOR_MUJ` (análisis de la mujer) · `FACTOR_VIV` (vivienda / activos) |
| `AREA` / `DEPARTAMENTO` | De la IE, no de la casa. El 12.7% no vive en el distrito de la IE. | Del hogar |

```mermaid
flowchart TB
  subgraph crs04 [CRS04 IE]
    A4["Estrato AREA x DEPARTAMENTO de la IE"] --> B4["PSU: ID colegio"]
    B4 --> C4["SSU opcional: C3SECC"]
    C4 --> D4["Alumna: COLEGIAL_ID"]
  end
  subgraph crs01 [CRS01 vivienda]
    A1["Estrato AREA x DEPARTAMENTO del hogar"] --> B1["PSU: CONGLOME"]
    B1 --> C1["Hogar ID / mujer seleccionada"]
  end
```

---

## CRS04 — el colegio es el conglomerado

No hay columna `CONGLOME`. La estructura de llaves alcanza: varias alumnas comparten el mismo `ID` y **no son independientes**.

| Estadístico | Valor |
| --- | ---: |
| IEs (`ID` distintos) | {fmt_n(ies)} |
| Alumnas por IE: mín / mediana / máx / media | {ie_size[0]} / {ie_size[1]:.0f} / {ie_size[2]} / {ie_size[3]:.1f} |
| Secciones distintas (`ID`+`C3SECC`) | {fmt_n(secc)} |
| Secciones por IE: mín / mediana / máx / media | {secc_ie[0]} / {secc_ie[1]:.0f} / {secc_ie[2]} / {secc_ie[3]:.2f} |
| Alumnas por sección: mín / mediana / máx / media | {alum_secc[0]} / {alum_secc[1]:.0f} / {alum_secc[2]} / {alum_secc[3]:.1f} |
| Estratos `AREA`×`DEPARTAMENTO` | {estratos} (de 25 × 2 = 50; falta Callao rural) |
| PSU por estrato: mín / mediana / máx | {psu_str[0]} / {psu_str[1]:.0f} / {psu_str[2]} |
| Estratos con 1 PSU | **{psu_str[3]}** |
| Estratos con exactamente 2 PSU | {psu_str[4]} |

`svydesign` exige ≥2 PSU por estrato. Aquí **cero singletons**. Los estratos flacos (≤4 IE):

{thin4_md}

Tacna rural es el más delicado: 2 colegios, 10 alumnas. `nest = TRUE` evita que `survey` cruce mal IEs homónimas entre estratos.

`C3SECC` es un segundo nivel real (mediana 2 secciones por IE; alumnas de la misma sección se parecen más). Un multinivel alumna → sección → colegio es defendible. **Para el LASSO con `survey::svydesign` alcanza `ids = ~ID`.** Si más adelante se quiere dos etapas: `ids = ~ID + seccion_uid` con `seccion_uid = paste(ID, C3SECC)`.

```r
library(survey)
diseno_crs04 <- svydesign(
  ids     = ~ID,
  strata  = ~interaction(AREA, DEPARTAMENTO),
  weights = ~FACTOR_ALUMNOS,
  data    = alumnas,   # SEXO == 1
  nest    = TRUE
)
```

---

## CRS01 — sí hay `CONGLOME`

Una mujer seleccionada por hogar: n = hogares = {fmt_n(n1)}. El PSU no es el hogar; es el conglomerado censal.

| Estadístico | Valor |
| --- | ---: |
| Conglomerados | {fmt_n(cong)} |
| Mujeres (= hogares) por `CONGLOME`: mín / mediana / máx / media | {cong_size[0]} / {cong_size[1]:.0f} / {cong_size[2]} / {cong_size[3]:.1f} |
| Estratos `AREA`×`DEPARTAMENTO` | {est1} |
| PSU por estrato: mín / mediana / máx | {psu1[0]} / {psu1[1]:.0f} / {psu1[2]} |
| Estratos con 1 PSU | **{psu1[3]}** |
| Estratos con exactamente 2 PSU | {psu1[4]} |

Estratos flacos (≤4 conglomerados):

{thin1_md}

Tumbes rural: 2 conglomerados, 24 mujeres. Mismo recaudo que Tacna rural en CRS04.

```r
diseno_crs01_mujer <- svydesign(
  ids     = ~CONGLOME,
  strata  = ~interaction(AREA, DEPARTAMENTO),
  weights = ~FACTOR_MUJ,
  data    = mujeres18,
  nest    = TRUE
)

# Solo si el análisis es de la vivienda (agua, C1P110):
diseno_crs01_viv <- svydesign(
  ids     = ~CONGLOME,
  strata  = ~interaction(AREA, DEPARTAMENTO),
  weights = ~FACTOR_VIV,
  data    = mujeres18,
  nest    = TRUE
)
```

`FACTOR_NIÑOS` no se usa en este recorte (80% null: no hay NNA en el hogar). `FACTOR_POBLACION` es del padrón, no de la seleccionada.

---

## Cómo las vamos a usar juntas

1. **Modelo de riesgo / LASSO / clusters de alumnas:** solo CRS04, `diseno_crs04`. PSU = `ID`. Estrato = `AREA`×`DEPARTAMENTO` de la IE.
2. **SES de vivienda (agua, desagüe, activos `C1P110`):** solo CRS01, `diseno_crs01_viv`. **No se pega a la fila de la alumna.** Si se quiere contexto territorial, se agregan medias por `DEPARTAMENTO`×`AREA` en CRS01 y se unen a la alumna por el depto/área **de su IE**. Eso es un rasgo del lugar, no de su casa.
3. **No** se usa `DEPARTAMENTO` como 25 dummies dentro del LASSO de alumnas (sobreajuste, sin interpretación). Sí se usa como estrato del diseño y como llave del dashboard.

---

## Lo que este diseño no arregla

- `RFINAL = 2` (encuesta incompleta) en CRS04: 12.4% de casos, 21.6% de la N. Los ítems de violencia están llenos; el peso de las incompletas es más alto.
- En CRS04, `AREA` urbana es de la IE. No es “vive en zona urbana”.
- 18 filas CAR (`C3P105 = 2`) se saltan el flujo de casa: missing de `C3P114`/`C3P115`/`C3P120` no es no-respuesta.

Especificación de la matriz X: [metodologia.md](metodologia.md). Números de las X candidatas: [../descriptivos/descriptivos_predictores_crs04.md](../descriptivos/descriptivos_predictores_crs04.md).
"""
    asegurar_docs()
    (DOC_MET / "diseno_muestral.md").write_text(md, encoding="utf-8")


def write_predictores(con, n: int, nexp: float) -> None:
    edad = dist(con, "EDAD")
    edad_stats = con.execute(
        "SELECT MIN(EDAD), MAX(EDAD), COUNT(DISTINCT EDAD), "
        "SUM(w*EDAD)/SUM(w), COUNT(*) FILTER (WHERE EDAD IS DISTINCT FROM C3P103EDAD) "
        "FROM alumna"
    ).fetchone()
    pers = con.execute(
        """
        SELECT MIN(C3P114_PERS), MAX(C3P114_PERS),
               SUM(w*C3P114_PERS)/SUM(CASE WHEN C3P114_PERS IS NOT NULL THEN w END),
               STDDEV_SAMP(C3P114_PERS),
               COUNT(*) FILTER (WHERE C3P114_PERS IS NULL),
               COUNT(*) FILTER (WHERE C3P114_VS = 1),
               COUNT(*) FILTER (WHERE C3P114_PERS = 0)
        FROM alumna
        """
    ).fetchone()
    pers_bin = dist(
        con,
        """
        CASE
          WHEN C3P114_PERS IS NULL THEN NULL
          WHEN C3P114_VS = 1 OR C3P114_PERS <= 1 THEN '1 / sola'
          WHEN C3P114_PERS BETWEEN 2 AND 3 THEN '2-3'
          WHEN C3P114_PERS BETWEEN 4 AND 5 THEN '4-5'
          WHEN C3P114_PERS BETWEEN 6 AND 8 THEN '6-8'
          ELSE '9+'
        END
        """,
        order="1",
    )
    etnia = dist(con, "C4P129", ETNIA, "2 DESC")
    idioma = dist(con, "C3P128", IDIOMA)
    mama = dist(con, "C3P106", {1: "Sí", 2: "No"})
    papa = dist(con, "C3P110", {1: "Sí", 2: "No"})
    cuid = dist(con, "C3P120", CUIDADOR, "2 DESC")
    sola = dist(con, "C3P120B", {1: "Sí", 2: "No"})
    comer = dist(con, "C3P121", {1: "Sí", 2: "No"})
    falta = dist(con, "C3P122", {1: "Sí", 2: "No"})
    peleas = dist(con, "C3P123", {1: "Sí", 2: "No"})
    frec_pelea = dist(con, "C3P124", {1: "Casi nunca", 2: "Algunas veces", 3: "Siempre/casi siempre", 4: "No sabe"})
    opinion = dist(con, "C3P126", {1: "Sí", 2: "No"})
    frec_op = dist(con, "C3P127", {1: "Casi nunca", 2: "Algunas veces", 3: "Siempre/casi siempre", 4: "No sabe"})
    area = dist(con, "AREA", {1: "Urbano", 2: "Rural"})
    ined = dist(con, "INED", {1: "Mujeres", 2: "Hombres", 3: "Mixto"})
    turno = dist(con, "TURNO", {1: "Mañana", 2: "Tarde", 3: "Noche"})
    siente = dist(con, "C3P217", SIENTE)
    jalo = dist(con, "C3P218", {1: "Sí", 2: "No"})
    repite = dist(con, "C3P219", {1: "Sí", 2: "No"})
    expulsa = dist(con, "C3P220", {1: "Sí", 2: "No"})
    amigos = dist(con, "C3P221", {1: "Sí", 2: "No"})
    miedo = dist(con, "C3P222", {1: "Sí", 2: "No"})
    disc_idx = dist(con, "disc_alguna", {True: "Alguna limitación", False: "Ninguna"})

    act_rows = []
    for i, lab in ACTITUD.items():
        a, d, ns, nexp_a = con.execute(
            f"""
            SELECT
              SUM(CASE WHEN C3P301_{i}=1 THEN 1 ELSE 0 END),
              SUM(CASE WHEN C3P301_{i}=2 THEN 1 ELSE 0 END),
              SUM(CASE WHEN C3P301_{i}=3 THEN 1 ELSE 0 END),
              SUM(CASE WHEN C3P301_{i}=1 THEN w ELSE 0 END)
            FROM alumna
            """
        ).fetchone()
        act_rows.append(
            [f"`C3P301_{i}`", lab, fmt_n(a), fmt_pct(nexp_a, nexp), fmt_n(d), fmt_n(ns)]
        )

    depto_n = con.execute("SELECT COUNT(DISTINCT DEPARTAMENTO) FROM alumna").fetchone()[0]

    # circular
    circ = []
    for col, nota in [
        ("C3P209", "Pidió ayuda (violencia en casa)"),
        ("C3P236", "Pidió ayuda (violencia en colegio)"),
        ("C3P216A_1", "Autolesión con objeto (lifetime)"),
        ("C3P216A_2", "Sustancia para hacerse daño"),
        ("C3P216A_3", "Durmió fuera sin permiso"),
        ("C3P216A_4", "Se fue de casa >1 día"),
        ("C3P216A_5", "Consumió licor"),
        ("C4P248C_1", "Sexual 12m (ítem 1; skip si C4P248_1 ≠ sí)"),
    ]:
        n_null, pct_skip, pct_yes = skip_block(con, col, n)
        circ.append(
            [
                f"`{col}`",
                nota,
                fmt_n(n_null),
                f"{pct_skip:.1f}%",
                "—" if pct_yes is None else f"{pct_yes:.1f}%",
            ]
        )

    n248a = con.execute(
        """
        SELECT SUM(CASE WHEN C4P248A_1_1 IS NOT NULL THEN 1 ELSE 0 END)
        FROM alumna
        """
    ).fetchone()[0]

    bar_h("pred_etnia.svg", [(a, 100.0 * ne / nexp) for a, _n, ne in etnia], "% N · C4P129")
    bar_h("pred_cuidador.svg", [(a, 100.0 * ne / nexp) for a, _n, ne in cuid[:10]], "% N · C3P120 (10 más frecuentes)")
    bar_h(
        "pred_actitudes.svg",
        [
            (ACTITUD[i], 100.0 * con.execute(
                f"SELECT SUM(CASE WHEN C3P301_{i}=1 THEN w ELSE 0 END) FROM alumna"
            ).fetchone()[0] / nexp)
            for i in range(1, 7)
        ],
        "% N de acuerdo (C3P301 = 1)",
    )
    bar_h("pred_siente.svg", [(a, 100.0 * ne / nexp) for a, _n, ne in siente], "% N · C3P217 cómo se siente en el colegio")

    t_act = md_table(
        ["Variable", "Oración", "n de acuerdo", "% N de acuerdo", "n no", "n NS"],
        act_rows,
        {2, 3, 4, 5},
    )
    t_circ = md_table(
        ["Variable", "Qué es", "n skip/null", "% n skip", "% sí entre preguntadas"],
        circ,
        {2, 3, 4},
    )
    mestiza_nexp = next((ne for a, _n, ne in etnia if a == "Mestiza"), 0)

    t_edad = dist_md(edad, n, nexp)
    t_edad_x = cross(con, "EDAD")
    t_etnia = dist_md(etnia, n, nexp)
    t_idioma = dist_md(idioma, n, nexp)
    t_disc = yes_items(con, [f"C4P130_{i}" for i in range(1, 7)], DISC, nexp)
    t_disc_idx = dist_md(disc_idx, n, nexp)
    t_opinion = dist_md(opinion, n, nexp)
    t_frec_op = dist_md(frec_op, n, nexp)
    t_mama = dist_md(mama, n, nexp)
    t_papa = dist_md(papa, n, nexp)
    t_pers_bin = dist_md(pers_bin, n, nexp)
    t_pers_x = cross(
        con,
        """
        CASE
          WHEN C3P114_PERS IS NULL THEN NULL
          WHEN C3P114_VS = 1 OR C3P114_PERS <= 1 THEN 1
          WHEN C3P114_PERS BETWEEN 2 AND 3 THEN 2
          WHEN C3P114_PERS BETWEEN 4 AND 5 THEN 3
          WHEN C3P114_PERS BETWEEN 6 AND 8 THEN 4
          ELSE 5
        END
        """,
        {1: "1 / sola", 2: "2-3", 3: "4-5", 4: "6-8", 5: "9+"},
    )
    t_convive = yes_items(con, [f"C3P115_{i}" for i in range(1, 18)], CONVIVE, nexp)
    t_cuarto = yes_items(con, [f"C3P118_{i}" for i in range(1, 16)], CUARTO, nexp)
    t_cuid = dist_md(cuid, n, nexp)
    t_sola = dist_md(sola, n, nexp)
    t_comer = dist_md(comer, n, nexp)
    t_falta = dist_md(falta, n, nexp)
    t_peleas = dist_md(peleas, n, nexp)
    t_frec_pelea = dist_md(frec_pelea, n, nexp)
    t_area = dist_md(area, n, nexp)
    t_ined = dist_md(ined, n, nexp)
    t_turno = dist_md(turno, n, nexp)
    t_siente = dist_md(siente, n, nexp)
    t_jalo = dist_md(jalo, n, nexp)
    t_repite = dist_md(repite, n, nexp)
    t_expulsa = dist_md(expulsa, n, nexp)
    t_amigos = dist_md(amigos, n, nexp)
    t_miedo = dist_md(miedo, n, nexp)

    md = f"""# Descriptivos de predictores candidatos — CRS04

{ficha(
    que_es="Cada X candidata: distribución, cruce con las 3 Y, y **tratamiento** (dummy, lineal, o fuera). Es el cuaderno de trabajo para armar la matriz.",
    que_no="No es el resultado del LASSO. No es cómo se ve la muestra en general (eso es descriptivos_controles). La lista cerrada de recodes está en metodologia.md.",
    tipo="Descriptivo",
    script="scripts/descriptivos/informe_muestral_predictores.py",
)}
Universo: mujeres (`SEXO = 1`) · n = {fmt_n(n)} · N = {fmt_n(nexp)} · `FACTOR_ALUMNOS` · ENARES 2024.

Lista cerrada de recodes: [../metodologia/metodologia.md](../metodologia/metodologia.md). Diseño: [../metodologia/diseno_muestral.md](../metodologia/diseno_muestral.md). Targets 12m: [violencia_crs04_si_no_missing.md](violencia_crs04_si_no_missing.md).

Códigos de sí/no: **1 = sí, 2 = no**. En multi-respuesta (`C3P115`, `C3P118`, `C4P130`) **1 = marcado, 0/NULL = no**. `C3P301`: **1 = de acuerdo, 2 = no, 3 = no sabe**.

---

## Individual

### `EDAD` / `C3P103EDAD`

Continua, {edad_stats[2]} valores ({edad_stats[0]}–{edad_stats[1]}). Media ponderada {edad_stats[3]:.2f}. Discordancias `EDAD` vs `C3P103EDAD`: {edad_stats[4]}. Missing = 0.

{t_edad}

Cruce con violencia 12m (ya en controles; se repite porque aquí se decide el cuadrático):

{t_edad_x}

**Tratamiento:** 6 puntos. Física baja casi lineal (34.5% → 16.9% de 12 a 16). Sexual es plana (~21–24%). `EDAD²` no aporta forma de U. **Primero dummies por año o `EDAD` lineal. Cuadrático solo si el jurado pide no-linealidad.** No hace falta estandarizar para el LASSO si penalizas; sí si comparas coeficientes.

### `C4P129` autoidentificación étnica (9 cat.)

Missing = 0.

![Etnia]({IMG_MD}/pred_etnia.svg)

{t_etnia}

**Tratamiento:** dummies, referencia **Mestiza** (mayoría, {fmt_pct(mestiza_nexp, nexp)}). Cola chica (Aimara, Amazonía, otro pueblo, otro): recode a “otra indígena / otro” o **group lasso**. No 8 dummies sueltas en LASSO normal.

### `C3P128` idioma del hogar (6 cat.)

22 missing ≈ CAR. **No es lengua materna** (en CRS01 `C1P306_F` sí lo es).

{t_idioma}

**Tratamiento:** dummies, referencia **Castellano**. Colapsar extranjero + otra nativa + NS si n ponderado < 2%.

### `C4P130_1`–`_6` discapacidad permanente

{t_disc}

Índice “alguna” (`OR` de las seis):

{t_disc_idx}

**Tratamiento:** las seis sueltas gastan gl y varias están < 3%. **Mejor un dummy `alguna_discapacidad` (12.4% N).** Si el jurado quiere tipo de limitación, deja ver/entender y tira el resto a “otra”.

### `C3P126` / `C3P127` toman en cuenta su opinión

{t_opinion}

Frecuencia (`C3P127`) solo si 126 = sí. Null = skip, no missing:

{t_frec_op}

**Tratamiento:** dummy de `C3P126`. `C3P127` como ordinal 1–3 (tirar NS) **o** no meterla: está definida solo en el sí y se pisa con 126.

### `C3P301_1`–`_6` actitudes (de acuerdo / no / NS)

![De acuerdo]({IMG_MD}/pred_actitudes.svg)

{t_act}

Ítems 2 y 6 son “pro derechos”; 1, 3, 4 y 5 son punitivos / restrictivos. **No sumes crudo.** Si quieres un índice: invierte 2 y 6 (o invierte 1/3/4/5) y suma. 4 y 5 tienen muy poco “de acuerdo” (~4% y ~9%): poca varianza para LASSO.

**Tratamiento:** 4 dummies de los ítems con varianza (1, 2, 3, 6) **o** un índice de 0–6 ya invertido. No seis dummies + NS.

---

## Relacional

### `C3P106` / `C3P110` tiene mamá / papá

{t_mama}

{t_papa}

**Tratamiento:** 0/1 (sí=1). Missing = CAR. No hace falta dummy de referencia.

### `C3P114_PERS` tamaño del hogar

Incluyéndola. n null = {pers[4]} (CAR). `C3P114_VS = 1` (vive sola): {pers[5]}. Valores 0 (raro; la pregunta pide incluirla): {pers[6]}. Rango {pers[0]}–{pers[1]}. Media ponderada {pers[2]:.2f}. DE muestral {pers[3]:.2f}.

{t_pers_bin}

{t_pers_x}

El cruce es **plano** en los tres targets. Hay variación real (0–20, DE ~2), pero no hay U ni J.

**Tratamiento:** lineal + estandarizar si comparas betas. **`PERS²` se puede probar, pero el cruce no lo pide.** No es el caso de `EDAD` (ahí la física sí es monótona).

### `C3P115_1`–`_17` con quién vive (multi-respuesta)

No son mutuamente excluyentes. 0/1 propias. Null ≈ CAR.

{t_convive}

**Tratamiento:** cada ítem ya es dummy. **No pongas referencia.** Tira o agrupa los < 2% N (hija/o de padrastro/madrastra, trabajadora del hogar). Madre+padre juntos se pisan con `C3P106`/`110`: o usas 115 o usas 106/110, no los dos bloques enteros.

### `C3P118` / `C3P119` comparte cuarto / cama

`C3P119` **no es missing al 50.8%**. Es skip: si `C3P118_12 = 1` (duerme sola en el cuarto) no preguntan la cama. En los datos: 4,860 alumnas con `C3P118_12=1` tienen `C3P119_*` NULL al 100%. No es evidencia de hacinamiento heterogéneo.

{t_cuarto}

**Tratamiento:** un dummy `duerme_sola_cuarto` = `C3P118_12`. Opcional: número de personas con quien comparte cuarto (suma de 118 excepto 12). **No metas las 15 + las 15 de cama.** `C3P119` solo como derivado “comparte cama” entre quienes no duermen solas en el cuarto.

### `C3P120` quién te cuida (17 cat., mutuamente excluyente)

22 missing ≈ CAR. Referencia natural = Madre.

![Cuidador]({IMG_MD}/pred_cuidador.svg)

{t_cuid}

**Tratamiento:** **no 16 dummies.** Recode a madre / padre / abuelos / hermanos / otros (como en controles) **o** group lasso sobre el bloque. Cola (tía, tío, prima, trabajador/a, hijastra) se va a “otros”.

### `C3P120B` se queda sola · `C3P121` sin comer · `C3P122` falta al colegio

`C3P120B` se queda sola sin adulto:

{t_sola}

`C3P121` la dejaron sin comer un día o más:

{t_comer}

`C3P122` le pidieron no ir al colegio para ayudar en casa:

{t_falta}

**Tratamiento:** 0/1 directo. Las tres tienen señal en el cruce de controles (`C3P121` y `C3P123` son de las más fuertes). Meterlas.

### `C3P123` / `C3P124` peleas en casa

{t_peleas}

`C3P124` solo si 123 = sí:

{t_frec_pelea}

**Tratamiento:** dummy de `C3P123` (alta). Frecuencia ordinal 1–3 si quieres intensidad; no las dos a la vez sin pensar el skip.

---

## Comunitario / escuela

`AREA`, `INED`, `TURNO`, `DEPARTAMENTO` son de la **IE**.

### `AREA`

{t_area}

**Tratamiento:** 0/1 (p. ej. rural=1). No dummy de referencia extra.

### `INED` tipo de IE

{t_ined}

**No hay IE solo de hombres** en este recorte (son alumnas). **Tratamiento:** un dummy mujeres vs mixto. No tres niveles.

### `TURNO`

{t_turno}

**Noche = 0 alumnas.** **Tratamiento:** un dummy tarde vs mañana. No tres.

### `C3P217` cómo se siente en el colegio

![Colegio]({IMG_MD}/pred_siente.svg)

{t_siente}

**Tratamiento:** ordinal 1–4 (tirar NS, n=11) **o** dummy mal/muy mal vs el resto. No asumas linealidad si dejas 4 dummies: “muy mal” es el 1.3% N.

### `C3P218` jaló curso · `C3P219` repitió · `C3P220` expulsión · `C3P221` amigos · `C3P222` lugares con miedo

`C3P218` jaló / desaprobó un curso (2023):

{t_jalo}

`C3P219` repitió de grado:

{t_repite}

`C3P220` la expulsaron:

{t_expulsa}

`C3P221` mejores amigos en este colegio:

{t_amigos}

`C3P222` hay lugares del colegio a los que no va por miedo:

{t_miedo}

**Tratamiento:** 0/1. `C3P220` expulsión es rarísima: poca varianza, candidata a caerse sola en el LASSO. `C3P222` (miedo a lugares del colegio) puede ser **circular** con bullying: es casi un síntoma de violencia escolar. Yo la dejaría fuera del LASSO de riesgo y la usaría después para caracterizar clusters.

### `DEPARTAMENTO` ({depto_n} niveles)

**No entra al LASSO** como 25 dummies. Es estrato del diseño y llave del dashboard. Si se insiste en “controlar territorio”, usa el proxy CRS01 (`DEPARTAMENTO`×`AREA`: electricidad, agua, activos), no 24 dummies de nombre.

---

## Fuera del LASSO: circularidad / leakage

Estas columnas **solo existen o solo se preguntan si ya hubo violencia** (o son consecuencias). Si entran como predictores, el modelo “adivina” el target con información posterior.

{t_circ}

Bloques enteros a **excluir** del X del LASSO:

| Bloque | Por qué |
| --- | --- |
| `C3P209`–`C3P215` | Ayuda / institución **después** de insultos o golpes en casa. Skip si no reportó. |
| `C3P216A_1`–`_6` (+ sufijo `C` 12m) | Autolesión, fuga, licor. Consecuencia o comorbilidad, no factor previo. |
| `C3P236`–`C3P247` | Ayuda y lesiones **después** de violencia escolar. |
| `C4P248A_*_*`, `C4P248B_*` | Quién agredió y edad de inicio. Llenos solo si `C4P248_i = 1`. `C4P248A` tiene n no-null ≈ {fmt_n(n248a)} en el primer ítem. Sirven **después** para describir el cluster, no para predecir `viol_sexual_12m`. |
| `C4P251`–`C4P260` | Ayuda por violencia sexual. Mismo patrón. |

Los 58 ítems madre (`C3P201_*`, `205_*`, `223_*`, `227_*`, `C4P248_*`) **son el target**, no controles.

---

## Qué sí meter, y cómo (resumen)

| Variable | ¿Entra? | Cómo | ¿Dummy / cuadrático? |
| --- | --- | --- | --- |
| `EDAD` | Sí | Lineal o 5 dummies (ref. 12) | Cuadrático: no primero |
| `C4P129` | Sí, recodificada | Dummies, ref. mestiza | Group lasso o cola colapsada |
| `C3P128` | Sí | Dummies, ref. castellano | Colapsar cola |
| `C4P130_*` | Sí | 1 dummy “alguna” | No 6 dummies |
| `C3P126` | Sí | 0/1 | `C3P127` opcional |
| `C3P301_*` | Probar | Índice invertido o 4 ítems | No 6 + NS |
| `C3P106` / `110` | Sí, o `C3P115` | 0/1 | No ambos bloques |
| `C3P114_PERS` | Sí | Lineal (CAR = missing) | `PERS²` opcional; el cruce es plano |
| `C3P115_*` | Sí, recorte | Multi 0/1, sin referencia | Tira < 2% N |
| `C3P118_12` | Sí | Duerme sola en el cuarto | No las 15+15 |
| `C3P120` | Sí, recode 5 | Dummies, ref. madre | Group lasso si dejas 17 |
| `C3P120B` `121` `122` `123` | Sí | 0/1 | Alta prioridad |
| `AREA` | Sí | Rural=1 | — |
| `INED` | Baja | Mujeres vs mixto | No 3 niveles |
| `TURNO` | Baja | Tarde vs mañana | No hay noche |
| `C3P217` | Probar | Ordinal 1–4 o dummy mal | — |
| `C3P218` `219` `221` | Probar | 0/1 | `220` casi no varía |
| `C3P222` | No (circular suave) | Post-cluster | — |
| `DEPARTAMENTO` | No en X | Estrato + dashboard | — |
| Bloques 209–215, 216A, 236–247, 248A/B | **No** | Leakage | — |

Próximo paso natural: script que arme la matriz `X` con estos recodes, lista para `glmnet` / group lasso, **sin** las circulares.
"""
    (DOC_DESC / "descriptivos_predictores_crs04.md").write_text(md, encoding="utf-8")


def main() -> None:
    con = duckdb.connect(str(DB), read_only=True)
    make_alumna(con)
    n, nexp = con.execute("SELECT COUNT(*), SUM(w) FROM alumna").fetchone()
    write_diseno(con, n, nexp)
    write_predictores(con, n, nexp)
    print("wrote", DOC_MET / "diseno_muestral.md")
    print("wrote", DOC_DESC / "descriptivos_predictores_crs04.md")


if __name__ == "__main__":
    main()
