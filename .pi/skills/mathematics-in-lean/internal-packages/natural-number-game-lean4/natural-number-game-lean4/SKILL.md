---
name: natural-number-game-lean4
description: Operational proof-strategy skill distilled from "Natural Number Game 4" by Kevin Buzzard and Jon Eugster. Use for NNG4/MyNat Peano-arithmetic proofs, induction, rewriting, order witnesses, cancellation, nonzero multiplication, powers, logic, and the game's custom tactics. Avoid unrelated standard Lean/Mathlib tasks unless explicitly transferring these methods.
when_to_use: Natural Number Game, NNG4, MyNat, Peano naturals in Lean, zero_add or add_comm in NNG, mul_comm or pow_add in NNG, induction in NNG, rw in NNG, prove a ≤ b in NNG, prove a ≠ b in NNG, addition cancellation in MyNat, multiplication cancellation in MyNat, simp_add, NNG tactic semantics, Fermat final boss
allowed-tools: Read Grep
argument-hint: [goal, theorem, tactic, concept, or world]
---

# Natural Number Game 4 — Operational Proof Skill

**Creators:** Kevin Buzzard, Jon Eugster | **Game version:** 4.3 | **Active worlds:** 9 | **Active levels:** 79 | **Generated:** 2026-09-12

## How to Use This Skill

- Give a **goal/theorem** to route to the narrowest proof method and relevant world.
- Give a **tactic name** to load its NNG-specific semantics and failure modes.
- Give a **world or chapter** to inspect that method layer directly.
- Ask for a **level-valid solution** to restrict the answer to tools unlocked at that point; ask for **unrestricted Lean** to translate the method beyond the game.
- Ask what the skill covers to browse the Chapter Index and Topic Index below.

Use this skill to solve or explain proofs in the **NNG4 `MyNat` environment** and to transfer its proof patterns to closely related Peano-arithmetic exercises. Treat the exact goal state, available lemmas, and unlocked world as hard constraints.

## First: route the goal

1. **Identify the outer form.**
   - `lhs = rhs` → try exact/reflexive closure, rewriting, recursive induction, or algebraic normalization.
   - `P → Q` → `intro` when the implication is the goal; `apply` to reason backward or transform evidence forward.
   - `a ≠ b` → read it as `a = b → False`; introduce the equality and drive it to a Peano contradiction.
   - `∃ x, P x` or `a ≤ b` → construct a witness with `use`; unpack an existential hypothesis with `cases`.
   - `P ∨ Q` → choose `left`/`right`; use `cases` on a disjunction hypothesis.
2. **Identify recursion.** NNG addition, multiplication, and power recurse on their second argument: `add_succ`, `mul_succ`, and `pow_succ`. Prefer induction on the argument that these equations expose.
3. **Check side conditions before algebra.** Multiplication cancellation and related conclusions can fail at zero. Find or derive the required `a ≠ 0` first.
4. **Choose the least powerful available method.** Preserve the game's intended progression when the user is solving a level. Do not import later automation unless the user asks for unrestricted Lean.

## Core Frameworks & Mental Models

### Rewrite until the recursive equation can fire
Use `rw [h]` for forward substitution and `rw [← h]` for reverse substitution. If Lean rewrites the wrong occurrence, instantiate theorem arguments or use `nth_rewrite`. If no pattern matches, inspect parentheses and association before changing strategy.

The game deliberately makes `rw` and several other tactics weaker than familiar Mathlib defaults. Do not count on a rewrite finishing the goal automatically; add `rfl` when the remaining sides are identical.

### Induct where the definition recurses
For a theorem about `a + b`, `a * b`, or `a ^ b`, induction on `b` usually aligns the step case with `add_succ`, `mul_succ`, or `pow_succ`. In each case:

1. unfold the zero/successor equation;
2. rewrite with the induction hypothesis;
3. normalize the remaining algebra;
4. close with `rfl` when both sides coincide.

If the induction hypothesis is too specific because another variable changes in the recursive step, use `induction ... generalizing ...`. This is essential in the advanced multiplication cancellation pattern.

### Reuse a one-sided theorem by symmetry
Once commutativity is available, avoid a second induction when a mirror theorem can be obtained by commuting the operation. NNG uses this repeatedly: e.g. `one_mul` from `mul_one`, and `add_mul` from `mul_add` plus `mul_comm`.

### Turn logic into goal-state movement
- `exact h`: close an exactly matching goal.
- `apply h` on the goal: replace the goal by the premise needed for `h`.
- `apply h at hx`: push a hypothesis through an implication.
- `intro h`: assume the premise of a goal `P → Q`.
- For `a ≠ b`, introduce `a = b`, simplify/inject successors, then reach `zero_ne_succ` or another contradiction.

### Treat `≤` as data
NNG defines `a ≤ b` by existence of an additive gap: `∃ c, b = a + c`.

- To prove `a ≤ b`, choose the gap with `use c`, then prove the additive equation.
- To use `h : a ≤ b`, `cases h with c hc` to expose the witness and equality.
- Compose gaps for transitivity; combine opposite gaps with addition cancellation for antisymmetry; split constructors to prove totality and small-bound classifications.

### Guard multiplication by nonzero facts
When a product theorem needs cancellation or positivity-like reasoning, route through the nonzero layer:

`a ≠ 0` → `a = succ n` for some `n` → `1 ≤ a` and successor-based rewrites.

For a product, distinguish: product nonzero, one factor nonzero, product zero, and cancellable equality. Never cancel a common multiplicative factor until its nonzeroness is available.

### Use automation only when its preconditions hold
For addition expressions that differ only by association and order, use manual `rw` while learning, then `simp only [...]` or the game's `simp_add` when Algorithm World automation is allowed. For a **closed** MyNat equality/inequality, the custom `decide` route becomes available after recursive `DecidableEq MyNat` is constructed.

## Failure recovery

- **`rw` finds no match:** reverse the lemma, supply explicit arguments, reassociate, or target one occurrence with `nth_rewrite`.
- **Induction step stalls:** verify you inducted on the recursive argument; commute the operation if needed. If the IH is frozen at one dependent value, generalize that variable.
- **`apply` does not fit:** rewrite the goal or hypothesis into the theorem's exact premise/conclusion first.
- **`use` leaves a hard equality:** the witness is probably unhelpful; derive the additive gap from hypotheses or constructor cases.
- **Cancellation seems obvious but Lean blocks it:** check the theorem orientation and, for multiplication, the nonzero premise.
- **`decide` fails:** confirm the proposition is closed and the NNG `DecidableEq`/custom tactic is in scope; otherwise return to structural proof.
- **Final FLT level:** the source closes this level with the hidden `xyzzy` axiom/macro. Treat it as a game escape hatch. Do not describe it as a proof of Fermat's Last Theorem from the preceding lemmas.

## Chapter Index

| # | World | Key capabilities |
|---|---|---|
| [ch01](chapters/ch01-tutorial.md) | Tutorial | `rfl`, directed `rw`, numerals, occurrence control |
| [ch02](chapters/ch02-addition.md) | Addition | induction, `zero_add`, `succ_add`, commutativity, associativity |
| [ch03](chapters/ch03-multiplication.md) | Multiplication | recursive multiplication, distribution, symmetry reuse |
| [ch04](chapters/ch04-power.md) | Power | exponent induction, power identities, FLT/`xyzzy` boundary |
| [ch05](chapters/ch05-implication.md) | Implication | `exact`, `apply`, `intro`, negation, Peano contradictions |
| [ch06](chapters/ch06-advanced-addition.md) | Advanced Addition | cancellation, self-equality, zero-sum decomposition |
| [ch07](chapters/ch07-less-or-equal.md) | ≤ | existential witnesses, transitivity, antisymmetry, totality, bounds |
| [ch08](chapters/ch08-advanced-multiplication.md) | Advanced Multiplication | nonzero structure, zero products, generalized induction, cancellation |
| [ch09](chapters/ch09-algorithm.md) | Algorithm | `simp_add`, `pred`, `is_zero`, `DecidableEq`, custom `decide` |

## Topic Index

- **Addition cancellation** → ch06
- **Addition recursion / induction** → ch02
- **Associativity / commutativity normalization** → ch02, ch09
- **`apply`, `exact`, `intro`** → ch05
- **`cases`** → ch06, ch07, ch08
- **`decide` / `DecidableEq`** → ch09
- **Fermat final boss / `xyzzy`** → ch04
- **Induction variable choice** → ch02, ch03, ch04; generalized induction → ch08
- **`≤` / existential gap witnesses** → ch07
- **Multiplication cancellation / nonzero** → ch08
- **Multiplication / distributivity** → ch03
- **MyNat primitives / Peano foundations** → [foundations](references/foundations.md)
- **Negation / `False` / `zero_ne_succ` / `succ_inj`** → ch05
- **Numerals / `rfl` / `rw` / `nth_rewrite`** → ch01
- **Power identities** → ch04
- **`simp_add`** → ch09
- **Tactic implementation differences** → [tactic semantics](references/tactic-semantics.md)
- **Theorem names and exact active signatures** → [theorem inventory](references/theorem-inventory.md)

## Supporting Files

- [glossary.md](glossary.md) — key terms and tactic concepts
- [patterns.md](patterns.md) — reusable proof procedures and trade-offs
- [cheatsheet.md](cheatsheet.md) — compact routing rules and failure checks
- [foundations.md](references/foundations.md) — primitive MyNat definitions and axioms
- [tactic-semantics.md](references/tactic-semantics.md) — custom NNG tactic behavior
- [theorem-inventory.md](references/theorem-inventory.md) — all 79 active level statements
- [proof-routing.md](workflows/proof-routing.md) — goal-shape decision workflow
- [failure-recovery.md](workflows/failure-recovery.md) — diagnosis and fallback routes
- [provenance.md](references/provenance.md) — source/derivation classification
- [coverage.md](references/coverage.md) — source coverage audit
- [legacy-wip-roadmap.md](references/legacy-wip-roadmap.md) — inactive and planned material

## Scope & Limits

This skill models the uploaded NNG4 source tree (game version 4.3), including its active curriculum, foundational `MyNat` definitions, custom tactics, tests/configuration context, translations as coverage evidence, and legacy/WIP worlds. It can explain standard Lean analogues, but proof scripts meant for ordinary `Nat`/Mathlib may need adaptation because the game intentionally overrides or weakens several tactics and uses its own `MyNat`.

## SELF_CHECK

Before answering or proposing a script, verify:

- the user's actual goal and desired restriction level are clear;
- every theorem/tactic used is available at that point in the game;
- induction follows the recursive argument, or there is a deliberate reason not to;
- existential and disjunction goals are routed by their constructors;
- multiplication cancellation has a nonzero premise;
- no custom NNG tactic is being confused with stronger standard Lean behavior;
- the proof handles zero/successor edge cases and does not hide an impossible step;
- a failure route is available if the first method does not match the goal;
- any claim about the FLT level explicitly distinguishes `xyzzy` from genuine mathematics.
