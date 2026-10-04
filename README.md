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

## Levantar el dashboard

Interfaz en `web/` (HTML + JS, sin npm). El servidor tiene que mandar UTF-8; si no, las ñ y tildes salen rotas.

**1.** En una terminal, ve a la raíz del repo (`C:\dev\dataton` o donde hayas clonado). Tienes que ver `web\serve.py` y `web\index.html`.

**2.** Comprueba que existan al menos estos archivos (si faltan, ve al paso 5):

- `web/index.html`
- `web/data/enares.json`
- `web/data/departamentos.json`
- `web/data/cem.geojson`
- `web/data/peru_departamentos.geojson`
- `web/data/perfiles.json`

**3.** Arranca el servidor (déjalo corriendo; no cierres esa terminal):

```bash
python web/serve.py
```

Tiene que imprimir:

```
Dashboard en http://127.0.0.1:8765/
```

**4.** En el navegador abre exactamente esa URL: [http://127.0.0.1:8765/](http://127.0.0.1:8765/). Debes ver el mapa del Perú, filtros (violencia, edad, región) y el panel. Para parar: `Ctrl+C` en la terminal.

No abras `web/index.html` con doble clic ni con `file://`: los módulos JS no cargan y las tildes se rompen. Tampoco uses `python -m http.server` (no pone `charset=utf-8`).

Puerto ocupado o quieres otro: `python web/serve.py 8766` y abre `http://127.0.0.1:8766/`.

**5.** Si el mapa sale vacío, “No se pudieron cargar los datos”, o no están los JSON del paso 2, regenera y vuelve a servir:

```bash
python scripts/tablas/armar_dashboard.py
python web/serve.py
```

`armar_dashboard.py` pide `data/tablas/crs04_modelo.parquet` y los CEM/SALUD/MP en `data/`. Recetario: [paso 4](#4-dashboard-web).

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

### 4. Dashboard (`web/`)

Solo ver la app (JSON ya listos): [Levantar el dashboard](#levantar-el-dashboard).

Necesita el JSON de `scripts/tablas/armar_dashboard.py` (y por tanto `crs04_modelo.parquet` + los CSV/GeoJSON en `data/`).

```bash
python scripts/tablas/armar_dashboard.py
python web/serve.py
```

Abre http://127.0.0.1:8765/ — módulos en `web/js/`. Usa `web/serve.py` (manda UTF-8) y no abras el HTML como `file://`.

| Comando | Sale |
| --- | --- |
| `armar_dashboard.py` | `web/data/` (ENARES por dpto, CEM, SALUD, MP) |
| servidor HTTP | interfaz en el navegador |

### Qué no sale de un script

Estos se editan a mano. Correr Python **no** los regenera:

- [docs/metodologia/metodologia.md](docs/metodologia/metodologia.md)
- [docs/metodologia/viabilidad_desfases.md](docs/metodologia/viabilidad_desfases.md)
- [docs/descriptivos/violencia_por_cuestionario.md](docs/descriptivos/violencia_por_cuestionario.md)
- [docs/descriptivos/violencia_crs04_si_no_missing.md](docs/descriptivos/violencia_crs04_si_no_missing.md) (el texto; las SVG sí las hace `generate_crs04_charts.py`)
