# Chapter 3: Multiplication World — Lift the Induction Pattern, Then Reuse Symmetry

## Core Idea

Multiplication repeats the addition architecture one level higher. Its primitive recursion is `mul_zero a : a * 0 = 0` and `mul_succ a b : a * succ b = a * b + a`. The efficient strategy is to prove the missing left-facing laws, establish commutativity, then use commutativity to turn expensive mirror proofs into short rewrites.

## Frameworks Introduced

- **Recursive lifting**
  - When to use: a multiplication theorem contains a variable in the second factor.
  - How: induct on that factor; `mul_succ` converts the step into addition, where earlier algebra closes the gap.

- **Symmetry reuse after `mul_comm`**
  - `one_mul` can be obtained from `mul_one` by commuting once.
  - `add_mul` can be obtained from `mul_add` by commuting the outer multiplication and the resulting factors, avoiding a second distributivity induction.

- **Cross-layer normalization**
  - Multiplication steps create sums, so addition associativity/commutativity is part of the multiplication proof toolkit.

## Key Concepts

- `mul_one m : m * 1 = m`: direct consequence of `mul_succ` at zero plus `mul_zero`/addition simplification.
- `zero_mul m : 0 * m = 0`: a mirror theorem proved by induction because the primitive recursion is on the second factor.
- `succ_mul a b : succ a * b = a * b + b`: the left-successor mirror needed for commutativity.
- `mul_comm`: swaps factors and unlocks theorem reuse.
- `two_mul`: converts `2 * m` into `m + m`, later useful in the square expansion.
- `mul_add` / `add_mul`: left/right distributivity.
- `mul_assoc`: nested products can be regrouped.

## Procedure: prove a multiplicative law

1. Inspect which factor contains the recursive variable.
2. If it is the second factor, induction usually exposes `mul_zero`/`mul_succ` directly.
3. If the theorem is a left-facing analogue, first check whether a known right-facing theorem plus `mul_comm` proves it.
4. In an induction step, rewrite `mul_succ`; this produces sums. Use `add_assoc`, `add_comm`, or `add_right_comm` to align the IH and desired result.
5. For distributivity, pick the variable whose successor expansion produces one recursive copy plus one new term; normalize the newly produced sums.
6. After `mul_comm` is established, prefer transport by symmetry over duplicate induction.

## Representative reuse pattern

```lean
-- schematic: derive right distributivity from left distributivity
rw [mul_comm, mul_add]
-- commute the component products into target orientation
repeat rw [mul_comm c]
rfl
```

The exact arguments matter: broad `rw [mul_comm]` can swap an unintended multiplication. Instantiate the theorem when the expression contains several products.

## Decision table

| Goal feature | Route |
|---|---|
| `a * 0` or `a * succ b` | primitive multiplication equations |
| `0 * b` or `succ a * b` | proved mirror lemmas / induction |
| factor order blocks a theorem | `mul_comm` with explicit arguments |
| multiplication over a sum | `mul_add` or `add_mul` |
| nested products | `mul_assoc` |
| step produces tangled sums | addition AC normalization |

## Anti-patterns

- **Re-proving every mirror theorem by induction** after `mul_comm` is available. This wastes proof effort and obscures dependency structure.
- **Unqualified commutativity rewrites** in expressions with multiple products. They can rewrite the wrong occurrence and create a loop.
- **Forgetting the addition layer**. A `mul_succ` step lands in additive algebra; if sums are not normalized, the IH may appear “missing.”
- **Assuming cancellation already holds**. Basic Multiplication World establishes algebraic laws; multiplicative cancellation needs nonzero reasoning developed later.

## Key Takeaways

1. Multiplication recursively reduces to addition, so multiplication proofs depend on additive normalization.
2. Establishing commutativity changes proof economics: many left/right variants become transport problems.
3. Use explicit theorem arguments when local symmetry must target one product.
4. Distribution and associativity follow the same base/step template as addition, with richer normalization in the step.
5. Zero remains a special multiplicative case; do not infer later cancellation principles prematurely.

## Connects To

- **Ch 4**: power recursion reduces to multiplication.
- **Ch 8**: product zero/nonzero and cancellation add the missing side conditions.
- **Ch 9**: controlled automation handles some normalization that is tedious by hand.

## Source anchors

`Game/Levels/Multiplication/L01mul_one.lean` through `L09mul_assoc.lean`; `Game/MyNat/Multiplication.lean`; additive dependencies from Addition World.
