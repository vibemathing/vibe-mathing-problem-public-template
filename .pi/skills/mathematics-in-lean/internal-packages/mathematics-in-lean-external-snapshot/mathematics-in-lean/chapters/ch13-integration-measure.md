# Chapter 13: Integration and Measure Theory

## Core Idea
Choose the integration layer first: interval integrals for one-dimensional finite intervals, measure-theoretic Bochner integrals for general spaces. Most useful theorems require explicit measurability and integrability evidence; almost-everywhere facts are filter statements through `ae μ`.

## Frameworks Introduced

- **Interval-integral route**
  - When to use: real functions on a finite interval `a..b`.
  - How: use `intervalIntegral`; exploit standard elementary integrals; for the fundamental theorem, pair continuity/interval integrability with derivative evidence such as `HasDerivAt`.
  - Side conditions: singular integrands such as `1/x` require the interval to avoid the singularity.

- **Measurable-space / measure layering**
  - When to use: general integration/probability/measure arguments.
  - How: start with `[MeasurableSpace α]`; prove sets/functions measurable using closure under complements and countable unions/intersections; introduce `μ : Measure α`; use measure monotonicity/subadditivity/countable-additivity lemmas with measurability/disjointness assumptions where required.

- **Almost-everywhere route**
  - When to use: a property may fail on a null set.
  - How: use `∀ᵐ x ∂μ, P x`, definitionally `∀ᶠ x in ae μ, P x`; combine/filter such facts with the same `Eventually` machinery from topology.

- **Bochner-integral evidence route**
  - When to use: vector-valued integrals into a Banach space.
  - How: keep `Integrable f μ` and (AE-)strong measurability hypotheses explicit. Use linearity theorems under integrability. Remember the integral is totalized to zero for nonintegrable functions, so theorem premises carry the semantics.

- **Convergence theorem route**
  - Dominated convergence: provide an integrable bound, almost-everywhere domination, strong measurability of approximants, and a.e. pointwise `Tendsto`.
  - Fubini: work on a product measure and establish integrability; common theorem versions require sigma-finite measures.
  - Change of variables: prove measurability of the domain, derivative-within hypotheses, injectivity on the domain, and use determinant/Jacobian scaling.

## Key Concepts

- **`intervalIntegral`**: oriented integral over finite real intervals.
- **Measurable space**: sigma-algebra structure describing measurable sets.
- **`MeasurableSet`**: predicate for membership in that sigma-algebra.
- **`Encodable`**: typeclass often used to express countable indexed unions/intersections.
- **Measure**: countably additive set function valued in extended nonnegative reals, extended in Mathlib to all sets by outer-measure-style definition.
- **`ℝ≥0∞` / ENNReal**: extended nonnegative reals including `⊤`.
- **Almost everywhere**: property outside a measure-zero exceptional set.
- **`Integrable`**: core premise for nontrivial integral algebra.
- **Bochner integral**: integral of Banach-space-valued functions.
- **`SigmaFinite`**: measure-theoretic finiteness condition used by common product/Fubini theorems.
- **Convolution**: integral operation combining two functions; generalized to continuous bilinear maps.
- **`BorelSpace` / Haar measure**: topological-measure compatibility assumptions used by change-of-variables theorems.

## Mental Models

- Measurability, integrability, and almost-everywhere conditions are first-class proof data; collect them before attempting an integral identity.
- Almost-everywhere reasoning is filter reasoning, so `.and`, `.mono`, and `filter_upwards` patterns transfer from Chapter 11.
- Totalized integrals and `ENNReal.toReal` make notation globally defined; check hypotheses before interpreting values analytically.
- Major convergence/change-of-variable theorems are routing endpoints: most of the proof work is assembling their side conditions in the expected form.

## Anti-patterns

- **Using linearity of the integral without integrability hypotheses**: standard theorem variants generally require them.
- **Interpreting a zero integral as meaningful before checking integrability**: the definition can return zero outside the integrable domain.
- **Dropping measurability in countable-additivity or change-of-variable steps**: some inequalities need less structure, equalities usually need more.
- **Confusing almost-everywhere equality with pointwise equality**: use the AE filter and theorems designed to respect it.
- **Applying Fubini without product-measure and sigma-finiteness/integrability checks**: theorem shape will not match.
- **Forgetting completeness of vector target**: Bochner integration targets Banach spaces in the presented API.

## Code Examples

```lean
open MeasureTheory intervalIntegral

example (a b : ℝ) : (∫ x in a..b, x) = (b^2 - a^2) / 2 :=
  integral_id
```

- **What it demonstrates**: elementary interval integration through the specialized API.

```lean
variable {α E : Type*} [MeasurableSpace α]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
  {μ : Measure α}

example {f g : α → E} (hf : Integrable f μ) (hg : Integrable g μ) :
    ∫ a, f a + g a ∂μ = (∫ a, f a ∂μ) + ∫ a, g a ∂μ :=
  integral_add hf hg
```

- **What it demonstrates**: integral linearity is routed through explicit integrability evidence.

```lean
example {P : α → Prop} : (∀ᵐ x ∂μ, P x) ↔ ∀ᶠ x in ae μ, P x :=
  Iff.rfl
```

- **What it demonstrates**: almost-everywhere logic is ordinary filter `Eventually` under specialized notation.

## Reference Table

| Task | Route / prerequisites |
|---|---|
| finite real interval | `intervalIntegral` |
| FTC derivative of integral | continuity + interval integrability + derivative theorem |
| measure of union inequality | `measure_iUnion_le` |
| measure of disjoint countable union equality | measurable sets + pairwise disjointness |
| almost-everywhere fact | `∀ᵐ x ∂μ, ...` / `ae μ` |
| integral addition | `Integrable` for each summand |
| dominated convergence | measurable approximants + integrable bound + a.e. domination + a.e. limit |
| Fubini | product measure + integrability + sigma-finiteness as theorem requires |
| change of variables | measurable domain + derivative-within + injectivity + finite-dimensional Jacobian determinant |
| vector-valued integral | normed space + completeness |

## Worked Example

For dominated convergence, organize the proof as an interface checklist before any manipulation of integrals: (1) each approximating function is a.e. strongly measurable; (2) one scalar bound is integrable; (3) every approximant is dominated by that bound almost everywhere; (4) the sequence converges pointwise almost everywhere, expressed with `Tendsto ... atTop (𝓝 ...)`. Once these are available, the theorem returns convergence of the sequence of integrals. This architecture prevents a common failure mode where pointwise limit algebra is proved first but the measurable/integrable envelope needed by the library is never assembled.

For change of variables on a set `s` in a finite-dimensional real normed space, prove `s` measurable, prove a Fréchet derivative within `s` at every point, and prove `f` injective on `s`. The library theorem changes integration over `f '' s` to integration over `s` with `|(f' x).det|` as the Jacobian factor. The derivative is a continuous linear map and determinant is the finite-dimensional bridge from differential calculus to measure scaling.

## Key Takeaways

1. Select interval or measure-theoretic integration before searching for theorems.
2. Treat measurability and integrability as required proof inputs, not background assumptions.
3. Almost-everywhere reasoning reuses filter `Eventually` methods.
4. Totalized integral definitions demand semantic side-condition checks.
5. Dominated convergence, Fubini, and change of variables are best approached by assembling their hypotheses as a checklist.

## Connects To

- **Ch 11**: `ae μ` is a filter and convergence hypotheses use `Tendsto`.
- **Ch 12**: FTC and change of variables depend on derivative evidence and continuous linear maps.
- **Ch 10**: finite-dimensional determinant appears in the Jacobian factor.
