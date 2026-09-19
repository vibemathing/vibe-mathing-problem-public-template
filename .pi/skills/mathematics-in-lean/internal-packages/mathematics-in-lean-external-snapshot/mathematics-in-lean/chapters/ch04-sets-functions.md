# Chapter 4: Sets and Functions

## Core Idea
Lean sets are predicates, so most set proofs reduce to elementwise logic. Direct images add existential witnesses; preimages reduce by evaluation. Choose the representation that minimizes witness and coercion bookkeeping, and use extensionality/Galois connections to move between forms.

## Frameworks Introduced

- **Set extensionality pipeline**
  - When to use: proving `s = t`.
  - How: `ext x`; reduce the target to `x ∈ s ↔ x ∈ t`; unfold only the set operators needed; finish with logical tactics or focused `simp`.
  - For inclusions: introduce `x` and the membership hypothesis directly.

- **Image / preimage asymmetry**
  - When to use: transport of sets along a function.
  - How: remember `x ∈ f ⁻¹' u` reduces to `f x ∈ u`, while `y ∈ f '' s` means `∃ x ∈ s, f x = y`. If an image proof creates unnecessary witnesses, seek a preimage reformulation such as `f '' s ⊆ u ↔ s ⊆ f ⁻¹' u`.

- **Injective / surjective inverse construction**
  - When to use: constructing an inverse from a one-sided property.
  - How: under classical logic, choose a preimage when surjectivity supplies existence; define a default when none exists if a total function is required; package left/right inverse properties separately and derive injectivity/surjectivity from them.

- **Bijection by piecewise inverse (Schröder–Bernstein)**
  - When to use: injections `f : α → β` and `g : β → α` must yield a bijection without cardinal arithmetic.
  - How: define an iterated family of subsets of `α`, take their union `sbSet`, use `f` on that region and a selected inverse of `g` outside it, then prove right-inverse behavior, injectivity, and surjectivity in separate lemmas.
  - Failure mode: the final piecewise function is difficult to prove bijective if the invariant defining the region is not isolated in helper lemmas.

## Key Concepts

- **`Set α`**: definitionally a predicate `α → Prop`.
- **Subset**: `s ⊆ t` means every member of `s` is a member of `t`.
- **Indexed union/intersection**: set-level quantification encoded by `⋃` / `⋂` and membership lemmas.
- **`sUnion` / `sInter`**: union/intersection of a set of sets.
- **Image**: direct transport with an existential preimage witness.
- **Preimage**: inverse transport by function evaluation.
- **`InjOn`**: injectivity restricted to a set.
- **Range**: image of the entire domain.
- **`LeftInverse` / `RightInverse`**: algebraic properties that imply injectivity/surjectivity.
- **`invFun`**: classical inverse-selection utility for arbitrary functions.
- **Cantor diagonalization**: prove no map onto a powerset by constructing the set that disagrees on its own index.

## Mental Models

- A set operation is a logical connective in disguise: intersection is conjunction, union is disjunction, complement/difference use negation.
- Preimage is often the proof-friendly side because it carries no existential witness.
- `map`/`comap` patterns in later algebra and topology generalize the same direct/inverse transport relationship.
- For a complicated bijection, define the function after defining the region where each branch is valid; the set invariant is part of the algorithm.

## Anti-patterns

- **Unfolding `Set` implementation everywhere**: prefer membership/extensionality APIs; unfold only when Lean cannot see the logical structure.
- **Using direct image when the theorem is contravariant**: creates avoidable existential goals.
- **Assuming a chosen inverse is a genuine inverse everywhere**: `invFun` needs injectivity/surjectivity hypotheses at the point where left/right inverse behavior is claimed.
- **One monolithic Schröder–Bernstein proof**: mixes recursive set construction, choice, and bijection obligations, making case reasoning brittle.

## Code Examples

```lean
example {α β : Type*} (f : α → β) (s : Set α) (u : Set β) :
    f '' s ⊆ u ↔ s ⊆ f ⁻¹' u := by
  constructor
  · intro h x hx
    exact h ⟨x, hx, rfl⟩
  · rintro h y ⟨x, hx, rfl⟩
    exact h hx
```

- **What it demonstrates**: image/preimage adjunction proven by witness construction and destruction.

```lean
example {α β : Type*} (f : α → β) (u : Set β) (x : α) :
    x ∈ f ⁻¹' u ↔ f x ∈ u := Iff.rfl
```

- **What it demonstrates**: preimage membership reduces definitionally to membership after function application.

```lean
example {α : Type*} (s t : Set α) : s ∩ t = t ∩ s := by
  ext x
  constructor <;> rintro ⟨h1, h2⟩ <;> exact ⟨h2, h1⟩
```

- **What it demonstrates**: set equality becomes propositional commutativity after extensionality.

## Reference Table

| Task | Route |
|---|---|
| set equality | `ext x` → membership iff |
| subset | `intro x hx` → prove target membership |
| preimage membership | reduce to function value membership |
| image membership | `rcases` witness / `refine ⟨x,hx,rfl⟩` |
| monotonicity of image/preimage | transport membership; use existing monotone/Galois lemmas |
| inverse from surjection | classical choice; prove right inverse |
| inverse from injection | chosen/default inverse; prove left inverse on range |
| bijection from two injections | Schröder–Bernstein piecewise construction |

## Worked Example

For a goal involving `f '' (s ∩ t)`, first decide whether the desired statement needs injectivity. The inclusion `f '' (s ∩ t) ⊆ f '' s ∩ f '' t` is immediate by reusing the same witness. The reverse inclusion supplies potentially different witnesses for membership in `f '' s` and `f '' t`; injectivity is exactly what lets you identify them. This diagnosis tells you whether to search for an equality theorem, prove only an inclusion, or add an injectivity hypothesis.

The Schröder–Bernstein construction follows the same discipline at a larger scale: isolate a subset of `α` where the forward injection `f` is used, use a selected inverse of `g` on the complement, prove that the inverse branch is valid there, then establish injectivity and surjectivity as separate invariants.

## Key Takeaways

1. Reduce set statements to membership logic with extensionality.
2. Direct images introduce witnesses; preimages usually simplify definitionally.
3. Use left/right inverse abstractions to organize injective/surjective proofs.
4. Large bijection constructions need helper invariants before the final function is defined.
5. The image/preimage adjunction is a prototype for `map`/`comap` patterns throughout Mathlib.

## Connects To

- **Ch 3**: supplies the logical constructor rules used in all membership proofs.
- **Ch 8–10**: subobjects and morphisms reuse set-like coercions and map/comap Galois connections.
- **Ch 11**: filter `map`/`comap` generalize direct/preimage transport to generalized sets.
