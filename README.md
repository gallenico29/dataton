# dataton

Encuesta ENARES (INEI). Los CSV/PDF van en `datos_dev/` (no están en git: GitHub rechaza archivos > 100 MB; `07_CRS01_CAP411.csv` pesa 113 MB). La base analítica se genera así:

```bash
pip install -r requirements.txt
python scripts/build_db.py
```

Queda en `data/enares.duckdb`. Las tablas listas para modelar están en el esquema `analisis` (`crs01_mujeres`, `crs02_adultos`, `crs03_ninos`, `crs04_adolescentes`). El detalle de grano y llaves está en `meta.catalogo`.