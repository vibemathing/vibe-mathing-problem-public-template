---
name: mathematics-in-lean
description: Lean 4 and Mathlib proof-engineering guidance for translating frozen mathematical statements, finding library declarations, choosing tactics and structures, debugging elaboration, and producing auditable proof candidates without sorry or unsafe escapes.
---

# Mathematics in Lean

Use this Skill when the current obligation calls for a Lean 4/Mathlib formalization or proof repair.

## Workflow

1. Freeze the natural-language statement, domains, quantifiers, definitions, assumptions, and allowed axioms.
2. Translate it into a minimal Lean declaration without strengthening, weakening, or changing implicit hypotheses.
3. Search existing Mathlib declarations before introducing new definitions or lemmas.
4. Prefer structural lemmas and typed intermediate claims over long tactic scripts.
5. Compile in the repository-pinned toolchain with explicit timeout and capture the exact command, versions, source digest, diagnostics, and exit status.
6. Audit for `sorry`, `admit`, `sorryAx`, unsafe escapes, unexpected axioms, and accidental vacuity.
7. Request a separate statement-faithfulness review. Kernel acceptance checks the encoded theorem, not its correspondence to the ProblemContract.

## Failure behavior

If the pinned toolchain is unavailable, the statement is ambiguous, or required imports cannot be established, return a bounded formalization plan and the precise obstruction. Never fabricate compilation or kernel receipts.

## Progressive disclosure

Read `references/consolidated-core.md` before substantial proof work. It consolidates goal-shape routing, equality/sets/induction/algebra/order/topology/analysis/linear-algebra/quotient/measure patterns, theorem search, tactic selection, elaboration diagnosis, abstraction control and formalization integrity from the reviewed Lean-oriented source families. The text is project-authored and does not redistribute source chapters.
