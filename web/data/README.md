# web/data/

JSON que sirve el tablero. Los regenera `armar_dashboard.py`, salvo `perfiles.json` y `peru_departamentos.geojson`. Para un HTML de un solo archivo: `exportar_tablero.py`.

| Archivo | |
| --- | --- |
| `meta.json` | Universo, etiquetas de factores, nota CEM. |
| `departamentos.json` | Catálogo 25 dptos (código, centro, n CEM). |
| `enares.json` | Prevalencias y factores CRS.04 por dpto y edad. |
| `vivienda.json` | Luz, agua, desagüe CRS.01 por dpto (territorio, no se une a la alumna). |
| `cem.json` | Centros por departamento (lista del panel). |
| `cem.geojson` | Mismos centros, puntos del mapa. |
| `perfiles.json` | Textos de las tarjetas k-medias. |
| `peru_departamentos.geojson` | Polígonos del mapa. |
