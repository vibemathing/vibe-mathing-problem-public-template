# Chapter 9: Algorithm World — Package Repetition into Verified Computation

## Core Idea

Algorithm World asks when repeated manual reasoning should become an algorithm. It first automates associative/commutative addition normalization, then reconstructs Peano facts computationally with `pred` and `is_zero`, and finally builds recursive decidable equality so closed MyNat propositions can be discharged by a custom `decide` tactic.

## Frameworks Introduced

- **AC normalization as a simp set**
  - Prove `add_left_comm` from existing associativity/commutativity.
  - Use `simp only [add_left_comm, add_comm, add_assoc]` to normalize large sums without opening the whole simp database.
  - The game packages this controlled set as `simp_add`.

- **Define an observation, then prove constructor behavior**
  - `pred` maps `0` to the deliberate junk value `37` and `succ n` to `n`; only the successor equation matters for proving injectivity.
  - `is_zero` maps zero/successor to the propositions `True`/`False`; it supports `succ_ne_zero`.

- **Contrapositive constructor transport**
  - `succ_ne_succ` can be obtained from successor injectivity by contraposition: unequal predecessors imply unequal successors.

- **Recursive `DecidableEq MyNat`**
  - Equality of two naturals is decided by constructor cases: zero/zero succeeds, zero/succ and succ/zero fail by constructor separation, succ/succ recursively decides the predecessors and transports the result.

- **Kernel-checked decision**
  - Once `DecidableEq` exists, a closed proposition such as `20 + 20 = 40` or `2 + 2 ≠ 5` can be computed by the custom `decide` tactic, after its MyNat-specific simplification step.

## Key Concepts

- `add_left_comm`: `a + (b + c) = b + (a + c)`.
- `simp only`: automation constrained to an explicit lemma set.
- `simp_add`: NNG macro for the chosen associative/commutative addition simp set.
- `pred`: predecessor observation used to recover a value under `succ`.
- `is_zero`: zero discriminator used to prove constructor inequality.
- `succ_ne_zero` and `succ_ne_succ`: negative constructor facts.
- `instDecidableEq`: recursive equality decision instance for MyNat.
- custom `decide`: simplifies with the `MyNat_decide` simp attribute and invokes Lean's decision procedure.

## Procedure: decide whether to automate

1. If the goal is pedagogically about one rewrite/induction idea, keep the proof explicit.
2. If a large addition equality differs only by association and permutation, use the controlled AC set. Prefer `simp_add` after it is introduced.
3. If a proposition is **closed**—no arbitrary variables remain—and equality is decidable, consider `decide`.
4. If variables remain, return to symbolic lemmas; computation cannot prove a universally quantified identity just by evaluating one case.
5. If custom `decide` is unavailable, verify that `DecidableEq MyNat` and its imports have been established before blaming the arithmetic.

## Recursive equality design

A robust decision procedure follows the datatype, not arithmetic notation:

- `zero` vs `zero`: equal.
- `zero` vs `succ n`: unequal by `zero_ne_succ`.
- `succ m` vs `zero`: unequal by the symmetric constructor fact.
- `succ m` vs `succ n`: recursively decide `m = n`; if equal, lift by congruence; if unequal, use `succ_ne_succ`.

This mirrors the proof curriculum itself: constructor structure supplies the algorithm.

## Why custom tactic semantics matter

The active Algorithm L04 macro defines `simp_add` as `simp only [add_assoc, add_left_comm, add_comm]`; the support file `Game/Tactic/SimpAdd.lean` contains an equivalent internal AC normalizer built from separately reproved `_x` lemmas. `Game/Tactic/Decide.lean` performs an NNG-specific simplification before invoking `decide` because MyNat operations/numerals do not reduce exactly like ordinary `Nat`. A proof assistant agent should therefore distinguish “standard Lean tactic named X” from “NNG macro/tactic named X”.

## Anti-patterns

- **Unrestricted `simp` too early**: it can use lemmas outside the lesson and hide the algebraic structure.
- **Running `decide` on an open symbolic theorem**: decision procedures evaluate closed instances; they do not replace induction for universal identities.
- **Treating `pred` as subtraction**: it is a constructor observer with exactly the equations supplied by its definition.
- **Assuming automation is untrusted**: `DecidableEq`/`decide` still produce terms checked by Lean's kernel; the risk here is curriculum mismatch, not proof checking.

## Key Takeaways

1. Good automation packages a proven normal form rather than guessing.
2. Restricting the simp set preserves predictability and pedagogy.
3. Datatype eliminators such as `pred`/`is_zero` can reconstruct Peano axioms algorithmically.
4. Recursive decidable equality follows the constructors exactly.
5. Closed computation and symbolic theorem proving are different routes; choose based on free variables and available instances.

## Connects To

- **Ch 1–3** provide the equations packaged by automation.
- **Ch 5** provides constructor inequality reasoning.
- **Tactic semantics** documents the custom implementations and their deviations from ordinary Lean.

## Source anchors

`Game/Levels/Algorithm/L01add_left_comm.lean` through `L09decide2.lean`; `Game/MyNat/PeanoAxioms.lean`; `Game/MyNat/DecidableEq.lean`; `Game/Tactic/SimpAdd.lean`, `Decide.lean`, and `LabelAttr.lean`.
