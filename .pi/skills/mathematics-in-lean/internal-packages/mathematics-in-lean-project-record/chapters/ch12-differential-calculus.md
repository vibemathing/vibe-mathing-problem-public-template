# Chapter 12: Differential Calculus

## Core Idea
Mathlib separates proof-bearing derivative predicates from total derivative functions, then generalizes one-dimensional derivatives to Fréchet derivatives valued in continuous linear maps. The surrounding infrastructure—normed spaces, filters, asymptotics, completeness—determines which calculus theorem is applicable.

## Frameworks Introduced
- **Predicate before total derivative function**
  - When to use: proving a concrete derivative or composing derivative facts.
  - How: prefer `HasDerivAt f f' x` / `HasFDerivAt f f' x` when the derivative is known; derive `DifferentiableAt` or equality with `deriv`/`fderiv` afterward.
  - Failure mode: `deriv` and `fderiv` are totalized and return a default (zero) when differentiability fails, so a syntactically valid statement may be mathematically degenerate.
- **Normed-space structure stack**
  - When to use: moving from real calculus to vector-valued calculus.
  - How: check `[NormedAddCommGroup E]`, `[NormedSpace 𝕜 E]`, and a suitable `NontriviallyNormedField 𝕜`; add `[CompleteSpace ...]` where Banach-space theorems require it.
- **Continuous linear map as derivative object**
  - When to use: Fréchet derivatives.
  - How: derivatives live in `E →L[𝕜] F`; use map/add/smul/continuity/operator-norm APIs from this bundled type rather than bare functions.
- **Little-o derivative definition**
  - When to use: reasoning at the foundational definition or matching asymptotic lemmas.
  - How: read `HasFDerivAt f f' x₀` as the error `f x - f x₀ - f'(x-x₀)` being little-o of `x-x₀` along `𝓝 x₀`.
- **Continuity/differentiability automation + exact theorem route**
  - When to use: routine derivative/continuity closure properties.
  - How: try `simp`/`continuity` for standard compositions, but know the explicit lemmas so you can recover when elaboration or automation stalls.
- **Strict derivative → local inverse**
  - When to use: inverse/implicit function theorem settings.
  - How: prove `HasStrictFDerivAt` and that the derivative is a continuous linear equivalence; use the local inverse construction and its eventual left/right inverse theorems.

## Key Concepts
- **`HasDerivAt`**: function has a specified scalar derivative at a point.
- **`DifferentiableAt`**: derivative exists, without naming it.
- **`deriv`**: total scalar derivative function with fallback value outside differentiability.
- **Normed additive group / normed space**: vector-space geometry needed for Fréchet calculus.
- **Banach space**: complete normed vector space.
- **Continuous linear map (`→L`)**: morphism object for normed spaces and derivative codomain.
- **Operator norm**: controls the size of a continuous linear map.
- **Big O / little o**: asymptotic comparison along a filter.
- **`HasFDerivAt`**: specified Fréchet derivative.
- **`ContDiff`**: continuous differentiability up to an order, including smooth/analytic variants.
- **`HasStrictFDerivAt`**: stronger differentiability notion used for inverse-function machinery.

## Mental Models
- Treat `Has*Deriv*` as the **proof-carrying interface**, and `deriv`/`fderiv` as convenient projections with a fallback convention.
- A Fréchet derivative is a **linear approximation object**, not a scalar formula.
- Little-o isolates the **remainder term**; filters specify the direction/location of the limit.
- Calculus theorems are layered on the same hierarchy as topology and linear algebra; missing instances often reveal which layer is absent.

## Anti-patterns
- **Using `deriv` equality as evidence of differentiability**: the fallback zero value prevents that inference in general.
- **Forgetting to state the scalar field** when differentiability can mean real or complex differentiability.
- **Treating a continuous linear map as only a function**: retain the bundled object to use norms, composition, and linear structure.
- **Reproving continuity of standard compositions manually** before trying the library's continuity/differentiability closure lemmas.
- **Ignoring completeness/finite-dimensional assumptions** required by Banach-space results.

## Code Examples
```lean
example : HasDerivAt Real.sin 1 0 := by
  simpa using Real.hasDerivAt_sin 0
```
```lean
example {𝕜 E F : Type*}
    [NontriviallyNormedField 𝕜]
    [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    (f : E → F) (f' : E →L[𝕜] F) (x : E)
    (h : HasFDerivAt f f' x) : fderiv 𝕜 f x = f' :=
  h.fderiv
```
- **What they demonstrate**: derivative facts are strongest when carried by `Has...` predicates, from which total derivative values follow.

## Reference Tables
| Need | Primary object |
|---|---|
| scalar derivative at point | `HasDerivAt` |
| existence only | `DifferentiableAt` |
| scalar derivative value | `deriv` (with differentiability awareness) |
| vector derivative | `HasFDerivAt` / `fderiv` |
| derivative map type | `E →L[𝕜] F` |
| asymptotic remainder | `IsLittleO` (`=o[...]`) |
| smoothness | `ContDiff` |
| inverse theorem hypotheses | `HasStrictFDerivAt` + linear equivalence |

## Section-by-Section Operational Map

**12.1 Elementary Differential Calculus.** The chapter distinguishes “has derivative `a` at `x`” from “is differentiable at `x`” and from the total function `deriv f x`. This distinction matters when using algebraic derivative rules, which normally need differentiability hypotheses, versus special extrema/Rolle theorems that can exploit the default-zero convention. `simp` knows many elementary derivative formulas. Interval versions of the mean value theorem require continuity on the closed interval and differentiability on the open interval.

**12.2 Differential Calculus in Normed Spaces.** The section moves from normed-space infrastructure through continuous linear maps and asymptotics to Fréchet and strict differentiability. Use this layer when scalar derivatives no longer capture the domain/codomain or when inverse-function-style results require stronger derivative notions.

**12.2.1 Normed spaces.** Normed additive groups supply nonnegativity, zero characterization, and triangle inequality; a norm induces metric/topological structure. Adding `[NormedSpace 𝕜 E]` controls scalar multiplication. Finite-dimensional spaces over complete nontrivially normed fields are complete, giving many Banach-space hypotheses automatically.

**12.2.2 Continuous linear maps.** `E →L[𝕜] F` bundles linearity and continuity and carries an operator norm. The uniform boundedness principle example is a synthesis exercise: define closed sets of points with uniform pointwise bounds, show they cover the Banach space, apply Baire to obtain a ball, then convert that local shell bound into a global operator-norm bound.

**12.2.3 Asymptotics.** Big-O with a constant is an eventual norm inequality; big-O existentially chooses a constant; little-o requires every positive constant. These are filter-indexed relations, so the same notion handles limits at points, infinity, or restricted domains.

**12.2.4 Differentiability.** Fréchet differentiability says the nonlinear remainder after subtracting a continuous linear approximation is little-o of the input displacement. Iterated derivatives take values in multilinear maps; `ContDiff` packages continuous differentiability to a chosen order. Strict differentiability supports local inverse/implicit function theorems; over real/complex-like fields sufficiently smooth maps give strict derivatives automatically.

## Failure Recovery Notes

- If a derivative theorem expects a continuous linear map but you have a linear map, find/construct continuity or use the finite-dimensional result that supplies it.
- If `simp` gives `0` unexpectedly for `deriv`, check differentiability at the point before trusting the value as mathematical information.
- If a smoothness theorem asks for an order in `WithTop N∞`, inspect whether the intended statement is finite `n`, smooth `⊤`, or analytic `ω`.
- If a local inverse theorem will not apply, verify both strict differentiability and that the derivative is a continuous linear equivalence, not merely an injective linear map.

## Worked Example
For a local inverse problem, do not start by defining an inverse function. First prove that `f` is strictly Fréchet differentiable at `a` with derivative represented by a continuous linear equivalence `f' : E ≃L[𝕜] F`. The library's local-inverse construction then supplies a candidate inverse. Its API gives eventual left-inverse behavior near `a`, eventual right-inverse behavior near `f a`, and the derivative of the local inverse as `f'.symm`. The difficult analytical hypotheses stay in the derivative theorem; the inverse construction becomes an application of a general interface.

## Key Takeaways
1. Prefer `HasDerivAt`/`HasFDerivAt` when carrying derivative data through a proof.
2. Check structural assumptions: normed group, normed space, scalar field, completeness.
3. Remember total derivative functions have fallback values.
4. Treat continuous linear maps as first-class derivative objects.
5. Use asymptotic/filter formulations when the concrete epsilon form becomes cumbersome.
6. For inverse-function reasoning, target strict differentiability plus an invertible derivative and reuse the local inverse API.

## Connects To
- **Ch 10**: continuous linear maps extend the bundled linear-map framework.
- **Ch 11**: `HasFDerivAt` is built from little-o behavior along neighborhood filters.
- **Ch 13**: fundamental-theorem and change-of-variables results connect derivatives to integrals.
