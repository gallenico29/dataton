# k-medias CRS04 por tipo de violencia

> Tipos de alumna **dentro** de las que sí reportaron una violencia y **dentro** de las que no. Primero se filtra; después se agrupa. X = las 13 del LASSO 3/3. (`scripts/modelos/perfiles_kmeans_crs04.py`)

## Cómo está armado

Agrupa alumnas parecidas en casa, actitudes y colegio (las 13 X que el LASSO dejó en los tres targets). La violencia no entra al agrupamiento; se cuenta después.

n = 9,575 alumnas en estas tablas. N = 1,415,383 (peso `FACTOR_ALUMNOS`). Se parte en sí y no, y dentro de cada lado se piden 3 grupos. k = 3 es un recorte. Silueta cerca de 0.1–0.15: los grupos se parecen.

Si el filtro es física = no, esa alumna puede tener psicológica o sexual. Las tres Y se muestran siempre. Solo con *alguna violencia = no* las tres quedan en 0 %.

El mapa PCA muestra cerca del 20 % de las diferencias entre las 13 preguntas. El nombre del grupo sale de qué barras están más altas, no del mapa. Un grupo con n chico no se lee como si fuera un tercio del país.

Reglas SI–ENTONCES: [perfiles_cart_crs04.md](perfiles_cart_crs04.md). Las 13 variables: [lasso_crs04.md](lasso_crs04.md).

## Qué X usó (primer filtro LASSO)

Coef ≠ 0 en los tres targets. Son 13: `edad`, `toma_en_cuenta`, `act_trabajar`, `act_deje_colegio`, `act_padres_golpear`, `vive_hermana`, `vive_tio`, `se_queda_sola`, `falta_colegio`, `peleas_casa`, `ie_mujeres`, `se_siente_mal`, `jalo_curso`.

### Entran (13)

| Variable | Qué es | En cuántos LASSO | ¿Entra al k-medias? |
| --- | --- | ---: | --- |
| `edad` | Edad (lineal) | 3/3 | sí (3/3) |
| `toma_en_cuenta` | Toman en cuenta su opinión | 3/3 | sí (3/3) |
| `act_trabajar` | Actitud: debe trabajar si falta plata | 3/3 | sí (3/3) |
| `act_deje_colegio` | Actitud: padres deciden que deje el colegio | 3/3 | sí (3/3) |
| `act_padres_golpear` | Actitud: padres tienen derecho a golpear | 3/3 | sí (3/3) |
| `vive_hermana` | Vive con hermana/s | 3/3 | sí (3/3) |
| `vive_tio` | Vive con tío | 3/3 | sí (3/3) |
| `se_queda_sola` | Se queda sola sin adulto | 3/3 | sí (3/3) |
| `falta_colegio` | Falta al colegio para ayudar | 3/3 | sí (3/3) |
| `peleas_casa` | Peleas en casa | 3/3 | sí (3/3) |
| `ie_mujeres` | IE de mujeres | 3/3 | sí (3/3) |
| `se_siente_mal` | Se siente mal/muy mal en el colegio | 3/3 | sí (3/3) |
| `jalo_curso` | Jaló un curso (2023) | 3/3 | sí (3/3) |

### No entran

| Variable | Qué es | En cuántos LASSO | ¿Entra al k-medias? |
| --- | --- | ---: | --- |
| `pers` | Tamaño del hogar | 2/3 | no |
| `alguna_discapacidad` | Alguna discapacidad | 2/3 | no |
| `tiene_mama` | Tiene mamá | 0/3 | no |
| `tiene_papa` | Tiene papá | 0/3 | no |
| `vive_madrastra` | Vive con madrastra | 0/3 | no |
| `vive_padrastro` | Vive con padrastro | 1/3 | no |
| `vive_hermano` | Vive con hermano/s | 2/3 | no |
| `vive_abuela` | Vive con abuela | 2/3 | no |
| `vive_abuelo` | Vive con abuelo | 1/3 | no |
| `vive_tia` | Vive con tía | 1/3 | no |
| `vive_prima` | Vive con prima | 1/3 | no |
| `vive_primo` | Vive con primo | 0/3 | no |
| `vive_otros_parientes` | Vive con otros parientes | 1/3 | no |
| `vive_otra_persona` | Vive con otra persona | 2/3 | no |
| `duerme_sola_cuarto` | Duerme sola en el cuarto | 2/3 | no |
| `sin_comer` | La dejaron sin comer | 2/3 | no |
| `rural` | IE rural | 2/3 | no |
| `turno_tarde` | Turno tarde | 1/3 | no |
| `repitio` | Repitió de grado | 2/3 | no |
| `amigos_colegio` | Mejores amigos en este colegio | 2/3 | no |
| `etnia_quechua` | Etnia: quechua (ref. mestiza) | 2/3 | no |
| `etnia_afroperuana` | Etnia: afroperuana | 2/3 | no |
| `etnia_blanca` | Etnia: blanca | 1/3 | no |
| `etnia_no_sabe` | Etnia: no sabe | 1/3 | no |
| `etnia_otra_indigena_otro` | Etnia: otra indígena / otro | 0/3 | no |
| `idioma_quechua` | Idioma: quechua (ref. castellano) | 0/3 | no |
| `idioma_otro` | Idioma: otro | 0/3 | no |
| `cuidador_padre` | Cuidador: padre (ref. madre) | 1/3 | no |
| `cuidador_abuelos` | Cuidador: abuelos | 0/3 | no |
| `cuidador_hermanos` | Cuidador: hermanos | 2/3 | no |
| `cuidador_otros` | Cuidador: otros | 1/3 | no |

---

## Alguna violencia (psic o fís o sexual)

Esta barra parte la muestra *antes* del k-medias. Sí = reportó `alguna_violencia`; no = no la reportó.

El 65.8% de la N (n=6,339) entra al cluster de las que sí; el 34.2% (n=3,236) al de las que no. Esta Y no entra al agrupamiento: solo las 13 X. Si el filtro es un tipo (p. ej. física), las del “no” igual pueden tener psicológica o sexual.

![Filtro alguna](../img/perfiles_alguna_filtro.svg)

### Las que sí — Alguna violencia (psic o fís o sexual)

n = 6,339 · N = 931,427 · silueta k=3: **0.134**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.088 |
| 3 | 0.134 ← usado |
| 4 | 0.119 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `alguna_si-1` | 2,145 | 287,403 | 92.5% | 54.5% | 39.3% | 13.94 | 67.1% | 58.9% | 28.2% | 66.3% | 59.9% | 13.1% | 74.4% | 19.4% | 73.5% | 0.0% | 31.0% | 43.5% |
| `alguna_si-2` | 603 | 84,089 | 91.0% | 38.6% | 30.2% | 14.37 | 86.6% | 17.6% | 17.6% | 31.1% | 51.6% | 6.5% | 63.7% | 7.1% | 60.6% | 100.0% | 12.1% | 26.0% |
| `alguna_si-3` | 3,591 | 559,934 | 89.7% | 31.5% | 33.4% | 14.57 | 94.7% | 8.3% | 7.8% | 21.6% | 54.8% | 8.8% | 59.4% | 3.4% | 50.7% | 0.0% | 7.3% | 20.3% |

#### Mapa PCA

![perfiles_alguna_si_pca.png](../img/perfiles_alguna_si_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (12 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, padres golpear. A la **izquierda**, más: la toman en cuenta.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear. Abajo: peleas casa, se queda sola.

PC1+PC2 solo muestran 21 % de cómo se distinguen las X. El otro 79 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `alguna_si-3` es el más grande (n=3,591).

#### Biplot (cada variable)

![perfiles_alguna_si_biplot.png](../img/perfiles_alguna_si_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, padres golpear vs la toman en cuenta”. Las que más pesan: debe trabajar (suma al PC1), la toman en cuenta (resta al PC1), padres golpear (suma al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear vs peleas casa, se queda sola”. Pesan: padres golpear (suma al PC2), peleas casa (resta al PC2), se queda sola (resta al PC2).

#### Una barra por variable

![perfiles_alguna_si_vars.png](../img/perfiles_alguna_si_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**IE mujeres:** `alguna_si-2` tiene 100.0% y `alguna_si-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `alguna_si-3` tiene 14.6 años y `alguna_si-1` 13.9 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `alguna_si-1` tiene 58.9% y `alguna_si-3` 8.3%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `alguna_si-1` tiene 66.3% y `alguna_si-3` 21.6%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`alguna_si-2` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Barras de las 13 X juntas

![perfiles_alguna_si_x.svg](../img/perfiles_alguna_si_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**IE mujeres:** `alguna_si-2` tiene 100.0% y `alguna_si-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `alguna_si-3` tiene 14.6 años y `alguna_si-1` 13.9 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `alguna_si-1` tiene 58.9% y `alguna_si-3` 8.3%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `alguna_si-1` tiene 66.3% y `alguna_si-3` 21.6%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`alguna_si-2` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Edad

![perfiles_alguna_si_edad.svg](../img/perfiles_alguna_si_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`alguna_si-1` = 13.94 años; `alguna_si-3` = 14.57 (brecha 0.64). `alguna_si-1` es un poco más joven. Eso no se lee como más violencia: mira el gráfico de las tres Y.

#### Cruce con los tres tipos de violencia

![perfiles_alguna_si_violencia.svg](../img/perfiles_alguna_si_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`alguna_si-1` (n=2,145): psicológica 92.5%, física 54.5%, sexual 39.3%.
`alguna_si-2` (n=603): psicológica 91.0%, física 38.6%, sexual 30.2%.
`alguna_si-3` (n=3,591): psicológica 89.7%, física 31.5%, sexual 33.4%.

Aquí **todas** ya tienen `alguna_violencia` = 1 (por el filtro). Si un grupo tiene más física o más sexual que otro, ese tipo de casa/actitud se junta más con violencia **superpuesta**, no con “descubrir” el filtro.

### Las que no — Alguna violencia (psic o fís o sexual)

n = 3,236 · N = 483,956 · silueta k=3: **0.133**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.120 |
| 3 | 0.133 ← usado |
| 4 | 0.171 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `alguna_no-1` | 120 | 16,002 | 0.0% | 0.0% | 0.0% | 14.63 | 96.2% | 27.7% | 10.4% | 35.2% | 52.0% | 3.8% | 56.9% | 100.0% | 37.5% | 5.4% | 1.2% | 22.1% |
| `alguna_no-2` | 1,040 | 135,801 | 0.0% | 0.0% | 0.0% | 14.46 | 94.5% | 34.8% | 14.7% | 100.0% | 63.9% | 7.6% | 47.4% | 0.0% | 32.0% | 8.7% | 3.5% | 23.8% |
| `alguna_no-3` | 2,076 | 332,154 | 0.0% | 0.0% | 0.0% | 14.59 | 97.1% | 11.7% | 8.7% | 0.0% | 54.9% | 8.1% | 47.3% | 0.0% | 30.3% | 13.4% | 1.8% | 24.0% |

#### Mapa PCA

![perfiles_alguna_no_pca.png](../img/perfiles_alguna_no_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (10 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, padres golpear, se queda sola. A la **izquierda**, más: esas X de la izquierda.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: peleas casa, se queda sola, se siente mal. Abajo: —.

PC1+PC2 solo muestran 20 % de cómo se distinguen las X. El otro 80 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `alguna_no-3` es el más grande (n=2,076). `alguna_no-1` tiene n=120: es un cajón chico, no un perfil para armar política.

#### Biplot (cada variable)

![perfiles_alguna_no_biplot.png](../img/perfiles_alguna_no_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, padres golpear, se queda sola vs —”. Las que más pesan: debe trabajar (suma al PC1), padres golpear (suma al PC1), se queda sola (suma al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “peleas casa, se queda sola, se siente mal vs —”. Pesan: peleas casa (suma al PC2), se queda sola (suma al PC2), se siente mal (suma al PC2).

#### Una barra por variable

![perfiles_alguna_no_vars.png](../img/perfiles_alguna_no_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**padres golpear:** `alguna_no-2` tiene 100.0% y `alguna_no-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**falta colegio:** `alguna_no-1` tiene 100.0% y `alguna_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `alguna_no-2` tiene 34.8% y `alguna_no-3` 11.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `alguna_no-1` tiene 14.6 años y `alguna_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`alguna_no-1` es casi 100 % “falta al colegio”: grupo flaco definido por una sola X. `alguna_no-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Barras de las 13 X juntas

![perfiles_alguna_no_x.svg](../img/perfiles_alguna_no_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**padres golpear:** `alguna_no-2` tiene 100.0% y `alguna_no-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**falta colegio:** `alguna_no-1` tiene 100.0% y `alguna_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `alguna_no-2` tiene 34.8% y `alguna_no-3` 11.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `alguna_no-1` tiene 14.6 años y `alguna_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`alguna_no-1` es casi 100 % “falta al colegio”: grupo flaco definido por una sola X. `alguna_no-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Edad

![perfiles_alguna_no_edad.svg](../img/perfiles_alguna_no_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`alguna_no-2` = 14.46 años; `alguna_no-1` = 14.63 (brecha 0.17). La edad no es lo que parte estos tipos.

#### Cruce con los tres tipos de violencia

![perfiles_alguna_no_violencia.svg](../img/perfiles_alguna_no_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`alguna_no-1` (n=120): psicológica 0.0%, física 0.0%, sexual 0.0%.
`alguna_no-2` (n=1,040): psicológica 0.0%, física 0.0%, sexual 0.0%.
`alguna_no-3` (n=2,076): psicológica 0.0%, física 0.0%, sexual 0.0%.

Aquí `alguna_violencia` = 0 para todas. Un % > 0 de psicológica/física/sexual es **otra** violencia, no la del filtro. Si los tres % son 0, este lado es “no reportó ninguna” (solo pasa con el filtro *alguna*).

## Violencia psicológica 12m

Esta barra parte la muestra *antes* del k-medias. Sí = reportó `viol_psicologica_12m`; no = no la reportó.

El 59.7% de la N (n=5,722) entra al cluster de las que sí; el 40.3% (n=3,853) al de las que no. Esta Y no entra al agrupamiento: solo las 13 X. Si el filtro es un tipo (p. ej. física), las del “no” igual pueden tener psicológica o sexual.

![Filtro psic](../img/perfiles_psic_filtro.svg)

### Las que sí — Violencia psicológica 12m

n = 5,722 · N = 844,334 · silueta k=3: **0.110**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.123 |
| 3 | 0.110 ← usado |
| 4 | 0.116 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `psic_si-1` | 562 | 86,532 | 100.0% | 47.5% | 36.0% | 14.14 | 82.4% | 27.4% | 17.5% | 41.4% | 47.2% | 100.0% | 54.1% | 15.3% | 60.2% | 6.1% | 20.2% | 34.4% |
| `psic_si-2` | 2,190 | 271,919 | 100.0% | 48.0% | 34.2% | 14.07 | 82.4% | 35.5% | 23.1% | 99.7% | 58.6% | 0.0% | 69.2% | 11.6% | 62.5% | 8.2% | 18.6% | 29.7% |
| `psic_si-3` | 2,970 | 485,884 | 100.0% | 31.9% | 30.4% | 14.51 | 86.2% | 17.6% | 10.7% | 0.0% | 55.5% | 0.0% | 64.7% | 6.6% | 58.9% | 10.1% | 13.9% | 26.8% |

#### Mapa PCA

![perfiles_psic_si_pca.png](../img/perfiles_psic_si_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (12 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, padres golpear. A la **izquierda**, más: la toman en cuenta.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear. Abajo: peleas casa, edad.

PC1+PC2 solo muestran 21 % de cómo se distinguen las X. El otro 79 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `psic_si-3` es el más grande (n=2,970).

#### Biplot (cada variable)

![perfiles_psic_si_biplot.png](../img/perfiles_psic_si_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, padres golpear vs la toman en cuenta”. Las que más pesan: debe trabajar (suma al PC1), padres golpear (suma al PC1), la toman en cuenta (resta al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear vs peleas casa, edad”. Pesan: padres golpear (suma al PC2), peleas casa (resta al PC2), edad (resta al PC2).

#### Una barra por variable

![perfiles_psic_si_vars.png](../img/perfiles_psic_si_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**vive tío:** `psic_si-1` tiene 100.0% y `psic_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `psic_si-2` tiene 99.7% y `psic_si-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `psic_si-3` tiene 14.5 años y `psic_si-2` 14.1 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `psic_si-2` tiene 35.5% y `psic_si-3` 17.6%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`psic_si-1` es casi 100 % “vive con tío”. `psic_si-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Barras de las 13 X juntas

![perfiles_psic_si_x.svg](../img/perfiles_psic_si_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**vive tío:** `psic_si-1` tiene 100.0% y `psic_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `psic_si-2` tiene 99.7% y `psic_si-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `psic_si-3` tiene 14.5 años y `psic_si-2` 14.1 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `psic_si-2` tiene 35.5% y `psic_si-3` 17.6%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`psic_si-1` es casi 100 % “vive con tío”. `psic_si-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Edad

![perfiles_psic_si_edad.svg](../img/perfiles_psic_si_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`psic_si-2` = 14.07 años; `psic_si-3` = 14.51 (brecha 0.44). `psic_si-2` es un poco más joven. Eso no se lee como más violencia: mira el gráfico de las tres Y.

#### Cruce con los tres tipos de violencia

![perfiles_psic_si_violencia.svg](../img/perfiles_psic_si_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`psic_si-1` (n=562): psicológica 100.0%, física 47.5%, sexual 36.0%.
`psic_si-2` (n=2,190): psicológica 100.0%, física 48.0%, sexual 34.2%.
`psic_si-3` (n=2,970): psicológica 100.0%, física 31.9%, sexual 30.4%.

Aquí **todas** ya tienen `viol_psicologica_12m` = 1 (por el filtro). Si un grupo tiene más física o más sexual que otro, ese tipo de casa/actitud se junta más con violencia **superpuesta**, no con “descubrir” el filtro.

### Las que no — Violencia psicológica 12m

n = 3,853 · N = 571,049 · silueta k=3: **0.164**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.116 |
| 3 | 0.164 ← usado |
| 4 | 0.126 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `psic_no-1` | 801 | 107,463 | 0.0% | 9.0% | 13.8% | 14.79 | 94.4% | 100.0% | 10.4% | 54.1% | 59.9% | 7.9% | 52.1% | 5.2% | 37.0% | 0.0% | 3.7% | 27.4% |
| `psic_no-2` | 2,637 | 398,736 | 0.0% | 6.6% | 8.6% | 14.51 | 96.2% | 0.0% | 9.7% | 25.0% | 57.0% | 7.6% | 49.6% | 3.4% | 31.5% | 0.0% | 2.4% | 22.1% |
| `psic_no-3` | 415 | 64,851 | 0.0% | 4.9% | 7.6% | 14.56 | 97.1% | 11.7% | 15.5% | 22.7% | 59.6% | 7.7% | 42.1% | 1.5% | 34.9% | 100.0% | 3.2% | 27.4% |

#### Mapa PCA

![perfiles_psic_no_pca.png](../img/perfiles_psic_no_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (11 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, padres golpear. A la **izquierda**, más: la toman en cuenta.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: peleas casa, se queda sola, se siente mal. Abajo: —.

PC1+PC2 solo muestran 20 % de cómo se distinguen las X. El otro 80 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `psic_no-2` es el más grande (n=2,637).

#### Biplot (cada variable)

![perfiles_psic_no_biplot.png](../img/perfiles_psic_no_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, padres golpear vs la toman en cuenta”. Las que más pesan: debe trabajar (suma al PC1), padres golpear (suma al PC1), la toman en cuenta (resta al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “peleas casa, se queda sola, se siente mal vs —”. Pesan: peleas casa (suma al PC2), se queda sola (suma al PC2), se siente mal (suma al PC2).

#### Una barra por variable

![perfiles_psic_no_vars.png](../img/perfiles_psic_no_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `psic_no-1` tiene 100.0% y `psic_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**IE mujeres:** `psic_no-3` tiene 100.0% y `psic_no-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `psic_no-1` tiene 54.1% y `psic_no-3` 22.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `psic_no-1` tiene 14.8 años y `psic_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`psic_no-1` es casi 100 % “debe trabajar si falta plata”. `psic_no-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Barras de las 13 X juntas

![perfiles_psic_no_x.svg](../img/perfiles_psic_no_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `psic_no-1` tiene 100.0% y `psic_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**IE mujeres:** `psic_no-3` tiene 100.0% y `psic_no-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `psic_no-1` tiene 54.1% y `psic_no-3` 22.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `psic_no-1` tiene 14.8 años y `psic_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`psic_no-1` es casi 100 % “debe trabajar si falta plata”. `psic_no-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Edad

![perfiles_psic_no_edad.svg](../img/perfiles_psic_no_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`psic_no-2` = 14.51 años; `psic_no-1` = 14.79 (brecha 0.28). La edad no es lo que parte estos tipos.

#### Cruce con los tres tipos de violencia

![perfiles_psic_no_violencia.svg](../img/perfiles_psic_no_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`psic_no-1` (n=801): psicológica 0.0%, física 9.0%, sexual 13.8%.
`psic_no-2` (n=2,637): psicológica 0.0%, física 6.6%, sexual 8.6%.
`psic_no-3` (n=415): psicológica 0.0%, física 4.9%, sexual 7.6%.

Aquí `viol_psicologica_12m` = 0 para todas. Un % > 0 de psicológica/física/sexual es **otra** violencia, no la del filtro. Si los tres % son 0, este lado es “no reportó ninguna” (solo pasa con el filtro *alguna*).

## Violencia física 12m

Esta barra parte la muestra *antes* del k-medias. Sí = reportó `viol_fisica_12m`; no = no la reportó.

El 25.8% de la N (n=2,598) entra al cluster de las que sí; el 74.2% (n=6,977) al de las que no. Esta Y no entra al agrupamiento: solo las 13 X. Si el filtro es un tipo (p. ej. física), las del “no” igual pueden tener psicológica o sexual.

![Filtro fis](../img/perfiles_fis_filtro.svg)

### Las que sí — Violencia física 12m

n = 2,598 · N = 365,429 · silueta k=3: **0.114**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.102 |
| 3 | 0.114 ← usado |
| 4 | 0.121 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fis_si-1` | 276 | 43,853 | 93.7% | 100.0% | 45.2% | 13.75 | 79.8% | 27.9% | 23.4% | 50.3% | 47.3% | 100.0% | 66.4% | 19.3% | 70.7% | 4.4% | 23.4% | 39.4% |
| `fis_si-2` | 760 | 91,202 | 89.2% | 100.0% | 38.6% | 14.15 | 74.2% | 100.0% | 23.1% | 58.5% | 59.5% | 0.0% | 73.4% | 16.2% | 73.0% | 7.0% | 19.6% | 39.5% |
| `fis_si-3` | 1,562 | 230,375 | 88.5% | 100.0% | 38.1% | 13.98 | 80.2% | 0.0% | 13.8% | 40.4% | 55.3% | 0.0% | 73.0% | 9.0% | 67.5% | 10.4% | 18.8% | 28.9% |

#### Mapa PCA

![perfiles_fis_si_pca.png](../img/perfiles_fis_si_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (11 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, falta colegio, padres golpear. A la **izquierda**, más: esas X de la izquierda.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear, la toman en cuenta. Abajo: se siente mal.

PC1+PC2 solo muestran 20 % de cómo se distinguen las X. El otro 80 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `fis_si-3` es el más grande (n=1,562).

#### Biplot (cada variable)

![perfiles_fis_si_biplot.png](../img/perfiles_fis_si_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, falta colegio, padres golpear vs —”. Las que más pesan: debe trabajar (suma al PC1), falta colegio (suma al PC1), padres golpear (suma al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear, la toman en cuenta vs se siente mal”. Pesan: padres golpear (suma al PC2), la toman en cuenta (suma al PC2), se siente mal (resta al PC2).

#### Una barra por variable

![perfiles_fis_si_vars.png](../img/perfiles_fis_si_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `fis_si-2` tiene 100.0% y `fis_si-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**vive tío:** `fis_si-1` tiene 100.0% y `fis_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `fis_si-2` tiene 14.2 años y `fis_si-1` 13.7 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `fis_si-2` tiene 58.5% y `fis_si-3` 40.4%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`fis_si-1` es casi 100 % “vive con tío”. `fis_si-2` es casi 100 % “debe trabajar si falta plata”.

#### Barras de las 13 X juntas

![perfiles_fis_si_x.svg](../img/perfiles_fis_si_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `fis_si-2` tiene 100.0% y `fis_si-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**vive tío:** `fis_si-1` tiene 100.0% y `fis_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `fis_si-2` tiene 14.2 años y `fis_si-1` 13.7 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `fis_si-2` tiene 58.5% y `fis_si-3` 40.4%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`fis_si-1` es casi 100 % “vive con tío”. `fis_si-2` es casi 100 % “debe trabajar si falta plata”.

#### Edad

![perfiles_fis_si_edad.svg](../img/perfiles_fis_si_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`fis_si-1` = 13.75 años; `fis_si-2` = 14.15 (brecha 0.41). `fis_si-1` es un poco más joven. Eso no se lee como más violencia: mira el gráfico de las tres Y.

#### Cruce con los tres tipos de violencia

![perfiles_fis_si_violencia.svg](../img/perfiles_fis_si_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`fis_si-1` (n=276): psicológica 93.7%, física 100.0%, sexual 45.2%.
`fis_si-2` (n=760): psicológica 89.2%, física 100.0%, sexual 38.6%.
`fis_si-3` (n=1,562): psicológica 88.5%, física 100.0%, sexual 38.1%.

Aquí **todas** ya tienen `viol_fisica_12m` = 1 (por el filtro). Si un grupo tiene más física o más sexual que otro, ese tipo de casa/actitud se junta más con violencia **superpuesta**, no con “descubrir” el filtro.

### Las que no — Violencia física 12m

n = 6,977 · N = 1,049,954 · silueta k=3: **0.158**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.141 |
| 3 | 0.158 ← usado |
| 4 | 0.126 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `fis_no-1` | 1,507 | 202,912 | 51.8% | 0.0% | 21.4% | 14.67 | 88.3% | 100.0% | 13.6% | 50.6% | 58.3% | 9.4% | 59.3% | 7.6% | 46.1% | 0.0% | 9.7% | 28.9% |
| `fis_no-2` | 4,771 | 738,117 | 49.5% | 0.0% | 16.9% | 14.54 | 93.7% | 0.0% | 11.2% | 25.0% | 56.6% | 8.0% | 53.1% | 4.5% | 40.7% | 0.0% | 7.2% | 22.8% |
| `fis_no-3` | 699 | 108,925 | 43.4% | 0.0% | 13.2% | 14.63 | 95.5% | 13.6% | 15.1% | 21.5% | 56.3% | 7.7% | 49.3% | 3.8% | 44.8% | 100.0% | 5.7% | 26.9% |

#### Mapa PCA

![perfiles_fis_no_pca.png](../img/perfiles_fis_no_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (11 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, padres golpear. A la **izquierda**, más: la toman en cuenta.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear. Abajo: peleas casa, se queda sola.

PC1+PC2 solo muestran 20 % de cómo se distinguen las X. El otro 80 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `fis_no-2` es el más grande (n=4,771).

#### Biplot (cada variable)

![perfiles_fis_no_biplot.png](../img/perfiles_fis_no_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, padres golpear vs la toman en cuenta”. Las que más pesan: debe trabajar (suma al PC1), padres golpear (suma al PC1), la toman en cuenta (resta al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear vs peleas casa, se queda sola”. Pesan: padres golpear (suma al PC2), peleas casa (resta al PC2), se queda sola (resta al PC2).

#### Una barra por variable

![perfiles_fis_no_vars.png](../img/perfiles_fis_no_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `fis_no-1` tiene 100.0% y `fis_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**IE mujeres:** `fis_no-3` tiene 100.0% y `fis_no-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `fis_no-1` tiene 50.6% y `fis_no-3` 21.5%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `fis_no-1` tiene 14.7 años y `fis_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`fis_no-1` es casi 100 % “debe trabajar si falta plata”. `fis_no-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Barras de las 13 X juntas

![perfiles_fis_no_x.svg](../img/perfiles_fis_no_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**debe trabajar:** `fis_no-1` tiene 100.0% y `fis_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**IE mujeres:** `fis_no-3` tiene 100.0% y `fis_no-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `fis_no-1` tiene 50.6% y `fis_no-3` 21.5%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `fis_no-1` tiene 14.7 años y `fis_no-2` 14.5 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`fis_no-1` es casi 100 % “debe trabajar si falta plata”. `fis_no-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Edad

![perfiles_fis_no_edad.svg](../img/perfiles_fis_no_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`fis_no-2` = 14.54 años; `fis_no-1` = 14.67 (brecha 0.13). La edad no es lo que parte estos tipos.

#### Cruce con los tres tipos de violencia

![perfiles_fis_no_violencia.svg](../img/perfiles_fis_no_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`fis_no-1` (n=1,507): psicológica 51.8%, física 0.0%, sexual 21.4%.
`fis_no-2` (n=4,771): psicológica 49.5%, física 0.0%, sexual 16.9%.
`fis_no-3` (n=699): psicológica 43.4%, física 0.0%, sexual 13.2%.

Aquí `viol_fisica_12m` = 0 para todas. Un % > 0 de psicológica/física/sexual es **otra** violencia, no la del filtro. Si los tres % son 0, este lado es “no reportó ninguna” (solo pasa con el filtro *alguna*).

## Violencia sexual 12m

Esta barra parte la muestra *antes* del k-medias. Sí = reportó `viol_sexual_12m`; no = no la reportó.

El 23.0% de la N (n=2,093) entra al cluster de las que sí; el 77.0% (n=7,482) al de las que no. Esta Y no entra al agrupamiento: solo las 13 X. Si el filtro es un tipo (p. ej. física), las del “no” igual pueden tener psicológica o sexual.

![Filtro sex](../img/perfiles_sex_filtro.svg)

### Las que sí — Violencia sexual 12m

n = 2,093 · N = 325,545 · silueta k=3: **0.128**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.151 |
| 3 | 0.128 ← usado |
| 4 | 0.114 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sex_si-1` | 600 | 83,120 | 82.1% | 47.7% | 100.0% | 14.33 | 78.0% | 99.8% | 23.5% | 55.3% | 58.8% | 14.2% | 68.6% | 15.0% | 67.7% | 0.0% | 22.3% | 40.2% |
| `sex_si-2` | 1,316 | 217,009 | 84.3% | 42.5% | 100.0% | 14.49 | 86.0% | 0.0% | 13.3% | 30.7% | 53.3% | 9.8% | 66.7% | 8.9% | 61.3% | 0.0% | 14.8% | 27.2% |
| `sex_si-3` | 177 | 25,417 | 80.7% | 43.3% | 100.0% | 14.33 | 79.3% | 21.0% | 20.6% | 38.5% | 53.1% | 7.4% | 66.1% | 6.5% | 53.7% | 100.0% | 12.1% | 31.7% |

#### Mapa PCA

![perfiles_sex_si_pca.png](../img/perfiles_sex_si_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (12 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: la toman en cuenta. A la **izquierda**, más: padres golpear, debe trabajar.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear, la toman en cuenta, debe trabajar. Abajo: —.

PC1+PC2 solo muestran 21 % de cómo se distinguen las X. El otro 79 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `sex_si-2` es el más grande (n=1,316). `sex_si-3` tiene n=177: es un cajón chico, no un perfil para armar política.

#### Biplot (cada variable)

![perfiles_sex_si_biplot.png](../img/perfiles_sex_si_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “la toman en cuenta vs padres golpear, debe trabajar”. Las que más pesan: la toman en cuenta (suma al PC1), padres golpear (resta al PC1), debe trabajar (resta al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear, la toman en cuenta, debe trabajar vs —”. Pesan: padres golpear (suma al PC2), la toman en cuenta (suma al PC2), debe trabajar (suma al PC2).

#### Una barra por variable

![perfiles_sex_si_vars.png](../img/perfiles_sex_si_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**IE mujeres:** `sex_si-3` tiene 100.0% y `sex_si-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `sex_si-1` tiene 99.8% y `sex_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `sex_si-1` tiene 55.3% y `sex_si-2` 30.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `sex_si-2` tiene 14.5 años y `sex_si-1` 14.3 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`sex_si-1` es casi 100 % “debe trabajar si falta plata”. `sex_si-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Barras de las 13 X juntas

![perfiles_sex_si_x.svg](../img/perfiles_sex_si_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**IE mujeres:** `sex_si-3` tiene 100.0% y `sex_si-1` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `sex_si-1` tiene 99.8% y `sex_si-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `sex_si-1` tiene 55.3% y `sex_si-2` 30.7%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `sex_si-2` tiene 14.5 años y `sex_si-1` 14.3 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`sex_si-1` es casi 100 % “debe trabajar si falta plata”. `sex_si-3` es casi 100 % IE de mujeres: el grupo se separa por ser colegio de mujeres.

#### Edad

![perfiles_sex_si_edad.svg](../img/perfiles_sex_si_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`sex_si-1` = 14.33 años; `sex_si-2` = 14.49 (brecha 0.16). La edad no es lo que parte estos tipos.

#### Cruce con los tres tipos de violencia

![perfiles_sex_si_violencia.svg](../img/perfiles_sex_si_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`sex_si-1` (n=600): psicológica 82.1%, física 47.7%, sexual 100.0%.
`sex_si-2` (n=1,316): psicológica 84.3%, física 42.5%, sexual 100.0%.
`sex_si-3` (n=177): psicológica 80.7%, física 43.3%, sexual 100.0%.

Aquí **todas** ya tienen `viol_sexual_12m` = 1 (por el filtro). Si un grupo tiene más física o más sexual que otro, ese tipo de casa/actitud se junta más con violencia **superpuesta**, no con “descubrir” el filtro.

### Las que no — Violencia sexual 12m

n = 7,482 · N = 1,089,838 · silueta k=3: **0.121**

| k | Silueta (sin peso) |
| ---: | ---: |
| 2 | 0.141 |
| 3 | 0.121 ← usado |
| 4 | 0.117 |

| Cluster | n | N | % psic. | % fís. | % sexual | Edad (lineal) | Toman en cuenta su opinión | Actitud: debe trabajar si falta plata | Actitud: padres deciden que deje el colegio | Actitud: padres tienen derecho a golpear | Vive con hermana/s | Vive con tío | Se queda sola sin adulto | Falta al colegio para ayudar | Peleas en casa | IE de mujeres | Se siente mal/muy mal en el colegio | Jaló un curso (2023) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sex_no-1` | 658 | 95,597 | 57.9% | 25.2% | 0.0% | 14.31 | 89.0% | 21.6% | 12.0% | 35.9% | 47.6% | 100.0% | 44.4% | 9.1% | 48.8% | 8.8% | 10.7% | 32.0% |
| `sex_no-2` | 2,574 | 323,388 | 55.4% | 26.9% | 0.0% | 14.24 | 88.2% | 34.6% | 18.4% | 99.8% | 62.9% | 0.0% | 59.6% | 7.5% | 46.9% | 7.9% | 11.0% | 25.6% |
| `sex_no-3` | 4,250 | 670,853 | 50.4% | 16.6% | 0.0% | 14.53 | 92.5% | 14.9% | 9.7% | 0.0% | 55.6% | 0.0% | 56.1% | 4.5% | 43.9% | 12.2% | 7.7% | 24.2% |

#### Mapa PCA

![perfiles_sex_no_pca.png](../img/perfiles_sex_no_pca.png)

Cada punto = una alumna. El k-medias las agrupó con las 13 X a la vez. Este dibujo **aplasta** esas 13 dimensiones a 2 ejes para que se vea. PC = componente principal = un eje resumen (un combo de las 13 X). No es violencia: es un resumen de casa / actitudes / colegio.

**PC1 (eje de lado a lado) significa** el combo que más diferencia a estas chicas (12 % de toda la variación de las 13 X). A la **derecha** tiende a haber más: debe trabajar, peleas casa. A la **izquierda**, más: la toman en cuenta.

**PC2 (eje de abajo a arriba) significa** el segundo combo, distinto del primero (9 %). Arriba: padres golpear. Abajo: peleas casa, IE mujeres.

PC1+PC2 solo muestran 21 % de cómo se distinguen las X. El otro 79 % no cabe en el plano: por eso los colores se mezclan. No quiere decir que los grupos no existan; quiere decir que 2D no alcanza. La cruz blanca es el centro de cada tipo. `sex_no-3` es el más grande (n=4,250).

#### Biplot (cada variable)

![perfiles_sex_no_biplot.png](../img/perfiles_sex_no_biplot.png)

Cada flecha es **una** de las 13 X. Si la alumna tiene esa X (sí = 1, o más edad), el punto se mueve hacia la flecha. Flechas juntas = esas X suelen ir a la par. Flechas opuestas = contrastan.

**PC1 implica:** un eje “debe trabajar, peleas casa vs la toman en cuenta”. Las que más pesan: debe trabajar (suma al PC1), la toman en cuenta (resta al PC1), peleas casa (suma al PC1). Ejemplo: si “la toman en cuenta” apunta al revés de “peleas / se siente mal”, tener voz en casa y vivir peleas no tiran para el mismo lado.

**PC2 implica:** un segundo eje “padres golpear vs peleas casa, IE mujeres”. Pesan: padres golpear (suma al PC2), peleas casa (resta al PC2), IE mujeres (resta al PC2).

#### Una barra por variable

![perfiles_sex_no_vars.png](../img/perfiles_sex_no_vars.png)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**vive tío:** `sex_no-1` tiene 100.0% y `sex_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `sex_no-2` tiene 99.8% y `sex_no-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `sex_no-3` tiene 14.5 años y `sex_no-2` 14.2 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `sex_no-2` tiene 34.6% y `sex_no-3` 14.9%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`sex_no-1` es casi 100 % “vive con tío”. `sex_no-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Barras de las 13 X juntas

![perfiles_sex_no_x.svg](../img/perfiles_sex_no_x.svg)

Un panel por cada X del LASSO. Edad en años; el resto = % del cluster que tiene esa X.

**vive tío:** `sex_no-1` tiene 100.0% y `sex_no-2` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**padres golpear:** `sex_no-2` tiene 99.8% y `sex_no-3` 0.0%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**edad:** `sex_no-3` tiene 14.5 años y `sex_no-2` 14.2 años. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

**debe trabajar:** `sex_no-2` tiene 34.6% y `sex_no-3` 14.9%. Eso implica que el k-medias usó esta X para apartar esos dos tipos.

`sex_no-1` es casi 100 % “vive con tío”. `sex_no-2` es casi 100 % “padres tienen derecho a golpear”: otra vez un corte por una dummy, no un perfil mixto.

#### Edad

![perfiles_sex_no_edad.svg](../img/perfiles_sex_no_edad.svg)

Edad media de cada tipo (años). El k-medias sí usó `edad` (estandarizada).

`sex_no-2` = 14.24 años; `sex_no-3` = 14.53 (brecha 0.29). La edad no es lo que parte estos tipos.

#### Cruce con los tres tipos de violencia

![perfiles_sex_no_violencia.svg](../img/perfiles_sex_no_violencia.svg)

Violencia 12m **después** de armar el grupo. No se usó para clusterizar.

`sex_no-1` (n=658): psicológica 57.9%, física 25.2%, sexual 0.0%.
`sex_no-2` (n=2,574): psicológica 55.4%, física 26.9%, sexual 0.0%.
`sex_no-3` (n=4,250): psicológica 50.4%, física 16.6%, sexual 0.0%.

Aquí `viol_sexual_12m` = 0 para todas. Un % > 0 de psicológica/física/sexual es **otra** violencia, no la del filtro. Si los tres % son 0, este lado es “no reportó ninguna” (solo pasa con el filtro *alguna*).


Asignación: `data/tablas/perfiles_kmeans_asig.csv` (columnas `filtro`, `universo`, `cluster`).
