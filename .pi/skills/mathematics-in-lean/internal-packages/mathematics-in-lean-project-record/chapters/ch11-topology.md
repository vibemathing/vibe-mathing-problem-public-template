# Chapter 11: Topology

## Core Idea
Mathlib organizes limits and continuity around filters. Filters factor dozens of specialized ε-style limit notions into one `Tendsto` relation, make “eventually” algebraic, and support topological/metric APIs through map, comap, lattice operations, neighborhood bases, and compactness.

## Frameworks Introduced
- **Filter as generalized large/near set**
  - When to use: limits, eventual behavior, neighborhoods, almost-everywhere statements.
  - How: think of `atTop` as very large indices, `𝓝 x` as points close to `x`, and `ae μ` as almost every point. A filter is upward closed and closed under finite intersections.
- **`Tendsto` as map-order relation**
  - When to use: any convergence/continuity statement.
  - How: read `Tendsto f F G` as `Filter.map f F ≤ G`. Compose limits using `Tendsto.comp`/map composition instead of reproving each source/target variant.
- **Map/comap Galois connection**
  - When to use: change domains, restrict to subtypes, or reason about images/preimages of generalized neighborhoods.
  - How: use `Filter.map_le_iff_le_comap`; remember map is covariant and comap is contravariant.
- **Filter basis bridge**
  - When to use: convert abstract `Tendsto` back to concrete ε–N or ball conditions.
  - How: obtain `HasBasis` for source/target filters and use its `tendsto_iff`/membership lemmas. Keep basis expansion at the boundary of the proof.
- **Eventually algebra**
  - When to use: combine facts that each hold sufficiently far out/near a point.
  - How: use `∀ᶠ x in F, P x`, `Eventually.and`, `.mono`, or `filter_upwards`; avoid manually taking maxima of thresholds unless you specifically need the concrete form.
- **Metric-to-topological layering**
  - When to use: concrete distance estimates and abstract topology appear together.
  - How: use metric characterizations (`Metric.tendsto_atTop`, `Metric.continuous_iff`, ball bases) for epsilon arguments; return to topological/filter theorems for composition, closure, compactness, and generality.
- **Induced/coinduced topology design**
  - When to use: subspaces, quotients, products, or topology transport.
  - How: use `TopologicalSpace.induced` to pull a topology back and `coinduced` to push one forward. Their Galois connection and the complete lattice produce canonical product/quotient topologies.

## Key Concepts
- **Principal filter**: sets containing a fixed set; embeds sets into filters.
- **`Filter.NeBot`**: nontriviality of a filter; necessary for conclusions that would fail for the bottom filter.
- **Filter product**: combines source filters on a product; neighborhoods of `(x,y)` decompose as product neighborhoods.
- **`Frequently` (`∃ᶠ`)**: dual to eventually; says a property occurs arbitrarily often with respect to the filter.
- **Metric ball / closed ball**: concrete neighborhood bases in metric spaces.
- **`Continuous` / `ContinuousAt`**: globally via preimages of open sets, locally via `Tendsto` between neighborhood filters.
- **Compactness**: filter-based cluster-point property; equivalent to familiar finite-subcover/sequential formulations under suitable hypotheses.
- **`T2Space` / Hausdorff**: ensures uniqueness of limits.
- **`RegularSpace` / `T3Space`**: supplies closed neighborhood bases and supports extension arguments.
- **First countability**: turns closure into existence of convergent sequences.
- **Complete space**: Cauchy sequences converge.

## Mental Models
- Filters are **generalized sets with order/lattice structure**; `Tendsto` is ordinary image containment lifted to them.
- `Eventually` is **quantifier bookkeeping compressed into filter membership**.
- Metric spaces are the **computational/geometric interface**; topological spaces are the **functorial interface**.
- Induced/coinduced topologies are **universal constructions** solving subspace/quotient/product problems.
- Separation/countability assumptions are **controlled antidotes to topological pathologies**; check which one a theorem needs.

## Anti-patterns
- **Writing a separate ε–N proof for every limit variant**: use `Tendsto` and specialize through bases only when needed.
- **Forgetting `NeBot`**: the bottom filter makes many “there exists a nearby point” claims vacuous/false without nontriviality.
- **Applying a composition-shaped theorem tactically when elaboration cannot see the composition**: choose a pointwise convenience lemma such as `Continuous.dist`, or provide the full term.
- **Assuming sequential criteria in arbitrary topological spaces**: first countability is often required.
- **Expecting metric constructions to be functorial under arbitrary quotients/products**: move to topological induced/coinduced structures.

## Code Examples
```lean
example {α β γ : Type*} {F : Filter α} {G : Filter β} {H : Filter γ}
    {f : α → β} {g : β → γ}
    (hf : Tendsto f F G) (hg : Tendsto g G H) : Tendsto (g ∘ f) F H :=
  hg.comp hf
```
```lean
example (P Q : Nat → Prop)
    (hP : ∀ᶠ n in Filter.atTop, P n)
    (hQ : ∀ᶠ n in Filter.atTop, Q n) :
    ∀ᶠ n in Filter.atTop, P n ∧ Q n :=
  hP.and hQ
```
- **What they demonstrate**: abstract limit composition and eventual conjunction without explicit threshold arithmetic.

## Reference Tables
| Concrete phrase | Filter form |
|---|---|
| sequence tends to `x` | `Tendsto u atTop (𝓝 x)` |
| function continuous at `x` | `Tendsto f (𝓝 x) (𝓝 (f x))` |
| for all sufficiently large `n` | `∀ᶠ n in atTop, ...` |
| arbitrarily large `n` | `∃ᶠ n in atTop, ...` |
| almost every `x` | `∀ᶠ x in ae μ, ...` |
| neighborhood membership | `s ∈ 𝓝 x` |
| domain restriction | `comap inclusion (...)` |
| transport filter forward | `map f F` |

## Section-by-Section Operational Map

**11.1 Filters.** A filter's axioms support the interpretation of its members as sufficiently large sets. `principal`, `map`, `comap`, product, inf/sup, top/bottom, and `NeBot` form an algebra of generalized sets. `Tendsto` is definitionally `map f F ≤ G`; this makes limit composition a one-line order/map calculation. `HasBasis` recovers concrete descriptions such as intervals around a real point or tails of naturals. `Eventually`, `EventuallyEq`, and `Frequently` make quantified “eventual” reasoning compositional. The chapter also connects cluster points/closure to nontrivial intersections of filters.

**11.2 Metric spaces.** Distance provides epsilon formulations of convergence/continuity and concrete neighborhood bases via balls. The `continuity` tactic automates standard closure properties; when it struggles, dot-notation composition lemmas (`hf.comp`, `.dist`, projections) give explicit proofs. Compactness supplies convergent subsequences, extrema, and closedness. Uniform continuity gains a global `δ`, and the compact-domain theorem is proved by converting failure into a compact set separated from the diagonal. Completeness turns Cauchy sequences into convergent ones; the geometric-bound criterion and Baire proof show how finite sums, filters, recursive constructions, and completeness interact.

**11.3 Topological spaces.** Open sets and neighborhood filters are equivalent interfaces; Mathlib leans heavily on neighborhoods. Topologies can be induced/pulled back and coinduced/pushed forward along any function, forming a Galois connection and a complete lattice. These abstract properties generate canonical quotient and product topologies. Separation classes control uniqueness/closed neighborhoods; first countability permits sequence characterizations of closure. Compactness is defined via cluster points of nontrivial filters, with open-cover and subsequence forms available through theorems.

## Failure Recovery Notes

- If a topological theorem asks for `ContinuousAt` but you have a metric epsilon statement, use the metric characterization instead of unfolding neighborhoods manually.
- If a filter proof needs existence from membership, check `NeBot` before attempting choice.
- If a product-continuity proof cannot elaborate a composition, use a theorem tailored to functions with shared domains (`Continuous.prod_mk`, `.dist`, `.fst'`, `.snd'`).
- If a compactness proof on a metric space becomes sequence-heavy, see whether the abstract `IsCompact` API directly supplies the needed image/closed/extreme-value result.

## Worked Example
To prove two eventual properties imply an eventual conjunction, the elementary sequence proof extracts thresholds `NP` and `NQ`, chooses their maximum, then checks both properties above it. With filters, each hypothesis is a set belonging to `atTop`; closure of a filter under intersection gives the conjunction immediately through `hP.and hQ`. The same abstraction works for neighborhoods and almost-everywhere filters. This illustrates why filters scale: one algebraic lemma replaces many domain-specific threshold arguments.

For a compactness-style metric proof, it is often effective to use concrete balls to construct a Cauchy sequence, then use completeness to obtain a limit, and finally switch back to closed-set/filter theorems to show the limit lies in every required set. The chapter's Baire-theorem skeleton exemplifies this layered approach.

## Key Takeaways
1. Default to filters for limit/continuity composition and eventual behavior.
2. Expand to ε–N or balls through a basis only when concrete estimates are needed.
3. Use `map`/`comap` and lattice structure to transport convergence cleanly.
4. Track `NeBot`, separation, completeness, compactness, and countability assumptions explicitly.
5. Use metric lemmas for distance calculations and topological lemmas for structural transport.
6. Let induced/coinduced topology universal properties handle subspace/product/quotient constructions.

## Connects To
- **Ch 3**: filters package repeated quantifier patterns from manual convergence proofs.
- **Ch 12**: differentiability is defined using neighborhood filters and asymptotic comparison.
- **Ch 13**: almost-everywhere reasoning is `Eventually` in the measure's `ae` filter.
