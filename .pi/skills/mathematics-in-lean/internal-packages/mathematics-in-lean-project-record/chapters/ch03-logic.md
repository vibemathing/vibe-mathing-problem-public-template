# Chapter 3: Logic

## Core Idea
Lean's tactics mirror the introduction and elimination rules of logic. Identify the outer logical constructor of a goal or hypothesis, then introduce, construct, destruct, or split exactly that structure. Complex analysis-style proofs become compositions of these small moves plus arithmetic/library lemmas.

## Frameworks Introduced
- **Implication / universal quantifier**
  - When to use: target begins with `A → ...` or `∀ x, ...`.
  - How: `intro`/`rintro` moves quantified variables and assumptions into the context. To use a universal/implicational theorem, apply it to objects/hypotheses or `apply` it backward.
- **Existential witness lifecycle**
  - When to use: target or hypothesis contains `∃`.
  - How: construct with `use` or an anonymous constructor; consume with `rcases`, `rintro`, or `obtain`. Nested patterns can destruct several layers at once; `rfl` inside a pattern can substitute an equality immediately.
- **Negation normalization**
  - When to use: negations wrap quantifiers or compound propositions.
  - How: remember `¬A` means `A → False`; prove it by introducing `A`. Use `by_contra` for classical contradiction, `push_neg` to move negations inward, and `contrapose!` when the contrapositive has a cleaner shape.
- **Conjunction / iff construction**
  - When to use: target `A ∧ B` or `A ↔ B`.
  - How: `constructor`; use `.1`/`.2`, `.left`/`.right`, or destructuring to consume. Iff lemmas can also rewrite goals.
- **Disjunction and case analysis**
  - When to use: a theorem/hypothesis offers alternatives, or a proof depends on whether `P` holds.
  - How: prove with `left`/`right`; consume with `rcases h with hA | hB`; generate classical alternatives with `by_cases h : P` or excluded middle.
- **Equality adjustment trio**
  - When to use: function equality, congruent outer functions, or almost-matching theorem conclusions.
  - How: `ext` for pointwise equality, `congr` to peel common outer functions, `convert` to apply a theorem modulo equality side-goals.

## Key Concepts
- **Lambda abstraction**: `fun x ↦ ...` creates a function/proof term by introducing a variable.
- **Hidden quantifier**: definitions such as monotonicity, subset, injectivity, surjectivity, or bounds unfold to quantified propositions.
- **Classical reasoning**: some transformations, such as deriving an existential counterexample from failure of a universal statement, need classical logic.
- **Ex falso**: from `False`, any proposition follows (`exfalso`, `False.elim`, `contradiction`).
- **Bounded quantifier**: notation like `∀ x ∈ s, ...` expands to implication with membership.
- **Convergence**: the chapter's ε–N example is a stress test for combining logic, witnesses, inequalities, and helper lemmas.

## Mental Models
- Treat a proposition as a **data shape**: `∃` packages a witness, `∧` packages two proofs, `∨` packages a tagged alternative.
- Use `rintro`/`rcases` as **pattern matching on proofs**.
- Think of `push_neg` as a **logical normalizer** that exposes the witnesses/counterexamples a direct proof needs.
- For long proofs, sketch the **pen-and-paper witness strategy first**; Lean is best at checking a clear plan, not inventing it.

## Anti-patterns
- **Trying arithmetic before opening logical structure**: `linarith` cannot invent an existential witness or choose a disjunct.
- **Using classical contradiction when direct construction is easy**: it hides useful computational content and often lengthens the proof.
- **Letting `rw` fight lambda syntax**: normalize with `dsimp` or `change` when the desired occurrence is hidden.
- **Flattening a convergence proof into one tactic call**: keep ε choices, thresholds, bounds, and final estimates explicit.

## Code Examples
```lean
example {P Q : Prop} (hP : P) (hPQ : P → Q) : Q := by
  exact hPQ hP
```
```lean
example {α : Type*} {P : α → Prop} (h : ∃ x, P x) : ∃ x, P x := by
  rcases h with ⟨x, hx⟩
  use x
```
```lean
example (P : Prop) : ¬¬P → P := by
  intro h
  by_cases hp : P
  · exact hp
  · exact False.elim (h hp)
```
- **What they demonstrate**: direct implication, existential unpack/repack, and classical case analysis.

## Reference Tables
| Shape | Construct | Consume |
|---|---|---|
| `∀ x, P x` | `intro x` | specialize `h x` |
| `A → B` | `intro hA` | apply theorem to `hA` |
| `∃ x, P x` | `use witness` | `rcases h with ⟨x, hx⟩` |
| `A ∧ B` | `constructor` | `h.1`, `h.2`, `rcases` |
| `A ↔ B` | `constructor` | `h.mp`/`h.mpr` or `.1`/`.2` |
| `A ∨ B` | `left` / `right` | case split |
| `¬A` | `intro hA`; prove `False` | apply to proof of `A` |

## Section-by-Section Operational Map

**3.1 Implication and the Universal Quantifier.** `intro` works even when a quantifier is hidden by a definition. Definitions such as function upper bounds and monotonicity turn into quantified goals on demand. If Lean's goal is syntactically noisy after beta reduction, `dsimp` or `change` can reveal the intended formula. Proof terms `fun x h ↦ ...` are the term-level counterpart of `intro` followed by theorem application.

**3.2 The Existential Quantifier.** The standard cycle is *destruct an existing witness → compute a new witness → verify it*. `rcases` supports nested patterns and `rfl` substitution. Surjectivity is a universal-existential property, so a proof often reads `intro y; use x; ...`. `field_simp` is useful after choosing a rational/algebraic witness with denominators.

**3.3 Negation.** Direct negation proofs end in `False`; contradiction and contraposition are adapters. `push_neg` is especially valuable when nested `¬∀`/`¬∃` expressions hide the witness shape. Classical reasoning appears when proving existence from double negation or from failure of a universal statement.

**3.4 Conjunction and iff.** Conjunctions can be unpacked by pattern, accessed with projections, or built with anonymous constructors. An iff can be treated both as a two-field object and as a rewrite theorem. This dual role makes iff lemmas ideal for normalization layers such as absolute-value or divisibility characterizations.

**3.5 Disjunction.** Producing `A ∨ B` requires choosing a side; consuming it creates multiple goals. Case splits often come from order trichotomy, zero-product lemmas, or `by_cases`. Use branch-local names and keep each case self-contained.

**3.6 Sequences and Convergence.** `ext`, `congr`, and `convert` appear because real proofs rarely match library statements syntactically. The convergence exercises teach how to isolate auxiliary results—eventual boundedness, constant multiplication, product-to-zero—and compose them into the main theorem. Generalize the index type when the proof used only order structure.

## Failure Recovery Notes

- If a proof of `¬A` gets stuck, inspect whether `A` itself contains quantifiers that should be destructured after introduction.
- If `push_neg` does not expose the expected shape, unfold the user-defined predicate first with `dsimp only [...]`.
- If `rcases` syntax becomes difficult, destruct one layer at a time; correctness matters more than a compact pattern.
- If a `convert` proof produces surprising side goals, check the conversion depth and whether a definitional equality would be better handled with `change`/`simpa`.

## Worked Example
To prove the sum of two convergent sequences converges, start with arbitrary `ε > 0`. Ask each convergence hypothesis for a threshold using `ε / 2`; destruct the resulting existentials to obtain `Ns` and `Nt`. Choose `max Ns Nt` for the new threshold. For any later `n`, derive both component bounds, rewrite the target difference into a sum of differences, apply the triangle inequality, then finish the arithmetic. This example illustrates a reusable architecture: introduce universal data → obtain witnesses from hypotheses → construct a combined witness → derive local facts → close by a domain theorem.

## Key Takeaways
1. Let the outer logical connective choose the structural tactic.
2. Witnesses are explicit data; plan them mathematically before invoking automation.
3. `rcases`/`rintro` are the default tools for consuming nested logical structure.
4. Use `push_neg` and `contrapose!` when they expose a constructive goal shape.
5. Build long proofs from named intermediate claims and controlled transformations.
6. `ext`, `congr`, and `convert` are essential adapters between mathematical equivalence and syntactic goal shape.

## Connects To
- **Ch 4**: sets/functions reduce extensively to the logic patterns here.
- **Ch 5–6**: induction adds recursive proof structure on top of these connectives.
- **Ch 11**: filters package the repeated quantifier bookkeeping seen in ε–N proofs.
