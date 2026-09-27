# Chapter 4: Integers, Rationals, and Gaps

## Core Idea

Chapter 4 demonstrates quotient-style construction of familiar number systems. Integers arise from formal differences of naturals; rationals arise from formal fractions of integers. The practical Lean skill is to distinguish representative-level calculations from quotient-level statements, prove operations respect the equivalence relation, and use bridge/equivalence results rather than reasoning by arbitrary representatives after the quotient API is established.

## Frameworks Introduced

- **Formal object → equivalence relation → quotient**: encode the intended mathematical object with easy representatives, state when two representatives denote the same value, then form a quotient. Every operation must be compatible with that relation before it descends.
- **Lift operations safely**: addition, negation, multiplication, order, and division-like operations are first defined on representatives or via quotient lifts. The critical obligation is well-definedness under equivalent representatives.
- **Structure accumulation**: once operations are well-defined, the chapter installs ring/ordered-ring/field behavior. After those instances exist, generic algebra tactics become useful.
- **Bridge to standard types**: the constructed integers/rationals are compared with Mathlib's `ℤ`/`ℚ`. Use these bridges for interoperability; preserve the local construction when solving construction exercises.
- **Gap diagnosis**: the rational-number discussion culminates in phenomena such as the square-root-of-two gap. This motivates the Cauchy-completion construction of Chapter 5.

## Key Concepts

- **representative invariance** — a proof about a quotient operation cannot depend on which equivalent representative was chosen.
- **quotient induction** — when a statement is inherently about representatives, use the quotient eliminator/induction principle and discharge the representative case.
- **normalization** — representative arithmetic often reduces to polynomial or ordered-ring goals, where `ring`, `linarith`, `nlinarith`, `norm_num`, and cast normalization can finish.
- **nonzero hypotheses** — formal fractions need denominator validity. If the implementation totalizes an otherwise partial operation, semantic results still require the appropriate nonzero assumptions.
- **absolute value and exponentiation** — by §4.3 the API is close enough to ordinary arithmetic that theorem selection matters more than quotient mechanics.

## Operational Procedure

1. Read the target definition to see whether the goal is on a raw pair/formal fraction or on the quotient type.
2. If defining a new quotient operation, prove congruence/well-definedness before attempting algebraic laws.
3. If proving a quotient theorem, prefer the established quotient API. Descend to representatives only when the theorem's proof genuinely needs their structure.
4. Normalize natural/integer/rational casts explicitly. Use `norm_cast` or `push_cast` after checking the direction of the coercion.
5. Separate denominator nonzero/positivity obligations from the main algebra. Prove them early and name them.
6. Use ring/order automation only after the quotient and coercion layers have been removed from the local goal.
7. For “why real numbers are needed” arguments, identify the rational cut/gap property; do not smuggle in completeness of `ℝ` before Chapter 5's construction.

## Decision Table

| Symptom | Diagnostic | Recovery |
|---|---|---|
| equality of quotient values is hard to rewrite | stuck at representative boundary | use quotient equality criterion or induction |
| `ring` does nothing | quotient/coercion wrappers remain | expose representative algebra first |
| division theorem proves nonsense at denominator 0 | totalization/domain issue | add/prove nonzero hypothesis |
| cast from custom integer/rational fails | wrong bridge direction | use established equivalence/map lemma |
| rational square-root argument wants completeness | theorem is ahead of chapter | stay with order/gap contradiction |

## Anti-patterns

- Proving quotient equality by asserting representatives are literally equal.
- Re-running well-definedness in every theorem instead of using the descended operation.
- Conflating Mathlib `ℤ`/`ℚ` with the chapter's constructed types merely because notation looks identical.
- Using real-number completeness to solve a rational-gap exercise whose purpose is to motivate reals.

## Source Map

- `Analysis/Section_4_1.lean` — integers from formal differences and their algebra/order.
- `Analysis/Section_4_2.lean` — rationals from formal fractions and field/order structure.
- `Analysis/Section_4_3.lean` — rational absolute value and exponentiation.
- `Analysis/Section_4_4.lean` — gaps in the rationals and square-root phenomena.

## Key Takeaways

1. Quotient proofs alternate between representation management and ordinary algebra; solve those layers separately.
2. Well-definedness is part of the operation, not an optional cleanup step.
3. Once algebraic instances exist, exploit generic tactics instead of expanding quotient internals again.
4. Guard every semantically partial operation with its domain condition.
5. Chapter 4's rational gaps are the direct dependency for Chapter 5's completion by Cauchy sequences.

## Connects To

- **Chapter 5** repeats the quotient pattern at a higher level: Cauchy sequences modulo equivalence become real numbers.
- **Chapter 6** assumes the standard real-number bridge and focuses on limit behavior rather than quotient construction.
