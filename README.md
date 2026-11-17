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
```

`import` escribe en `~/.cache/preflight/<tarea>/` el texto numerado de las instrucciones
(`spec.md`) y los datos de la tarea (`meta.json`). Con el archivo de la lista del curso,
muestra las tareas vencidas o abiertas sin entrega.

`extract` convierte a texto los docx, pptx (con notas del orador) y pdf de la entrega y
los guarda en `~/.cache/preflight/extract/<carpeta>/`. Nunca escribe dentro de la carpeta
revisada. Los archivos de trabajo quedan fuera del repositorio para que auditar este mismo
repositorio no los exponga ni los modifique.

Pendiente: auditoría y reporte.

## Pruebas

Pendiente.

## Resultados

Pendiente.

## Limitaciones

Pendiente.
