# Patterns — Mathematics in Lean

## Goal-Shape Routing
**When to use**: At the start of any proof or debugging session.
**How**: Read the target's outer constructor; inventory local hypotheses and typeclasses; choose a structural tactic that removes one layer; only then invoke domain automation. Equality suggests rewriting/extensionality; implication/universal quantification suggests introduction; existence suggests a witness; conjunction suggests two subgoals; disjunction suggests a branch or case split.
**Trade-offs**: A fast guess can work, but systematic routing avoids long tactic searches.

## Rewrite → Normalize → Automate
**When to use**: An algebraic goal contains local equalities, definitions, or awkward syntax.
**How**: Rewrite hypotheses/definitions in the smallest useful scope; normalize with `simp only`, `dsimp`, or `change`; use `ring`, `linarith`, `norm_num`, `omega`, `group`, `abel`, or `noncomm_ring` on the simplified residue.
**Trade-offs**: Aggressive `simp` or `erw` can hide the reason a proof works and may become brittle.

## Local Lemma Bridge
**When to use**: The final step is routine once one non-obvious fact is available.
**How**: State the missing fact with `have`; prove it in an indented subproof; return to the main goal and discharge it with `exact`, `apply`, `linarith`, or rewriting.
**Trade-offs**: More lines, but clearer proof states and better maintainability.

## Library-First Search
**When to use**: The mathematical step is standard.
**How**: Guess the theorem-name prefix from the operation and conclusion; inspect neighboring declarations; use completion or `apply?`; check exact types before forcing a custom proof. Search the weakest relevant structure, not only the concrete type.
**Trade-offs**: Depends on source-version naming; current Mathlib may rename declarations.

## Introduce / Destruct / Construct
**When to use**: Logical connectives or data constructors dominate the goal.
**How**: `intro`/`rintro` for `∀` and `→`; `rcases`/`obtain` to consume `∃`, `∧`, and `∨`; `use` for existential witnesses; `constructor` for `∧` and `↔`; `left`/`right` for `∨`; `by_cases` for explicit classical splits.
**Trade-offs**: Compact nested patterns are powerful but can become unreadable.

## Extensionality Before Algebra
**When to use**: Equality of functions, sets, structures, or matrices.
**How**: Use `ext` to reduce equality to values/membership/components; then normalize and solve each component. For sets, `Subset.antisymm` is an alternative when directional inclusions are more natural.
**Trade-offs**: Extensionality can create many component goals; use structure-specific lemmas when available.

## Induction Mirrors Recursion
**When to use**: The theorem follows a recursive definition or inductive datatype.
**How**: Induct on the argument structurally consumed by the definition. Generalize parameters that must vary in the inductive step. Use strong induction when the recursive call is to an arbitrary smaller value, and well-founded recursion when the decrease is governed by a custom measure.
**Trade-offs**: Inducting on the wrong variable often produces an unusable hypothesis.

## Map / Comap / Universal Property
**When to use**: Subobjects, quotients, images, filters, topologies, or morphisms are involved.
**How**: Prefer `map`/`comap` to element-chasing; use `ker` and `range` as canonical subobjects; construct maps from quotients with `lift`; construct linear maps from a basis with `Basis.constr`; use Galois connections to switch between direct and inverse forms.
**Trade-offs**: Requires knowing the bundled API, but scales much better than unfolding definitions.

## Forgetful Hierarchy Design
**When to use**: Defining reusable typeclasses and inherited mathematical structures.
**How**: Put raw operations in data classes; let richer classes `extends` poorer ones; ensure inherited data is definitionally identical along every path; use `outParam` only when source/target parameters should be inferred from the morphism type; use `DFunLike`/`SetLike` for bundled morphisms/subobjects.
**Trade-offs**: Redundant fields with canonical defaults may be necessary to avoid bad diamonds.

## Filter-First Limit Proof
**When to use**: Limits, continuity, eventual behavior, closure, or almost-everywhere reasoning.
**How**: Express convergence as `Tendsto`; compose limits algebraically; combine eventual statements with `.and`, `.mono`, or `filter_upwards`; use a `HasBasis` theorem only when converting to an ε–N/ball formulation.
**Trade-offs**: Filters add abstraction upfront but prevent a combinatorial explosion of specialized limit lemmas.

## Totalized-Operation Guard
**When to use**: `deriv`, `fderiv`, matrix inverse, division, or integration appears to work without an expected side condition.
**How**: Check the library's default value outside the intended domain. For meaningful computational statements, carry differentiability, invertibility, nonzero-denominator, or integrability hypotheses explicitly.
**Trade-offs**: Totalized definitions simplify theorem statements but can conceal degenerate cases.
