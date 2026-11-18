# Pre-flight: Proyecto 2 - Machine Learning

Revisión como si se entregara el 2026-10-26 18:59 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 0 de 100.**

La rúbrica de 100 puntos está cubierta: no identifico puntos de contenido en riesgo. Los riesgos son de proceso: L029-L031 fechan código, informe y presentación el Oct 21 y la entrega en Canvas es del 26 de octubre a las 18:11; además hay un commit (19:49) y una modificación del pptx (20:08) posteriores a la hora límite y al intento ya enviado, más 4 cambios sin commitear. La propuesta (L011, L028) no está en la carpeta y su aprobación no se puede comprobar aquí.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Problema bien definido y dataset con origen documentado (propuesta aprobada) | Cumple | 0 de 10 | L036 |
| Análisis exploratorio y preprocesamiento justificado | Cumple | 0 de 15 | L037 |
| Baseline y al menos 3 modelos, con búsqueda de hiperparámetros | Cumple | 0 de 20 | L038 |
| Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste | Cumple | 0 de 20 | L039 |
| Análisis de errores, limitaciones y sesgos | Cumple | 0 de 10 | L040 |
| Código reproducible y claro | Cumple | 0 de 10 | L041 |
| Informe y presentación | Cumple | 0 de 15 | L042 |
| Propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal | No verificable | - | L011 |
| Declaración del uso de IA en el informe | Cumple | - | L032 |
| Dataset no usado antes en laboratorios del curso u otros cursos | No verificable | - | L008 |

### 1. Problema bien definido y dataset con origen documentado (propuesta aprobada)

Estado: Cumple. En riesgo: 0 de 10.

El problema, la variable objetivo y el origen del dataset con fuente, licencia y fecha están documentados; la propuesta aprobada no está en la carpeta y no se puede comprobar aquí.

Según las instrucciones:
- L036: "Problema bien definido y dataset con origen documentado (propuesta aprobada)"
- L009: "Origen documentado: fuente, licencia y fecha de obtención. Los datos personales deben anonimizarse."
- L007: "Al menos 500 filas y 5 variables predictoras."
- L006: "Tarea supervisada (clasificación o regresión) con una variable objetivo definida."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Secciones Problema, Objetivos y Datos: variable objetivo Diabetes_012 de tres clases, 253,680 filas y 21 predictoras, UCI #891 con DOI y CC BY 4.0, versión Kaggle CC0, obtención en octubre de 2026 y nota de que no hay identificadores personales.
- `README.md`: Tabla del dataset con nombre, referencia, licencia, fecha de obtención (26 de octubre de 2026) y tamaño.
- `notebooks/01_EDA.ipynb`: Diccionario de variables y documentación del dataset.

### 2. Análisis exploratorio y preprocesamiento justificado

Estado: Cumple. En riesgo: 0 de 15.

Hay tres visualizaciones ligadas a decisiones posteriores y cada decisión de limpieza, codificación, escalado y desbalance viene justificada.

Según las instrucciones:
- L037: "Análisis exploratorio y preprocesamiento justificado"
- L013: "Explorar la distribución de la variable objetivo, valores faltantes y outliers, con al menos 3 visualizaciones que informen decisiones posteriores."
- L014: "Limpiar, codificar variables categóricas, escalar cuando el modelo lo requiera y tratar el desbalance si existe."
- L015: "Justificar cada decisión."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Tres visualizaciones (distribución de la clase, boxplot de IMC por clase y mapa de correlación de Spearman) más revisión de faltantes, duplicados y outliers.
- `Informe-Proyecto2.docx`: Sección Decisiones de preprocesamiento con tipos de datos, faltantes, duplicados, outliers, codificación, escalado con StandardScaler en pipeline y pesos de clase para el desbalance, cada uno con su razón.
- `Presentacion-Proyecto2.pptx`: Diapositivas 4 y 5 resumen hallazgos del EDA y las decisiones derivadas.

### 3. Baseline y al menos 3 modelos, con búsqueda de hiperparámetros

Estado: Cumple. En riesgo: 0 de 20.

Están el baseline trivial, el simple y tres algoritmos adicionales, todos con búsqueda de hiperparámetros validada.

Según las instrucciones:
- L038: "Baseline y al menos 3 modelos, con búsqueda de hiperparámetros"
- L017: "Implementar un baseline trivial (clase mayoritaria o media) y uno simple (regresión lineal o logística)."
- L018: "Entrenar al menos 3 algoritmos vistos en clase o investigados por ustedes"
- L019: "Realizar búsqueda de hiperparámetros con validaciones."

Evidencia revisada:
- `notebooks/02_Baselines_Arbol.ipynb`: DummyClassifier de clase mayoritaria, regresión logística y árbol de decisión con GridSearchCV sobre validación cruzada estratificada.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Random forest y gradient boosting con RandomizedSearchCV y la misma validación cruzada.
- `resultados/resultados_integrante2.csv`: Tabla con las métricas de validación cruzada de los cinco modelos.

### 4. Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste

Estado: Cumple. En riesgo: 0 de 20.

La partición, el uso único del test, la justificación de la métrica y el diagnóstico de sobreajuste por brecha y por profundidad están presentes.

Según las instrucciones:
- L039: "Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste"
- L021: "Particionar en train, validación y test, o usar validación cruzada. El test se usa una sola vez, al final."
- L022: "Elegir y justificar la métrica principal según el costo de los errores del problema."
- L023: "Presentar matriz de confusión y métricas que consideren importantes."

Evidencia revisada:
- `notebooks/03_Modelos_Evaluacion.ipynb`: Sección de evaluación final marcada como única vez que se carga el test, matriz de confusión con ConfusionMatrixDisplay y classification_report.
- `notebooks/02_Baselines_Arbol.ipynb`: Análisis de sobreajuste del árbol comparando F1 de entrenamiento y validación por profundidad.
- `Informe-Proyecto2.docx`: Partición 80/20 estratificada con CV de 5, justificación del F1 macro por el costo de no detectar diabetes, tabla de brechas entrenamiento-validación y Tabla 3 con métricas por clase en prueba.
- `resultados/figuras/matriz_confusion_test.png`: Matriz de confusión del modelo final en el conjunto de prueba.

### 5. Análisis de errores, limitaciones y sesgos

Estado: Cumple. En riesgo: 0 de 10.

Hay ejemplos concretos de errores con explicación propuesta y discusión de limitaciones y sesgos de recolección y etiquetado.

Según las instrucciones:
- L040: "Análisis de errores, limitaciones y sesgos"
- L025: "Analizar ejemplos concretos que el mejor modelo clasifica o predice mal, y proponer por qué."
- L026: "Discutir limitaciones y posibles sesgos en cómo se recolectaron o etiquetaron los datos."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Sección Análisis de errores con perfiles de aciertos y errores, cinco casos concretos de diabetes no detectada y cinco falsas alarmas con hipótesis, desempeño por subgrupos y sección Limitaciones sobre etiqueta autorreportada, población y duplicados.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Análisis de errores con probabilidades del modelo, métricas por subgrupo e importancia por permutación.
- `Presentacion-Proyecto2.pptx`: Diapositivas 10, 11 y 12 con errores, sesgos por edad e ingreso y limitaciones.

### 6. Código reproducible y claro

Estado: Cumple. En riesgo: 0 de 10.

Los notebooks están ejecutados de principio a fin y el repo incluye README, dependencias, dataset y script para obtenerlo.

Según las instrucciones:
- L041: "Código reproducible y claro"
- L029: "notebook o scripts que corran de principio a fin, con el dataset o el script para obtenerlo y un README con instrucciones"

Evidencia revisada:
- `README.md`: Instrucciones de entorno, orden de ejecución de los tres notebooks, comando de nbconvert y descripción de la partición compartida con random_state=42.
- `requirements.txt`: Dependencias con versiones mínimas.
- `scripts/descargar_datos.py`: Script de descarga desde Kaggle con verificación SHA-256.
- `notebooks/01_EDA.ipynb`: Todas las celdas de los tres notebooks tienen execution_count asignado y rutas que funcionan desde la raíz o desde notebooks/.

### 7. Informe y presentación

Estado: Cumple. En riesgo: 0 de 15.

El informe trae todas las secciones pedidas y la presentación está completa; la exposición en vivo no se puede revisar desde archivos.

Según las instrucciones:
- L042: "Informe y presentación"
- L030: "Informe breve: problema, datos, decisiones de preprocesamiento, comparación de modelos, análisis de errores y limitaciones."
- L031: "Presentación de su trabajo"

Evidencia revisada:
- `Informe-Proyecto2.docx`: Cubre problema, datos, preprocesamiento, comparación de modelos, evaluación, análisis de errores, limitaciones, conclusiones, uso de IA y referencias.
- `Presentacion-Proyecto2.pptx`: 13 diapositivas con notas del orador que recorren todo el flujo.
- `Guion-Presentacion.docx`: Guion con reparto entre los dos integrantes, tiempos y preguntas probables.

> Aviso: la validación encontró problemas en este criterio.

### 8. Propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal

Estado: No verificable. En riesgo: sin puntos.

El archivo de la propuesta no está en la carpeta de entrega; fue un entregable aparte del Oct 5 y su aprobación no se puede comprobar aquí.

Según las instrucciones:
- L011: "Antes de empezar, cada grupo entrega una propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal."
- L028: "Propuesta (Oct 5, 2026): media página con problema, variable objetivo, fuente de datos y métrica principal."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Menciona que la regla de elección del modelo se definió en la propuesta, pero el documento de la propuesta no está en la carpeta.
- `Guion-Presentacion.docx`: Repite que la regla del mayor F1 macro venía de la propuesta.

### 9. Declaración del uso de IA en el informe

Estado: Cumple. En riesgo: sin puntos.

El informe declara la herramienta, el uso y lo verificado manualmente.

Según las instrucciones:
- L032: "El informe indica qué herramienta se usó, para qué y qué se verificó a mano."
- L044: "Penalizaciones: Uso de IA no declarado, se aplica la política de plagio del curso."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Sección Uso de inteligencia artificial: nombra la herramienta, para qué se usó y lista cuatro verificaciones hechas a mano.

### 10. Dataset no usado antes en laboratorios del curso u otros cursos

Estado: No verificable. En riesgo: sin puntos.

No hay forma de comprobar desde la carpeta si este dataset se usó antes en laboratorios u otros cursos.

Según las instrucciones:
- L008: "No se aceptan datasets ya usados en los laboratorios del curso o proyectos trabajados en otros cursos."
- L044: "Uso de otros proyectos de otros cursos ya trabajados anteriormente."

Evidencia revisada:
- `README.md`: Identifica el dataset como CDC Diabetes Health Indicators de Kaggle y UCI, sin referencia a su uso previo en el curso.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Propuesta de media página | Oct 5, 2026 | L028 |
| Código (notebooks o scripts, dataset o script de descarga y README) | Oct 21, 2026 | L029 |
| Informe breve | Oct 21, 2026 | L030 |
| Presentación | Oct 21, 2026 | L031 |

## Hechos revisados por script

- Aviso: Quedan 0.02 horas para la fecha de entrega (2026-10-26 19:00).
- Aviso: Fechas del texto que ya pasaron: 2026-10-05 (L028), 2026-10-21 (L029), 2026-10-21 (L030), 2026-10-21 (L031). Revisa que esas entregas estén hechas.
- Aviso: Hay 4 cambios sin commit.
- Aviso: Hay 1 commits con fecha posterior a la entrega: f0f375f (2026-10-26 19:49) docs: changes to ppt.
- Bien: Ya hay una entrega en Canvas (2026-10-26 18:11).
- Bien: La rúbrica tiene 7 criterios que suman 100 puntos.
- Bien: Todas las instrucciones están en el texto de Canvas.
- Bien: La carpeta tiene 19 archivos.
- Bien: Todo está subido al remoto.
- Nota: Canvas no restringe los tipos de archivo.
- Nota: Repositorio git en la rama main.

## Lo que no se pudo revisar

- La propuesta del Oct 5 y su aprobación: el documento no está en la carpeta de entrega.
- Si el dataset ya se usó en laboratorios del curso o en otros cursos (L008).
- La exposición oral de la presentación (L031): solo se puede revisar el pptx y el guion.
- data/raw/diabetes_012_health_indicators_BRFSS2015.csv.zip no se copió por ser binario: el contenido del dataset solo se comprueba por lo que reportan los notebooks.
- data/processed/particion.csv no se copió por tamaño: la partición solo se comprueba por el código que la genera.
- 1 archivo omitido por seguridad (oculto o con secretos), según inventario.txt.
- Qué versión exacta de los archivos se subió a Canvas a las 18:11: hay un commit del 26/10 a las 19:49 y el pptx figura modificado a las 20:08, ambos posteriores a la hora límite de las 19:00.
- 4 cambios sin commitear en el repositorio: no se puede saber si afectan los archivos entregados.
- Enlaces externos del informe y del README (UCI, Kaggle, GitHub, CDC): no se abrieron.

## Validación de la respuesta del agente

Se encontraron 2 problemas. Los criterios marcados no son confiables:

- cita no textual: `criterios[6].citas[1]` ('Informe breve: problema, datos, decisiones de preprocesamiento, comparación de modelos, análisis de errores y limitaciones.' is not in L030)
- cita no textual: `criterios[6].citas[2]` ('Presentación de su trabajo' is not in L031)

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
