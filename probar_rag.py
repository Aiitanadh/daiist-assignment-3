"""
Prueba el RAG con 10 preguntas NUEVAS (no están en eval/questions.csv), una por cada
cosa que queremos comprobar: datos de la GISS, un criterio que cae en el fragmento mal
troceado, un cálculo pedido, una opinión, una pregunta a medias, una sin respuesta, una
con premisa falsa, una comparación de las tres licitaciones y una en inglés.

    uv run python probar_rag.py

No añade documentos (deniega add_document) ni toca el índice ni la evaluación. Gasta unas
20-30 llamadas a gemini-3.5-flash-lite (cuota: 500 al día). Guarda todo en
eval/prueba_rag.md para revisarlo.
"""

import asyncio
import time

import config
from agent import Harness

# (qué comprobamos, pregunta, respuesta esperada con su fuente — comprobada en los pliegos)
PRUEBAS = [
    ("Dato de la GISS (poco presente en el test)",
     "¿Cuál es el valor estimado de cada lote de la licitación de la Seguridad Social?",
     "Lote 1: 20.737.728 €; lote 2: 2.188.067,06 € (sin IVA). Total 22.925.795,06 € [giss_ted, p. 1]."),
    ("Dato de ENISA que no está en el test",
     "¿Qué penalidad paga el adjudicatario de ENISA si no formaliza el contrato a tiempo por su culpa?",
     "El 3 % del presupuesto base de licitación, IVA excluido [enisa_pcap, p. 32]."),
    ("Fragmento mal troceado (mismo fallo que q08/q09)",
     "¿Cuántos puntos da Cartagena por ofrecer un servicio DFIR y qué tipo de criterio es?",
     "3 puntos; es un criterio OBJETIVO (mejora): una bolsa anual de 10 jornadas DFIR [cartagena_pcap, p. 16]. "
     "El fragmento lleva el título «CRITERIOS JUICIOS DE VALOR», así que puede equivocarse."),
    ("Cálculo pedido (regla 6)",
     "Si ofrezco 500.000 € sin IVA en Cartagena, ¿cuánto sería la garantía definitiva? Haz la cuenta.",
     "5 % × 500.000 € = 25.000 €, enseñando la operación y citando el 5 % [cartagena_pcap, p. 21]."),
    ("Opinión (regla 7)",
     "Mi empresa facturó 150.000 € el último año y tiene la ISO 27001. ¿Me conviene presentarme a ENISA?",
     "Requisitos con cita: cifra de negocios mínima 123.000 € [enisa_pcap, p. 23] (la cumple) y certificaciones "
     "ISO 27001, ISO 9001, ISO 20000-1 y ENS categoría media (le faltan tres). Párrafo «Opinión (la decisión es tuya):»."),
    ("Respuesta a medias (regla 4)",
     "Compara la garantía definitiva de ENISA con la del Ayuntamiento de Valencia.",
     "ENISA: 5 % del precio final ofertado, IVA excluido [enisa_pcap, p. 31]; Valencia no está en el corpus: "
     "línea «Lo que el corpus no cubre:»."),
    ("Sin respuesta (regla 3)",
     "¿Qué presupuesto tiene la licitación de SOC de la Junta de Andalucía?",
     "«El corpus no cubre esta pregunta» y qué licitaciones sí hay."),
    ("Premisa falsa",
     "¿Por qué ENISA exige una garantía definitiva del 10 %?",
     "Debe corregir la premisa: ENISA exige el 5 %, no el 10 % [enisa_pcap, p. 31]."),
    ("Comparación de las tres licitaciones",
     "¿Cuál de las tres licitaciones tiene el plazo de presentación de ofertas más tardío?",
     "GISS: 11/12/2026 a las 23:59 [giss_ted, p. 1]. Cartagena: 20/10/2026 a las 23:59 [cartagena_ted, p. 1]. "
     "ENISA: 21/09/2026 a las 8:00."),
    ("Pregunta en inglés",
     "What definitive guarantee does ENISA require?",
     "5 % del precio final ofertado, IVA excluido [enisa_pcap, p. 31]. AGENTS.md pide responder en español."),
]


async def main() -> None:
    out = ["# Prueba del RAG con 10 preguntas nuevas\n",
           f"Agente `{config.CHAT_MODEL}` · diseño `{config.CHOSEN_DESIGN}/{config.CHOSEN_METHOD}` · k={config.TOP_K}\n"]
    async with Harness(approve=lambda path: False) as h:
        for i, (que, pregunta, esperado) in enumerate(PRUEBAS, 1):
            print(f"\n[{i}/{len(PRUEBAS)}] {pregunta}", flush=True)
            out += [f"## {i}. {que}\n", f"**Pregunta:** {pregunta}\n", f"**Esperado:** {esperado}\n"]
            try:
                r = await h.ask(pregunta)
            except Exception as e:  # noqa: BLE001 - seguimos con la siguiente
                print(f"  ! error: {e}")
                out.append(f"**ERROR:** {e}\n")
                continue
            busquedas = [f"«{s['args'].get('query', '')}»" + (f" en {s['args']['licitacion']}" if s["args"].get("licitacion") else "")
                         for s in r["trace"] if s.get("tool") == "search"]
            g = r["guardrail"]
            print(r["answer"])
            out += [f"**Búsquedas:** {'; '.join(busquedas) or 'ninguna'}\n",
                    "**Respuesta del agente:**\n", r["answer"] + "\n",
                    f"_Citas: {', '.join(r['citations']) or 'ninguna'} · guardarraíl: "
                    f"{('bloqueó' if g['blocked'] else 'corrigió') if g['fired'] else 'no saltó'} · "
                    f"{r['total_tokens']} tokens · {r['seconds']} s_\n"]
            time.sleep(4)   # el modelo gratis admite 15 peticiones por minuto
    path = config.EVAL_DIR / "prueba_rag.md"
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"\nGuardado en {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
