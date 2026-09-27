# Chapter 8: Countability, Infinite Sums, Choice, and Ordered Sets

## Core Idea

Chapter 8 replaces the deprecated Chapter 3 cardinal framework with Mathlib-native type/cardinal notions, develops summation over infinite sets, formalizes choice and countable choice, and builds order-theoretic tools through well-foundedness and Zorn-style principles. The main operational boundary is §8.2: after connecting the chapter's custom generalized sum to Mathlib, prefer `Summable` and `tsum` for subsequent work.

## Frameworks Introduced

- **Cardinality by equivalence**: `EqualCard` is linked to `Equiv`/`Cardinal.mk`; countably infinite behavior relates to `Denumerable`, while Mathlib's `Countable` means “at most countable.” Translate terminology before theorem search.
- **Enumeration method**: prove countability by constructing an injection/surjection/equivalence or an explicit enumeration. Minimum/find lemmas on `ℕ` support canonical enumerations.
- **Generalized sum → `tsum` bridge**: the section defines absolute convergence and generalized sums over sets, proves compatibility with `Summable`/`tsum`, then deprecates its custom notation. A generalized sum may carry a junk value when convergence fails, so summability is a semantic precondition.
- **Cantor/Schröder–Bernstein cardinal arguments**: uncountability is established by diagonal/power-set reasoning and cardinal injections in both directions.
- **Choice through dependent products**: infinite Cartesian products are best represented by dependent functions `∀ i, X i`. The project uses Mathlib's `Classical.choice`; the fine foundational distinction between theorem variants is blurred because classical choice already underlies many imported results.
- **Order-theoretic escalation**: finite maxima/minima → well-founded/well-ordered structures → Zorn's lemma → well-ordering/choice-style principles.

## Key Concepts

- equal cardinality, countably infinite, at most countable;
- explicit bijections for `ℤ` and `ℚ`;
- `AbsConvergent` / generalized `Sum'` and their limits;
- `Summable`, `tsum`, subtype sums;
- Cantor power-set theorem, uncountability of reals;
- Schröder–Bernstein;
- dependent products and classical/countable choice;
- partial/linear/well-founded orders, maximal elements, Zorn.

## Operational Procedure

1. Translate the prose cardinality claim into the Mathlib notion actually used by the section: `Equiv`, `Countable`, `Denumerable`, `Cardinal`, or a local wrapper.
2. For countability, choose a concrete map and prove injectivity/surjectivity; avoid cardinal arithmetic if an explicit enumeration is simpler.
3. For arbitrary-set sums, first prove `Summable` (or the local absolute-convergence premise), then use the bridge to `tsum`. Do not read meaning into `Sum'` on a nonsummable function.
4. For sums on subsets, consider passing to a subtype; compare with `Summable.subtype` and the project's bridge lemmas.
5. For uncountability, identify whether diagonalization, power-set strictness, or Schröder–Bernstein is the shortest dependency chain.
6. For choice problems, encode the selected family as a dependent function. Use `Classical.choice` only after confirming the project accepts classical reasoning here.
7. For Zorn/order problems, establish the exact chain-upper-bound hypothesis required by the Mathlib theorem before invoking maximal-element existence.

## Failure Modes

- **`Countable` theorem proves weaker/stronger statement than expected** → remember Mathlib's naming corresponds to “at most countable.”
- **Infinite sum rewrites to an arbitrary value** → summability/absolute convergence is missing.
- **Set-indexed sum type is awkward** → move to the subtype or use a `tsum` over the ambient type with an indicator.
- **Choice theorem appears circular** → the formalization already imports classical infrastructure; state this limitation rather than claiming a constructive distinction.
- **Schröder–Bernstein sequence has shifted indices** → source intentionally shifts a sequence to fit Mathlib set types; follow that implementation rather than the prose indices.

## Reference Table

| Goal | Tool family |
|---|---|
| countably infinite | `Equiv`/`Denumerable` |
| at most countable | `Countable` |
| general convergent indexed sum | `Summable` + `tsum` |
| cardinal inequality both ways | Schröder–Bernstein |
| select one value from each nonempty type | dependent function + classical choice |
| maximal element from chain bounds | Zorn/order API |

## Source Map

`Section_8_1` countability; `8_2` infinite-set summation and Mathlib bridge; `8_3` uncountable sets; `8_4` choice; `8_5` ordered sets and Zorn-style results.

## Key Takeaways

1. Translate vocabulary into Mathlib's cardinality vocabulary before searching.
2. After §8.2, prefer `Summable`/`tsum` over the custom generalized sum.
3. Convergence is mandatory before generalized sums have mathematical meaning.
4. Choice arguments are classical in this project environment.
5. Order-theoretic existence proofs require carefully stated chain/well-founded hypotheses.

## Connects To

- **Chapter 3** provides the earlier custom cardinal framework that Chapter 8 intentionally leaves behind.
- **Chapter 11 / Measure Theory** rely heavily on standard Mathlib sets, countability, `tsum`, and classical constructions.
