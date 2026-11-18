# Pre-flight: Presentación Algoritmo de Machine Learning en Parejas - Hoja de trabajo 2

Revisión como si se entregara el 2026-08-24 20:29 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

Las instrucciones no tienen puntos por criterio.

Las instrucciones no traen tabla de puntos, asi que ningun criterio tiene puntaje y los puntos en riesgo quedan sin cifra. El contenido esta completo: las siete secciones obligatorias (L019 a L025) se cubren para los cuatro algoritmos del Tema 8, con ejemplo numerico a mano y metricas discutidas. El riesgo esta en el formato de entrega: la carpeta solo tiene el .pptx, falta el PDF de las slides y no aparece el link al Colab ni el notebook que piden L005 y L006, y quedan minutos para el cierre.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Tema asignado al Grupo 4: K-Means + K-Medianas + K-Medoids + Fuzzy K-Means | Cumple | - | L016 |
| Cubrir las secciones obligatorias en orden | Cumple | - | L018 |
| Sección 1 — ¿Qué problema resuelve? tipo de tarea y cuándo aplica | Cumple | - | L019 |
| Sección 2 — La intuición sin ecuaciones, con analogía o ejemplo cotidiano | Cumple | - | L020 |
| Sección 3 — Cómo funciona paso a paso con al menos un ejemplo numérico resuelto a mano | Cumple | - | L021 |
| Sección 4 — Hiperparámetros clave y su efecto | Cumple | - | L022 |
| Sección 5 — Fortalezas y limitaciones, cuándo usarlo y cuándo no | Cumple | - | L023 |
| Sección 6 — Demo en Colab: notebook con dataset real, modelo entrenado y al menos una métrica discutida | Parcial | - | L024 |
| Sección 7 — Conexión con el curso | Cumple | - | L025 |
| Formato: slides + notebook de Google Colab ejecutable con un dataset real | Parcial | - | L005 |
| Entrega del PDF de las slides | Falta | - | L006 |
| Entrega del link al Colab compartido | Parcial | - | L006 |
| Duración aproximada de 30 minutos de presentación mas 5 de preguntas | No verificable | - | L004 |
| Trabajo en parejas; ambos integrantes deben poder responder cualquier pregunta | Cumple | - | L007 |

### 1. Tema asignado al Grupo 4: K-Means + K-Medianas + K-Medoids + Fuzzy K-Means

Estado: Cumple. En riesgo: sin puntos.

Los cuatro algoritmos del tema asignado aparecen tratados cada uno en su propio bloque.

Según las instrucciones:
- L016: "Grupo 4 - Tema 8 — K-Means + K-Medianas + K-Medoids + Fuzzy K-Means"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Portada y bloques dedicados a los cuatro algoritmos (slides 5-10 K-Means, 11-16 Fuzzy, 17-22 K-Medianas, 23-28 K-Medoids).

### 2. Cubrir las secciones obligatorias en orden

Estado: Cumple. En riesgo: sin puntos.

Están las siete secciones y cada bloque respeta el orden 3-4-5, pero la secuencia global no es 1 a 7 de corrido porque 3, 4 y 5 se repiten por algoritmo; el propio deck declara esa decision en las notas.

Según las instrucciones:
- L018: "Todos los grupos deben cubrir estas secciones en orden:"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 2 (mapa del deck) y numeración de secciones 1 a 7 en el encabezado de cada diapositiva; las siete secciones aparecen.

### 3. Sección 1 — ¿Qué problema resuelve? tipo de tarea y cuándo aplica

Estado: Cumple. En riesgo: sin puntos.

Cumple: define el tipo de tarea y los casos de aplicación y de no aplicación.

Según las instrucciones:
- L019: "- ¿Qué problema resuelve? — tipo de tarea (clasificación, regresión, clustering) y cuándo aplica"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 3 identifica la tarea como aprendizaje no supervisado y lista cuándo aplica y cuándo no.

### 4. Sección 2 — La intuición sin ecuaciones, con analogía o ejemplo cotidiano

Estado: Cumple. En riesgo: sin puntos.

Cumple: hay una analogía cotidiana concreta y la diapositiva no contiene ecuaciones.

Según las instrucciones:
- L020: "- La intuición — sin ecuaciones primero; una analogía o ejemplo cotidiano concreto"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 4 desarrolla la analogía de los food trucks sin formulas.

### 5. Sección 3 — Cómo funciona paso a paso con al menos un ejemplo numérico resuelto a mano

Estado: Cumple. En riesgo: sin puntos.

Cumple: hay desarrollo paso a paso y ejemplos numéricos a mano con iteraciones y valores de J para cada algoritmo.

Según las instrucciones:
- L021: "- Cómo funciona — el algoritmo paso a paso, con al menos un ejemplo numérico simple resuelto a mano"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slides 6 y 8 (K-Means), 13 y 14 (Fuzzy), 18-20 (K-Medianas), 25 y 26 (K-Medoids): bucle paso a paso y ejemplo a mano con seis puntos e iteraciones.

### 6. Sección 4 — Hiperparámetros clave y su efecto

Estado: Cumple. En riesgo: sin puntos.

Cumple: cada bloque tiene su diapositiva de hiperparámetros con el efecto de cada uno.

Según las instrucciones:
- L022: "- Hiperparámetros clave — qué se puede ajustar y qué efecto tiene"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slides 9, 15, 21 y 27 tratan k, inicializacion, n_init, el fuzzifier m, la métrica de distancia y la variante del algoritmo, con su efecto.

### 7. Sección 5 — Fortalezas y limitaciones, cuándo usarlo y cuándo no

Estado: Cumple. En riesgo: sin puntos.

Cumple: hay fortalezas y limitaciones para los cuatro algoritmos y criterios de elección.

Según las instrucciones:
- L023: "- Fortalezas y limitaciones — cuándo usarlo y cuándo no"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slides 10, 16, 22 y 28 listan fortalezas y limitaciones por algoritmo; slide 29 añade una tabla comparativa con 'cuándo elegirlo'.

### 8. Sección 6 — Demo en Colab: notebook con dataset real, modelo entrenado y al menos una métrica discutida

Estado: Parcial. En riesgo: sin puntos.

La diapositiva de la demo existe con dataset real y métricas discutidas, pero en la carpeta no hay ningún notebook ni enlace a él, y las notas indican que faltan las capturas de la corrida.

Según las instrucciones:
- L024: "- Demo en Colab — notebook con dataset real, modelo entrenado y al menos una métrica de evaluación discutida"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 30 describe el dataset HELP International de 167 países y discute ARI y silhouette; las notas piden rellenar la diapositiva con capturas del notebook ya corrido.

### 9. Sección 7 — Conexión con el curso

Estado: Cumple. En riesgo: sin puntos.

Cumple: hay una diapositiva dedicada a la conexión con los pilares del curso.

Según las instrucciones:
- L025: "- Conexión con el curso"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 31 conecta el tema con el pilar de Machine Learning y con el pilar de búsqueda.

### 10. Formato: slides + notebook de Google Colab ejecutable con un dataset real

Estado: Parcial. En riesgo: sin puntos.

Están las slides, pero en la carpeta no hay notebook de Colab ni referencia a uno; el único enlace del deck apunta a GitHub.

Según las instrucciones:
- L005: "Formato: slides (cualquier herramienta) + notebook de Google Colab ejecutable con un dataset real"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Único archivo de la entrega; es el deck de slides. No hay archivo .ipynb en la carpeta.
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 1 muestra un enlace a un repositorio de GitHub, no a Google Colab.

### 11. Entrega del PDF de las slides

Estado: Falta. En riesgo: sin puntos.

No hay PDF de las slides en la entrega, solo el archivo .pptx.

Según las instrucciones:
- L006: "Entrega: PDF de las slides y link al Colab compartido antes de la sesión de presentación"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: La carpeta contiene un solo archivo y su extensión es .pptx; no hay ningún PDF.

### 12. Entrega del link al Colab compartido

Estado: Parcial. En riesgo: sin puntos.

No aparece ningún enlace a Colab en los archivos revisados; podría estar en el texto de la entrega de Canvas, que no forma parte de la carpeta y no se puede comprobar.

Según las instrucciones:
- L006: "Entrega: PDF de las slides y link al Colab compartido antes de la sesión de presentación"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Búsqueda de 'colab', 'drive.google' e 'ipynb' en el texto y notas del deck: solo aparece un enlace a github.com/fabianpradod/ml-algorithms.

### 13. Duración aproximada de 30 minutos de presentación mas 5 de preguntas

Estado: No verificable. En riesgo: sin puntos.

Depende de la exposición en vivo y no se puede comprobar con los archivos.

Según las instrucciones:
- L004: "Duración: aprox 30 minutos de presentación + 5 minutos de preguntas del grupo"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: 31 diapositivas con notas del orador extensas; la duración real solo se mide en la sesión en vivo.

### 14. Trabajo en parejas; ambos integrantes deben poder responder cualquier pregunta

Estado: Cumple. En riesgo: sin puntos.

La portada acredita a la pareja; la parte de responder preguntas ocurre en vivo y no se puede comprobar con los archivos.

Según las instrucciones:
- L007: "Trabajo: en parejas — ambos integrantes deben poder responder cualquier pregunta"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Slide 1 identifica al Grupo 4 con dos integrantes: Fabian Prado Dluzniewski y Sofia Lopez.

## Hechos revisados por script

- Aviso: Quedan 0.02 horas para la fecha de entrega (2026-08-24 20:30).
- Bien: Ya hay una entrega en Canvas (2026-08-24 18:28).
- Bien: El texto no menciona otras fechas.
- Bien: Todas las instrucciones están en el texto de Canvas.
- Bien: La carpeta tiene 1 archivos.
- Nota: Las instrucciones no tienen tabla de puntos.
- Nota: Canvas no restringe los tipos de archivo.
- Nota: La carpeta no es un repositorio git.

## Lo que no se pudo revisar

- La fecha límite (Due 2026-08-24 20:30) aparece en el encabezado de las instrucciones, en una línea sin identificador L, por lo que no se puede citar como requisito numerado.
- L006 fija la entrega 'antes de la sesión de presentación', sin fecha concreta en el texto de las instrucciones.
- Posible link al Colab en el texto de la entrega de Canvas (online_text_entry): no está en la carpeta y no se puede revisar.
- Enlace externo https://github.com/fabianpradod/ml-algorithms de la portada: no se visita ni se comprueba su contenido.
- Imágenes, figuras y capturas dentro del .pptx: solo se extrajo el texto, así que no se puede confirmar si la figura 2x2 de la demo o las gráficas de codo y silhouette están insertadas.
- No hay notebook en la carpeta, por lo que no se puede comprobar que sea ejecutable ni que el modelo esté entrenado.
- La carpeta no es un repositorio git, así que no hay historial que revisar.

## Validación de la respuesta del agente

Todas las citas son textuales (14) y la evidencia citada existe (15 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
