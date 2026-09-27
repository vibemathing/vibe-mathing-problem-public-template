# Chapter 5: Prover Mode Routing

## Core Idea
Choose a prover mode from the state of the objective. Repeating the same generic prompt after a qualitatively different failure wastes budget.

## Decision Tree
- **Blueprint declarations exist; Lean file/stubs are missing** → `formalize`. Create compiling declaration stubs with intended signatures and scoped `sorry` bodies.
- **Normal proof obligations in a compiling file** → `prove`. Search, attempt, build helpers, and close sorries.
- **Complex theorem stalled after ordinary proof passes** → `fine-grained`. Convert each mathematical sentence of the blueprint proof into an atomic named lemma, attempt each, then assemble.
- **Planner has verified a genuine missing Mathlib ingredient** → `mathlib-build`. Implement an axiom-free project-side abstraction/lemma instead of repeatedly searching for a nonexistent theorem.
- **Sorries are gone and code quality needs cleanup** → `polish`. Improve structure while preserving semantics and working proofs.
- **Explicit proof minimization request** → `golf`. Reduce proof size only after correctness is secure.

## Fine-Grained Recovery Pattern
Extract atomic claims; prove easy ones quickly; preserve partial tactic bodies at the exact stuck point; compile the file; report N/M claims closed and precise blockers. If a sentence remains too large, decompose recursively.

## Missing Infrastructure Ladder
Before declaring an infrastructure gap: check whether an informal-agent provider is available; search/try the current library; if the missing local helper is reasonably small, attempt to implement it; only then record the precise missing statement and route it to `mathlib-build` or planning.

## Integrity Constraints
Never weaken a substantive type just to remove a sorry. Keep working proof bodies unchanged unless the selected mode specifically targets refactoring/golf. New helpers must be reported as blueprint debt.

## Source Provenance
Primary: all files under `src/archon/.archon-src/prover-modes/`, Lean4 command/reference corpus, prompt validation tests.

## Frameworks Introduced
- **State-to-mode router**: file/declaration state selects the prover behavior.
- **Recursive atomization**: when a theorem is too large, convert proof sentences into named lemmas; recurse until blockers are local and testable.
- **Infrastructure gradient**: verify absence, attempt local construction, then elevate genuine gaps to dedicated infrastructure work.

## Key Concepts
- **Formalize**: statement/stub generation from an existing blueprint.
- **Prove**: default proof-closing mode.
- **Fine-grained**: sentence-level decomposition and proof attempts.
- **Mathlib-build**: project-side implementation of missing reusable infrastructure.
- **Polish**: post-proof quality cleanup.
- **Golf**: explicit proof minimization.

## Mental Models
- Think of modes as **failure-specialized algorithms**. A mode switch changes the search geometry; it is more meaningful than merely granting another generic session.
- In fine-grained mode, optimize **coverage of proof sentences** before depth on a single blocker.

## Anti-patterns
- **Formalize a file that already has correct stubs**: duplicates declarations or avoids the real proof task.
- **Repeated generic prove on a monolith**: hides which mathematical sentence is blocking.
- **Type weakening**: turns an unresolved theorem into a different easier statement and corrupts the project contract.
- **“Mathlib lacks it” without evidence**: absence must follow actual search/attempts.

## Worked Example
A theorem's sorry survives three `prove` passes. The blueprint proof has seven substantive sentences. Switch to `fine-grained`: create seven private lemmas, close five quickly, leave partial tactic bodies in the two blocked lemmas, and assemble the main theorem using all seven names. The result still has sorries, yet the next plan sees two precise blockers instead of one opaque theorem. If one blocker is a verified missing reusable theorem of moderate size, route that lemma to `mathlib-build`.

## Key Takeaways
1. Mode selection is a routing decision, not decoration.
2. Preserve intended signatures through failure.
3. Decompose until a failure has a named mathematical cause.
4. Promote genuine reusable gaps into explicit infrastructure tasks.

## Connects To
- **Ch 03**: blueprint detail determines decomposition quality.
- **Ch 06**: Lean tactics/search/verification inside a mode.
- **Ch 07**: mode switches are a convergence intervention.
