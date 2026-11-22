# Resumen de la evaluación

Agente: `gemini-3.5-flash-lite` · juez: `gemini-3.6-flash` · diseño: `struct / dense / filtro=True / k=5`

## Resultados (12 de 37 preguntas puntuadas)

- **Correctas:** 12/12 (100 %)  single: 6/6 (100 %) · unanswerable: 6/6 (100 %)
- **Respuestas con afirmaciones no respaldadas:** 0/6 (0 %) de las respuestas que no son rechazo
- **Rechazos correctos:** 6/6 (100 %) de las preguntas sin respuesta
- **Rechazos indebidos (wrong refusals):** 0/6 (0 %) de las preguntas con respuesta
- **Rechazos que faltaron** (contestó una pregunta sin respuesta): 0
- **Citas inválidas:** 0 respuestas · guardarraíl de citas: saltó 0 veces, bloqueó 0

## Coste por pregunta

- Tokens del agente: media 7196, mediana 5677
- Segundos: media 7.5, mediana 3.8, máximo 36.45
- Llamadas a herramientas: media 1.32

## Acuerdo con tus notas (human_labels.csv)

- correct: acuerdo None en 0 respuestas (kappa de Cohen None)
- supported: acuerdo None en 0 respuestas (kappa de Cohen None)

Desacuerdos (humano vs. sistema, correct/supported):

(ninguno)


## Fallos por causa sugerida (revísalos en failures.csv)

(sin datos)


## Retrieval

| design | method | tender_filter | hit@1 | hit@3 | hit@5 | multi_all@5 | words_in_prompt@5 | chunks |
|---|---|---|---|---|---|---|---|---|
| fixed300 | dense | no | 0.581 | 0.839 | 0.903 | 0.167 | 1413 | 320 |
| fixed300 | dense | sí | 0.581 | 0.839 | 0.903 | 0.167 | 1413 | 320 |
| fixed300 | bm25 | no | 0.484 | 0.71 | 0.839 | 0.5 | 1445 | 320 |
| fixed300 | bm25 | sí | 0.548 | 0.839 | 0.935 | 0.5 | 1467 | 320 |
| fixed300 | hybrid | no | 0.613 | 0.839 | 0.935 | 0.333 | 1455 | 320 |
| fixed300 | hybrid | sí | 0.613 | 0.839 | 0.935 | 0.333 | 1450 | 320 |
| struct | dense | no | 0.71 | 0.935 | 1.0 | 0.5 | 876 | 405 |
| struct | dense | sí | 0.71 | 0.935 | 1.0 | 0.5 | 869 | 405 |
| struct | bm25 | no | 0.419 | 0.774 | 0.806 | 0.5 | 976 | 405 |
| struct | bm25 | sí | 0.581 | 0.806 | 0.871 | 0.5 | 944 | 405 |
| struct | hybrid | no | 0.645 | 0.871 | 0.935 | 0.5 | 911 | 405 |
| struct | hybrid | sí | 0.645 | 0.871 | 0.935 | 0.5 | 907 | 405 |
