# LASSO CRS04 (alumnas)

> Coeficiente y OR del L1 en cada violencia a 12 meses. (`scripts/modelos/lasso_crs04.py`)

Logístico L1 (`sklearn.linear_model.LogisticRegressionCV`, `penalty='l1'`, 5-fold, `roc_auc`).
Peso `FACTOR_ALUMNOS` (reescalado a media 1). `edad` y `pers` estandarizadas.
Referencias de dummy: etnia = mestiza, idioma = castellano, cuidador = madre.

Universo: `data/tablas/crs04_modelo.parquet`, se excluyen 18 CAR (no se imputa el flujo de casa).
Especificación: [../metodologia/metodologia.md](../metodologia/metodologia.md).

El peso entra al ajuste. La validación cruzada no incorpora el conglomerado. Lectura de los OR: [../metodologia/metodologia.md](../metodologia/metodologia.md).

## Fuera de X

Servicios de vivienda de CRS01: otra muestra. En el tablero van por departamento.

Tampoco entran el nombre del departamento, `C3P222`, `C3P301_2`, `_4` y `_6`, expulsión, `C3P127`, `C3P124`, ni los bloques de ayuda, agresor y autolesión (`C3P209`–`215`, `216A`, `236`–`247`, `C4P248A/B`, ítems madre).

## Coeficientes

Las 44 variables que entraron al L1. `0` es coeficiente apagado. “En los 3” cuenta en cuántos indicadores queda distinta de cero. Edad y tamaño del hogar están estandarizados.

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

| Variable | Qué es | Coef. (logit) | OR |
| --- | --- | ---: | ---: |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 1.4609 | 4.310 |
| `peleas_casa` | Peleas en casa | 0.9328 | 2.542 |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.9326 | 0.394 |
| `falta_colegio` | Falta al colegio para ayudar | 0.6042 | 1.830 |
| `se_queda_sola` | Se queda sola sin adulto | 0.4235 | 1.527 |
| `alguna_discapacidad` | Alguna discapacidad | 0.2425 | 1.274 |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.1695 | 1.185 |
| `ie_mujeres` | IE de mujeres | -0.1553 | 0.856 |
| `rural` | IE rural | -0.1493 | 0.861 |
| `amigos_colegio` | Mejores amigos en este colegio | -0.1389 | 0.870 |
| `cuidador_hermanos` | Cuidador: hermanos | 0.1009 | 1.106 |
| `vive_hermana` | Vive con hermana/s | -0.1001 | 0.905 |
| `edad` | Edad (lineal) | -0.0976 | 0.907 |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.0863 | 1.090 |
| `vive_hermano` | Vive con hermano/s | -0.0717 | 0.931 |
| `jalo_curso` | Jaló un curso (2023) | 0.0593 | 1.061 |
| `vive_tio` | Vive con tío | 0.0566 | 1.058 |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | -0.0532 | 0.948 |
| `etnia_afroperuana` | Etnia: afroperuana | 0.0416 | 1.042 |
| `repitio` | Repitió de grado | -0.0385 | 0.962 |
| `vive_prima` | Vive con prima | 0.0345 | 1.035 |
| `vive_abuela` | Vive con abuela | -0.0271 | 0.973 |
| `vive_tia` | Vive con tía | 0.0247 | 1.025 |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.0038 | 1.004 |
| `pers` | Tamaño del hogar | 0 | 1 |
| `vive_madrastra` | Vive con madrastra | 0 | 1 |
| `tiene_papa` | Tiene papá | 0 | 1 |
| `tiene_mama` | Tiene mamá | 0 | 1 |
| `vive_padrastro` | Vive con padrastro | 0 | 1 |
| `vive_otra_persona` | Vive con otra persona | 0 | 1 |
| `vive_primo` | Vive con primo | 0 | 1 |
| `vive_otros_parientes` | Vive con otros parientes | 0 | 1 |
| `vive_abuelo` | Vive con abuelo | 0 | 1 |
| `sin_comer` | La dejaron sin comer | 0 | 1 |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 0 | 1 |
| `turno_tarde` | Turno tarde | 0 | 1 |
| `etnia_blanca` | Etnia: blanca | 0 | 1 |
| `etnia_no_sabe` | Etnia: no sabe | 0 | 1 |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 |
| `idioma_otro` | Idioma: otro | 0 | 1 |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0 | 1 |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 |
| `cuidador_otros` | Cuidador: otros | 0 | 1 |

Distintas de cero: 24 de 44.

### Violencia física 12m

n completa = 9,575 · AUC-CV = 0.750 · variables distintas de cero = 31.

| Variable | Qué es | Coef. (logit) | OR |
| --- | --- | ---: | ---: |
| `peleas_casa` | Peleas en casa | 0.9172 | 2.502 |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.8301 | 0.436 |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 0.7134 | 2.041 |
| `falta_colegio` | Falta al colegio para ayudar | 0.6026 | 1.827 |
| `se_queda_sola` | Se queda sola sin adulto | 0.5637 | 1.757 |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.5284 | 1.696 |
| `edad` | Edad (lineal) | -0.3256 | 0.722 |
| `vive_tio` | Vive con tío | 0.3219 | 1.380 |
| `alguna_discapacidad` | Alguna discapacidad | 0.2711 | 1.311 |
| `jalo_curso` | Jaló un curso (2023) | 0.2612 | 1.298 |
| `sin_comer` | La dejaron sin comer | 0.2518 | 1.286 |
| `vive_padrastro` | Vive con padrastro | 0.2068 | 1.230 |
| `etnia_afroperuana` | Etnia: afroperuana | 0.1843 | 1.202 |
| `vive_otros_parientes` | Vive con otros parientes | -0.1780 | 0.837 |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | -0.1486 | 0.862 |
| `vive_otra_persona` | Vive con otra persona | -0.1348 | 0.874 |
| `vive_hermana` | Vive con hermana/s | -0.1105 | 0.895 |
| `etnia_blanca` | Etnia: blanca | 0.1087 | 1.115 |
| `etnia_no_sabe` | Etnia: no sabe | -0.0940 | 0.910 |
| `vive_abuelo` | Vive con abuelo | -0.0805 | 0.923 |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.0775 | 1.081 |
| `amigos_colegio` | Mejores amigos en este colegio | -0.0622 | 0.940 |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.0578 | 1.059 |
| `vive_hermano` | Vive con hermano/s | -0.0480 | 0.953 |
| `cuidador_hermanos` | Cuidador: hermanos | 0.0413 | 1.042 |
| `repitio` | Repitió de grado | 0.0387 | 1.039 |
| `pers` | Tamaño del hogar | -0.0318 | 0.969 |
| `cuidador_otros` | Cuidador: otros | 0.0275 | 1.028 |
| `turno_tarde` | Turno tarde | -0.0029 | 0.997 |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 0.0027 | 1.003 |
| `ie_mujeres` | IE de mujeres | -0.0015 | 0.999 |
| `tiene_mama` | Tiene mamá | 0 | 1 |
| `tiene_papa` | Tiene papá | 0 | 1 |
| `vive_madrastra` | Vive con madrastra | 0 | 1 |
| `vive_tia` | Vive con tía | 0 | 1 |
| `vive_primo` | Vive con primo | 0 | 1 |
| `rural` | IE rural | 0 | 1 |
| `vive_abuela` | Vive con abuela | 0 | 1 |
| `vive_prima` | Vive con prima | 0 | 1 |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 |
| `idioma_otro` | Idioma: otro | 0 | 1 |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0 | 1 |

Distintas de cero: 31 de 44.

### Violencia sexual 12m

n completa = 9,575 · AUC-CV = 0.628 · variables distintas de cero = 20.

| Variable | Qué es | Coef. (logit) | OR |
| --- | --- | ---: | ---: |
| `peleas_casa` | Peleas en casa | 0.5209 | 1.684 |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 0.4127 | 1.511 |
| `toma_en_cuenta` | Toman en cuenta su opinión | -0.3570 | 0.700 |
| `se_queda_sola` | Se queda sola sin adulto | 0.2775 | 1.320 |
| `falta_colegio` | Falta al colegio para ayudar | 0.2697 | 1.310 |
| `ie_mujeres` | IE de mujeres | -0.1819 | 0.834 |
| `rural` | IE rural | -0.1792 | 0.836 |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | -0.1457 | 0.864 |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 0.1384 | 1.148 |
| `jalo_curso` | Jaló un curso (2023) | 0.1273 | 1.136 |
| `sin_comer` | La dejaron sin comer | 0.1177 | 1.125 |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 0.1171 | 1.124 |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 0.0963 | 1.101 |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 0.0721 | 1.075 |
| `vive_abuela` | Vive con abuela | 0.0711 | 1.074 |
| `vive_otra_persona` | Vive con otra persona | 0.0508 | 1.052 |
| `pers` | Tamaño del hogar | -0.0427 | 0.958 |
| `edad` | Edad (lineal) | 0.0338 | 1.034 |
| `vive_tio` | Vive con tío | 0.0220 | 1.022 |
| `vive_hermana` | Vive con hermana/s | -0.0184 | 0.982 |
| `vive_padrastro` | Vive con padrastro | 0 | 1 |
| `vive_madrastra` | Vive con madrastra | 0 | 1 |
| `tiene_papa` | Tiene papá | 0 | 1 |
| `tiene_mama` | Tiene mamá | 0 | 1 |
| `alguna_discapacidad` | Alguna discapacidad | 0 | 1 |
| `vive_primo` | Vive con primo | 0 | 1 |
| `vive_otros_parientes` | Vive con otros parientes | 0 | 1 |
| `vive_tia` | Vive con tía | 0 | 1 |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | 0 | 1 |
| `vive_prima` | Vive con prima | 0 | 1 |
| `vive_abuelo` | Vive con abuelo | 0 | 1 |
| `vive_hermano` | Vive con hermano/s | 0 | 1 |
| `repitio` | Repitió de grado | 0 | 1 |
| `amigos_colegio` | Mejores amigos en este colegio | 0 | 1 |
| `etnia_afroperuana` | Etnia: afroperuana | 0 | 1 |
| `turno_tarde` | Turno tarde | 0 | 1 |
| `etnia_blanca` | Etnia: blanca | 0 | 1 |
| `etnia_no_sabe` | Etnia: no sabe | 0 | 1 |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0 | 1 |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0 | 1 |
| `idioma_otro` | Idioma: otro | 0 | 1 |
| `cuidador_abuelos` | Cuidador: abuelos | 0 | 1 |
| `cuidador_hermanos` | Cuidador: hermanos | 0 | 1 |
| `cuidador_otros` | Cuidador: otros | 0 | 1 |

Distintas de cero: 20 de 44.


---

Coeficientes: `data/tablas/lasso_crs04_coef.csv` (los leen k-medias y CART).
