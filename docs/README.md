# Informes

Tres carpetas. El `.py` **escribe** el `.md`; tú lees el markdown. No son Rmd.

Los CSV no son un segundo informe: son la misma tabla para Excel o para que otro script la lea. Viven en `data/tablas/`, no aquí.

```
docs/
  descriptivos/     cómo se ve la muestra y el diccionario
  metodologia/      decisiones (universo, diseño, recodes)
  resultados/       lo que salió de LASSO / k-medias / CART
  img/              figuras de todos (los md apuntan a ../img/)
```

Cada informe abre con un recuadro: **qué es**, **qué no es**, **tipo**, **quién lo escribe**.

Para **crear de nuevo** tablas e informes: recetario en el [README de la raíz](../README.md#cómo-crear-todo-de-nuevo). En corto:

```bash
# tablas
python scripts/tablas/build_db.py
python scripts/tablas/procesar_crs04.py
python scripts/tablas/armar_filtro_violencia.py

# resultados (LASSO primero)
python scripts/modelos/lasso_crs04.py
python scripts/modelos/perfiles_kmeans_crs04.py
python scripts/modelos/perfiles_cart_crs04.py

# descriptivos + diseño
python scripts/descriptivos/inventario_variables.py
python scripts/descriptivos/descriptivos_controles.py
python scripts/descriptivos/informe_muestral_predictores.py
python scripts/descriptivos/descriptivos_crs01.py
python scripts/descriptivos/generate_crs04_charts.py
```

No se regeneran (texto a mano): `metodologia/metodologia.md`, `descriptivos/violencia_por_cuestionario.md`, el texto de `violencia_crs04_si_no_missing.md`.

---

## Descriptivos

Cómo se ve la encuesta. No eligen el modelo.

| Informe | Para qué |
| --- | --- |
| [inventario_crs04.md](descriptivos/inventario_crs04.md) | Diccionario de preguntas CRS04 (12–17). |
| [inventario_crs01.md](descriptivos/inventario_crs01.md) | Diccionario de preguntas CRS01 (mujeres 18+). |
| [violencia_por_cuestionario.md](descriptivos/violencia_por_cuestionario.md) | Qué ítems de violencia trae cada cuestionario (CRS03/04/01/02). |
| [violencia_crs04_si_no_missing.md](descriptivos/violencia_crs04_si_no_missing.md) | Cómo se arman las 3 Y y las prevalencias 12m. |
| [descriptivos_controles.md](descriptivos/descriptivos_controles.md) | Edad, área, cuidador, hogar, cruces livianos con las Y. |
| [descriptivos_predictores_crs04.md](descriptivos/descriptivos_predictores_crs04.md) | Cada X candidata: dummy / lineal / fuera. |
| [descriptivos_crs01_vs_crs04.md](descriptivos/descriptivos_crs01_vs_crs04.md) | Qué se pregunta a ambas. No une personas. |

Controles ≠ predictores: uno describe la muestra; el otro decide el recode.

---

## Metodología

Decisiones. No son coeficientes ni clusters.

| Informe | Para qué |
| --- | --- |
| [metodologia.md](metodologia/metodologia.md) | Universo, Y, qué entra a X, leakage, lista cerrada de recodes. |
| [diseno_muestral.md](metodologia/diseno_muestral.md) | PSU, estrato, peso, estratos flacos (los números). |

---

## Resultados

Lo que salió de correr los modelos. En este orden: LASSO → k-medias y CART.

| Informe | Para qué |
| --- | --- |
| [lasso_crs04.md](resultados/lasso_crs04.md) | Qué X quedaron y con qué coeficiente. |
| [perfiles_kmeans_crs04.md](resultados/perfiles_kmeans_crs04.md) | Tipos de alumna **dentro** de sí / no violencia. |
| [perfiles_cart_crs04.md](resultados/perfiles_cart_crs04.md) | Reglas SI–ENTONCES de riesgo. |

k-medias y CART no son lo mismo: el primero agrupa personas parecidas; el segundo corta la muestra con preguntas sí/no.
