# Rúbrica del juez

<!--
DECISIÓN TUYA: esta rúbrica la escribes tú (el enunciado lo exige). evaluate.py la pega
literalmente al principio del prompt del juez, seguida de la pregunta, la respuesta de
referencia, la evidencia recuperada y la respuesta del agente. El juez devuelve
correct (0/1), supported (0/1) y reason.

Mantén las dos definiciones base (vienen de eval/README.md) y concreta TU CRITERIO en
los huecos. Mientras quede el texto "TU CRITERIO" en este fichero, evaluate.py avisará
de que la rúbrica sigue siendo la plantilla. Borra este comentario al terminar.
-->

## correct (1/0)

Base: 1 si la respuesta dice lo mismo que la respuesta de referencia (o, si la pregunta no
tiene respuesta en el corpus, si lo reconoce). 0 si no.

Mi criterio:
- Respuestas parciales (p. ej. pregunta `multi` con una de las dos partes bien): TU CRITERIO
- Importes, porcentajes, plazos y fechas: TU CRITERIO (¿exactos? ¿se acepta redondeo?)
- Información extra correcta que no está en la referencia: TU CRITERIO
- Mezclar datos de otra licitación: TU CRITERIO

## supported (1/0)

Base: 1 si TODAS las afirmaciones de la respuesta aparecen en la evidencia recuperada; 0 si
alguna no aparece, aunque sea cierta.

Mi criterio:
- Paráfrasis o cálculos sencillos a partir de la evidencia (p. ej. sumar puntos): TU CRITERIO
- Frases genéricas sin dato ("conviene revisar el pliego"): TU CRITERIO
