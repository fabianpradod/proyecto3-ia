# Pre-flight: Proyecto 3 - Automatiza algo tuyo con IA

Revisión como si se entregara el 2026-11-18 15:14 (hora de Guatemala).
Modelo: claude-opus-5. Prompt: v1. La carpeta no cambió durante la revisión.

## Resumen

**Puntos en riesgo: 78 de 100.**

Si se enviara ahora, el riesgo es de unos 78 de 100 puntos: faltan la lista de tareas (10), la tabla de exploración (20), la reflexión (20) y el informe con la presentación (10); están a medias la justificación de la elección (8 de 25) y las pruebas documentadas con tiempo ahorrado (10 de 15). Lo entregado es solo el código con su README, cuyas secciones de justificación, pruebas y resultados dicen \"Pendiente\", y sin screenshots. Quedan 8.76 horas y Canvas no tiene nada entregado.

## Criterios

| Criterio | Estado | En riesgo | Línea |
|---|---|---|---|
| Lista de tareas creativa y bien definida | Falta | 10 de 10 | L007 |
| Exploración de 3 herramientas con tabla comparativa | Falta | 20 de 20 | L011 |
| Automatización final funcionando y elección justificada | Parcial | 8 de 25 | L017 |
| Pruebas con casos reales y análisis de errores | Parcial | 10 de 15 | L021 |
| Reflexión: semejanzas y diferencias con los humanos, e implicaciones | Falta | 20 de 20 | L025 |
| Presentación e informe claros | Falta | 10 de 10 | L033 |
| Entregable de automatización: README de reproducción, screenshots y camino seguido | Parcial | - | L032 |

### 1. Lista de tareas creativa y bien definida

Estado: Falta. En riesgo: 10 de 10.

No aparece en la carpeta ninguna lista de al menos 5 tareas con su descripción, uso y criterio de "bien hecha".

Según las instrucciones:
- L007: "Hagan una lista de al menos 5 tareas reales y repetitivas de su vida que les gustaría automatizar"
- L008: "Cada tarea se describe, el uso y con qué cuenta como "bien hecha""
- L039: "Lista de tareas creativa y bien definida | 10"

Evidencia revisada:
- `README.md`: Solo menciona "Es la tarea 1 de mi lluvia de ideas", sin la lista ni la descripción de cada tarea.
- `casos/casos.yaml`: Lista casos de prueba de la herramienta, no tareas de la vida del estudiante.

### 2. Exploración de 3 herramientas con tabla comparativa

Estado: Falta. En riesgo: 20 de 20.

No hay tabla comparativa ni registro de los casos explorados con las distintas herramientas.

Según las instrucciones:
- L011: "Prueben al menos 3 herramientas de IA distintas con tareas de su lista"
- L013: "Documenten los resultados en una tabla comparativa: herramienta, tarea intentada, si funcionó, qué tan fácil fue, gratis o de pago, y una observación"
- L015: "Se deben entregar al menos 6 casos explorados de forma rápida"
- L040: "Exploración de 3 herramientas con tabla comparativa | 20"

Evidencia revisada:
- `README.md`: Remite a una carpeta `exploracion/` que no existe en la entrega y marca la sección como "Pendiente".
- `casos/casos.yaml`: Anota que la tabla de exploración todavía no está en el repositorio.

### 3. Automatización final funcionando y elección justificada

Estado: Parcial. En riesgo: 8 de 25.

La automatización está construida y es ejecutable, pero falta la justificación de la elección de herramienta y tarea a partir de la exploración.

Según las instrucciones:
- L017: "Elijan una herramienta y una tarea, y construyan la automatización completa"
- L018: "Justifiquen por qué eligieron esa combinación a partir de lo que encontraron en la exploración"
- L019: "La automatización debe funcionar de verdad, no solo como idea"
- L041: "Automatización final funcionando y elección justificada | 25"

Evidencia revisada:
- `preflight/__main__.py`: Comandos completos (import, extract, check, audit, report) de la automatización construida.
- `README.md`: Explica qué hace y cómo correrla, pero la sección "Por qué esta herramienta" dice "Pendiente".
- `tests/test_audit.py`: Pruebas automatizadas del flujo de auditoría, señal de que la automatización corre.

### 4. Pruebas con casos reales y análisis de errores

Estado: Parcial. En riesgo: 10 de 15.

Los casos reales están definidos, pero no hay resultados documentados de aciertos y fallos con su explicación ni la estimación de tiempo ahorrado.

Según las instrucciones:
- L021: "Prueben la automatización con al menos 3 casos reales"
- L022: "Documenten dónde acierta, dónde falla y por qué creen que falla"
- L023: "Estimen cuánto tiempo ahorra frente a hacerlo a mano, incluyendo el tiempo de configurarla"
- L042: "Pruebas con casos reales y análisis de errores | 15"

Evidencia revisada:
- `casos/casos.yaml`: Define 7 casos reales con expectativas escritas antes de correr la auditoría.
- `preflight/cases.py`: Corre los casos y genera un archivo de resultados, pero ese resultado no está en la entrega.
- `README.md`: Las secciones "Pruebas", "Resultados" y "Limitaciones" dicen "Pendiente".

### 5. Reflexión: semejanzas y diferencias con los humanos, e implicaciones

Estado: Falta. En riesgo: 20 de 20.

No hay ningún texto de reflexión personal sobre semejanzas, diferencias e implicaciones.

Según las instrucciones:
- L025: "La presentación y el informe deben incluir una reflexión personal que responda, al menos"
- L026: "En qué se parece la IA a una persona haciendo esa tarea"
- L027: "En qué no se parece: qué no entiende, qué no recuerda, qué juicio no tiene, qué responsabilidad no asume"
- L028: "Implicaciones: ¿qué dejaron de hacer ustedes y está bien que así sea?"
- L043: "Reflexión: semejanzas y diferencias con los humanos, e implicaciones | 20"

Evidencia revisada:
- `README.md`: Es documentación técnica de uso; no contiene reflexión personal.
- `casos/casos.yaml`: Anota que la reflexión todavía no está en el repositorio.

### 6. Presentación e informe claros

Estado: Falta. En riesgo: 10 de 10.

No hay informe ni archivo de presentación en la carpeta; la parte oral o en video queda fuera de lo revisable.

Según las instrucciones:
- L033: "Informe breve (Nov 18 2026, 2 a 3 páginas): tarea elegida, por qué esa herramienta, resultados de las pruebas, errores encontrados y reflexión"
- L034: "Presentación (Nov 18, 2026): Hablar de su proceso de escoger la tarea, de su proceso de exploración"
- L044: "Presentación e informe claros | 10"

Evidencia revisada:
- `README.md`: Único documento de la entrega; no es el informe de 2 a 3 páginas pedido.
- `casos/casos.yaml`: Anota que el informe y la presentación todavía no están en el repositorio.

### 7. Entregable de automatización: README de reproducción, screenshots y camino seguido

Estado: Parcial. En riesgo: sin puntos.

Están el README reproducible, los scripts y el prompt, pero no hay screenshots del proceso ni documentación del camino seguido.

Según las instrucciones:
- L032: "configuración, prompts, scripts o flujos usados, con un README que explique cómo reproducirla"
- L032: "Tomar varios screenshots de su proceso y documentar el camino seguido"

Evidencia revisada:
- `README.md`: Explica configuración, uso y validación, suficiente para reproducir la automatización.
- `preflight/prompts/v1.md`: Prompt versionado incluido en la entrega.
- `preflight/schema.json`: Esquema que exige el flujo, parte de la configuración entregada.

## Fechas en las instrucciones

| Entregable | Fecha | Línea |
|---|---|---|
| Lluvia de ideas: lista de tareas | Nov 2, 2026 | L030 |
| Exploración: lista de tareas y tabla comparativa de las 3 herramientas | Nov 11, 2026 | L031 |
| Automatización: configuración, prompts, scripts o flujos, README y screenshots | Nov 18, 2026 | L032 |
| Informe breve de 2 a 3 páginas | Nov 18 2026 | L033 |
| Presentación con demostración en vivo o en video | Nov 18, 2026 | L034 |

## Hechos revisados por script

- Aviso: Quedan 8.76 horas para la fecha de entrega (2026-11-18 23:59).
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

- La demostración en vivo o en video de la automatización (L034) ocurre fuera de la carpeta y no se puede comprobar con archivos.
- Que el informe y la reflexión hayan sido escritos por el estudiante y no por la herramienta (L035) no se puede comprobar desde los archivos.
- Los archivos de work/958579/ y work/959073/ (assignment.json, meta.json, spec.md) no se copiaron por estar ignorados por git.
- 2 archivos se omitieron por seguridad (ocultos o con secretos), así que su contenido no se revisó.
- Estado en Canvas: no hay nada entregado todavía; eso viene del hecho verificado, no de la carpeta.
- Git: la entrega vive en la rama fabian/preflight con 9 commits que no están en origin/main, la rama que ve quien revisa; no se pudo ver el contenido de origin/main.

## Validación de la respuesta del agente

Todas las citas son textuales (30) y la evidencia citada existe (17 entradas).

---

Este reporte no hace la tarea: solo señala qué falta según las instrucciones.
