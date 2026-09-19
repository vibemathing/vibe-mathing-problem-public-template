# Active Curriculum Theorem / Goal Inventory

Exact signatures were extracted from the uploaded active level files. Anonymous level goals are labeled as such.

## 1. Tutorial World (`Tutorial`)

- **L01 — (anonymous level goal)**: `(x q : ℕ) : 37 * x + q = 37 * x + q`
  - introduces tactic(s): `rfl`
- **L02 — (anonymous level goal)**: `(x y : ℕ) (h : y = x + 7) : 2 * y = 2 * (x + 7)`
  - introduces tactic(s): `rw`
- **L03 — (anonymous level goal)**: `: 2 = succ (succ 0)`
  - introduces definition(s): `MyNat`
- **L04 — (anonymous level goal)**: `: 2 = succ (succ 0)`
- **L05 — (anonymous level goal)**: `(a b c : ℕ) : a + (b + 0) + (c + 0) = a + b + c`
  - introduces definition(s): `Add`
- **L06 — (anonymous level goal)**: `(a b c : ℕ) : a + (b + 0) + (c + 0) = a + b + c`
- **L07 — succ_eq_add_one**: `n : succ n = n + 1`
- **L08 — (anonymous level goal)**: `: (2 : ℕ) + 2 = 4`

## 2. Addition World (`Addition`)

- **L01 — zero_add**: `(n : ℕ) : 0 + n = n`
  - introduces tactic(s): `induction`
- **L02 — succ_add**: `(a b : ℕ) : succ a + b = succ (a + b)`
- **L03 — add_comm**: `(a b : ℕ) : a + b = b + a`
- **L04 — add_assoc**: `(a b c : ℕ) : a + b + c = a + (b + c)`
- **L05 — add_right_comm**: `(a b c : ℕ) : a + b + c = a + c + b`

## 3. Multiplication World (`Multiplication`)

- **L01 — mul_one**: `(m : ℕ) : m * 1 = m`
  - introduces definition(s): `Mul`
- **L02 — zero_mul**: `(m : ℕ) : 0 * m = 0`
- **L03 — succ_mul**: `(a b : ℕ) : succ a * b = a * b + b`
- **L04 — mul_comm**: `(a b : ℕ) : a * b = b * a`
- **L05 — one_mul**: `(m : ℕ): 1 * m = m`
- **L06 — two_mul**: `(m : ℕ): 2 * m = m + m`
- **L07 — mul_add**: `(a b c : ℕ) : a * (b + c) = a * b + a * c`
- **L08 — add_mul**: `(a b c : ℕ) : (a + b) * c = a * c + b * c`
- **L09 — mul_assoc**: `(a b c : ℕ) : (a * b) * c = a * (b * c)`

## 4. Power World (`Power`)

- **L01 — zero_pow_zero**: `: (0 : ℕ) ^ 0 = 1`
  - introduces definition(s): `Pow`
- **L02 — zero_pow_succ**: `(m : ℕ) : (0 : ℕ) ^ (succ m) = 0`
- **L03 — pow_one**: `(a : ℕ) : a ^ 1 = a`
- **L04 — one_pow**: `(m : ℕ) : (1 : ℕ) ^ m = 1`
- **L05 — pow_two**: `(a : ℕ) : a ^ 2 = a * a`
- **L06 — pow_add**: `(a m n : ℕ) : a ^ (m + n) = a ^ m * a ^ n`
- **L07 — mul_pow**: `(a b n : ℕ) : (a * b) ^ n = a ^ n * b ^ n`
- **L08 — pow_pow**: `(a m n : ℕ) : (a ^ m) ^ n = a ^ (m * n)`
- **L09 — add_sq**: `(a b : ℕ) : (a + b) ^ 2 = a ^ 2 + b ^ 2 + 2 * a * b`
- **L10 — (anonymous level goal)**: `(a b c n : ℕ) : (a + 1) ^ (n + 3) + (b + 1) ^ (n + 3) ≠ (c + 1) ^ (n + 3)`

## 5. Implication World (`Implication`)

- **L01 — (anonymous level goal)**: `(x y z : ℕ) (h1 : x + y = 37) (h2 : 3 * x + z = 42) : x + y = 37`
  - introduces tactic(s): `exact`
- **L02 — (anonymous level goal)**: `(x y : ℕ) (h : 0 + x = 0 + y + 2) : x = y + 2`
- **L03 — (anonymous level goal)**: `(x y : ℕ) (h1 : x = 37) (h2 : x = 37 → y = 42) : y = 42`
  - introduces tactic(s): `apply`
- **L04 — (anonymous level goal)**: `(x : ℕ) (h : x + 1 = 4) : x = 3`
- **L05 — (anonymous level goal)**: `(x : ℕ) (h : x + 1 = 4) : x = 3`
- **L06 — (anonymous level goal)**: `(x : ℕ) : x = 37 → x = 37`
  - introduces tactic(s): `intro`
- **L07 — (anonymous level goal)**: `(x y : ℕ) : x + 1 = y + 1 → x = y`
- **L08 — (anonymous level goal)**: `(x y : ℕ) (h1 : x = y) (h2 : x ≠ y) : False`
  - introduces definition(s): `Ne`
- **L09 — zero_ne_one**: `: (0 : ℕ) ≠ 1`
- **L10 — one_ne_zero**: `: (1 : ℕ) ≠ 0`
  - introduces tactic(s): `symm`
- **L11 — (anonymous level goal)**: `: succ (succ 0) + succ (succ 0) ≠ succ (succ (succ (succ (succ 0))))`

## 6. Advanced Addition World (`AdvAddition`)

- **L01 — add_right_cancel**: `(a b n : ℕ) : a + n = b + n → a = b`
- **L02 — add_left_cancel**: `(a b n : ℕ) : n + a = n + b → a = b`
- **L03 — add_left_eq_self**: `(x y : ℕ) : x + y = y → x = 0`
- **L04 — add_right_eq_self**: `(x y : ℕ) : x + y = x → y = 0`
- **L05 — add_right_eq_zero**: `(a b : ℕ) : a + b = 0 → a = 0`
  - introduces tactic(s): `cases`
- **L06 — add_left_eq_zero**: `(a b : ℕ) : a + b = 0 → b = 0`

## 7. ≤ World (`LessOrEqual`)

- **L01 — le_refl**: `(x : ℕ) : x ≤ x`
  - introduces tactic(s): `use`
  - introduces definition(s): `LE`
- **L02 — zero_le**: `(x : ℕ) : 0 ≤ x`
- **L03 — le_succ_self**: `(x : ℕ) : x ≤ succ x`
- **L04 — le_trans**: `(x y z : ℕ) (hxy : x ≤ y) (hyz : y ≤ z) : x ≤ z`
- **L05 — le_zero**: `(x : ℕ) (hx : x ≤ 0) : x = 0`
- **L06 — le_antisymm**: `(x y : ℕ) (hxy : x ≤ y) (hyx : y ≤ x) : x = y`
- **L07 — (anonymous level goal)**: `(x y : ℕ) (h : x = 37 ∨ y = 42) : y = 42 ∨ x = 37`
  - introduces tactic(s): `left right`
- **L08 — le_total**: `(x y : ℕ) : x ≤ y ∨ y ≤ x`
- **L09 — succ_le_succ**: `(x y : ℕ) (hx : succ x ≤ succ y) : x ≤ y`
- **L10 — le_one**: `(x : ℕ) (hx : x ≤ 1) : x = 0 ∨ x = 1`
- **L11 — le_two**: `(x : ℕ) (hx : x ≤ 2) : x = 0 ∨ x = 1 ∨ x = 2`

## 8. Advanced Multiplication World (`AdvMultiplication`)

- **L01 — mul_le_mul_right**: `(a b t : ℕ) (h : a ≤ b) : a * t ≤ b * t`
- **L02 — mul_left_ne_zero**: `(a b : ℕ) (h : a * b ≠ 0) : b ≠ 0`
- **L03 — eq_succ_of_ne_zero**: `(a : ℕ) (ha : a ≠ 0) : ∃ n, a = succ n`
  - introduces tactic(s): `tauto`
- **L04 — one_le_of_ne_zero**: `(a : ℕ) (ha : a ≠ 0) : 1 ≤ a`
- **L05 — le_mul_right**: `(a b : ℕ) (h : a * b ≠ 0) : a ≤ a * b`
- **L06 — mul_right_eq_one**: `(x y : ℕ) (h : x * y = 1) : x = 1`
  - introduces tactic(s): `«have»`
- **L07 — mul_ne_zero**: `(a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0) : a * b ≠ 0`
- **L08 — mul_eq_zero**: `(a b : ℕ) (h : a * b = 0) : a = 0 ∨ b = 0`
- **L09 — mul_left_cancel**: `(a b c : ℕ) (ha : a ≠ 0) (h : a * b = a * c) : b = c`
- **L10 — mul_right_eq_self**: `(a b : ℕ) (ha : a ≠ 0) (h : a * b = a) : b = 1`

## 9. Algorithm World (`Algorithm`)

- **L01 — add_left_comm**: `(a b c : ℕ) : a + (b + c) = b + (a + c)`
- **L02 — (anonymous level goal)**: `(a b c d : ℕ) : a + b + (c + d) = a + c + d + b`
- **L03 — (anonymous level goal)**: `(a b c d e f g h : ℕ) : (d + f) + (h + (a + c)) + (g + e + b) = a + b + c + d + e + f + g + h`
  - introduces tactic(s): `simp`
- **L04 — (anonymous level goal)**: `(a b c d e f g h : ℕ) : (d + f) + (h + (a + c)) + (g + e + b) = a + b + c + d + e + f + g + h`
  - introduces tactic(s): `simp_add`
- **L05 — (anonymous level goal)**: `(a b : ℕ) (h : succ a = succ b) : a = b`
- **L06 — succ_ne_zero**: `(a : ℕ) : succ a ≠ 0`
  - introduces tactic(s): `trivial`
- **L07 — succ_ne_succ**: `(m n : ℕ) (h : m ≠ n) : succ m ≠ succ n`
  - introduces tactic(s): `contrapose`
- **L08 — (anonymous level goal)**: `: (20 : ℕ) + 20 = 40`
  - introduces tactic(s): `decide`
- **L09 — (anonymous level goal)**: `: (2 : ℕ) + 2 ≠ 5`

## Primitive names to remember

- Addition: `add_zero`, `add_succ`.
- Multiplication: `mul_zero`, `mul_succ`.
- Power: `pow_zero`, `pow_succ`.
- Peano structure: `succ_inj`, `zero_ne_succ`.
- Numeral bridges: `one_eq_succ_zero`, `two_eq_succ_one`, `three_eq_succ_two`, `four_eq_succ_three`.

For proof strategy, read the matching chapter; this inventory is for exact-name/signature lookup.
