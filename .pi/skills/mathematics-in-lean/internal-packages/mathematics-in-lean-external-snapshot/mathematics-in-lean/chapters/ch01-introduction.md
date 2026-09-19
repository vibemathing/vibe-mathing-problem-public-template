# Chapter 1: Introduction

## Core Idea
Treat Lean formalization as an interactive loop between the mathematical plan, the current proof state, and the library. The book is designed to be worked through with its Lean source files and exercises; compiler feedback is part of the reasoning process.

## Frameworks Introduced

- **Proof-state driven development**
  - When to use: every tactic proof.
  - How: inspect the local context and goal, make one structural move, inspect the resulting goals, then continue. Keep the gap between the mathematical step and Lean step small.
  - Why it works: tactic states expose exactly what the elaborator still needs, so failures become local rather than mysterious.

- **Proof terms and tactics as two views of one proof**
  - When to use: when a tactic sequence feels opaque or a direct term is hard to elaborate.
  - How: remember that tactics construct terms. Switch to explicit terms for small reusable lemmas; switch to tactics when intermediate state inspection or case management helps.

- **Source / exercise / solution loop**
  - When to use: while learning or repairing a proof in the scope of this book.
  - How: read the statement and surrounding examples, attempt the exercise, use theorem discovery and compiler messages, then compare against the supplied solution for a stable API pattern.

## Key Concepts

- **Dependent type theory**: the foundational language in which propositions are types and proofs are terms.
- **`Prop`**: the universe of propositions.
- **Type inference**: Lean fills omitted type information when constraints determine it.
- **Elaboration**: the phase that resolves notation, implicit arguments, coercions, typeclasses, and metavariables.
- **Tactic mode**: interactive construction of a proof term while exposing goals.
- **Mathlib**: the main mathematical library; effective formalization depends heavily on reusing its abstractions and theorems.
- **`sorry`**: temporary placeholder useful for scaffolding, unacceptable in a completed proof.

## Mental Models

- Think of the editor as a theorem-proving REPL: each edit is a query about the next proof obligation.
- Treat a Lean error as evidence about an elaboration mismatch, missing premise, or wrong theorem shape; diagnose it before changing tactics at random.
- Separate the mathematical proof plan from the syntax used to communicate that plan to Lean.

## Anti-patterns

- **Writing a long tactic script without checking intermediate states**: makes the first wrong assumption expensive to locate.
- **Reproving library facts from first principles**: increases fragility and hides the intended abstraction.
- **Using `sorry` as completion**: suppresses the obligation and prevents validation.
- **Treating a successful automated tactic as an explanation**: keep enough structure in the proof to reveal the mathematical route when maintainability matters.

## Code Examples

```lean
example (a b c : ℝ) : a * (b * c) = b * (a * c) := by
  rw [← mul_assoc]
  rw [mul_comm a b]
  rw [mul_assoc]
```

- **What it demonstrates**: build an algebraic proof from named equalities while observing how each rewrite changes the target.

```lean
example (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by
  ring
```

- **What it demonstrates**: once the target is recognized as a polynomial identity, use an automation tool whose semantics match the subproblem.

## Reference Table

| Need | Typical move |
|---|---|
| See what theorem/type Lean inferred | `#check` |
| Evaluate computable expression | `#eval` |
| Explore simplification | `#simp` |
| Explore concrete arithmetic normalization | `#norm_num` |
| Inspect proof obligation | tactic state in editor |
| Scaffold a later lemma | temporary `sorry`, then remove before completion |

## Worked Example

Suppose a paper proof says “by commutativity and associativity.” In Lean, identify the exact subterm whose parenthesization blocks the commutativity step. Rewrite associativity to expose the pair, rewrite commutativity on that pair, then restore the desired association. If the expression is purely polynomial, replace the whole manual route with `ring`. The method choice follows the learning goal: explicit rewrites teach and document the algebraic laws; domain automation is more concise once the algebraic fragment is understood.

## Key Takeaways

1. Compiler feedback is part of the formal reasoning loop.
2. Tactics should correspond to identifiable mathematical transformations.
3. Learn library abstractions early; most scalable Lean proofs reuse them.
4. Keep temporary placeholders separate from finished proof status.
5. Use the supplied source and solutions as API-calibrated examples, while current project compiler output remains authoritative.

## Connects To

- **Ch 2**: turns the interactive loop into concrete rewrite, theorem-application, and automation methods.
- **Ch 3**: gives deterministic proof moves based on logical structure.
- **All later chapters**: progressively replace hand-built proofs with library abstractions and universal properties.
