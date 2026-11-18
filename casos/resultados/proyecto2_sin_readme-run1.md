# Pre-flight: Proyecto 2 - Machine Learning

Revisión como si se entregara el 2026-10-26 18:59 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 3 de 100.**

La entrega cubre casi toda la rubrica; el unico faltante claro es el README con instrucciones que pide L029, con unos 3 de 100 puntos en riesgo dentro de Codigo reproducible y claro. Los demas criterios tienen evidencia en el informe, la presentacion y los tres notebooks, incluida la declaracion de uso de IA. Queda por confirmar fuera de la carpeta la propuesta aprobada y si el pptx subido a Canvas es la version actual.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Problema bien definido y dataset con origen documentado (propuesta aprobada) | Cumple | 0 de 10 | L036 |
| Propuesta de media pagina como entregable previo (Oct 5, 2026) | No verificable | - | L028 |
| Análisis exploratorio y preprocesamiento justificado | Cumple | 0 de 15 | L037 |
| Baseline y al menos 3 modelos, con búsqueda de hiperparámetros | Cumple | 0 de 20 | L038 |
| Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste | Cumple | 0 de 20 | L039 |
| Análisis de errores, limitaciones y sesgos | Cumple | 0 de 10 | L040 |
| Código reproducible y claro | Parcial | 3 de 10 | L041 |
| Informe y presentación | Cumple | 0 de 15 | L042 |
| Declaración del uso de IA en el informe | Cumple | - | L032 |
| Dataset no usado en laboratorios del curso ni en otros cursos | No verificable | - | L008 |

### 1. Problema bien definido y dataset con origen documentado (propuesta aprobada)

Estado: Cumple. En riesgo: 0 de 10.

El problema, la variable objetivo y el origen del dataset con licencia y fecha estan documentados; la aprobacion de la propuesta no se ve en la carpeta.

Según las instrucciones:
- L036: "Problema bien definido y dataset con origen documentado (propuesta aprobada)"
- L009: "Origen documentado: fuente, licencia y fecha de obtención. Los datos personales deben anonimizarse."
- L007: "Al menos 500 filas y 5 variables predictoras."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Define el problema de clasificacion de 3 clases, variable objetivo Diabetes_012, 253,680 filas y 21 predictoras, fuente UCI #891 con DOI y licencia CC BY 4.0, version Kaggle CC0, obtenido en octubre de 2026 y sin identificadores personales.
- `notebooks/01_EDA.ipynb`: Seccion Fuente, variable objetivo y diccionario de las 21 variables.

### 2. Propuesta de media pagina como entregable previo (Oct 5, 2026)

Estado: No verificable. En riesgo: sin puntos.

La propuesta era un entregable aparte con fecha anterior y no esta en esta carpeta, por lo que no se puede comprobar aqui.

Según las instrucciones:
- L028: "Propuesta (Oct 5, 2026): media página con problema, variable objetivo, fuente de datos y métrica principal."
- L011: "Antes de empezar, cada grupo entrega una propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal."

Evidencia revisada:
- `inventario.txt`: No aparece ningun archivo de propuesta entre los 17 archivos listados.
- `Informe-Proyecto2.docx`: El informe menciona la regla definida en la propuesta (mayor F1 macro), pero el documento de la propuesta no esta en la carpeta.

### 3. Análisis exploratorio y preprocesamiento justificado

Estado: Cumple. En riesgo: 0 de 15.

Hay mas de tres visualizaciones que sustentan decisiones y cada decision de limpieza, codificacion, escalado y desbalance esta justificada.

Según las instrucciones:
- L037: "Análisis exploratorio y preprocesamiento justificado"
- L013: "Explorar la distribución de la variable objetivo, valores faltantes y outliers, con al menos 3 visualizaciones que informen decisiones posteriores."
- L014: "Limpiar, codificar variables categóricas, escalar cuando el modelo lo requiera y tratar el desbalance si existe."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Secciones de tipos de datos, faltantes, valores fuera de rango, duplicados y outliers, con cuatro graficas: distribucion de la objetivo, boxplot de IMC por clase, heatmap de correlacion y factores de riesgo por clase.
- `Informe-Proyecto2.docx`: Seccion Decisiones de preprocesamiento con justificacion de tipos, faltantes, duplicados, outliers, codificacion, escalado con StandardScaler en pipeline y pesos de clase frente a SMOTE.

### 4. Baseline y al menos 3 modelos, con búsqueda de hiperparámetros

Estado: Cumple. En riesgo: 0 de 20.

Hay baseline trivial, baseline simple y cuatro algoritmos adicionales, todos con busqueda de hiperparametros validada por validacion cruzada.

Según las instrucciones:
- L038: "Baseline y al menos 3 modelos, con búsqueda de hiperparámetros"
- L017: "Implementar un baseline trivial (clase mayoritaria o media) y uno simple (regresión lineal o logística)."
- L019: "Realizar búsqueda de hiperparámetros con validaciones."

Evidencia revisada:
- `notebooks/02_Baselines_Arbol.ipynb`: DummyClassifier de clase mayoritaria, regresion logistica con GridSearchCV y arbol de decision con busqueda en malla.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Random forest y HistGradientBoosting con RandomizedSearchCV sobre StratifiedKFold de 5 particiones.
- `resultados/mejores_hiperparametros_integrante2.json`: Mejores hiperparametros guardados de la busqueda.

### 5. Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste

Estado: Cumple. En riesgo: 0 de 20.

Particion estratificada mas validacion cruzada, test usado una sola vez, metrica principal justificada por el costo de los errores y diagnostico de sobreajuste por brecha entre entrenamiento y validacion.

Según las instrucciones:
- L039: "Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste"
- L021: "Particionar en train, validación y test, o usar validación cruzada. El test se usa una sola vez, al final."
- L022: "Elegir y justificar la métrica principal según el costo de los errores del problema."
- L023: "Presentar matriz de confusión y métricas que consideren importantes."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Particion estratificada 80/20 guardada en data/processed/particion.csv antes del analisis.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Validacion cruzada estratificada de 5 particiones y evaluacion final unica en test con classification_report y ConfusionMatrixDisplay.
- `Informe-Proyecto2.docx`: Justifica el F1 macro por el desbalance y el costo de no detectar diabetes, y presenta la tabla de brecha entrenamiento-validacion por modelo.
- `resultados/figuras/matriz_confusion_test.png`: Matriz de confusion del modelo final en el conjunto de prueba.

### 6. Análisis de errores, limitaciones y sesgos

Estado: Cumple. En riesgo: 0 de 10.

Hay ejemplos concretos de errores con explicacion propuesta, mas limitaciones y sesgos de recoleccion y etiquetado.

Según las instrucciones:
- L040: "Análisis de errores, limitaciones y sesgos"
- L025: "Analizar ejemplos concretos que el mejor modelo clasifica o predice mal, y proponer por qué."
- L026: "Discutir limitaciones y posibles sesgos en cómo se recolectaron o etiquetaron los datos."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Seccion Analisis de errores con perfil de falsos negativos y falsas alarmas, cinco casos concretos de cada tipo con hipotesis, desempeno por subgrupos y seccion Limitaciones sobre etiqueta autorreportada, poblacion y duplicados.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Secciones Analisis de errores, Prediabetes, Desempeno por subgrupos (posibles sesgos) e Importancia de las variables.

### 7. Código reproducible y claro

Estado: Parcial. En riesgo: 3 de 10.

Estan el dataset, el script para obtenerlo, las dependencias y los notebooks encadenados con semilla, pero falta el README con instrucciones que pide L029.

Según las instrucciones:
- L041: "Código reproducible y claro"
- L029: "Código (Oct 21, 2026): notebook o scripts que corran de principio a fin, con el dataset o el script para obtenerlo y un README con instrucciones."

Evidencia revisada:
- `inventario.txt`: Entre los 17 archivos de la entrega no hay ningun README.
- `scripts/descargar_datos.py`: Script de descarga del dataset desde Kaggle con verificacion SHA-256 y docstring de uso.
- `requirements.txt`: Lista de dependencias con versiones minimas.
- `notebooks/02_Baselines_Arbol.ipynb`: Notebooks numerados y encadenados por data/processed/particion.csv, con semilla fija en particion y modelos.

### 8. Informe y presentación

Estado: Cumple. En riesgo: 0 de 15.

Estan el informe con todas las secciones pedidas y la presentacion; la exposicion en vivo no se puede revisar desde los archivos.

Según las instrucciones:
- L042: "Informe y presentación"
- L030: "Informe breve (Oct 21, 2026): problema, datos, decisiones de preprocesamiento, comparación de modelos, análisis de errores y limitaciones."
- L031: "Presentación (Oct 21, 2026): presentación de su trabajo"

Evidencia revisada:
- `Informe-Proyecto2.docx`: Cubre problema, datos, decisiones de preprocesamiento, comparacion de modelos, evaluacion final, analisis de errores, limitaciones, conclusiones y referencias.
- `Presentacion-Proyecto2.pptx`: 13 diapositivas con notas del orador que recorren problema, datos, preprocesamiento, modelos, evaluacion, errores, sesgos, limitaciones y conclusiones.
- `Guion-Presentacion.docx`: Guion con reparto por integrante, tiempos y preguntas probables.

### 9. Declaración del uso de IA en el informe

Estado: Cumple. En riesgo: sin puntos.

El informe declara herramienta, usos y lo verificado manualmente, por lo que no aplica la penalizacion por IA no declarada.

Según las instrucciones:
- L032: "El informe indica qué herramienta se usó, para qué y qué se verificó a mano."
- L044: "Penalizaciones: Uso de IA no declarado, se aplica la política de plagio del curso."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Seccion Uso de inteligencia artificial que nombra la herramienta, para que se uso y cuatro puntos verificados a mano.

### 10. Dataset no usado en laboratorios del curso ni en otros cursos

Estado: No verificable. En riesgo: sin puntos.

No se puede comprobar desde la carpeta si este dataset se uso antes en el curso o en otro curso.

Según las instrucciones:
- L008: "No se aceptan datasets ya usados en los laboratorios del curso o proyectos trabajados en otros cursos."
- L044: "Uso de otros proyectos de otros cursos ya trabajados anteriormente."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Identifica el dataset CDC Diabetes Health Indicators (BRFSS 2015), pero no hay forma de contrastarlo con los datasets de los laboratorios del curso.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Propuesta de media pagina | Oct 5, 2026 | L028 |
| Codigo (notebook o scripts, dataset o script para obtenerlo y README) | Oct 21, 2026 | L029 |
| Informe breve | Oct 21, 2026 | L030 |
| Presentacion | Oct 21, 2026 | L031 |

## Hechos revisados por script

- Aviso: Quedan 0.02 horas para la fecha de entrega (2026-10-26 19:00).
- Aviso: Fechas del texto que ya pasaron: 2026-10-05 (L028), 2026-10-21 (L029), 2026-10-21 (L030), 2026-10-21 (L031). Revisa que esas entregas estén hechas.
- Bien: Ya hay una entrega en Canvas (2026-10-26 18:11).
- Bien: La rúbrica tiene 7 criterios que suman 100 puntos.
- Bien: Todas las instrucciones están en el texto de Canvas.
- Bien: La carpeta tiene 18 archivos.
- Nota: Canvas no restringe los tipos de archivo.
- Nota: La carpeta no es un repositorio git.

## Lo que no se pudo revisar

- Propuesta (L028): no esta en la carpeta y su aprobacion por el catedratico no se puede comprobar aqui.
- Exposicion oral de la presentacion (L031): es una actividad en vivo, fuera de los archivos.
- data/processed/particion.csv no se copio por ser grande, asi que no se pudo revisar su contenido.
- data/raw/diabetes_012_health_indicators_BRFSS2015.csv.zip no se copio por ser binario, asi que no se verifico el dataset en si.
- Ejecucion real de los notebooks de principio a fin: solo se leyo el codigo y las salidas guardadas, no se ejecutaron.
- Enlaces externos del informe (repositorio de GitHub, UCI, Kaggle, CDC): no se abrieron.
- No es un repositorio git, asi que no hay historial para revisar autoria ni fechas.
- Un archivo oculto o con secretos fue omitido del inventario y no se pudo revisar.
- Presentacion-Proyecto2.pptx tiene fecha de modificacion 2026-10-26 20:08, posterior al envio en Canvas (18:11): no se puede confirmar que lo subido sea esa version.

## Validación de la respuesta del agente

Todas las citas son textuales (31) y la evidencia citada existe (24 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
