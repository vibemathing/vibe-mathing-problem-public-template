# Chapter 7: Proof Translation and Proof Equivalence

**Source coverage**: §2.3, printed pp. 982-984.

## Core Idea
Expansion proofs can act as a normalizing intermediate representation: many surface proofs share the same expansion structure. Translate that compact core into natural deduction for readability, checking, and mixed interactive/automatic proving.

## Frameworks Introduced
- **Proof-to-expansion-to-natural-deduction pipeline**
  - When to use: when a machine proof is difficult to inspect or comes from a search calculus optimized for automation.
  - How: derive an expansion proof from the machine proof (eliminating cuts if needed), merge redundant branches/instances, then reconstruct a natural-deduction proof.
- **Tactic-guided reconstruction**
  - When to use: when converting an expansion proof into a structured derivation.
  - How: treat the current goal and assumptions as a goal situation; consult the expansion proof before choosing backwards/forwards inference rules and witness terms.
- **Essential-sameness criterion**
  - When to use: when comparing two proofs for substantive equivalence.
  - How: regard proofs corresponding to the same expansion proof as sharing the same fundamental proof idea, despite different rule orderings or presentation details.

## Key Concepts
- **merging**: eliminating redundancy in an expansion proof before presentation.
- **natural deduction**: a human-readable proof style used as a reconstruction target.
- **tactic**: a procedure that reduces a goal to subgoals by applying inference rules.
- **goal situation**: a conclusion to derive under a set of assumptions.
- **proof equivalence via expansion proof**: a way to ignore superficial ordering differences and compare proof ideas.

## Mental Models
- Search in a representation optimized for **finding**, present in a representation optimized for **understanding**.
- Use the expansion proof as a **semantic spine**: tactics should consult it to avoid arbitrary rule choices during reconstruction.
- Treat merging as **proof compression**, not only formatting.

## Anti-patterns
- **Forcing search to operate directly in a human-pretty proof format**: this can entangle search with irrelevant ordering and presentation choices.
- **Translating without removing redundancy**: the resulting proof may be correct yet obscure the actual idea.
- **Using a reconstruction rule too early**: for an existential goal, wait until the expansion proof supplies a suitable witness instead of guessing blindly.

## Reference Tables

| Need | Use expansion proof to decide |
|---|---|
| prove a disjunction | whether one disjunct already follows from assumptions |
| prove an existential | whether a suitable witness term is supported |
| choose indirect proof | whether the expansion structure indicates a contradiction route |
| compare proof presentations | whether they reduce to the same expansion structure |

## Worked Example
For a goal `A or B`, a reconstruction tactic can inspect the expansion proof. If the proof data already shows `A` follows from the current assumptions, the tactic works backward from disjunction introduction and replaces the goal with `A`. For a goal `exists x. A(x)`, the tactic waits until the expansion proof identifies a suitable term `t`; then it reduces the goal to `A(t)`. This prevents proof presentation from becoming a second blind search problem.

## Key Takeaways
1. Keep proof discovery and proof presentation as separate stages.
2. Merge expansion proofs before reconstruction to remove redundancy.
3. Let proof data guide tactic choices and witness selection.
4. Use natural deduction as an independent readability/correctness check.
5. For semi-automatic proving, let users supply an outline and automate the gaps.

## Connects To
- **Ch 6**: expansion proofs provide the intermediate representation.
- **Ch 10**: search procedures should focus on finding the invariant proof core.
- **Ch 14**: proof transformation quality is part of prover architecture.
