# Pre-flight: Proyecto 3 - Automatiza algo tuyo con IA

Revisión como si se entregara el 2026-11-18 15:09 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 80 de 100.**

Entregando ahora el riesgo es de unos 80 de 100 puntos. Faltan por completo la lista de tareas (10), la tabla comparativa de exploracion (20), la reflexion (20) y el informe con la presentacion (10). La automatizacion esta construida pero sin justificacion ni screenshots (10 en riesgo), y los casos reales estan definidos sin resultados, analisis de errores ni tiempo ahorrado (10 en riesgo). Ademas Canvas no registra entrega y los commits no estan en origin/main.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Lista de tareas creativa y bien definida | Falta | 10 de 10 | L039 |
| Exploración de 3 herramientas con tabla comparativa | Falta | 20 de 20 | L040 |
| Automatización final funcionando y elección justificada | Parcial | 10 de 25 | L041 |
| Pruebas con casos reales y análisis de errores | Parcial | 10 de 15 | L042 |
| Reflexión: semejanzas y diferencias con los humanos, e implicaciones | Falta | 20 de 20 | L043 |
| Presentación e informe claros | Falta | 10 de 10 | L044 |

### 1. Lista de tareas creativa y bien definida

Estado: Falta. En riesgo: 10 de 10.

No hay en la carpeta ninguna lista de al menos 5 tareas con su descripción, su uso y su criterio de "bien hecha"; solo se menciona de paso que la automatización es la tarea 1.

Según las instrucciones:
- L039: "Lista de tareas creativa y bien definida | 10"
- L007: "Hagan una lista de al menos 5 tareas reales y repetitivas de su vida que les gustaría automatizar"
- L008: "Cada tarea se describe, el uso y con qué cuenta como "bien hecha""

Evidencia revisada:
- `README.md`: Menciona "Es la tarea 1 de mi lluvia de ideas" pero no contiene la lista de tareas ni su descripción.
- `casos/casos.yaml`: Lista casos de prueba de la herramienta, no tareas de la lluvia de ideas con uso y criterio de "bien hecha".

### 2. Exploración de 3 herramientas con tabla comparativa

Estado: Falta. En riesgo: 20 de 20.

No existe la tabla comparativa ni documentación de los casos explorados con las 3 herramientas; la carpeta de exploración referida en el README no está en la entrega.

Según las instrucciones:
- L040: "Exploración de 3 herramientas con tabla comparativa | 20"
- L011: "Prueben al menos 3 herramientas de IA distintas con tareas de su lista."
- L013: "Documenten los resultados en una tabla comparativa: herramienta, tarea intentada, si funcionó, qué tan fácil fue, gratis o de pago, y una observación."
- L015: "Se deben entregar al menos 6 casos explorados de forma rápida."

Evidencia revisada:
- `README.md`: La sección "Por qué esta herramienta" dice "Pendiente" y remite a una carpeta `exploracion/` que no existe en la entrega.
- `inventario.txt`: Los 41 archivos son código, tests, configuración y README; no hay ningún documento de exploración.

### 3. Automatización final funcionando y elección justificada

Estado: Parcial. En riesgo: 10 de 25.

La automatización está construida y documentada para reproducirla, pero falta la justificación de la combinación herramienta/tarea y no hay screenshots del proceso ni el camino seguido documentado.

Según las instrucciones:
- L041: "Automatización final funcionando y elección justificada | 25"
- L018: "Justifiquen por qué eligieron esa combinación a partir de lo que encontraron en la exploración."
- L032: "Tomar varios screenshots de su proceso y documentar el camino seguido."

Evidencia revisada:
- `preflight/__main__.py`: CLI completa con los subcomandos import, check, audit, report, cases, extract, fetch, list y bookmarklet.
- `README.md`: Explica configuración, uso y reproducción, pero la justificación de la herramienta dice "Pendiente".
- `preflight/prompts/v1.md`: Prompt versionado del agente auditor, parte de la configuración pedida.

### 4. Pruebas con casos reales y análisis de errores

Estado: Parcial. En riesgo: 10 de 15.

Los casos reales están definidos y hay pruebas automatizadas, pero no se documentan los resultados de esas corridas, dónde acierta o falla y por qué, ni la estimación de tiempo ahorrado.

Según las instrucciones:
- L042: "Pruebas con casos reales y análisis de errores | 15"
- L021: "Prueben la automatización con al menos 3 casos reales."
- L022: "Documenten dónde acierta, dónde falla y por qué creen que falla."
- L023: "Estimen cuánto tiempo ahorra frente a hacerlo a mano, incluyendo el tiempo de configurarla."

Evidencia revisada:
- `casos/casos.yaml`: Define 7 casos reales de tareas del curso con lo que ocurrió de verdad y lo esperado de la auditoría.
- `tests/test_cases.py`: Prueba el mecanismo que compara la auditoría con las expectativas de casos.yaml.
- `README.md`: Las secciones "Pruebas", "Resultados" y "Limitaciones" dicen "Pendiente".

### 5. Reflexión: semejanzas y diferencias con los humanos, e implicaciones

Estado: Falta. En riesgo: 20 de 20.

No hay reflexión personal en ningún archivo de la entrega, ni sobre semejanzas y diferencias con una persona ni sobre las implicaciones.

Según las instrucciones:
- L043: "Reflexión: semejanzas y diferencias con los humanos, e implicaciones | 20"
- L025: "La presentación y el informe deben incluir una reflexión personal que responda, al menos:"
- L026: "En qué se parece la IA a una persona haciendo esa tarea"
- L027: "En qué no se parece: qué no entiende, qué no recuerda, qué juicio no tiene, qué responsabilidad no asume."
- L028: "Implicaciones: ¿qué dejaron de hacer ustedes y está bien que así sea?"

Evidencia revisada:
- `README.md`: Documentación técnica de la herramienta, sin ninguna reflexión personal.
- `inventario.txt`: No hay ningún documento (md, docx o pdf) de reflexión en la entrega.

### 6. Presentación e informe claros

Estado: Falta. En riesgo: 10 de 10.

No está el informe de 2 a 3 páginas ni ningún archivo de presentación en la entrega; la parte oral o en video no se puede comprobar desde la carpeta.

Según las instrucciones:
- L044: "Presentación e informe claros | 10"
- L033: "Informe breve (Nov 18 2026, 2 a 3 páginas): tarea elegida, por qué esa herramienta, resultados de las pruebas, errores encontrados y reflexión."
- L034: "Presentación (Nov 18, 2026): Hablar de su proceso de escoger la tarea, de su proceso de exploración"

Evidencia revisada:
- `inventario.txt`: Ningún docx, pptx o pdf en la entrega; no se extrajo texto de presentaciones ni informes.
- `README.md`: Es documentación de uso de la herramienta, no el informe de 2 a 3 páginas con resultados, errores y reflexión.
- `casos/casos.yaml`: Un comentario indica que las notas reales van solo en el informe, informe que no está en la carpeta.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Lluvia de ideas: lista de tareas | Nov 2, 2026 | L030 |
| Exploración: lista de tareas y tabla comparativa de las 3 herramientas | Nov 11, 2026 | L031 |
| Automatización: configuración, prompts, scripts o flujos, README y screenshots | Nov 18, 2026 | L032 |
| Informe breve de 2 a 3 páginas | Nov 18 2026 | L033 |
| Presentación con demostración en vivo o en video | Nov 18, 2026 | L034 |

## Hechos revisados por script

- Aviso: Quedan 8.85 horas para la fecha de entrega (2026-11-18 23:59).
- Aviso: Todavía no hay nada entregado en Canvas.
- Aviso: Fechas del texto que ya pasaron: 2026-11-02 (L030), 2026-11-11 (L031). Revisa que esas entregas estén hechas.
- Aviso: 9 commits de la rama fabian/preflight no están en origin/main, la rama que ve quien revisa.
- Bien: La rúbrica tiene 6 criterios que suman 100 puntos.
- Bien: Todas las instrucciones están en el texto de Canvas.
- Bien: La carpeta tiene 41 archivos.
- Bien: No hay cambios sin commit.
- Bien: Todo está subido al remoto.
- Bien: No hay commits después de la fecha de entrega.
- Nota: Canvas no restringe los tipos de archivo.
- Nota: Repositorio git en la rama fabian/preflight.

## Lo que no se pudo revisar

- La presentación en vivo o en video (L034) no se puede comprobar desde la carpeta.
- Los 6 archivos de work/958579 y work/959073 no se copiaron por estar ignorados por git.
- 2 archivos se omitieron por seguridad (archivos ocultos o secretos), así que no se revisó su contenido.
- El estado en Canvas se toma de hechos.json: no hay nada entregado todavía (quedan 8.85 horas).
- La rama del repositorio es fabian/preflight con 9 commits que no están en origin/main, la rama que ven los revisores.

## Validación de la respuesta del agente

Todas las citas son textuales (27) y la evidencia citada existe (15 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
