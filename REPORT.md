# Assignment 3 Report

- **Name**: Aitana Damotte Huedo
- **Student ID**: 18654
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case
The user is the bid manager of a Spanish SME that sells managed cybersecurity services (SOC/MDR) and decides which public tenders on PLACSP and TED to bid for. They use the answers twice: first for a go/no-go decision (solvency thresholds, required certifications such as ISO/IEC 27001 or ENS, business classification) before investing days of work in a proposal; then to prepare the bid (submission deadline, guarantees, award criteria and their weights, service levels and penalties). A wrong answer is expensive: missing the deadline, not lodging the 5 % guarantee or misreading a solvency threshold gets the bid excluded, and a misread service level or penalty becomes a binding commitment on a €246k–€585k contract. “I don’t know” is cheap: every answer cites [document, page], so the user reads that page of the tender documents, which are the legally binding text anyway. The assistant should therefore refuse whenever the passage is not retrieved.

## Corpus

*Table: document, URL, date, licence, words.*

## Ingestion

*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

## Test set

I wrote 37 questions from the indexed documents (index/chunks_struct.csv and the original PDFs), drafted with Claude’s help and checked page by page against the PDFs. They cover what a bid manager asks before bidding: eligibility (solvency, certifications, classification), money (budget, estimated value, guarantees, penalties), timing (deadline, duration, extensions), scoring (criteria and weights) and service levels. Counts: 25 single, 6 multi, 6 unanswerable. Multi questions compare two tenders, or two documents of the same tender; one of them (q28) has the PCAP and the TED notice disagreeing on the contract duration. Unanswerable questions stay on topic: tenders that are not in the corpus (EMVS Madrid, Murcia), facts the tender documents do not contain (winner, number of bids, signature date) and thresholds set by other regulations.

## Retrieval
*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*

I compared two chunking designs, each with its own full set of embeddings (gemini-embedding-2, 768 dimensions):

- **fixed300**: 300-word windows with a 30-word overlap that ignore the document structure (320 chunks).
- **struct**: one chunk per clause or section of the tender document, keeping the heading with its text; short sections are merged and long ones split, 60–350 words (405 chunks).

On each design I ran three search methods: dense (cosine similarity of embeddings), BM25 keyword search, and a hybrid that fuses both rankings with Reciprocal Rank Fusion. Each was run with and without a filter that restricts the search to the tender named in the question. Results on the 31 answerable questions (a hit is a chunk from the expected document that overlaps the expected page; filter on):

| Design | Method | hit@1 | hit@3 | hit@5 | multi_all@5 | Words added to the prompt |
|---|---|---|---|---|---|---|
| fixed300 | dense | 0.58 | 0.84 | 0.90 | 0.17 | 1,413 |
| fixed300 | hybrid | 0.61 | 0.84 | 0.94 | 0.33 | 1,450 |
| struct | bm25 | 0.58 | 0.81 | 0.87 | 0.50 | 944 |
| struct | hybrid | 0.65 | 0.87 | 0.94 | 0.50 | 907 |
| **struct** | **dense** | **0.71** | **0.94** | **1.00** | **0.50** | **869** |

The full table, with all 12 combinations, is in `eval/retrieval.md`.

**I chose struct + dense, with the tender filter on and 5 chunks per search:**

1. **It has the highest hit rate at every k.** With 5 chunks, the expected passage is retrieved for all 31 questions, and for 22 of them it comes first. Chunking matters more than the search method: fixed windows cut clauses in half, so a chunk can hold the heading "garantía definitiva" while the percentage falls into the next chunk.
2. **It is the cheapest.** It adds 869 words to the prompt per search against 1,413 for fixed300 (38 % fewer), because clauses are shorter than 300-word windows.
3. **Hybrid did not help.** BM25 is weak on this corpus because legal boilerplate repeats the same words (garantía, plazo, contrato) across many clauses. Fusing both rankings with equal weight pulls those clauses up (hit@1 0.65 against 0.71 for dense alone).
4. **The tender filter changes nothing for dense** (0.71 with and without it), but I keep it on: it costs nothing and it guards against the most expensive error in my use case, answering with a figure from a different tender.

**Limitation:** a single search retrieves both passages for only 3 of the 6 multi questions (multi_all@5 = 0.50). That is why AGENTS.md tells the agent to run one search per tender when comparing tenders; the end-to-end evaluation shows whether that is enough.

## Tools and subagent
*Your tools' descriptions, one search result, the subagent's instructions, one transcript from your editor.*

`server.py` exposes two MCP tools. Their descriptions are what the model reads, so they say what the corpus contains, when to call the tool, what each argument means and how to cite.

- **`search(query, licitacion="")`**: searches PCAP and PPT documents and TED notices of three real Spanish cybersecurity (SOC/MDR) tenders, and lists the tenders available (cartagena, enisa, giss). It tells the model to always search before answering, to run several searches when comparing tenders, and to use the optional `licitacion` argument to search only one tender. If the argument is omitted and the query names a tender, the filter is applied automatically. It returns the top 5 chunks, each with the exact citation to copy.
- **`add_document(path)`**: indexes a new file, to be used only when the user explicitly asks (see *Adding a document*).

One search result (trimmed; full results return 5 chunks):

```text
5 fragmentos para «garantia definitiva» (filtrados por la licitación «cartagena»)
---
[1] Cita: [cartagena_pcap, p. 21]
Documento: Pliego de Cláusulas Administrativas Particulares (PCAP) — Servicio de SOC/MDR y herramientas de ciberseguridad (Ayuntamiento de Cartagena, expte. SE2026/44)
Apartado: B) DOCUMENTACIÓN JUSTIFICATIVA DE HALLARSE AL CORRIENTE EN EL CUMPLIMIENTO DE SUS | Páginas: 21-22
Texto: … una garantía definitiva del 5% del precio final ofertado, excluido el Impuesto sobre el Valor añadido, de conformidad con lo establecido en el artículo 107 de la LCSP. …
---
[2] …
```

**Subagent** (`.claude/agents/corpus-researcher.md`): it can only use `mcp__corpus__search`. Its instructions are to search before answering, to run one search per tender when comparing (with the `licitacion` argument), to reformulate with the words a tender document would use, with at most 4 searches, to cite every claim as `[doc_id, p. N]`, and to start with «El corpus no cubre esta pregunta» when the chunks do not answer.

**Transcript from Claude Code** (full export in `eval/subagent_transcript.txt`). Claude Code ran in auto permission mode, so the read-only `search` calls were approved without a prompt.

```text
(paste here the content of eval/subagent_transcript.txt)
```

The subagent ran one search per tender and cited every figure. For ENISA it gave the exact threshold (€123,000, [enisa_pcap, p. 23]). For Cartagena it reported that the PCAP only gives the rule ("precio de licitación anual") and declined to compute the amount itself. It also warned that it had hit its 4-search limit. That warning was justified: the annual amount is in the PPT (p. 37: €195,000 per year excluding VAT, €235,950 including VAT), which it did not search. It is a useful example of an honest but incomplete answer, and of why the user still has to read the cited pages.

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails
*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

**System prompt.** `agent.py` (LangChain `create_agent`, model gemini-3.5-flash-lite) loads `AGENTS.md` as the system prompt, unchanged. It has the three required rules and four of mine, each with its reason written in the file:

1. Answer only from what `search` returns, and always search first.
2. Cite every claim as `[doc_id, p. N]`, copied from the search results.
3. If the corpus does not cover the question, start with «El corpus no cubre esta pregunta».
4. *(mine)* If the corpus covers only part of the question, answer that part and end with «Lo que el corpus no cubre:». The refusal phrase is kept for full refusals.
5. *(mine)* If two documents contradict each other, give both values with their citations and say they differ, without choosing one.
6. *(mine)* Copy figures exactly as written. Calculate only if the user asks, showing the operation and where each input comes from.
7. *(mine)* An opinion is allowed in a paragraph starting «Opinión (la decisión es tuya):», based only on the cited facts; the decision is the user's.

The harness also caps each question at 6 tool calls and 10 model calls (LangChain middleware), so a confused agent cannot loop and use up the quota.

**Approval step.** The MCP tools are wrapped as LangChain tools. Before `add_document` runs, the wrapper shows the path and asks `[s/N]` in the terminal. Any answer except «s» denies it: the tool is not called, and the agent receives «DENEGADO: el usuario no ha aprobado añadir este documento. No lo vuelvas a intentar; explica que hace falta su aprobación.» When there is no terminal (for example inside `main.py evaluate`), it denies automatically. Example run:

```text
$ uv run python main.py ask "Añade al índice el documento nuevos/emvs_madrid_pcap.pdf"
[APROBACIÓN] El agente quiere AÑADIR al índice el fichero:
    nuevos/emvs_madrid_pcap.pdf
Esto gasta cuota de embeddings y cambia el índice. ¿Lo apruebas? [s/N] N
El corpus no cubre esta pregunta. Tras buscar en el corpus los expedientes disponibles (Cartagena, ENISA y GISS), no se encuentra el documento `nuevos/emvs_madrid_pcap.pdf` ni información relativa a la EMVS de Madrid, ya que el sistema requiere la aprobación expresa del usuario para añadir nuevos documentos al índice (véase, por ejemplo, [enisa_pcap, p. 1]).

[guardarraíl de citas] corregida: la respuesta no tiene ninguna cita [doc_id, p. N]

--- Primera respuesta del agente (la que paró el guardarraíl) ---
El corpus no cubre esta acción porque el usuario no ha aprobado añadir el documento. Para poder añadir `nuevos/emvs_madrid_pcap.pdf` al índice, se requiere su aprobación expresa.
--- Fin de la primera respuesta ---

[2 llamadas a herramientas · 8862 tokens · 23.93 s]
```

The document was not added and the index did not change.

**Extra guardrail: citation check.** After the agent answers, the harness checks two things in code. Every answer that is not a refusal must have at least one citation. Every cited `[doc_id, p. N]` must fall inside a chunk that `search` returned for that question (same document, page within the chunk's page range). If either check fails, the harness tells the agent what is wrong and asks once for a rewrite with valid citations, or for a refusal. If the rewrite still fails, the harness replaces it with «El corpus no cubre esta pregunta con fuentes verificables» plus the reason. Both answers are saved in the trace. I chose this guardrail because rule 2 is what makes an answer usable in my use case, and a model can write a citation-shaped string pointing to a page it never retrieved.

**Where it fired.**
- *The approval run above.* The first answer explained the denial correctly. It began «El corpus no cubre esta acción» instead of the exact refusal phrase, so the code treated it as an answer without citations. The rewrite searched, started with the refusal phrase and added `[enisa_pcap, p. 1]`. That page says nothing about approvals, but it had been retrieved, so the guardrail let it through. This shows the guardrail's limit: it checks that a citation points to retrieved text, not that the text supports the sentence. Only the judge's *supported* grade checks that, and only during evaluation. In this case the guardrail made a correct answer worse.
- *q26, first evaluation run.* It blocked a correct answer comparing the Cartagena and ENISA guarantees. The blocked text was not saved at the time. The most likely cause is that the agent grouped two citations in one bracket, as it did in the re-run (`[cartagena_pcap, p. 21, enisa_pcap, p. 31]`), and my first parser did not recognise that format. I changed the parser to read several citations in one bracket, made the harness save the original answer, and re-ran q26. It passed.
- *A direct attempt that did not fire.* I asked the agent to answer from memory and cite `[cartagena_pcap, p. 99]`. It refused by itself, quoting rules 1 and 2, without calling any tool. Refusals are not checked, so the guardrail had nothing to do.

**What I would fix first:** skip the check when the agent's turn ended with a denied `add_document`, since there is nothing in the corpus to cite. Then add a runtime check that the cited chunk shares the key figures or terms of the sentence it supports.

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
