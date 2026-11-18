# Pre-flight: Laboratorio 6 - Naive Bayes and Decision Trees

Revisión como si se entregara el 2026-09-11 23:58 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

Las instrucciones no tienen puntos por criterio.

A un minuto del cierre no hay nada entregado en Canvas y la carpeta de la entrega no existe, asi que los 4 puntos de la nota final estan en riesgo completo. Falta todo: notebook con los cuatro modelos sobre la misma matriz TF-IDF y el mismo split, las 5 metricas de cada uno, la captura del leaderboard y las 6 preguntas de reflexion. Las instrucciones no traen tabla de puntos, por eso los criterios quedan sin puntaje desglosado.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Notebook .ipynb con los cuatro modelos obligatorios sobre las mismas features y el mismo split | Falta | - | L028 |
| Multinomial Naive Bayes: 5 metricas y palabras con mayor peso hacia cada clase | Falta | - | L019 |
| Arbol de decision: dos arboles (sin limite y con max_depth acotado), 5 metricas de ambos y brecha train/test | Falta | - | L020 |
| Random Forest: 5 metricas y tiempo de entrenamiento | Falta | - | L021 |
| Gradient Boosting: 5 metricas y tiempo de entrenamiento | Falta | - | L022 |
| Vectorizacion del texto con TfidfVectorizer antes de entrenar | Falta | - | L013 |
| Todos los modelos sobre la misma matriz TF-IDF y el mismo split | Falta | - | L025 |
| Metricas calculadas sobre un split local hecho a partir de train.csv | Falta | - | L009 |
| Captura del leaderboard de Kaggle con usuario y score visibles, del modelo con mejor F1 | Falta | - | L029 |
| Reflexion con las 6 preguntas de la plantilla, idealmente al final del notebook | Falta | - | L030 |
| Subida del .ipynb a Canvas | Falta | - | L045 |
| Modelos de referencia opcionales: regresion logistica y KNN sobre la misma matriz TF-IDF | Falta | - | L024 |
| Poder explicar en vivo cualquier linea del notebook entregado | No verificable | - | L042 |

### 1. Notebook .ipynb con los cuatro modelos obligatorios sobre las mismas features y el mismo split

Estado: Falta. En riesgo: sin puntos.

No existe la carpeta de la entrega ni ningun archivo .ipynb que revisar.

Según las instrucciones:
- L028: "Notebook (.ipynb) | Con los cuatro modelos obligatorios implementados sobre las mismas features y el mismo split."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 2. Multinomial Naive Bayes: 5 metricas y palabras con mayor peso hacia cada clase

Estado: Falta. En riesgo: sin puntos.

Sin archivos de entrega no hay evidencia de este modelo ni de sus metricas.

Según las instrucciones:
- L019: "Multinomial Naive Bayes | Reportar las 5 métricas. Además, extraer las palabras con mayor peso hacia cada clase: ¿qué palabras delatan un desastre real?"
- L023: "Las 5 métricas son: accuracy, precision, recall, F1 y AUC-ROC."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 3. Arbol de decision: dos arboles (sin limite y con max_depth acotado), 5 metricas de ambos y brecha train/test

Estado: Falta. En riesgo: sin puntos.

No hay ningun archivo donde comprobar los dos arboles ni la brecha train/test.

Según las instrucciones:
- L020: "Árbol de decisión | Entrenar dos : uno sin límite de profundidad y uno con max_depth acotado. Reportar las 5 métricas de ambos y la brecha entre train y test de cada uno."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 4. Random Forest: 5 metricas y tiempo de entrenamiento

Estado: Falta. En riesgo: sin puntos.

No hay evidencia del modelo ni del tiempo de entrenamiento.

Según las instrucciones:
- L021: "Random Forest | Reportar las 5 métricas y el tiempo que tarda en entrenar."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 5. Gradient Boosting: 5 metricas y tiempo de entrenamiento

Estado: Falta. En riesgo: sin puntos.

No hay evidencia del modelo ni del tiempo de entrenamiento.

Según las instrucciones:
- L022: "Gradient Boosting | Reportar las 5 métricas y el tiempo que tarda en entrenar."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 6. Vectorizacion del texto con TfidfVectorizer antes de entrenar

Estado: Falta. En riesgo: sin puntos.

No hay codigo entregado donde verificar la vectorizacion.

Según las instrucciones:
- L013: "Antes de entrenar deben convertir cada tweet en un vector con TfidfVectorizer."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 7. Todos los modelos sobre la misma matriz TF-IDF y el mismo split

Estado: Falta. En riesgo: sin puntos.

Sin notebook no se puede comprobar que los modelos compartan matriz y split.

Según las instrucciones:
- L025: "Todos los modelos deben usar la misma matriz TF-IDF y el mismo split. Si no, la comparación no significa nada."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 8. Metricas calculadas sobre un split local hecho a partir de train.csv

Estado: Falta. En riesgo: sin puntos.

No hay archivos donde verificar el split local ni las metricas.

Según las instrucciones:
- L009: "Las 5 métricas se calculan sobre un split local que ustedes hacen a partir de train.csv. Ese es el conjunto donde sí tienen las respuestas correctas."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 9. Captura del leaderboard de Kaggle con usuario y score visibles, del modelo con mejor F1

Estado: Falta. En riesgo: sin puntos.

No hay ninguna imagen ni archivo de captura en la entrega.

Según las instrucciones:
- L029: "Captura del leaderboard | Una sola captura de Kaggle, con su usuario y su score visibles. Suban el modelo que les haya dado mejor F1."
- L046: "Incluyan la captura del leaderboard de Kaggle, con usuario y score visibles."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 10. Reflexion con las 6 preguntas de la plantilla, idealmente al final del notebook

Estado: Falta. En riesgo: sin puntos.

No hay texto de reflexion en ningun archivo porque no existe la entrega.

Según las instrucciones:
- L030: "Reflexión | Las 6 preguntas de la plantilla, idealmente al final del notebook."
- L032: "Pongan las métricas de los cuatro modelos lado a lado. ¿Cuál ganó en F1 sobre su split local, y por cuánto?"
- L033: "¿Que pueden decir de los resultados del uso de algoritmos basados en árboles?"
- L034: "Comparen el árbol sin límite contra el podado: ¿cuánta brecha hay entre train y test en cada uno? ¿Qué les dice eso sobre el sobreajuste con datos de texto?"
- L035: "Miren cuánto tardó cada modelo en entrenar. Random Forest es de los más lentos aquí, ¿le rindió ese costo?"
- L036: "Vean las palabras más informativas de Naive Bayes. ¿Tienen sentido? ¿Encuentran alguna que probablemente sea una trampa del dataset y no una señal real de desastre?"
- L037: "¿Qué pueden decir de los modelos utilizados y las métricas reportadas? ¿Por qué esta competencia se evalúa con F1 y no con accuracy?"

Evidencia revisada:
- Sin evidencia en la carpeta.

### 11. Subida del .ipynb a Canvas

Estado: Falta. En riesgo: sin puntos.

Los hechos verificados indican que no hay nada entregado en Canvas.

Según las instrucciones:
- L045: "Suban el .ipynb (con los cuatro modelos) a Canvas, igual que los otros labs."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 12. Modelos de referencia opcionales: regresion logistica y KNN sobre la misma matriz TF-IDF

Estado: Falta. En riesgo: sin puntos.

No hay evidencia, pero las instrucciones los marcan como opcionales y fuera de los cuatro obligatorios.

Según las instrucciones:
- L024: "Modelos de referencia (opcionales, para comparar): entrenen también regresión logística y KNN sobre la misma matriz TF-IDF. No son parte de los cuatro obligatorios."

Evidencia revisada:
- Sin evidencia en la carpeta.

### 13. Poder explicar en vivo cualquier linea del notebook entregado

Estado: No verificable. En riesgo: sin puntos.

Es una condicion oral que no se puede comprobar con archivos.

Según las instrucciones:
- L042: "Deben poder explicar, en vivo y con sus palabras, cualquier línea del notebook que entreguen. Esa es la verdadera regla."

Evidencia revisada:
- Sin evidencia en la carpeta.

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

- La carpeta de la entrega ~/Documents/projects/2026 - 2 /ai/lab6 no existe, asi que no hay ningun archivo que revisar.
- La exigencia de explicar en vivo el codigo (L042) es oral y queda fuera de los archivos.
- El leaderboard y la cuenta de Kaggle estan en un servicio externo, no en la carpeta.
- Los tres enlaces externos de las instrucciones no fueron leidos.
- No hay repositorio git, asi que no hay historial que revisar.

## Validación de la respuesta del agente

Todas las citas son textuales (21) y la evidencia citada existe (0 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
