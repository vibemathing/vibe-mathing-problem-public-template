# Chapter 4: Quantifiers and Equality

## Core Idea
Universal quantification is dependent function space, existential quantification packages a witness with evidence, and equality provides substitution. Effective Lean equality proofs move from definitional equality to targeted rewriting, congruence, and explicit calculation chains.

## Frameworks Introduced
- **Quantifier-as-type reasoning**
  - When to use: goals or hypotheses contain `∀` or `∃`.
  - How: introduce a universally quantified variable like a function argument; construct an existential with a witness; eliminate it by unpacking witness and proof.
- **Equality substitution**
  - When to use: a known equality should change a dependent proposition or expression.
  - How: use equality elimination (`Eq.subst`, `▸`), rewriting, or congruence according to the target shape.
- **Calculational proof chain**
  - When to use: equality/transitive reasoning has meaningful intermediate expressions.
  - How: write a `calc` chain so each step has a local justification and Lean composes the relation transitively.
- **Context-directed proof language**
  - When to use: existing hypotheses should solve or feed a subgoal.
  - How: use `this`, anonymous `have`, `assumption`, or direct hypothesis notation when it makes dependency clear.

## Key Concepts
- **Universal quantifier** `∀ x : α, p x`: dependent function returning proof of `p x` for every `x`.
- **Existential quantifier** `∃ x : α, p x`: inductive proposition carrying a witness and proof.
- **Reflexivity** `Eq.refl` / `rfl`: establishes definitional equality.
- **Symmetry/transitivity**: reverse and compose equality proofs.
- **Substitution**: transport a proof/value across an equality.
- **`congrArg`**: equal inputs yield equal outputs under a function.
- **`congrFun`**: equal functions yield equal values at a shared argument.
- **`congr`**: broader congruence support.
- **`rw`**: tactic-level replacement using an equality.
- **`simp`**: repeated simplification via equations and reductions.
- **`calc`**: structured transitive proof notation.

## Mental Models
- Treat `∀` as **a function with an arbitrary input**; proving it means your construction cannot depend on a special case unless that case is justified from assumptions.
- Treat `∃` as **constructive output**: a witness is part of the proof, unlike mere external assurance that one exists.
- Use equality as a **transport license**: if `a = b`, propositions/types involving `a` can be transported to corresponding ones involving `b`.
- Think of `calc` as **making the semantic path visible** when automation would conceal the important intermediate forms.

## Anti-patterns
- **Expecting `rfl` for a merely mathematical identity**: `rfl` only sees definitional reduction.
- **Using a broad simplifier when one substitution is intended**: it can hide why the equality holds.
- **Over-specifying `Eq.subst` arguments** when higher-order unification cannot infer the predicate: use rewriting or `h ▸ e`, or state the predicate explicitly.
- **Eliminating an existential without preserving its witness relationship**: destructure it where the witness and proof remain in scope together.

## Code Examples
```lean
example (α : Type) (p : α → Prop) (h : ∀ x, p x) (a : α) : p a :=
  h a
```
- **What it demonstrates**: universal elimination is function application.

```lean
example (α : Type) (p : α → Prop) (a : α) (ha : p a) : ∃ x, p x := by
  exact ⟨a, ha⟩
```
- **What it demonstrates**: existential introduction includes a concrete witness.

```lean
example (f : Nat → Nat) (a b : Nat) (h : a = b) : f a = f b := by
  exact congrArg f h
```
- **What it demonstrates**: congruence transports equality through a function.

```lean
example (a b c : Nat) (h₁ : a = b) (h₂ : b = c) : a = c := by
  calc
    a = b := h₁
    _ = c := h₂
```
- **What it demonstrates**: explicit transitive chain.

## Reference Tables
| Equality situation | Tool | Why |
|---|---|---|
| expressions reduce to same term | `rfl` | definitional equality |
| replace known equals in target/hypothesis | `rw` | surgical substitution |
| normalize by many canonical equations | `simp` | iterative canonicalization |
| show equality after applying function | `congrArg` | congruence |
| show pointwise equality from equal functions | `congrFun` | function congruence |
| several meaningful steps | `calc` | readable transitive composition |
| dependent proof transport | `▸` / `Eq.subst` | equality elimination |

## Worked Example
Assume `h : a = b` and `ha : p a`; the target is `p b`.
1. The equality means `a` and `b` may be substituted in dependent propositions.
2. A concise proof is `h ▸ ha`: transport `ha` along `h`.
3. If elaboration cannot determine the dependent predicate in a more explicit `Eq.subst` expression, the `▸` syntax supplies better contextual information.
4. For a nondependent expression such as `f a = f b`, use `congrArg f h` or `rw [h]` instead; they communicate the simpler structure.

## Key Takeaways
1. `∀` and `∃` follow the same typed introduction/elimination discipline as propositional connectives.
2. `rfl` diagnoses definitional equality; failure does not mean the theorem is false.
3. Pick equality tools by intent: substitution, normalization, congruence, or transitive calculation.
4. Expected types and concise transport syntax can solve inference problems that verbose equality eliminators expose.
5. Existential proofs preserve witnesses, making them constructive evidence.

## Connects To
- **Ch 3**: extends propositions-as-types to quantification.
- **Ch 5**: `rw` and `simp` become central tactic workflows.
- **Ch 7**: equality itself is an inductive family whose eliminator underlies substitution.
- **Ch 11**: `conv` handles equality rewriting when ordinary occurrence targeting is insufficient.
- **Ch 12**: function/propositional extensionality broaden ways to establish equality.
