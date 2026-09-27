# Chapter 5: Cauchy Construction of the Real Numbers

## Core Idea

Chapter 5 constructs real numbers from rational Cauchy sequences. It starts with a deliberately concrete sequence API, defines eventual closeness and equivalence, quotients Cauchy sequences, equips the quotient with field/order structure, proves least-upper-bound behavior, develops roots and rational powers, then identifies the constructed type with Mathlib `ℝ`. This chapter is the main template for handling totalized definitions plus semantic side conditions.

## Frameworks Introduced

- **Extended sequence representation**: `Chapter5.Sequence` records a starting integer and acts like `ℤ → ℚ`; values before the starting point are filled with zero. `Sequence.from` similarly has an intended region and a fallback outside it. When evaluating, prove the index bound first.
- **Cauchy by eventual ε-steadiness**: Cauchy behavior is built from `Rat.Steady` and `Rat.EventuallySteady`. For direct textbook proofs, expand these quantifiers carefully; for later interoperability, look for packaged boundedness/equivalence lemmas.
- **Equivalence modulo vanishing difference**: two Cauchy sequences represent the same real when they are eventually ε-close for every positive ε. Prove this relation behaves well under arithmetic before relying on quotient operations.
- **Formal limit with validity guard**: the real construction treats suitable Cauchy sequences semantically, while unsuitable inputs may receive a default. Establish `IsCauchy` before invoking meaning-bearing `LIM` facts.
- **Completeness pipeline**: order and absolute value → upper bounds → supremum/least-upper-bound → roots/powers. Each layer uses results from the prior one; do not jump directly to Mathlib completeness when the task is about the construction.
- **Final bridge**: the epilogue relates `Chapter5.Real` to standard `ℝ`, allowing Chapter 6 to use Mathlib reals.

## Key Concepts

- `Sequence`, starting index, `ofNatFun`, `from` — representations with explicit index conventions.
- `Steady`, `EventuallySteady`, `IsCauchy` — epsilon control and boundedness.
- `CloseSeq`, `EventuallyClose`, `Sequence.Equiv` — quotient relation.
- Cauchy-sequence wrapper and quotient real type — construction boundary.
- order/absolute value, Archimedean behavior, rational density — tools for comparing constructed reals.
- custom extended-real/supremum machinery in §5.5 — completeness before the later `EReal`-centric sequence API.
- nth roots and rational exponentiation — valid-domain reasoning is essential.

## Operational Procedure

1. Normalize the sequence representation. If a source sequence starts at 1, decide whether to encode it by `mk'`, a shifted `ℕ → ℚ`, or `Sequence.from`.
2. For a Cauchy proof, fix `ε > 0`, choose a concrete threshold `N`, prove `N ≥ n₀`, then establish the pairwise bound for indices beyond `N`.
3. Prove boundedness once and reuse it for products/quotient arithmetic; Cauchy ⇒ bounded is a major helper.
4. For equivalence, work with the difference or direct eventual-closeness inequality, and explicitly manage triangle inequalities.
5. At the quotient-real layer, use the lifted algebra/order API. Avoid reopening representatives unless proving well-definedness or a construction theorem.
6. For `LIM`, root, reciprocal, or power statements, check the theorem's preconditions before simplification. A fallback value outside the valid domain is an implementation artifact.
7. For supremum/root existence, separate the order-theoretic existence step from algebraic identification.
8. When interoperability matters, cross through the epilogue equivalence and continue in `ℝ`; do not mix both real types in the same algebraic calculation without explicit maps.

## Failure Recovery

- **Sequence evaluates to 0 unexpectedly** → prove the index is at/after `n₀` and use the appropriate evaluation lemma.
- **Product of Cauchy sequences stalls** → derive bounds for both sequences, then split the product difference using those bounds.
- **Quotient arithmetic cannot rewrite** → locate the well-defined lifted operation theorem; do not compare raw representatives.
- **Root/power statement lacks a sign hypothesis** → inspect the totalized definition; add the intended nonnegativity and exponent conditions.
- **Goal contains both `Chapter5.Real` and `ℝ`** → choose one side of the equivalence for the whole local argument.

## Source Map

`Section_5_1` Cauchy sequences; `5_2` Equivalent Cauchy sequences; `5_3` The construction of the real numbers; `5_4` Ordering the reals; `5_5` The least upper bound property; `5_6` Real exponentiation, part I; `5_epilogue` Equivalence of reals / Mathlib bridge.

## Key Takeaways

1. Index bounds and Cauchy hypotheses are semantic guards, not bookkeeping.
2. Quotient well-definedness should be established once and then hidden behind the API.
3. Boundedness is the reusable engine behind Cauchy arithmetic.
4. Completeness is assembled from the custom order theory before the Mathlib bridge.
5. Cross to `ℝ` only at the intended migration point.

## Connects To

- **Chapter 4** supplies the quotient-construction pattern and rational arithmetic.
- **Chapter 6** turns from constructing reals to studying real sequences and bridges epsilon limits to Mathlib filters.
