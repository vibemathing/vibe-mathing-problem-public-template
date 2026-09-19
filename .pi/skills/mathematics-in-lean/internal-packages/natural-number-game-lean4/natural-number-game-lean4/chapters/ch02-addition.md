# Chapter 2: Addition World — Induction Aligned with Recursion

## Core Idea

The decisive proof pattern is **induct on the argument that the operation recursively consumes**. NNG addition is specified on its second argument by `add_zero` and `add_succ`; induction on that argument makes the base and step cases line up with the defining equations.

## Frameworks Introduced

- **Base/step induction loop**
  - When to use: a proposition depends on an arbitrary `n : ℕ` and its successor case can be reduced to the `n` case.
  - How: `induction n with d hd`; rewrite the zero case with base equations; rewrite the successor case with recursive equations and `hd`.

- **Mirror-lemma strategy**
  - Recursive equations describe `a + 0` and `a + succ b`, so facts about `0 + a` and `succ a + b` must be proved. Once those mirror facts exist, later proofs become short rewrites.

- **Algebra from recursion**
  - Commutativity and associativity are not primitive. They are derived by induction, after which they become routing tools for later worlds.

## Key Concepts

- `zero_add n : 0 + n = n`: proves the “other side” of the primitive `add_zero` equation.
- `succ_add a b : succ a + b = succ (a + b)`: mirrors `add_succ`, whose recursion is on the second argument.
- `add_comm a b : a + b = b + a`: the world boss and a major theorem-reuse tool.
- `add_assoc a b c : a + b + c = a + (b + c)`: controls parentheses so recursive and cancellation lemmas can match.
- `add_right_comm a b c : a + b + c = a + c + b`: a useful local permutation theorem.

## Procedure: choose an induction variable

1. Find the recursive equation relevant to the target. For addition, `add_succ a b` changes the **second** argument.
2. Inspect each side of the proposed theorem. Prefer a variable whose zero/successor split exposes `add_zero`/`add_succ` after a small number of rewrites.
3. In the base case, eliminate `+ 0` and known zero-left terms.
4. In the step case, rewrite both sides until the induction hypothesis appears literally.
5. Apply the IH, then normalize successor/addition placement with previously proved lemmas.
6. Close by `rfl` once expressions coincide.

This explains why `zero_add` is proved first: later proofs such as `add_comm` need a theorem for the left-zero case that the primitive definition does not provide.

## Representative code shape

```lean
induction n with d hd
· rw [add_zero]
  -- normalize remaining zero-side expression
  rfl
· rw [add_succ]
  -- expose the same recursive call on the other side
  rw [hd]
  rfl
```

Exact rewrites vary by theorem; the invariant is that the step goal must be reduced to the IH plus one constructor-level equality.

## Decision rules

| Situation | Preferred move |
|---|---|
| theorem varies over second addend | induct on that addend |
| theorem places recursion on the “wrong” side | use/prove mirror lemma such as `zero_add` or `succ_add` |
| terms differ by swapping addends | use `add_comm` once available |
| parentheses block a match | rewrite `add_assoc` in the useful direction |
| three terms need a local swap | use `add_right_comm` or derive via assoc/comm |

## Anti-patterns

- **Inducting on a visually prominent variable** without checking the recursive definition. The resulting step can lack a usable IH occurrence.
- **Trying to compute abstract addition**. The operation is opaque; only its axioms and proved lemmas expose behavior.
- **Circular use of commutativity**. While proving `add_comm`, do not use a theorem whose proof already depends on `add_comm`.
- **Reassociating randomly**. Parentheses should be moved to create the exact subterm expected by the next theorem.

## Key Takeaways

1. Recursive definitions determine profitable induction variables.
2. One-sided recursion creates a predictable need for mirror lemmas.
3. Induction reduces a global law to a constructor equation plus an IH.
4. Commutativity/associativity become infrastructure for nearly every later arithmetic proof.
5. When an IH is not visible after unfolding, diagnose variable choice and expression shape before adding more tactics.

## Connects To

- **Ch 3** and **Ch 4** repeat the same architecture for multiplication and powers.
- **Ch 6** uses additive algebra to derive cancellation and zero equations.
- **Ch 7** represents order entirely through addition, so these lemmas become the order engine.

## Source anchors

`Game/Levels/Addition/L01zero_add.lean` through `L05add_right_comm.lean`; primitive equations in `Game/MyNat/Addition.lean`; custom induction behavior in `Game/Tactic/Induction.lean`.
