# Chapter 9: Real Sets, Function Limits, and Continuity

## Core Idea

Chapter 9 moves fully into real analysis with Mathlib sets and topology. It develops adherent/limit points, closure and boundedness, function limits, continuity, one-sided limits, compact extrema, the intermediate value theorem, monotonicity, uniform continuity, and limits at infinity. The key operational technique is to make the domain filter explicit and use `Filter.Tendsto` when composition or topology is involved.

## Frameworks Introduced

- **Set topology on the line**: adherent points, limit points, isolated points, closure, closedness, and boundedness are tied to Mathlib concepts. Heine–Borel is the bridge from closed+bounded to compact behavior on `ℝ`.
- **Globally defined functions with domain restriction**: to avoid dependent-type friction, source functions are often `ℝ → ℝ` even when the mathematics studies them only on `X ⊆ ℝ`; values outside `X` are irrelevant/junk. Always carry the domain in the limit/continuity predicate.
- **Epsilon limit ↔ filter limit**: `Convergesto` captures the chapter's pointwise limit and has a bridge to Mathlib filter convergence. Use it to transfer uniqueness, arithmetic, composition, and sequential criteria.
- **One-sided filters**: left/right limits are domain restrictions, not separate algebraic objects. Existence must precede any use of a totalized one-sided limit value.
- **Compactness → extrema/uniformity**: continuous functions on compact/closed bounded intervals attain extrema and become uniformly continuous. This is the standard route when a proof asks for global control from local continuity.
- **Infinity as `atTop`/`atBot` behavior**: limits at infinity are expressed using filter combinations such as `atTop ⊓ principal X`.

## Key Concepts

- intervals, adherent points, closure, closed sets, bounded sets, Heine–Borel;
- pointwise arithmetic on functions;
- `Convergesto`, sequential and filter characterizations;
- continuity / continuity on a set;
- one-sided limits and discontinuity types;
- maximum/minimum principle on compact sets;
- intermediate value/fixed-point arguments;
- monotone functions and inverse behavior;
- uniform continuity and sequence criteria;
- limits at infinity and unbounded sets.

## Operational Procedure

1. Write down the domain `X` and the approach point `x₀`. Determine whether `x₀` is an adherent or limit point; uniqueness theorems often need this.
2. For a direct epsilon proof, introduce `ε`, obtain a `δ`, and keep the conjunction “x in X, x near x₀” visible.
3. For sums/products/compositions or library topology theorems, convert the chapter predicate to `Filter.Tendsto` and use the restricted/principal filter corresponding to the domain.
4. For continuity, reuse the limit bridge rather than duplicating epsilon arithmetic whenever a Mathlib continuity theorem already matches the section's phase.
5. For one-sided limits, encode the appropriate side in the domain/filter and prove existence before using `left_lim`/`right_lim`-style values.
6. For extrema or uniform continuity on a bounded interval, first establish compactness via closed+bounded/Heine–Borel, then apply the compactness theorem.
7. For an IVT problem, establish continuity and endpoint order/sign conditions, then invoke connected/intermediate-value behavior.
8. For limits at infinity, use `atTop`/`atBot`; translate back to the quantified `M`–`ε` form only when the target asks for it.

## Failure Recovery

- **A continuity theorem ignores the set** → you chose global `Continuous` instead of `ContinuousOn`/restricted filter.
- **Limit uniqueness fails** → the approach point may not be an adherent/limit point of the domain.
- **Function value outside X enters the proof** → restrict the statement; those values were introduced only to keep the function total.
- **One-sided limit simplification yields a default** → establish existence first.
- **Uniform continuity proof repeats local δ choices indefinitely** → use compactness of the domain.

## Reference Table

| Problem | First route |
|---|---|
| closure/limit point | topology + sequence/adherent characterization |
| limit algebra/composition | `Filter.Tendsto` bridge |
| pointwise continuity | continuity/limit equivalence |
| endpoint / one-sided behavior | restricted side filter/domain |
| attain max/min | compactness + continuity |
| uniform continuity on interval | compactness theorem |
| `x → +∞` | `Filter.atTop` |

## Source Map

`Section_9_1` Subsets of the real line; `9_2` The algebra of real-valued functions; `9_3` Limiting values of functions; `9_4` Continuous functions; `9_5` Limits from the left and right; `9_6` The maximum principle; `9_7` The intermediate value theorem; `9_8` Monotone functions; `9_9` Uniform continuity; `9_10` Limits at infinity.

## Key Takeaways

1. Domain filters are part of the theorem; total functions do not erase domain assumptions.
2. Use the epsilon representation for pedagogy and filters for composition/interoperability.
3. Adherent/limit-point hypotheses control uniqueness and differentiability-like statements.
4. Compactness packages the hard global arguments behind extrema and uniform continuity.
5. One-sided and infinite limits are most robustly handled as filter restrictions.

## Connects To

- **Chapter 6** supplies the convergence/filter pattern for sequences.
- **Chapter 10** builds differentiability within sets on the continuity/domain infrastructure here.
- **Chapter 11** uses compactness and uniform continuity to prove integrability.
