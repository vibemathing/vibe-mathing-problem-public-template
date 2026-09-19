# 08 — Human Summary Pipeline

## Purpose

`human-summary` turns a project's verified mathematics into a reader-facing progress report while preventing internal orchestration details from leaking into the prose. It can be used before the project is complete.

## Architecture

The main agent calls `summary_write`; it does not author the report itself. The tool:

1. reads the project problem;
2. reads every verified fact in dependency-aware order;
3. strips each fact's YAML frontmatter and internal identifiers;
4. embeds only statement/proof/intuition math plus the fixed report-writer prompt;
5. runs an isolated writer with no filesystem/tools;
6. scans output for internal identifiers and machinery vocabulary;
7. keeps `report.md` only when the writer succeeds and the leak scan is clean.

This keeps large fact bodies and internal metadata out of the main agent's working context and gives the report a separate disclosure boundary.

## Report content

A useful report contains:

- precise problem statement;
- verified partial results with understandable proof sketches;
- the main mathematical obstacle;
- neutral progress timeline/context;
- the next missing lemma or bridge;
- narrative in the operator's chosen language while preserving standard mathematical terminology.

It should describe the mathematics, not the internal fact ids, worker roster, verifier machinery, global-memory channels, or strategy plumbing.

## Scrubbing model

Fact frontmatter is excluded before the writer sees the bundle. The writer receives numbered mathematical results only. The output leak scanner acts as a second line of defense for things such as hash-like ids, fact slugs, role vocabulary, and internal strategy terms.

If a leak is detected, the output is quarantined and the clean report path is not produced. Do not manually rename the quarantined output into delivery; regenerate after diagnosing why internal language appeared.

## Failure recovery

| Failure | Response |
|---|---|
| no verified results yet | state that the report can only describe the problem and lack of verified progress |
| isolated writer errors/times out | inspect returned status/logs; retry after fixing environment, not by pretending a report exists |
| output empty | treat as non-ok |
| leak findings | quarantine, adjust source/prompt boundary, regenerate |
| language wrong | supply explicit narrative language while keeping math terminology standard |
| report overclaims | regenerate from verified facts; do not use global-memory claims as completed results |

## When to use instead of write-paper

Use human-summary for operator updates, progress communication, and a clean explanation of what is established and open. Use write-paper only when an operator-selected verified target is ready for formal manuscript curation.

## Validation

Before delivery confirm:

- `status=ok` from the summary tool;
- non-empty report artifact exists;
- leak findings are empty;
- mathematical claims trace to verified fact bodies;
- no internal identifier/machinery vocabulary appears;
- open obstacles are described as open.
