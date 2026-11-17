# Pre-flight: revisar una entrega antes de enviarla

Proyecto 3 de Inteligencia Artificial (UVG, 2026): "Automatiza algo tuyo con IA".
Es la tarea 1 de mi lluvia de ideas.

## Qué hace

Lee una tarea de Canvas (instrucciones y rúbrica), revisa la carpeta o el repositorio
de la entrega y reporta qué puntos se perderían si se entregara en ese momento. También
saca las fechas y los entregables que solo aparecen en el texto de la tarea.

Cada observación cita la parte de la instrucción o de la rúbrica en la que se basa. No
hace la tarea ni escribe contenido de la entrega: solo la audita.

## Por qué esta herramienta

Pendiente: justificación a partir de la tabla de exploración (`exploracion/`).

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

Pendiente: reporte.

## Pruebas

Pendiente.

## Resultados

Pendiente.

## Limitaciones

Pendiente.
