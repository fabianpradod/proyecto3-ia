# Resultados de los casos reales

Prompt v1, modelo claude-opus-5, 2 corridas por caso. Las expectativas están en casos.yaml y se escribieron antes de correr.

| Caso | Corrida | Expectativas cumplidas | En riesgo | Cumple / Parcial / Falta / No verificable | Validación | Tiempo |
|---|---|---|---|---|---|---|
| lab6 | 1 | 3 / 3 | - | 0 / 0 / 11 / 1 | ok | 102 s |
| lab6 | 2 | 3 / 3 | - | 0 / 0 / 12 / 1 | ok | 91 s |
| evaluaciones | 1 | 3 / 3 | - | 0 / 0 / 4 / 1 | ok | 52 s |
| evaluaciones | 2 | 3 / 3 | - | 0 / 0 / 3 / 0 | ok | 41 s |
| hoja_notas | 1 | 3 / 3 | - | 0 / 0 / 1 / 0 | ok | 22 s |
| hoja_notas | 2 | 3 / 3 | - | 0 / 0 / 1 / 0 | ok | 27 s |
| proyecto2 | 1 | 3 / 3 | 0 / 100 | 8 / 0 / 0 / 2 | 2 problemas | 160 s |
| proyecto2 | 2 | 3 / 3 | 0 / 100 | 8 / 0 / 0 / 2 | ok | 218 s |
| hoja_trabajo2 | 1 | 1 / 2 | - | 7 / 3 / 1 / 2 | 2 problemas | 148 s |
| hoja_trabajo2 | 2 | 1 / 2 | - | 9 / 3 / 1 / 1 | ok | 165 s |
| proyecto3 | 1 | 5 / 5 | 80 / 100 | 0 / 2 / 4 / 0 | ok | 137 s |
| proyecto3 | 2 | 5 / 5 | 78 / 100 | 0 / 3 / 4 / 0 | ok | 147 s |
| proyecto2_sin_readme | 1 | 1 / 1 | 3 / 100 | 7 / 1 / 0 / 2 | ok | 222 s |
| proyecto2_sin_readme | 2 | 1 / 1 | 3 / 100 | 7 / 1 / 0 / 1 | ok | 134 s |

## Laboratorio 6 - Naive Bayes and Decision Trees

Lo que pasó de verdad: Nunca se entregó y no hay carpeta local.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| hecho folder = problem | sí | sí |
| hecho submission = warning | sí | sí |
| ningun criterio en cumple | sí | sí |

Variación entre corridas: puntos en riesgo 0, 0.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/lab6-run1.md), [Corrida 2](resultados/lab6-run2.md)

## Proyecto 2 - Evaluaciones de otros grupos

Lo que pasó de verdad: Nunca se entregó. La plantilla adjunta no se leyó (la copia local es otra).

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| hecho folder = problem | sí | sí |
| hecho sources = warning | sí | sí |
| ningun criterio en cumple | sí | sí |

Variación entre corridas: puntos en riesgo 0, 0.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/evaluaciones-run1.md), [Corrida 2](resultados/evaluaciones-run2.md)

## Hoja de notas Temas 4, 6 y 7

Lo que pasó de verdad: Nunca se entregó. La instrucción completa es una línea, sin criterios.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| hecho folder = problem | sí | sí |
| hecho rubric = info | sí | sí |
| ningun criterio en cumple | sí | sí |

Variación entre corridas: puntos en riesgo 0, 0.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/hoja_notas-run1.md), [Corrida 2](resultados/hoja_notas-run2.md)

## Proyecto 2 - Machine Learning

Lo que pasó de verdad: El profesor no señaló faltantes; comentó commits posteriores a la fecha.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| hecho git_after_due = warning | sí | sí |
| hecho submission = ok | sí | sí |
| ningun criterio en falta | sí | sí |

Variación entre corridas: puntos en riesgo 0, 0.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/proyecto2-run1.md), [Corrida 2](resultados/proyecto2-run2.md)

## Presentación Algoritmo de Machine Learning en Parejas - Hoja de trabajo 2

Lo que pasó de verdad: Se restó por no explicar el método del codo (se mencionó sin explicarlo) y el profesor pidió el link del demo, que no se había entregado.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| detecta L006/L024 (colab/demo/link/enlace) | sí | sí |
| detecta L021/L022 (codo/elbow) | no | no |

Variación entre corridas: puntos en riesgo 0, 0.
Criterios que cambiaron de estado: Cubrir las secciones obligatorias en orden (parcial, cumple).

Reportes: [Corrida 1](resultados/hoja_trabajo2-run1.md), [Corrida 2](resultados/hoja_trabajo2-run2.md)

## Proyecto 3 - Automatiza algo tuyo con IA

Lo que pasó de verdad: En curso. La tabla de exploración, el informe, la reflexión y la presentación todavía no están en el repositorio.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| hecho text_dates = warning | sí | sí |
| hecho git_branch = warning | sí | sí |
| detecta L040/L011/L013/L015 (exploraci/tabla) | sí | sí |
| detecta L043/L025/L026/L027/L028 (reflexi) | sí | sí |
| fecha en L031 | sí | sí |

Variación entre corridas: puntos en riesgo 80, 78.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/proyecto3-run1.md), [Corrida 2](resultados/proyecto3-run2.md)

## Proyecto 2 sin README (copia modificada a propósito)

Lo que pasó de verdad: Copia de Proyecto 2 sin el README, que la instrucción L029 pide de forma explícita.

| Expectativa | Corrida 1 | Corrida 2 |
|---|---|---|
| detecta L029/L041 (readme) | sí | sí |

Variación entre corridas: puntos en riesgo 3, 3.
Ningún criterio cambió de estado entre corridas.

Reportes: [Corrida 1](resultados/proyecto2_sin_readme-run1.md), [Corrida 2](resultados/proyecto2_sin_readme-run2.md)
