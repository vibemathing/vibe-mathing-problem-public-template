# Chapter 12: Differential Calculus

## Core Idea
Formalize derivatives through evidence-bearing predicates first. In one dimension use `HasDerivAt`; in normed spaces use Fréchet derivatives `HasFDerivAt` whose derivative is a continuous linear map. Asymptotic little-o supplies the definition, and strict differentiability is the form needed for inverse/implicit-function machinery.

## Frameworks Introduced

- **Derivative evidence before derivative value**
  - When to use: proving or using a derivative formula.
  - How: prove/obtain `HasDerivAt f f' x` or `DifferentiableAt`; derive `deriv f x = f'` via the evidence. In normed spaces prove `HasFDerivAt f L x` and derive `fderiv` equality.
  - Failure mode: `deriv`/`fderiv` are totalized and return zero where differentiability fails, so equations involving them can be true for unintended reasons.

- **One-dimensional theorem route**
  - Local derivative formula: `HasDerivAt` and standard derivative lemmas.
  - Global interval theorem: `ContinuousOn` on `Icc`, `DifferentiableOn` on `Ioo`, then Rolle/mean-value theorems.
  - Automatic simple derivatives: `simp` can combine registered derivative rules.

- **Normed-space structure route**
  - When to use: multivariable/infinite-dimensional calculus.
  - How: require `NormedAddCommGroup` and `NormedSpace` over a `NontriviallyNormedField`; add `[CompleteSpace]` when Banach-space theorems need completeness. Finite-dimensional spaces over complete normed fields inherit completeness.

- **Continuous-linear-map derivative model**
  - When to use: Fréchet derivatives.
  - How: derivative value lives in `E →L[𝕜] F`. Use its function coercion, linearity laws, continuity, and operator norm bounds. Linear isomorphisms are `E ≃L[𝕜] F`.

- **Asymptotic comparison route**
  - When to use: derivative definitions and error estimates.
  - How: use `f =O[l] g` for bounded-ratio behavior and `f =o[l] g` for error negligible relative to `g` along filter `l`. Fréchet differentiability at `x₀` states the first-order remainder is little-o of `x-x₀` along `𝓝 x₀`.

- **Strict derivative / local inverse route**
  - When to use: inverse-function or implicit-function settings.
  - How: obtain `HasStrictFDerivAt f f' a` with derivative a continuous linear equivalence; invoke the local inverse construction and its eventual left/right inverse plus derivative theorem. Over `ℝ`/`ℂ`, sufficient `ContDiffAt` regularity yields strict differentiability.

## Key Concepts

- **`HasDerivAt f a x`**: `f` has one-dimensional derivative `a` at `x`.
- **`DifferentiableAt`**: derivative exists without naming it.
- **`deriv f x`**: totalized derivative value.
- **Normed additive group**: additive group with norm inducing metric/topology.
- **Normed space**: module whose scalar multiplication respects norms.
- **Banach space**: complete normed vector space.
- **Nontrivially normed field**: normed field with a genuinely nontrivial norm scale.
- **`ContinuousLinearMap` / `→L`**: bundled continuous linear map, the derivative type in Fréchet calculus.
- **Operator norm**: norm controlling `‖f x‖ ≤ ‖f‖ ‖x‖`.
- **Big-O / little-o**: asymptotic comparison along a filter.
- **`HasFDerivAt`**: Fréchet derivative predicate.
- **`iteratedFDeriv` / `ContDiff`**: higher derivatives and smoothness.
- **`HasStrictFDerivAt`**: stronger local linear approximation stable enough for inverse theorems.
- **Within/filter derivative variants**: derivatives restricted to sets/directions/filters.

## Mental Models

- A derivative is a linear approximation plus a remainder estimate; in higher dimensions the linear approximation must be a continuous linear map.
- `fderiv` is a convenience projection from evidence, not a substitute for differentiability hypotheses.
- Asymptotic notation is filter-parametric, so it inherits the topological routing from Chapter 11.
- Completeness enters nonlinear functional analysis through Baire and inverse-function arguments; make it an explicit typeclass checkpoint.

## Anti-patterns

- **Starting from `deriv f x` without proving differentiability**: risks default-zero reasoning.
- **Treating a Fréchet derivative as a bare function**: loses continuity/linearity APIs and makes composition theorems harder to apply.
- **Forgetting the base field in `DifferentiableAt`/`fderiv`**: real versus complex differentiability can differ.
- **Using pointwise derivative theorems for a restricted domain**: switch to `HasFDerivWithinAt` or `HasFDerivAtFilter`.
- **Applying Banach-space theorems without completeness**: check `[CompleteSpace E]` explicitly.

## Code Examples

```lean
open Real

example : HasDerivAt sin 1 0 := by
  simpa using hasDerivAt_sin 0
```

- **What it demonstrates**: prove a derivative by reusing an evidence-bearing library theorem.

```lean
variable {𝕜 E F : Type*} [NontriviallyNormedField 𝕜]
  [NormedAddCommGroup E] [NormedSpace 𝕜 E]
  [NormedAddCommGroup F] [NormedSpace 𝕜 F]

example (f : E → F) (f' : E →L[𝕜] F) (x₀ : E) :
    HasFDerivAt f f' x₀ ↔
      (fun x => f x - f x₀ - f' (x - x₀)) =o[𝓝 x₀] (fun x => x - x₀) :=
  hasFDerivAt_iff_isLittleO
```

- **What it demonstrates**: Fréchet differentiability is a first-order remainder little-o statement.

```lean
example (f : E →L[𝕜] F) (x : E) : ‖f x‖ ≤ ‖f‖ * ‖x‖ :=
  f.le_opNorm x
```

- **What it demonstrates**: bundled continuous linear maps carry analytic control through the operator norm.

## Reference Table

| Task | Preferred API |
|---|---|
| derivative at real point | `HasDerivAt` |
| existence only | `DifferentiableAt ℝ/ℂ/...` |
| read derivative value | derive from `HasDerivAt` via `.deriv` |
| multivariable derivative | `HasFDerivAt` + `E →L[𝕜] F` |
| restricted derivative | `HasFDerivWithinAt` / `HasFDerivAtFilter` |
| asymptotic error | `=O[l]`, `=o[l]`, `IsBigOWith` |
| higher smoothness | `ContDiff`, `iteratedFDeriv` |
| local inverse theorem | `HasStrictFDerivAt` + continuous linear equivalence |
| completeness-dependent functional analysis | `[CompleteSpace E]` |

## Worked Example

The Uniform Boundedness Principle starts with a family `g : ι → E →L[𝕜] F` that is pointwise bounded on a Banach space `E`. Define closed sets `e n = ⋂ i, {x | ‖g i x‖ ≤ n}`. Pointwise boundedness says their union is all of `E`; Baire's theorem gives one `e m` with nonempty interior. A ball contained in that interior bounds every `g i` on a shell. Scale the shell using an element of the normed field with norm greater than one, then apply the operator-norm bound theorem to obtain a uniform bound on `‖g i‖`. The route depends on topology/completeness, continuous-linear-map norms, and scaling; attempting direct pointwise estimates misses the Baire step.

For a local inverse, first prove strict Fréchet differentiability with derivative `f' : E ≃L[𝕜] F`. The library constructs a local inverse and gives eventual left/right inverse properties in neighborhood filters, plus a strict derivative for the inverse equal to `f'.symm`. The theorem's output is local/eventual by design; do not strengthen it to a global inverse without extra hypotheses.

## Key Takeaways

1. Prove derivative evidence before using totalized derivative values.
2. Fréchet derivatives are continuous linear maps, not scalars or bare functions.
3. Little-o along neighborhood filters is the core higher-dimensional derivative condition.
4. Completeness and finite-dimensionality are explicit side conditions for major analytic theorems.
5. Use Within/AtFilter variants when the domain of differentiation is restricted.

## Connects To

- **Ch 10**: continuous linear maps extend the bundled linear-map interface.
- **Ch 11**: norms induce topology; little-o and local inverse statements are filter-based.
- **Ch 13**: the fundamental theorem of calculus connects derivative evidence to interval integrals.
