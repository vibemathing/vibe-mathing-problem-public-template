# NNG4 Cheatsheet

## Route by goal shape

| Goal | First route |
|---|---|
| `X = X` | `rfl` |
| equality with known substitution | `rw [h]` / `rw [← h]` |
| universal recursive identity | induction on recursive argument |
| `P → Q` | `intro`; then rewrite/apply/exact |
| `a ≠ b` | `intro hEq`; derive `False` |
| `∃ x, P x` | `use witness` |
| `a ≤ b` | find `c` with `b = a + c`; `use c` |
| `P ∨ Q` | `left` / `right`; `cases` to consume |
| closed MyNat comparison | custom `decide` if available |

## Recursive equations

- `a + 0 = a`; `a + succ b = succ (a+b)`
- `a * 0 = 0`; `a * succ b = a*b + a`
- `a ^ 0 = 1`; `a ^ succ n = a^n * a`

**Induction heuristic:** choose the second addend, second factor, or exponent when these equations drive the proof.

## Rewrite recovery

1. wrong direction → add `←`;
2. wrong occurrence → explicit theorem arguments or `nth_rewrite`;
3. no match → inspect parentheses; reassociate;
4. near-match implication → rewrite first, then `apply`;
5. finished equality remains → `rfl` (NNG `rw` does not auto-close).

## Order (`≤`)

`a ≤ b` = `∃ c, b = a + c`.

- prove: `use c` → additive equality;
- use: `cases h with c hc` → witness + equality;
- transitive: add gaps;
- antisymmetric: opposite gaps + cancellation;
- tiny bound: constructor cases + disjunction.

## Multiplication safety

Before cancelling `a` from `a*b = a*c`, require `a ≠ 0`.

If IH is too specific in multiplication cancellation, redo induction with `generalizing` on the changing variable.

## Automation

- sum reordering only → `simp_add` after Algorithm World;
- closed concrete proposition → custom `decide` after `DecidableEq MyNat`;
- open theorem with variables → symbolic proof/induction.

## Game-specific warnings

- `rfl`, `rw`, `use`, `induction`, `cases`, and `decide` have custom NNG behavior.
- `xyzzy` is an axiom-backed final-boss escape hatch. Never present it as a derivation of FLT.
