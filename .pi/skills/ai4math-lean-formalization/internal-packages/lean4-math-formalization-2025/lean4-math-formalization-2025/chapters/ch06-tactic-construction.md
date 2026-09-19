# 06 — Tactic Construction

## Core Idea

A tactic proof is an incremental term construction. Select tactics by the term constructor/function they represent and by the exact transformation they make to the proof state.

## Core tactics

### `by`

Starts tactic construction after a declaration whose target type is already known.

### `exact term`

Close the current goal with a term whose type matches it exactly.

Use when the required proof/data is already available or can be written compactly.

### `apply term`

Use a function/theorem whose result can unify with the current target. Unfilled arguments become new goals.

Diagnostic rule: if `apply` creates unexpected subgoals, inspect the full type of `term` and implicit arguments.

### `intro`

For a function/dependent-function target, introduce the first binder into the context. Multiple names introduce multiple leading binders.

### `rfl`

Close a reflexive/definitionally equal target. If it fails, look for a rewrite/normalization theorem rather than assuming equality is false.

### `apply?`

Use during theorem discovery to obtain compatible candidate applications. Finished proofs should normally record the selected explicit theorem.

## Rewriting and calculation

### `rw`

Rewrites the first suitable occurrence by equality/equivalence.

```lean
rw [h]
rw [← h]
rw [h] at hx
rw [h] at *
```

Failure checklist: wrong direction, no syntactic/definitional match, wrong location, hidden definition.

### `calc`

Use when a proof is naturally a chain. Each link can have a different compatible relation if Lean has the transitivity instance connecting them.

If `calc` fails on an order relation, inspect direction and transitivity support rather than forcing the syntax.

### `simp`

Use simplification lemmas plus supplied facts. For robust proofs:

- prefer `simp only [...]` when you need a controlled normal form;
- add local simp lemmas only when they are valid canonical rewrites;
- avoid relying on incidental global simp behavior when an explicit step is clearer.

## Managing multiple subgoals

`case name => ...` selects a named generated case. A dot focuses the next unresolved goal.

Use case names when the constructor semantics matter or when subgoals may be reordered; dots are concise for short, obvious sequences.

## Eliminating inductive values

### `cases`

Split a term by its constructors in tactic mode. Each branch gains that constructor's arguments.

### `match`

The term-mode counterpart. Use when a direct construction remains readable.

### `rcases`

Pattern-oriented elimination. It handles structures, disjunctions, existentials, and nested combinations concisely.

Examples of pattern ideas:

```lean
rcases hAnd with ⟨ha, hb⟩
rcases hOr with ha | hb
rcases hEx with ⟨x, hx⟩
rcases h with ha | ⟨hb, hc⟩
```

Use nested patterns when they clarify the resulting context; split into separate steps when a dense pattern hides branch meaning.

## Existentials

For a goal `∃ x, P x`:

```lean
exists witness
```

creates goal `P witness`. Consecutive witnesses can be supplied together for nested existentials.

To consume an existential, destruct it with `rcases` and retain the dependency between witness and evidence.

## `let` vs `have`

This distinction is operationally important.

### `let`

Introduces a local definition and remembers how it reduces. Use for values such as an epsilon choice, midpoint, maximum index, or auxiliary expression that later needs unfolding.

### `have`

Introduces a local term/lemma of a specified type; the internal construction is not the definition you later unfold. Use for propositions and intermediate facts.

If you define a data value with `have` and later expect Lean to reduce it to its construction, you may lose the needed definitional equality. Use `let` instead.

## Contradiction and contraposition

- `contradiction`: close from contradictory context.
- `by_contra h`: assume negation of the goal and target `False` (classical when required).
- `contrapose h`: exchange/negate goal and a hypothesis.

After contraposition, rename a hypothesis if its old name now describes the opposite proposition.

## Induction

`induction t with ...` splits by constructors and provides induction hypotheses for recursive fields.

If the generated induction hypothesis is too specialized:

1. inspect which context terms depend on `t`;
2. `revert` them before induction;
3. or `generalize` an expression so induction ranges over a useful variable;
4. introduce the generalized data again in each branch.

This is a standard recovery route for failed induction design.

## Context/goal reshaping

### `revert`

Moves context terms (and dependent terms) back into the target as binders. Think of it as the inverse of `intro`.

### `generalize`

Replace a specific subexpression with a fresh variable, optionally retaining an equality linking them. Use this to strengthen an induction statement or abstract a repeated expression.

### `intros` and `rename_i`

`intros` introduces all leading binders with inaccessible names. Use `rename_i` to name the newly relevant hidden terms explicitly.

## Repetition and constructors

### `repeat`

Repeats a tactic while it succeeds. Good when repetition count is structurally obvious; risky when it hides proof shape or loops through unexpected states. Prefer explicit repetition when clarity matters.

### `constructor`

Applies the first constructor that fits; very convenient for single-constructor structures. For inductives with several constructors, specify the intended constructor via `apply`.

Constructor application can produce dependent subgoals in an order that surprises you. `fconstructor` (Mathlib) is useful when preserving field order matters.

## Worked Example — existential plus conjunction

For a goal shaped `∃ x, P x ∧ Q x`, first choose a witness with `exists`/`refine`; the remaining goal becomes a conjunction. Apply its constructor and solve the two properties separately. If the witness arrives from a hypothesis `∃ x, P x ∧ Q x`, use `rcases` to expose the witness and fields. The tactic route follows the term constructors exactly.

## Discouraged/fragile patterns from the course

### Opaque assumption search

`assumption` can be concise, but an explicit `exact hp` records which hypothesis closes the goal. Prefer explicit evidence in pedagogical or maintenance-sensitive proofs.

### Blanket `<;>`

Use `<;>` when the same following tactic genuinely belongs on every generated subgoal. Avoid it when branches soon diverge; branch structure becomes hard to read.

### `first` and nested search scripts

A script that repeatedly tries alternatives can make a proof compact but obscures why a branch works. Use deterministic constructor/theorem choices when available.

### `left` / `right`

These choose constructors by position. `apply Or.inl` / `apply Or.inr` communicates the actual constructor and survives better when the surrounding type changes.

## Tactic selection table

| Need | Prefer |
|---|---|
| close with known term | `exact` |
| use theorem/function backward | `apply` |
| introduce binder | `intro` |
| definitional/reflexive goal | `rfl` |
| substitute equality | `rw` |
| transitive calculation | `calc` |
| normalize by rewrite database | `simp` / `simp only` |
| branch on inductive evidence | `cases` / `rcases` |
| construct existential | `exists` / `refine` |
| named lemma | `have` |
| named reducible value | `let` |
| recursive proof | `induction` |
| strengthen before induction | `revert` / `generalize` |

## Key Takeaways

- Pick tactics from the target/hypothesis constructor shape.
- Use `rw` for focused substitution and `calc` for meaningful chains.
- Distinguish `let` definitions from `have` proofs.
- Strengthen the statement with `revert`/`generalize` before forcing a weak induction.
- Prefer explicit constructors and deterministic branches when maintainability matters.

## SELF_CHECK for tactic proofs

- Can you state the term-level reason each major tactic is valid?
- Does every generated branch correspond to a constructor/case you intended?
- Are local definitions (`let`) distinguished from proved facts (`have`)?
- Could a broad automation/repetition be replaced with a more stable explicit step?
- After finishing, does InfoView report no goals and does the theorem type still express the intended mathematics?

## Connects To

- Tactic semantics → [ch05](ch05-dependent-types-term-construction.md)
- Logical routing → [ch03](ch03-first-order-logic-formalization.md)
- Theorem search and long-proof blueprints → [ch04](ch04-mathlib-search-sets-blueprints.md)
