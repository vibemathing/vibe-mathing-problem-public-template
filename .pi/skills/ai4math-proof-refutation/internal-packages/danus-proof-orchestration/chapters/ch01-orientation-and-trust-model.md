# 01 — Orientation and Trust Model

## Core idea

Danus separates mathematical production from correctness authority. Many agents may explore and propose; a cold-start verifier decides whether a candidate result crosses the truth boundary. The fact graph is the only store whose nodes may be treated as established mathematics.

## Actors and authority

### Operator

Provides the problem and operating preferences, decides whether a verified result is the intended answer, approves destructive or outward actions, and remains the escalation point for high-stakes claims.

### Main agent

Owns the global strategy, approach portfolio, worker assignments, literature map, elaboration, and master guidance. It can search verified facts and shared findings and may revoke a bad fact when the operator decision is satisfied. It intentionally lacks `fact_submit`, so strategy cannot directly manufacture truth.

### Workers

Run autonomous proof-search rounds. They can read shared memory and verified facts, publish typed findings, search literature, and submit candidate facts. Their private local memory stays private. They cannot revoke facts.

### Verifier

Starts fresh for each candidate. It reads the proposed statement/proof, may inspect cited facts and literature, and produces a strict verdict plus repair hints. It has no shared-state write surface. The gateway writes a fact only after a `correct` verdict.

### Exploratory subagents

Extend the main agent's reasoning capacity. Their outputs are hypotheses and strategic evidence. Any result needed by a proof must move through a worker and verifier.

## Two-lane reasoning model

Use two concurrent lanes:

1. **Speculative lane:** main-agent reasoning and exploratory subagents generate architectures, analogies, conjectures, and literature leads quickly.
2. **Evidentiary lane:** workers build self-contained claims and push them through verification into the fact graph.

Never collapse the lanes. Speculation can determine what to prove next; it cannot become a predecessor fact.

## Lifecycle

1. Initialize environment and operator preferences.
2. Create project and workers; ensure verifier service is healthy.
3. Fix the mathematical goal in `PROBLEM.md`.
4. Main agent performs an initial global review and dispatches differentiated work.
5. Workers iterate through proof-search skills and publish findings.
6. Verifiable results enter `fact_submit`; rejected work is repaired; accepted work becomes a fact.
7. Main agent periodically re-evaluates the whole portfolio and updates steering.
8. When a verified fact is judged to be the intended answer, the operator records it as target with `finalize`.
9. Generate a clean human report at any stage, or a paper from the selected verified target.
10. Stop workers when the intended targets are verified and the dependency route is credible, or when the operator pauses/stops the project.

## Boundary tests

A claim is safe to use as a proved premise only if all are true:

- it exists in the fact graph;
- it has not been revoked;
- its predecessor chain remains valid;
- the statement actually supplies the hypothesis/conclusion needed at the current interface.

A verifier verdict establishes trust within Danus. Because the verifier is an LLM, distinguish “Danus-verified” from machine-checked formal proof.

## Common failures

- Main agent starts doing detailed proof search while the portfolio goes stale.
- Workers treat an attractive global-memory conclusion as established.
- Several agents repeat the same dead route because failures were left private.
- A verified theorem is cited at an interface where its hypotheses have not been matched.
- The operator-facing report exposes worker names, fact ids, or pipeline jargon.
- A paper is generated from “whatever looks terminal” instead of an approved target.

## Key takeaway

Trust is a pipeline property: role separation + verifier gate + content-addressed fact storage + revocation. Any shortcut around one of those weakens the system's central guarantee.


## Precondition check

Before applying a Danus method, confirm the relevant role, service, trust state, and operator authority are available. If a required precondition is absent, stop that transition and route to the documented recovery path.
