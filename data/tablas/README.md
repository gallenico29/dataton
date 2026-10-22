# data/tablas/

| Archivo | |
| --- | --- |
| `enares.duckdb` | CSV de `datos_dev/` cargados. Lo escribe `build_db.py`. |
| `crs04_modelo.parquet` | Matriz X + Y de alumnas. Lo escribe `procesar_crs04.py`. |
| `crs04_filtro_violencia.parquet` | Sí/no de las 3 Y + alguna. Lo escribe `armar_filtro_violencia.py`. |
| `lasso_crs04_coef.csv` | Coeficientes L1. Lo escribe `lasso_crs04.py`; lo leen k-medias y CART. |
| `perfiles_kmeans_asig.csv` | Cluster por alumna. Lo escribe `perfiles_kmeans_crs04.py`. |
