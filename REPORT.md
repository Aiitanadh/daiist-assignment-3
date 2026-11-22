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

## Adding a document

*What happens when a document is already indexed. The unanswerable question, the document you added, the answer before and after.*

## Harness and guardrails

*Your AGENTS.md rules, the approval step, and your extra guardrail with one case where it fired.*

## Evaluation

*Code checks, the judge's rubric, your agreement with the judge, and results: correct, unsupported, correct refusals, wrong refusals.*

## Failures

*Failed questions by cause, with counts, and what to fix first.*

## Decision

*Would you let users rely on it, for what, with which safeguard? Cost and latency per question.*

## AI use

*What you used and how, or "none".*
