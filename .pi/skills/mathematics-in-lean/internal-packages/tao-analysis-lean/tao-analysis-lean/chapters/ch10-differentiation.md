# Chapter 10: Differentiation and Mean-Value Methods

## Core Idea

Chapter 10 is largely a Mathlib-API chapter. It uses `HasDerivWithinAt`, `derivWithin`, and `DifferentiableWithinAt`, then develops local extrema, Rolle's theorem, the mean value theorem, monotonicity tests, an inverse-function theorem, and L'Hôpital-style filter results. The central caution is that Mathlib's within-derivative conventions are total and can differ from the textbook at non-limit points.

## Frameworks Introduced

- **Derivative relation before derivative value**: prefer `HasDerivWithinAt f f' X x` when the derivative value is known or being proved. It carries the strongest usable local information. Use `derivWithin` only when a chosen derivative value is required.
- **Within-set semantics**: differentiation takes place relative to a set. Endpoint behavior and isolated points depend on the domain filter. Mathlib can regard differentiability at points that are not limit points differently from the prose convention.
- **Totalized derivative selection**: `derivWithin` may choose a derivative in non-unique situations and returns `0` when no derivative exists. Never infer differentiability from the bare value of `derivWithin`.
- **Local linearization**: Newton approximation/first-order error is the bridge from derivative definitions to continuity and calculus rules.
- **Extremum → stationary → Rolle → MVT**: many global derivative applications share one chain: compact/interval extrema give a stationary point; Rolle yields a zero derivative; MVT converts a function increment into a derivative value.
- **Derivative sign → monotonicity**: positive/negative derivative hypotheses feed MVT to prove strict monotonicity/antitonicity.
- **Filter-native quotient limits**: L'Hôpital statements are naturally `Filter.Tendsto` results and should stay in filter form.

## Key Concepts

- `HasDerivWithinAt`, `DifferentiableWithinAt`, `derivWithin`;
- derivative uniqueness under the correct limit-point assumption;
- sum/product/quotient/chain rules;
- local maxima/minima and stationary points;
- Rolle and mean-value theorems;
- Lipschitz estimates and uniform continuity;
- monotonicity from derivative sign;
- inverse derivative theorem;
- L'Hôpital under filters.

## Operational Procedure

1. State the domain set and point. Check whether the theorem requires the point to be a limit point/interior point or only uses Mathlib's within convention.
2. If proving a specific derivative, target `HasDerivWithinAt` and compose rule lemmas. Convert to `DifferentiableWithinAt` or `derivWithin` at the end if required.
3. For uniqueness, supply the source's limit-point/adherent hypothesis; without it Mathlib's within derivatives can be non-unique.
4. For extrema, establish the local max/min hypothesis on the correct set, then apply the stationary-derivative theorem.
5. For MVT, verify continuity on the closed interval, differentiability on the interior, and endpoint ordering. Do not hide interval-side conditions in automation.
6. For monotonicity, turn the derivative sign into a difference sign via MVT; this is usually clearer than expanding derivative definitions.
7. For inverse functions, prove local injectivity/monotonicity and nonzero derivative conditions before applying the inverse derivative formula.
8. For L'Hôpital, keep numerator/denominator limits and derivative quotient in `Filter.Tendsto` form; verify denominator/derivative nonvanishing and approach filter assumptions.

## Failure Recovery

- **`derivWithin` equals 0 unexpectedly** → check whether differentiability was established or the totalized fallback branch is active.
- **Two derivatives cannot be shown equal** → supply the limit-point condition needed for uniqueness.
- **global derivative theorem fails at an endpoint** → use a within-set theorem with the correct interval domain.
- **MVT theorem does not match** → audit closed/open interval placement and endpoint inequality.
- **inverse theorem has a division-by-zero side goal** → prove the derivative is nonzero before simplification.
- **L'Hôpital epsilon proof becomes unwieldy** → stay in filter form and use the source's `Filter.Tendsto` statements.

## Reference Table

| Goal | Preferred API |
|---|---|
| prove derivative `f'` | `HasDerivWithinAt` |
| assert existence | `DifferentiableWithinAt` |
| retrieve chosen value | `derivWithin` after differentiability/uniqueness |
| local extremum | `IsLocalMaxOn` / `IsLocalMinOn` |
| slope bound / monotonicity | MVT family |
| quotient limit | `Filter.Tendsto` L'Hôpital family |

## Source Map

`Section_10_1` Basic definitions and calculus rules; `10_2` Local maxima, local minima, and derivatives (Rolle/MVT/Lipschitz); `10_3` Monotone functions and derivatives; `10_4` The inverse function theorem; `10_5` L'Hôpital's rule.

## Key Takeaways

1. Use derivative relations as the primary proof object; derivative values are derived data.
2. Within-set and limit-point conventions are mathematically significant.
3. A selected derivative value alone does not certify differentiability.
4. MVT is the main engine connecting local derivative bounds to global behavior.
5. Filter form is the natural representation for L'Hôpital and composition of limiting statements.

## Connects To

- **Chapter 9** supplies continuity, compactness, intervals, and filter limits.
- **Chapter 11** uses antiderivatives and derivative rules in the fundamental theorem of calculus and integration by parts.
