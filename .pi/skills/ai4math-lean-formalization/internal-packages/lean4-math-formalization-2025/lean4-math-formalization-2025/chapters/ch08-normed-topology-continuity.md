# 08 — Normed Spaces, Topology, and Continuity

## Core Idea

Mathlib reuses weaker structures aggressively. Before proving an analysis fact, identify the minimum structure the theorem needs:

**metric → normed → inner-product**, with **completeness** adding Banach/Hilbert behavior and **topology/filters** providing continuity.

## Normed spaces

A norm satisfies positivity/separation, scalar homogeneity, and the triangle inequality. In Mathlib, a normed additive group induces a metric via:

```text
dist x y = ‖x - y‖
```

A normed space also carries a module/vector-space action compatible with the norm.

### Common norm facts

Search/use standard lemmas for:

- `0 ≤ ‖x‖`;
- `‖x‖ = 0 ↔ x = 0` under the appropriate structure;
- triangle inequality `‖x + y‖ ≤ ‖x‖ + ‖y‖`;
- norm of scalar multiplication.

Do not unfold the norm structure to prove these facts.

### Instance inheritance

If you already have a normed structure, a metric structure is usually inferable. Use:

```lean
infer_instance
```

as a diagnostic/construction when the desired structure should follow automatically.

A complete normed space is a Banach space. Finite-dimensional normed spaces over the usual complete scalar fields commonly obtain completeness through existing instances/theorems; check inference before writing a proof.

## Inner-product spaces

An inner product adds linear/sesquilinear and conjugate-symmetry structure and induces the norm. Mathlib encodes the exact scalar-field conventions in `InnerProductSpace`.

Use an inner-product assumption only when the theorem needs inner products/orthogonality. Norm-only results should remain at the normed-space layer.

A complete inner-product space is a Hilbert space in the mathematical sense. In Lean, this is usually represented by combining `InnerProductSpace` with `CompleteSpace`, not by requiring a special “HilbertSpace” wrapper.

## Open and closed sets

In a metric space:

- an open set contains a ball around each point;
- a closed set has open complement.

Mathlib also exposes these topologically, so choose the formulation that matches the proof.

### Metric-to-topology bridge

Useful forms include:

- `Metric.isOpen_iff` for ball-based openness;
- neighborhood-basis lemmas connecting `s ∈ nhds x` to a ball/closed ball contained in `s`.

If a proof is about a numeric radius, metric balls are natural. If it is about continuity/composition, neighborhood/filter forms are usually more compositional.

## Neighborhoods

`nhds x` contains sets that include some open neighborhood of `x`. A neighborhood need not itself be open.

This distinction matters: prove “`U` is a neighborhood of x” by finding an open set/ball around `x` inside `U`, or use an existing neighborhood-basis theorem.

## Continuity hierarchy

### Global continuity

Conceptually, `Continuous f` says open sets pull back to open sets. In practice, use its API rather than unfolding this definition.

### Continuity at a point

```lean
ContinuousAt f x
```

is expressed through a filter limit from `nhds x` to `nhds (f x)`.

### Within a set

```lean
ContinuousWithinAt f s x
ContinuousOn f s
```

replace the source neighborhood by a neighborhood restricted to `s`. Use these when the domain restriction matters, especially near boundaries.

## Epsilon–delta bridge

In metric spaces, `ContinuousAt f a` has an epsilon–delta characterization. The source course points to `Metric.continuousAt_iff`.

Decision:

- use abstract continuity API for composition and standard functions;
- use epsilon–delta when proving a concrete estimate or translating textbook analysis;
- convert back to `ContinuousAt` after the estimate so downstream theorems can reuse it.

## `continuity` and `continuity?`

For expressions built from functions already known continuous, try:

```lean
by continuity
```

If it works but you need transparency, or if you want to see the compositional theorem chain, try `continuity?` in an exploratory proof and inspect the suggested steps.

### Recovery when `continuity` fails

1. identify the outermost function constructor (composition, addition, product, power, etc.);
2. `apply` the corresponding continuity lemma;
3. prove each component's continuity;
4. confirm required metric/topological instances;
5. use a within/at version matching the target.

Do not immediately unfold `Continuous` into open-set preimages unless the proof is genuinely topological.

## Structure-selection checklist

Before writing the theorem, ask:

- only distance? → `MetricSpace` may suffice;
- vector operations + norm? → normed additive group/module/normed space;
- inner product? → `InnerProductSpace`;
- convergence of Cauchy sequences? → add `CompleteSpace`;
- finite-dimensional fact? → add/check `FiniteDimensional` and let instances derive consequences;
- topology only? → a weaker topological structure may be enough than metric.

Keeping assumptions minimal improves theorem matching and reuse.

## Worked Example — continuity routing

### Prove continuity of a composite algebraic expression

Given `hf : Continuous f` and target such as continuity of `x ↦ f (x^2 + x)`:

1. try `continuity`;
2. if debugging, decompose into continuity of `f` and the polynomial inner function;
3. use continuity of identity, power, addition, and composition;
4. retain a high-level `Continuous` result.

### Prove an open-set fact via a radius

If the goal is `IsOpen s` and you can explicitly produce a radius around every `x ∈ s`, use the metric characterization instead of constructing topology internals.

## Failure modes

- **Too-strong assumptions:** theorem search misses a lemma stated for a weaker structure; search at the parent layer.
- **Missing instance despite obvious mathematics:** inspect exact scalar field/module/norm assumptions and run `infer_instance` as a test.
- **Confusing neighborhood with open set:** a neighborhood only has to contain an open set around the point.
- **Using epsilon–delta for every composition:** leverage abstract continuity lemmas first.
- **Using `continuity` as a black box during debugging:** inspect `continuity?` or manually decompose the outer operation.

## Key Takeaways

Choose the weakest sufficient structure and keep proofs at the API level. Cross to metric balls/epsilon estimates only when the mathematics calls for an explicit bound.

## Connects To

- Filters and metric convergence → [ch07](ch07-filters-limits-metric.md)
- Continuous linear maps and derivatives → [ch09](ch09-continuous-linear-derivatives.md)
- Typeclass diagnosis → [ch05](ch05-dependent-types-term-construction.md)
