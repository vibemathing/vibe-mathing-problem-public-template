# 07 — Extended Reals, Filters, Limits, and Metric Spaces

## Core Idea

Mathlib analysis scales by replacing ad-hoc epsilon definitions with reusable structure. Learn the abstraction chain and move between concrete and abstract formulations deliberately:

**extended reals → filters → `Tendsto` → metric epsilon characterizations → Cauchy/completeness**.

## Extended real numbers

Mathlib uses types such as:

- `ENNReal`: nonnegative reals with `∞`;
- `EReal`: reals with both `-∞` and `∞`.

Arithmetic at infinity has defined behavior that can differ from informal algebraic manipulation. Therefore, do not send an `EReal` inequality directly to real-only automation and expect ordinary field laws.

### EReal inequality procedure

When a goal involves order/arithmetic on `EReal`:

1. identify operands that may be `⊤` or `⊥`;
2. split the infinite cases using available cases/lemmas;
3. discharge trivial/impossible infinity branches using order facts;
4. in the finite branch, convert/lift values to real numbers (`toReal`, `lift`, or current API equivalent);
5. prove side conditions guaranteeing finiteness as required;
6. run real arithmetic (`linarith`, normalization) only after the goal is genuinely real-valued.

Do not treat `toReal` as an inverse on infinities: its total definition has fallback values. Finiteness hypotheses are part of the proof obligation.

## Euclidean space as the familiar base case

Finite-dimensional Euclidean space can be represented directly or via a finite-dimensional real inner-product space. It supports distance, norm, and inner product simultaneously.

Use this level when the problem is genuinely coordinate/Euclidean. Move to weaker structures when a theorem only requires a metric or norm; weaker assumptions make lemmas more reusable and easier for Mathlib to match.

## Filters

A filter on a type packages the sets that count as “eventually” or “near enough.” Conceptually it contains:

- the whole space;
- supersets of every member;
- finite intersections of members.

Important examples:

- `atTop`: sufficiently large ordered values, especially indices;
- `nhds x`: neighborhoods of `x`.

### Filter order warning

Filter order is chosen so that a **finer/stronger** filter can be `≤` a coarser one. The membership formulation therefore looks reversed compared with ordinary set inclusion. When unsure, inspect `le_def` or the current theorem rather than reasoning from the symbol alone.

## Preimages and `Filter.map`

For `f : α → β`, the preimage of `s : Set β` is the set of `x` whose image lies in `s`.

This is the bridge from functions to filters. `Filter.map f l` is the filter on `β` whose sets are those with preimage in `l`.

Operational intuition:

```text
V is eventually true after applying f
⇔ f ⁻¹' V is eventually true before applying f
```

Preimages compose, which is why filter-based limits compose cleanly.

## `Tendsto`

The generic limit relation is:

```lean
Tendsto f l₁ l₂
```

meaning that `f` sends behavior described by source filter `l₁` into behavior described by target filter `l₂`.

For a sequence `u : Nat → X` converging to `a`:

```lean
Tendsto u atTop (nhds a)
```

This single shape supports sequences, limits at points, limits at infinity, and continuity.

### How to prove a `Tendsto` goal

First search for compositional lemmas at the `Tendsto` layer:

- limit of sum/product;
- composition;
- monotone/subsequence behavior;
- known continuous function tending to its value.

Only descend to filter membership or epsilon estimates when the high-level theorem is missing or the proof is fundamentally quantitative.

### How to use a `Tendsto` hypothesis

Prefer API lemmas that consume it. If you need an explicit eventual estimate, switch through a metric/order characterization instead of unfolding the raw filter structure manually.

## Eventually

The notation `∀ᶠ x in l, P x` means that `P` holds eventually with respect to filter `l`. For `atTop`, read it as “for all sufficiently large values.”

This is useful for statements that are tail properties without a numeric limit, and it composes with filter reasoning.

## Subsequences

A strictly monotone map `φ : Nat → Nat` selects a subsequence. A convergent sequence remains convergent along such a reindexing. Operationally, search for `Tendsto` lemmas about composition with `atTop`/strict monotonicity rather than re-proving epsilon–N facts from scratch.

## Metric spaces

A metric space adds a distance satisfying the usual metric axioms. In Mathlib, `MetricSpace` refines a pseudometric structure by adding separation (`dist x y = 0 → x = y`).

### Metric sequence convergence

For `u : Nat → X`, the filter limit is equivalent to an epsilon tail condition. The course points to `Metric.tendsto_atTop` as the bridge.

Use the two directions intentionally:

- **filter → epsilon:** extract explicit `N` and distance bounds for estimates;
- **epsilon → filter:** package a concrete convergence proof back into the reusable `Tendsto` form.

Verify the current theorem signature with `#check Metric.tendsto_atTop`.

## Cauchy sequences and completeness

A Cauchy sequence eventually has all pairs of terms close to each other. Mathlib exposes an epsilon characterization (`Metric.cauchySeq_iff` in the source version).

A complete space ensures Cauchy sequences converge. The course highlights a theorem in the direction “if every Cauchy sequence converges, obtain `CompleteSpace X`.” More commonly, existing types already carry a `CompleteSpace` instance that can be inferred.

### Completeness workflow

1. check whether `CompleteSpace X` is already an instance (`infer_instance`);
2. if proving convergence from Cauchy, search the completeness API before expanding definitions;
3. switch to the epsilon characterization only for the quantitative step;
4. keep the final convergence result in `Tendsto` form when later lemmas consume it.

## Worked Example — combine known limits

When `u` tends to `a` and `v` tends to `b` along the same source filter, keep the argument at the `Tendsto` layer and use the library rule for addition rather than reopening both epsilon definitions. Switch to a metric epsilon characterization only if a later goal asks for an explicit tail index or distance estimate. This illustrates the chapter's main abstraction rule: compose abstractly, estimate concretely.

## Decision table

| Goal | Preferred level |
|---|---|
| concrete sequence estimate | metric epsilon form |
| addition/composition of known limits | `Tendsto` |
| “eventually P” tail fact | filter/eventually |
| point approaching another point | `nhds` |
| index → infinity | `atTop` |
| EReal inequality | infinity cases → finite real case |
| Cauchy/convergence bridge | metric/completeness API |

## Failure modes

- **Unfolding `Filter` too early:** search `Tendsto`, neighborhood, or basis lemmas first.
- **Confusing filter order with set inclusion:** use the membership characterization.
- **Using `toReal` without finiteness:** prove non-infinite side conditions.
- **Trying `linarith` on extended reals:** reduce to a finite real branch first.
- **Proving epsilon algebra repeatedly:** package convergence as `Tendsto` and compose it.
- **Missing completeness:** check typeclass inference before constructing a completeness proof.

## Key Takeaways

Filters are an interface for “approach/eventually.” Use them for composition; cross to metric epsilon statements when explicit bounds are the real work.

## Connects To

- Sets/preimages → [ch04](ch04-mathlib-search-sets-blueprints.md)
- Normed/inner-product structures and continuity → [ch08](ch08-normed-topology-continuity.md)
- Derivatives use filters + continuous linear maps → [ch09](ch09-continuous-linear-derivatives.md)
