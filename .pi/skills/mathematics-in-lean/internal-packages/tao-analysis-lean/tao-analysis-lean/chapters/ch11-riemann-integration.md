# Chapter 11: Riemann and Riemann–Stieltjes Integration

## Core Idea

Chapter 11 builds integration from bounded intervals and partitions through piecewise-constant approximations, upper/lower Riemann integrals, integrability criteria, continuous and monotone integrability, a nonintegrable example, Riemann–Stieltjes integration, the two fundamental theorems of calculus, and change-of-variable/integration-by-parts formulas. The dominant proof pattern is approximation plus order bounds, with explicit attention to interval representation and totalized limit-like operations.

## Frameworks Introduced

- **Interval/partition infrastructure**: `BoundedInterval` coerces to sets, but the coercion is not injective because multiple interval descriptions can denote the empty set. Prove set-level facts when representation identity is unnecessary.
- **Piecewise-constant approximation**: integrability is approached through step-like majorants/minorants. Many inequalities reduce to finite partition sums and monotonicity.
- **Upper/lower integral squeeze**: the Riemann integral is characterized when upper and lower values coincide. To prove integrability, construct approximations whose gap can be made arbitrarily small.
- **Integrability closure laws**: addition, scalar multiplication, negation/subtraction, order bounds, extension, joining intervals, products/absolute values/max-min supply a reusable algebra after the definition is established.
- **Regularity ⇒ integrability**: uniform continuity on bounded intervals gives integrability of continuous functions; monotonicity gives another route; piecewise continuity extends the class.
- **Riemann–Stieltjes extension**: integration against a monotone/controlled `α` uses left/right limits, jumps, and `α_length`. Several source definitions are totalized; continuity/monotonicity/bounded-variation-like hypotheses carry semantic weight.
- **FTC pipeline**: integration creates continuous/differentiable accumulation functions; antiderivatives recover integrals; integration by parts and change of variables follow from derivative/product/chain rules.

## Key Concepts

- bounded intervals, partitions and common refinements;
- piecewise constant functions;
- majorization/minorization;
- upper/lower Riemann integral and `IntegrableOn`;
- continuous, piecewise-continuous, monotone integrability;
- integral test for series;
- Dirichlet-style nonintegrable function;
- one-sided limits/jumps and Riemann–Stieltjes integral;
- antiderivatives and the two FTCs;
- integration by parts and substitution.

## Operational Procedure

1. Normalize the interval at the set level. If the proof only uses the points contained in an interval, avoid proving equality of `BoundedInterval` constructors.
2. For a partition argument, isolate finiteness/order/mesh facts and prove the finite sum inequality first.
3. For integrability, choose the criterion matching the function: uniform continuity, continuity on compact interval, monotonicity, piecewise continuity, or direct upper/lower approximation.
4. Once `IntegrableOn` is known, use the closure API rather than returning to the upper/lower definition for algebraic combinations.
5. For the integral test, connect monotone nonnegative function bounds to series partial sums; check index shifts from the chapter's 0-based conventions.
6. For Riemann–Stieltjes, establish the integrator's monotonicity/continuity or the theorem's exact conditions before evaluating `right_lim`, `left_lim`, jump, or `α_length` expressions.
7. For FTC I, treat the integral as an accumulation function and use continuity/integrability to obtain derivative statements.
8. For FTC II, provide an antiderivative on the correct interval and rewrite the integral as endpoint difference.
9. For integration by parts or substitution, prove derivative/continuity/integrability hypotheses first, then invoke the chapter's consequence theorem.

## Failure Recovery

- **interval coercion equality fails** → compare the coerced sets; empty bounded intervals have nonunique representations.
- **upper/lower integral inequality stalls** → explicitly build or refine a majorant/minorant/partition instead of manipulating the infimum/supremum abstractly.
- **continuous integrability proof is long** → route through uniform continuity on compact intervals.
- **Riemann–Stieltjes limit gives a default** → prove the one-sided limit exists from continuity/monotonicity before using it.
- **change-of-variables theorem has extra conditions** → inspect source conventions; some continuity assumptions were added to make `α_length` behavior valid.

## Reference Table

| Function class / goal | Route |
|---|---|
| continuous on bounded interval | compactness → uniform continuity → integrable |
| monotone | monotone-integrability theorem |
| piecewise continuous | partition into continuous pieces |
| prove nonintegrable | exhibit persistent upper/lower gap |
| Riemann–Stieltjes | integrator regularity + RS API |
| integral from antiderivative | FTC II |
| derivative of accumulated integral | FTC I |
| product/substitution formula | FTC + derivative rules |

## Source Map

`Section_11_1` Partitions; `11_2` Piecewise constant functions; `11_3` Upper and lower Riemann integrals; `11_4` Basic properties of the Riemann integral; `11_5` Riemann integrability of continuous functions; `11_6` Riemann integrability of monotone functions / integral test; `11_7` A non-Riemann integrable function; `11_8` The Riemann–Stieltjes integral; `11_9` The two fundamental theorems of calculus; `11_10` Consequences of the fundamental theorem of calculus, including integration by parts/change of variables.

## Key Takeaways

1. Prove set-level interval facts when constructor identity is irrelevant.
2. Integrability proofs are approximation/squeeze arguments; reuse regularity theorems when available.
3. Once integrability is established, use closure laws rather than unfolding definitions.
4. Riemann–Stieltjes operations have meaningful domain/regularity guards.
5. FTC converts between derivative and integral representations and powers the final transformation formulas.

## Connects To

- **Chapter 9** supplies compactness and uniform continuity.
- **Chapter 10** supplies derivative/chain/product rules.
- **Measure Theory supplement** generalizes integration beyond Riemann methods.
