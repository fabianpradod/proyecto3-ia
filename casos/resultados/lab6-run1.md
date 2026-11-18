# Pre-flight: Laboratorio 6 - Naive Bayes and Decision Trees

Revisión como si se entregara el 2026-09-11 23:58 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

Las instrucciones no tienen puntos por criterio.

No hay entrega que auditar: la carpeta indicada no existe y Canvas no registra nada subido, con el plazo cerrando en aproximadamente un minuto. Las instrucciones no traen tabla de puntos, asi que no se cuantifica la perdida por criterio, pero los 11 criterios verificables estan en falta y el valor completo de la tarea (4 puntos de la nota final) esta en riesgo. Lo urgente es confirmar si los archivos estan en otra ruta.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Notebook .ipynb con los cuatro modelos obligatorios implementados | Falta | - | L028 |
| Conversion del texto a numeros con TfidfVectorizer | Falta | - | L013 |
| Misma matriz TF-IDF y mismo split para todos los modelos | Falta | - | L025 |
| Multinomial Naive Bayes: 5 metricas y palabras con mayor peso hacia cada clase | Falta | - | L019 |
| Arbol de decision: dos arboles (sin limite y con max_depth), 5 metricas de ambos y brecha train/test | Falta | - | L020 |
| Random Forest: 5 metricas y tiempo de entrenamiento | Falta | - | L021 |
| Gradient Boosting: 5 metricas y tiempo de entrenamiento | Falta | - | L022 |
| Las 5 metricas (accuracy, precision, recall, F1, AUC-ROC) calculadas sobre el split local de train.csv | Falta | - | L023 |
| Captura del leaderboard de Kaggle con usuario y score visibles | Falta | - | L029 |
| Reflexion con las 6 preguntas de la plantilla | Falta | - | L030 |
| Subir el .ipynb a Canvas | Falta | - | L045 |
| Poder explicar en vivo cualquier linea del notebook | No verificable | - | L042 |

### 1. Notebook .ipynb con los cuatro modelos obligatorios implementados

Estado: Falta. En riesgo: sin puntos.

No hay ningun archivo de entrega disponible, por lo que no existe notebook alguno.

Según las instrucciones:
- L028: "Notebook (.ipynb) | Con los cuatro modelos obligatorios implementados sobre las mismas features y el mismo split."
- L017: "Los cuatro son obligatorios, todos sobre el mismo split y la misma matriz TF-IDF:"

Evidencia revisada:
- `(carpeta de entrega)`: La carpeta de la entrega no existe segun hechos.json e inventario.txt, no hay ningun .ipynb que revisar.

### 2. Conversion del texto a numeros con TfidfVectorizer

Estado: Falta. En riesgo: sin puntos.

No hay evidencia de la vectorizacion TF-IDF porque no existe entrega.

Según las instrucciones:
- L013: "Antes de entrenar deben convertir cada tweet en un vector con TfidfVectorizer."

Evidencia revisada:
- `(carpeta de entrega)`: Sin archivos en la entrega no hay codigo donde buscar el vectorizador.

### 3. Misma matriz TF-IDF y mismo split para todos los modelos

Estado: Falta. En riesgo: sin puntos.

No se puede constatar el uso compartido de features y split porque no hay entrega.

Según las instrucciones:
- L025: "Todos los modelos deben usar la misma matriz TF-IDF y el mismo split. Si no, la comparación no significa nada."

Evidencia revisada:
- `(carpeta de entrega)`: No hay codigo que permita comprobar que features y split se comparten entre modelos.

### 4. Multinomial Naive Bayes: 5 metricas y palabras con mayor peso hacia cada clase

Estado: Falta. En riesgo: sin puntos.

Falta por completo: no hay archivos con el modelo ni con sus resultados.

Según las instrucciones:
- L019: "Multinomial Naive Bayes | Reportar las 5 métricas. Además, extraer las palabras con mayor peso hacia cada clase: ¿qué palabras delatan un desastre real?"

Evidencia revisada:
- `(carpeta de entrega)`: No hay notebook ni salidas donde aparezcan metricas ni palabras informativas.

### 5. Arbol de decision: dos arboles (sin limite y con max_depth), 5 metricas de ambos y brecha train/test

Estado: Falta. En riesgo: sin puntos.

Falta por completo: no existe entrega donde revisar los dos arboles.

Según las instrucciones:
- L020: "Árbol de decisión | Entrenar dos : uno sin límite de profundidad y uno con max_depth acotado. Reportar las 5 métricas de ambos y la brecha entre train y test de cada uno."

Evidencia revisada:
- `(carpeta de entrega)`: No hay archivos de entrega donde verificar los dos arboles ni la brecha train/test.

### 6. Random Forest: 5 metricas y tiempo de entrenamiento

Estado: Falta. En riesgo: sin puntos.

Falta por completo: no hay archivos de entrega.

Según las instrucciones:
- L021: "Random Forest | Reportar las 5 métricas y el tiempo que tarda en entrenar."

Evidencia revisada:
- `(carpeta de entrega)`: No hay notebook ni salidas con metricas ni medicion de tiempo.

### 7. Gradient Boosting: 5 metricas y tiempo de entrenamiento

Estado: Falta. En riesgo: sin puntos.

Falta por completo: no hay archivos de entrega.

Según las instrucciones:
- L022: "Gradient Boosting | Reportar las 5 métricas y el tiempo que tarda en entrenar."

Evidencia revisada:
- `(carpeta de entrega)`: No hay notebook ni salidas con metricas ni medicion de tiempo.

### 8. Las 5 metricas (accuracy, precision, recall, F1, AUC-ROC) calculadas sobre el split local de train.csv

Estado: Falta. En riesgo: sin puntos.

No hay ninguna metrica reportada porque no existe entrega.

Según las instrucciones:
- L023: "Las 5 métricas son: accuracy, precision, recall, F1 y AUC-ROC."
- L009: "Las 5 métricas se calculan sobre un split local que ustedes hacen a partir de train.csv."

Evidencia revisada:
- `(carpeta de entrega)`: Sin archivos no hay ninguna metrica reportada ni evidencia del split local.

### 9. Captura del leaderboard de Kaggle con usuario y score visibles

Estado: Falta. En riesgo: sin puntos.

No hay captura de leaderboard en la entrega.

Según las instrucciones:
- L029: "Captura del leaderboard | Una sola captura de Kaggle, con su usuario y su score visibles. Suban el modelo que les haya dado mejor F1."
- L046: "Incluyan la captura del leaderboard de Kaggle, con usuario y score visibles."

Evidencia revisada:
- `(carpeta de entrega)`: No hay ninguna imagen en la entrega; la carpeta no existe.

### 10. Reflexion con las 6 preguntas de la plantilla

Estado: Falta. En riesgo: sin puntos.

No hay respuestas de reflexion porque no existe entrega.

Según las instrucciones:
- L030: "Reflexión | Las 6 preguntas de la plantilla, idealmente al final del notebook."
- L032: "Pongan las métricas de los cuatro modelos lado a lado. ¿Cuál ganó en F1 sobre su split local, y por cuánto?"
- L034: "Comparen el árbol sin límite contra el podado: ¿cuánta brecha hay entre train y test en cada uno?"
- L036: "Vean las palabras más informativas de Naive Bayes. ¿Tienen sentido?"
- L037: "¿Por qué esta competencia se evalúa con F1 y no con accuracy?"

Evidencia revisada:
- `(carpeta de entrega)`: No hay notebook ni documento con texto de reflexion.

### 11. Subir el .ipynb a Canvas

Estado: Falta. En riesgo: sin puntos.

Canvas no registra ninguna entrega y el plazo cierra en aproximadamente un minuto.

Según las instrucciones:
- L045: "Suban el .ipynb (con los cuatro modelos) a Canvas, igual que los otros labs."

Evidencia revisada:
- `(Canvas)`: hechos.json reporta: nothing submitted in Canvas yet.

### 12. Poder explicar en vivo cualquier linea del notebook

Estado: No verificable. En riesgo: sin puntos.

Es una comprobacion en vivo, fuera del alcance de la revision de archivos.

Según las instrucciones:
- L042: "Deben poder explicar, en vivo y con sus palabras, cualquier línea del notebook que entreguen. Esa es la verdadera regla."

Evidencia revisada:
- `(no aplica)`: Requisito oral, no comprobable con archivos.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Competencia de Kaggle (Natural Language Processing with Disaster Tweets) | sin fecha límite | L004 |

## Hechos revisados por script

- Problema: La carpeta no existe o está vacía.
- Aviso: Quedan 0.02 horas para la fecha de entrega (2026-09-11 23:59).
- Aviso: Todavía no hay nada entregado en Canvas.
- Bien: El texto no menciona otras fechas.
- Nota: Las instrucciones no tienen tabla de puntos.
- Nota: Enlaces externos que no se leyeron (referencias o datos): 3.
- Nota: Canvas no restringe los tipos de archivo.
- Nota: La carpeta no es un repositorio git.

## Lo que no se pudo revisar

- La carpeta de la entrega ~/Documents/projects/2026 - 2 /ai/lab6 no existe, asi que no hay ningun archivo que revisar (entrega/ y texto/ estan vacias).
- El requisito de explicar el codigo en vivo (L042) es oral y no se puede comprobar con archivos.
- Los 3 enlaces externos citados en las instrucciones (Kaggle y material de TF-IDF) no fueron leidos.
- El estado del leaderboard de Kaggle y la cuenta del estudiante estan fuera de la carpeta y no se pueden comprobar.
- No es un repositorio git, por lo que no hay historial que revisar.

## Validación de la respuesta del agente

Todas las citas son textuales (20) y la evidencia citada existe (12 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
