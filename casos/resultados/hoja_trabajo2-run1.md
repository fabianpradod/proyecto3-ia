# Pre-flight: Presentación Algoritmo de Machine Learning en Parejas - Hoja de trabajo 2

Revisión como si se entregara el 2026-08-24 20:29 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

Las instrucciones no tienen puntos por criterio.

Las instrucciones no traen tabla de puntos, asi que no hay puntos cuantificables en riesgo; el riesgo esta en los entregables formales. Falta el PDF de las slides y el link al Colab (L006) y el notebook de la demo (L005, L024): la carpeta solo contiene un .pptx. El contenido cubre los cuatro algoritmos del Tema 8 y las siete secciones, aunque agrupadas por algoritmo y no en la secuencia de L018. Con el plazo casi vencido y un intento ya enviado, lo urgente es el PDF y el enlace al notebook.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Formato: slides + notebook de Google Colab ejecutable con dataset real | Parcial | - | L005 |
| Entrega: PDF de las slides y link al Colab compartido | Falta | - | L006 |
| Tema 8 asignado al Grupo 4: K-Means + K-Medianas + K-Medoids + Fuzzy K-Means | Cumple | - | L016 |
| Seccion: que problema resuelve, tipo de tarea y cuando aplica | Cumple | - | L019 |
| Seccion: la intuicion sin ecuaciones, con analogia o ejemplo cotidiano | Cumple | - | L020 |
| Seccion: como funciona paso a paso, con al menos un ejemplo numerico resuelto a mano | Cumple | - | L021 |
| Seccion: hiperparametros clave y su efecto | Cumple | - | L022 |
| Seccion: fortalezas y limitaciones, cuando usarlo y cuando no | Cumple | - | L023 |
| Seccion: demo en Colab con dataset real, modelo entrenado y al menos una metrica discutida | Parcial | - | L024 |
| Seccion: conexion con el curso | Cumple | - | L025 |
| Cubrir las secciones obligatorias en orden | Parcial | - | L018 |
| Duracion aproximada de 30 minutos mas 5 de preguntas | No verificable | - | L004 |
| Trabajo en parejas: ambos integrantes deben poder responder cualquier pregunta | No verificable | - | L007 |

### 1. Formato: slides + notebook de Google Colab ejecutable con dataset real

Estado: Parcial. En riesgo: sin puntos.

Las slides estan, pero el notebook de Colab ejecutable no aparece en la entrega ni como archivo ni como enlace.

Según las instrucciones:
- L005: "Formato: slides (cualquier herramienta) + notebook de Google Colab ejecutable con un dataset real"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Deck completo de 31 diapositivas con notas del orador; ninguna contiene un enlace a Colab, solo una URL de GitHub en la portada.
- `(carpeta de la entrega)`: hechos.json y inventario.txt registran un unico archivo .pptx: no hay notebook ni .ipynb.

> Aviso: la validación encontró problemas en este criterio.

### 2. Entrega: PDF de las slides y link al Colab compartido

Estado: Falta. En riesgo: sin puntos.

No se entrego el PDF de las slides ni el link al Colab compartido que pide la linea.

Según las instrucciones:
- L006: "Entrega: PDF de las slides y link al Colab compartido antes de la sesión de presentación"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: El unico archivo entregado esta en formato pptx, no en PDF.
- `(carpeta de la entrega)`: hechos.json reporta 1 archivo con extension .pptx y ningun enlace externo detectado en el texto.

### 3. Tema 8 asignado al Grupo 4: K-Means + K-Medianas + K-Medoids + Fuzzy K-Means

Estado: Cumple. En riesgo: sin puntos.

Los cuatro algoritmos del tema asignado estan cubiertos con bloque propio cada uno.

Según las instrucciones:
- L016: "Grupo 4 - Tema 8 — K-Means + K-Medianas + K-Medoids + Fuzzy K-Means"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Bloques dedicados a K-Means (diapositivas 5-10), Fuzzy K-Means (11-16), K-Medianas (17-22) y K-Medoids (23-28), mas una comparacion de los cuatro.

### 4. Seccion: que problema resuelve, tipo de tarea y cuando aplica

Estado: Cumple. En riesgo: sin puntos.

La seccion aparece completa con tipo de tarea y casos de aplicacion.

Según las instrucciones:
- L019: "- ¿Qué problema resuelve? — tipo de tarea (clasificación, regresión, clustering) y cuándo aplica"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositiva 3 identifica el aprendizaje no supervisado y lista cuando aplica y cuando no aplica.

### 5. Seccion: la intuicion sin ecuaciones, con analogia o ejemplo cotidiano

Estado: Cumple. En riesgo: sin puntos.

Hay una analogia cotidiana concreta y sin formulas, como pide la linea.

Según las instrucciones:
- L020: "- La intuición — sin ecuaciones primero; una analogía o ejemplo cotidiano concreto"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositiva 4 desarrolla la analogia de los food trucks sin ecuaciones.

### 6. Seccion: como funciona paso a paso, con al menos un ejemplo numerico resuelto a mano

Estado: Cumple. En riesgo: sin puntos.

El algoritmo paso a paso y el ejemplo numerico a mano estan presentes para los cuatro algoritmos.

Según las instrucciones:
- L021: "- Cómo funciona — el algoritmo paso a paso, con al menos un ejemplo numérico simple resuelto a mano"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositivas 6, 13, 18 y 25 describen el bucle paso a paso; diapositivas 8, 14, 19 y 26 resuelven a mano el mismo ejemplo de seis puntos con iteraciones y valores de J.

### 7. Seccion: hiperparametros clave y su efecto

Estado: Cumple. En riesgo: sin puntos.

Cada bloque incluye sus hiperparametros con la explicacion del efecto.

Según las instrucciones:
- L022: "- Hiperparámetros clave — qué se puede ajustar y qué efecto tiene"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositivas 9, 15, 21 y 27 cubren k, inicializacion, n_init, el fuzzifier m, la metrica de distancia y las variantes de PAM con su efecto.

### 8. Seccion: fortalezas y limitaciones, cuando usarlo y cuando no

Estado: Cumple. En riesgo: sin puntos.

Fortalezas, limitaciones y criterio de eleccion estan desarrollados para los cuatro algoritmos.

Según las instrucciones:
- L023: "- Fortalezas y limitaciones — cuándo usarlo y cuándo no"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositivas 10, 16, 22 y 28 listan fortalezas y limitaciones; la diapositiva 29 agrega una tabla de cuando elegir cada uno.

### 9. Seccion: demo en Colab con dataset real, modelo entrenado y al menos una metrica discutida

Estado: Parcial. En riesgo: sin puntos.

La seccion esta en las slides con dataset real y metricas discutidas, pero el notebook de la demo no forma parte de la entrega.

Según las instrucciones:
- L024: "- Demo en Colab — notebook con dataset real, modelo entrenado y al menos una métrica de evaluación discutida"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositiva 30 describe el dataset de 167 paises y discute ARI y silhouette, pero sus notas indican que las capturas del notebook aun estan por colocar.
- `(carpeta de la entrega)`: No hay notebook ni enlace a Colab entre los archivos entregados.

> Aviso: la validación encontró problemas en este criterio.

### 10. Seccion: conexion con el curso

Estado: Cumple. En riesgo: sin puntos.

La seccion existe y relaciona el tema con los pilares del curso.

Según las instrucciones:
- L025: "- Conexión con el curso"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: Diapositiva 31 conecta el tema con el pilar de Machine Learning y con el pilar de busqueda.

### 11. Cubrir las secciones obligatorias en orden

Estado: Parcial. En riesgo: sin puntos.

Todas las secciones estan, pero no siguen la secuencia unica de 1 a 7 sino un agrupamiento por algoritmo declarado como decision propia.

Según las instrucciones:
- L018: "Todos los grupos deben cubrir estas secciones en orden:"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: La diapositiva 2 declara que las secciones 1, 2, 6 y 7 se ven una sola vez y que 3, 4 y 5 se repiten por algoritmo, en lugar de una secuencia unica de 1 a 7.

### 12. Duracion aproximada de 30 minutos mas 5 de preguntas

Estado: No verificable. En riesgo: sin puntos.

Depende de la presentacion oral y no puede comprobarse con los archivos.

Según las instrucciones:
- L004: "Duración: aprox 30 minutos de presentación + 5 minutos de preguntas del grupo"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: El deck tiene 31 diapositivas con notas extensas, pero la duracion real solo se mide en la sesion en vivo.

### 13. Trabajo en parejas: ambos integrantes deben poder responder cualquier pregunta

Estado: No verificable. En riesgo: sin puntos.

La pareja esta identificada, pero la capacidad de responder de ambos solo se comprueba de forma oral.

Según las instrucciones:
- L007: "Trabajo: en parejas — ambos integrantes deben poder responder cualquier pregunta"

Evidencia revisada:
- `Tema8_Clustering_Grupo4 (3).pptx`: La portada identifica al Grupo 4 con dos integrantes; el dominio individual del contenido solo se evalua en la sesion de preguntas.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| PDF de las slides y link al Colab compartido | antes de la sesión de presentación | L006 |

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

- La presentacion oral de 30 minutos y los 5 minutos de preguntas: ocurren en vivo y no dejan archivo.
- Que ambos integrantes puedan responder cualquier pregunta: se evalua en la defensa oral.
- El notebook de Colab: no hay archivo ni enlace en la carpeta, asi que no se puede revisar su dataset, su ejecucion ni sus metricas.
- El repositorio de GitHub citado en la portada: es un enlace externo que no se visito ni se descargo.
- El texto de la entrada online_text_entry de Canvas: Canvas acepta ese tipo de entrega pero su contenido no esta en la carpeta revisada.
- Control de versiones: hechos.json indica que la carpeta no es un repositorio git, asi que no hay historial que revisar.

## Validación de la respuesta del agente

Se encontraron 2 problemas. Los criterios marcados no son confiables:

- evidencia que no existe: `criterios[0].evidencia[1]` ((carpeta de la entrega) is not in ~/.cache/preflight/casos/ht2)
- evidencia que no existe: `criterios[8].evidencia[1]` ((carpeta de la entrega) is not in ~/.cache/preflight/casos/ht2)

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
