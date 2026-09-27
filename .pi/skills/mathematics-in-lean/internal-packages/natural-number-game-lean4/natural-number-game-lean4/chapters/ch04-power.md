# Chapter 4: Power World — Recursive Exponents and the Final-Boss Boundary

## Core Idea

Exponentiation inherits the same proof architecture: `pow_zero a : a ^ 0 = 1` and `pow_succ a n : a ^ succ n = a ^ n * a`. Induct on the exponent, then use multiplication and addition laws to normalize. The final level is also a critical epistemic boundary: the game states a version of Fermat's Last Theorem and closes it with a hidden `xyzzy` axiom/macro, so completion of that level must not be presented as a derivation of FLT from the curriculum.

## Frameworks Introduced

- **Exponent induction**
  - When to use: a law is universal in an exponent.
  - How: induct on that exponent; rewrite `pow_zero` in the base case and `pow_succ` in the step; use the IH and multiplicative algebra.

- **Layered algebra**
  - Power proofs often descend `pow → mul → add`. Select normalization lemmas from the lower layer after each recursive expansion.

- **Boundary-aware proof reporting**
  - When a source intentionally introduces an unrestricted axiom/tactic, report that mechanism explicitly. Do not infer mathematical validity from kernel acceptance under that added axiom.

## Key Concepts

- `zero_pow_zero : 0 ^ 0 = 1`: follows from the chosen definition; NNG explicitly adopts this convention.
- `zero_pow_succ`: positive powers of zero reduce via `pow_succ` and multiplication by zero.
- `pow_one`, `one_pow`, `pow_two`: bridge recursion to familiar notation.
- `pow_add`: `a^(m+n) = a^m * a^n`, proved by exponent induction.
- `mul_pow`: distributes a common exponent over a product.
- `pow_pow`: `(a^m)^n = a^(m*n)`.
- `add_sq`: expands `(a+b)^2` using prior power, multiplication, distribution, and AC laws.

## Procedure: solve a power identity

1. If the exponent is concrete (`0`, `1`, `2`), rewrite it into the form targeted by `pow_zero`, `pow_succ`, `pow_one`, or `pow_two`.
2. For a variable exponent, induct on the exponent unless a previously proved power theorem gives a direct rewrite.
3. Rewrite `pow_succ` in the step. Locate the IH literally and apply it.
4. Normalize the resulting products with `mul_assoc`, `mul_comm`, distribution, and lower-layer theorems.
5. If addition occurs in the exponent, align it with `add_zero`/`add_succ` so the recursive exponent equation fires.
6. Use explicit arguments on commutativity when many products are present.

## Example proof shape

For `pow_add a m n`, induction on `n` works because addition and power both expose their recursive behavior on the second argument:

```lean
induction n with t ht
· rw [add_zero, pow_zero, mul_one]
  rfl
· rw [add_succ, pow_succ, pow_succ, ht, mul_assoc]
  rfl
```

This is a model example of **aligned recursion**: the exponent sum and the power definition advance on the same successor variable.

## The FLT level

The final statement encodes positive bases as `a + 1`, `b + 1`, `c + 1` and an exponent at least three as `n + 3`, avoiding order notation that may not yet be unlocked. In the source, its proof is simply the hidden tactic `xyzzy`. `Game/Tactic/Xyzzy.lean` introduces an axiom that can inhabit an arbitrary proposition and a macro that exacts it.

Operational rule:

- For **game completion**, explain that `xyzzy` is the intended hidden escape hatch present in the source.
- For **mathematical proof**, decline to infer FLT from the preceding levels; route to external number-theory machinery or a formal FLT development if one is requested.

## Anti-patterns

- Inducting on the base when only the exponent recurses.
- Expanding powers while ignoring product association/order; the IH can become buried inside a differently parenthesized product.
- Treating `0^0=1` as a universal convention rather than this development's definition.
- Calling `xyzzy` a proof derived from NNG's arithmetic lemmas.

## Key Takeaways

1. Exponent recursion is on the exponent, so induction should usually follow it.
2. `pow_add` is a clean aligned-recursion template.
3. Higher power identities require disciplined product normalization.
4. Small numeral lemmas (`pow_one`, `pow_two`) make later algebra readable.
5. Source-level axioms change what Lean can accept; always separate acceptance under an axiom from theorem derivation.

## Connects To

- **Ch 3** supplies the multiplication laws used after `pow_succ`.
- **Ch 5** supplies negation notation used in the FLT statement.
- **References/tactic semantics** documents `xyzzy` precisely.

## Source anchors

`Game/Levels/Power/L01zero_pow_zero.lean` through `L10FLT.lean`; `Game/MyNat/Power.lean`; `Game/Tactic/Xyzzy.lean`; dependency note in `Game.lean`.
