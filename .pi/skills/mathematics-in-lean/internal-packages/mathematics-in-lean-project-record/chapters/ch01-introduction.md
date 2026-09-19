# Chapter 1: Introduction

## Core Idea
Lean formalization is interactive construction of typed expressions. Mathematical objects have types, propositions have type `Prop`, and a proof is a term whose type is the proposition being proved; tactics are instructions that help Lean build such terms while exposing intermediate proof states.

## Frameworks Introduced
- **Propositions as types / proofs as terms**
  - When to use: whenever a theorem statement or tactic behavior feels opaque.
  - How: inspect an expression with `#check`; distinguish object types such as `Nat → Nat` from propositions; interpret a theorem `P` as the task of constructing an inhabitant of `P`.
  - Why it works: tactic mode and term mode ultimately produce the same kind of proof object.
- **Interactive proof-state loop**
  - When to use: every nontrivial proof.
  - How: write one step, inspect the new context and target in the editor, adjust, and continue. Use the state as feedback about what Lean inferred and what remains.
- **Tactic/term interleaving**
  - When to use: when a proof is clearer with a short explicit term inside a larger tactic script or a compact tactic block inside a term.
  - How: use `by ...` where a proof term is expected; use theorem applications directly when the result exactly matches the target.

## Key Concepts
- **Type**: every Lean expression has one; types prevent ill-formed mathematical combinations.
- **`Prop`**: the type of propositions.
- **Proof term**: an expression whose type is the proposition it proves.
- **Tactic proof**: a procedure that incrementally constructs a proof term.
- **Goal state**: local variables/hypotheses plus the target still to prove.
- **Mathlib**: the mathematical library supplying structures, theorems, notation, and automation used throughout the book.
- **`#check`**: asks Lean for an expression's type.
- **`#eval`**: evaluates computable expressions for exploration; it is not the proof mechanism.
- **`sorry`**: placeholder accepted by Lean with a warning; never acceptable in a finished proof.

## Mental Models
- Think of **formalization as typed programming for mathematics**: definitions, theorems, and proofs are expressions checked by Lean.
- Think of **tactics as a proof compiler front-end**: `rintro`, `use`, `rw`, and `ring` each transform the current obligation until a complete term exists.
- Use **incremental feedback instead of predicting the whole term**: let each proof state tell you what construction is needed next.
- Think of Mathlib as a **large API**, not a list to memorize. Learn entry points, naming patterns, and how to inspect types.

## Anti-patterns
- **Reading without running examples**: the source is designed around experimentation; proof-state feedback is part of the method.
- **Treating tactic scripts as magic strings**: always relate a tactic to the term or logical construction it creates.
- **Finishing with `sorry`**: it bypasses the correctness guarantee that makes formalization valuable.
- **Over-compressing early**: one-line proofs can be elegant after the structure is understood, but they are poor debugging surfaces.

## Code Examples
```lean
example : ∀ m n : Nat, Even n → Even (m * n) := by
  rintro m n ⟨k, hk⟩
  use m * k
  rw [hk]
  ring
```
- **What it demonstrates**: introduce variables/hypothesis, destruct an existential representation, choose a witness, rewrite, then delegate ring arithmetic.

## Reference Tables
| Need | First tool |
|---|---|
| inspect type | `#check` |
| test a computable value | `#eval` |
| see remaining obligations | editor goal view |
| construct proof incrementally | `by` + tactics |
| insert compact proof into a term | `by ...` |
| reuse a complete proof directly | theorem/proof term |

## Section-by-Section Operational Map

**1.1 Getting Started.** Set up Lean 4, VS Code, and the Mathematics in Lean project; work in a copy of the exercise files so the source stays updateable. The operational lesson is to learn interactively: run examples, inspect the Infoview after each line, edit proofs, and compare with solutions only after attempting the exercises.

**1.2 Overview.** Read Lean expressions by type: objects inhabit mathematical types, propositions inhabit `Prop`, and proofs inhabit propositions. Tactic scripts and proof terms are two interfaces to the same underlying construction. The book emphasizes tactics plus Mathlib so that formalization becomes a cycle of exposing structure, applying library knowledge, and checking each state incrementally.

## Worked Example
To prove that multiplying an even natural number by an arbitrary natural preserves evenness, first read the definition of `Even n` operationally: there is a witness `k` with `n = k + k`. `rintro` exposes that witness. The goal asks for another existential witness for `m * n`; choose `m * k`. Rewriting by the hypothesis changes the goal into an algebraic identity, and `ring` handles the routine normalization. The proof works because each tactic matches the current outer structure rather than because the tactics were guessed in advance.

## Key Takeaways
1. Always know the type of the expression you are building.
2. Read tactic execution through changes in the proof state.
3. Combine explicit mathematical choices with automation for routine residue.
4. Prefer an understandable multi-step proof while discovering the argument; compress only after it is stable.
5. Treat Mathlib as the reusable mathematical substrate for later chapters.

## Connects To
- **Ch 2**: turns the interactive loop into concrete rewriting, theorem application, and automation habits.
- **Ch 3**: explains the logical constructors behind common tactic steps.
- **Ch 7–8**: explains the typeclass machinery that makes Mathlib notation and generic theorems feel automatic.
