# CRS01 vs CRS04: ¿la misma información individual?

> **Qué es este informe.** Qué se les pregunta a las de 18+ y a las de 12–17: qué dominio se pisa y qué no. Sirve para no mezclar ítems que parecen iguales.
> **Qué no es.** No une personas. No es el inventario completo ni las distribuciones de controles.
> **Tipo.** Descriptivo.
> **Lo escribe.** `scripts/descriptivos/descriptivos_crs01.py` (Python → markdown; no es Rmd).

No. Las mujeres de 18+ **no tienen el mismo cuestionario** que las de 12–17. Hay un núcleo que se pregunta a ambas (etnia, migración, discapacidad, tamaño/composición del hogar, tareas). El resto no se cruza: las adultas tienen vivienda y violencia de pareja; las adolescentes tienen cuidado, colegio y victimización escolar.

Universo CRS01: `analisis.crs01_mujeres` · n = 13,826 · N = 12,401,665 con `FACTOR_MUJ` · edad 18–99 (media ponderada 43.6).

Universo CRS04: alumnas `SEXO=1` · n = 9,608 · N = 1,419,491 con `FACTOR_ALUMNOS`. Detalle: [descriptivos_controles.md](descriptivos_controles.md).

---

## Lo que se les pregunta a ambos

No son los mismos nombres de columna (`C3P`/`C4P` vs `C1P`). Sí es el mismo **dominio**.

| Dominio | CRS04 12–17 (IE) | CRS01 18+ (vivienda) | ¿Misma pregunta? |
| --- | --- | --- | --- |
| Área | `AREA` de la IE | `AREA` de la vivienda | Mismo código 1/2. Distinto objeto. |
| Departamento | `DEPARTAMENTO` de la IE | `DEPARTAMENTO` del hogar | Mismo. Distinto objeto. |
| Edad | `EDAD` / `C3P103EDAD` | `C1P208_A` (padrón) | Sí: años cumplidos. |
| Sexo | `SEXO` | `C1P207` | Sí (en C1 la seleccionada es mujer). |
| Autoidentificación étnica | `C4P129` | `C1P306_E` | Sí. Mismas 9 categorías. |
| Lengua | `C3P128` idioma que hablan en su casa | `C1P306_F` lengua materna de ella | No. Hogar vs materna. |
| ¿Vivía en este distrito hace 5 años? | `C4P104B` + `C4P104C_*` | `C1P306_A` + `C1P306B_*` | Sí, casi calcado. |
| ¿Dónde vivía su madre cuando nació? | `C4P104D` + `C4P104E_*` | `C1P306C` + `C1P306D_*` | Sí, casi calcado. |
| Discapacidad (6 ítems) | `C4P130_1`…`_6` | `C1P209_A_1`…`_6` (padrón) | Sí. Mismo listado. |
| Tamaño del hogar | `C3P114_PERS` (ella cuenta) | Conteo del padrón `C1P204=1` | Mismo concepto, distinta fuente. |
| Con quién vive | `C3P115_*` (óptica de la niña) | `C1P203` parentesco al jefe | Mismo concepto, distinta óptica. |
| Quién hace las tareas | `C3P302_*` | `C1P316_*` | Parecido. Códigos distintos. |
| Quién mantiene económicamente | `C3P302_4` | `C1P316_7` | Mismo concepto. |
| Educación | `C3ANIO` año actual (todas en secundaria) | `C1P210` último nivel aprobado | No comparable 1 a 1. |
| Trabajo | `C3P120A` si el cuidador trabaja | `C1P307` si ella trabajó | No. Distinto sujeto. |

Para comparar prevalencias entre edades, usa solo esa lista. Recode etnia y discapacidad 1:1. Área y departamento: en CRS04 es la IE; en CRS01 es el hogar. Lengua **no** se compare sin recode: en la niña es “qué hablan en casa”, en la adulta es “qué aprendió de niña”.

Tamaño de hogar de referencia: CRS01 media 3.60 miembros (padrón); CRS04 media 5.16 (ella cuenta, incluye a ella).

---

## Solo un grupo

| Solo CRS04 (12–17) | Variable |
| --- | --- |
| Quién la cuida / se queda sola | `C3P120`, `C3P120B` |
| Sin comer, faltar al colegio para ayudar, peleas en casa | `C3P121`, `C3P122`, `C3P123` |
| Comparte cuarto / cama | `C3P118_*`, `C3P119_*` |
| Violencia psic/fís en casa y colegio + sexual CAP248 | `C3P201+`, `C4P248` |
| Contexto de la IE (turno, mixto, UGEL) | `TURNO`, `INED`, `UNGEEDLO` |

| Solo CRS01 (18+) | Variable |
| --- | --- |
| Vivienda, servicios, 21 activos | `C1P101`–`C1P110_*` |
| Estado civil, hijas/os, embarazo | `C1P302`, `C1P304`, `C1P306` |
| Trabajo, ocupación, quién gasta su ingreso | `C1P307`–`C1P313` |
| Seguro, programas sociales (JUNTOS, Pensión 65…) | `C1P314`, `C1P315` |
| Violencia de pareja, control, otras personas desde los 18 | `C1P402`, `C1P411`, CAP400 |
| Recuerdo de infancia hasta los 11 (no es el módulo CRS04) | `CAP441A_1`…`_6` |

---

## Descriptivos CRS01 (mujeres 18+)

Peso `FACTOR_MUJ`. Missing de edad = 0.

### Territorio

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Urbano | 9,669 | 69.9% | 10,884,369 | 87.8% |
| Rural | 4,157 | 30.1% | 1,517,296 | 12.2% |

Top departamentos:

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| LIMA | 1,424 | 10.3% | 4,594,705 | 37.0% |
| LA LIBERTAD | 620 | 4.5% | 762,453 | 6.1% |
| PIURA | 638 | 4.6% | 752,310 | 6.1% |
| AREQUIPA | 657 | 4.8% | 609,306 | 4.9% |
| LAMBAYEQUE | 550 | 4.0% | 500,741 | 4.0% |
| CAJAMARCA | 612 | 4.4% | 482,479 | 3.9% |
| CUSCO | 555 | 4.0% | 472,587 | 3.8% |
| JUNIN | 618 | 4.5% | 471,510 | 3.8% |

Hace 5 años, ¿vivía en este distrito?

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Hace 5 años vivía en este distrito | 12,761 | 92.3% | 11,333,531 | 91.4% |
| No | 1,065 | 7.7% | 1,068,134 | 8.6% |

### Edad, estado civil, hijas/os

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| 18-24 | 1,210 | 8.8% | 1,900,333 | 15.3% |
| 25-34 | 2,570 | 18.6% | 2,570,376 | 20.7% |
| 35-44 | 2,983 | 21.6% | 2,534,807 | 20.4% |
| 45-59 | 3,718 | 26.9% | 2,874,273 | 23.2% |
| 60+ | 3,345 | 24.2% | 2,521,876 | 20.3% |

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Conviviente | 4,454 | 32.2% | 3,417,562 | 27.6% |
| Casada | 3,998 | 28.9% | 2,980,866 | 24.0% |
| Viuda | 1,251 | 9.0% | 924,256 | 7.5% |
| Divorciada | 158 | 1.1% | 173,542 | 1.4% |
| Separada / exconviviente | 2,244 | 16.2% | 2,002,293 | 16.1% |
| Soltera | 1,721 | 12.4% | 2,903,145 | 23.4% |

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Alguna vez tuvo hija/o | 12,042 | 87.1% | 9,445,924 | 76.2% |
| No | 1,784 | 12.9% | 2,955,741 | 23.8% |

### Educación y trabajo

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Sin nivel | 1,286 | 9.3% | 578,555 | 4.7% |
| Inicial | 25 | 0.2% | 13,117 | 0.1% |
| Primaria incompleta | 2,087 | 15.1% | 1,089,486 | 8.8% |
| Primaria completa | 1,656 | 12.0% | 1,157,930 | 9.3% |
| Secundaria incompleta | 1,428 | 10.3% | 1,067,050 | 8.6% |
| Secundaria completa | 3,587 | 25.9% | 3,600,496 | 29.0% |
| Básica especial | 4 | 0.0% | 9,078 | 0.1% |
| Sup. no univ. incompleta | 443 | 3.2% | 535,777 | 4.3% |
| Sup. no univ. completa | 1,256 | 9.1% | 1,473,247 | 11.9% |
| Univ. incompleta | 531 | 3.8% | 912,191 | 7.4% |
| Univ. completa | 1,421 | 10.3% | 1,847,263 | 14.9% |
| Maestría/doctorado | 102 | 0.7% | 117,474 | 0.9% |

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Sí trabajó (semana pasada) | 8,023 | 58.0% | 7,316,912 | 59.0% |
| No | 5,803 | 42.0% | 5,084,753 | 41.0% |

Quién mantiene económicamente (`C1P316_7`):

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Esposo/pareja | 3,991 | 28.9% | 3,001,556 | 24.2% |
| Otra persona | 2,018 | 14.6% | 2,780,214 | 22.4% |
| Todos en el hogar | 1,318 | 9.5% | 2,085,403 | 16.8% |
| Ella | 2,496 | 18.1% | 2,079,579 | 16.8% |
| Ella y pareja | 2,936 | 21.2% | 1,888,629 | 15.2% |
| missing | 1,067 | 7.7% | 566,284 | 4.6% |

### Etnia y lengua materna

`C1P306_E` (mismas categorías que `C4P129`):

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Mestiza | 6,865 | 49.7% | 7,405,443 | 59.7% |
| Quechua | 3,866 | 28.0% | 2,246,100 | 18.1% |
| Afroperuana | 905 | 6.5% | 839,040 | 6.8% |
| Blanca | 720 | 5.2% | 809,104 | 6.5% |
| No sabe | 465 | 3.4% | 464,251 | 3.7% |
| Aimara | 569 | 4.1% | 308,051 | 2.5% |
| Otro | 187 | 1.4% | 246,458 | 2.0% |
| Nativo Amazonía | 245 | 1.8% | 81,817 | 0.7% |
| Otro pueblo indígena | 4 | 0.0% | 1,400 | 0.0% |

`C1P306_F` (no es el idioma del hogar de CRS04):

| Nivel | n | % n | N exp. | % N |
| --- | ---: | ---: | ---: | ---: |
| Castellano | 10,072 | 72.8% | 10,421,069 | 84.0% |
| Quechua | 3,107 | 22.5% | 1,696,140 | 13.7% |
| Aimara | 428 | 3.1% | 210,901 | 1.7% |
| Otra nativa | 198 | 1.4% | 61,712 | 0.5% |
| Extranjera | 21 | 0.2% | 11,844 | 0.1% |

### Discapacidad

Algún `C1P209_A_*` = 1: n = 249 (1.8% de casos) · N = 180,092 (1.5%). En CRS04 el mismo listado da 12.4% de N: otro universo y otro flujo (en C1 hay un filtro de “dependencia”).

### Vivienda (solo C1)

Agua, luz, desagüe y activos: [descriptivos_controles.md](descriptivos_controles.md#crs01--servicios-y-activos-no-se-pegan-a-crs04). No se le preguntan a la de 12–17.

---

## Qué implica para el modelo

No armes un solo LASSO mezclando filas de C1 y CRS04: factores, grano y targets son distintos.

Si quieres **comparar perfiles** (adolescente vs adulta): usa el bloque común (etnia, migración, discapacidad, composición/tamaño, quién mantiene, área) con recodes alineados, y deja vivienda solo en C1 y cuidado/colegio solo en CRS04.

Si el modelo es **solo CRS04**, C1 aporta controles territoriales (depto × área), no variables individuales de la niña.
