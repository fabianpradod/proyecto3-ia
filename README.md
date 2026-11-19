# Pre-flight: revisar una entrega antes de enviarla

Proyecto 3 de Inteligencia Artificial (UVG, 2026): "Automatiza algo tuyo con IA".
Es la tarea 1 de mi [lluvia de ideas](lluvia-de-ideas.md). El informe está en
[informe/Informe-Proyecto3.docx](informe/Informe-Proyecto3.docx) (también en
[Markdown](informe/informe.md)) y la reflexión aparte en
[informe/Reflexion-Proyecto3.docx](informe/Reflexion-Proyecto3.docx).

## Qué hace

Lee una tarea de Canvas (instrucciones y rúbrica), revisa la carpeta o el repositorio
de la entrega y reporta qué puntos se perderían si se entregara en ese momento. También
saca las fechas y los entregables que solo aparecen en el texto de la tarea.

Cada observación cita la parte de la instrucción o de la rúbrica en la que se basa. No
hace la tarea ni escribe contenido de la entrega: solo la audita.

## Por qué esta herramienta

Decidí usar Claude Code porque pago la suscripción Pro y ya trabajo en este entorno, lo que
me llevó a elegirlo. Pero decidí usar Opus en vez de Sonnet por su razonamiento.

Además, la tarea pide revisar una carpeta completa sin tocarla, y Claude Code permite eso de
forma verificable:

- Lee carpetas, busca dentro de los archivos y lee PDF sin código adicional (Read, Grep, Glob).
- Se puede correr sin herramientas de escritura (`--tools Read,Grep,Glob`). La garantía de
  que solo audita la da la herramienta, no una petición en el prompt.
- Corre sin interfaz (`claude -p`), así que un script le pasa una carpeta preparada.
- Obliga a responder con un esquema JSON (`--json-schema`), que después se valida con
  reglas fijas.
- Es de pago: usa la suscripción Pro.

## Cómo funciona

1. Un marcador del navegador guarda de Canvas las instrucciones, la fecha de entrega y el
   estado de la entrega, usando la sesión ya iniciada.
2. Convierte a texto los archivos de la entrega (docx, pptx, pdf), sin tocar la carpeta original.
3. Revisa con reglas fijas lo que no necesita juicio: fechas, archivos y commits.
4. Un agente con permisos de solo lectura compara la entrega con cada criterio.
5. Un script verifica que cada cita exista textual en las instrucciones y que la carpeta
   auditada no haya cambiado.
6. Genera el reporte.

## Requisitos

- Python 3 con las librerías de `requirements.txt`.
- Claude Code (de pago, requiere suscripción).
- Chrome (u otro navegador) con la sesión de Canvas iniciada.

## Configuración

UVG no permite que los estudiantes generen tokens de la API de Canvas, así que los datos
salen del navegador con un marcador (bookmarklet). El marcador solo hace consultas de
lectura (GET) al mismo sitio de Canvas y guarda un archivo JSON en Descargas.

1. Copiar el marcador: `python -m preflight bookmarklet | pbcopy`
2. En Chrome: administrador de marcadores (Cmd+Shift+O) > menú de tres puntos > Agregar
   marcador nuevo. Nombre: `Pre-flight export`. URL: pegar.
3. Abrir la tarea en Canvas y hacer clic en el marcador. Se descarga
   `preflight_<curso>_<tarea>.json`. En la página de tareas del curso, descarga la lista
   completa (`preflight_<curso>_assignments.json`).
4. Si la tarea enlaza archivos (por ejemplo una plantilla o un PDF con la rúbrica),
   descargarlos desde la misma página a la misma carpeta.

Si tu Canvas sí permite tokens, `python -m preflight fetch` y `python -m preflight list`
usan la API directamente: copiar `.env.example` a `~/.config/preflight/.env`, fuera de
este repositorio y de cualquier carpeta auditada, y llenar `CANVAS_TOKEN`.

## Uso

```bash
python -m preflight import ~/Downloads/preflight_46981_959073.json
python -m preflight extract ~/ruta/a/mi/entrega
python -m preflight check 959073 ~/ruta/a/mi/entrega
```

Con la lista del curso también se puede importar una tarea sin exportarla aparte
(`import preflight_46981_assignments.json --assignment 953531`), salvo que tenga archivos
adjuntos: la lista no trae sus tamaños.

`check` revisa con reglas fijas lo que no necesita juicio y lo guarda en `checks.json`:
tiempo restante, estado de la entrega en Canvas, fechas del texto que ya pasaron (como
entregas intermedias que no aparecen como tarea propia), suma de la rúbrica, archivos
adjuntos sin leer, contenido de la carpeta y, si es un repositorio, cambios sin commit,
commits sin push, commits que no están en la rama principal y commits después de la fecha
de entrega. No usa notas ni comentarios del profesor. Con `--as-of due` revisa como si
fuera un minuto antes de la fecha de entrega, para probar con tareas pasadas.

`import` escribe en `~/.cache/preflight/<tarea>/` el texto numerado de las instrucciones
(`spec.md`) y los datos de la tarea (`meta.json`). Con el archivo de la lista del curso,
muestra las tareas vencidas o abiertas sin entrega.

`extract` convierte a texto los docx, pptx (con notas del orador) y pdf de la entrega y
los guarda en `~/.cache/preflight/extract/<carpeta>/`. Nunca escribe dentro de la carpeta
revisada. Los archivos de trabajo quedan fuera del repositorio para que auditar este mismo
repositorio no los exponga ni los modifique.

```bash
python -m preflight audit 959073 ~/ruta/a/mi/entrega
```

`audit` corre `check` y después el agente auditor (Claude Code sin interfaz, `claude -p`).
El agente trabaja sobre una carpeta preparada en `~/.cache/preflight/<tarea>/agent/` que
solo tiene: las instrucciones numeradas, los hechos de `check`, un inventario, una copia de
la entrega sin archivos ocultos, secretos, binarios, archivos grandes ni archivos ignorados
por git, y el texto extraído de los docx, pptx y pdf. Las notas y los comentarios del
profesor nunca llegan al agente.

Límites del agente, comprobados con una prueba de archivos trampa:

- Solo existen las herramientas Read, Grep y Glob: no puede escribir ni ejecutar nada.
- Un intento de leer fuera de su carpeta queda bloqueado y registrado.
- Sin servidores MCP, sin sesión guardada y sin la configuración ni el CLAUDE.md del
  usuario (`--setting-sources project`), para que el resultado dependa solo del prompt.
- La respuesta debe cumplir el esquema `preflight/schema.json`: cada criterio lleva al
  menos una cita con su línea (L001...).

El prompt está versionado en `preflight/prompts/`. `audit.json` guarda el modelo que corrió,
la versión del prompt y una huella de la carpeta antes y después, que debe ser igual.

Al terminar, `audit` valida la respuesta del agente con reglas fijas: cada cita debe estar
textual en su línea, cada archivo de evidencia debe existir en la carpeta real, los puntos
en riesgo deben cuadrar con el estado y con la rúbrica, y los criterios deben cubrir toda
la rúbrica. Los problemas no se corrigen: se marcan en el reporte.

El reporte queda en `~/.cache/preflight/<tarea>/reporte.md`, en español: puntos en riesgo,
tabla de criterios, cada criterio con sus citas y su evidencia, fechas del texto, hechos
revisados por script, lo que no se pudo revisar y el resultado de la validación.
`python -m preflight report <tarea>` lo vuelve a generar desde una auditoría guardada.

## Pruebas

```bash
python -m pytest
python -m preflight cases casos/casos.yaml
```

- `pytest` corre 129 pruebas sin red: lectura de las instrucciones, fechas, revisiones de
  git, extracción de docx, pptx y pdf (incluida una prueba de que un docx malicioso no
  puede leer archivos del sistema), la carpeta aislada del agente, el validador y el reporte.
- `cases` corre la auditoría completa sobre 7 casos reales, dos veces cada uno, y compara
  el resultado con las expectativas de `casos/casos.yaml`. Las expectativas se escribieron
  y se subieron al repositorio antes de correr (commit 5a2e087); los resultados llegaron
  después (commit f13e914).
- Los límites del agente se comprobaron con archivos trampa: un intento de leer un archivo
  fuera de su carpeta quedó bloqueado y registrado.

## Resultados

Prompt v1, modelo claude-opus-5, 7 casos, 2 corridas por caso. Se cumplieron 38 de 40
expectativas. Detalle y los 14 reportes: [casos/resultados.md](casos/resultados.md).

| Caso | Qué se esperaba | Resultado |
|---|---|---|
| Laboratorio 6, nunca entregado | Todo en falta, carpeta inexistente | Sí, en las dos corridas |
| Evaluaciones de Proyecto 2, nunca entregado | Todo en falta, aviso de plantilla adjunta sin leer | Sí, en las dos |
| Hoja de notas 4, 6 y 7, nunca entregada | En falta sin inventar criterios (la instrucción es una línea) | Sí: un solo criterio |
| Proyecto 2, sin faltantes según el profesor | No inventar faltantes | Sí: 0 de 100 puntos en riesgo; además marcó un commit posterior a la fecha |
| Hoja de trabajo 2 | Falta el link al Colab y no se explicó el método del codo | Colab sí; método del codo no, en ninguna corrida |
| Proyecto 3, en curso | Exploración y reflexión faltantes, fecha del 11 de noviembre, trabajo fuera de main | Sí, en las dos |
| Proyecto 2 sin README, copia modificada | Detectar el README faltante | Sí, en las dos |

Dónde falla y por qué:

- **Criterios que no están escritos.** En la Hoja de trabajo 2 el profesor restó por no
  explicar el método del codo, pero la instrucción solo pide "qué se puede ajustar y qué
  efecto tiene". La presentación nombra el codo y cubre el efecto de cada hiperparámetro,
  así que el agente lo dio por cumplido. El agente revisa contra el texto; lo que se espera
  sin escribirse no lo ve.
- **Señales que ignora.** La presentación entregada todavía tenía una nota del orador con
  "TODO 4.4" sobre la figura del codo. El agente no la tomó como señal de algo pendiente.
- **Errores de formato, atrapados por el validador** en 2 de 14 corridas: dos citas armadas
  con pedazos de una línea en vez de copiadas textuales, y un "archivo de evidencia" que no
  era un camino ("(carpeta de la entrega)").
- **Variación entre corridas.** Con la misma entrada, Proyecto 3 dio 80 y 78 puntos en
  riesgo, y en la Hoja de trabajo 2 un criterio salió parcial en una corrida y cumple en la
  otra.

Cada auditoría tardó entre 22 y 222 segundos, más un clic en Canvas para exportar la tarea.
A mano, revisar una tarea me toma de 30 a 45 minutos; con el pre-flight, unos 10. La
configuración se recupera después de 6 a 9 tareas (cálculo en el
[informe](informe/informe.md)).

## Capturas del proceso

En `capturas/`:

- `01`: captura de pantalla de Canvas con el botón "Nuevo token de acceso" deshabilitado
  para estudiantes, recortada para quitar las pestañas del navegador y la foto de perfil.
- `02` a `08`: imágenes de la salida real de cada comando, generadas a partir del texto que
  imprimió; no son capturas de pantalla. En `02` se quitó la columna de notas.
    - `02` lista del curso con las tareas vencidas sin entrega
    - `03` importar Proyecto 3
    - `04` revisiones fijas de Proyecto 3
    - `05` una auditoría completa en vivo
    - `06` el reporte de Proyecto 3
    - `07` la tabla de los casos reales
    - `08` la prueba de aislamiento del agente (lectura fuera de su carpeta bloqueada)
- `09`: diagrama del flujo de seis pasos.

## Limitaciones

- Revisa contra las instrucciones escritas. Lo que el profesor espera sin escribirlo no se
  detecta, y lo oral (presentación en vivo) queda como no verificable.
- El agente no es determinista: dos corridas pueden diferir en el estado de un criterio o
  en los puntos estimados de un parcial.
- Al revisar tareas pasadas con `--as-of due` solo se retroceden el historial de git y el
  estado de la entrega en Canvas; la carpeta se revisa como está hoy.
- En Word, los títulos solo se reconocen si usan estilos de título.
- No revisa archivos ocultos, secretos, binarios, archivos de más de 2 MB ni archivos que
  git ignora; solo los lista en el inventario.
- En UVG cada tarea se exporta con un clic y los archivos adjuntos se descargan a mano.
- Lo que sale de la máquina: la copia de la entrega, el texto extraído y las instrucciones
  se envían a Anthropic al correr la auditoría. Las notas, los comentarios del profesor y
  los archivos ocultos no se envían.
- Usa la cuota de la suscripción. En el plan Pro, el alias `opus` corrió como
  claude-opus-5; el reporte guarda el modelo real.

Mejoras posibles para un prompt v2: pedir "." para referirse a toda la carpeta, exigir que
cada cita sea un solo fragmento continuo de una línea, y agregar una revisión fija de
marcas como TODO o "pendiente" en la entrega. Esta última surgió del caso de la Hoja de
trabajo 2, así que ese caso ya no serviría como prueba independiente de esa mejora.
