"""Carga los CSV de ENARES en DuckDB y arma tablas de análisis.

Uso:
    python scripts/build_db.py
"""

from __future__ import annotations

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATOS = ROOT / "datos_dev"
DB_PATH = ROOT / "data" / "enares.duckdb"

CSV = {
    "raw.crs01_cap100": DATOS / "976-Modulo1941/976-Modulo1941/01_CRS01_CAP100.csv",
    "raw.crs01_cap200": DATOS / "976-Modulo1942/976-Modulo1942/02_CRS01_CAP200.csv",
    "raw.crs01_cap300": DATOS / "976-Modulo1943/976-Modulo1943/03_CRS01_CAP300.csv",
    "raw.crs01_cap400": DATOS / "976-Modulo1944/976-Modulo1944/04_CRS01_CAP400.csv",
    "raw.crs01_cap402": DATOS / "976-Modulo1945/976-Modulo1945/05_CRS01_CAP402.csv",
    "raw.crs01_cap405": DATOS / "976-Modulo1946/976-Modulo1946/06_CRS01_CAP405.csv",
    "raw.crs01_cap411": DATOS / "976-Modulo1947/976-Modulo1947/07_CRS01_CAP411.csv",
    "raw.crs01_cap500": DATOS / "976-Modulo1948/976-Modulo1948/08_CRS01_CAP500.csv",
    "raw.crs01_cap600": DATOS / "976-Modulo1949/976-Modulo1949/09_CRS01_CAP600.csv",
    "raw.crs01_cap700": DATOS / "976-Modulo1950/976-Modulo1950/10_CRS01_CAP700.csv",
    "raw.crs02_cap100": DATOS / "976-Modulo1951/976-Modulo1951/11_CRS02_CAP100.csv",
    "raw.crs02_cap200": DATOS / "976-Modulo1952/976-Modulo1952/12_CRS02_CAP200.csv",
    "raw.crs02_cap300": DATOS / "976-Modulo1953/976-Modulo1953/13_CRS02_CAP300.csv",
    "raw.crs02_cap400": DATOS / "976-Modulo1954/976-Modulo1954/14_CRS02_CAP400.csv",
    "raw.crs02_cap500": DATOS / "976-Modulo1955/976-Modulo1955/15_CRS02_CAP500.csv",
    "raw.crs03_cap100": DATOS / "976-Modulo1956/976-Modulo1956/16_CRS03_CAP100.csv",
    "raw.crs03_cap200": DATOS / "976-Modulo1957/976-Modulo1957/17_CRS03_CAP200.csv",
    "raw.crs03_cap300": DATOS / "976-Modulo1958/976-Modulo1958/18_CRS03_CAP300.csv",
    "raw.crs04_cap100": DATOS / "976-Modulo1959/976-Modulo1959/19_CRS04_CAP100.csv",
    "raw.crs04_cap200": DATOS / "976-Modulo1960/976-Modulo1960/20_CRS04_CAP200.csv",
    "raw.crs04_cap248": DATOS / "976-Modulo1961/976-Modulo1961/21_CRS04_CAP248.csv",
    "raw.crs04_cap300": DATOS / "976-Modulo1962/976-Modulo1962/22_CRS04_CAP300.csv",
}

def ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def columns(con: duckdb.DuckDBPyConnection, table: str) -> list[str]:
    return [row[0] for row in con.execute(f"DESCRIBE {table}").fetchall()]


def load_csvs(con: duckdb.DuckDBPyConnection) -> None:
    for table, path in CSV.items():
        if not path.exists():
            raise FileNotFoundError(path)
        csv_path = path.resolve().as_posix()
        print(f"Cargando {table} <- {path.name}")
        con.execute(
            f"""
            CREATE TABLE {table} AS
            SELECT * FROM read_csv(
                '{csv_path}',
                header = true,
                auto_detect = true,
                sample_size = -1,
                nullstr = ['', ' ']
            )
            """
        )


def select_all(alias: str, cols: list[str]) -> list[str]:
    return [f"{alias}.{ident(col)} AS {ident(col)}" for col in cols]


def select_extra(alias: str, cols: list[str], skip: set[str]) -> tuple[list[str], set[str]]:
    pieces = []
    added = set()
    for col in cols:
        if col in skip:
            continue
        pieces.append(f"{alias}.{ident(col)} AS {ident(col)}")
        added.add(col)
    return pieces, skip | added


def create_joined_table(
    con: duckdb.DuckDBPyConnection,
    dest: str,
    base: tuple[str, str],
    extras: list[tuple[str, str, str]],
    base_exclude: set[str] | None = None,
) -> None:
    """Une tablas por la expresión SQL `on`, sin repetir columnas de identificación."""
    base_table, base_alias = base
    exclude = base_exclude or set()
    base_cols = [col for col in columns(con, base_table) if col not in exclude]
    select_sql = select_all(base_alias, base_cols)
    skip = set(base_cols)

    joins = []
    for table, alias, on_sql in extras:
        extra_sql, skip = select_extra(alias, columns(con, table), skip)
        select_sql.extend(extra_sql)
        joins.append(f"LEFT JOIN {table} {alias} ON {on_sql}")

    con.execute(
        f"""
        CREATE TABLE {dest} AS
        SELECT
            {", ".join(select_sql)}
        FROM {base_table} {base_alias}
        {" ".join(joins)}
        """
    )


def create_analysis(con: duckdb.DuckDBPyConnection) -> None:
    create_joined_table(
        con,
        "analisis.crs01_mujeres",
        ("raw.crs01_cap100", "v"),
        [
            ("raw.crs01_cap300", "p", "v.ID = p.ID"),
            ("raw.crs01_cap200", "pad", "p.ID = pad.ID AND p.PERSONA_ID = pad.PERSONA_ID"),
            ("raw.crs01_cap400", "c400", "v.ID = c400.ID"),
            ("raw.crs01_cap500", "c500", "v.ID = c500.ID"),
            ("raw.crs01_cap600", "c600", "v.ID = c600.ID"),
            ("raw.crs01_cap700", "c700", "v.ID = c700.ID"),
        ],
        base_exclude={"PERSONA_ID"},
    )

    con.execute("CREATE TABLE analisis.crs01_padron AS SELECT * FROM raw.crs01_cap200")
    con.execute("CREATE VIEW analisis.crs01_cap402 AS SELECT * FROM raw.crs01_cap402")
    con.execute("CREATE VIEW analisis.crs01_cap405 AS SELECT * FROM raw.crs01_cap405")
    con.execute("CREATE VIEW analisis.crs01_cap411 AS SELECT * FROM raw.crs01_cap411")

    create_joined_table(
        con,
        "analisis.crs02_adultos",
        ("raw.crs02_cap100", "v"),
        [
            ("raw.crs02_cap300", "p", "v.ID = p.ID"),
            ("raw.crs02_cap200", "pad", "p.ID = pad.ID AND p.PERSONA_ID = pad.PERSONA_ID"),
            ("raw.crs02_cap400", "c400", "v.ID = c400.ID"),
            ("raw.crs02_cap500", "c500", "v.ID = c500.ID"),
        ],
        base_exclude={"PERSONA_ID"},
    )
    con.execute("CREATE TABLE analisis.crs02_padron AS SELECT * FROM raw.crs02_cap200")

    create_joined_table(
        con,
        "analisis.crs03_ninos",
        ("raw.crs03_cap100", "a"),
        [
            ("raw.crs03_cap200", "c200", "a.ID = c200.ID AND a.COLEGIAL_ID = c200.COLEGIAL_ID"),
            ("raw.crs03_cap300", "c300", "a.ID = c300.ID AND a.COLEGIAL_ID = c300.COLEGIAL_ID"),
        ],
    )

    create_joined_table(
        con,
        "analisis.crs04_adolescentes",
        ("raw.crs04_cap100", "a"),
        [
            ("raw.crs04_cap200", "c200", "a.ID = c200.ID AND a.COLEGIAL_ID = c200.COLEGIAL_ID"),
            ("raw.crs04_cap248", "c248", "a.ID = c248.ID AND a.COLEGIAL_ID = c248.COLEGIAL_ID"),
            ("raw.crs04_cap300", "c300", "a.ID = c300.ID AND a.COLEGIAL_ID = c300.COLEGIAL_ID"),
        ],
    )

    con.execute(
        """
        CREATE TABLE analisis.ubigeo AS
        SELECT DISTINCT CCDD, DEPARTAMENTO, CCPP, PROVINCIA, CCDI, DISTRITO, CODCCPP, NOMCCPP, AREA
        FROM (
            SELECT CCDD, DEPARTAMENTO, CCPP, PROVINCIA, CCDI, DISTRITO, CODCCPP, NOMCCPP, AREA
            FROM raw.crs01_cap100
            UNION
            SELECT CCDD, DEPARTAMENTO, CCPP, PROVINCIA, CCDI, DISTRITO, CODCCPP, NOMCCPP, AREA
            FROM raw.crs02_cap100
            UNION
            SELECT CCDD, DEPARTAMENTO, CCPP, PROVINCIA, CCDI, DISTRITO, CODCCPP, NOMCCPP, AREA
            FROM raw.crs03_cap100
            UNION
            SELECT CCDD, DEPARTAMENTO, CCPP, PROVINCIA, CCDI, DISTRITO, CODCCPP, NOMCCPP, AREA
            FROM raw.crs04_cap100
        )
        """
    )

    con.execute(
        """
        CREATE TABLE meta.catalogo (
            objeto VARCHAR,
            tipo VARCHAR,
            grano VARCHAR,
            llave VARCHAR,
            factor VARCHAR,
            descripcion VARCHAR
        )
        """
    )
    con.executemany(
        "INSERT INTO meta.catalogo VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                "analisis.crs01_mujeres",
                "tabla",
                "mujer seleccionada 18+",
                "ID",
                "FACTOR_MUJ / FACTOR_VIV / FACTOR_POBLACION",
                "CRS01 vivienda + entrevistada + padrón de la seleccionada + caps 400/500/600/700",
            ),
            (
                "analisis.crs01_padron",
                "tabla",
                "persona del hogar",
                "ID + PERSONA_ID",
                "FACTOR_POBLACION",
                "CRS01 CAP200, todos los residentes",
            ),
            (
                "analisis.crs01_cap402",
                "vista",
                "mujer seleccionada 18+",
                "ID + PERSONA_ID",
                "FACTOR_MUJ",
                "Satélite: ítems detallados de violencia (ancho)",
            ),
            (
                "analisis.crs01_cap405",
                "vista",
                "mujer seleccionada 18+",
                "ID + PERSONA_ID",
                "FACTOR_MUJ",
                "Satélite: ítems detallados CAP405 (ancho)",
            ),
            (
                "analisis.crs01_cap411",
                "vista",
                "mujer seleccionada 18+",
                "ID + PERSONA_ID",
                "FACTOR_MUJ",
                "Satélite: ítems detallados CAP411 (muy ancho, ~113 MB)",
            ),
            (
                "analisis.crs02_adultos",
                "tabla",
                "adulto seleccionado 18+",
                "ID",
                "FACTOR_HYM / FACTOR_VIV / FACTOR_POBLACION",
                "CRS02 vivienda + entrevistado + padrón del seleccionado + caps 400/500",
            ),
            (
                "analisis.crs02_padron",
                "tabla",
                "persona del hogar",
                "ID + PERSONA_ID",
                "FACTOR_POBLACION",
                "CRS02 CAP200, todos los residentes",
            ),
            (
                "analisis.crs03_ninos",
                "tabla",
                "alumno 9-11",
                "ID + COLEGIAL_ID",
                "FACTOR_ALUMNOS",
                "CRS03 todos los capítulos unidos",
            ),
            (
                "analisis.crs04_adolescentes",
                "tabla",
                "alumno 12-17",
                "ID + COLEGIAL_ID",
                "FACTOR_ALUMNOS",
                "CRS04 todos los capítulos unidos",
            ),
            (
                "analisis.ubigeo",
                "tabla",
                "centro poblado / área",
                "CCDD + CCPP + CCDI + CODCCPP + AREA",
                "",
                "Geografía distinta de las cuatro encuestas, para cruces agregados",
            ),
        ],
    )


def report(con: duckdb.DuckDBPyConnection) -> None:
    print("\n=== Conteos ===")
    for name in [
        "raw.crs01_cap100",
        "raw.crs01_cap200",
        "analisis.crs01_mujeres",
        "analisis.crs01_padron",
        "raw.crs02_cap100",
        "raw.crs02_cap200",
        "analisis.crs02_adultos",
        "analisis.crs02_padron",
        "raw.crs03_cap100",
        "analisis.crs03_ninos",
        "raw.crs04_cap100",
        "analisis.crs04_adolescentes",
        "analisis.ubigeo",
    ]:
        n = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        k = len(columns(con, name))
        print(f"  {name:32} {n:>8} filas  {k:>5} cols")

    print("\n=== Integridad de joins ===")
    checks = [
        (
            "CRS01 mujeres vs CAP100",
            """
            SELECT
                (SELECT COUNT(*) FROM raw.crs01_cap100) AS vivienda,
                (SELECT COUNT(*) FROM analisis.crs01_mujeres) AS analisis,
                (SELECT COUNT(*) FROM analisis.crs01_mujeres WHERE PERSONA_ID IS NULL) AS sin_persona
            """,
        ),
        (
            "CRS02 adultos vs CAP100",
            """
            SELECT
                (SELECT COUNT(*) FROM raw.crs02_cap100) AS vivienda,
                (SELECT COUNT(*) FROM analisis.crs02_adultos) AS analisis,
                (SELECT COUNT(*) FROM analisis.crs02_adultos WHERE PERSONA_ID IS NULL) AS sin_persona
            """,
        ),
        (
            "CRS03 niños vs CAP100",
            """
            SELECT
                (SELECT COUNT(*) FROM raw.crs03_cap100) AS alumnos,
                (SELECT COUNT(*) FROM analisis.crs03_ninos) AS analisis
            """,
        ),
        (
            "CRS04 adolescentes vs CAP100",
            """
            SELECT
                (SELECT COUNT(*) FROM raw.crs04_cap100) AS alumnos,
                (SELECT COUNT(*) FROM analisis.crs04_adolescentes) AS analisis
            """,
        ),
        (
            "Llaves duplicadas CRS01",
            "SELECT COUNT(*) - COUNT(DISTINCT ID) AS dup_id FROM analisis.crs01_mujeres",
        ),
        (
            "Llaves duplicadas CRS02",
            "SELECT COUNT(*) - COUNT(DISTINCT ID) AS dup_id FROM analisis.crs02_adultos",
        ),
        (
            "Llaves duplicadas CRS03",
            "SELECT COUNT(*) - COUNT(DISTINCT (ID, COLEGIAL_ID)) AS dup_id FROM analisis.crs03_ninos",
        ),
        (
            "Llaves duplicadas CRS04",
            "SELECT COUNT(*) - COUNT(DISTINCT (ID, COLEGIAL_ID)) AS dup_id FROM analisis.crs04_adolescentes",
        ),
        (
            "CRS01 padron de seleccionada",
            """
            SELECT
                COUNT(*) FILTER (WHERE C1P201 IS NULL) AS sin_padron,
                COUNT(*) FILTER (WHERE C1P201 IS NOT NULL) AS con_padron
            FROM analisis.crs01_mujeres
            """,
        ),
        (
            "CRS02 padron de seleccionado",
            """
            SELECT
                COUNT(*) FILTER (WHERE C1P201 IS NULL) AS sin_padron,
                COUNT(*) FILTER (WHERE C1P201 IS NOT NULL) AS con_padron
            FROM analisis.crs02_adultos
            """,
        ),
    ]
    for title, sql in checks:
        print(f"  {title}: {con.execute(sql).fetchone()}")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    wal = Path(str(DB_PATH) + ".wal")
    if wal.exists():
        wal.unlink()

    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA raw")
        con.execute("CREATE SCHEMA analisis")
        con.execute("CREATE SCHEMA meta")
        load_csvs(con)
        print("\nCreando tablas de análisis...")
        create_analysis(con)
        report(con)
        print(f"\nListo: {DB_PATH}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
