# Assignment 3 Report

- **Name**: Aitana Damotte Huedo
- **Student ID**: 18654
- **Group**: [BBADBA 5A | BBADBA 5B | PPLEDBA 5A]

## Use case
The user is the bid manager of a Spanish SME that sells managed cybersecurity services (SOC/MDR). They decide which public tenders on PLACSP and TED to bid for.

They use the answers twice:
- **Go/no-go:** solvency thresholds, required certifications (ISO/IEC 27001, ENS) and business classification. This comes before spending days on a proposal.
- **Preparing the bid:** deadline, guarantees, award criteria and their weights, service levels and penalties.

A wrong answer is expensive. Missing the deadline, not lodging the 5 % guarantee or misreading a solvency threshold gets the bid excluded. A misread service level or penalty becomes a binding commitment on a €246k–€585k contract.
"I don't know" is cheap. Every answer cites [document, page], so the user opens that page of the tender documents, which are the legally binding text anyway. So the assistant should refuse whenever it does not retrieve the passage.

## Corpus

Nine public documents from three real Spanish cybersecurity tenders (SOC/MDR), all from 2026. For each tender:
- **PCAP** (administrative clauses: solvency, guarantees, award criteria, penalties), from PLACSP.
- **PPT** (technical specifications: service levels, staff, tools), from PLACSP.
- **TED notice**, downloaded as JSON from the TED Search API. It is the official summary (value, duration, deadline). It is also where one contradiction with the PCAP shows up (q28).

| Document | Tender | Type | URL | Date | Licence | Words |
|---|---|---|---|---|---|---|
| `cartagena_pcap` | Ayuntamiento de Cartagena (SE2026/44) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=3RvTg%2BqJGplpqK%2BNayOJdmu3brxMJj85yHdub21Tk8IRUVsFr1wAigfAsquMfDh9lBaZNGbs4SxQbAtLZnFB2c83c%2Bb8gBCF4jisIX8LfHOHAj0WEJrB5sP7amrh2jBD) | 2026-09-09 | Ley 37/2007 (PLACSP) | 13,106 |
| `cartagena_ppt` | Ayuntamiento de Cartagena (SE2026/44) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4LNw9X8Oth%2BSn9NbTkZ4FS6sIE23mzU7WXFZ56WAvbF1G%2BlP4OQLs1MxqFW16iI7xeK%2BjNty6lM6gGPDyy6wJX7drdkgQxKh8ayOdg%2BOlwGHAj0WEJrB5sP7amrh2jBD) | 2026-07-28 | Ley 37/2007 (PLACSP) | 6,657 |
| `cartagena_ted` | Ayuntamiento de Cartagena (SE2026/44) | TED notice | [TED 649174-2026](https://ted.europa.eu/es/notice/-/detail/649174-2026) | 2026-09-21 | Decision 2011/833/EU (TED) | 315 |
| `enisa_pcap` | ENISA (56/2026) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=9ETPlYBON0QDBMg/Qhi65LuaWFeo/yh0sxRjsJQIi9I23eR5bxfQbFmYrhtwrA6xiOf5PEsipiU7Qc1eWPlT2bG9QfRLddT5kTx4EkNbrTqCx2e6p7hqtlp2aFupgHMr) | 2026-07-27 | Ley 37/2007 (PLACSP) | 13,660 |
| `enisa_ppt` | ENISA (56/2026) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=47dHKqAqtfJ1wQ0TG75owUHSgz94ch%2BQdgK4Ni1EKa/Fn5t09e5eP/7%2BHUMzKwCqXx5FiJeMlcwnb6%2BXDhu8vvAFA9Kll/3leo9p7zi5FHht/o8fNevwsujgRzaBbugn) | 2026-07-27 | Ley 37/2007 (PLACSP) | 6,920 |
| `enisa_ted` | ENISA (56/2026) | TED notice | [TED 530695-2026](https://ted.europa.eu/es/notice/-/detail/530695-2026) | 2026-07-31 | Decision 2011/833/EU (TED) | 336 |
| `giss_pcap` | GISS (2026/7028) | PCAP | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=utdJKrcIIi8TnaqXvWAbH6rIIccFdesQyEoNK3OwOZWh6ayu5tQXrTM7Ellxz2qtMvT/tGixw9fore9Gnhnf402jEM6FdBnnUZRaT5ybWWjfdyQgZAdTm3EfcUAC7CJ6) | 2026-11-19 | Ley 37/2007 (PLACSP) | 22,717 |
| `giss_ppt` | GISS (2026/7028) | PPT | [PLACSP](https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?cifrado=QUC1GjXXSiLkydRHJBmbpw%3D%3D&DocumentIdParam=4Olo7kYgFvEES5uZIJmlCdK2/Qrpoei5GZTfHej2T75bfV%2BsuxKUo7kvgBuuBPt6bwuwEw2f9qdtYb4ExfoogqlYTMRd9VRC8R9/oCOZn6Q//q7NB2iMZvNyf0xrJmjt) | 2026-11-19 | Ley 37/2007 (PLACSP) | 20,873 |
| `giss_ted` | GISS (2026/7028) | TED notice | [TED 809807-2026](https://ted.europa.eu/es/notice/-/detail/809807-2026) | 2026-11-20 | Decision 2011/833/EU (TED) | 477 |
| **Total** | 3 tenders | 9 documents | | | | **85,061** |

- **Date:** for PDFs, the date of the final version in the file metadata. For TED notices, the publication date.
- **Words:** counted after cleaning and redaction (`index/corpus_stats.csv`). 293 pages in total.
- **Licence:** PLACSP documents are public sector information, and Ley 37/2007 allows their reuse if the source is cited. TED notices can be reused under the European Commission's reuse policy (Decision 2011/833/EU).
- **Personal data:** the PDFs are electronically signed, so they contain the signers' names and some emails. `index.py` replaces them with tags before chunking: 70 signature blocks, 4 emails and 1 name. From TED I request only the fields I need, with no contact-person fields.
- The original PDFs are not committed (`corpus/` is in `.gitignore`). `main.py index` downloads them again from the URLs above.


## Ingestion
*How you extract, clean and chunk; one extraction problem you fixed; chunk metadata; number of chunks.*

`index.py` runs one pipeline for every document. `server.py` imports it for `add_document`.

1. **Extract.** PDFs are read with `pypdf`, page by page, so each chunk keeps its page number. TED notices arrive as JSON from the TED API; `index.py` turns them into one page of text with Spanish labels («Valor estimado total (sin IVA): 585000 Moneda: EUR»).
2. **Redact personal data**, once before cleaning and once after.
3. **Clean.**
   - Remove lines that repeat on 40 % or more of a document's pages (headers, footers, signature blocks).
   - Remove table-of-contents lines and page numbers.
   - Join words split by a hyphen at the end of a line (81 cases in `giss_ppt`).
   - Fix small capitals that pypdf splits: «D ESCRIPCIÓN» → «DESCRIPCIÓN» (31 cases in `giss_ppt`).
4. **Chunk.** There are two designs (see *Retrieval*). The structural one finds clause headings («CLÁUSULA 12», «TERCERA.-», «4.1. PRESUPUESTO», lines in capitals) and makes one chunk per clause. Clauses under 60 words are merged with the next one. Clauses over 350 words are split into equal parts, and each part after the first starts with `[heading] (continuación)`.
5. **Embed and store.** gemini-embedding-2 (768 dimensions), in batches of 20, into ChromaDB (`index/chroma`, cosine distance), one collection per design. The chunk id is a hash of its text, so running `main.py index` again only embeds chunks that have no saved vector.

**Extraction problem I fixed: the Cartagena signature footer.**
- Every page of the two Cartagena PDFs ends with an e-signature footer. pypdf extracts it as eight lines: «La comprobación de la autenticidad de este documento…», «Código Seguro de Verificación: …», «AYUNTAMIENTO DE CARTAGENA», «FIRMADO POR», the signer's name, the job title, the date and «Pág. 10 de 31».
- It caused three problems. It cut in two every clause that crosses a page. It repeated the same noise on all 69 pages of the two documents. And it put a person's name in the index.
- The fix has three parts:
  1. A redaction pattern for this format, because the name is on the line after «FIRMADO POR».
  2. The header/footer filter replaces digits with `#` before counting lines, so «Pág. 10 de 31» and «Pág. 11 de 31» count as the same line.
  3. A second redaction pass after cleaning, for emails that only become whole once hyphenated words are joined.
- Result: no chunk in `index/chunks_struct.csv` contains «Código Seguro», «FIRMADO POR» or a page footer.
- I accepted one side effect. The small-capitals fix also joins a few real one-letter words, for example «anexo X lo» → «anexo Xlo» (about 7 cases). This does not hurt retrieval.

**Another fix: headings.** Numbered paragraphs like «2.5. El desconocimiento del contrato…» looked like headings and produced tiny chunks. Now a numbered line counts as a heading only if the next line does not start in lower case.

**Chunk metadata:** `doc_id`, `doc_type` (pcap, ppt, ted), `title`, `tender_key`, `tender_id`, `buyer`, `aliases`, `url`, `section` (the clause heading), `page_start`, `page_end`, `words`, `design`, `file_sha256` and `origin`. Citations are `[doc_id, p. page_start]`. The tender filter uses `tender_key`.

**Number of chunks:**
- **struct:** 405 (Cartagena 65 PCAP + 42 PPT + 3 TED; ENISA 66 + 38 + 3; GISS 100 + 85 + 3). They have 60–356 words, median 211.
- **fixed300:** 320.

## Test set

There are 37 questions in `eval/questions.csv`, written from the indexed documents. Claude helped me draft them, and I checked each one against the PDF page.

- **25 single:** one passage answers them. Example: «¿Cuál es el valor estimado del contrato de SOC/MDR del Ayuntamiento de Cartagena?» (585.000 € sin IVA).
- **6 multi:** they need two passages, from two tenders or from two documents of the same tender. Example: «¿Exigen Cartagena y ENISA la misma garantía definitiva?». In q28 («¿Coinciden la duración del contrato de Cartagena en el pliego y en el anuncio de TED?») the two documents disagree: the PCAP says «tres años y tres meses» and TED says 455 días.
- **6 unanswerable**, all on topic:
  - tenders that are not in the corpus: «¿Qué garantía definitiva exige la EMVS de Madrid en su licitación de SOC?», and one from the Ayuntamiento de Murcia;
  - facts that tender documents do not contain: the winner, the number of bids, the signature date;
  - a threshold set by another regulation: «¿Cuál es el umbral de regulación armonizada para contratos de servicios en 2027?».

The questions cover what a bid manager checks before bidding: eligibility (solvency, certifications, classification), money (budget, estimated value, guarantees, penalties), timing (deadline, duration, extensions), scoring (criteria and weights) and service levels.

## Retrieval
*Hit rate at 1/3/5 per design, words added to the prompt, the design you chose.*
I compared two chunking designs. Each one has its own full set of embeddings (gemini-embedding-2, 768 dimensions).
- **fixed300:** 300-word windows with a 30-word overlap. Ignores the document structure. 320 chunks.
- **struct:** one chunk per clause, with its heading. 60–350 words. 405 chunks.

On each design I tested three search methods:
- **dense:** cosine similarity of the embeddings;
- **BM25:** keyword search;
- **hybrid:** both rankings fused with Reciprocal Rank Fusion.

I ran each one with and without a filter that only searches the tender named in the question. A hit is a chunk from the expected document that overlaps the expected page. Results on the 31 answerable questions, with the filter on:

| Design | Method | hit@1 | hit@3 | hit@5 | multi_all@5 | Words added to the prompt |
|---|---|---|---|---|---|---|
| fixed300 | dense | 0.58 | 0.84 | 0.90 | 0.17 | 1,413 |
| fixed300 | hybrid | 0.61 | 0.84 | 0.94 | 0.33 | 1,450 |
| struct | bm25 | 0.58 | 0.81 | 0.87 | 0.50 | 944 |
| struct | hybrid | 0.65 | 0.87 | 0.94 | 0.50 | 907 |
| **struct** | **dense** | **0.71** | **0.94** | **1.00** | **0.50** | **869** |

All 12 combinations are in `eval/retrieval.md`.

**I chose struct + dense, with the tender filter on and 5 chunks per search.**
1. **Best hit rate at every k.** With 5 chunks, the right passage is retrieved for all 31 questions, and for 22 of them it comes first. Chunking matters more than the search method: fixed windows cut clauses in half, so the heading «garantía definitiva» can land in one chunk and the percentage in the next.
2. **Cheapest.** It adds 869 words to the prompt per search, against 1,413 for fixed300 (38 % less).
3. **Hybrid did not help.** Legal boilerplate repeats the same words (garantía, plazo, contrato) in many clauses, so BM25 is weak here. Fusing it pulls those clauses up: hit@1 is 0.65, against 0.71 for dense alone.
4. **The filter changes nothing for dense** (0.71 with and without it), but I keep it. It costs nothing, and it protects against the most expensive error in my use case: a figure from the wrong tender.

**Limitation:** one search finds both passages for only 3 of the 6 multi questions (multi_all@5 = 0.50). That is why `AGENTS.md` tells the agent to run one search per tender when comparing.

## Tools and subagent


## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails
**System prompt.** `agent.py` (LangChain `create_agent`, model gemini-3.5-flash-lite) uses `AGENTS.md` as the system prompt, unchanged. Each rule has its reason written in the file.

Required rules:
1. «Responde solo con lo que devuelve `search`.»
2. «Cita cada afirmación con el formato exacto `[doc_id, p. N]`.»
3. «Si el corpus no cubre la pregunta, dilo.» The answer must start with «El corpus no cubre esta pregunta».

My rules:

4. «Si el corpus solo cubre una parte de la pregunta, responde esa parte y avisa de lo que falta.» The answer ends with «Lo que el corpus no cubre:».
5. «Si dos documentos se contradicen, da los dos valores y avisa.»
6. «Copia las cifras tal como salen en el pliego.» It calculates only if the user asks, showing the operation.
7. «Puedes dar una opinión, pero la decisión es del usuario.» The opinion goes in a paragraph that starts with «Opinión (la decisión es tuya):».

**Limits:** at most 6 tool calls and 10 model calls per question (LangChain middleware). A confused agent cannot loop and use up the quota.

**Approval step.**
- The MCP tools are wrapped as LangChain tools.
- Before `add_document` runs, the wrapper shows the path and asks `[s/N]`.
- Any answer except «s» denies it. The tool is not called, and the agent receives: «DENEGADO: el usuario no ha aprobado añadir este documento. No lo vuelvas a intentar; explica que hace falta su aprobación.»
- When there is no terminal (for example inside `main.py evaluate`), it denies automatically.

Example:

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

The document was not added, and the index did not change.

**Extra guardrail: citation check.** After each answer, code checks two things:
- an answer that is not a refusal has at least one citation;
- each cited `[doc_id, p. N]` falls inside a chunk that `search` returned for that question.

If a check fails, the harness tells the agent what is wrong and asks for one rewrite. If the rewrite also fails, the harness replaces it with «El corpus no cubre esta pregunta con fuentes verificables» plus the reason. Both answers are saved in the trace.

Why this guardrail: in my use case, an answer is only useful if the user can open the cited page. A model can write a citation that looks right but points to a page it never retrieved.

**Where it fired:**
- **The approval run above.** The first answer was correct, but it started with «El corpus no cubre esta acción» instead of the exact phrase, so the code saw an answer without citations. In the rewrite, the agent added `[enisa_pcap, p. 1]`, a page that says nothing about approvals. The guardrail let it through because that page had been retrieved. **This is its limit:** it checks that a citation points to retrieved text, not that the text supports the sentence. Only the judge's *supported* grade checks that, and only during evaluation. Here the guardrail made a correct answer worse.
- **q26 in the first evaluation run** («¿Exigen Cartagena y ENISA la misma garantía definitiva?»). It blocked a correct answer. The blocked text was not saved at the time. The most likely cause is two citations in one bracket, as in the re-run (`[cartagena_pcap, p. 21, enisa_pcap, p. 31]`), which my first parser could not read. I fixed the parser, made the harness save the original answer and re-ran q26, which passed. In the final run of all 37 questions, the guardrail fired 0 times.
- **A test where it did not fire.** I asked the agent to answer from memory and cite `[cartagena_pcap, p. 99]`. It refused by itself, quoting rules 1 and 2, without calling any tool. Refusals are not checked, so the guardrail had nothing to do.

**What I would fix first:** skip the check when the turn ended with a denied `add_document`, since there is nothing to cite. Then check that the cited chunk contains the key figure or term of the sentence it supports.


## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
