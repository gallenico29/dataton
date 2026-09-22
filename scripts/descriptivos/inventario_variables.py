"""Inventario CRS04 y CRS01 (mujeres 18+): una fila por pregunta, con descripción.

Agrupa baterías (C3P115_1–17, C1P110_1–20, C1P411A_*_*) en un solo renglón.
Las etiquetas salen de los diccionarios PDF de datos_dev/.

Uso:
    python scripts/descriptivos/inventario_variables.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import duckdb
import fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import CRUDOS, DB, DOC_DESC, INV_CRS01_CSV, INV_CRS04_CSV, asegurar_docs, ficha

DATOS = CRUDOS

DICTS = {
    "crs04": [
        DATOS / "976-Modulo1959/976-Modulo1959/Diccionario de variables 19_CRS.04_CAP100.pdf",
        DATOS / "976-Modulo1960/976-Modulo1960/Diccionario de variables 20_CRS.04_CAP200.pdf",
        DATOS / "976-Modulo1961/976-Modulo1961/Diccionario de variables 21_CRS.04_CAP248.pdf",
        DATOS / "976-Modulo1962/976-Modulo1962/Diccionario de variables 22_CRS.04_CAP300.pdf",
    ],
    "crs01": [
        DATOS / "976-Modulo1941/976-Modulo1941/Diccionario de variables 01_CRS.01_CAP100.pdf",
        DATOS / "976-Modulo1942/976-Modulo1942/Diccionario de variables 02_CRS.01_CAP200.pdf",
        DATOS / "976-Modulo1943/976-Modulo1943/Diccionario de variables 03_CRS.01_CAP300.pdf",
        DATOS / "976-Modulo1944/976-Modulo1944/Diccionario de variables 04_CRS.01_CAP400.pdf",
        DATOS / "976-Modulo1945/976-Modulo1945/Diccionario de variables 05_CRS.01_CAP402.pdf",
        DATOS / "976-Modulo1946/976-Modulo1946/Diccionario de variables 06_CRS.01_CAP405.pdf",
        DATOS / "976-Modulo1947/976-Modulo1947/Diccionario de variables 07_CRS.01_CAP411.pdf",
        DATOS / "976-Modulo1948/976-Modulo1948/Diccionario de variables 08_CRS.01_CAP500.pdf",
        DATOS / "976-Modulo1949/976-Modulo1949/Diccionario de variables 09_CRS.01_CAP600.pdf",
        DATOS / "976-Modulo1950/976-Modulo1950/Diccionario de variables 10_CRS.01_CAP700.pdf",
    ],
}

HEADERS = {
    "Nro",
    "Nombre del Campo",
    "Descripción",
    "Descripcion",
    "Valor",
    "Tipo",
    "Longitud",
}
PART_SUFFIX = {"MES", "ANIO", "PERS", "VS"}
ID_SKIP_SAT = {
    "ID",
    "CONGLOME",
    "NSELV",
    "ID_MUESTRA",
    "CCDD",
    "DEPARTAMENTO",
    "CCPP",
    "PROVINCIA",
    "CCDI",
    "DISTRITO",
    "CODCCPP",
    "NOMCCPP",
    "AREA",
    "RESVIV",
    "RFINAL",
    "TOHOGAR",
    "HOGARN",
    "HOGAR_ID",
    "PERSONA_ID",
    "FACTOR_MUJ",
}


def ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


FACTOR_LABEL = {
    "FACTOR_ALUMNOS": "Factor de expansión de alumnas/os",
    "FACTOR_MUJ": "Factor de expansión de la mujer seleccionada",
    "FACTOR_VIV": "Factor de expansión de la vivienda",
    "FACTOR_POBLACION": "Factor de expansión poblacional (padrón)",
    "FACTOR_NIÑOS": "Factor de expansión de niñas/os",
}


def chapter_crs04(col: str) -> str:
    u = col.upper()
    if u.startswith("C4P248") or u.startswith("C4P25") or u.startswith("C4P26"):
        return "CAP248 violencia sexual"
    if u.startswith("C3P30"):
        return "CAP300 actitudes y tareas"
    if u.startswith("C3P2") or u.startswith("C4P21") or u.startswith("C4P24"):
        return "CAP200 psic/fís casa y colegio"
    if (
        u.startswith("C3P1")
        or u.startswith("C4P104")
        or u.startswith("C4P129")
        or u.startswith("C4P130")
    ):
        return "CAP100 alumna, hogar, identidad"
    return "ID / IE / peso"


def chapter_crs01(col: str, table: str) -> str:
    if "cap402" in table:
        return "CAP402 control/psic pareja (satélite)"
    if "cap405" in table:
        return "CAP405 consecuencias golpes (satélite)"
    if "cap411" in table:
        return "CAP411 agresión desde los 18 (satélite)"
    u = col.upper()
    if u.startswith("C1P1") or u == "FACTOR_VIV":
        return "CAP100 vivienda"
    if u.startswith("C1P2"):
        return "CAP200 padrón (seleccionada)"
    if u.startswith("C1P3"):
        return "CAP300 sociodemográfico"
    if u.startswith("C1P4") or u.startswith("CAP44"):
        return "CAP400 pareja, infancia, disciplina"
    if u.startswith("C1P5"):
        return "CAP500"
    if u.startswith("C1P6"):
        return "CAP600"
    if u.startswith("C1P7"):
        return "CAP700"
    return "ID / geo / peso"


def tidy(text: str) -> str:
    text = text.replace("|", "/").replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return text.strip(" :;")


def is_noise(line: str) -> bool:
    if not line or line in HEADERS:
        return True
    if line.startswith("DICCIONARIO DE VARIABLES"):
        return True
    if re.fullmatch(r"\d+_CRS\.?\d+_CAP\d+", line):
        return True
    if re.fullmatch(r"\d+_CRS\d+_CAP\d+", line):
        return True
    return False


def parse_pdf(path: Path, colnames: set[str]) -> dict[str, dict]:
    doc = fitz.open(path)
    lines = []
    for page in doc:
        for raw in page.get_text("text").splitlines():
            line = raw.strip()
            if is_noise(line):
                continue
            lines.append(line)
    doc.close()

    out: dict[str, dict] = {}
    i, n = 0, len(lines)
    while i < n:
        if (
            re.fullmatch(r"\d+", lines[i])
            and i + 1 < n
            and lines[i + 1] in colnames
        ):
            name = lines[i + 1]
            i += 2
            desc_parts: list[str] = []
            vals: list[str] = []
            tipo = ""
            while i < n and not (
                re.fullmatch(r"\d+", lines[i])
                and i + 1 < n
                and lines[i + 1] in colnames
            ):
                line = lines[i]
                if line in {"N", "A", "AN"} and i + 1 < n and re.fullmatch(r"\d+", lines[i + 1]):
                    tipo = line
                    i += 2
                    continue
                if re.fullmatch(r"\d{1,3}", line) and not desc_parts:
                    i += 1
                    continue
                if tipo and re.match(r"^\d+\.", line):
                    vals.append(tidy(line))
                elif tipo and vals:
                    vals[-1] = tidy(vals[-1] + " " + line)
                else:
                    desc_parts.append(line)
                i += 1
            out[name] = {
                "descripcion": tidy(" ".join(desc_parts)),
                "valores": vals,
                "tipo_dicc": tipo,
            }
        else:
            i += 1
    return out


def load_labels(paths: list[Path], colnames: set[str]) -> dict[str, dict]:
    labels: dict[str, dict] = {}
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        labels.update(parse_pdf(path, colnames))
    return labels


def strip_trailing_indices(name: str) -> str:
    while True:
        m = re.fullmatch(r"(.+)_(\d+)", name)
        if not m:
            break
        name = m.group(1)
    return name


def group_key(name: str) -> str:
    if name in {"TURNO_M", "TURNO_T", "TURNO_N"}:
        return "TURNO_IE"
    if name.endswith("_COD"):
        return strip_trailing_indices(name[:-4]) + "_COD"
    if re.fullmatch(r".+_\d+_O", name) or name.endswith("_O"):
        base = re.sub(r"_O$", "", name)
        return strip_trailing_indices(base) + "_O"
    if re.fullmatch(r".+_\d+E", name):
        return re.sub(r"_\d+E$", "_E", name)
    head, _, tail = name.rpartition("_")
    if tail in PART_SUFFIX and head:
        return head
    if name.endswith("_P") and re.match(r".+P\d+", name):
        return strip_trailing_indices(name[:-2])
    if name.endswith(("_HER", "_NOH")):
        return name.rsplit("_", 1)[0]
    return strip_trailing_indices(name)


def format_names(names: list[str]) -> str:
    if len(names) == 1:
        return f"`{names[0]}`"
    two = [re.fullmatch(r"(.+)_(\d+)_(\d+)", n) for n in names]
    if all(two):
        stem = two[0].group(1)
        if all(m.group(1) == stem for m in two):
            return f"`{stem}_*_*` ({len(names)} cols)"
    one = [re.fullmatch(r"(.+)_(\d+)", n) for n in names]
    if all(one):
        stem = one[0].group(1)
        if all(m.group(1) == stem for m in one):
            nums = [int(m.group(2)) for m in one]
            lo, hi = min(nums), max(nums)
            if nums == list(range(lo, hi + 1)):
                return f"`{stem}_{lo}`–`_{hi}`"
            return f"`{stem}_*` ({len(names)} cols, {lo}–{hi})"
    if names[0].startswith("TURNO_"):
        return "`TURNO_M` / `_T` / `_N`"
    tails = {n.rsplit("_", 1)[-1] for n in names}
    if tails <= PART_SUFFIX:
        stem = names[0].rsplit("_", 1)[0]
        bits = " / ".join(f"`_{t}`" for t in sorted(tails))
        return f"`{stem}` ({bits})"
    return f"`{names[0]}` … `{names[-1]}` ({len(names)} cols)"


def common_prefix(texts: list[str]) -> str:
    if not texts:
        return ""
    first = texts[0]
    end = len(first)
    for other in texts[1:]:
        i = 0
        limit = min(end, len(other))
        while i < limit and first[i] == other[i]:
            i += 1
        end = i
        if end == 0:
            break
    prefix = first[:end]
    cut = max(prefix.rfind(":"), prefix.rfind("?"))
    dot = prefix.rfind(".")
    if dot >= 8 and not re.fullmatch(r"\d+\.", prefix[: dot + 1].strip()):
        cut = max(cut, dot)
    if cut >= 8:
        prefix = prefix[: cut + 1]
    return tidy(prefix)


def drop_footnote(text: str) -> str:
    return re.sub(r"(?<=\D)\s+\d{1,2}$", "", text).strip()


def compose_text(names: list[str], labels: dict[str, dict]) -> tuple[str, str]:
    if len(names) == 1 and names[0] in FACTOR_LABEL:
        return FACTOR_LABEL[names[0]], "peso"

    metas = [labels.get(n, {}) for n in names]
    descs = [drop_footnote(m.get("descripcion") or "") for m in metas]
    filled = [d for d in descs if d]
    if not filled:
        if names[0] in FACTOR_LABEL:
            return FACTOR_LABEL[names[0]], "peso"
        return "Sin etiqueta en el diccionario PDF.", ""

    prefix = common_prefix(filled)
    tails: list[str] = []
    seen: set[str] = set()
    for i, desc in enumerate(filled, 1):
        tail = desc[len(prefix) :].strip(" :;.") if prefix else ""
        tail = drop_footnote(tidy(tail))
        if not tail:
            continue
        if not re.match(r"^\d+\.", tail):
            tail = f"{i}. {tail}"
        key = tail.lower()
        if key not in seen:
            seen.add(key)
            tails.append(tail)

    question = prefix or filled[0]
    vals = metas[0].get("valores") or []
    # códigos completos (a veces el wrap del PDF parte el primer ítem)
    if len(vals) <= 3:
        for m in metas[1:]:
            if len(m.get("valores") or []) > len(vals):
                vals = m["valores"]
                break

    if len(tails) >= 2:
        return question, "; ".join(tails)

    if vals:
        shown = vals[:24]
        extra = "; …" if len(vals) > 24 else ""
        return question, "; ".join(shown) + extra
    return question, ""


def null_counts(con, table: str, cols: list[str], where: str) -> tuple[int, list[int]]:
    n = con.execute(f"SELECT COUNT(*) FROM {table} {where}").fetchone()[0]
    out: list[int] = []
    for i in range(0, len(cols), 60):
        batch = cols[i : i + 60]
        sel = ", ".join(
            f"SUM(CASE WHEN {ident(c)} IS NULL THEN 1 ELSE 0 END)" for c in batch
        )
        row = con.execute(f"SELECT {sel} FROM {table} {where}").fetchone()
        out.extend(int(x or 0) for x in row)
    return n, out


def inventory(
    con,
    table: str,
    where: str,
    chap_fn,
    labels: dict[str, dict],
    skip: set[str] | None = None,
) -> tuple[int, list[dict]]:
    meta = [(r[0], r[1]) for r in con.execute(f"DESCRIBE {table}").fetchall()]
    cols = [c for c, _t in meta if not skip or c not in skip]
    types = dict(meta)
    n, nulls = null_counts(con, table, cols, where)
    null_map = dict(zip(cols, nulls))

    buckets: dict[str, list[str]] = defaultdict(list)
    for col in cols:
        buckets[group_key(col)].append(col)

    rows = []
    for _key, names in buckets.items():
        desc, cats = compose_text(names, labels)
        pcts = [100.0 * null_map[c] / n if n else 0.0 for c in names]
        rows.append(
            {
                "tabla": table,
                "capitulo": chap_fn(names[0]),
                "variables": format_names(names),
                "n_cols": len(names),
                "descripcion": desc,
                "categorias": cats,
                "tipo": types[names[0]],
                "n": n,
                "pct_null_min": min(pcts),
                "pct_null_max": max(pcts),
            }
        )
    return n, rows


def md_cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(c) for c in row) + " |")
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = [
        "tabla",
        "capitulo",
        "variables",
        "n_cols",
        "descripcion",
        "categorias",
        "tipo",
        "n",
        "pct_null_min",
        "pct_null_max",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_md(
    path: Path,
    title: str,
    intro: str,
    n: int,
    n_raw: int,
    rows: list[dict],
    box: str,
) -> None:
    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(r["capitulo"], []).append(r)
    parts = [
        f"# {title}",
        "",
        box.rstrip(),
        "",
        intro,
        "",
        f"Filas en el recorte: **{n:,}**. "
        f"Columnas crudas: **{n_raw:,}**. "
        f"Preguntas (filas de este inventario, baterías agrupadas): **{len(rows):,}**.",
        "",
        md_table(
            ["Capítulo", "Preguntas", "Columnas"],
            [
                [k, str(len(v)), str(sum(x["n_cols"] for x in v))]
                for k, v in by.items()
            ],
        ),
    ]
    for cap, items in by.items():
        parts += ["", f"## {cap}", ""]
        parts.append(
            md_table(
                ["Variables", "Qué pregunta", "Ítems / códigos", "N cols", "% null"],
                [
                    [
                        r["variables"],
                        r["descripcion"],
                        r["categorias"] or "—",
                        str(r["n_cols"]),
                        (
                            f"{r['pct_null_min']:.1f}"
                            if abs(r["pct_null_min"] - r["pct_null_max"]) < 0.05
                            else f"{r['pct_null_min']:.1f}–{r['pct_null_max']:.1f}"
                        ),
                    ]
                    for r in items
                ],
            )
        )
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    con = duckdb.connect(str(DB), read_only=True)

    cols4 = [r[0] for r in con.execute("DESCRIBE analisis.crs04_adolescentes").fetchall()]
    cols1 = [r[0] for r in con.execute("DESCRIBE analisis.crs01_mujeres").fetchall()]
    sat_cols: list[str] = []
    for t in (
        "analisis.crs01_cap402",
        "analisis.crs01_cap405",
        "analisis.crs01_cap411",
    ):
        sat_cols.extend(r[0] for r in con.execute(f"DESCRIBE {t}").fetchall())

    print("Leyendo diccionarios PDF…")
    lab4 = load_labels(DICTS["crs04"], set(cols4))
    lab1 = load_labels(DICTS["crs01"], set(cols1) | set(sat_cols))
    print(f"  etiquetas CRS04 {len(lab4)} / {len(cols4)} cols")
    print(f"  etiquetas CRS01 {len(lab1)} / {len(set(cols1) | set(sat_cols))} cols")

    n4, r4 = inventory(
        con,
        "analisis.crs04_adolescentes",
        "WHERE SEXO = 1",
        chapter_crs04,
        lab4,
    )
    n1, r1 = inventory(
        con,
        "analisis.crs01_mujeres",
        "",
        lambda c: chapter_crs01(c, "analisis.crs01_mujeres"),
        lab1,
    )
    sat: list[dict] = []
    for table in (
        "analisis.crs01_cap402",
        "analisis.crs01_cap405",
        "analisis.crs01_cap411",
    ):
        _n, rows = inventory(
            con,
            table,
            "",
            lambda c, t=table: chapter_crs01(c, t),
            lab1,
            skip=ID_SKIP_SAT,
        )
        sat.extend(rows)

    asegurar_docs()
    write_csv(INV_CRS04_CSV, r4)
    write_csv(INV_CRS01_CSV, r1 + sat)

    write_md(
        DOC_DESC / "inventario_crs04.md",
        "Inventario CRS04 (adolescentes 12–17, mujeres)",
        "Tabla `analisis.crs04_adolescentes`, recorte `SEXO = 1`. "
        "Una fila = una pregunta. Si el cuestionario tiene ítems `_1` a `_14`, "
        "van juntos con la descripción del diccionario (no una columna por renglón). "
        "Etiquetas: diccionarios PDF CAP100/200/248/300. "
        "La misma lista en CSV (para filtrar en Excel) está en "
        "`data/tablas/inventario_crs04.csv`. No es otro informe.",
        n4,
        len(cols4),
        r4,
        ficha(
            que_es="Diccionario corto de las preguntas CRS04: nombre de columna, qué pregunta el PDF y códigos.",
            que_no="No hay prevalencias, cruces ni modelos. No es el catálogo de violencia (eso es violencia_por_cuestionario).",
            tipo="Descriptivo",
            script="scripts/descriptivos/inventario_variables.py",
        ),
    )
    n_raw_01 = len(cols1) + sum(r["n_cols"] for r in sat)
    write_md(
        DOC_DESC / "inventario_crs01.md",
        "Inventario CRS01 (mujeres 18+)",
        "Sí: CRS01 es el cuestionario de **mujeres de 18 y más** en vivienda. "
        "Tabla ancha `analisis.crs01_mujeres` más satélites CAP402, CAP405 y CAP411. "
        "Una fila = una pregunta; las baterías (p. ej. `C1P110_1`–`_20`, `C1P411_1`–`_N`) "
        "están colapsadas. Etiquetas: diccionarios PDF. "
        "La misma lista en CSV está en `data/tablas/inventario_crs01.csv`. No es otro informe.",
        n1,
        n_raw_01,
        r1 + sat,
        ficha(
            que_es="Diccionario corto de las preguntas CRS01 (mujeres 18+ en vivienda), satélites incluidos.",
            que_no="No se une a la alumna. No es el comparativo CRS01 vs CRS04 (eso es descriptivos_crs01_vs_crs04).",
            tipo="Descriptivo",
            script="scripts/descriptivos/inventario_variables.py",
        ),
    )
    print(f"CRS04 {len(cols4)} cols -> {len(r4)} preguntas")
    print(f"CRS01 {n_raw_01} cols -> {len(r1) + len(sat)} preguntas")


if __name__ == "__main__":
    main()
