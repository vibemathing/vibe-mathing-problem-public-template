# Chapter 9: Strict Verification

## Core Idea
Rethlas verification is a separate, structured pass over the complete markdown proof. It checks local deductions in order, independently checks external references, validates the final JSON shape, and accepts only when every critical error and every gap is gone.

## Frameworks Introduced

- **Sequential statement verification**
  - **When to use**: every complete candidate proof.
  - **How**: extract target assumptions first; read the proof in textual order; split reasoning into small deductions; check logical validity, theorem use, required assumptions, existence/property claims, and unexplained jumps.
- **Definition/formula identity audit**
  - **When to use**: a step transfers a property, theorem, or term across contexts.
  - **How**: compare exact definitions, formulas, notation, quantifiers, and ambient objects. Similar names or formulas are insufficient.
- **External-reference verification**
  - **When to use**: any paper theorem/lemma/definition is cited.
  - **How**: search `search_arxiv_theorems` with the complete referenced statement, compare the matched text, expand paper-local definitions, then check both applicability and the deduction made from the cited result. If theorem search finds no match, repeat with web search; if the reference still cannot be found, record a critical error at the citation site.
- **Strict verdict rule**
  - **When to use**: report synthesis.
  - **How**: `correct` only when both `critical_errors` and `gaps` are empty. Any finding forces `wrong` plus concrete non-empty repair hints.
- **Verifier-driven repair loop**
  - **When to use**: a candidate returns any error/gap.
  - **How**: persist the verification service response exactly as returned—`verification_report.summary`, `critical_errors`, `gaps`, `verdict`, and `repair_hints` keep their names and JSON structure. Repair critical errors first, allow strategy/backtracking changes when necessary, close all remaining gaps, then run verification again.

## Key Concepts

- **Critical error** — false implication, contradiction, theorem misuse, or invalid external application.
- **Gap** — missing derivation, vague justification, unsupported existence/property claim, suspiciously unused assumptions, or definition/formula ambiguity.
- **Statement checks** — per-location local proof findings.
- **Reference checks** — independent external citation findings.
- **Repair hints** — concrete instructions required whenever verdict is wrong.
- **Verification schema** — JSON structure enforcing report, verdict, and repair-hint consistency.

## Mental Models

- Verify a proof as **an executable dependency chain**: every step must have its prerequisites.
- Treat similar terminology as **potential type mismatch** until definitions agree exactly.
- Treat unused assumptions as a **diagnostic smell**: they may be redundant, or the proof may have skipped the place they matter.
- Let verifier findings trigger **global strategy repair** when a local patch would preserve a broken route.

## Anti-patterns

- **Self-accepting a proof because generation feels confident**.
- **Checking only the final theorem conclusion** while skipping intermediate deductions.
- **Accepting a citation after finding a similar theorem title**.
- **Returning `correct` with a gap list** or returning `wrong` without actionable repair hints.
- **Calling the canonical verifier on an incomplete fragment**.

## Reference Table

| Finding state | Verdict | Repair hints |
|---|---|---|
| no critical errors, no gaps | `correct` | empty |
| any critical error | `wrong` | non-empty |
| any gap | `wrong` | non-empty |
| malformed verification payload | invalid output | repair report shape first |

The verification schema permits only the expected top-level fields and requires each finding to contain a non-empty location and issue.

## Worked Example

A cited theorem is real, but its paper defines “regular” with respect to a topology different from the current proof. The reference check should classify the application as a critical error even if the displayed theorem looks similar. The generator must either prove the required compatibility or replace the citation, then submit the entire repaired proof again.

## Key Takeaways

1. Check the proof in textual order at small-step granularity.
2. Audit existence and property assumptions explicitly.
3. Compare exact definitions and formulas across contexts.
4. Verify external references and their downstream deductions separately.
5. Apply the zero-errors/zero-gaps acceptance rule mechanically.
6. Persist every verifier response and repair until the strict gate passes.

## Connects To

- **Ch 5**: applicability discipline begins during retrieval.
- **Ch 8**: complete proof/citation formatting makes verification possible.
- **Ch 10**: the local HTTP API runs the verifier and returns the structured payload.

## Source Provenance

Primary source files: `agents/verification/AGENTS.md`, all three verification skill files, `agents/verification/mcp/server.py`, `agents/verification/api/server.py`, and `agents/verification/schemas/verification_output.schema.json`.
