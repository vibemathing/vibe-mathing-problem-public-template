# Foundations and Primitive API

Use this file when theorem selection depends on what is primitive versus what the game proves later.

## MyNat

The game defines its own inductive natural-number type with two constructors:

```lean
inductive MyNat
| zero : MyNat
| succ : MyNat → MyNat
```

The game notation displays this type as `ℕ`. Decimal numerals are interpreted through a custom `OfNat` path; `one` is `succ 0`. Do not assume ordinary `Nat` reduction behavior when writing a game proof.

## Addition

Addition is opaque and specified by equations on the second argument:

```lean
add_zero (a)      : a + 0 = a
add_succ (a) (d) : a + succ d = succ (a + d)
```

Consequences such as `0+a=a`, `succ a+b=succ(a+b)`, commutativity, and associativity are theorems proved in the curriculum.

## Multiplication

Multiplication is opaque and recursively specified on the second factor:

```lean
mul_zero (a)      : a * 0 = 0
mul_succ (a) (b) : a * succ b = a * b + a
```

Left-zero, left-successor, commutativity, distribution, and associativity are derived later.

## Power

Exponentiation is opaque and recursively specified on the exponent:

```lean
pow_zero (m)      : m ^ 0 = 1
pow_succ (m) (n) : m ^ succ n = m ^ n * m
```

The choice entails `0^0=1` in this development.

## Peano observations

`Game/MyNat/PeanoAxioms.lean` supplies/derives the structural tools used in Implication World:

- `pred`: predecessor observer with a deliberate junk zero case (`pred 0 = 37`) and the useful equation `pred (succ n) = n`.
- `pred_succ`.
- `succ_inj`: successor injectivity.
- `is_zero`: constructor discriminator.
- `is_zero_zero`, `is_zero_succ`.
- `zero_ne_succ`: zero differs from every successor.

Algorithm World later demonstrates how these facts can be obtained through explicit computation/definitions, reducing their “axiomatic” feel pedagogically.

## Numeral bridge lemmas

`Game/MyNat/TutorialLemmas.lean` includes named bridges such as:

- `one_eq_succ_zero`
- `two_eq_succ_one`
- `three_eq_succ_two`
- `four_eq_succ_three`

These are useful when a concrete numeral must match a successor theorem.

## Order

The active `≤` curriculum uses the existential-gap definition:

```lean
le (a b : ℕ) := ∃ c, b = a + c
```

`Game/MyNat/Inequality.lean` also contains an experimental/legacy `<` development, defining strict order from `≤` plus failure of the reverse relation. Treat it as reference/WIP unless the user's context imports it.

## Decidable equality

`Game/MyNat/DecidableEq.lean` builds a recursive `DecidableEq MyNat` instance using constructor cases and the zero/successor and successor/successor inequality facts. This instance powers closed computation with `decide` after Algorithm World.

## Source files

`Game/MyNat/Definition.lean`, `Addition.lean`, `Multiplication.lean`, `Power.lean`, `PeanoAxioms.lean`, `LE.lean`, `Inequality.lean`, `TutorialLemmas.lean`, `DecidableEq.lean`, and `DecidableTests.lean`.
