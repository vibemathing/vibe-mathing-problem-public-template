# Chapter 8: Advanced Multiplication — Zero Is the Side Condition

## Core Idea

Multiplication looks like advanced addition until zero enters. Additive cancellation has no extra guard, while multiplicative cancellation is invalid for a zero common factor. The world therefore builds an explicit **nonzero reasoning layer** before proving product cancellation and “product equals self/one” results.

## Frameworks Introduced

- **Product witness transport**
  - From `a ≤ b` with `b = a + c`, multiply through and construct a new gap to prove `a*t ≤ b*t` using distribution.

- **Product nonzero propagation**
  - If `a*b ≠ 0`, each relevant factor must be nonzero; conversely, nonzero factors produce a nonzero product after constructor analysis.

- **Nonzero-to-successor bridge**
  - A natural `a ≠ 0` must be `succ n` for some `n`. Case-split `a`: the zero branch contradicts `ha`; the successor branch supplies the predecessor witness.
  - This immediately supports `1 ≤ a` for nonzero `a`.

- **Zero-product dichotomy**
  - From `a*b = 0`, conclude `a = 0 ∨ b = 0`. This is the branch structure required before safe cancellation.

- **Generalized induction for cancellation**
  - `mul_left_cancel` has multiple variables coupled by the equation `a*b = a*c`. A naive induction can freeze `c` and yield an IH too weak for successor cases. Generalize the dependent variable while inducting.

## Key Concepts

- `mul_le_mul_right`: right multiplication preserves the witness-based `≤` relation.
- `mul_left_ne_zero`: product nonzero implies a factor nonzero.
- `eq_succ_of_ne_zero`: structural form of positive/nonzero naturals.
- `one_le_of_ne_zero`: converts nonzero to an order fact.
- `le_mul_right`: a nonzero product provides a witness that `a ≤ a*b`.
- `mul_right_eq_one`: if a product equals one, the relevant factor is one.
- `mul_ne_zero` / `mul_eq_zero`: positive and zero branches for products.
- `mul_left_cancel`: cancellation with explicit `ha : a ≠ 0`.
- `mul_right_eq_self`: from `a*b=a` plus `a≠0`, infer `b=1` by rewriting `a` as `a*1` then cancelling.

## Procedure: any multiplication cancellation problem

1. Locate the common factor.
2. Check for an explicit proof that this factor is nonzero.
3. If missing, determine whether the existing hypotheses imply nonzero; product-nonzero hypotheses can often supply it.
4. Normalize the equation so the common factor occupies the theorem's supported side. Use `mul_comm` only as needed.
5. Apply `mul_left_cancel` (or a mirrored route).
6. For `a*b=a`, first rewrite the standalone `a` as `a*1`; then cancel `a` under `ha`.
7. If the factor may be zero, stop: the desired cancellation is not valid without stronger assumptions.

## Procedure: derive cancellation theorem by induction

When proving the theorem itself, induction must preserve enough generality. If the recursive step changes a second variable, use the custom induction tactic's `generalizing` facility so the IH remains universally quantified over that variable. Then split zero/successor cases and use zero-product/nonzero lemmas plus additive cancellation after `mul_succ` expansion.

## Failure diagnostics

- **“Obvious” cancellation cannot be applied**: inspect `ha : a ≠ 0`. Its absence is a mathematical blocker, not just a tactic mismatch.
- **IH cannot be applied after a case split**: the IH is too specialized; generalize the variable before induction.
- **Product nonzero proof stalls**: case-split a factor and use the zero branch to contradict its nonzero hypothesis; the successor branch unfolds multiplication.
- **`a*b=1` proof seems to require factorization machinery**: exploit tiny target `1`, nonzero deductions, and constructor/order lemmas already available.

## Anti-patterns

- Canceling a common multiplicative factor without proving it nonzero.
- Copying the simpler addition proof architecture unchanged; multiplication has a genuine exceptional zero branch.
- Using a fixed-variable induction hypothesis when recursive manipulation changes that variable.
- Treating `tauto` as arithmetic automation; it only resolves propositional consequences once arithmetic facts are supplied.

## Key Takeaways

1. Zero is the central exceptional case for multiplication.
2. Nonzero facts should be converted into structural successor data when arithmetic needs a concrete shape.
3. Multiplicative cancellation is conditional and must keep the nonzero guard visible.
4. Generalizing dependent variables is a proof-design tool, not a syntax trick.
5. Advanced multiplication combines every earlier layer: recursion, addition, implication, order witnesses, cases, and contradiction.

## Connects To

- **Ch 7** supplies the witness-based order methods.
- **Ch 5** supplies implication/negation reasoning.
- **Ch 3** supplies distribution/commutativity/associativity.
- **Failure recovery** contains the generalized-induction diagnostic in compact form.

## Source anchors

`Game/Levels/AdvMultiplication/L01mul_le_mul_right.lean` through `L10mul_right_eq_self.lean`; custom `Induction.lean`, `Have.lean`; dependencies from prior active worlds.
