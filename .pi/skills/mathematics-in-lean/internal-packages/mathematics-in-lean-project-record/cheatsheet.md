# Cheatsheet — Lean Proof Decisions

| If you see | Do first | Then |
|---|---|---|
| `a = b` from identities | `rw` or `calc` | `ring` / `simp` |
| equality of functions/sets/structures | `ext` | pointwise/membership/component proof |
| `∀ x, ...` or `A → B` | `intro` / `rintro` | use hypotheses with `apply`/`exact` |
| `∃ x, P x` | choose witness with `use` | prove property |
| hypothesis `∃ x, P x` | `rcases h with ⟨x, hx⟩` | continue with witness |
| `A ∧ B` / `A ↔ B` | `constructor` | solve both branches |
| `A ∨ B` | `left` or `right` | prove chosen branch |
| hypothesis `A ∨ B` | `rcases h with hA | hB` | prove both cases |
| negation | `intro` contradiction or `by_contra` | `push_neg` when nested |
| linear arithmetic | expose useful inequalities | `linarith` |
| concrete numerals | — | `norm_num` |
| Nat/Int order arithmetic | simplify structure first | `omega` |
| polynomial identity | check commutativity | `ring` / `noncomm_ring` |
| additive commutative group identity | — | `abel` |
| multiplicative group identity | — | `group` |
| fractions obscure identity | prove nonzero side conditions | `field_simp`; then `ring` |
| theorem almost matches | `convert theorem` | solve conversion equalities |
| unknown intermediate in transitivity | name it | `calc` or `trans y` |
| recursive definition | induct on recursive argument | generalize changing params |
| set image proof is awkward | seek preimage/comap form | unpack image only when needed |
| quotient construction | identify universal property | `lift`/`liftQ` |
| subobject transport | identify direction | `map` vs `comap` |
| limit/continuity | state as `Tendsto` | use filter algebra / bases |
| typeclass inference stuck | add carrier/base type | inspect inheritance/instances |

## Recovery rules

- `rw` misses: check direction → occurrence → `change`/`dsimp` → targeted `simp only` → `erw` last.
- `apply` creates `?m`: give the missing object/argument explicitly.
- Coercion noise: add a type ascription or `show` the intended target.
- `simp` does too much: replace with `simp only [...]`.
- Automation fails: extract a helper `have`; feed the exact residue back to automation.
- Proof uses too much structure: restate at a weaker class if the argument only uses weaker axioms.
- Hierarchy creates ambiguous operations: make inheritance forgetful; eliminate duplicate data paths.
- New Mathlib version breaks a name: preserve the mathematical route, re-search the current API.

## Defaults worth remembering

- Prefer `≤` orientation over `≥` when automation is sensitive.
- Prefer bundled morphisms (`→*`, `→+*`, `→+*`, `→ₗ`, `→L`) for reusable algebra.
- Prefer abstract basis/submodule/filter interfaces over coordinates or unfolded membership.
- Check empty/nonempty cases for `Finset.min'`, choice, quotients, and nontrivial filters.
- Treat `deriv`/`fderiv`/integral defaults as implementation conventions, not evidence that hypotheses are unnecessary.
