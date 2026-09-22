# LASSO CRS04 (alumnas)

> **Qué es este informe.** Qué variables quedaron vivas y con qué coeficiente (logit, OR, lectura) en cada violencia a 12 meses. Es el primer resultado del modelo: la selección de X.
> **Qué no es.** No es un descriptivo. No arma tipos de alumna (k-medias) ni reglas (CART). Esas X se usan después.
> **Tipo.** Resultado del modelo.
> **Lo escribe.** `scripts/modelos/lasso_crs04.py` (Python → markdown; no es Rmd).

Logístico L1 (`sklearn.linear_model.LogisticRegressionCV`, `penalty='l1'`, 5-fold, `roc_auc`).
Peso `FACTOR_ALUMNOS` (reescalado a media 1). `edad` y `pers` estandarizadas.
Referencias de dummy: etnia = mestiza, idioma = castellano, cuidador = madre.

Universo: `data/tablas/crs04_modelo.parquet`, se excluyen 18 CAR (no se imputa el flujo de casa).
Especificación: [../metodologia/metodologia.md](../metodologia/metodologia.md).

No es group lasso ni `survey::svyglm`. Es selección de variables para armar perfiles.

## Qué no entra a X (ni se creó)

**Servicios y activos de vivienda (CRS01).** No se creó ninguna variable nueva de agua, luz, desagüe ni `C1P110`. Esas columnas viven en otra muestra; `ID` no une a la alumna. Tampoco se pegó el promedio `DEPARTAMENTO × AREA` de CRS01. Si más adelante se quiere un rasgo del **lugar**, eso sería un paso aparte (medias territoriales), no “tiene refrigeradora” en la fila.

Tampoco entran: `DEPARTAMENTO` (25 dummies), `C3P222` (circular suave), `C3P301_2/_4/_6` y `expulsion` (varianza nula o casi), `C3P127`/`C3P124` (skip, prioridad baja), ni los bloques de leakage (`C3P209`–`215`, `216A`, `236`–`247`, `C4P248A/B`, ítems madre).

## Cómo leer el coeficiente

Es un logístico: el número es el cambio en **log-odds** de reportar esa violencia a 12 meses, condicional al resto de X que el L1 dejó vivas.

- **OR** = exp(coef). Multiplicador de odds. OR > 1 = más odds; OR < 1 = menos odds; OR = 1 y coef = 0 = no queda.
- Dummy 0/1: el salto es de 0 a 1. Etnia vs mestiza, idioma vs castellano, cuidador vs madre.
- `edad` y `pers` van **estandarizadas**: el coef es por 1 desviación estándar, no por un año ni por una persona.
- El L1 encoge hacia 0. Un 0 no es “no existe asociación cruda”; es “no aporta lo suficiente dado las demás”. No es causal.

## Qué queda y qué cae a cero

Las 44 que **sí** entraron al LASSO. Célula = coeficiente logit (4 decimales). `0` = el L1 la apagó. “En los 3” cuenta cuántos targets la dejan viva.

| Variable | Qué es | Psic. (logit) | Fís. (logit) | Sexual (logit) | En los 3 |
| --- | --- | ---: | ---: | ---: | --- |
| `edad` | Edad (lineal) | -0.0976 | -0.3256 | 0.0338 | 3/3 |
| `pers` | Tamaño del hogar | 0 | -0.0318 | -0.0427 | 2/3 |
| `alguna_discapacidad` | Alguna discapacidad | 0.2425 | 0.2711 | 0 | 2/3 |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.9326 | -0.8301 | -0.3570 | 3/3 |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.0038 | 0.0775 | 0.1384 | 3/3 |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.1695 | 0.0578 | 0.1171 | 3/3 |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.0863 | 0.5284 | 0.0721 | 3/3 |
| `tiene_mama` | Tiene mamá | 0 | 0 | 0 | 0/3 |
| `tiene_papa` | Tiene papá | 0 | 0 | 0 | 0/3 |
| `vive_madrastra` | Vive con madrastra | 0 | 0 | 0 | 0/3 |
| `vive_padrastro` | Vive con padrastro | 0 | 0.2068 | 0 | 1/3 |
| `vive_hermana` | Vive con hermana/s | -0.1001 | -0.1105 | -0.0184 | 3/3 |
| `vive_hermano` | Vive con hermano/s | -0.0717 | -0.0480 | 0 | 2/3 |
| `vive_abuela` | Vive con abuela | -0.0271 | 0 | 0.0711 | 2/3 |
| `vive_abuelo` | Vive con abuelo | 0 | -0.0805 | 0 | 1/3 |
| `vive_tia` | Vive con tía | 0.0247 | 0 | 0 | 1/3 |
| `vive_tio` | Vive con tío | 0.0566 | 0.3219 | 0.0220 | 3/3 |
| `vive_prima` | Vive con prima | 0.0345 | 0 | 0 | 1/3 |
| `vive_primo` | Vive con primo | 0 | 0 | 0 | 0/3 |
| `vive_otros_parientes` | Vive con otros parientes | 0 | -0.1780 | 0 | 1/3 |
| `vive_otra_persona` | Vive con otra persona | 0 | -0.1348 | 0.0508 | 2/3 |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | -0.0532 | -0.1486 | 0 | 2/3 |
| `se_queda_sola` | Se queda sola sin adulto | 0.4235 | 0.5637 | 0.2775 | 3/3 |
| `sin_comer` | La dejaron sin comer | 0 | 0.2518 | 0.1177 | 2/3 |
| `falta_colegio` | Falta al colegio para ayudar | 0.6042 | 0.6026 | 0.2697 | 3/3 |
| `peleas_casa` | Peleas en casa | 0.9328 | 0.9172 | 0.5209 | 3/3 |
| `rural` | IE rural | -0.1493 | 0 | -0.1792 | 2/3 |
| `ie_mujeres` | IE de mujeres | -0.1553 | -0.0015 | -0.1819 | 3/3 |
| `turno_tarde` | Turno tarde | 0 | -0.0029 | 0 | 1/3 |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 1.4609 | 0.7134 | 0.4127 | 3/3 |
| `jalo_curso` | Jaló un curso (2023) | 0.0593 | 0.2612 | 0.1273 | 3/3 |
| `repitio` | Repitió de grado | -0.0385 | 0.0387 | 0 | 2/3 |
| `amigos_colegio` | Mejores amigos en este colegio | -0.1389 | -0.0622 | 0 | 2/3 |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 0 | 0.0027 | -0.1457 | 2/3 |
| `etnia_afroperuana` | Etnia: afroperuana | 0.0416 | 0.1843 | 0 | 2/3 |
| `etnia_blanca` | Etnia: blanca | 0 | 0.1087 | 0 | 1/3 |
| `etnia_no_sabe` | Etnia: no sabe | 0 | -0.0940 | 0 | 1/3 |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 0 | 0 | 0/3 |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 0 | 0 | 0/3 |
| `idioma_otro` | Idioma: otro | 0 | 0 | 0 | 0/3 |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0 | 0 | 0.0963 | 1/3 |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 0 | 0 | 0/3 |
| `cuidador_hermanos` | Cuidador: hermanos | 0.1009 | 0.0413 | 0 | 2/3 |
| `cuidador_otros` | Cuidador: otros | 0 | 0.0275 | 0 | 1/3 |

---

## Coeficientes por target

### Violencia psicológica 12m

n completa = 9,575 · AUC-CV = 0.723 · variables distintas de cero = 24.

| Variable | Qué es | Coef. (logit) | OR | Lectura |
| --- | --- | ---: | ---: | --- |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 1.4609 | 4.310 | queda: más odds de esta violencia (si = 1 vs 0) |
| `peleas_casa` | Peleas en casa | 0.9328 | 2.542 | queda: más odds de esta violencia (si = 1 vs 0) |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.9326 | 0.394 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `falta_colegio` | Falta al colegio para ayudar | 0.6042 | 1.830 | queda: más odds de esta violencia (si = 1 vs 0) |
| `se_queda_sola` | Se queda sola sin adulto | 0.4235 | 1.527 | queda: más odds de esta violencia (si = 1 vs 0) |
| `alguna_discapacidad` | Alguna discapacidad | 0.2425 | 1.274 | queda: más odds de esta violencia (si = 1 vs 0) |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.1695 | 1.185 | queda: más odds de esta violencia (si = 1 vs 0) |
| `ie_mujeres` | IE de mujeres | -0.1553 | 0.856 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `rural` | IE rural | -0.1493 | 0.861 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `amigos_colegio` | Mejores amigos en este colegio | -0.1389 | 0.870 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `cuidador_hermanos` | Cuidador: hermanos | 0.1009 | 1.106 | queda: más odds de esta violencia (vs madre) |
| `vive_hermana` | Vive con hermana/s | -0.1001 | 0.905 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `edad` | Edad (lineal) | -0.0976 | 0.907 | queda: menos odds de esta violencia (por 1 DE) |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.0863 | 1.090 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_hermano` | Vive con hermano/s | -0.0717 | 0.931 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `jalo_curso` | Jaló un curso (2023) | 0.0593 | 1.061 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_tio` | Vive con tío | 0.0566 | 1.058 | queda: más odds de esta violencia (si = 1 vs 0) |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | -0.0532 | 0.948 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `etnia_afroperuana` | Etnia: afroperuana | 0.0416 | 1.042 | queda: más odds de esta violencia (vs mestiza) |
| `repitio` | Repitió de grado | -0.0385 | 0.962 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `vive_prima` | Vive con prima | 0.0345 | 1.035 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_abuela` | Vive con abuela | -0.0271 | 0.973 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `vive_tia` | Vive con tía | 0.0247 | 1.025 | queda: más odds de esta violencia (si = 1 vs 0) |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.0038 | 1.004 | queda: más odds de esta violencia (si = 1 vs 0) |
| `pers` | Tamaño del hogar | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_madrastra` | Vive con madrastra | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `tiene_papa` | Tiene papá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `tiene_mama` | Tiene mamá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_padrastro` | Vive con padrastro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_otra_persona` | Vive con otra persona | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_primo` | Vive con primo | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_otros_parientes` | Vive con otros parientes | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_abuelo` | Vive con abuelo | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `sin_comer` | La dejaron sin comer | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `turno_tarde` | Turno tarde | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_blanca` | Etnia: blanca | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_no_sabe` | Etnia: no sabe | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_otro` | Idioma: otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_otros` | Cuidador: otros | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |

Quedan **24**. No quedan **20** (el L1 las apagó).

### Violencia física 12m

n completa = 9,575 · AUC-CV = 0.750 · variables distintas de cero = 31.

| Variable | Qué es | Coef. (logit) | OR | Lectura |
| --- | --- | ---: | ---: | --- |
| `peleas_casa` | Peleas en casa | 0.9172 | 2.502 | queda: más odds de esta violencia (si = 1 vs 0) |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.8301 | 0.436 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 0.7134 | 2.041 | queda: más odds de esta violencia (si = 1 vs 0) |
| `falta_colegio` | Falta al colegio para ayudar | 0.6026 | 1.827 | queda: más odds de esta violencia (si = 1 vs 0) |
| `se_queda_sola` | Se queda sola sin adulto | 0.5637 | 1.757 | queda: más odds de esta violencia (si = 1 vs 0) |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.5284 | 1.696 | queda: más odds de esta violencia (si = 1 vs 0) |
| `edad` | Edad (lineal) | -0.3256 | 0.722 | queda: menos odds de esta violencia (por 1 DE) |
| `vive_tio` | Vive con tío | 0.3219 | 1.380 | queda: más odds de esta violencia (si = 1 vs 0) |
| `alguna_discapacidad` | Alguna discapacidad | 0.2711 | 1.311 | queda: más odds de esta violencia (si = 1 vs 0) |
| `jalo_curso` | Jaló un curso (2023) | 0.2612 | 1.298 | queda: más odds de esta violencia (si = 1 vs 0) |
| `sin_comer` | La dejaron sin comer | 0.2518 | 1.286 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_padrastro` | Vive con padrastro | 0.2068 | 1.230 | queda: más odds de esta violencia (si = 1 vs 0) |
| `etnia_afroperuana` | Etnia: afroperuana | 0.1843 | 1.202 | queda: más odds de esta violencia (vs mestiza) |
| `vive_otros_parientes` | Vive con otros parientes | -0.1780 | 0.837 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | -0.1486 | 0.862 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `vive_otra_persona` | Vive con otra persona | -0.1348 | 0.874 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `vive_hermana` | Vive con hermana/s | -0.1105 | 0.895 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `etnia_blanca` | Etnia: blanca | 0.1087 | 1.115 | queda: más odds de esta violencia (vs mestiza) |
| `etnia_no_sabe` | Etnia: no sabe | -0.0940 | 0.910 | queda: menos odds de esta violencia (vs mestiza) |
| `vive_abuelo` | Vive con abuelo | -0.0805 | 0.923 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.0775 | 1.081 | queda: más odds de esta violencia (si = 1 vs 0) |
| `amigos_colegio` | Mejores amigos en este colegio | -0.0622 | 0.940 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.0578 | 1.059 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_hermano` | Vive con hermano/s | -0.0480 | 0.953 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `cuidador_hermanos` | Cuidador: hermanos | 0.0413 | 1.042 | queda: más odds de esta violencia (vs madre) |
| `repitio` | Repitió de grado | 0.0387 | 1.039 | queda: más odds de esta violencia (si = 1 vs 0) |
| `pers` | Tamaño del hogar | -0.0318 | 0.969 | queda: menos odds de esta violencia (por 1 DE) |
| `cuidador_otros` | Cuidador: otros | 0.0275 | 1.028 | queda: más odds de esta violencia (vs madre) |
| `turno_tarde` | Turno tarde | -0.0029 | 0.997 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 0.0027 | 1.003 | queda: más odds de esta violencia (vs mestiza) |
| `ie_mujeres` | IE de mujeres | -0.0015 | 0.999 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `tiene_mama` | Tiene mamá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `tiene_papa` | Tiene papá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_madrastra` | Vive con madrastra | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_tia` | Vive con tía | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_primo` | Vive con primo | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `rural` | IE rural | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_abuela` | Vive con abuela | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_prima` | Vive con prima | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_otro` | Idioma: otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |

Quedan **31**. No quedan **13** (el L1 las apagó).

### Violencia sexual 12m

n completa = 9,575 · AUC-CV = 0.628 · variables distintas de cero = 20.

| Variable | Qué es | Coef. (logit) | OR | Lectura |
| --- | --- | ---: | ---: | --- |
| `peleas_casa` | Peleas en casa | 0.5209 | 1.684 | queda: más odds de esta violencia (si = 1 vs 0) |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 0.4127 | 1.511 | queda: más odds de esta violencia (si = 1 vs 0) |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.3570 | 0.700 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `se_queda_sola` | Se queda sola sin adulto | 0.2775 | 1.320 | queda: más odds de esta violencia (si = 1 vs 0) |
| `falta_colegio` | Falta al colegio para ayudar | 0.2697 | 1.310 | queda: más odds de esta violencia (si = 1 vs 0) |
| `ie_mujeres` | IE de mujeres | -0.1819 | 0.834 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `rural` | IE rural | -0.1792 | 0.836 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | -0.1457 | 0.864 | queda: menos odds de esta violencia (vs mestiza) |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.1384 | 1.148 | queda: más odds de esta violencia (si = 1 vs 0) |
| `jalo_curso` | Jaló un curso (2023) | 0.1273 | 1.136 | queda: más odds de esta violencia (si = 1 vs 0) |
| `sin_comer` | La dejaron sin comer | 0.1177 | 1.125 | queda: más odds de esta violencia (si = 1 vs 0) |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.1171 | 1.124 | queda: más odds de esta violencia (si = 1 vs 0) |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0.0963 | 1.101 | queda: más odds de esta violencia (vs madre) |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.0721 | 1.075 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_abuela` | Vive con abuela | 0.0711 | 1.074 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_otra_persona` | Vive con otra persona | 0.0508 | 1.052 | queda: más odds de esta violencia (si = 1 vs 0) |
| `pers` | Tamaño del hogar | -0.0427 | 0.958 | queda: menos odds de esta violencia (por 1 DE) |
| `edad` | Edad (lineal) | 0.0338 | 1.034 | queda: más odds de esta violencia (por 1 DE) |
| `vive_tio` | Vive con tío | 0.0220 | 1.022 | queda: más odds de esta violencia (si = 1 vs 0) |
| `vive_hermana` | Vive con hermana/s | -0.0184 | 0.982 | queda: menos odds de esta violencia (si = 1 vs 0) |
| `vive_padrastro` | Vive con padrastro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_madrastra` | Vive con madrastra | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `tiene_papa` | Tiene papá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `tiene_mama` | Tiene mamá | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `alguna_discapacidad` | Alguna discapacidad | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_primo` | Vive con primo | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_otros_parientes` | Vive con otros parientes | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_tia` | Vive con tía | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_prima` | Vive con prima | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_abuelo` | Vive con abuelo | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `vive_hermano` | Vive con hermano/s | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `repitio` | Repitió de grado | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `amigos_colegio` | Mejores amigos en este colegio | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_afroperuana` | Etnia: afroperuana | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `turno_tarde` | Turno tarde | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_blanca` | Etnia: blanca | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_no_sabe` | Etnia: no sabe | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `idioma_otro` | Idioma: otro | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_hermanos` | Cuidador: hermanos | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |
| `cuidador_otros` | Cuidador: otros | 0 | 1 | no queda: el L1 deja efecto 0 dado el resto |

Quedan **20**. No quedan **24** (el L1 las apagó).


---

Los coeficientes en tabla (para que k-medias y CART los lean) están en `data/tablas/lasso_crs04_coef.csv`. No es un segundo informe.
