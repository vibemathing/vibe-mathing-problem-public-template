# Chapter 2: Natural Numbers and the Peano Layer

## Core Idea

Chapter 2 deliberately reconstructs natural-number arithmetic before using Mathlib's `ℕ`. The operational lesson is to stay inside `Chapter2.Nat` while proving the chapter's Peano, addition, multiplication, and order results, then cross the explicit equivalence in the epilogue. This chapter is a controlled environment for recursion, induction, algebraic structures, and transporting theorems across an equivalence.

## Frameworks Introduced

- **Peano-first construction**: `Chapter2.Nat` is an inductive natural-number type used to realize the Peano axioms. Use its constructors and its own induction principles for §2.1 proofs.
- **Recursive operation → algebraic laws**: addition and multiplication are defined recursively, then associativity, commutativity, cancellation, distributivity, order laws, and exponentiation are built from those recurrences. Prove the defining equations first; use them as rewrite rules for later algebra.
- **Bridge after construction**: the epilogue defines `Chapter2.Nat.toNat`, proves `equivNat`, and establishes preservation of addition, multiplication, order, and powers. Use this as the sanctioned escape hatch to Mathlib `ℕ`.
- **Axiomatic portability**: the epilogue packages Peano axioms for an abstract type. This separates properties caused by the concrete inductive implementation from properties available to every Peano model.

## Key Concepts

- **successor and induction** — the engine for every recursive proof in the custom type.
- **recursive addition/multiplication** — unfold at the argument dictated by the definition; do not assume Mathlib's `Nat.add` equations apply definitionally.
- **order from addition** — many early order facts are characterized by existence of an additive difference; cancellation lemmas are therefore central.
- **structure instances** — the chapter gradually installs algebraic/order instances, so later proofs can use generic notation and tactics once those instances exist.
- **equivalence transport** — a theorem on `Chapter2.Nat` can be moved to `ℕ` only after using the provided equivalence/preservation lemmas.

## Operational Procedure

1. Confirm the goal's `Nat` means `Chapter2.Nat`; namespace ambiguity is common.
2. Search the same section for the recursive equation corresponding to the outermost operation.
3. For universally quantified natural-number statements, choose the induction form that matches the recurrence. The project also develops stronger/backward-style induction helpers; use them when the hypothesis naturally refers to all smaller values.
4. Normalize successors, zero, and recursive additions/multiplications with local rewrite lemmas.
5. Use `simp`, `omega`, or algebraic tactics only after the custom structure has supplied the required instances and rewrite facts.
6. In the epilogue or later chapters, convert through `equivNat` rather than reusing custom definitions indefinitely.

## Decision Points

| Situation | Route |
|---|---|
| Goal is §2.1–2.3 | stay in `Chapter2.Nat` |
| Need familiar arithmetic automation | first expose local semiring/order structure; then use automation |
| Goal compares custom and Mathlib naturals | use `toNat`/`equivNat` and map lemmas |
| Proof works only by importing a later Mathlib theorem | check whether it bypasses the chapter's intended construction |

## Anti-patterns

- Replacing `Chapter2.Nat` with `ℕ` at the start. This erases the exercise's purpose and often creates coercion noise.
- Assuming theorem names such as `Nat.add_comm` refer to Mathlib. Namespace resolution must be checked.
- Golfing an inductive argument into an opaque automation call when the local recursive equations are the actual lesson.
- Transporting equality across the bridge without showing the operation is preserved.

## Code Example

```lean
-- Shape of the intended workflow:
induction n with
| zero => simp
| succ n ih => simp [Chapter2.Nat.add, ih]
```

Use the exact local recursive lemma names present in the target section; the snippet shows the proof shape, not a universal drop-in proof.

## Source Map

- `Analysis/Section_2_1.lean` — Peano axioms, custom naturals, induction.
- `Analysis/Section_2_2.lean` — addition, order, cancellation, induction variants.
- `Analysis/Section_2_3.lean` — multiplication, distributivity, exponentiation, ordered semiring behavior.
- `Analysis/Section_2_epilogue.lean` — equivalence with Mathlib naturals and abstract Peano models.

## Key Takeaways

1. Treat Chapter 2 as its own arithmetic universe until the epilogue.
2. Recursive definitions determine the useful induction and rewrite orientation.
3. Bridge the custom type to `ℕ` explicitly and transport operations with preservation lemmas.
4. Automation is a finisher; the conceptual proof remains recursion/induction plus cancellation/order.
5. When a later chapter uses `ℕ`, do not reintroduce `Chapter2.Nat` unless the task explicitly asks about the construction.

## Connects To

- **Chapter 3**: foundations and custom constructions continue, then are retired through a bridge.
- **Chapter 4–5**: quotient-style number constructions repeat the pattern “construct locally, prove laws, connect to standard types.”
- **Appendix A**: induction proofs still rely on the same implication/quantifier mechanics described there.
