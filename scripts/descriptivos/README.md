# Descriptivos

Son **Python**, no R Markdown. Cada script **escribe** el informe en `docs/descriptivos/` o `docs/metodologia/` (y a veces SVG en `docs/img/`). Tú corres el `.py`; el entregable que se lee es el `.md`.

Necesitan `data/tablas/enares.duckdb` (sale de `scripts/tablas/build_db.py`).

El mapa de *todos* los informes (descriptivos / metodología / resultados): [docs/README.md](../../docs/README.md).

| Script | Para qué | Qué escribe |
| --- | --- | --- |
| `inventario_variables.py` | Diccionario de preguntas CRS04 y CRS01. | `docs/descriptivos/inventario_*.md` · CSV en `data/tablas/` (misma tabla para Excel, no es otro informe) |
| `descriptivos_controles.py` | Cómo se ve la muestra + cruces livianos con las 3 Y. | `docs/descriptivos/descriptivos_controles.md` |
| `informe_muestral_predictores.py` | **Dos** informes: (1) números del diseño; (2) cada X candidata. | `docs/metodologia/diseno_muestral.md` · `docs/descriptivos/descriptivos_predictores_crs04.md` |
| `descriptivos_crs01.py` | Qué se pregunta a 18+ vs 12–17. No une personas. | `docs/descriptivos/descriptivos_crs01_vs_crs04.md` |
| `generate_crs04_charts.py` | Solo las figuras del doc de violencia 12m. | `docs/img/crs04_*.svg` |

```bash
python scripts/descriptivos/inventario_variables.py
python scripts/descriptivos/descriptivos_controles.py
python scripts/descriptivos/informe_muestral_predictores.py
python scripts/descriptivos/descriptivos_crs01.py
```
