# Chapter 13: Integration and Measure Theory

## Core Idea
Mathlib's integration theory sits on measurable spaces and measures, uses almost-everywhere filters for negligible exceptions, and defines highly general Banach-valued integrals. Effective proofs first discharge measurability/integrability hypotheses, then apply structural theorems such as dominated convergence, Fubini, or change of variables.

## Frameworks Introduced
- **Measurable-space layer first**
  - When to use: any measure/integration theorem.
  - How: identify the `MeasurableSpace` instance and measurable sets/functions involved. Countable closure conditions typically use an `Encodable` index.
- **Measure as total set function**
  - When to use: manipulating `μ s` without carrying measurability everywhere.
  - How: Mathlib extends a measure to arbitrary sets through outer-measure style infima; expect some inequalities to hold generally and equalities/additivity to request measurability/disjointness.
- **Almost-everywhere as filter reasoning**
  - When to use: pointwise properties may fail on a null set.
  - How: use `∀ᵐ x ∂μ, P x`, definitionally an eventual statement in `ae μ`; combine facts using the same filter algebra as topology.
- **Integrability gate**
  - When to use: algebraic identities for integrals.
  - How: prove `Integrable` (or interval integrability) before using additivity, limit interchange, Fubini, etc. Remember the integral is totalized to zero when the function is not integrable.
- **Dominated convergence pipeline**
  - When to use: exchange limit and integral for a sequence of functions.
  - How: establish almost-everywhere strong measurability, an integrable dominating function, an AE norm bound, and pointwise-AE `Tendsto`; apply the dominated-convergence theorem.
- **Product integration / Fubini**
  - When to use: integrate over a product type.
  - How: provide measurable spaces, measures, sigma-finiteness, and integrability; use the product-measure integral theorem to exchange a product integral for iterated integrals.
- **Change of variables**
  - When to use: integrate over the image of an injective differentiable map in finite-dimensional normed spaces.
  - How: prove measurable domain, within-set Fréchet derivative, injectivity on the set, and supply the Haar/Borel measure context; the Jacobian factor is the absolute determinant of the derivative.

## Key Concepts
- **`MeasurableSpace`**: sigma-algebra structure on a type.
- **`MeasurableSet`**: membership in that sigma-algebra.
- **Measure**: set function valued in extended nonnegative reals, with countable additivity on measurable disjoint families.
- **`ae μ`**: filter of sets whose complement has measure zero.
- **`AEStronglyMeasurable`**: measurability notion appropriate to Bochner integration up to null sets.
- **`Integrable f μ`**: condition required for the intended Bochner integral behavior.
- **Bochner integral**: vector-valued integral into a Banach space.
- **Interval integral**: oriented real interval integral built on the general theory.
- **Product measure**: basis for Fubini/Tonelli-style statements.
- **Sigma-finite measure**: structural assumption used by product/integration theorems.
- **Haar measure**: invariant measure structure used in general change-of-variables results.

## Mental Models
- The analysis stack is **topology → measurability → integrability → integration theorem**.
- Almost-everywhere facts are **ordinary `Eventually` facts on a special filter**.
- Totalized integrals simplify syntax but make **integrability a semantic guardrail**.
- Theorems such as dominated convergence are best approached as a **hypothesis checklist**, not by unfolding the integral.

## Anti-patterns
- **Applying integral algebra without integrability hypotheses**: totalization can make accidental zero cases look plausible.
- **Using pointwise equality where AE equality is sufficient**: it creates unnecessary obligations on null sets.
- **Opening the definition of the Bochner integral** for standard theorems: use the library interface.
- **Ignoring sigma-finiteness/product-measure requirements** in Fubini-style results.
- **Treating change of variables as scalar calculus only**: Mathlib states a much more structural finite-dimensional Fréchet result.

## Code Examples
```lean
example {α E : Type*} [MeasurableSpace α]
    [NormedAddCommGroup E] [NormedSpace R E] [CompleteSpace E]
    (μ : MeasureTheory.Measure α) {f g : α → E}
    (hf : MeasureTheory.Integrable f μ)
    (hg : MeasureTheory.Integrable g μ) :
    (∫ x, (f x + g x) ∂μ) = (∫ x, f x ∂μ) + ∫ x, g x ∂μ := by
  exact MeasureTheory.integral_add hf hg
```
- **What it demonstrates**: integral linearity is an API theorem gated by explicit integrability evidence.

## Reference Tables
| Task | Required evidence to check |
|---|---|
| measurable set closure | measurable-space + countable index where needed |
| countable additivity equality | measurability + pairwise disjointness |
| AE property | `∀ᵐ ... ∂μ` / `ae μ` filter |
| add integrals | integrability of both functions |
| dominated convergence | AE measurability, integrable bound, AE domination, AE pointwise convergence |
| Fubini | product measures, sigma-finiteness, integrability |
| change of variables | measurable set, derivative, injectivity, finite dimension, appropriate measure structure |

## Section-by-Section Operational Map

**13.1 Elementary integration.** Interval integrals on `R` are instances of the general integration framework. Mathlib knows standard elementary integrals and versions of the fundamental theorem of calculus. One direction differentiates an integral with variable endpoint; another integrates a derivative over an interval. Convolution is already defined in the general library and specializes to the familiar real formula.

**13.2 Measure theory.** `MeasurableSpace` provides the sigma-algebra; empty/universal/complement/countable unions/intersections are the main closure interface. Countable indexing is expressed by `Encodable`. Measures take values in extended nonnegative reals and are defined on all sets, with measurable-set assumptions controlling equality/additivity results. Countable subadditivity is general; countable additivity requires measurability and pairwise disjointness. Almost-everywhere notation is exactly the `Eventually` notation for the measure's `ae` filter, linking measure theory directly to Chapter 11.

**13.3 Integration.** The integral is Bochner-valued in a complete normed real vector space and totalized to zero outside integrability. Constant integrals reveal another totalization: `ENNReal.toReal ⊤ = 0`, matching the nonintegrable infinite-measure case. Dominated convergence is presented in its filter/AE form. Fubini integrates over product measures under sigma-finiteness and integrability. Convolution is generalized to continuous bilinear forms. The change-of-variables theorem integrates over an injective Fréchet-differentiable image and weights by the absolute determinant of the derivative under a Borel/Haar measure setup.

## Failure Recovery Notes

- If an AE theorem will not rewrite pointwise, convert the pointwise premise to an `Eventually.of_forall` fact or prove an AE version directly.
- If countable union equality fails, check measurability and pairwise disjointness; otherwise only an inequality may be available.
- If an integral theorem returns a surprising zero, inspect `Integrable` and whether an extended-real quantity was converted with `toReal` at infinity.
- If Fubini/change-of-variables typeclass synthesis fails, inventory sigma-finite, Borel, Haar, finite-dimensional, completeness, and measurability instances explicitly.

## Worked Example
For dominated convergence, organize the proof around the theorem's inputs rather than the integral expression. For a sequence `F n`, first produce `AEStronglyMeasurable (F n) μ` for every `n`. Choose a scalar `bound`; prove it integrable and show `‖F n a‖ ≤ bound a` almost everywhere for every `n`. Then prove that for almost every `a`, the sequence `F n a` tends to `f a`. Once these four components are present, apply the library theorem to obtain convergence of the integrals. The proof remains stable because it mirrors the semantic theorem statement instead of manipulating integral definitions.

## Key Takeaways
1. Establish measurability and integrability before integral algebra.
2. Use `ae μ` as a filter and reuse eventual-reasoning tools from topology.
3. Recognize Bochner integration as vector-valued and structurally general.
4. Treat dominated convergence/Fubini/change of variables as theorem-interface checklists.
5. Keep totalized-definition corner cases in mind when a theorem appears to need fewer hypotheses than expected.
6. Reuse Fréchet derivatives, determinants, and finite-dimensional structure from earlier chapters for change of variables.

## Connects To
- **Ch 11**: `ae μ` is an `Eventually` filter; convergence uses `Tendsto`.
- **Ch 12**: fundamental theorem and change-of-variables bridge integration with derivatives.
- **Ch 10**: determinant and finite-dimensional linear maps enter the Jacobian term.
