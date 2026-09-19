# Consolidated core: Prove2me operations

## Purpose

Use Prove2me to discover formalization work, inspect exact Lean statements, prepare and replay candidates, contribute reusable material and interpret server verification. The platform is an external verification surface, not the local truth ledger.

## Identity first

For every platform object capture:

- canonical mission/theorem/definition identifier;
- exact Lean declaration and imports;
- platform revision or visible update time;
- parent mission and dependency links;
- current public status;
- author/submission identity when relevant.

Titles and paraphrases are not stable identifiers. Never infer one ID from another number.

## Discovery

Select work by exact theorem type, dependency value, local toolchain compatibility and absence of conflicting active/public work. Distinguish:

- open mission;
- reusable definition request;
- theorem proof;
- sketch/decomposition;
- review or verification;
- already-proved/public object.

Before claiming novelty, perform a fresh platform/repository competition check when that policy applies.

## Statement comparison

Compare the platform type with the local ProblemContract field by field:

- carrier/domain;
- quantifier order;
- definitions and imported namespaces;
- explicit/implicit hypotheses;
- equality/equivalence notion;
- conclusion strength;
- classical assumptions.

Record exact, stronger, weaker, overlapping or unrelated. A platform theorem can be valuable without being the root theorem.

## Local proving loop

1. reproduce the pinned Lean environment;
2. place the exact declaration in a minimal local file;
3. inspect existing definitions and dependencies;
4. construct a proof without placeholders or unsafe escapes;
5. replay from a clean process;
6. inspect axioms and theorem type;
7. freeze source and environment digests.

If exact local reproduction is unavailable, label the artifact a candidate and state the obstruction.

## Sketch and decomposition

A sketch must expose child lemmas, why they imply the parent and which are already established. Child missions should be reusable mathematical interfaces, not arbitrary fragments designed only to create activity. Preserve a dependency DAG and avoid circular proof through published child results.

## Reusable definitions

Definitions should have stable names, minimal imports, explicit semantics and useful API lemmas. Check that a definition does not make a theorem vacuous or encode the desired result directly. Publication of a definition is not verification of downstream claims.

## Submission gate

Before network write, re-check:

- exact target ID and current status;
- source digest and theorem name;
- local clean replay;
- forbidden-token/axiom policy;
- permissions and active account;
- duplicate/competition state;
- public-boundary and secret scan;
- authorized transport.

If delivery status is ambiguous, observe the target before retrying to avoid duplicates.

## Server verdict handling

Bind a verdict to submitted bytes, theorem ID, environment, server receipt and time. Interpret outcomes narrowly:

- `Proved`: server accepted the exact submitted theorem in its environment;
- rejected/error: diagnose statement, elaboration, dependency, policy or transport separately;
- pending/unknown: no mathematical conclusion.

A server `Proved` verdict does not establish local ProblemContract faithfulness, novelty, independent replay or Result admission.

## Contribution and publication

Keep candidate preparation, server verification and public visibility separate. Public writes require explicit authorization. Preserve attribution and platform terms. Never publish local private paths, credentials, hidden session state or unrelated research artifacts.

## Failure recovery

- statement drift: freeze the newly observed type and redo comparison;
- dependency mismatch: pin or reconstruct the exact environment;
- duplicate work: stop publication and retain local reusable facts;
- server/local disagreement: compare source bytes, imports, toolchain and axioms;
- transport uncertainty: inspect before retry;
- proof search stall: record the precise Lean goal and mathematical obligation, not repeated tactic noise.

## Handoff receipt

Return identifiers, statement comparison, local replay data, source digest, dependency graph, server result if any, public-write status, residual obligations and the strongest justified evidence capability.
