# Diseño muestral: CRS04 (12–17) y CRS01 (mujeres 18+)

> PSU, estrato y peso de CRS04 y CRS01. (`scripts/descriptivos/informe_muestral_predictores.py`)

ENARES 2024. Estrato, conglomerado y peso de las dos encuestas. Las muestras no se unen a nivel persona (`ID` no es llave común).

Universo de trabajo CRS04: `analisis.crs04_adolescentes`, `SEXO = 1` · n = 9,608 · N = 1,419,491 (`FACTOR_ALUMNOS`).

Universo CRS01: `analisis.crs01_mujeres` · n = 13,826 · N mujer = 12,401,665 (`FACTOR_MUJ`) · N hogar = 10,517,286 (`FACTOR_VIV`).

---

## CRS04 y CRS01

| Pieza | CRS04 alumnas 12–17 | CRS01 mujeres 18+ |
| --- | --- | --- |
| Marco | Institución educativa (secundaria regular) | Vivienda / hogar |
| Fila | Alumna | Mujer seleccionada (1 por hogar) |
| Llave de la fila | `ID` + `COLEGIAL_ID` | `ID` (hogar) · `PERSONA_ID` de la seleccionada |
| Conglomerado | `ID` de la escuela. `CONGLOME` no está en el archivo (0 columnas). | `CONGLOME` |
| Sección | `C3SECC` | Una mujer por hogar |
| Estrato | `AREA` × `DEPARTAMENTO` de la escuela (49 celdas; Callao sin rural) | `AREA` × `DEPARTAMENTO` del hogar (49 celdas; Callao sin rural) |
| Peso | `FACTOR_ALUMNOS` (mín 2.12, máx 5,194) | `FACTOR_MUJ` en la mujer · `FACTOR_VIV` en la vivienda |
| Área y departamento | De la escuela. El 12,7 % de la N no vive en el distrito de la escuela. | Del hogar |

---

## CRS04

El conglomerado es `ID`. Varias alumnas comparten escuela.

| Estadístico | Valor |
| --- | ---: |
| IEs (`ID` distintos) | 1,086 |
| Alumnas por IE: mín / mediana / máx / media | 3 / 10 / 20 / 8.8 |
| Secciones distintas (`ID`+`C3SECC`) | 1,794 |
| Secciones por IE: mín / mediana / máx / media | 1 / 2 / 5 / 1.65 |
| Alumnas por sección: mín / mediana / máx / media | 1 / 5 / 20 / 5.4 |
| Estratos `AREA`×`DEPARTAMENTO` | 49 (de 25 × 2 = 50; falta Callao rural) |
| PSU por estrato: mín / mediana / máx | 2 / 25 / 70 |
| Estratos con 1 PSU | **0** |
| Estratos con exactamente 2 PSU | 1 |

Ningún estrato tiene una sola escuela. Estratos con 4 escuelas o menos:

| Departamento | Área | IE (PSU) | n alumnas |
| --- | --- | ---: | ---: |
| TACNA | Rural | 2 | 10 |
| AREQUIPA | Rural | 4 | 21 |
| ICA | Rural | 4 | 20 |
| MOQUEGUA | Rural | 4 | 20 |
| TUMBES | Rural | 4 | 20 |

Tacna rural: 2 escuelas, 10 alumnas. `nest = TRUE` porque el identificador de escuela puede repetirse entre estratos. La sección (`C3SECC`, mediana 2 por escuela) no entra como segunda etapa. El ajuste usa `ids = ID`, estrato `AREA` × `DEPARTAMENTO` y peso `FACTOR_ALUMNOS`.

---

## CRS01

Una mujer por hogar: n = 13,826. El conglomerado es `CONGLOME`, no el hogar.

| Estadístico | Valor |
| --- | ---: |
| Conglomerados | 1,750 |
| Mujeres (= hogares) por `CONGLOME`: mín / mediana / máx / media | 1 / 8 / 12 / 7.9 |
| Estratos `AREA`×`DEPARTAMENTO` | 49 |
| PSU por estrato: mín / mediana / máx | 2 / 27 / 262 |
| Estratos con 1 PSU | **0** |
| Estratos con exactamente 2 PSU | 1 |

Estratos con 4 conglomerados o menos:

| Departamento | Área | CONGLOME (PSU) | n mujeres |
| --- | --- | ---: | ---: |
| TUMBES | Rural | 2 | 24 |
| ICA | Rural | 4 | 48 |

Tumbes rural: 2 conglomerados, 24 mujeres.

La mujer se expande con `FACTOR_MUJ`. La vivienda (agua, desagüe, activos) se expande con `FACTOR_VIV`. Mismo conglomerado y mismo estrato. `FACTOR_NIÑOS` está vacío en el 80 % de las filas de este recorte. `FACTOR_POBLACION` es el peso del padrón.

El modelo de alumnas usa solo CRS04. Los servicios de CRS01 se muestran por departamento de la escuela y no se pegan a la fila.

---

## Límites

- `RFINAL = 2` (encuesta incompleta) en CRS04: 12.4% de casos, 21.6% de la N. Los ítems de violencia están llenos; el peso de las incompletas es más alto.
- En CRS04, `AREA` urbana es de la IE. No es “vive en zona urbana”.
- 18 filas CAR (`C3P105 = 2`) se saltan el flujo de casa: missing de `C3P114`/`C3P115`/`C3P120` no es no-respuesta.

Las tres Y y la lectura de los OR: [metodologia.md](metodologia.md). Distribuciones de las X: [../descriptivos/descriptivos_predictores_crs04.md](../descriptivos/descriptivos_predictores_crs04.md).
