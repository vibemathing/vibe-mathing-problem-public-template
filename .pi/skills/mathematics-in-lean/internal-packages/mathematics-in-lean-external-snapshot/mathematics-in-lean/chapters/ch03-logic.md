# Chapter 3: Logic

## Core Idea
Read a proposition by its outer connective and use the corresponding introduction or elimination rule. Once logical structure is exposed, domain-specific mathematics becomes a smaller local obligation.

## Frameworks Introduced

- **Connective-driven proof routing**
  - `∀ x, P x` / `A → B`: `intro` or `rintro` the bound data/hypothesis.
  - `∃ x, P x`: provide a witness with `use` or `refine ⟨..., ...⟩`; destruct assumptions with `rcases`/`obtain`.
  - `¬ A`: remember this is `A → False`; introduce `A` and derive contradiction.
  - `A ∧ B`: construct both parts; destruct with tuple patterns.
  - `A ↔ B`: construct two implications; use `.mp`/`.mpr` or rewrite by the iff.
  - `A ∨ B`: choose a branch for a goal; split an assumed disjunction with `rcases`.

- **Classical escape hatch**
  - When to use: direct constructive structure is awkward and the theorem is classically valid.
  - How: `by_contra` converts a target to contradiction; `by_cases p` splits on a proposition; `push_neg` normalizes negated quantifiers/relations; `contrapose!` can turn an implication into a more usable equivalent.
  - Failure mode: classical reasoning can make witness extraction less transparent. Prefer direct constructions when they are available.

- **Definition exposure**
  - When to use: a logical definition is hidden behind a named predicate such as monotonicity, injectivity, set inclusion, or convergence.
  - How: `dsimp`/`change` to expose its quantified/implicational structure, then use the connective router.

- **Epsilon proof assembly**
  - When to use: elementary sequence convergence stated as `∀ ε > 0, ∃ N, ∀ n ≥ N, ...`.
  - How: introduce epsilon and positivity, extract bounds from convergence hypotheses, combine indices with `max`, and finish the pointwise inequality. For products, first derive eventual boundedness of one factor.

## Key Concepts

- **Currying**: multi-argument implications are nested functions, so repeated `intro` matches function construction.
- **Function.Injective**: hidden universal implication `f x = f y → x = y`.
- **Function.Surjective**: hidden `∀ y, ∃ x, f x = y`.
- **Contrapositive**: replace `A → B` by `¬B → ¬A` under classical/propositional equivalence when it fits hypotheses better.
- **Excluded middle**: classical split `p ∨ ¬p`, exposed operationally by `by_cases p`.
- **Extensionality**: functions are equal when equal on every input; usually begin with `ext`.
- **`congr`**: peel equal outer applications to expose equality of arguments.
- **`convert`**: use a theorem whose statement nearly matches the goal, generating equality side goals for the mismatch.
- **`ConvergesTo`**: the chapter’s explicit epsilon–N predicate for real sequences; Chapter 11 later subsumes this pattern with filters and `Tendsto`.

## Mental Models

- Propositions are interfaces: each connective defines how to build a proof and how to consume one.
- Destructure assumptions early when their internal witness/cases are needed; keep them bundled when a library lemma consumes the whole proposition.
- Negation is an implication into `False`, so contradiction tactics do not introduce a new logical universe; they reorganize an implication proof.
- Epsilon convergence is a nested quantifier protocol. Every bound has a scope; combine finite many “eventually” requirements by taking a maximum index.

## Anti-patterns

- **Trying arithmetic before opening logical connectives**: solvers cannot invent missing witnesses or choose disjunction branches.
- **Using `rw` against a definition that has not reduced to the expected syntax**: use `change`/`dsimp` first.
- **Blind contradiction**: `by_contra` can enlarge the context without moving toward a concrete contradiction; identify which hypothesis will clash with the negated goal.
- **Product-limit proof without boundedness**: convergence of `s n` to `a` does not directly give a small product error until one factor is controlled.

## Code Examples

```lean
example {P Q : Prop} (h : P ∧ Q) : Q ∧ P := by
  rcases h with ⟨hP, hQ⟩
  exact ⟨hQ, hP⟩
```

- **What it demonstrates**: destruct and reconstruct according to conjunction structure.

```lean
example {f : ℝ → ℝ} (h : ∀ a, ∃ x, f x < a) : ¬ ∃ b, ∀ x, b ≤ f x := by
  rintro ⟨b, hb⟩
  rcases h b with ⟨x, hx⟩
  linarith [hb x]
```

- **What it demonstrates**: existential witness extraction reduces a logical contradiction to linear arithmetic.

```lean
example {x : ℝ} (h : x^2 = 1) : x = 1 ∨ x = -1 := by
  have : (x - 1) * (x + 1) = 0 := by nlinarith
  rcases mul_eq_zero.mp this with h1 | h2
  · left; linarith
  · right; linarith
```

- **What it demonstrates**: algebraic normalization creates a disjunction, then each logical branch becomes a local arithmetic goal.

## Reference Table

| Proposition shape | Build it | Consume it |
|---|---|---|
| `∀ x, P x` | `intro x` | specialize `h x` |
| `A → B` | `intro hA` | `exact h hA` / `apply h` |
| `∃ x, P x` | `use x` | `rcases h with ⟨x, hx⟩` |
| `¬ A` | `intro hA` → contradiction | apply to proof of `A` |
| `A ∧ B` | `constructor` / `⟨hA,hB⟩` | `.1`, `.2`, `rcases` |
| `A ↔ B` | two implications | `.mp`, `.mpr`, `rw [h]` |
| `A ∨ B` | `left` / `right` | `rcases h with hA | hB` |

## Worked Example

For a product of convergent real sequences, expand `s n * t n - a * b` into a sum such as `(s n - a) * t n + a * (t n - b)`. Convergence of `t` first yields an eventual bound on `|t n|`. Choose an index large enough for that bound and for both error estimates; `max` combines the finite index requirements. Then use triangle/product inequalities and linear arithmetic. This elementary proof pattern motivates the filter `Eventually` abstraction in Chapter 11, where the “take a maximum index” bookkeeping is handled by filter intersection.

## Key Takeaways

1. The outer logical connective supplies the default first tactic.
2. Existence and images carry witnesses; expose them when the next mathematical step depends on the witness.
3. Classical tactics are routing tools; use them when the direct constructive route is less natural.
4. `change`, `congr`, and `convert` are bridges between mathematically equivalent forms that elaboration does not align automatically.
5. Explicit epsilon proofs reveal the bookkeeping later abstracted by filters.

## Connects To

- **Ch 4**: set membership and image/preimage statements reduce to the same logical constructors.
- **Ch 5–6**: induction and finite combinatorics add recursion/case structure to this logical core.
- **Ch 11**: replaces repeated epsilon/eventual bookkeeping with `Filter`, `Tendsto`, and `Eventually`.
