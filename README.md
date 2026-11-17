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

1. Descarga de Canvas las instrucciones, la fecha de entrega y el estado de la entrega.
2. Convierte a texto los archivos de la entrega (docx, pptx, pdf), sin tocar la carpeta original.
3. Revisa con reglas fijas lo que no necesita juicio: fechas, archivos y commits.
4. Un agente con permisos de solo lectura compara la entrega con cada criterio.
5. Un script verifica que cada cita exista textual en las instrucciones y que la carpeta
   auditada no haya cambiado.
6. Genera el reporte.

## Requisitos

- Python 3 con requests, beautifulsoup4, lxml, pypdf, pyyaml y pytest.
- Claude Code (de pago, requiere suscripción).
- Un token de acceso personal de Canvas.

## Configuración

1. En Canvas: Cuenta > Configuraciones > Nuevo token de acceso. Ponerle fecha de vencimiento.
2. Copiar `.env.example` a `~/.config/preflight/.env` y llenar `CANVAS_TOKEN`.

El archivo con el token queda fuera de este repositorio y fuera de cualquier carpeta
auditada, para que el agente no pueda leerlo.

## Uso

Pendiente.

## Pruebas

Pendiente.

## Resultados

Pendiente.

## Limitaciones

Pendiente.
