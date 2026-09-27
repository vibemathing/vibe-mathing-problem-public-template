# Chapter 5: Elementary Number Theory

## Core Idea
Number-theoretic formalization is driven by representation choices and induction strength. Expose divisibility witnesses and prime-factor facts explicitly, avoid accidental behavior of natural subtraction/division, and select ordinary, strong, or well-founded induction from the recursive dependency of the proof.

## Frameworks Introduced

- **Divisibility-to-witness reduction**
  - When to use: `m ∣ n`, gcd/coprime, prime-factor arguments.
  - How: use existing divisibility lemmas when possible; otherwise destruct `m ∣ n` into `n = m * k`. Track nonzero and order hypotheses before cancellation/division.
  - Failure mode: natural-number division and subtraction are totalized/truncated, so paper algebra can silently change meaning without divisibility/order conditions.

- **Prime obstruction proof**
  - When to use: irrational-root style contradictions.
  - How: assume a coprime numerator/denominator representation, show a prime divides a square, use primality to infer it divides the base, propagate the divisibility to both numerator and denominator, then contradict coprimality.
  - Alternative: use `Nat.factorization` and compare multiplicities modulo the exponent.

- **Induction-strength router**
  - Ordinary induction: recursive proof needs only predecessor case.
  - Strong induction: proof of `P n` may use `P m` for arbitrary `m < n`, e.g. prime factor existence.
  - Structural recursion: definition/theorem mirrors constructors of a custom inductive type.
  - Well-founded recursion: recursive call decreases under a custom measure or relation rather than the syntactic predecessor.

- **Finite-bounded contradiction**
  - When to use: proving infinitely many objects by assuming boundedness/finite enumeration.
  - How: turn a bounded predicate into a `Finset`, build a new number from the product/factorial of listed elements, extract a prime factor, and prove it lies outside the enumeration or has an impossible residue property.

## Key Concepts

- **`Nat.Prime`**: primality API with divisibility and factorization lemmas.
- **`Nat.Coprime`**: gcd-one relation used to formalize reduced fractions.
- **Strong induction**: `Nat.strong_induction_on` gives hypotheses for all smaller naturals.
- **Factorization**: finite-support map recording prime exponents of a natural number.
- **`Finset`**: bridge between a bounded/finite predicate and a product over all candidates.
- **Recursive theorem style**: theorem equations can mirror a recursive definition and call the theorem recursively.
- **`generalizing`**: strengthens an induction hypothesis by moving changing parameters back into the quantified statement.

## Mental Models

- Ask which quantities actually decrease in recursive calls; that relation determines the induction principle.
- Natural-number arithmetic is an ordered semiring with truncated subtraction. Rearrange paper equations before porting cancellation steps.
- A prime proof often splits into an algebraic layer (divisibility/factorization) and a logical layer (existence/contradiction/induction).
- If a proof says “take a prime divisor of a smaller factor,” strong induction is usually the intended Lean structure.

## Anti-patterns

- **Using ordinary induction when the recursive divisor can be any smaller number**: the induction hypothesis is too weak.
- **Dividing both sides in `Nat` without proving divisibility and positivity**: can yield goals that reflect floor division, not exact division.
- **Porting integer subtraction algebra directly to naturals**: `a - b` truncates at zero.
- **Keeping a changing auxiliary parameter fixed during induction**: later recursive call cannot instantiate the hypothesis; add `generalizing`.
- **Expanding factorization definitions**: use multiplicity lemmas and prime-specific facts instead.

## Code Examples

```lean
@[simp] def fib : ℕ → ℕ
  | 0 => 0
  | 1 => 1
  | n + 2 => fib n + fib (n + 1)
```

- **What it demonstrates**: recursive equations become simplification rules and determine the natural induction structure.

```lean
theorem fib_add (m n : ℕ) :
    fib (m + n + 1) = fib m * fib n + fib (m + 1) * fib (n + 1) := by
  induction n generalizing m with
  | zero => simp
  | succ n ih =>
    specialize ih (m + 1)
    simp [fib, ih]
    ring
```

- **What it demonstrates**: generalize a parameter that shifts in the recursive call.

```lean
example {p m : ℕ} (hp : p.Prime) (h : p ∣ m^2) : p ∣ m := by
  exact hp.dvd_of_dvd_pow h
```

- **What it demonstrates**: prefer prime API lemmas over rebuilding divisibility reasoning.

## Reference Table

| Recursion shape | Proof method |
|---|---|
| `P (n+1)` depends on `P n` | ordinary induction |
| `P n` depends on any `P m`, `m < n` | strong induction |
| object defined by constructors | structural induction |
| call decreases under measure `μ` | well-founded recursion/induction |
| finite/bounded contradiction | convert to `Finset`, product/factorial construction |
| prime multiplicity parity/exponent | `Nat.factorization` |

## Worked Example

To prove that every natural `n ≥ 2` has a prime divisor, strong-induct on `n`. If `n` is prime, choose `n`. Otherwise the negation of primality supplies a nontrivial divisor `m` with `2 ≤ m < n`. Apply the strong induction hypothesis to `m` to obtain a prime `p ∣ m`, then compose divisibility to get `p ∣ n`. The proof needs `P m` for a divisor that can be far below `n-1`, which is exactly why ordinary induction is poorly matched.

For infinitely many primes in a residue class, the same architecture gains a modular layer: assume all desired primes lie in a finite set, build a number from their product arranged to have the target residue, extract a prime factor with that residue by strong induction/modular case analysis, then show it both belongs to and cannot divide the listed product.

## Key Takeaways

1. Choose induction by the actual recursive dependency, not habit.
2. Track exact division, positivity, and order before manipulating naturals algebraically.
3. Use prime/factorization APIs as stable abstractions.
4. Generalize parameters that evolve through recursion.
5. Infinite-number-theory proofs often become finite-enumeration contradictions built from `Finset` products.

## Connects To

- **Ch 3**: existential witnesses and contradiction structure organize divisibility arguments.
- **Ch 6**: `Finset`, finite counting, and structural induction become first-class tools.
- **Ch 7–9**: Euclidean-domain and ring abstractions generalize many number-theoretic mechanisms.
