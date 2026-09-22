# dataton

ENARES 2024 (INEI). Crudos y productos van **separados**. Los CSV/PDF de INEI no están en git (`datos_dev/`; `07_CRS01_CAP411.csv` pesa 113 MB).

## Carpetas

```
datos_dev/                 crudos INEI (CSV + PDF). No se modifican.
data/tablas/               productos: duckdb, parquet, csv de trabajo
scripts/
  rutas.py                 un solo mapa de rutas
  tablas/                  creación de tablas
  descriptivos/            inventarios y descriptivos → docs/descriptivos/
  modelos/                 LASSO, k-medias, CART → docs/resultados/
docs/
  descriptivos/            cómo se ve la muestra
  metodologia/             decisiones (universo, diseño, recodes)
  resultados/              LASSO / k-medias / CART
  img/                     figuras
```

Índice de informes (qué es cada uno): [docs/README.md](docs/README.md).

| Qué | Dónde |
| --- | --- |
| Microdatos INEI | `datos_dev/` |
| DuckDB analítico | `data/tablas/enares.duckdb` |
| Matriz X + Y recodificada | `data/tablas/crs04_modelo.parquet` |
| Filtro sí/no violencia (k-medias) | `data/tablas/crs04_filtro_violencia.parquet` |
| Coeficientes LASSO (tabla de trabajo) | `data/tablas/lasso_crs04_coef.csv` |
| Asignación de clusters | `data/tablas/perfiles_kmeans_asig.csv` |

Los CSV en `data/tablas/` no son informes: son la misma tabla para Excel o para que el siguiente script la lea.

El k-medias **no** arma el sí/no al vuelo: lee la tabla de filtro.

---

## Cómo crear todo de nuevo

Hace falta `datos_dev/` (crudos INEI) y Python. Desde la raíz del repo.

```bash
pip install -r requirements.txt
```

### 1. Tablas (`data/tablas/`)

En este orden. Cada uno **pisa** el archivo que escribe.

```bash
python scripts/tablas/build_db.py
python scripts/tablas/procesar_crs04.py
python scripts/tablas/armar_filtro_violencia.py
```

| Comando | Sale |
| --- | --- |
| `build_db.py` | `data/tablas/enares.duckdb` (crudos → tablas analíticas) |
| `procesar_crs04.py` | `crs04_modelo.parquet` (+ `.csv`) — X e Y recodificadas |
| `armar_filtro_violencia.py` | `crs04_filtro_violencia.parquet` (+ `.csv`) — sí/no de las 3 Y + alguna |

Si solo cambiaste un recode: `procesar_crs04.py` y después el filtro. El duckdb solo si cambió un crudo.

### 2. Informes de resultados (`docs/resultados/`)

Necesitan las tablas del paso 1. El LASSO primero: k-medias y CART leen `lasso_crs04_coef.csv`.

```bash
python scripts/modelos/lasso_crs04.py
python scripts/modelos/perfiles_kmeans_crs04.py
python scripts/modelos/perfiles_cart_crs04.py
```

| Comando | Sale |
| --- | --- |
| `lasso_crs04.py` | [docs/resultados/lasso_crs04.md](docs/resultados/lasso_crs04.md) y `data/tablas/lasso_crs04_coef.csv` |
| `perfiles_kmeans_crs04.py` | [docs/resultados/perfiles_kmeans_crs04.md](docs/resultados/perfiles_kmeans_crs04.md), figuras `docs/img/perfiles_*`, `perfiles_kmeans_asig.csv` |
| `perfiles_cart_crs04.py` | [docs/resultados/perfiles_cart_crs04.md](docs/resultados/perfiles_cart_crs04.md) y `docs/img/cart_*` |

Si solo quieres rehacer CART, basta el LASSO ya corrido. Si cambiaste la matriz, vuelve a correr los tres.

### 3. Informes descriptivos y de diseño

Necesitan el duckdb del paso 1. No necesitan el LASSO. Cada `.py` **escribe** el `.md` (no son Rmd). Detalle: [scripts/descriptivos/README.md](scripts/descriptivos/README.md).

```bash
python scripts/descriptivos/inventario_variables.py
python scripts/descriptivos/descriptivos_controles.py
python scripts/descriptivos/informe_muestral_predictores.py
python scripts/descriptivos/descriptivos_crs01.py
python scripts/descriptivos/generate_crs04_charts.py
```

| Comando | Sale |
| --- | --- |
| `inventario_variables.py` | `docs/descriptivos/inventario_crs04.md` y `inventario_crs01.md` · CSV en `data/tablas/` |
| `descriptivos_controles.py` | `docs/descriptivos/descriptivos_controles.md` y `docs/img/controles_*` |
| `informe_muestral_predictores.py` | `docs/metodologia/diseno_muestral.md` y `docs/descriptivos/descriptivos_predictores_crs04.md` |
| `descriptivos_crs01.py` | `docs/descriptivos/descriptivos_crs01_vs_crs04.md` |
| `generate_crs04_charts.py` | solo figuras `docs/img/crs04_*.svg` (el texto del doc de violencia es a mano) |

### Qué no sale de un script

Estos se editan a mano. Correr Python **no** los regenera:

- [docs/metodologia/metodologia.md](docs/metodologia/metodologia.md)
- [docs/descriptivos/violencia_por_cuestionario.md](docs/descriptivos/violencia_por_cuestionario.md)
- [docs/descriptivos/violencia_crs04_si_no_missing.md](docs/descriptivos/violencia_crs04_si_no_missing.md) (el texto; las SVG sí las hace `generate_crs04_charts.py`)
