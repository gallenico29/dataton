# dataton

ENARES 2024. Perfiles de alumnas 12–17 (CRS.04) y contexto de vivienda por departamento (CRS.01, mujeres 18+). El tablero está en `web/`.

```
datos_dev/          crudos INEI (gitignored)
data/               CEM fuente + tablas de trabajo (ver data/README.md)
scripts/tablas/     duckdb, matriz, JSON del tablero
scripts/modelos/    LASSO → k-medias → CART
scripts/descriptivos/
docs/               informes
web/                tablero
```

Índice de informes: [docs/README.md](docs/README.md).

## Tablero

Es HTML/CSS/JS estático. No hace falta Railway.

**Para mostrarlo a alguien ahora:** abre o manda `web/tablero.html`. Es el tablero entero en un solo archivo (necesita internet por el mapa). Si cambiaste datos o textos:

```bash
uv run python scripts/tablas/exportar_tablero.py
```

**En tu máquina, con el repo:**

```bash
uv sync
uv run python web/serve.py
```

Abre [http://127.0.0.1:8765/](http://127.0.0.1:8765/). Otro puerto: `uv run python web/serve.py 8766`.

**URL pública:** [https://gallenico29.github.io/dataton/](https://gallenico29.github.io/dataton/). GitHub Pages sirve `web/` (workflow en `.github/workflows/pages.yml`). Si el link da 404, en el repo: Settings → Pages → Source = GitHub Actions, y espera a que corra el workflow.

Si faltan los JSON de `web/data/`:

```bash
uv run python scripts/tablas/armar_dashboard.py
uv run python scripts/tablas/exportar_tablero.py
uv run python web/serve.py
```

`armar_dashboard.py` pide `crs04_modelo.parquet`, `enares.duckdb` y `data/cem_regulares_2025.geojson`.

## Recrear tablas e informes

Los scripts pisan el archivo que escriben. Prefijo: `uv run python`.

```bash
uv run python scripts/tablas/build_db.py
uv run python scripts/tablas/procesar_crs04.py
uv run python scripts/tablas/armar_filtro_violencia.py

uv run python scripts/modelos/lasso_crs04.py
uv run python scripts/modelos/perfiles_kmeans_crs04.py
uv run python scripts/modelos/perfiles_cart_crs04.py

uv run python scripts/descriptivos/inventario_variables.py
uv run python scripts/descriptivos/descriptivos_controles.py
uv run python scripts/descriptivos/informe_muestral_predictores.py
uv run python scripts/descriptivos/descriptivos_crs01.py
uv run python scripts/descriptivos/generate_crs04_charts.py

uv run python scripts/tablas/armar_dashboard.py
uv run python scripts/tablas/exportar_tablero.py
```

| Script | Sale |
| --- | --- |
| `build_db.py` | `data/tablas/enares.duckdb` |
| `procesar_crs04.py` | `crs04_modelo.parquet` |
| `armar_filtro_violencia.py` | `crs04_filtro_violencia.parquet` (sí/no de las 3 Y) |
| `lasso_crs04.py` | [lasso_crs04.md](docs/resultados/lasso_crs04.md) · `lasso_crs04_coef.csv` |
| `perfiles_kmeans_crs04.py` | [perfiles_kmeans_crs04.md](docs/resultados/perfiles_kmeans_crs04.md) · `perfiles_kmeans_asig.csv` |
| `perfiles_cart_crs04.py` | [perfiles_cart_crs04.md](docs/resultados/perfiles_cart_crs04.md) |
| `inventario_variables.py` | `inventario_crs04.md` / `inventario_crs01.md` |
| `descriptivos_controles.py` | `descriptivos_controles.md` |
| `informe_muestral_predictores.py` | `diseno_muestral.md` · `descriptivos_predictores_crs04.md` |
| `descriptivos_crs01.py` | `descriptivos_crs01_vs_crs04.md` |
| `generate_crs04_charts.py` | `docs/img/crs04_*.svg` |
| `armar_dashboard.py` | `web/data/` |
| `exportar_tablero.py` | `web/tablero.html` (un archivo, para mandar) |

A mano (no los pisa ningún script): [metodologia.md](docs/metodologia/metodologia.md) y [violencia_crs04_si_no_missing.md](docs/descriptivos/violencia_crs04_si_no_missing.md).

Si cambió un recode: `procesar_crs04.py` → filtro → LASSO → k-medias / CART. El duckdb solo si cambió un crudo.
