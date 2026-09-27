# Chapter 5: Implication World — Forward Evidence, Backward Goals, and Negation

## Core Idea

Implication World changes proof search from pure equation manipulation to **movement between propositions**. `exact`, `apply`, and `intro` let you decide whether to transform available evidence forward or transform the goal backward. Negation is then handled as an implication to `False`, with Peano's successor injectivity and zero/successor separation providing structural contradictions.

## Frameworks Introduced

- **Exact-match closure**
  - `exact h` when `h` has the goal type. If it almost matches, normalize the hypothesis or goal first.

- **Forward application**
  - Given `h1 : P` and `h2 : P → Q`, `apply h2 at h1` turns `h1` into evidence for `Q`.

- **Backward application**
  - If the goal is `Q` and a theorem proves `P → Q`, `apply theorem` changes the goal to `P`. This is goal-directed reasoning.

- **Implication introduction**
  - For a goal `P → Q`, `intro h` places `h : P` in the context and leaves `Q`.

- **Negation as contradiction**
  - `a ≠ b` means `a = b → False`. Prove a negation by assuming equality and reducing it to an impossible constructor equality.

## Key Concepts

- `succ_inj`: if `succ a = succ b`, then `a = b`.
- `zero_ne_succ`: `0 ≠ succ a`.
- `symm`: flip equality orientation when the available contradiction theorem faces the other direction.
- Hypothesis rewriting: `rw [...] at h` normalizes evidence until it can be used directly.
- Goal rewriting: normalize the conclusion until a known implication/theorem applies.

## Procedure: implication goal

1. If the goal itself is `P → Q`, start with `intro hP`.
2. Inspect the context for a theorem/hypothesis ending in `Q`.
3. If found, `apply` it backward and solve its premise.
4. If instead you already possess evidence for a premise, apply an implication **at that evidence** to push it forward.
5. Rewrite the relevant side before `apply` when syntactic forms differ.
6. Use `exact` once the produced evidence has the exact goal type.

The levels `x + 1 = 4 → x = 3` deliberately show both directions: one solution rewrites the hypothesis then applies `succ_inj` forward; another applies `succ_inj` to the goal and rewrites backward until the original hypothesis closes it.

## Procedure: prove `a ≠ b`

1. Read the goal as `a = b → False` and `intro h`.
2. Normalize numerals and arithmetic so both sides become zero/successor chains.
3. Apply `succ_inj` repeatedly to strip equal successor constructors.
4. Reach an equality such as `0 = succ n` or its symmetric form.
5. Apply `zero_ne_succ` (or symmetry plus it) to obtain `False`.

This is the structural reason `2 + 2 ≠ 5`: after reducing addition/numerals and injecting matching successors, the hypothetical equality eventually claims zero equals a successor.

## Decision table

| Shape | Move |
|---|---|
| goal exactly in context | `exact` |
| goal `P → Q` | `intro` |
| have `P`, have `P → Q` | `apply ... at ...` |
| goal `Q`, theorem `P → Q` | `apply theorem` |
| goal `a ≠ b` | `intro` equality, derive `False` |
| equality differs by succ wrappers | `succ_inj` |
| contradiction is reversed | `symm`/rewrite orientation |

## Anti-patterns

- **Applying before normalizing**: Lean matches types syntactically enough that mathematically equivalent forms can still fail to fit.
- **Using `exact` on a near-match**: rewrite first; `exact` is intentionally strict.
- **Treating `≠` as a primitive comparison operation**. In this curriculum it is proof-producing logic: equality implies `False`.
- **Throwing automation at constructor contradictions** when the intended Peano structure is available directly.

## Key Takeaways

1. `apply` supports two complementary modes: forward on evidence and backward on goals.
2. `intro` turns a hypothetical goal into local data.
3. Rewrite and logical routing compose: normalize first, then apply.
4. Natural-number inequality is grounded in constructor separation.
5. Exact goal-state shape matters as much as mathematical equivalence in tactic selection.

## Connects To

- **Ch 6** uses implication plus cancellation to derive advanced additive consequences.
- **Ch 8** uses contradiction and nonzero implications extensively.
- **Ch 9** reconstructs Peano facts algorithmically using `pred`, `is_zero`, and decidable equality.

## Source anchors

`Game/Levels/Implication/L01exact.lean` through `L11two_add_two_ne_five.lean`; `Game/MyNat/PeanoAxioms.lean`; numeral lemmas from the Tutorial; notation behavior in `Game/Tactic/Ne.lean`.
