# 02 — Memory and Fact Graph

## The three tiers

| Tier | Scope | Unit | Truth status | Primary use |
|---|---|---|---|---|
| local memory | one worker | rough note/event | unverified | private continuity |
| global memory | project | typed claim + evidence | unverified awareness | coordination, dedup, dead ends, strategy |
| fact graph | project | verified fact node | trusted within Danus | proof dependencies |

### Local memory

Per-worker append-only JSONL. Typical channels are `notes` and `events`. It records what the worker tried, saw, or plans. Other agents do not read it. When an idea becomes a formed claim useful to others, publish it to global memory rather than relying on private notes.

### Global memory

Shared typed JSONL with BM25 search. Important kinds include:

- verifiable by default: `conclusion`, `example`, `counterexample`, `proof_attempt`;
- judgment/strategy: `plan`, `dead_end`, `direction`, `obstacle`, `master_guidance`, `elaboration`, `verification`.

Verifiable entries carry explicit evidence and move through `unverified → verifying → verified|refuted`. Judgment entries remain steering, typically `open → supported|challenged`. A `verified` global-memory status can link to a `fact_id`; the fact graph remains the correctness source.

### Fact graph

Each fact is a Markdown node containing structured frontmatter plus `statement`, `proof`, and optional `intuition`. Core fields:

- `fact_id`
- `problem_id`
- `author`
- `predecessors`
- `glossary_introduces`
- `external_refs`

The graph is a DAG. Search is derived from fact bodies; fact files stay authoritative.

## Content addressing

A fact id is the first 16 hex characters of SHA-256 over normalized mathematical content: problem id, sorted predecessors, sorted glossary entries, statement, and proof. External references are deliberately excluded, allowing bibliography metadata to be corrected later without changing mathematical identity.

Consequences:

- identical mathematical content deduplicates naturally;
- references are stable across citation cleanup;
- a changed proof or statement produces a different id;
- the predecessor list participates in identity, binding the dependency context.

## Revocation

Revoking a fact cascade-revokes all descendants that depend on it. A new fact cannot be built on a revoked predecessor. Recovery means finding an alternative surviving proof chain or re-establishing the invalidated result under a new valid fact.

Decision rule: never “patch around” a revoked node in prose. Rebuild the dependency route explicitly.

## Glossary discipline

Project symbols must be defined and used consistently. Facts carry `glossary_introduces`; the project glossary merges definitions. A small global glossary covers universal notation. Undefined-symbol checks are heuristic support and do not replace mathematical verification.

## Retrieval procedure

Before starting a subgoal:

1. Search the worker's local memory for its own prior attempts.
2. Search global memory for related findings, counterexamples, dead ends, verification traces, and strategy.
3. Search the fact graph for established statements that can serve as predecessors.
4. Use global-memory hits to avoid duplicate search; use fact-graph hits as the only established premises.
5. If a global-memory claim is load-bearing, prove/verify it rather than citing the memory entry.

## Writing a shareable finding

A useful finding has one scope and one claim. Include:

- what is asserted or observed;
- explicit evidence or reasoning;
- whether it is objectively verifiable;
- links to subgoals/predecessors;
- glossary terms introduced;
- branch impact when it kills or strengthens a route.

Examples and counterexamples should say which assumptions hold and what conclusion does or does not hold. A dead end should name the concrete obstruction so siblings can skip the same failure.

## Failure modes

- treating global memory as a theorem database;
- hiding reusable failures in local memory;
- storing vague “look into X” entries with no scope or evidence;
- inventing fact ids in strategy prose;
- changing citation metadata and assuming fact identity changed;
- revoking a node without accounting for descendants;
- searching only one memory tier and rediscovering known work.

## Validation checklist

Before using a result downstream, ask: Is there an extant fact id? Does its statement actually match this use? Are its predecessors live? Are the relevant definitions aligned? If any answer is uncertain, stop and inspect the fact itself.
