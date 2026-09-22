# Inventario CRS04 (adolescentes 12–17, mujeres)

> **Qué es este informe.** Diccionario corto de las preguntas CRS04: nombre de columna, qué pregunta el PDF y códigos.
> **Qué no es.** No hay prevalencias, cruces ni modelos. No es el catálogo de violencia (eso es [violencia_por_cuestionario.md](violencia_por_cuestionario.md)).
> **Tipo.** Descriptivo.
> **Lo escribe.** `scripts/descriptivos/inventario_variables.py` (Python → markdown; no es Rmd).

Tabla `analisis.crs04_adolescentes`, recorte `SEXO = 1`. Una fila = una pregunta. Si el cuestionario tiene ítems `_1` a `_14`, van juntos con la descripción del diccionario (no una columna por renglón). Etiquetas: diccionarios PDF CAP100/200/248/300. La misma lista en CSV (para filtrar en Excel) está en `data/tablas/inventario_crs04.csv`. No es otro informe.

Filas en el recorte: **9,608**. Columnas crudas: **1,206**. Preguntas (filas de este inventario, baterías agrupadas): **202**.

| Capítulo | Preguntas | Columnas |
| --- | --- | --- |
| ID / IE / peso | 29 | 31 |
| CAP100 alumna, hogar, identidad | 39 | 116 |
| CAP200 psic/fís casa y colegio | 116 | 492 |
| CAP248 violencia sexual | 15 | 547 |
| CAP300 actitudes y tareas | 3 | 20 |

## ID / IE / peso

| Variables | Qué pregunta | Ítems / códigos | N cols | % null |
| --- | --- | --- | --- | --- |
| `ID` | IDENTIFICACIÓN INFORMÁTICA | — | 1 | 0.0 |
| `COLEGIAL_ID` | IDENTIFICACIÓN INFORMÁTICA ALUMNO | — | 1 | 0.0 |
| `USUARIO_ID` | IDENTIFICACIÓN INFORMÁTICA ENCUESTADORA | — | 1 | 0.0 |
| `ID_MUESTRA_IE` | TIPO DE CUESTIONARIO | 4. DIRIGIDA A ADOLESCENTES DE 12 A 17 AÑOS DE EDAD | 1 | 0.0 |
| `CCDD` | CÓDIGO DE DEPARTAMENTO | — | 1 | 0.0 |
| `DEPARTAMENTO` | NOMBRE DE DEPARTAMENTO | — | 1 | 0.0 |
| `CCPP` | CÓDIGO DE PROVINCIA | — | 1 | 0.0 |
| `PROVINCIA` | NOMBRE DE PROVINCIA | — | 1 | 0.0 |
| `CCDI` | CÓDIGO DE DISTRITO | — | 1 | 0.0 |
| `DISTRITO` | DISTRITO | — | 1 | 0.0 |
| `CODCCPP` | CÓDIGO DE CENTRO POBLADO | — | 1 | 0.0 |
| `NOMCCPP` | NOMBRE DE CENTRO POBLADO | — | 1 | 0.0 |
| `AREA` | ÁREA | 1. Urbano; 2. Rural | 1 | 0.0 |
| `DIREED` | DIRECCIÓN REGIONAL DE EDUCACIÓN | — | 1 | 0.0 |
| `UNGEEDLO` | UNIDAD DE GESTIÓN EDUCATIVA LOCAL | — | 1 | 0.0 |
| `TIEDBA` | TIPO DE EDUCACIÓN BÁSICA | 1. Regular; 2. Alternativa | 1 | 0.0 |
| `NIED` | NIVEL EDUCATIVO | 1. Primaria; 2. Secundaria | 1 | 0.0 |
| `INED` | INSTITUCIÓN EDUCATIVA DE | 1. Mujeres; 2. Hombres; 3. Mixto | 1 | 0.0 |
| `TURNO_M` / `_T` / `_N` | TURNO_IE | 1. MAÑANA; 2. TARDE; 3. NOCHE | 3 | 0.0 |
| `RFINAL` | RESULTADO FINAL DE LA ENCUESTA | 1. Completa; 2. Incompleta; 3. Rechazo; 4. Visita de coordinación; 5. Otro | 1 | 0.0 |
| `C3ANIO` | AÑO DE ESTUDIO | — | 1 | 0.0 |
| `TURNO` | TURNO DE ESTUDIO | 1. Mañana; 2. Tarde; 3. Noche | 1 | 0.0 |
| `C3SECC` | SECCIÓN | — | 1 | 0.0 |
| `TOTAL_V` | TOTAL DE VARONES DE LA SECCIÓN | — | 1 | 0.0 |
| `TOTAL_M` | TOTAL DE MUJERES DE LA SECCIÓN | — | 1 | 0.0 |
| `EDAD` | EDAD DEL ALUMNO | — | 1 | 0.0 |
| `SEXO` | SEXO | 1. Mujer; 2. Hombre | 1 | 0.0 |
| `RESULTFINENTREV` | RESULTADO FINAL DE LA ENTREVISTA | 1. Completa; 2. Incompleta; 3. Informante ausente; 4. Rechazo | 1 | 0.0 |
| `FACTOR_ALUMNOS` | Factor de expansión de alumnas/os | peso | 1 | 0.0 |

## CAP100 alumna, hogar, identidad

| Variables | Qué pregunta | Ítems / códigos | N cols | % null |
| --- | --- | --- | --- | --- |
| `C3P102` (`_ANIO` / `_MES`) | 102. | 1. MES DE NACIMIENTO; 2. AÑO DE NACIMIENTO | 2 | 0.0 |
| `C3P103EDAD` | 103. ¿CUÁNTOS AÑOS TIENES? | — | 1 | 0.0 |
| `C3P104` | 104. ¿VIVES EN ESTE DISTRITO DE……………………………? | 1. Sí; 2. No | 1 | 0.0 |
| `C4P104A_1` … `C4P104A_P` (4 cols) | 104A. ¿EN QUÉ DISTRITO Y PROVINCIA VIVES? | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO; 4. PAÍS | 4 | 89.4–100.0 |
| `C4P104A_1_COD` … `C4P104A_3_COD` (3 cols) | 104A. CÓDIGO DE | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO | 3 | 89.4 |
| `C4P104B` | 104B. HACE 5 AÑOS, ¿VIVÍAS EN EL DISTRITO DE ……… ? | 1. Sí; 2. No; 3. No sabe/ No recuerda | 1 | 0.0 |
| `C4P104C_1` … `C4P104C_P` (4 cols) | 104C. ¿EN QUÉ DISTRITO Y PROVINCIA VIVÍAS HACE 5 AÑOS? | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO; 4. PAÍS | 4 | 85.8–99.6 |
| `C4P104C_1_COD` … `C4P104C_3_COD` (3 cols) | 104C. CÓDIGO DE | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO | 3 | 85.8 |
| `C4P104D` | 104D. CUANDO NACISTE, ¿VIVÍA TU MADRE EN EL DISTRITO DE ……… ? | 1. Sí; 2. No; 3. No sabe/ No recuerda | 1 | 0.0 |
| `C4P104E_1` … `C4P104E_P` (4 cols) | 104E. ¿EN QUÉ DISTRITO Y PROVINCIA VIVÍA TU MADRE? | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO; 4. PAÍS | 4 | 74.9–98.9 |
| `C4P104E_1_COD` … `C4P104E_3_COD` (3 cols) | 104E. CÓDIGO DE | 1. DISTRITO; 2. PROVINCIA; 3. DEPARTAMENTO | 3 | 74.9 |
| `C3P105` | 105. ¿EL LUGAR DONDE VIVES ES | 1. Casa?; 2. Centro de Acogida Residencial -CAR [albergue o casa hogar]? | 1 | 0.0 |
| `C3P106` | 106. ¿TIENES MAMÁ? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P110` | 110. ¿TIENES PAPÁ? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P114` (`_PERS` / `_VS`) | 114. | 1. EN TU CASA, INCLUYÉNDOTE ¿CUÁNTAS PERSONAS VIVEN CONTIGO? Nº de personas; 2. VIVO SOLA/O | 2 | 0.2 |
| `C3P115_1`–`_17` | 115. EN TU CASA, ¿CON QUIÉNES VIVES? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/s; 6. Hermano/s; 7. Abuela/s; 8. Abuelo/s; 9. Tía/s [hermana de la madre o padre]; 10. Tío/s [hermano de la madre o padre]; 11. Prima/s [hija de la/del hermana/o de la madre o padre]; 12. Primo/s [hijo de la/del hermana/o de la madre o padre]; 13. Otros parientes [consanguíneos]; 14. Otra persona; 15. Hija/o del padrastro; 16. Hija/o de la madrastra; 17. Trabajadora del hogar | 17 | 0.2 |
| `C3P116_HER` … `C3P116_NOH` (2 cols) | 116. ¿CUÁNTAS HERMANAS Y HERMANOS TIENES? | 1. Nº de hermanas/os; 2. No tiene hermanas/os | 2 | 0.2–5.2 |
| `C3P118_1`–`_15` | 118. ¿CON QUIÉN O QUIÉNES COMPARTES EL CUARTO DONDE DUERMES? | 1. Con mi madre; 2. Con mi padre; 3. Con mi madrastra; 4. Con mi padrastro; 5. Con mi/s hermana/s; 6. Con mi/s hermano/s; 7. Con mi abuela; 8. Con mi abuelo; 9. Con mi tía [hermana de la madre o padre]; 10. Con mi tío [hermano de la madre o padre]; 11. Con otra persona; 12. CON NADIE, DUERMO SOLA/O EN EL CUARTO; 13. Hija/o del padrastro; 14. Hija/o de la madrastra; 15. Trabajadora del hogar | 15 | 0.2 |
| `C3P119_1`–`_15` | 119. ¿CON QUIÉN O QUIÉNES COMPARTES LA CAMA DONDE DUERMES? | 1. Con mi madre; 2. Con mi padre; 3. Con mi madrastra; 4. Con mi padrastro; 5. Con mi/s hermana/s; 6. Con mi/s hermano/s; 7. Con mi abuela; 8. Con mi abuelo; 9. Con mi tía [hermana de la madre o padre]; 10. Con mi tío [hermano de la madre o padre]; 11. Con otra persona; 12. CON NADIE, DUERMO SOLA/O; 13. Hija/o del padrastro; 14. Hija/o de la madrastra; 15. Trabajadora del hogar | 15 | 50.8 |
| `C3P120` | 120. CUANDO ESTÁS EN TU CASA, ¿QUIÉN ES LA PERSONA QUE TE CUIDA, O ESTÁ CONTIGO LA MAYOR PARTE DEL TIEMPO? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/s; 6. Hermano/s; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Prima [hija de la/del hermana/o de la madre o padre]; 12. Primo [hijo de la/del hermana/o de la madre o padre]; 13. Otro pariente [consanguíneo] [Especifique]; 14. Otra persona [Especifique]; 15. Hija/o del padrastro; 16. Hija/o de la madrastra; 17. Trabajadora del hogar | 1 | 0.2 |
| `C3P120A` | 120A. ACTUALMENTE, ¿TU [MENCIONAR A LA PERSONA DE LA PREGUNTA 120] QUE TE CUIDA O ESTÁ LA MAYOR PARTE DEL TIEMPO CONTIGO, TRABAJA? | 1. Sí; 2. No; 3. No sabe/no responde | 1 | 0.2 |
| `C3P120B` | 120B. EN TU CASA, ¿EN ALGÚN MOMENTO TE QUEDAS SOLO/A SIN LA PRESENCIA DE UN ADULTO QUE TE CUIDE O ACOMPAÑE? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P120C` | 120C. EL MOMENTO EN QUE TE QUEDAS SOLO/A ES | 1. ¿Toda la mañana? [desde el desayuno hasta el almuerzo]; 2. ¿Toda la tarde? [desde el almuerzo hasta el lonche/cena]; 3. ¿Toda la noche? [desde la cena y mientras duermes]; 4. ¿Todo el día? [desde el desayuno hasta el lonche/cena]; 5. ¿Solo un horas? [menos de tres horas]; 6. ¿Solo unos minutos? [menos de una hora] | 1 | 41.1 |
| `C3P120D` | 120D. ESTO OCURRE | 1. ¿Todos los días de la semana?; 2. ¿Algún día de lunes a viernes, es decir todos los días del colegio?; 3. ¿Algún día de sábado o domingo?; 4. ¿Otro?; 5. No sabe/no responde | 1 | 41.1 |
| `C3P120E` | 120E. MAYORMENTE, ¿QUIÉN TE ACOMPAÑA PARA VENIR A TU COLEGIO? | 1. Madre; 2. Padre 5; 3. Madrastra; 4. Padrastro; 5. Hermana; 6. Hermano; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Prima [hija de la/ del hermana/o de la madre o padre]; 12. Primo [hijo de la/del hermana/o de la madre o padre]; 13. Otro pariente [consanguíneo]; 14. Otra persona; 15. Voy sola/o; 16. Trabajadora del hogar; 17. Va en movilidad escolar | 1 | 0.2 |
| `C3P120F` | 120F. ¿QUIÉN TE BAÑA O TE AYUDA A BAÑARTE? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana; 6. Hermano; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Prima [hija de la/del hermana/o de la madre o padre]; 12. Primo [hijo de la/del hermana/o de la madre o padre]; 13. Otro pariente [consanguíneo]; 14. Otra persona; 15. Se baña sola/o; 16. Trabajadora del hogar | 1 | 0.2 |
| `C3P120G` | 120G. EN TU CASA, ¿CUIDAS A ALGUNA PERSONA … | 1. Menor que tú?; 2. De tu edad?; 3. Mayor que tú?; 4. No cuida a nadie | 1 | 0.2 |
| `C3P120H_1`–`_7` | 120H. ¿A QUIÉN CUIDAS? | 1. Madre; 2. Padre; 3. Hermana/o mayor; 4. Hermana/o menor; 5. Abuela/o; 6. Otro pariente [consanguíneo] [Especifique]; 7. Otra persona [Especifique] | 7 | 76.6 |
| `C3P121` | 121. EN TU CASA, ¿TE HAN DEJADO SIN COMER POR UN DÍA O MÁS? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P121A_1`–`_5` | 121A. ¿POR QUÉ MOTIVO TE DEJARON SIN COMER POR UN DÍA O MÁS? | 1. Se olvidaron; 2. Fue una forma de castigo; 3. No había dinero para la comida; 4. Estaban enfermos y no podían cocinar; 5. Otro [Especifique] | 5 | 98.3 |
| `C3P122` | 122. ¿TE PIDEN O TE HAN ORDENADO NO IR AL COLEGIO PARA AYUDAR A TU MAMÁ O PAPÁ U OTRA PERSONA EN LA CASA U OTRO LUGAR? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P123` | 123. EN TU CASA, ¿HAY PELEAS O DISCUSIONES ENTRE MAMÁ O PAPÁ O ENTRE LAS PERSONAS CON QUIENES VIVES? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P124` | 124. ¿CON QUÉ FRECUENCIA OCURREN ESTAS PELEAS O DISCUSIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 50.5 |
| `C3P125` | 125. CUANDO ESTO OCURRE, ¿QUÉ HACEN PARA SOLUCIONARLO? | 1. Se evita hablar de los problemas; 2. Discuten y pelean sin resolver el problema; 3. Discuten y pelean, luego resuelven el problema; 4. Quién manda en la casa lo resuelve sin consultar a nadie; 5. Todos los integrantes de la casa conversamos para resolver el problema; 6. Conversan solo mamá y papá y resuelven el problema; 7. Otro; 8. No sabe | 1 | 50.5 |
| `C3P126` | 126. EN TU CASA, ¿TOMAN EN CUENTA LO QUE TÚ DICES O PIENSAS? | 1. Sí; 2. No | 1 | 0.2 |
| `C3P127` | 127. ¿CON QUÉ FRECUENCIA TOMAN EN CUENTA LO QUE TÚ DICES O PIENSAS | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 12.0 |
| `C3P128` | 128. HABITUALMENTE, ¿QUÉ IDIOMA O LENGUA HABLAN LAS PERSONAS QUE VIVEN EN TU CASA | 1. Castellano?; 2. Quechua?; 3. Aimara?; 4. Otra lengua nativa?; 5. Idioma extranjero?; 6. No sabe | 1 | 0.2 |
| `C4P129` | 129. POR TUS COSTUMBRES Y TUS ANTEPASADOS ¿TE SIENTES O CONSIDERAS | 1. Quechua?; 2. Aimara?; 3. Nativo o indígena de la Amazonía? [Especifique] 7; 4. Perteneciente o parte de otro pueblo indígena u originario?; 5. Negro, moreno, zambo, mulato/ pueblo Afroperuano o afrodescendiente?; 6. Blanco?; 7. Mestizo?; 8. Otro?; 9. NO SABE/ NO RESPONDE | 1 | 0.0 |
| `C4P130_1`–`_6` | 130. ¿TIENES LIMITACIONES DE FORMA PERMANENTE, PARA | 1. Moverte o caminar, para usar brazos o piernas?; 2. Ver, aun usando anteojos?; 3. Hablar o comunicarse, aun usando la lengua de señas u otro?; 4. Oír, aun usando audífonos?; 5. Entender o aprender [concentrarse o recordar]?; 6. Relacionarte con los demás, por sus pensamientos, sentimientos, emociones o conductas? | 6 | 0.0 |

## CAP200 psic/fís casa y colegio

| Variables | Qué pregunta | Ítems / códigos | N cols | % null |
| --- | --- | --- | --- | --- |
| `C3P201_1`–`_11` | 201. TE HA SUCEDIDO ALGUNA DE LAS SIGUIENTES SITUACIONES | 1. ¿Te insultan o te han insultado o te han dicho lisuras que te hacen sentir mal?; 2. ¿Te ponen o te han puesto apodos que te hacen sentir mal?; 3. ¿Te dicen o te han dicho que todo lo que haces o dices está mal?; 4. ¿Se burlan o se han burlado de ti?; 5. ¿Te dicen o te han dicho cosas que te han hecho sentir avergonzada/o o humillada/o?; 6. ¿Te amenazan o te han amenazado con golpearte o abandonarte?; 7. ¿Te amenazan o te han amenazado con matarte?; 8. ¿Te han encerrado en algún lugar?; 9. ¿Te han botado o te han amenazado con botarte de tu casa [albergue]?; 10. ¿Las personas con quienes vives, te prohíben jugar con tus amigas/os, primas/os u otras/os niñas/os de tu edad?; 11. ¿Alguna otra situación parecida? | 11 | 0.0 |
| `C3P201A_1`–`_11` | 201A. MAYORMENTE, ¿QUIÉN TE HIZO O TE HACE PASAR POR ESTA SITUACIÓN EN LA QUE [MENCIONE LA SITUACIÓN]? | 0. Ninguno; 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro 1; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela/Abuelastra; 8. Abuelo/ Abuelastro; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Sobrina [hija de la hermana/o]; 12. Sobrino [hijo de la hermana/o]; 13. Prima [hija de la hermana/o de la madre o padre]; 14. Primo [hijo de la hermana/o de la madre o padre]; 15. Cuñada; 16. Cuñado; 17. Otros ascendientes [Bisabuela/o, tatarabuela/o, tía/o abuela/o, entre otros]; 18. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 19. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de Acogida Residencial [albergue o casa hogar]; 21. Compañera/o del Centro de Acogida Residencial [albergue o casa hogar]; 22. Otra persona | 11 | 57.6–99.4 |
| `C3P201B_1`–`_11` | 201B. ¿ESTA PERSONA VIVE CONTIGO? | 1. Sí; 2. No | 11 | 57.6–99.4 |
| `C3P201C_1`–`_11` | 201C. ¿TU ......... ES UNA PERSONA ADULTA? | 1. [Persona adulta, mayor de 18 años de edad]; 2. [Persona adulta, mayor de 18 años de edad]; 3. [Persona adulta, mayor de 18 años de edad]; 4. [Persona adulta, mayor de 18 años de edad]; 5. [Persona adulta, mayor de 18 años de edad]; 6. [Persona adulta, mayor de 18 años de edad]; 7. [Persona adulta, mayor de 18 años de edad]; 8. [Persona adulta, mayor de 18 años de edad]; 9. [Persona adulta, mayor de 18 años de edad]; 10. [Persona adulta, mayor de 18 años de edad]; 11. [Persona adulta, mayor de 18 años de edad] | 11 | 87.8–99.9 |
| `C3P201D_1`–`_11` | 201D. ¿TU [MENCIONE LA PERSONA] ES COMO UN PADRE/ UNA MADRE PARA TI? | 1. Sí; 2. No | 11 | 91.5–99.9 |
| `C3P201E_1`–`_11` | 201E. ALGÚN ADULTO MÁS TE HACE PASAR POR ESTA SITUACIÓN ¿QUIÉN? | 0. Ninguno; 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela/Abuelastra; 8. Abuelo/ Abuelastro; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Sobrina [hija de la hermana/o]; 12. Sobrino [hijo de la hermana/o]; 13. Prima [hija de la hermana/o de la madre o padre]; 14. Primo [hijo de la hermana/o de la madre o padre]; 15. Cuñada; 16. Cuñado; 17. Otros ascendientes [Bisabuela/o, tatarabuela/o, tía/o abuela/o, entre otros]; 18. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 19. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de Acogida Residencial [albergue o casa hogar]; 21. Compañera/o del Centro de Acogida Residencial [albergue o casa hogar]; 22. Otra persona | 11 | 90.6–100.0 |
| `C3P201F_1`–`_11` | 201F. ¿TU [MENCIONE LA PERSONA DE LA PREGUNTA 201E.] ES COMO UN PADRE/ UNA MADRE PARA TI? | 1. Sí; 2. No | 11 | 98.2–100.0 |
| `C3P202` | 202. ¿QUÉ EDAD TENÍAS CUANDO TE OCURRIERON ESTAS SITUACIONES POR PRIMERA VEZ? | — | 1 | 37.5 |
| `C3P203` | 203. EN LAS SITUACIONES QUE TE HICIERON SENTIR MAL, ¿TE HA OCURRIDO EN LOS ÚLTIMOS 12 MESES, DE ……… A ………? | 1. Sí; 2. No | 1 | 37.5 |
| `C3P204` | 204. ¿CON QUÉ FRECUENCIA TE HAN OCURRIDO ESTAS SITUACIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 61.6 |
| `C3P205_1`–`_7` | 205. TE HA SUCEDIDO ALGUNA DE LAS SITUACIONES SIGUIENTES | 1. ¿Te jalan o te han jalado el cabello u orejas?; 2. ¿Te dan o te han dado cachetadas o nalgadas?; 3. ¿Te han pateado, mordido o te han dado puñetazos?; 4. ¿Te han golpeado o han tratado de golpearte con objetos como: correa, soga, palo, madera u otros?; 5. ¿Te han quemado en alguna parte de tu cuerpo?; 6. ¿Te han atacado o han tratado de atacarte con cuchillo, armas u otros?; 7. ¿Alguna otra situación parecida? | 7 | 0.0 |
| `C3P205A_1`–`_7` | 205A. MAYORMENTE, ¿QUIÉN TE HIZO O TE HACE PASAR POR ESTA SITUACIÓN EN LA QUE [MENCIONE SITUACIÓN]? | 0. Ninguno; 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela/Abuelastra; 8. Abuelo/ Abuelastro; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Sobrina [hija de la hermana/o]; 12. Sobrino [hijo de la hermana/o]; 13. Prima [hija de la hermana/o de la madre o padre]; 14. Primo [hijo de la hermana/o de la madre o padre]; 15. Cuñada; 16. Cuñado; 17. Otros ascendientes [Bisabuela/o, tatarabuela/o, tía/o abuela/o, entre otros]; 18. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 19. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de Acogida Residencial [albergue o casa hogar]; 21. Compañera/o del Centro de Acogida Residencial [albergue o casa hogar]; 22. Otra persona | 7 | 58.1–99.2 |
| `C3P205B_1`–`_7` | 205B. ¿ESTA PERSONA VIVE CONTIGO? | 1. Sí; 2. No | 7 | 58.1–99.2 |
| `C3P205C_1`–`_7` | 205C. ¿TU ......... ES UNA PERSONA ADULTA? | 1. [Persona adulta, mayor de 18 años de edad]; 2. [Persona adulta, mayor de 18 años de edad]; 3. [Persona adulta, mayor de 18 años de edad]; 4. [Persona adulta, mayor de 18 años de edad]; 5. [Persona adulta, mayor de 18 años de edad]; 6. [Persona adulta, mayor de 18 años de edad]; 7. [Persona adulta, mayor de 18 años de edad] | 7 | 95.3–99.8 |
| `C3P205D_1`–`_7` | 205D. ¿TU…[MENCIONE LA PERSONA] ES COMO UN PADRE/UNA MADRE PARA TI? | 1. Sí; 2. No | 7 | 96.8–99.9 |
| `C3P205E_1`–`_7` | 205E. ALGÚN ADULTO MÁS TE HACE PASAR POR ESTA SITUACIÓN ¿QUIÉN? | 0. Ninguno; 1. Madre; 2. Padre 13; 3. Madrastra; 4. Padrastro; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela/Abuelastra; 8. Abuelo/ Abuelastro; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Sobrina [hija de la hermana/o]; 12. Sobrino [hijo de la hermana/o]; 13. Prima [hija de la hermana/o de la madre o padre]; 14. Primo [hijo de la hermana/o de la madre o padre]; 15. Cuñada; 16. Cuñado; 17. Otros ascendientes [Bisabuela/o, tatarabuela/o, tía/o abuela/o, entre otros]; 18. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 19. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de Acogida Residencial [albergue o casa hogar]; 21. Compañera/o del Centro de Acogida Residencial [albergue o casa hogar]; 22. Otra persona | 7 | 96.5–99.9 |
| `C3P205F_1`–`_7` | 205F. ¿TU [MENCIONE LA PERSONA DE LA PREGUNTA 205E] ES COMO UN PADRE/ UNA MADRE PARA TI? | 1. Sí; 2. No | 7 | 99.4–100.0 |
| `C3P206` | 206. ¿QUÉ EDAD TENÍAS CUANDO TE OCURRIERON ESTAS SITUACIONES POR PRIMERA VEZ? | — | 1 | 47.4 |
| `C3P207` | 207. EN LAS SITUACIONES QUE TE HICIERON DAÑO, ¿TE HA OCURRIDO EN LOS ÚLTIMOS 12 MESES, DE …..A….? | 1. Sí; 2. No | 1 | 47.4 |
| `C3P208` | 208. ¿CON QUÉ FRECUENCIA TE HAN OCURRIDO ESTAS SITUACIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 79.0 |
| `C3P209` | 209. CUANDO TE HICIERON SENTIR MAL CON INSULTOS O GOLPES ¿ACUDISTE A ALGUNA PERSONA CERCANA PARA CONTARLE LO QUE TE SUCEDIÓ Y PEDIRLE AYUDA? | 1. Sí; 2. No; 3. No sabe | 1 | 28.3 |
| `C3P210_1`–`_21` | 210. ¿A QUIÉN LE PEDISTE AYUDA? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Otro pariente [consanguíneo]; 12. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 13. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 14. Compañero/a del Centro de Acogida Residencial [albergue o casa hogar]; 15. Director/a del colegio; 16. Profesora; 17. Profesor; 18. Auxiliar de educación; 19. Amiga; 20. Amigo; 21. Otra persona | 21 | 71.2 |
| `C3P211` | 211. ESTA/S PERSONA/S, ¿TE AYUDÓ / AYUDARON? | 1. Sí; 2. No; 3. No sabe | 1 | 71.2 |
| `C3P212_1`–`_6` | 212. ¿CÓMO TE AYUDÓ / AYUDARON ESTA/S PERSONA/S? | 1. Me consolaron; 2. Me aconsejaron [Que me porte bien/ que avise cuando me agreden, entre otros]; 3. Conversaron con mi madre/padre/familiares; 4. Llamó/Llamaron la atención a quien me agredió; 5. Respondió con una agresión a la persona que me agredió; 6. Otro | 6 | 72.3 |
| `C3P213` | 213. ¿POR QUÉ CREES QUE NO TE AYUDÓ /AYUDARON ? | 1. No me creyeron; 2. Porque soy malcriada/o, desobediente; 3. Consideran que es normal; 4. No me hicieron caso/están ocupadas/os, sin tiempo; 5. No supieron cómo ayudarme; 6. Otro; 7. No sabe | 1 | 98.9 |
| `C3P214` | 214. EN LOS ÚLTIMOS 12 MESES, DE ......... A ........, CUANDO TE HICIERON SENTIR MAL CON INSULTOS O GOLPES ¿FUISTE O TE LLEVARON A ALGUNA INSTITUCIÓN PARA BUSCAR AYUDA? | 1. Sí; 2. No | 1 | 28.3 |
| `C3P215_1`–`_11` | 215. ¿A QUÉ INSTITUCIÓN FUISTE O TE LLEVARON? | 1. Comisaría; 2. Juzgado/Juez de Paz; 3. Fiscalía/Ministerio Público; 4. Defensoría Municipal de la Niña, Niño y del Adolescente [DEMUNA]; 5. Unidad de Protección Especial [UPE]; 6. Centro Emergencia Mujer [CEM]; 7. Ministerio de Educación/Dirección Regional de Educación [DRE]/Unidad de Gestión Educativa Local [UGEL]; 8. Establecimiento de salud [Hospital, centro de salud, posta médica]; 9. Gobernación; 10. Otra institución; 11. No sabe | 11 | 97.1 |
| `C4P216` | 216. LA/S INSTITUCIÓN/ES A LA/S QUE FUISTE O TE LLEVARON, ¿TE AYUDÓ / AYUDARON? | 1. Sí; 2. No; 3. No sabe | 1 | 97.1 |
| `C4P217_1`–`_4` | 217. ¿CÓMO TE AYUDÓ/ AYUDARON ESTA/S INSTITUCIÓN/ES? | 1. Conversaron con mi madre/padres/familiares; 2. Asistí a terapias; 3. Llamó/Llamaron la atención a quien le agredió; 4. Otro | 4 | 97.6 |
| `C3P216_1`–`_13` | 218. ¿POR QUÉ RAZONES CREES TÚ QUE LOS ADOLESCENTES SON MALTRATADOS? | 1. Porque desobedecen; 2. Porque sacan malas notas; 3. Porque hacen cosas que les prohibieron; 4. Porque faltan el respeto a la madre/ al padre; 5. Porque las/los madres/ padres están estresados o están cansados; 6. Porque las/los madres/ padres no los comprenden/no los respetan/no tienen paciencia; 7. Porque no los quieren o no les importan; 8. Porque las/los madres/ padres también fueron maltratados; 9. Porque las/los madres/ padres tienen problemas [familiares, emocionales, económicos, entre otros]; 10. Porque las/los madres/ padres se emborracharon /drogaron; 11. No encuentro ninguna razón; 12. Otra razón; 13. No sabe | 13 | 0.0 |
| `C3P216A_1`–`_6` | 218A. ALGUNA VEZ | 1. ¿Te has hecho daño en alguna parte de tu cuerpo con algún objeto?; 2. ¿Has tomado alguna sustancia con intención de hacerte daño [pastillas, lejía, ácido, veneno, entre otros?; 3. ¿Has dormido alguna noche fuera de tu casa / del Centro de Acogida Residencial [albergue o casa hogar] sin el permiso de tu mamá, papá o de la persona que te cuida?; 4. ¿Te fuiste de tu casa / del Centro de Acogida Residencial [albergue o casa hogar] por más de un día sin que nadie lo sepa?; 5. ¿Consumes o has consumido licor?; 6. ¿Otra situación parecida? | 6 | 0.0 |
| `C3P216A_1C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 82.2 |
| `C3P216A_2C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 94.0 |
| `C3P216A_3C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 96.6 |
| `C3P216A_4C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 97.4 |
| `C3P216A_5C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 82.3 |
| `C3P216A_6C` | 218A. ¿Esto ocurrió en los últimos 12 meses, de ........ a ........? | 1. Sí; 2. No | 1 | 99.3 |
| `C3P216B_1`–`_2` | 218B. TE ESTA PASANDO O TE PASÓ ALGUNAS DE LAS SIGUIENTES SITUACIONES | 1. ¿Tienes miedo que alguna persona que no vive contigo entre a tu casa / al Centro de Acogida Residencial [albergue o casa hogar] para hacerte daño?; 2. ¿No puedes dormir por miedo a que te hagan daño? | 2 | 0.0 |
| `C3P216B_1C` | 218B. ¿Con que frecuencia te ocurre esta situación | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe 24 | 1 | 47.5 |
| `C3P216B_2C` | 218B. ¿Con que frecuencia te ocurre esta situación | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 86.4 |
| `C3P216C_1`–`_5` | 218C. TU MAMÁ, TU PAPÁ O LA PERSONA ADULTA QUE TE CUIDA / ALGUNA PERSONA ADULTA DEL CENTRO DE ACOGIDA RESIDENCIAL [ALBERGUE O CASA HOGAR] TE HA PEDIDO QUE | 1. ¿Le quites o robes a una persona algo que le pertenece?; 2. ¿Pruebes o fumes cigarrillos o algo parecido?; 3. ¿Vendas cosas que hacen o pueden hacer daño a las personas?; 4. ¿Lleves cosas que hacen daño de un lugar a otro que tú no quieres hacer?; 5. ¿Ir a lugares en los que te sientes mal o que te pueden hacer daño? | 5 | 0.0 |
| `C3P216C_1C` | 218C. ¿Esto ocurrió en los últimos 12 meses, de .......... a ..........? | 1. Sí; 2. No | 1 | 99.7 |
| `C3P216C_2C` | 218C. ¿Esto ocurrió en los últimos 12 meses, de .......... a ..........? | 1. Sí; 2. No | 1 | 99.4 |
| `C3P216C_3C` | 218C. ¿Esto ocurrió en los últimos 12 meses, de .......... a ..........? | 1. Sí; 2. No | 1 | 99.9 |
| `C3P216C_4C` | 218C. ¿Esto ocurrió en los últimos 12 meses, de .......... a ..........? | 1. Sí; 2. No | 1 | 99.9 |
| `C3P216C_5C` | 218C. ¿Esto ocurrió en los últimos 12 meses, de .......... a ..........? | 1. Sí; 2. No | 1 | 98.2 |
| `C3P217` | 219. ACTUALMENTE ¿CÓMO TE SIENTES EN TU COLEGIO? | 1. Me siento muy bien; 2. Me siento bien; 3. Me siento mal; 4. Me siento muy mal; 5. No sabe 25 | 1 | 0.0 |
| `C3P218` | 220. EL AÑO PASADO[2023] ¿HAS JALADO O DESAPROBADO ALGÚN CURSO? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P219` | 221. ALGUNA VEZ ¿HAS REPETIDO DE GRADO? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P220` | 222. ALGUNA VEZ ¿TE EXPULSARON DEL COLEGIO? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P221` | 223. ¿TUS MEJORES AMIGOS O AMIGAS ESTUDIAN EN ESTE COLEGIO? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P222` | 224. ¿HAY LUGARES DENTRO DE TU COLEGIO, POR DONDE NO VAS POR MIEDO A QUE ALGUIEN TE HAGA DAÑO? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P223_1`–`_14` | 225. TE HA SUCEDIDO ALGUNA DE LAS SIGUIENTES SITUACIONES | 1. ¿Te tratan o te han tratado con insultos, burlas o desprecio?; 2. ¿Te ponen o te han puesto apodos o chapas que te hacen sentir mal?; 3. ¿Te dicen o te han dicho que tus amigas/os, hermanas/os u otras/os niñas/os son mejores que tú?; 4. ¿Te dicen o te han dicho que todo lo que tú haces o dices está mal?; 5. ¿Te dejan o te han dejado de hablar, te rechazan o no te dejan jugar con ellos o ser parte de su grupo haciéndote sentir mal?; 6. ¿Han roto o han tratado de romper tus cosas?; 7. ¿Te han escondido o te esconden tus cosas haciéndote sentir mal?; 8. ¿Hablan o han hablado chismes sobre ti que te han hecho sentir mal?; 9. ¿Han colgado en internet o Facebook fotos o videos tuyos que te avergüenzan?; 10. ¿Has recibido mensajes de texto ofensivos en forma virtual o escritos?; 11. ¿Te encierran o te han encerrado en algún lugar [baño, salones de clase, entre otros]?; 12. ¿Te amenazan o te han amenazado con pegarte o hacerte algún daño físico?; 13. ¿Te amenazan o te han amenazado con matarte?; 14. ¿Alguna otra situación parecida? | 14 | 0.0 |
| `C3P223A_1`–`_14` | 225A. ¿QUIEN TE HIZO PASAR POR ESTA SITUACIÓN EN LA QUE [MENCIONE SITUACIÓN] ES TU COMPAÑERO O COMPAÑERA DE SALÓN? | 1. Sí; 2. No | 14 | 59.0–99.7 |
| `C3P223B_1`–`_14` | 225B. ¿ESTE/A COMPAÑERO O COMPAÑERA ES | 1. Mayor que tú?; 2. De tu misma edad?; 3. Menor que tú? | 14 | 67.5–99.8 |
| `C3P223C_1`–`_14` | 225C. ¿OTRO ALUMNO O ALUMNA DEL COLEGIO QUE NO ES DE TU SALÓN TE HIZO PASAR POR ESTA SITUACIÓN? | 1. Sí; 2. No | 14 | 59.0–99.7 |
| `C3P223D_1`–`_14` | 225D. ¿ESTE/A ALUMNO O ALUMNA ES | 1. Mayor que tú?; 2. De tu misma edad?; 3. Menor que tú? | 14 | 85.3–99.9 |
| `C3P223E_1`–`_14` | 225E. ¿OTRO ALUMNO O ALUMNA DE OTRO COLEGIO TE HIZO PASAR POR ESTA SITUACIÓN? | 1. Sí; 2. No | 14 | 59.0–99.7 |
| `C3P224` | 226. ¿QUÉ EDAD TENÍAS CUANDO TE OCURRIERON ESTAS SITUACIONES POR PRIMERA VEZ? | — | 1 | 35.3 |
| `C3P225` | 227. EN LAS SITUACIONES QUE TE HICIERON SENTIR MAL, ¿TE HA OCURRIDO EN LOS ÚLTIMOS 12 MESES, DE….A…? | 1. Sí; 2. No | 1 | 35.3 |
| `C3P226` | 228. ¿CON QUÉ FRECUENCIA TE HAN OCURRIDO ESTAS SITUACIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 54.8 |
| `C3P227_1`–`_10` | 229. TE HA SUCEDIDO ALGUNA DE LAS SIGUIENTES SITUACIONES | 1. ¿Te jalan o te han jalado el cabello u orejas?; 2. ¿Te dan o te han dado cachetadas, cocachos, pellizcos o nalgadas?; 3. ¿Te dan o te han dado patadas, puñetazos, codazos o rodillazos?; 4. ¿Te golpean o te han golpeado con correas, sogas, palos, leñas, maderas, bastones, piedras u otros objetos?; 5. ¿Te han ahorcado o han intentado asfixiarte?; 6. ¿Te han hecho o te hacen daño con el lápiz, lapicero o regla?; 7. ¿Te han quemado o te queman en alguna parte de tu cuerpo?; 8. ¿Te han atacado con cuchillo, navaja, verduguillo u otros objetos filudos?; 9. ¿Te han atacado con una pistola?; 10. ¿Alguna otra situación parecida? | 10 | 0.0 |
| `C3P227A_1`–`_10` | 229A. ¿QUIEN TE HIZO PASAR POR ESTA SITUACIÓN EN LA QUE [MENCIONE...SITUACIÓN] ES TU COMPAÑERA O COMPAÑERO DE SALÓN? | 1. Sí; 2. No | 10 | 92.8–100.0 |
| `C3P227B_1`–`_10` | 229B. ¿ESTE/A COMPAÑERO O COMPAÑERA ES | 1. Mayor que tú?; 2. De tu misma edad?; 3. Menor que tú? | 10 | 93.7–100.0 |
| `C3P227C_1`–`_10` | 229C. ¿OTRO ALUMNO O ALUMNA DEL COLEGIO QUE NO ES DE TU SALÓN TE HIZO PASAR POR ESTA SITUACIÓN? | 1. Sí; 2. No | 10 | 92.8–100.0 |
| `C3P227D_1`–`_10` | 229D. ¿ESTE/A ALUMNO O ALUMNA ES | 1. Mayor que tú?; 2. De tu misma edad?; 3. Menor que tú? | 10 | 98.9–100.0 |
| `C3P227E_1`–`_10` | 229E. ¿OTRO ALUMNO O ALUMNA DE OTRO COLEGIO TE HIZO PASAR POR ESTA SITUACIÓN? | 1. Sí; 2. No | 10 | 92.8–100.0 |
| `C3P228` | 230. ¿QUÉ EDAD TENÍAS CUANDO TE OCURRIERON ESTAS SITUACIONES POR PRIMERA VEZ? | — | 1 | 83.8 |
| `C3P229` | 231. EN LAS SITUACIONES QUE JUEGAN O SE PELEAN A GOLPES, ¿TE HA OCURRIDO EN LOS ÚLTIMOS 12 MESES, DE….A…? | 1. Sí; 2. No | 1 | 83.8 |
| `C3P230` | 232. ¿CON QUÉ FRECUENCIA TE HAN OCURRIDO ESTAS SITUACIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 89.0 |
| `C3P231_1`–`_6` | 233. ¿DÓNDE SUCEDIERON ESTAS SITUACIONES? | 1. Salón de clase; 2. Patio; 3. Baño; 4. Pasillos/escalera; 5. Otro lugar; 6. Fuera del perímetro del colegio | 6 | 34.2 |
| `C3P231_1E1` | 233. ¿ESTO OCURRIÓ DURANTE……LA HORA DE ENTRADA DEL COLEGIO? | — | 1 | 46.7 |
| `C3P231_1E2` | 233. ¿ESTO OCURRIÓ DURANTE…… EL HORARIO DE CLASES? | — | 1 | 46.7 |
| `C3P231_1E3` | 233. ¿ESTO OCURRIÓ DURANTE…… EL RECREO? | — | 1 | 46.7 |
| `C3P231_1E4` | 233. ¿ESTO OCURRIÓ DURANTE… ... A LA HORA DE SALIDA DEL COLEGIO? | — | 1 | 46.7 |
| `C3P231_2E1` | 233. ¿ESTO OCURRIÓ DURANTE…… LA HORA DE ENTRADA DEL COLEGIO? | — | 1 | 81.1 |
| `C3P231_2E2` | 233. ¿ESTO OCURRIÓ DURANTE…… EL HORARIO DE CLASES? | — | 1 | 81.1 |
| `C3P231_2E3` | 233. ¿ESTO OCURRIÓ DURANTE…… EL RECREO? | — | 1 | 81.1 |
| `C3P231_2E4` | 233. ¿ESTO OCURRIÓ DURANTE… ... A LA HORA DE SALIDA DEL COLEGIO? | — | 1 | 81.1 |
| `C3P231_3E1` | 233. ¿ESTO OCURRIÓ DURANTE……LA HORA DE ENTRADA DEL COLEGIO? | — | 1 | 97.2 |
| `C3P231_3E2` | 233. ¿ESTO OCURRIÓ DURANTE…… EL HORARIO DE CLASES? | — | 1 | 97.2 |
| `C3P231_3E3` | 233. ¿ESTO OCURRIÓ DURANTE…… EL RECREO? | — | 1 | 97.2 |
| `C3P231_3E4` | 233. ¿ESTO OCURRIÓ DURANTE… ... A LA HORA DE SALIDA DEL COLEGIO? | — | 1 | 97.2 |
| `C3P231_4E1` | 233. ¿ESTO OCURRIÓ DURANTE…… LA HORA DE ENTRADA DEL COLEGIO? | — | 1 | 94.6 |
| `C3P231_4E2` | 233. ¿ESTO OCURRIÓ DURANTE…… EL HORARIO DE CLASES? | — | 1 | 94.6 |
| `C3P231_4E3` | 233. ¿ESTO OCURRIÓ DURANTE…… EL RECREO? | — | 1 | 94.6 |
| `C3P231_4E4` | 233. ¿ESTO OCURRIÓ DURANTE… ... A LA HORA DE SALIDA DEL COLEGIO? | — | 1 | 94.6 |
| `C3P231_5E1` | 233. ¿ESTO OCURRIÓ DURANTE…… LA HORA DE ENTRADA DEL COLEGIO? | — | 1 | 99.6 |
| `C3P231_5E2` | 233. ¿ESTO OCURRIÓ DURANTE…… EL HORARIO DE CLASES? | — | 1 | 99.6 |
| `C3P231_5E3` | 233. ¿ESTO OCURRIÓ DURANTE…… EL RECREO? | — | 1 | 99.6 |
| `C3P231_5E4` | 233. ¿ESTO OCURRIÓ DURANTE… ... A LA HORA DE SALIDA DEL COLEGIO? | — | 1 | 99.6 |
| `C3P232_1`–`_14` | 234. ¿POR QUÉ CREES QUE LOS ALUMNOS O ALUMNAS DE TU COLEGIO O DE OTROS COLEGIOS TE TRATAN ASÍ? | 1. Por la apariencia física [color de la piel, estatura, peso, entre otros]; 2. Por ser provinciana/o; 3. Por tener plata; 4. Por no tener plata; 5. Por discapacidad [uso de lentes, tartamudez, sordera, cojera, entre otros]; 6. Por sacar buenas notas [exámenes, trabajos, entre otros]; 7. Por tener malas notas; 8. Por envidia [por destacar en algo o por las cosas que tengo]; 9.Por ser muy inquieta/o / provocador/a; 10. Por ser muy callada/o o tímida/o; 11. Porque creen que soy gay/lesbiana; 12. Sin motivo alguno [solo por molestarme o burlarse de mí]; 13. Otro; 14. No sabe | 14 | 34.2 |
| `C3P233_1`–`_3` | 235. ALGUNA VEZ, ESTANDO EN TU SALÓN, DENTRO O FUERA DE TU COLEGIO, O CUANDO ESTÁS CAMINO A TU COLEGIO O DE REGRESO A TU CASA | 1. ¿Has golpeado a algún compañero o compañera de tu salón u otro/a alumno/a de tu colegio?; 2. ¿Has insultado o amenazado a alguna compañera o compañero de tu salón u otro/a alumno/a de tu colegio?; 3. ¿Has sacado de tu grupo o ignorado a algún compañero o compañera de tu salón u otro/a alumno o alumna de tu colegio? | 3 | 0.0 |
| `C3P233_1A` | 235. ALGUNA VEZ, ESTANDO EN TU SALÓN, DENTRO O FUERA DE TU COLEGIO, O CUANDO ESTÁS CAMINO A TU COLEGIO O DE REGRESO A TU CASA: 1A. ¿Has golpeado a algún alumno o alumna de otro colegio? | 1. Sí; 2. No; 3. No sabe | 1 | 0.0 |
| `C3P233_2A` | 235. ALGUNA VEZ, ESTANDO EN TU SALÓN, DENTRO O FUERA DE TU COLEGIO, O CUANDO ESTÁS CAMINO A TU COLEGIO O DE REGRESO A TU CASA: 2A. ¿Has insultado o amenazado a algún alumno o alumna de otro colegio? | 1. Sí; 2. No; 3. No sabe 36 | 1 | 0.0 |
| `C3P233A` | 235A. ¿ESTO OCURRIÓ EN LOS ÚLTIMOS 12 MESES, DE …….. A …….? | 1. Sí; 2. No | 1 | 77.6 |
| `C3P234` | 236. ¿ALGUNA VEZ HAS VISTO QUE FUE INSULTADO, AMENAZADO O GOLPEADO, ALGÚN COMPAÑERO O COMPAÑERA, POR ALUMNOS O ALUMNAS DE TU COLEGIO O DE OTROS COLEGIOS? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P235_1`–`_7` | 237. ¿QUÉ HICISTE CUANDO LE OCURRIÓ ESA SITUACIÓN A TU COMPAÑERO O COMPAÑERA? | 1. Defendí y ayudé al/a la compañero/a que agredían; 2. Aconsejé y conversé para que no sigan agrediéndose; 3. Me dio miedo/me puse triste; 4. Avisé al/a la Director/a / profesor/a u otra persona adulta del colegio; 5. Participé también en la agresión; 6. Otro; 7. No hice nada | 7 | 47.0 |
| `C3P236` | 238. CUANDO TE HICIERON SENTIR MAL EN TU COLEGIO, CON INSULTOS O GOLPES ¿ACUDISTE A ALGUNA PERSONA CERCANA PARA CONTARLE LO QUE TE SUCEDIÓ Y PEDIRLE AYUDA? | 1. Sí; 2. No; 3. No sabe | 1 | 34.2 |
| `C3P237_1`–`_21` | 239. ¿A QUIÉN LE PEDISTE AYUDA? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/ Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Otro pariente [consanguíneo]; 12. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 13. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 14. Compañero/a del Centro de Acogida Residencial [albergue o casa hogar]; 15. Director/a del colegio; 16. 16 Profesora; 17. Profesor; 18. Auxiliar de educación; 19. Amiga; 20. Amigo; 21. Otra persona | 21 | 64.1 |
| `C3P238` | 240. ESTA/S PERSONA/S ¿TE AYUDÓ/ AYUDARON? | 1. Sí; 2. No; 3. No sabe | 1 | 64.1 |
| `C3P239_1`–`_8` | 241. ¿CÓMO TE AYUDÓ/ AYUDARON ESTA/S PERSONA/S? | 1. Me consolaron; 2. Avisaron o fueron hablar con la/el profesora/profesor; 3. Conversaron con la persona agresora [fuera o dentro del colegio]; 4. Llamó/llamaron la atención a la persona agresora; 5. Hablaron con el/la Director/a del colegio; 6. Fueron a hablar con los padres de la persona agresora; 7. Me aconsejaron que no haga caso/que los ignore/que me defienda; 8. Otro | 8 | 65.6 |
| `C3P240` | 242. ¿POR QUÉ CREES QUE NO TE AYUDÓ/ AYUDARON? | 1. No me creyeron; 2. Porque pensaron que no era importante; 3. Me dijeron que no les corresponde ayudarme; 4. No supieron cómo ayudarme; 5. Porque no tenían tiempo; 6. Otro; 7. No sabe | 1 | 98.6 |
| `C3P241` | 243. EN LOS ÚLTIMOS 12 MESES, DE …….. A …….., CUANDO TE HICIERON SENTIR MAL CON INSULTOS O GOLPES, ¿FUISTE O TE LLEVARON A ALGUNA INSTITUCIÓN PARA BUSCAR AYUDA? | 1. Sí; 2. No; 3. No sabe | 1 | 34.2 |
| `C3P242_1`–`_12` | 244. ¿A QUÉ INSTITUCIÓN FUISTE O TE LLEVARON? | 1. Comisaría; 2. Juzgado/Juez de Paz; 3. Fiscalía/Ministerio Público; 4. Defensoría Municipal de la Niña, Niño y del Adolescente [DEMUNA]; 5. Unidad de Protección Especial [UPE]; 6. Centro Emergencia Mujer [CEM]; 7. Ministerio de Educación/Dirección Regional de Educación [DRE]/Unidad de Gestión Educativa Local [UGEL]; 8. A la oficina de la Dirección de la institución educativa; 9. Establecimiento de salud [Hospital, centro de salud, posta medica]; 10. Gobernación; 11. Otra institución; 12. No sabe | 12 | 98.2 |
| `C4P245` | 245. LA/S INSTITUCIÓN/ES A LA/S QUE ACUDISTE PARA CONTARLE/S LO QUE TE PASA O PASÓ ¿TE AYUDÓ /AYUDARON? | 1. Sí; 2. No; 3. No sabe | 1 | 98.2 |
| `C4P246_1`–`_4` | 246. ¿CÓMO TE AYUDÓ / AYUDARON ESTA/S INSTITUCIÓN/ES? | 1. Conversaron con mis padres/familiares; 2. Asistí a terapias; 3. Llamó/Llamaron la atención a quien me agredió; 4. Otro | 4 | 98.5 |
| `C3P243_1`–`_6` | 247. DEBIDO A LOS GOLPES O MALTRATO QUE RECIBISTE EN TU CASA/ EL CENTRO DE ACOGIDA RESIDENCIAL [ALBERGUE O CASA HOGAR] O COLEGIO | 1. ¿Tienes o has tenido moretones o hinchazones?; 2. ¿Tienes o has tenido heridas o cicatrices en alguna parte de tu cuerpo?; 3. ¿Tienes fracturas en la cabeza, huesos o tienes dientes rotos?; 4. ¿Has tenido sangrado?; 5. ¿Tienes o has tenido quemaduras?; 6. ¿Otra consecuencia? | 6 | 44.0 |
| `C3P243_T1` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 79.8 |
| `C3P243_T2` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 92.5 |
| `C3P243_T3` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 99.3 |
| `C3P243_T4` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 93.8 |
| `C3P243_T5` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 99.2 |
| `C3P243_T6` | 247. POR ESTO, ¿TUVISTE QUE IR AL MÉDICO, HOSPITAL O ALGÚN ESTABLECIMIENTO DE SALUD? | 1. Sí; 2. No | 1 | 98.9 |
| `C3P246` | 263. ¿CONOCES O HAS ESCUCHADO DE LA DEMUNA [DEFENSORÍA MUNICIPAL DE LA NIÑA, NIÑO Y ADOLESCENTE]? | 1. Sí; 2. No | 1 | 0.0 |
| `C3P247` | 264. ALGUNA VEZ, ¿HAS IDO A UNA DEMUNA? | 1. Sí; 2. No | 1 | 50.9 |

## CAP248 violencia sexual

| Variables | Qué pregunta | Ítems / códigos | N cols | % null |
| --- | --- | --- | --- | --- |
| `C4P248_1`–`_16` | 248. | 1. ¿Te miran o te han mirado tus partes íntimas que te han hecho sentir mal o incomoda/o?; 2. ¿Alguien te hace o te hizo comentarios o bromas de tipo sexual?; 3. ¿Te han obligado a ver personas desnudas o teniendo relaciones sexuales en revistas, fotos, figuras o por internet?; 4. ¿Alguien ha tratado o te ha quitado la ropa en contra de tu voluntad?; 5. ¿Te obligan o te han obligado a realizar tocamientos o manoseos al cuerpo de otra persona?; 6. ¿Eres o has sido víctima de tocamientos incómodos en alguna parte de tu cuerpo?; 7. ¿Alguien se ha masturbado delante de ti?; 8. ¿Alguien te obliga o te ha obligado a masturbarte?; 9. ¿Alguien te muestra o te ha mostrado sus genitales?; 10. ¿Te amenazan o has sido amenazada/o para tener relaciones sexuales?; 11. ¿Te han obligado o te obligan a tener relaciones sexuales?; 12. ¿Otra situación parecida?; 13. ¿Alguien se ha ganado tu confianza y luegoha intentado aprovecharse sexualmente de ti?; 14. ¿Te han llamado o enviado mensajes privados de tipo sexual o subidos de tono?; 15. ¿Alguién te ha amenazado con publicar fotos y/o videos tuyos mostrando tus partes íntimas?; 16. ¿Han compartido fotos y/o videos mostrando tus partes íntimas sin tu permiso o sin que tú quieras? | 16 | 0.0 |
| `C4P248A_*_*` (448 cols) | 248A. ¿QUIÉN O QUIÉNES TE HICIERON PASAR POR ESTA/S SITUACIONES? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/Hermanastra; 6. Hermano/Hermanastro; 7. Abuela/Abuelastra; 8. Abuelo/Abuelastro; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Sobrina [hija de la hermana/o]; 12. Sobrino [hijo de la hermana/o]; 13. Prima [hija de la hermana/o de la madre o padre]; 14. Primo [hijo de la hermana/o de la madre o padre]; 15. Cuñada; 16. Cuñado; 17. Otros ascendientes [Bisabuela/o, tatarabuela/o, tía/o abuela/o, entre otros]; 18. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 19. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de Acogida Residencial [albergue o casa hogar]; 21. Compañera/o del Centro de Acogida Residencial [albergue o casa hogar]; 22. Director/a del colegio; 23. Profesor/a del colegio; 24. Otra persona adulta del colegio; 25. Otra persona; 26. Pareja [novio/a, enamorado/a o pareja sexual] o Expareja [exnovio, exenamorado o expareja sexual]; 27. Algún/a alumno/a del colegio; 28. Algún alumno/a de otro colegio [cerca del colegio o en el trayecto]; 18. Director/a del Centro de cogida Residencial [albergue o casa hogar]; 20. Otra persona del Centro de cogida Residencial [albergue o casa hogar] | 448 | 83.6–100.0 |
| `C4P248B_1`–`_16` | 248B. ¿QUÉ EDAD TENÍAS CUANDO SUCEDIÓ POR PRIMERA VEZ? | 1. Edad; 2. Edad; 3. Edad; 4. Edad; 5. Edad; 6. Edad; 7. Edad; 8. Edad; 9. Edad; 10. Edad; 11. Edad; 12. Edad; 13. Edad; 14. Edad; 15. Edad; 16. Edad | 16 | 83.6–100.0 |
| `C4P248C_1`–`_16` | 248C. EN LOS ÚLTIMOS 12 MESES, DE …… A ……. ¿TE HA OCURRIDO ESTA SITUACIÓN? | 1. Sí; 2. No | 16 | 83.6–100.0 |
| `C4P248_O_12` | 248. Otro [Especifique] | — | 1 | 100.0 |
| `C4P251` | 251. ¿CON QUÉ FRECUENCIA TE HAN OCURRIDO ESTAS SITUACIONES | 1. Casi nunca?; 2. Algunas veces?; 3. Siempre/Casi siempre?; 4. No sabe | 1 | 61.9 |
| `C4P252` | 252. POR LA/S SITUACIÓN/ES QUE MENCIONASTE, DE ACUERDO A LA TARJETA ¿ACUDISTE A ALGUNA PERSONA CERCANA PARA CONTARLE LO QUE TE SUCEDIÓ Y PEDIRLE AYUDA? | 1. Sí; 2. No; 3. No sabe | 1 | 61.9 |
| `C4P253_1`–`_21` | 253. ¿A QUIÉN LE PEDISTE AYUDA? | 1. Madre; 2. Padre; 3. Madrastra; 4. Padrastro; 5. Hermana/Hermanastra; 6. Hermano/ Hermanastro; 7. Abuela; 8. Abuelo; 9. Tía [hermana de la madre o padre]; 10. Tío [hermano de la madre o padre]; 11. Otro pariente [consanguíneo] [Especifique]; 12. Director/a del Centro de Acogida Residencial [albergue o casa hogar]; 13. Tutor/a / Cuidador/a del Centro de Acogida Residencial [albergue o casa hogar]; 14. Compañero/a del Centro de Acogida Residencial [albergue o casa hogar]; 15. Director/a del colegio; 16. Profesora; 17. Profesor; 18. Auxiliar de educación; 19. Amiga; 20. Amigo; 21. Otra persona | 21 | 80.0 |
| `C4P254` | 254. Esta/s persona/s, ¿Te ayudó/ayudaron? | — | 1 | 80.0 |
| `C4P255_1`–`_7` | 255. ¿CÓMO TE AYUDÓ / AYUDARON ESTA/S PERSONA/S? | 1. Me aconsejaron; 2. Conversaron con mi madre/padre; 3. Hablaron/reclamaron al agresor/a; 4. Avisaron a las autoridades; 5. Me refugiaron en su casa; 6. Me llevaron a un especialista; 7. Otro | 7 | 81.7 |
| `C4P256` | 256. ¿POR QUÉ CREES QUE NO TE AYUDÓ / AYUDARON? | 1. No me creyeron; 2. No supieron cómo ayudarme; 3. No quisieron involucrarse; 4. Otro; 5. No sabe | 1 | 98.4 |
| `C4P257` | 257. EN LOS ÚLTIMOS 12 MESES, DE …… A ……., POR LAS SITUACIONES QUE MENCIONASTE DE ACUERDO A LA TARJETA, ¿FUISTE O TE LLEVARON A ALGUNA INSTITUCIÓN PARA BUSCAR AYUDA? | 1. Sí; 2. No | 1 | 61.9 |
| `C4P258_1`–`_12` | 258. ¿A QUÉ INSTITUCIÓN FUISTE O TE LLEVARON? | 1. Comisaría; 2. Juzgado/Juez de Paz; 3. Fiscalía/Ministerio Público; 4. Defensoría Municipal de la Niña, Niño y del Adolescente [DEMUNA]; 5. Unidad de Protección Especial [UPE]; 6. Centro Emergencia Mujer [CEM]; 7. Ministerio de Educación/Dirección Regional de Educación [DRE]/Unidad de Gestión Educativa Local [UGEL]; 8. A la oficina de la Dirección de la institución educativa; 9. Establecimiento de salud [Hospital, centro de salud, posta médica]; 10. Gobernación; 11. Otra institución; 12. No sabe | 12 | 97.2 |
| `C4P259` | 259. LA/ LAS INSTITUCIÓN/ES A LA/S QUE FUISTE O TE LLEVARON ¿TE AYUDÓ/AYUDARON? | 1. Sí; 2. No; 3. No sabe | 1 | 97.2 |
| `C4P260_1`–`_4` | 260. ¿CÓMO TE AYUDÓ /AYUDARON ESTA/S INSTITUCIÓN/ES? | 1. Conversaron con mi madre/ padre/familiares; 2. Asistí a terapias; 3. Llamó/Llamaron la atención a quien me agredió; 4. Otro | 4 | 97.7 |

## CAP300 actitudes y tareas

| Variables | Qué pregunta | Ítems / códigos | N cols | % null |
| --- | --- | --- | --- | --- |
| `C3P301_1`–`_6` | 301. A CONTINUACIÓN, VOY A LEERTE ALGUNAS ORACIONES, PARA QUE ME DIGAS SI ESTÁS DE ACUERDO O NO | 1. Una niña, un niño o una/un adolescente debe trabajar cuando falta la plata en la casa; 2. Una niña, un niño o una/un adolescente puede hablar y decir las cosas que piensa y siente; 3. La madre y/o padre pueden decidir que su hija o hijo deje de estudiar; 4. Las profesoras o los profesores tienen el derecho a golpear a una niña, un niño o una/un adolescente para corregirla/o; 5. La madre y/o el padre tiene el derecho de golpear a su hija o hijo cuando se porta mal; 6. Una niña, un niño o una/un adolescente puede denunciar a la persona que lo lastima, lo golpea y lo maltrata | 6 | 0.0 |
| `C3P302_1`–`_10` | 302. EN TU CASA ¿QUÉ PERSONA REALIZA CON MAYOR FRECUENCIA LAS TAREAS DEL HOGAR, TALES COMO | 1. Cocinar? [Espere la respuesta]; 2. Lavar o planchar la ropa? [Espere la respuesta]; 3. Hacer las compras en el mercado para la comida? [Espere la respuesta]; 4. Dar dinero para la comida, comprarles ropa a ti y a tus hermanos, y otros gastos? [Espere la respuesta]; 5. Hacer la limpieza del hogar? [Espere la respuesta]; 6. Lavar los platos, ollas u otros utensilios? [Espere la respuesta]; 7. Cuidar a tus hermanas/os? [Espere la respuesta]; 8. Ayudarte con las tareas que te dejan en el colegio? [Espere la respuesta]; 9. Aconsejarte y escucharte? [Espere la respuesta]; 10. Jugar contigo? [Espere la respuesta] | 10 | 0.0 |
| `C3P303_*` (4 cols, 1–5) | 303. AHORA TE VOY A LEER ALGUNAS ORACIONES, PARA QUE ME DIGAS SI ESTÁS DE ACUERDO O NO | 1. La violencia sexual contra una niña, niño o una/un adolescente solo es cometida por personas que están locas; 3. La violencia sexual solo le ocurre a las niñas, niños y adolescentes pobres; 4. La violencia sexual contra una niña, un niño o una/un adolescente se dan mayormente fuera de la casa; 5. La violencia sexual ocurre más en sitios oscuros y solitarios | 4 | 0.0 |
