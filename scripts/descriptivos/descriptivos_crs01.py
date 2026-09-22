"""Descriptivos CRS01 (mujeres 18+) y solape conceptual con CRS04."""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rutas import DB, DOC_DESC, asegurar_docs, ficha

DOC = DOC_DESC / "descriptivos_crs01_vs_crs04.md"


def fmt_n(x: float) -> str:
    return f"{int(round(x)):,}"


def fmt_pct(part: float, total: float) -> str:
    return f"{100.0 * part / total:.1f}%"


def md_table(headers: list[str], rows: list[list[str]], right: set[int] | None = None) -> str:
    right = right or set()
    align = ["---:" if i in right else "---" for i in range(len(headers))]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(align) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def dist(con, sql: str, total_n: float, total_N: float, labels: dict) -> str:
    rows = con.execute(sql).fetchall()
    out = []
    for lab, n, nexp in rows:
        name = labels.get(lab, str(lab) if lab is not None else "missing")
        out.append([name, fmt_n(n), fmt_pct(n, total_n), fmt_n(nexp), fmt_pct(nexp, total_N)])
    return md_table(["Nivel", "n", "% n", "N exp.", "% N"], out, {1, 2, 3, 4})


def main() -> None:
    con = duckdb.connect(str(DB), read_only=True)
    n, nexp = con.execute("SELECT COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres").fetchone()

    t_area = dist(
        con,
        "SELECT AREA, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {1: "Urbano", 2: "Rural"},
    )
    t_edad = dist(
        con,
        """
        SELECT tramo, COUNT(*), SUM(FACTOR_MUJ) FROM (
            SELECT FACTOR_MUJ,
                CASE
                    WHEN C1P208_A < 25 THEN '18-24'
                    WHEN C1P208_A < 35 THEN '25-34'
                    WHEN C1P208_A < 45 THEN '35-44'
                    WHEN C1P208_A < 60 THEN '45-59'
                    ELSE '60+'
                END AS tramo,
                CASE
                    WHEN C1P208_A < 25 THEN 1
                    WHEN C1P208_A < 35 THEN 2
                    WHEN C1P208_A < 45 THEN 3
                    WHEN C1P208_A < 60 THEN 4
                    ELSE 5
                END AS ord
            FROM analisis.crs01_mujeres
        ) GROUP BY tramo, ord ORDER BY ord
        """,
        n,
        nexp,
        {},
    )
    t_civil = dist(
        con,
        "SELECT C1P302, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {
            1: "Conviviente",
            2: "Casada",
            3: "Viuda",
            4: "Divorciada",
            5: "Separada / exconviviente",
            6: "Soltera",
        },
    )
    t_educ = dist(
        con,
        "SELECT C1P210, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {
            1: "Sin nivel",
            2: "Inicial",
            3: "Primaria incompleta",
            4: "Primaria completa",
            5: "Secundaria incompleta",
            6: "Secundaria completa",
            7: "Básica especial",
            8: "Sup. no univ. incompleta",
            9: "Sup. no univ. completa",
            10: "Univ. incompleta",
            11: "Univ. completa",
            12: "Maestría/doctorado",
        },
    )
    t_etnia = dist(
        con,
        "SELECT C1P306_E, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY SUM(FACTOR_MUJ) DESC",
        n,
        nexp,
        {
            1: "Quechua",
            2: "Aimara",
            3: "Nativo Amazonía",
            4: "Otro pueblo indígena",
            5: "Afroperuana",
            6: "Blanca",
            7: "Mestiza",
            8: "Otro",
            9: "No sabe",
        },
    )
    t_lengua = dist(
        con,
        """
        SELECT CASE
            WHEN C1P306_F = 10 THEN 'Castellano'
            WHEN C1P306_F = 1 THEN 'Quechua'
            WHEN C1P306_F = 2 THEN 'Aimara'
            WHEN C1P306_F BETWEEN 3 AND 9 THEN 'Otra nativa'
            WHEN C1P306_F IN (11, 12) THEN 'Extranjera'
            ELSE 'Otra / no habla'
        END, COUNT(*), SUM(FACTOR_MUJ)
        FROM analisis.crs01_mujeres GROUP BY 1
        ORDER BY SUM(FACTOR_MUJ) DESC
        """,
        n,
        nexp,
        {},
    )
    t_trab = dist(
        con,
        "SELECT C1P307, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {1: "Sí trabajó (semana pasada)", 2: "No"},
    )
    t_hijos = dist(
        con,
        "SELECT C1P304, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {1: "Alguna vez tuvo hija/o", 2: "No"},
    )
    t_mig = dist(
        con,
        "SELECT C1P306_A, COUNT(*), SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres GROUP BY 1 ORDER BY 1",
        n,
        nexp,
        {1: "Hace 5 años vivía en este distrito", 2: "No"},
    )
    t_depto = dist(
        con,
        """
        SELECT DEPARTAMENTO, COUNT(*), SUM(FACTOR_MUJ)
        FROM analisis.crs01_mujeres GROUP BY 1
        ORDER BY SUM(FACTOR_MUJ) DESC LIMIT 8
        """,
        n,
        nexp,
        {},
    )
    t_dinero = dist(
        con,
        """
        SELECT CASE
            WHEN C1P316_7 IS NULL THEN 'missing'
            WHEN C1P316_7 = 1 THEN 'Ella'
            WHEN C1P316_7 = 2 THEN 'Esposo/pareja'
            WHEN C1P316_7 = 9 THEN 'Ella y pareja'
            WHEN C1P316_7 = 10 THEN 'Todos en el hogar'
            ELSE 'Otra persona'
        END, COUNT(*), SUM(FACTOR_MUJ)
        FROM analisis.crs01_mujeres GROUP BY 1
        ORDER BY SUM(FACTOR_MUJ) DESC
        """,
        n,
        nexp,
        {},
    )

    disc = con.execute(
        """
        SELECT
            SUM(CASE WHEN C1P209_A_1=1 OR C1P209_A_2=1 OR C1P209_A_3=1
                OR C1P209_A_4=1 OR C1P209_A_5=1 OR C1P209_A_6=1 THEN 1 ELSE 0 END),
            SUM(CASE WHEN C1P209_A_1=1 OR C1P209_A_2=1 OR C1P209_A_3=1
                OR C1P209_A_4=1 OR C1P209_A_5=1 OR C1P209_A_6=1 THEN FACTOR_MUJ ELSE 0 END)
        FROM analisis.crs01_mujeres
        """
    ).fetchone()
    hog = con.execute(
        """
        SELECT AVG(n) FROM (
            SELECT m.ID, COUNT(*) AS n
            FROM analisis.crs01_mujeres m
            JOIN analisis.crs01_padron p ON m.ID = p.ID AND p.C1P204 = 1
            GROUP BY 1
        )
        """
    ).fetchone()[0]
    edad = con.execute(
        "SELECT MIN(C1P208_A), MAX(C1P208_A), SUM(FACTOR_MUJ * C1P208_A)/SUM(FACTOR_MUJ) FROM analisis.crs01_mujeres"
    ).fetchone()

    overlap = md_table(
        ["Dominio", "CRS04 12–17 (IE)", "CRS01 18+ (vivienda)", "¿Misma pregunta?"],
        [
            ["Área", "`AREA` de la IE", "`AREA` de la vivienda", "Mismo código 1/2. Distinto objeto."],
            ["Departamento", "`DEPARTAMENTO` de la IE", "`DEPARTAMENTO` del hogar", "Mismo. Distinto objeto."],
            ["Edad", "`EDAD` / `C3P103EDAD`", "`C1P208_A` (padrón)", "Sí: años cumplidos."],
            ["Sexo", "`SEXO`", "`C1P207`", "Sí (en C1 la seleccionada es mujer)."],
            ["Autoidentificación étnica", "`C4P129`", "`C1P306_E`", "Sí. Mismas 9 categorías."],
            ["Lengua", "`C3P128` idioma que hablan en su casa", "`C1P306_F` lengua materna de ella", "No. Hogar vs materna."],
            ["¿Vivía en este distrito hace 5 años?", "`C4P104B` + `C4P104C_*`", "`C1P306_A` + `C1P306B_*`", "Sí, casi calcado."],
            ["¿Dónde vivía su madre cuando nació?", "`C4P104D` + `C4P104E_*`", "`C1P306C` + `C1P306D_*`", "Sí, casi calcado."],
            ["Discapacidad (6 ítems)", "`C4P130_1`…`_6`", "`C1P209_A_1`…`_6` (padrón)", "Sí. Mismo listado."],
            ["Tamaño del hogar", "`C3P114_PERS` (ella cuenta)", "Conteo del padrón `C1P204=1`", "Mismo concepto, distinta fuente."],
            ["Con quién vive", "`C3P115_*` (óptica de la niña)", "`C1P203` parentesco al jefe", "Mismo concepto, distinta óptica."],
            ["Quién hace las tareas", "`C3P302_*`", "`C1P316_*`", "Parecido. Códigos distintos."],
            ["Quién mantiene económicamente", "`C3P302_4`", "`C1P316_7`", "Mismo concepto."],
            ["Educación", "`C3ANIO` año actual (todas en secundaria)", "`C1P210` último nivel aprobado", "No comparable 1 a 1."],
            ["Trabajo", "`C3P120A` si el cuidador trabaja", "`C1P307` si ella trabajó", "No. Distinto sujeto."],
        ],
    )

    only04 = md_table(
        ["Solo CRS04 (12–17)", "Variable"],
        [
            ["Quién la cuida / se queda sola", "`C3P120`, `C3P120B`"],
            ["Sin comer, faltar al colegio para ayudar, peleas en casa", "`C3P121`, `C3P122`, `C3P123`"],
            ["Comparte cuarto / cama", "`C3P118_*`, `C3P119_*`"],
            ["Violencia psic/fís en casa y colegio + sexual CAP248", "`C3P201+`, `C4P248`"],
            ["Contexto de la IE (turno, mixto, UGEL)", "`TURNO`, `INED`, `UNGEEDLO`"],
        ],
    )
    only01 = md_table(
        ["Solo CRS01 (18+)", "Variable"],
        [
            ["Vivienda, servicios, 21 activos", "`C1P101`–`C1P110_*`"],
            ["Estado civil, hijas/os, embarazo", "`C1P302`, `C1P304`, `C1P306`"],
            ["Trabajo, ocupación, quién gasta su ingreso", "`C1P307`–`C1P313`"],
            ["Seguro, programas sociales (JUNTOS, Pensión 65…)", "`C1P314`, `C1P315`"],
            ["Violencia de pareja, control, otras personas desde los 18", "`C1P402`, `C1P411`, CAP400"],
            ["Recuerdo de infancia hasta los 11 (no es el módulo CRS04)", "`CAP441A_1`…`_6`"],
        ],
    )

    asegurar_docs()
    DOC.write_text(
        f"""# CRS01 vs CRS04: ¿la misma información individual?

{ficha(
    que_es="Qué se les pregunta a las de 18+ y a las de 12–17: qué dominio se pisa y qué no. Sirve para no mezclar ítems que parecen iguales.",
    que_no="No une personas. No es el inventario completo ni las distribuciones de controles.",
    tipo="Descriptivo",
    script="scripts/descriptivos/descriptivos_crs01.py",
)}
No. Las mujeres de 18+ **no tienen el mismo cuestionario** que las de 12–17. Hay un núcleo que se pregunta a ambas (etnia, migración, discapacidad, tamaño/composición del hogar, tareas). El resto no se cruza: las adultas tienen vivienda y violencia de pareja; las adolescentes tienen cuidado, colegio y victimización escolar.

Universo CRS01: `analisis.crs01_mujeres` · n = {fmt_n(n)} · N = {fmt_n(nexp)} con `FACTOR_MUJ` · edad {edad[0]}–{edad[1]} (media ponderada {edad[2]:.1f}).

Universo CRS04: alumnas `SEXO=1` · n = 9,608 · N = 1,419,491 con `FACTOR_ALUMNOS`. Detalle: [descriptivos_controles.md](descriptivos_controles.md).

---

## Lo que se les pregunta a ambos

No son los mismos nombres de columna (`C3P`/`C4P` vs `C1P`). Sí es el mismo **dominio**.

{overlap}

Para comparar prevalencias entre edades, usa solo esa lista. Recode etnia y discapacidad 1:1. Área y departamento: en CRS04 es la IE; en CRS01 es el hogar. Lengua **no** se compare sin recode: en la niña es “qué hablan en casa”, en la adulta es “qué aprendió de niña”.

Tamaño de hogar de referencia: CRS01 media {hog:.2f} miembros (padrón); CRS04 media 5.16 (ella cuenta, incluye a ella).

---

## Solo un grupo

{only04}

{only01}

---

## Descriptivos CRS01 (mujeres 18+)

Peso `FACTOR_MUJ`. Missing de edad = 0.

### Territorio

{t_area}

Top departamentos:

{t_depto}

Hace 5 años, ¿vivía en este distrito?

{t_mig}

### Edad, estado civil, hijas/os

{t_edad}

{t_civil}

{t_hijos}

### Educación y trabajo

{t_educ}

{t_trab}

Quién mantiene económicamente (`C1P316_7`):

{t_dinero}

### Etnia y lengua materna

`C1P306_E` (mismas categorías que `C4P129`):

{t_etnia}

`C1P306_F` (no es el idioma del hogar de CRS04):

{t_lengua}

### Discapacidad

Algún `C1P209_A_*` = 1: n = {fmt_n(disc[0])} ({fmt_pct(disc[0], n)} de casos) · N = {fmt_n(disc[1])} ({fmt_pct(disc[1], nexp)}). En CRS04 el mismo listado da 12.4% de N: otro universo y otro flujo (en C1 hay un filtro de “dependencia”).

### Vivienda (solo C1)

Agua, luz, desagüe y activos: [descriptivos_controles.md](descriptivos_controles.md#crs01--servicios-y-activos-no-se-pegan-a-crs04). No se le preguntan a la de 12–17.

---

## Qué implica para el modelo

No armes un solo LASSO mezclando filas de C1 y CRS04: factores, grano y targets son distintos.

Si quieres **comparar perfiles** (adolescente vs adulta): usa el bloque común (etnia, migración, discapacidad, composición/tamaño, quién mantiene, área) con recodes alineados, y deja vivienda solo en C1 y cuidado/colegio solo en CRS04.

Si el modelo es **solo CRS04**, C1 aporta controles territoriales (depto × área), no variables individuales de la niña.
""",
        encoding="utf-8",
    )
    print(f"wrote {DOC}")


if __name__ == "__main__":
    main()
