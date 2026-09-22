# Apartado metodológico

> **Qué es este informe.** Las **decisiones**: universo, qué es la Y, qué entra a X, qué se tira por leakage y la lista cerrada de recodes. Es la especificación que siguen `procesar_crs04.py` y el LASSO.
> **Qué no es.** No son los números del diseño (estratos flacos: [diseno_muestral.md](diseno_muestral.md)). No son las distribuciones ([../descriptivos/descriptivos_predictores_crs04.md](../descriptivos/descriptivos_predictores_crs04.md)). No es el resultado del modelo ([../resultados/lasso_crs04.md](../resultados/lasso_crs04.md)).
> **Tipo.** Metodológico.
> **Lo escribe.** Texto a mano (no sale de un script).

ENARES 2024 (INEI). Este documento fija, de una vez, el universo, el diseño muestral de las dos encuestas que se utilizan y la **especificación de la matriz de predictores** del modelo de alumnas. Está escrito para un lector que no ha revisado los descriptivos: cada decisión de recode, dummy o exclusión queda justificada aquí.

El detalle numérico (distribuciones, cruces, gráficos) está en [../descriptivos/descriptivos_predictores_crs04.md](../descriptivos/descriptivos_predictores_crs04.md). El detalle del `svydesign` y de los estratos flacos está en [diseno_muestral.md](diseno_muestral.md). La construcción de los tres indicadores de violencia a 12 meses está en [../descriptivos/violencia_crs04_si_no_missing.md](../descriptivos/violencia_crs04_si_no_missing.md).

---

## 1. Universo y unidades

El análisis de riesgo y de perfiles se realiza sobre **adolescentes mujeres de 12 a 17 años** entrevistadas en institución educativa (cuestionario CRS.04).

| Pieza | Definición |
| --- | --- |
| Tabla | `analisis.crs04_adolescentes` |
| Recorte | `SEXO = 1` |
| n muestral | 9,608 alumnas |
| N expandida | 1,419,491 (`FACTOR_ALUMNOS`) |
| Llave de la fila | `ID` (institución educativa) + `COLEGIAL_ID` (alumna dentro de la IE) |

La encuesta de **mujeres de 18 y más años en vivienda** (CRS.01, `analisis.crs01_mujeres`, n = 13,826, N = 12,401,665 con `FACTOR_MUJ`) **no se une** a la alumna a nivel persona. `ID` no es llave común. CRS.01 se usa solo para (i) descriptivos de vivienda y (ii) promedios territoriales `DEPARTAMENTO × AREA` que, de pegarse, se pegan al **lugar de la IE**, no a la casa de la adolescente.

En CRS.04, `AREA` y `DEPARTAMENTO` son de la institución educativa. El 12,7 % de la N no vive en el distrito de la IE.

---

## 2. Diseño muestral

Las alumnas del mismo colegio no son independientes. CRS.04 **no trae** la columna `CONGLOME`; el conglomerado se lee de la llave.

| Pieza | CRS.04 (alumnas 12–17) | CRS.01 (mujeres 18+) |
| --- | --- | --- |
| Marco | Institución educativa | Vivienda / hogar |
| Unidad de análisis | Alumna | Mujer seleccionada (una por hogar) |
| **Conglomerado (PSU)** | `ID` = colegio (1,086 IE; mediana 10 alumnas) | `CONGLOME` (1,750 conglomerados; mediana 8 mujeres) |
| SSU opcional | `C3SECC` (sección; mediana 2 por IE) | No aplica |
| **Estrato** | `AREA × DEPARTAMENTO` de la IE (49 celdas; Callao sin rural) | `AREA × DEPARTAMENTO` del hogar (49 celdas) |
| Peso | `FACTOR_ALUMNOS` | `FACTOR_MUJ` (mujer) · `FACTOR_VIV` (vivienda) |
| Estratos con 1 PSU | 0 | 0 |
| Estrato más flaco | Tacna rural: 2 IE, 10 alumnas | Tumbes rural: 2 conglomerados, 24 mujeres |

Para el LASSO y los totales ponderados basta un diseño de dos etapas con la IE como PSU. Un modelo de tres niveles (alumna → sección → colegio) es defendible, pero no es necesario para `survey::svydesign`.

```r
library(survey)

diseno_crs04 <- svydesign(
  ids     = ~ID,
  strata  = ~interaction(AREA, DEPARTAMENTO),
  weights = ~FACTOR_ALUMNOS,
  data    = alumnas,   # SEXO == 1
  nest    = TRUE
)

diseno_crs01_mujer <- svydesign(
  ids     = ~CONGLOME,
  strata  = ~interaction(AREA, DEPARTAMENTO),
  weights = ~FACTOR_MUJ,
  data    = mujeres18,
  nest    = TRUE
)
```

`DEPARTAMENTO` entra como **estrato del diseño** y como llave del tablero territorial. No entra como 25 dummies en la matriz X del LASSO.

---

## 3. Variable dependiente

Tres indicadores binarios de victimización en los **últimos 12 meses**, construidos sobre las baterías de CAP200 y CAP248. El NULL del filtro temporal es skip del cuestionario y se trata como 0. Missing real de los ítems madre = 0.

| Indicador | Contenido | % N sí |
| --- | --- | ---: |
| `viol_psicologica_12m` | Casa (`C3P201_*` + `C3P203`) o colegio (`C3P223_*` + `C3P225`) | 59,7 % |
| `viol_fisica_12m` | Casa (`C3P205_*` + `C3P207`) o colegio (`C3P227_*` + `C3P229`) | 25,9 % |
| `viol_sexual_12m` | `C4P248_i = 1` y `C4P248C_i = 1` (i = 1…16) | 23,0 % |

Esos 58 ítems madre **son el target**. No reingresan como predictores.

---

## 4. Especificación de predictores

Los predictores se organizan según un esquema ecológico (individual, relacional, comunitario/escolar). Las cifras de missing, prevalencia y referencia son **ponderadas con `FACTOR_ALUMNOS`**, salvo cuando se indica n muestral.

**Convención de códigos.** En ítems sí/no: 1 = sí, 2 = no. En multi-respuesta (`C3P115`, `C3P118`, `C4P130`): 1 = marcado, 0 o NULL = no. En `C3P301`: 1 = de acuerdo, 2 = no, 3 = no sabe. Los 18 casos CAR (`C3P105 = 2`) se saltan el flujo de casa: el 0,2 % missing de `C3P114`/`C3P115`/`C3P120` no es no-respuesta.

Esta tabla es la especificación para escribir el script de la matriz X. No hace falta volver a los descriptivos para recodes, referencias ni exclusiones.

### 4.1 Nivel individual

| Variable(s) | Pregunta (resumen) | Tipo | N categorías | Missing / skip | Tratamiento final | Referencia (dummy) | Prioridad | Justificación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EDAD` / `C3P103EDAD` | Edad en años | Continua | 6 valores (12–17) | 0 % | Numérica lineal | — | Alta | Física cae de forma monótona (34,5 % → 16,9 % entre 12 y 16 años). El término cuadrático no aporta forma de U. Sexual es plana (~21–24 %). |
| `C4P129` | Autoidentificación étnica | Categórica nominal | 9 → recodificar a 5–6 | 0 % | Dummies tras colapsar la cola | Mestiza (43,4 % N) | Media | Aimara, Amazonía, otro pueblo y otro quedan cada uno por debajo de 3 % N. Colapsar en `otra_indigena_otro` antes de dummy. “No sabe” (14,2 % N) se conserva como categoría. |
| `C3P128` | Idioma hablado en el hogar | Categórica nominal | 6 → recodificar a 3 | 0,2 % (≈ CAR) | Dummies tras colapsar la cola | Castellano (94,3 % N) | Media | No es lengua materna (eso es `C1P306_F` en CRS.01). Extranjero + otra nativa + NS < 2 % cada uno: colapsar en `otro_idioma`. Quechua se mantiene. |
| `C4P130_1`–`_6` | Discapacidad permanente (6 tipos) | 6 binarias | — | 0 % | Colapsar a 1 dummy `alguna_discapacidad` (OR) | — | Media | Cada tipo queda por debajo de 7 % N (moverse 0,6 %; ver 2,3 %; entender 7,0 %). Seis dummies gastan grados de libertad sin ganancia. |
| `C3P126` | ¿Toman en cuenta tu opinión? | Binaria | 2 | 0,2 % (CAR) | 0/1 directo | — | Alta | Indicador de voz / agencia en el hogar. |
| `C3P127` | Frecuencia de lo anterior | Ordinal (skip si 126 = no) | 3 + NS | 12,0 % skip lógico | Opcional; ordinal 1–3, NULL = no aplica | — | Baja | Se pisa con `C3P126`. Incluir solo si se quiere intensidad, no las dos a la vez sin recode del skip. |
| `C3P301_1` | De acuerdo: debe trabajar si falta plata | Binaria (de acuerdo / no / NS) | — | ~1,5 % NS | 0/1 (de acuerdo = 1) | — | Media | 22,7 % N de acuerdo: varianza suficiente. |
| `C3P301_2` | De acuerdo: puede hablar lo que piensa | Binaria | — | ~0,4 % NS | 0/1 | — | Baja | 95,4 % N de acuerdo: poca varianza; candidata a caer sola en el LASSO. |
| `C3P301_3` | De acuerdo: los padres pueden decidir que deje el colegio | Binaria | — | ~1,3 % NS | 0/1 | — | Media | 13,4 % N de acuerdo: varianza aceptable. |
| `C3P301_4` | De acuerdo: los profesores tienen derecho a golpear | Binaria | — | ~0,6 % NS | Excluir o dejar con cautela | — | Muy baja | 2,8 % N de acuerdo: varianza insuficiente. |
| `C3P301_5` | De acuerdo: los padres tienen derecho a golpear | Binaria | — | ~2,6 % NS | 0/1 | — | Media | 33,8 % N de acuerdo: buena varianza. |
| `C3P301_6` | De acuerdo: puede denunciar a quien la maltrata | Binaria | — | ~1,2 % NS | 0/1 (invertir si se construye un índice) | — | Baja | 93,8 % N de acuerdo: poca varianza. Ítems 2 y 6 son “pro derechos”; 1, 3, 4 y 5 son punitivos. **No se suman en crudo.** |

### 4.2 Nivel relacional

| Variable(s) | Pregunta (resumen) | Tipo | N categorías | Missing / skip | Tratamiento final | Referencia (dummy) | Prioridad | Justificación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `C3P106` | ¿Tiene mamá? | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Media | Usar este bloque **o** `C3P115_1`, no ambos. |
| `C3P110` | ¿Tiene papá? | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Media | Usar este bloque **o** `C3P115_2`, no ambos. |
| `C3P114_PERS` | Tamaño del hogar (incluyéndola) | Continua | 0–20 | 0,2 % (CAR) | Numérica lineal, estandarizada si se comparan betas | — | Media | Media ponderada 5,16; DE 1,97. El cruce con los tres targets es plano. El cuadrático es opcional, no prioritario. |
| `C3P115_3`–`_14` | Con quién vive (madrastra, padrastro, hermanos, abuelos, tíos, primos, otros) | Multi-binaria (12 ítems) | — | 0,2 % (CAR) | 0/1 cada una, **sin** dummy de referencia | — | Alta (padrastro / madrastra en especial) | No son mutuamente excluyentes: cada ítem es su propia variable. `C3P115_1` y `_2` se omiten si ya entran `C3P106` / `C3P110`. |
| `C3P115_15`, `_16`, `_17` | Hijastros / trabajadora del hogar | Multi-binaria | — | 0,2 % | Excluir o agrupar en “otros” | — | Muy baja | Cada una < 0,5 % N. |
| `C3P118_12` | Duerme sola en el cuarto | Binaria (derivada) | 2 | 0,2 % (CAR) | 0/1 | — | Media | 50,8 % N. Resume hacinamiento sin las 30 columnas de `C3P118`+`C3P119`. El 50,8 % “missing” de `C3P119` es skip: si `C3P118_12 = 1` no preguntan la cama. |
| `C3P120` recodificada | Quién la cuida la mayor parte del tiempo | Categórica nominal | 17 → recodificar a 5 | 0,2 % (CAR) | Dummies tras recode | Madre (70,1 % N) | Alta | Recode: madre / padre / abuelos / hermanos / otros. La cola (tía, tío, prima, trabajadora, hijastros) va a “otros”. No 16 dummies sueltas. |
| `C3P120B` | Se queda sola sin adulto | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Alta | 58,6 % N. Volumen y plausibilidad teórica altos. |
| `C3P121` | La dejaron sin comer (negligencia) | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Alta | Prevalencia baja (1,4 % N) y, aun así, de las más fuertes en el cruce con los targets. |
| `C3P122` | Falta al colegio para ayudar en casa | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Alta | Señal de sobrecarga / explotación doméstica (6,8 % N). |
| `C3P123` | Hay peleas o discusiones en casa | Binaria | 2 | 0,2 % (CAR) | 0/1 | — | Alta | 49,1 % N. Una de las variables más fuertes del bloque relacional. |
| `C3P124` | Frecuencia de esas peleas | Ordinal (skip si 123 = no) | 3 + NS | 50,9 % skip lógico | Opcional; ordinal 1–3 | — | Baja | Redundante con `C3P123` si solo se quiere el binario. |

### 4.3 Nivel comunitario / escolar

`AREA`, `INED`, `TURNO` y `DEPARTAMENTO` describen la **institución educativa**, no el hogar.

| Variable(s) | Pregunta (resumen) | Tipo | N categorías | Missing / skip | Tratamiento final | Referencia (dummy) | Prioridad | Justificación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AREA` | Área urbano / rural de la IE | Binaria | 2 | 0 % | 0/1 (rural = 1) | — | Alta | Base del estrato del diseño y predictor sustantivo (20,2 % N rural). |
| `INED` | Tipo de IE (mujeres / mixto) | Binaria en este recorte | 2 (no hay “solo hombres”) | 0 % | 0/1 (mujeres = 1) | Mixto | Baja | 90,0 % N en IE mixta. No se crean tres niveles. |
| `TURNO` | Turno de estudio | Binaria en este recorte | 2 (no hay “noche”) | 0 % | 0/1 (tarde = 1) | Mañana | Baja | 81,0 % N en la mañana. No hay alumnas en turno noche. |
| `C3P217` | Cómo se siente en el colegio | Ordinal | 4 + NS | ~0,1 % NS | Ordinal 1–4, o dummy mal / muy mal frente al resto | — | Media | “Muy mal” es 1,5 % N. Cuidado si se usan cuatro dummies. NS (n = 11) se descarta. |
| `C3P218` | Jaló o desaprobó un curso (2023) | Binaria | 2 | 0 % | 0/1 | — | Media | 26,6 % N: varianza razonable. |
| `C3P219` | Repitió de grado | Binaria | 2 | 0 % | 0/1 | — | Baja | 5,8 % N: varianza baja, no crítica. |
| `C3P220` | La expulsaron alguna vez | Binaria | 2 | 0 % | 0/1 (probable que el LASSO la lleve a 0) | — | Muy baja | 1,1 % N: varianza casi nula. |
| `C3P221` | Mejores amigos en el mismo colegio | Binaria | 2 | 0 % | 0/1 | — | Media | 74,8 % N. Proxy de integración social. |
| `C3P222` | Lugares del colegio a los que no va por miedo | Binaria | 2 | 0 % | **Excluir del LASSO.** Solo post-cluster | — | — | Circular: es casi un síntoma de violencia o acoso escolar. |
| `DEPARTAMENTO` | Departamento de la IE | Categórica | 25 | 0 % | **No entra a X.** Estrato del diseño + llave del dashboard | — | — | Veinticinco dummies sobreajustan y no se interpretan. El control territorial, si se quiere, es el promedio CRS.01 por `DEPARTAMENTO × AREA` (electricidad, agua, activos), no el nombre del departamento. |

---

## 5. Variables excluidas por circularidad (leakage)

No entran a X bajo ninguna forma: recode, índice o interacción. Si se incluyen, el modelo recupera el target con información **posterior** al evento (o con el evento mismo).

| Bloque | Rango de variables | Por qué se excluye |
| --- | --- | --- |
| Búsqueda de ayuda en casa | `C3P209`–`C3P215` | Solo se pregunta si ya hubo violencia en el hogar. Es consecuencia, no factor previo. Skip: 28,3 % en `C3P209`. |
| Autolesión, fuga, consumo | `C3P216A_1`–`_6` (+ sufijo `C` de 12 meses) | Comorbilidad o consecuencia. Se pregunta a todas (0 % skip), pero no es un factor de riesgo precedente. |
| Búsqueda de ayuda en el colegio y lesiones | `C3P236`–`C3P247` | Posteriores a la violencia escolar. Skip: 34,2 % en `C3P236`. |
| Quién agredió y edad de inicio (sexual) | `C4P248A_*_*`, `C4P248B_*` | Solo existen si `C4P248_i = 1`. Sirven para **caracterizar** los clusters después de estimar, no para predecir `viol_sexual_12m`. |
| Búsqueda de ayuda (violencia sexual) | `C4P251`–`C4P260` | El mismo patrón que la ayuda en casa y en el colegio. |
| Los 58 ítems madre de violencia | `C3P201_*`, `C3P205_*`, `C3P223_*`, `C3P227_*`, `C4P248_*` | **Son el target**, no predictores. |

---

## 6. Recodes que el script debe aplicar (lista cerrada)

Antes de dummyficar, y en este orden:

1. `etnia`: `C4P129` → mestiza / quechua / afroperuana / blanca / no_sabe / `otra_indigena_otro` (2, 3, 4, 8).
2. `idioma`: `C3P128` → castellano / quechua / `otro_idioma` (3, 4, 5, 6). Missing CAR → NA.
3. `alguna_discapacidad` = 1 si algún `C4P130_1`…`_6` = 1.
4. `cuidador`: `C3P120` → madre (1) / padre (2) / abuelos (7, 8) / hermanos (5, 6) / otros (resto).
5. `duerme_sola_cuarto` = (`C3P118_12` = 1).
6. `C3P115_15`–`_17` no entran; `_1` y `_2` no entran si ya están `C3P106` y `C3P110`.
7. `INED_mujeres` = (`INED` = 1); `turno_tarde` = (`TURNO` = 2); `rural` = (`AREA` = 2).
8. `C3P301_k` = 1 si de acuerdo, 0 si no; NS → NA (o 0, documentado). No sumar 1–6 sin invertir 2 y 6.
9. `C3P222`, `DEPARTAMENTO` como predictor, y todos los bloques de la sección 5: **fuera de X**.
10. CAR (18 filas): NA en el flujo de casa; no imputar como “no”.

Con esta especificación se puede construir la matriz de predictores desde `analisis.crs04_adolescentes` sin volver a abrir los descriptivos.

```bash
python scripts/tablas/build_db.py
python scripts/tablas/procesar_crs04.py              # → data/tablas/crs04_modelo.parquet
python scripts/tablas/armar_filtro_violencia.py      # → data/tablas/crs04_filtro_violencia.parquet
python scripts/modelos/lasso_crs04.py
python scripts/modelos/perfiles_kmeans_crs04.py      # lee la tabla de filtro; no la arma
python scripts/modelos/perfiles_cart_crs04.py
```
