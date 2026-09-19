# 04 — Mathlib Search, Sets, and Proof Blueprints

## Core Idea

Most formalization effort should reuse existing abstractions and theorems. The practical skill is finding the right declaration, choosing the right abstraction level, and turning a natural proof into a dependency blueprint.

## Abstraction rule: theorem first, definition when needed

A newly introduced local definition often has few specialized lemmas. Then unfolding can expose a mature lower-level theory:

```lean
unfold MyDefinition
```

For established Mathlib concepts, direct unfolding can create implementation-level obligations. Prefer high-level theorems when they exist.

Decision:

1. Is the concept local/new and transparent? Try unfolding.
2. Is it a mature Mathlib object? Search its API first.
3. Is the searched theorem expressed at a neighboring abstraction? Move one level up/down.
4. Did unfolding make the state much larger without revealing the mathematics? Undo that route and return to the API.

## Mathlib search ladder

### 1. Nearby source and navigation

Ctrl-click a definition/theorem and inspect nearby declarations. File location often reveals the relevant API family and naming vocabulary.

For a domain you use repeatedly, learn the key files and namespaces rather than repeatedly searching globally.

### 2. Naming conventions and autocomplete

Mathlib names often encode relations and argument flow. Examples of useful vocabulary:

- `lt`, `le` for `<`, `≤`;
- `of` frequently signals “derive result from arguments”;
- names concatenate logical steps, e.g. a theorem converting `<` to `≤` or chaining inequalities.

Use autocomplete after typing a plausible prefix. Treat guessed names as hypotheses, not facts: verify with `#check`.

### 3. `apply?`

Inside a tactic proof, `apply?` asks Lean for candidate applications compatible with the current goal. Use it during discovery; replace the exploratory command with the chosen explicit step in finished code.

### 4. Semantic theorem search

Use `#leansearch` or an available semantic search UI with a clear natural-language description. Also consider current equivalents of Moogle/Loogle where installed.

A good search query states:

- object type/structure;
- assumptions;
- desired conclusion;
- important relation directions.

### 5. Focused local bridge

If the exact theorem is absent but nearby primitives exist, prove a small helper lemma. Avoid building a large custom library until search confirms that the needed abstraction truly is missing.

## Sets are predicates

Mathlib's basic set model is operationally simple:

```lean
Set α  ≈  α → Prop
```

Membership `x ∈ s` means the predicate `s x` holds. This immediately explains many set operations as logical operations.

### Core correspondences

| Set notion | Predicate/logical reading |
|---|---|
| `x ∈ s` | `s x` |
| `s ⊆ t` | every `x ∈ s` implies `x ∈ t` |
| `∅` | always false predicate |
| `Set.univ` | always true predicate |
| `s ∪ t` | membership in `s` OR `t` |
| `s ∩ t` | membership in `s` AND `t` |
| `sᶜ` | NOT membership in `s` |
| `s \ t` | in `s` AND not in `t` |
| `Set.powerset s` | sets `t` satisfying `t ⊆ s` |

This lets the logic tactics from [ch03](ch03-first-order-logic-formalization.md) solve many elementary set goals once membership is exposed by `simp` or a suitable theorem.

### Image and preimage

For `f : α → β`:

- `f '' s` contains outputs `f x` for `x ∈ s`; proofs often introduce or extract a witness;
- `f ⁻¹' t` contains `x` with `f x ∈ t`; this is usually definitionally close to function application and simpler to manipulate.

Preimages compose naturally, which becomes important for topology and filters.

### Injective / Surjective / Bijective

Operational shapes:

```lean
Function.Injective f
-- f a₁ = f a₂ → a₁ = a₂

Function.Surjective f
-- ∀ b, ∃ a, f a = b

Function.Bijective f
-- Injective f ∧ Surjective f
```

So their proofs route directly through implication/universal/existential/conjunction logic.

Useful source modules highlighted by the course include the set definitions/basic operations and function-definition modules. Current Mathlib file layout can change; search by declaration name if paths differ.

## Proof blueprint method

A blueprint is the bridge between a natural proof and Lean code. It records dependencies and major state transitions without committing to every tactic.

### Construction process

1. Write the mathematical proof in numbered steps.
2. For each step, list inputs (variables/hypotheses/earlier lemmas).
3. Write the intended Lean-shaped result of that step.
4. Identify whether it is:
   - theorem application/search;
   - definition unfolding;
   - logical introduction/elimination;
   - witness choice;
   - arithmetic/normalization.
5. Draw or list dependency edges.
6. Scaffold each independent lemma.
7. Fill leaves from easiest to hardest.
8. Reintegrate and simplify the proof state.

## Worked Example — uniqueness of an elementary sequence limit

The course example gives a reusable pattern.

### Natural proof structure

Assume a sequence converges to both `a` and `b`. Suppose `a ≠ b`; reduce by symmetry to one strict order, choose epsilon roughly half the gap, obtain tail bounds for both limits, choose an index beyond both thresholds, and derive incompatible inequalities.

### Lean-shaped dependency graph

```text
goal a = b
  ↓ contradiction route
hab : a ≠ b
  ↓ order theorem + optional symmetry reduction
horder : a > b
  ↓ define ε and prove ε > 0
ε, hε
  ↙                         ↘
ha ε hε                     hb ε hε
  ↓ extract Nₐ              ↓ extract Nᵦ
Nₐ, tailₐ                   Nᵦ, tailᵦ
  ↘                         ↙
choose n > max Nₐ Nᵦ
  ↓ instantiate both tails
lower/upper inequalities
  ↓ expose ε and arithmetic
False
```

### Operational choices

- Use `unfold` for the local elementary limit definition.
- Use `let` for epsilon/index values whose definitions should remain available.
- Use `have` for positivity/order lemmas.
- Instantiate universal hypotheses by function application.
- `rcases` existential hypotheses to extract bounds.
- Use `linarith` only after all inequalities are present and expressed over reals.
- Use `wlog` for symmetry only if you can discharge the reduction branch cleanly.

## Search/recovery examples

### Unknown ordering lemma

Desired mathematical step: from `a ≠ b` in a linear order, obtain `a < b ∨ a > b`.

Search by natural language or relation vocabulary, inspect the candidate type, then apply it. Do not hardcode a remembered name until current `#check` confirms it.

### New custom set definition

If a local set is literally a predicate wrapper and no theorem exists, unfold/simp it. Once you have several reusable facts about it, stop unfolding everywhere and create a small API around the definition.

## Failure modes

- **Searching with natural-language vocabulary that differs from Mathlib structure:** include typeclass/operation names in the query.
- **Guessing a theorem name and debugging the guess:** verify immediately with `#check` or autocomplete.
- **Unfolding everything:** creates fragile proofs coupled to implementations.
- **Never unfolding anything:** traps a local concept behind an opaque wrapper with no API.
- **Blueprint merely restates prose:** every node must have inputs and an actionable Lean form.

## Key Takeaways

Mathlib work is navigation plus abstraction control. Search at the current level, descend definitions only for a reason, and use proof blueprints to separate mathematical dependencies from tactic details.

## Connects To

- Logic mechanics → [ch03](ch03-first-order-logic-formalization.md)
- Tactic mechanics → [ch06](ch06-tactic-construction.md)
- Filters rely on sets/preimages → [ch07](ch07-filters-limits-metric.md)
