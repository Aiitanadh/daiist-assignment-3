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
