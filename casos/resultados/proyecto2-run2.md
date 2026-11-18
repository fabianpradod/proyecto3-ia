# Pre-flight: Proyecto 2 - Machine Learning

Revisión como si se entregara el 2026-10-26 18:59 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 0 de 100.**

Sin puntos en riesgo por contenido: los 7 criterios de la rubrica (100 puntos) tienen evidencia clara en informe, presentacion, los tres notebooks, README y resultados. Lo urgente es de fechas y sincronizacion: las instrucciones fechan codigo, informe y presentacion el Oct 21 (L029-L031) y la entrega se hizo el 26 de octubre, y la presentacion aparece modificada, con un commit posterior, despues del envio en Canvas de las 18:11. La propuesta del Oct 5 y su aprobacion no estan en la carpeta.

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
| Declaración del uso de IA en el informe (L032, penalización L044) | Cumple | - | L032 |
| Propuesta de media página entregada antes de empezar | No verificable | - | L011 |
| Dataset no usado antes en laboratorios del curso ni en otros cursos | No verificable | - | L008 |

### 1. Problema bien definido y dataset con origen documentado (propuesta aprobada)

Estado: Cumple. En riesgo: 0 de 10.

El problema, la variable objetivo y el origen del dataset con fuente, licencia y fecha están documentados en el informe y el README; la aprobación de la propuesta no es verificable desde la carpeta.

Según las instrucciones:
- L036: "Problema bien definido y dataset con origen documentado (propuesta aprobada) | 10"
- L009: "Origen documentado: fuente, licencia y fecha de obtención. Los datos personales deben anonimizarse."
- L007: "Al menos 500 filas y 5 variables predictoras"

Evidencia revisada:
- `Informe-Proyecto2.docx`: Secciones Problema, Objetivos y Datos: variable objetivo Diabetes_012, 253,680 filas y 21 predictoras, UCI #891 con DOI y CC BY 4.0, versión Kaggle CC0, obtenido en octubre de 2026 y sin identificadores personales.
- `README.md`: Tabla del dataset con nombre, referencia UCI con DOI y licencia, archivo de Kaggle con licencia, fecha de obtención (26 de octubre de 2026) y tamaño.

### 2. Análisis exploratorio y preprocesamiento justificado

Estado: Cumple. En riesgo: 0 de 15.

Hay más de tres visualizaciones que sustentan decisiones y cada decisión de limpieza, codificación, escalado y desbalance viene justificada.

Según las instrucciones:
- L037: "Análisis exploratorio y preprocesamiento justificado | 15"
- L013: "Explorar la distribución de la variable objetivo, valores faltantes y outliers, con al menos 3 visualizaciones que informen decisiones posteriores."
- L014: "Limpiar, codificar variables categóricas, escalar cuando el modelo lo requiera y tratar el desbalance si existe."
- L015: "Justificar cada decisión."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Secciones de tipos de datos, valores faltantes, valores fuera de rango, duplicados, distribución de la variable objetivo, outliers de IMC, correlación y factores de riesgo, con cuatro figuras renderizadas y un resumen de decisiones.
- `Informe-Proyecto2.docx`: Secciones Análisis exploratorio (Figuras 1-3 y Tabla 1) y Decisiones de preprocesamiento con justificación de duplicados, outliers, codificación ordinal, StandardScaler en pipeline y pesos de clase frente a SMOTE.

### 3. Baseline y al menos 3 modelos, con búsqueda de hiperparámetros

Estado: Cumple. En riesgo: 0 de 20.

Están el baseline trivial, el baseline simple y tres algoritmos adicionales (árbol, random forest, gradient boosting), todos con búsqueda de hiperparámetros validada.

Según las instrucciones:
- L038: "Baseline y al menos 3 modelos, con búsqueda de hiperparámetros | 20"
- L017: "Implementar un baseline trivial (clase mayoritaria o media) y uno simple (regresión lineal o logística)."
- L018: "Entrenar al menos 3 algoritmos vistos en clase o investigados por ustedes"
- L019: "Realizar búsqueda de hiperparámetros con validaciones."

Evidencia revisada:
- `notebooks/02_Baselines_Arbol.ipynb`: DummyClassifier de clase mayoritaria, regresión logística con GridSearchCV y árbol de decisión con búsqueda de hiperparámetros sobre validación cruzada.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Random forest y gradient boosting con RandomizedSearchCV y StratifiedKFold de 5 particiones, más la comparación de los cinco modelos.
- `resultados/resultados_integrante2.csv`: Tabla con métricas de validación cruzada de los cinco modelos, incluida la brecha entrenamiento-validación.

### 4. Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste

Estado: Cumple. En riesgo: 0 de 20.

Partición y validación cruzada explícitas con test usado una sola vez, métrica principal justificada por el costo de los errores y diagnóstico de sobreajuste por brecha entrenamiento-validación.

Según las instrucciones:
- L039: "Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste | 20"
- L021: "Particionar en train, validación y test, o usar validación cruzada. El test se usa una sola vez, al final."
- L022: "Elegir y justificar la métrica principal según el costo de los errores del problema."
- L023: "Presentar matriz de confusión y métricas que consideren importantes."

Evidencia revisada:
- `notebooks/03_Modelos_Evaluacion.ipynb`: Partición 80/20 estratificada compartida, StratifiedKFold de 5 particiones, evaluación única en prueba con classification_report y ConfusionMatrixDisplay (conteos y normalizada).
- `Informe-Proyecto2.docx`: Justificación del F1 macro por el desbalance y el costo de los errores, sección Comparación y diagnóstico de sobreajuste con la brecha por modelo, y Tabla 3 con métricas por clase en prueba.
- `resultados/figuras/matriz_confusion_test.png`: Figura de la matriz de confusión del modelo final en el conjunto de prueba.

### 5. Análisis de errores, limitaciones y sesgos

Estado: Cumple. En riesgo: 0 de 10.

Hay ejemplos concretos de errores con explicación propuesta y una discusión de limitaciones y sesgos de recolección y etiquetado.

Según las instrucciones:
- L040: "Análisis de errores, limitaciones y sesgos | 10"
- L025: "Analizar ejemplos concretos que el mejor modelo clasifica o predice mal, y proponer por qué."
- L026: "Discutir limitaciones y posibles sesgos en cómo se recolectaron o etiquetaron los datos."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Sección Análisis de errores con perfiles de aciertos y errores (Tabla 4), cinco ejemplos concretos de diabetes no detectada y de falsas alarmas con hipótesis, desempeño por subgrupos (Tabla 5) y sección Limitaciones.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Secciones Análisis de errores, Prediabetes, Desempeño por subgrupos (posibles sesgos) e Importancia de las variables.

### 6. Código reproducible y claro

Estado: Cumple. En riesgo: 0 de 10.

Están los notebooks con salidas, el dataset incluido y un script para obtenerlo, el README con instrucciones y las semillas fijas; la ejecución de principio a fin no se comprobó corriendo el código.

Según las instrucciones:
- L041: "Código reproducible y claro | 10"
- L029: "notebook o scripts que corran de principio a fin, con el dataset o el script para obtenerlo y un README con instrucciones."

Evidencia revisada:
- `README.md`: Instrucciones de instalación, orden de ejecución de los tres notebooks, comando de nbconvert, tiempos aproximados y explicación de la partición compartida.
- `scripts/descargar_datos.py`: Script que descarga el dataset desde Kaggle y verifica el SHA-256 del archivo usado.
- `requirements.txt`: Dependencias con versiones mínimas (numpy, pandas, scikit-learn, matplotlib, seaborn, jupyter, kaggle).
- `notebooks/03_Modelos_Evaluacion.ipynb`: Semilla fija en particiones, búsquedas y modelos, y rutas que funcionan desde la raíz o desde notebooks/.

### 7. Informe y presentación

Estado: Cumple. En riesgo: 0 de 15.

El informe cubre las seis secciones pedidas y la presentación existe; la exposición oral y el guion no se pueden revisar desde la carpeta.

Según las instrucciones:
- L042: "Informe y presentación | 15"
- L030: "problema, datos, decisiones de preprocesamiento, comparación de modelos, análisis de errores y limitaciones."
- L031: "Presentación (Oct 21, 2026): presentación de su trabajo"

Evidencia revisada:
- `Informe-Proyecto2.docx`: Informe con problema, datos, análisis exploratorio, decisiones de preprocesamiento, comparación de modelos, evaluación final, análisis de errores, limitaciones, conclusiones y referencias.
- `Presentacion-Proyecto2.pptx`: Trece diapositivas con problema, datos, preprocesamiento, modelos, evaluación en prueba, errores, sesgos, limitaciones y conclusiones, cada una con notas del orador.

### 8. Declaración del uso de IA en el informe (L032, penalización L044)

Estado: Cumple. En riesgo: sin puntos.

El informe declara la herramienta, los usos y lo verificado manualmente, por lo que no aplica la penalización por IA no declarada.

Según las instrucciones:
- L032: "El informe indica qué herramienta se usó, para qué y qué se verificó a mano."
- L044: "Penalizaciones: Uso de IA no declarado, se aplica la política de plagio del curso."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Sección Uso de inteligencia artificial: nombra la herramienta, para qué se usó en notebooks e informe y lista cuatro puntos verificados a mano.

### 9. Propuesta de media página entregada antes de empezar

Estado: No verificable. En riesgo: sin puntos.

La propuesta fue un entregable anterior y separado: no está en la carpeta, así que no se puede comprobar su contenido ni su aprobación.

Según las instrucciones:
- L011: "Antes de empezar, cada grupo entrega una propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal."
- L028: "Propuesta (Oct 5, 2026): media página con problema, variable objetivo, fuente de datos y métrica principal."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Menciona la regla de elección del modelo definida en la propuesta, pero el documento de la propuesta no está entre los archivos de la entrega.
- `Presentacion-Proyecto2.pptx`: Las notas de la diapositiva 9 citan la regla de la propuesta; tampoco incluye el documento.

### 10. Dataset no usado antes en laboratorios del curso ni en otros cursos

Estado: No verificable. En riesgo: sin puntos.

No hay información en la carpeta que permita comprobar si este dataset se usó antes en el curso o en otro curso.

Según las instrucciones:
- L008: "No se aceptan datasets ya usados en los laboratorios del curso o proyectos trabajados en otros cursos."
- L044: "Uso de otros proyectos de otros cursos ya trabajados anteriormente."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Documenta el origen del dataset (BRFSS 2015 del CDC vía UCI y Kaggle) pero no hay forma de contrastarlo con los datasets usados en laboratorios u otros cursos.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Propuesta de media página | Oct 5, 2026 | L028 |
| Código (notebook o scripts, dataset o script para obtenerlo y README) | Oct 21, 2026 | L029 |
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

- Guion-Presentacion.docx: no se copió por estar ignorado por git, así que no se pudo revisar su contenido.
- data/raw/diabetes_012_health_indicators_BRFSS2015.csv.zip: no se copió por ser binario; no se pudo verificar el contenido del dataset.
- data/processed/particion.csv: no se copió por tamaño; no se pudo comprobar la partición generada.
- 1 archivo omitido por seguridad (oculto o con secretos) que no se pudo inspeccionar.
- Documento de la propuesta (Oct 5) y su aprobación por el catedrático: no están en la carpeta de la entrega.
- Ejecución real de los tres notebooks de principio a fin: solo se vieron las salidas guardadas, no se corrió el código.
- Exposición oral de la presentación: no es revisable desde archivos.
- Si el dataset ya se usó en laboratorios del curso o en otros cursos: no hay información en la carpeta para comprobarlo.
- Enlaces externos del informe y el README (UCI, Kaggle, CDC, repositorio de GitHub): no se consultaron.
- Si el archivo adjunto en Canvas (entrega de las 18:11) corresponde a la versión local actual de Presentacion-Proyecto2.pptx, modificada después según los hechos.

## Validación de la respuesta del agente

Todas las citas son textuales (33) y la evidencia citada existe (22 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
