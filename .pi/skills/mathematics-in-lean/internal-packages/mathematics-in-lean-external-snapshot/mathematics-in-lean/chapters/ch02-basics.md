# Chapter 2: Basics

## Core Idea
Choose proof tools from the semantic shape of the subgoal: rewrite known equalities, compose named structural theorems, and use specialized automation only after the expression has been normalized into the domain that tactic understands.

## Frameworks Introduced

- **Rewrite / calculation pipeline**
  - When to use: equality reasoning and local substitution.
  - How: orient an equality with `rw [h]` or `rw [← h]`; target a hypothesis with `at`; use `calc` when intermediate expressions matter; use `nth_rw` when only one occurrence should change.
  - Failure mode: rewriting depends on syntactic matching modulo definitional equality. If it misses, expose the hidden definition or provide explicit arguments.

- **Structural theorem application**
  - When to use: order, lattice, group, ring, divisibility, or metric facts.
  - How: inspect the theorem type with `#check`; use `exact` when it matches, `apply` when its conclusion determines premises, and named arguments/type annotations when inference is underconstrained.
  - Failure mode: `apply` can create a metavariable for an intermediate object. A `calc` chain often makes that object explicit.

- **Domain automation dispatch**
  - When to use: a normalized subgoal belongs to a tactic's decision procedure.
  - How: `ring` for polynomial identities; `linarith` for linear ordered-ring arithmetic using hypotheses; `norm_num` for concrete numerals; `group` for noncommutative group identities; `abel` for additive commutative group normalization.
  - Failure mode: automation fails when side conditions or non-domain functions are still mixed into the target. Prove monotonicity/positivity facts separately, then feed the solver the resulting inequalities.

- **Weakest sufficient typeclass**
  - When to use: proving reusable algebra/order facts.
  - How: state variables under the minimal structure (`Ring`, `Lattice`, `PartialOrder`, etc.), use that structure's defining lemmas, and add stronger assumptions only when a step truly needs them.

## Key Concepts

- **Definitional equality**: expressions Lean can reduce to the same term without a theorem; often closed by `rfl`.
- **Implicit argument**: argument inferred from expected types and other parameters.
- **Typeclass**: implicit structure parameter synthesized from registered instances.
- **`calc`**: explicit chain of equality/inequality transformations.
- **Monotonicity**: property used to lift an order relation through a function.
- **Lattice**: structure with infimum `⊓` and supremum `⊔`; generalized `min`/`max` reasoning.
- **Divisibility**: relation whose proof usually carries a multiplicative witness.
- **`IsStrictOrderedRing`**: compatibility layer connecting ring operations and order.
- **Metric space**: structure where `dist` satisfies nonnegativity, identity, symmetry, and triangle inequality.

## Mental Models

- Use `rw` when you know *what equality changes the expression*; use `apply` when you know *which theorem produces the goal*.
- Prefer `calc` when a human proof names intermediate quantities or changes relation direction.
- Treat tactic automation as a local solver attached to a mathematical theory, not as a universal search procedure.
- Generality comes from typeclasses: a proof written for a lattice or ring automatically specializes to many concrete types.

## Anti-patterns

- **`apply le_trans` with an unknown midpoint**: leaves Lean to invent a term it cannot infer. Supply the middle expression in a `calc` chain.
- **Using `linarith` before proving monotonicity facts for `exp`, `log`, or other nonlinear functions**: the solver sees opaque atoms; first derive linear inequalities between those atoms.
- **Overusing global simplification**: hides which law was decisive and can create brittle proofs.
- **Strengthening assumptions for convenience**: reduces theorem reuse and can mask the actual proof dependency.

## Code Examples

```lean
variable {R : Type*} [Ring R]

example (a b : R) : a + b + -b = a := by
  rw [add_assoc, add_neg_cancel, add_zero]
```

- **What it demonstrates**: generic algebraic proof using only ring laws.

```lean
variable (a b : ℝ)

example : a * b * 2 ≤ a^2 + b^2 := by
  have h : 0 ≤ a^2 - 2*a*b + b^2 := by
    calc
      _ = (a - b)^2 := by ring
      _ ≥ 0 := by apply pow_two_nonneg
  linarith
```

- **What it demonstrates**: derive a nonlinear mathematical fact, normalize polynomial structure, then let linear arithmetic close the final relation.

```lean
variable {α : Type*} [Lattice α] (x y : α)

example : x ⊓ y = y ⊓ x := by
  apply le_antisymm
  · exact le_inf inf_le_right inf_le_left
  · exact le_inf inf_le_right inf_le_left
```

- **What it demonstrates**: characterize equality by order and use the universal property of `inf`.

## Reference Table

| Goal class | Preferred tools | Common prerequisite |
|---|---|---|
| exact equality substitution | `rw`, `nth_rw`, `calc` | theorem orientation |
| theorem conclusion matches goal | `exact`, `apply` | inferable arguments |
| polynomial equality | `ring` | semiring/ring structure |
| linear inequality | `linarith` | ordered ring/field facts already exposed |
| numeral calculation | `norm_num` | computable/ordered algebraic structure |
| group normalization | `group` | group structure |
| commutative additive normalization | `abel` | additive commutative group |
| lattice identity | `le_antisymm`, `le_inf`, `sup_le` | lattice/order laws |

## Worked Example

To prove a statement such as `c - exp b ≤ c - exp a` from `a ≤ b`, split the proof into theories. First obtain `exp a ≤ exp b` using the library monotonicity theorem for `exp`. Then either apply an order lemma such as `sub_le_sub_left`, or let `linarith` combine the derived inequality with linear subtraction. The exponential never needs to be expanded; it is treated as an opaque quantity after its order relation is established.

## Key Takeaways

1. Normalize the goal enough to expose the mathematical theory, then choose the corresponding solver.
2. Structural lemmas and typeclasses produce more reusable proofs than concrete calculations.
3. `calc` is the safest route when a transitivity theorem leaves an intermediate term ambiguous.
4. Theorem discovery starts with exact types; inspect implicit parameters before fighting elaboration.
5. Order and lattice universal properties are reusable templates for `min`/`max`, gcd/lcm-like, and subobject reasoning.

## Connects To

- **Ch 3**: logical constructors determine proof structure before algebraic tactics run.
- **Ch 8**: explains why typeclass inference can supply the structures used here and how it can fail.
- **Ch 10–13**: the same normalize-then-apply pattern governs linear algebra and analysis APIs.
