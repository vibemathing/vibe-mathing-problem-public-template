# Chapter 1: Tutorial World — Equality, Rewriting, and Numerals

## Core Idea

Treat a proof state as an expression-transformation problem. Tutorial World builds the minimal loop used throughout NNG4: recognize a reflexive goal, rewrite with an equality in the useful direction, expose the recursive definitions of arithmetic, and finish once both sides coincide.

## Frameworks Introduced

- **Reflexive closure (`rfl`)**
  - When to use: the two sides of an equality are literally or reducibly the same in the NNG environment.
  - How: simplify only as far as needed, then run `rfl`.
  - Game-specific constraint: NNG's custom `rfl` uses a restricted transparency mode, so it intentionally does less computation than full-strength Lean may do.

- **Directed substitution (`rw`)**
  - When to use: a theorem or hypothesis gives an equality matching a subterm of the goal or a hypothesis.
  - How: `rw [h]` replaces the left side by the right side; `rw [← h]` goes backward. Give explicit arguments for precision when the same theorem can match several places.

- **Occurrence control (`nth_rewrite`)**
  - When to use: several syntactically identical occurrences exist and only one should change.
  - How: identify the occurrence, rewrite it, then continue with ordinary `rw`/`rfl`.

- **Numerals as successor structure**
  - Think of `2` as `succ (succ 0)`. The tutorial lemmas `one_eq_succ_zero`, `two_eq_succ_one`, `three_eq_succ_two`, and `four_eq_succ_three` bridge notation to the Peano representation.

## Key Concepts

- **MyNat (`ℕ` in the game)**: an inductive type with constructors `zero` and `succ`.
- **Addition**: opaque operation characterized initially by `add_zero a : a + 0 = a` and `add_succ a d : a + succ d = succ (a + d)`.
- **Rewrite direction**: proof search often depends on whether a theorem is used forward or backward.
- **Precision rewriting**: instantiate theorem arguments when a broad rewrite changes the wrong subterm.
- **Definitional endpoint**: `rfl` is best viewed as a final check after explicit transformations in the game.

## Procedure: solve an elementary equality

1. Compare both sides. If identical under the game's reducible computation, try `rfl`.
2. Scan available equalities for a subterm match.
3. Choose rewrite direction by asking which form exposes a recursive axiom or matches the other side.
4. If repeated patterns exist, instantiate the theorem or use `nth_rewrite`.
5. For concrete numerals, convert between numeral and `succ` forms only when a Peano lemma requires it.
6. Apply `add_zero`/`add_succ` as the recursive structure appears.
7. Stop rewriting when both sides agree; close with `rfl`.

## Representative code

```lean
-- Forward substitution
rw [h]
rfl

-- Backward substitution
rw [← h]
rfl
```

For `succ n = n + 1`, the useful observation is that `1 = succ 0`; then `add_succ` and `add_zero` expose the same successor expression. For `2 + 2 = 4`, numeral-to-successor rewrites plus `add_succ`/`add_zero` reduce both sides to the same constructor chain.

## Anti-patterns

- **Blind rewriting**: repeatedly running a theorem without checking which occurrence changed can move the goal away from a solvable normal form.
- **Over-unfolding numerals**: expanding every numeral at once creates noise; expose only the constructor structure needed by the current lemma.
- **Assuming standard `rw` closes the goal**: NNG's custom rewrite avoids the usual automatic reflexivity cleanup; expect a final `rfl`.
- **Using a later theorem to skip the lesson**: when solving the game progressively, preserve the theorem inventory available at the current level.

## Key Takeaways

1. Equality proofs in NNG begin with exact syntactic control.
2. Direction and occurrence are first-class rewrite decisions.
3. Arithmetic is governed by a few recursive equations; expose those equations instead of asking Lean to “calculate” abstract terms.
4. Numerals are notation over the same zero/successor structure used in proofs.
5. `rfl` is a reliable endpoint after the intended rewrites have aligned both sides.

## Connects To

- **Ch 2**: induction turns this rewrite loop into a method for all naturals.
- **Ch 5**: the same rewrite discipline is applied inside hypotheses and implication goals.
- **Ch 9**: Algorithm World later packages repeated rewriting into controlled automation.

## Source anchors

`Game/Levels/Tutorial/L01rfl.lean` through `L08twoaddtwo.lean`; `Game/MyNat/Definition.lean`; `Game/MyNat/Addition.lean`; `Game/MyNat/TutorialLemmas.lean`; custom tactics in `Game/Tactic/Rfl.lean` and `Rw.lean`.
