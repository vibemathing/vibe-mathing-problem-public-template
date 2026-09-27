# 09 — Continuous Linear Maps and Derivatives

## Core Idea

Mathlib's derivative API treats the derivative as a **continuous linear map** and expresses “error is little-o of displacement” along a **filter**. Route derivative problems by domain restriction and abstraction level instead of forcing one-dimensional calculus notation everywhere.

## Continuous linear maps

For normed spaces `E` and `F`, a real continuous linear map is commonly written:

```lean
E →L[ℝ] F
```

It packages both linearity and continuity, allowing direct use of the corresponding API.

Typical facts include:

- continuity (`f.cont` in the source version);
- additivity (`f.map_add`);
- scalar compatibility (`f.map_smul`);
- norm bounds from the operator norm.

Verify exact method names against the installed Mathlib if they differ.

## Boundedness and continuity

For linear maps on normed spaces, boundedness and continuity are equivalent under the standard hypotheses. In Mathlib, use the library bridge rather than re-proving the analytic equivalence whenever possible.

### Operator norm

The operator norm is the least/suitable bound controlling:

```text
‖f x‖ ≤ ‖f‖ * ‖x‖
```

The course points to `le_opNorm`-style lemmas on continuous linear maps.

Operational use:

1. identify that the function is packaged as a continuous linear map;
2. apply the norm-bound theorem;
3. reduce the remaining goal to scalar/norm arithmetic;
4. let `linarith`, `ring`, or appropriate norm lemmas handle the remaining numeric layer.

If you only have a plain `LinearMap`, first prove/obtain boundedness/continuity and package it into the continuous-linear-map type expected by downstream calculus APIs.

## Fréchet derivative

For `f : E → F`, a Fréchet derivative at `x` is a continuous linear map `f' : E →L[ℝ] F` whose first-order error is little-o of the displacement.

Mathlib's general predicate uses a filter:

```text
HasFDerivAtFilter f f' x L
```

Conceptually:

```text
f x' - f x - f' (x' - x) = o(x' - x)  along L
```

The two key components are therefore:

- **continuous linear map** = candidate derivative;
- **filter** = how `x'` approaches `x`.

## At vs within a set

When differentiating only along a subset `s`, the approach filter is restricted to `s` near `x`.

Choose the predicate that matches the task:

- `HasFDerivAtFilter` — arbitrary approach filter;
- `HasFDerivWithinAt` — approach within `s`;
- `HasFDerivAt` — unrestricted neighborhood at `x`.

Current signatures should be checked with `#check`; the naming hierarchy is the stable part.

### Routing rule

If the original theorem says “for x in s,” “on a domain,” or concerns a boundary point where only one-sided/domain-restricted approach is valid, start with the `Within` API. If `f` is defined/considered on a full neighborhood, use the unrestricted `At` API.

## Differentiability vs a chosen derivative

Predicates such as:

- `DifferentiableWithinAt`;
- `DifferentiableAt`;
- `DifferentiableOn`;
- `Differentiable`;

assert existence of a derivative at the corresponding scope.

Functions such as `fderivWithin` / `fderiv` return a continuous linear map value. The source notes an important semantic detail: these definitions have fallback behavior (commonly zero) when a suitable derivative is unavailable or in certain degenerate within-set situations.

**Do not infer differentiability merely because `fderiv f x` is a well-typed term.** Carry/prove a `HasFDeriv...` or `Differentiable...` hypothesis when correctness depends on existence.

## Ordinary derivatives

For one-dimensional source spaces (scalar → target), Mathlib offers specialized derivative predicates/functions such as:

- `HasDerivAtFilter`;
- `HasDerivWithinAt`;
- `HasDerivAt`;
- `derivWithin`;
- `deriv`.

Use them when the problem is genuinely one-dimensional and the specialized API is more convenient. For maps between general normed spaces, stay with Fréchet derivatives.

## Gradients

For scalar-valued functions on inner-product spaces, the Riesz/inner-product structure allows a gradient representation of the derivative. The source points to the family:

- `HasGradientAtFilter`;
- `HasGradientWithinAt`;
- `HasGradientAt`;
- `gradientWithin`;
- `gradient`.

Again, separate an existence predicate from a total function that returns some value even outside its intended differentiability conditions.

## Derivative problem workflow

### A. Prove a known derivative formula

1. identify `At` vs `Within` scope;
2. decide scalar derivative vs Fréchet derivative;
3. search for a `HasFDeriv...` / `HasDeriv...` theorem for each primitive function;
4. compose using calculus rules (sum/product/chain/etc.);
5. discharge continuity/typeclass side conditions;
6. convert to a `Differentiable...` or derivative-value statement only at the end if needed.

Why prefer `Has...`? It carries the candidate derivative explicitly and composes more predictably than manipulating `fderiv` values directly.

### B. Use differentiability to get regularity

1. keep the differentiability predicate in context;
2. extract/use established theorems giving continuity or derivative properties;
3. avoid unfolding the little-o definition unless proving foundational calculus theory.

### C. Bound a derivative/linearized error

Use continuous-linear-map norm bounds and norm inequalities. Keep the derivative packaged as `→L` long enough to use its operator-norm API.

## Worked Example — diagnose a misleading `fderiv` term

Suppose `fderiv ℝ f x` is well typed and the goal needs a derivative formula. Do not treat the existence of that term as differentiability evidence. First obtain a `HasFDerivAt`/`DifferentiableAt` fact from primitive derivative rules or hypotheses; then identify the candidate continuous linear map and only afterward rewrite or extract the `fderiv` value. If the point is domain-restricted, start with the `Within` form instead.

## Failure recovery

- **The theorem is stated for `Within`, target is `At`:** search conversion lemmas and check whether the set is a neighborhood/interior condition; do not erase the domain restriction casually.
- **`fderiv` expression exists but proof needs differentiability:** introduce/derive the proper `HasFDeriv...` or `Differentiable...` fact.
- **Chain rule search fails:** inspect whether the inner/outer derivative theorem is scalar or Fréchet and whether scalar fields match.
- **Typeclass errors:** check normed-space/module/scalar assumptions and continuous-linear-map codomain.
- **Goal explodes into little-o/filter internals:** back out and search the `HasFDeriv...` API for a composition theorem.
- **Operator bound unavailable:** verify the map is truly a `ContinuousLinearMap`, not only a `LinearMap`.

## Validation checklist

Before accepting a derivative proof:

- domain restriction (`At`/`Within`) matches the mathematical statement;
- candidate derivative has the correct continuous-linear-map type;
- differentiability/existence is established where needed;
- scalar field and normed-space instances align;
- fallback values of `fderiv`/`deriv` are not being mistaken for existence;
- current Mathlib names/signatures are verified.

## Key Takeaways

Use `Has...` predicates as the compositional proof layer, continuous linear maps as derivative values, and `fderiv`/`deriv`/gradient functions as convenient extracted values only with the proper existence conditions in view.

## Connects To

- `Tendsto`, filters, metric approach → [ch07](ch07-filters-limits-metric.md)
- Normed/inner-product structure and continuity → [ch08](ch08-normed-topology-continuity.md)
- Search strategy for current API names → [ch04](ch04-mathlib-search-sets-blueprints.md)
