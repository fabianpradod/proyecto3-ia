# Pre-flight: Proyecto 2 - Machine Learning

Revisión como si se entregara el 2026-10-26 18:59 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 3 de 100.**

La entrega esta casi completa: seis de los siete criterios de la rubrica tienen evidencia clara en el informe, la presentacion y los tres notebooks, incluida la declaracion de uso de IA que evita la penalizacion. El unico hueco es la falta del README con instrucciones que exige L029, lo que pone en riesgo unos 3 de los 10 puntos de "Codigo reproducible y claro". Urge porque quedan minutos para el cierre de las 19:00 y ya hay un intento registrado en Canvas a las 18:11.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Problema bien definido y dataset con origen documentado (propuesta aprobada) | Cumple | 0 de 10 | L036 |
| Análisis exploratorio y preprocesamiento justificado | Cumple | 0 de 15 | L037 |
| Baseline y al menos 3 modelos, con búsqueda de hiperparámetros | Cumple | 0 de 20 | L038 |
| Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste | Cumple | 0 de 20 | L039 |
| Análisis de errores, limitaciones y sesgos | Cumple | 0 de 10 | L040 |
| Código reproducible y claro | Parcial | 3 de 10 | L041 |
| Informe y presentación | Cumple | 0 de 15 | L042 |
| Declaración del uso de IA en el informe | Cumple | - | L032 |
| Propuesta previa de media página | No verificable | - | L011 |

### 1. Problema bien definido y dataset con origen documentado (propuesta aprobada)

Estado: Cumple. En riesgo: 0 de 10.

El problema, la variable objetivo, el tamano del dataset y el origen con fuente, licencia y fecha estan documentados en informe y notebook.

Según las instrucciones:
- L036: "Problema bien definido y dataset con origen documentado (propuesta aprobada)"
- L009: "Origen documentado: fuente, licencia y fecha de obtención. Los datos personales deben anonimizarse."
- L007: "Al menos 500 filas y 5 variables predictoras."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Problema, variable objetivo de 3 clases y metrica principal definidos; fuente UCI #891 y version de Kaggle con licencias CC BY 4.0 y CC0, fecha de obtencion octubre 2026 y nota de ausencia de identificadores personales.
- `notebooks/01_EDA.ipynb`: Celda de fuente con enlaces a UCI y Kaggle, diccionario de variables y carga que muestra 253,680 filas y 21 predictoras.

### 2. Análisis exploratorio y preprocesamiento justificado

Estado: Cumple. En riesgo: 0 de 15.

Hay mas de tres visualizaciones que derivan en decisiones y cada decision de limpieza, codificacion, escalado y desbalance viene justificada.

Según las instrucciones:
- L037: "Análisis exploratorio y preprocesamiento justificado"
- L013: "Explorar la distribución de la variable objetivo, valores faltantes y outliers, con al menos 3 visualizaciones que informen decisiones posteriores."
- L014: "Limpiar, codificar variables categóricas, escalar cuando el modelo lo requiera y tratar el desbalance si existe."
- L015: "Justificar cada decisión."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Cuatro figuras con salida guardada (distribucion de clases, IMC por clase, correlacion de Spearman, factores de riesgo), revision de faltantes, rangos, duplicados y outliers, mas una tabla final de hallazgo-decision.
- `Informe-Proyecto2.docx`: Seccion de decisiones de preprocesamiento con tipos, faltantes, duplicados, outliers, codificacion sin one-hot, StandardScaler en pipeline y pesos de clase en lugar de SMOTE, cada una con su razon.

### 3. Baseline y al menos 3 modelos, con búsqueda de hiperparámetros

Estado: Cumple. En riesgo: 0 de 20.

Estan el baseline trivial, el baseline simple y tres algoritmos adicionales, cada uno con busqueda de hiperparametros validada por validacion cruzada.

Según las instrucciones:
- L038: "Baseline y al menos 3 modelos, con búsqueda de hiperparámetros"
- L017: "Implementar un baseline trivial (clase mayoritaria o media) y uno simple (regresión lineal o logística)."
- L018: "Entrenar al menos 3 algoritmos vistos en clase o investigados por ustedes"
- L019: "Realizar búsqueda de hiperparámetros con validaciones."

Evidencia revisada:
- `notebooks/02_Baselines_Arbol.ipynb`: DummyClassifier de clase mayoritaria, regresion logistica en pipeline con GridSearchCV y arbol de decision con malla de hiperparametros, todo sobre StratifiedKFold de 5 particiones.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Random forest y gradient boosting con RandomizedSearchCV y la misma validacion cruzada, con seccion de comparacion de los cinco modelos.
- `resultados/mejores_hiperparametros_integrante2.json`: Archivo con los mejores hiperparametros encontrados en la busqueda.

### 4. Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste

Estado: Cumple. En riesgo: 0 de 20.

Hay particion estratificada con validacion cruzada, test usado una sola vez, metrica justificada por el costo de los errores, matriz de confusion y brechas de sobreajuste por modelo.

Según las instrucciones:
- L039: "Evaluación correcta: partición, métrica justificada y diagnóstico de sobreajuste"
- L021: "Particionar en train, validación y test, o usar validación cruzada. El test se usa una sola vez, al final."
- L022: "Elegir y justificar la métrica principal según el costo de los errores del problema."
- L023: "Presentar matriz de confusión y métricas que consideren importantes."

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Particion estratificada 80/20 con semilla fija guardada en data/processed/particion.csv antes del analisis.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Seccion de eleccion del modelo final y evaluacion unica en prueba, con metricas por clase e importancia por permutacion.
- `Informe-Proyecto2.docx`: Justificacion del F1 macro por el costo de no detectar diabetes, tabla con brecha entrenamiento-validacion por modelo y resultados de prueba.
- `resultados/figuras/matriz_confusion_test.png`: Matriz de confusion del modelo final en el conjunto de prueba.

### 5. Análisis de errores, limitaciones y sesgos

Estado: Cumple. En riesgo: 0 de 10.

Hay ejemplos concretos mal clasificados con explicacion propuesta, y discusion de limitaciones y sesgos de recoleccion y etiquetado.

Según las instrucciones:
- L040: "Análisis de errores, limitaciones y sesgos"
- L025: "Analizar ejemplos concretos que el mejor modelo clasifica o predice mal, y proponer por qué."
- L026: "Discutir limitaciones y posibles sesgos en cómo se recolectaron o etiquetaron los datos."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Perfil promedio de aciertos y errores, cinco casos concretos de diabetes no detectada y cinco de falsa alarma con hipotesis, tabla de desempeno por subgrupo y lista de limitaciones sobre etiqueta autorreportada y poblacion.
- `notebooks/03_Modelos_Evaluacion.ipynb`: Secciones de analisis de errores, prediabetes, desempeno por subgrupos como posibles sesgos y conclusiones con limitaciones.

### 6. Código reproducible y claro

Estado: Parcial. En riesgo: 3 de 10.

Falta el README con instrucciones que pide L029; el resto del paquete de codigo (notebooks ejecutados, script de obtencion del dataset y dependencias) si esta.

Según las instrucciones:
- L041: "Código reproducible y claro"
- L029: "notebook o scripts que corran de principio a fin, con el dataset o el script para obtenerlo y un README con instrucciones"

Evidencia revisada:
- `notebooks/01_EDA.ipynb`: Notebook con salidas ejecutadas, semilla fija y rutas relativas, pero sin seccion de instrucciones de instalacion ni de orden de ejecucion.
- `scripts/descargar_datos.py`: Script de descarga con verificacion SHA-256 y docstring de uso.
- `requirements.txt`: Lista de dependencias con versiones minimas.

### 7. Informe y presentación

Estado: Cumple. En riesgo: 0 de 15.

El informe cubre los seis apartados exigidos y la presentacion esta en la carpeta; la exposicion en vivo no se puede revisar desde archivos.

Según las instrucciones:
- L042: "Informe y presentación"
- L030: "problema, datos, decisiones de preprocesamiento, comparación de modelos, análisis de errores y limitaciones"
- L031: "Presentación (Oct 21, 2026): presentación de su trabajo"

Evidencia revisada:
- `Informe-Proyecto2.docx`: Informe con las seis secciones pedidas, tablas de resultados y referencias.
- `Presentacion-Proyecto2.pptx`: Trece diapositivas con notas del orador que cubren problema, datos, preprocesamiento, modelos, evaluacion, errores, limitaciones y conclusiones.
- `Guion-Presentacion.docx`: Guion con reparto, tiempos y preguntas probables.

### 8. Declaración del uso de IA en el informe

Estado: Cumple. En riesgo: sin puntos.

La declaracion incluye herramienta, para que se uso y que se verifico manualmente, por lo que no se activa la penalizacion.

Según las instrucciones:
- L032: "El informe indica qué herramienta se usó, para qué y qué se verificó a mano."
- L044: "Penalizaciones: Uso de IA no declarado, se aplica la política de plagio del curso."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Seccion de uso de inteligencia artificial con la herramienta, los usos concretos y cuatro puntos verificados a mano.

### 9. Propuesta previa de media página

Estado: No verificable. En riesgo: sin puntos.

La propuesta era un entregable anterior y separado; no esta en esta carpeta y su aprobacion no se puede comprobar aqui.

Según las instrucciones:
- L011: "cada grupo entrega una propuesta de media página con problema, variable objetivo, fuente de datos y métrica principal"
- L028: "Propuesta (Oct 5, 2026): media página con problema, variable objetivo, fuente de datos y métrica principal."

Evidencia revisada:
- `Informe-Proyecto2.docx`: Se menciona que la regla de eleccion del modelo venia definida en la propuesta, pero el documento de la propuesta no esta en la carpeta.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Propuesta de media página | Oct 5, 2026 | L028 |
| Código (notebook o scripts, dataset o script de obtención y README) | Oct 21, 2026 | L029 |
| Informe breve | Oct 21, 2026 | L030 |
| Presentación | Oct 21, 2026 | L031 |

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

- data/processed/particion.csv no se copio por tamano, asi que no se pudo revisar su contenido.
- data/raw/diabetes_012_health_indicators_BRFSS2015.csv.zip no se copio por ser binario; no se pudo comprobar el dataset en si.
- 1 archivo quedo omitido por seguridad (oculto o con secretos) segun el inventario.
- No se pudo ejecutar los notebooks, asi que la afirmacion de que corren de principio a fin solo se apoya en las salidas guardadas.
- La exposicion oral de la presentacion es en vivo y no se puede revisar desde la carpeta.
- El repositorio de GitHub citado en el informe y los enlaces a UCI y Kaggle son externos y no se consultaron.
- La aprobacion de la propuesta por el catedratico ocurre fuera de la carpeta.
- No se puede saber que version se subio a Canvas: el archivo mas reciente de la carpeta (Presentacion-Proyecto2.pptx) figura modificado el 2026-10-26 20:08, despues de la entrega registrada a las 18:11.
- No es un repositorio git, asi que no hay historial para revisar.

## Validación de la respuesta del agente

Todas las citas son textuales (31) y la evidencia citada existe (21 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
