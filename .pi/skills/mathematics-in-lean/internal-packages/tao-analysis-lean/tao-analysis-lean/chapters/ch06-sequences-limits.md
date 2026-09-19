# Chapter 6: Real Sequences, Limits, and Extended Reals

## Core Idea

Chapter 6 develops limits of real sequences, extended-real suprema/infima, limsup/liminf and limit points, standard limits, subsequences, and real exponentiation, then connects the chapter's definitions with Mathlib's filter language. The operational strategy is to choose one convergence representation for each proof and to move to `EReal` whenever infinity is a legitimate bound or limit value.

## Frameworks Introduced

- **Pedagogical epsilon layer**: the chapter provides concrete notions of closeness, Cauchy behavior, boundedness, convergence, and a `lim`-style value. Direct exercises often expect epsilon proofs with explicit thresholds.
- **Totalized limit**: a numeric limit operator can return a fallback when a sequence does not converge. Use a convergence theorem before extracting semantic facts from the chosen value.
- **Extended-real envelope**: `EReal` supports `⊤` and `⊥`, making it the safe codomain for unrestricted suprema/infima and limsup/liminf. Finiteness becomes an explicit theorem rather than an implicit assumption.
- **Tail sup/inf method**: limsup and liminf are built from suprema/infima of sequence tails. Monotonicity of these tail envelopes drives comparison and convergence theorems.
- **Subsequence invariants**: convergence passes to subsequences; limit points are captured via subsequential behavior. For divergence/compactness arguments, construct or extract a subsequence rather than manipulating a global limit symbol.
- **Filter bridge**: the epilogue connects chapter notions to Mathlib's `Filter.Tendsto`, Cauchy sequences, `limUnder`, `sSup`, and `sInf`. This is the preferred route for composition and mature Mathlib theorems.

## Key Concepts

- real sequence convergence and uniqueness;
- Cauchy criterion and completeness;
- bounded/monotone sequences and convergence;
- `EReal` order, suprema, infima;
- limsup, liminf, limit points;
- squeeze/comparison principles;
- standard limits such as reciprocal powers, geometric behavior, roots;
- subsequences and extraction;
- rational/real exponentiation continuation.

## Operational Procedure

1. Classify the target as **epsilon-native**, **filter-native**, or **extended-real**.
2. For epsilon-native goals, introduce `ε > 0`, choose a threshold, and explicitly manage all “for n ≥ N” conditions. Use `max` to merge thresholds from multiple convergent sequences.
3. For algebraic limit laws, consider converting known limits to `Filter.Tendsto`, applying Mathlib composition/arithmetic lemmas, then converting back only if the statement requires the chapter predicate.
4. For sup/inf or limsup/liminf, stay in `EReal` until you have a theorem establishing finiteness. Coercing too early loses the unbounded cases the definition is designed to represent.
5. For a monotone bounded sequence, separate monotonicity from boundedness; then apply the monotone-convergence result matching the direction.
6. For standard limits, reduce to one of a few reusable shapes: geometric decay, squeeze, monotone bounds, or logarithmic/exponential comparison.
7. For subsequences, prove the index map is strictly monotone/unbounded before transferring convergence.
8. For real exponentiation, verify positivity/nonnegativity conditions and distinguish the chapter's construction from native Mathlib power notation.

## Failure Modes

- **`lim` gives a usable-looking number without a convergence proof**: semantic guard is missing.
- **supremum theorem asks for boundedness**: the quantity may naturally belong in `EReal`; change representation rather than inventing a bound.
- **epsilon algebra grows uncontrollably**: switch through the documented filter equivalence.
- **a subsequence statement has an index mismatch**: check the 0-based strictly monotone index map and any shifted convention.
- **root/ratio comparison mixes `ℝ` and `EReal`**: prove finiteness or keep the whole inequality in `EReal`.

## Reference Table

| Task | Preferred representation |
|---|---|
| elementary definition exercise | epsilon predicates |
| combine limits / compose functions | `Filter.Tendsto` bridge |
| unbounded sup/inf | `EReal` |
| limsup/liminf | tail sup/inf in `EReal` |
| convergence from subsequence | subsequence API + uniqueness |
| later Mathlib interoperability | filters / native `sSup`/`sInf` |

## Source Map

`Section_6_1` convergence/laws; `6_2` extended reals; `6_3` sequence sup/inf; `6_4` limsup/liminf/limit points; `6_5` standard limits; `6_6` subsequences; `6_7` exponentiation II; `6_epilogue` Mathlib-limit connections.

## Key Takeaways

1. Pick epsilon, filter, or extended-real form deliberately; repeated conversions create proof friction.
2. Never infer mathematical convergence from a totalized numeric limit alone.
3. Keep infinity-sensitive quantities in `EReal` until finiteness is proven.
4. Threshold combination and subsequence index control are recurring low-level proof obligations.
5. The epilogue is the interoperability layer for subsequent analysis.

## Connects To

- **Chapter 7** uses sequence limits to define and test series convergence.
- **Chapter 9** generalizes the epsilon/filter pattern from sequences to function limits and continuity.
