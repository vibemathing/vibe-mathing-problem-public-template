# Cheatsheet

## Route by Goal

| Signal | Chapter/API |
|---|---|
| custom Peano naturals | ch02; `Chapter2.Nat` |
| custom sets/functions | ch03; `Chapter3.SetTheory` |
| constructed `ℤ`/`ℚ` | ch04; quotient workflow |
| rational Cauchy → custom real | ch05; `Chapter5.Real` |
| sequence limits / limsup | ch06; epsilon ↔ filters, `EReal` |
| series / root-ratio tests | ch07; partial sums, tails, `EReal` |
| countable / indexed sums | ch08; `Equiv`, `Countable`, `Summable`, `tsum` |
| function limits / continuity | ch09; restricted filters / `Tendsto` |
| derivatives | ch10; `HasDerivWithinAt` first |
| Riemann / FTC | ch11; `IntegrableOn` + regularity routes |
| logic/quantifiers | ch12 |
| decimals | ch13 |
| Lebesgue/Jordan | ch14 |
| units / SI | ch15; `Scalar` → `Formal` |

## Before Theorem Search

1. Which source section?
2. Custom type, bridge, or Mathlib phase?
3. 0-based index shift needed?
4. Does the definition have a junk/default branch?
5. `ℝ`, `EReal`, or `ENNReal`?
6. set or subtype?
7. epsilon predicate or filter?

## Common Repairs

| Symptom | Repair |
|---|---|
| expected `ℕ`, got custom Nat | use Ch2 epilogue map/equiv |
| set/subtype mismatch | expose `Subtype.val` / membership |
| limit algebra too verbose | bridge to `Filter.Tendsto` |
| no real supremum bound | move to `EReal` |
| infinite sum has arbitrary value | prove `Summable` first |
| derivative value exists but uniqueness fails | add limit-point condition |
| `derivWithin = 0` unexpectedly | prove differentiability; inspect fallback |
| sequence/sum off by one | state the 0↔1 index map first |
| scalar dimensions commute but types differ | `Scalar.cast` or `toFormal_inj` |
| interval constructors refuse equality | compare coerced sets |

## Tactic Roles

- `intro`, `constructor`, `obtain`/`rcases`: logical skeleton.
- `rw`, `simp`, `simpa`: local normalization.
- `calc`, `have`: expose mathematical steps.
- `ext`, `funext`: extensional equality.
- `norm_cast`, `push_cast`: numeric coercions.
- `omega`: discrete Nat/Int arithmetic.
- `linarith` / `nlinarith`: ordered algebra.
- `ring` / `field_simp`: polynomial/rational algebra after denominators/types are settled.
- `positivity`, `gcongr`: positivity and monotone inequalities.

## Stop Conditions

Return “insufficient to justify” when a required convergence, boundedness, measurability, nonzero/sign, domain, or limit-point hypothesis cannot be derived. Do not infer mathematics from a totalized default value.
