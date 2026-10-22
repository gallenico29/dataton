# Metodología

ENARES 2024. Alumnas de 12 a 17 años, cuestionario CRS.04, mujeres. Diseño: [diseno_muestral.md](diseno_muestral.md). Construcción de los tres indicadores: [violencia_crs04_si_no_missing.md](../descriptivos/violencia_crs04_si_no_missing.md). Coeficientes: [lasso_crs04.md](../resultados/lasso_crs04.md).

## Universo

La matriz es `analisis.crs04_adolescentes`, `SEXO = 1`: 9.608 alumnas, N = 1.419.491 con `FACTOR_ALUMNOS`. La fila es `ID` (la escuela) + `COLEGIAL_ID`.

CRS.01 queda aparte. Son mujeres de 18 años o más en vivienda (n = 13.826, N = 12.401.665 con `FACTOR_MUJ`). `ID` no identifica a la misma persona y el peso es otro. En el tablero, luz, agua, desagüe e internet son el promedio del departamento de la escuela.

`AREA` y `DEPARTAMENTO` en CRS.04 son de la escuela. El 12,7 % de la N no vive en el distrito de esa escuela.

## Diseño

Las alumnas de una misma escuela no son independientes. CRS.04 no tiene columna `CONGLOME`; el conglomerado es `ID` (1.086 escuelas, mediana de 10 alumnas). El estrato es `AREA` × `DEPARTAMENTO` de la escuela: 49 celdas, Callao sin rural. El peso es `FACTOR_ALUMNOS`.

Ese peso entra al LASSO, reescalado a media 1. La validación cruzada no incorpora el conglomerado. El departamento no entra a X: es estrato del diseño y llave del tablero.

## Indicadores

Tres variables de los últimos 12 meses. El vacío del filtro de 12 meses es skip: no le preguntaron porque no hubo un sí de por vida, y se codifica como no en el año. Los 58 ítems madre están completos y no vuelven a entrar como predictores.

| Indicador | Regla | % de la N |
| --- | --- | ---: |
| `viol_psicologica_12m` | Casa (`C3P201_*` y `C3P203`) o colegio (`C3P223_*` y `C3P225`) | 59,7 % |
| `viol_fisica_12m` | Casa (`C3P205_*` y `C3P207`) o colegio (`C3P227_*` y `C3P229`) | 25,9 % |
| `viol_sexual_12m` | `C4P248_i = 1` y `C4P248C_i = 1` (i = 1…16) | 23,0 % |

## Ajuste

Un logístico L1 por indicador (`LogisticRegressionCV`, 5 folds, AUC). n = 9.575. Las 18 filas de centro de acogida residencial quedan fuera: el cuestionario se salta el bloque de casa y ese vacío no se imputa como no.

Edad y tamaño del hogar van estandarizados. Etnia se contrasta con mestiza, idioma con castellano y cuidador con la madre.

Fuera de X: búsqueda de ayuda, quién agredió, autolesión y fuga; `C3P222`; expulsión; frecuencia de las peleas (`C3P124`); `C3P127`; actitudes `C3P301_2`, `_4` y `_6`; nombre del departamento. El listado de lo que sí entró está en [descriptivos_predictores_crs04.md](../descriptivos/descriptivos_predictores_crs04.md).

Trece variables quedan distintas de cero en los tres indicadores: `edad`, `toma_en_cuenta`, `act_trabajar`, `act_deje_colegio`, `act_padres_golpear`, `vive_hermana`, `vive_tio`, `se_queda_sola`, `falta_colegio`, `peleas_casa`, `ie_mujeres`, `se_siente_mal`, `jalo_curso`. Con esas trece se arman los grupos: primero se parte la muestra en sí y no, y dentro de cada lado se piden tres grupos. La violencia no entra a ese agrupamiento.

El árbol usa las 36 variables que el L1 dejó vivas en al menos un indicador. Ahí la violencia sí entra: es lo que el árbol separa. Profundidad 3, peso `FACTOR_ALUMNOS`. Hay tres árboles porque el indicador de “alguna violencia” queda dominado por la psicológica (59,7 %).

## Odds ratios

El OR es exp(coeficiente). Dice por cuánto se multiplican las chances de reportar esa violencia cuando la condición está presente, frente a cuando no lo está, con las demás variables del modelo constantes. Mayor a 1: más chance de reportarla. Menor a 1: menos chance. No es una diferencia en puntos porcentuales.

Peleas en casa: 2,5 en violencia psicológica, 2,5 en física y 1,7 en sexual. Sentirse mal o muy mal en el colegio: 4,3 en psicológica, la asociación más fuerte; 2,0 en física y 1,5 en sexual. Quedarse sola sin un adulto: 1,5, 1,8 y 1,3. Faltar al colegio para ayudar en casa: 1,8 en psicológica y en física, y 1,3 en sexual. Que tomen en cuenta su opinión es el principal factor protector: las chances de violencia psicológica quedan en 39 % de las de una alumna a la que no escuchan, las de física en 44 % y las de sexual en 70 %.
