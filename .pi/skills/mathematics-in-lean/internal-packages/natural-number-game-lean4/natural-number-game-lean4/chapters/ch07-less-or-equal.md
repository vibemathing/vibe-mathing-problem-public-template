# Chapter 7: ≤ World — Order as an Explicit Additive Witness

## Core Idea

NNG defines `a ≤ b` constructively as **there exists a gap `c` with `b = a + c`**. Every order proof should exploit this representation. Proving `≤` means constructing a witness; using `≤` means unpacking one. Standard order laws then become calculations on additive gaps plus constructor case analysis.

## Frameworks Introduced

- **Witness construction (`use`)**
  - When to use: the goal is existential, especially `a ≤ b` under the NNG definition.
  - How: choose the concrete gap `c`; the remaining goal is an additive equality.

- **Witness elimination (`cases`)**
  - When to use: a hypothesis carries existential data.
  - How: `cases h with c hc` exposes both the witness and the equality relating endpoints.

- **Gap composition**
  - If `y = x + a` and `z = y + b`, then `z = x + (a+b)` after rewriting/associating. This proves transitivity.

- **Constructor totality**
  - Totality `x ≤ y ∨ y ≤ x` is proved structurally, tracking how successor constructors transform witnesses.

- **Finite upper-bound classification**
  - For tiny bounds, `x ≤ 1` or `x ≤ 2` can be turned into a finite disjunction of constructor possibilities by unpacking the gap and splitting cases.

## Key Concepts

- `le_refl`: witness `0`.
- `zero_le`: witness `x`, using `zero_add`.
- `le_succ_self`: witness `1`, using the successor/add-one relation.
- `le_trans`: add the two gaps.
- `le_zero`: a witness for `x ≤ 0` forces `x = 0`.
- `le_antisymm`: opposite gaps force both gaps to vanish/cancel, yielding equality.
- `le_total`: structural comparison returns one of two witness directions.
- `succ_le_succ`: removes matching successors from an inequality witness equation.
- `le_one`, `le_two`: finite classification under small bounds.

## Procedure: prove `a ≤ b`

1. Expand the meaning mentally: find `c` such that `b = a + c`.
2. Run `use c`.
3. Normalize the resulting equality with addition lemmas.
4. If the witness is inherited from another inequality, unpack that hypothesis rather than guessing a fresh witness.

## Procedure: use `h : a ≤ b`

1. `cases h with c hc` to obtain `c` and `hc : b = a + c` (orientation may be source-specific but the content is an additive gap).
2. Rewrite `b` using `hc` wherever useful.
3. For transitivity, unpack the second inequality too and use `c₁ + c₂` as the composed witness.
4. For antisymmetry, combine both gap equations, normalize, and use additive cancellation/zero facts to collapse the gaps.

## Disjunction routing

When the goal is `P ∨ Q`, choose a branch with `left` or `right` only when you have enough data to finish it. When a disjunction is a hypothesis, `cases` creates one goal per branch. Totality and bounded-classification proofs mix this logical case split with natural-number constructor cases.

## Decision table

| Goal/hypothesis | Operational view |
|---|---|
| `a ≤ b` goal | construct additive gap |
| `a ≤ b` hypothesis | unpack gap + endpoint equality |
| transitivity | add gaps |
| antisymmetry | opposite gaps + cancellation |
| `x ≤ 0` | gap equation forces zero |
| `succ x ≤ succ y` | strip matching successor structure |
| `x ≤ 1/2` | finite constructor enumeration |
| totality | structural cases, return left/right witness |

## Anti-patterns

- **Treating `≤` as a built-in arithmetic oracle**. The skill should preserve the explicit existential meaning in NNG.
- **Writing an unnecessary rewrite of the definition before `use`**. The custom tactic can work directly with the definitional existential.
- **Guessing subtraction**. Subtraction is not available; the “difference” is an existential witness supplied constructively.
- **Losing witness orientation**. Before rewriting, check whether the equation says `b = a + c` or is currently reversed.

## Key Takeaways

1. Order is data: a `≤` proof contains a concrete additive gap.
2. `use` constructs order evidence; `cases` extracts it.
3. Transitivity is gap addition.
4. Antisymmetry is a cancellation/zero argument over opposite gaps.
5. Small upper bounds can be classified by explicit Peano cases without general arithmetic automation.

## Connects To

- **Ch 6** provides cancellation and zero-sum lemmas.
- **Ch 8** uses `≤` to express consequences of nonzero multiplication.
- **Foundations** records the exact `le` definition.

## Source anchors

`Game/Levels/LessOrEqual/L01le_refl.lean` through `L11le_two.lean`; `Game/MyNat/LE.lean` and `Inequality.lean`; custom `Use.lean`, `Cases.lean`, and `LeftRight.lean`.
