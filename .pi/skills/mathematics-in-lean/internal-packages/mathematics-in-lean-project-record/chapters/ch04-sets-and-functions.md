# Chapter 4: Sets and Functions

## Core Idea
Mathlib sets are predicates on a fixed type, so set reasoning reduces to logic plus extensionality. Function images introduce existential witnesses, preimages reduce directly to membership, and bundled notions such as injective/surjective/inverse become reusable interfaces for larger constructions.

## Frameworks Introduced
- **Membership-first set proof**
  - When to use: subset, union, intersection, difference, indexed union/intersection.
  - How: `intro x`; unpack membership with logical tactics or `simp only`; reconstruct the desired membership. For equality, use `ext x` or two subset directions.
- **Prefer preimage when possible**
  - When to use: a statement compares `f '' s` and `f ⁻¹' t`.
  - How: exploit `f '' s ⊆ v ↔ s ⊆ f ⁻¹' v`. Preimage membership reduces to `f x ∈ v`; image membership requires an existential preimage.
- **Function-property interfaces**
  - When to use: injectivity, surjectivity, `InjOn`, range, left/right inverses.
  - How: unfold only enough to introduce the relevant objects; use composition properties rather than repeatedly expanding definitions.
- **Classical choice for partial inverses**
  - When to use: define an inverse-like function even when a preimage may not exist or may not be unique.
  - How: supply an inhabitant/default, use classical choice when a witness exists, then prove a specification theorem. Downstream proofs should use the specification, not reopen the choice construction.
- **Schröder–Bernstein decomposition**
  - When to use: injections exist both ways and a bijection must be constructed.
  - How: recursively generate the region where the forward injection is used; use the inverse of the other injection elsewhere; prove injectivity and surjectivity by case analysis on membership in that region.

## Key Concepts
- **`Set α`**: definitionally `α → Prop`.
- **Set-builder**: `{x | P x}` is a predicate/function.
- **Extensionality**: sets are equal iff they have identical membership.
- **Image**: `f '' s`; membership packages a source point plus membership/equality evidence.
- **Preimage**: `f ⁻¹' t`; membership reduces to membership of `f x`.
- **`range f`**: values attained by a function; closely related to image of `univ`.
- **`InjOn f s`**: injectivity restricted to a set.
- **Indexed unions/intersections**: membership exposes existential/universal indices.
- **`Classical.choose` / `invFun`**: choice-backed witness/inverse mechanisms.

## Mental Models
- Think of a set as a **predicate with extensional equality**.
- Think of image/preimage as a **Galois connection**: direct image is existential and forward; preimage is substitution and backward.
- Treat a choice-defined inverse as an **opaque implementation behind a specification theorem**.
- For large set constructions, prefer **membership algebra** (`simp`, extensionality, lattice laws) over manipulating set constructors syntactically.

## Anti-patterns
- **Unfolding every set definition manually**: it makes goals noisy; often `intro`, `rcases`, and definitional reduction suffice.
- **Using image when the equivalent preimage form is available**: image forces witness bookkeeping.
- **Reasoning from implementation of a chosen inverse**: use `inverse_spec`/`invFun` lemmas instead.
- **Ignoring type boundaries**: Lean sets are typed; membership between unrelated types is intentionally ill-formed.

## Code Examples
```lean
example {α : Type*} (s t : Set α) : s ∩ t = t ∩ s := by
  ext x
  simp [and_comm]
```
```lean
example {α β : Type*} (f : α → β) (s : Set α) : s ⊆ f ⁻¹' (f '' s) := by
  intro x hx
  exact ⟨x, hx, rfl⟩
```
- **What they demonstrate**: set equality via pointwise membership and image membership via explicit witness.

## Reference Tables
| Construction | Membership shape | Typical tactic |
|---|---|---|
| `x ∈ s ∩ t` | `x ∈ s ∧ x ∈ t` | `rcases` / `constructor` |
| `x ∈ s ∪ t` | `x ∈ s ∨ x ∈ t` | cases / `left` / `right` |
| `x ∈ s \ t` | `x ∈ s ∧ x ∉ t` | conjunction + negation |
| `y ∈ f '' s` | `∃ x ∈ s, f x = y` | `rcases` / `use` |
| `x ∈ f ⁻¹' t` | `f x ∈ t` | often definitional |
| `x ∈ ⋃ i, A i` | `∃ i, x ∈ A i` | witness/index case |
| `x ∈ ⋂ i, A i` | `∀ i, x ∈ A i` | `intro i` |

## Section-by-Section Operational Map

**4.1 Sets.** `simp only [subset_def, mem_inter_iff, ...]` is a useful learning tool, but definitional reduction often lets `intro` and pattern matching work without unfolding. Set difference is conjunction plus negated membership. Set equality is best attacked with `ext`; indexed unions/intersections turn into existential/universal index statements. Bounded quantifiers behave like nested membership + logical quantifiers. `sUnion`/`sInter` are unindexed versions of the same ideas.

**4.2 Functions.** Preimage preserves unions/intersections with little effort because it is definitionally substitution. Image preservation requires witnesses; injectivity is exactly what upgrades some image inclusions to equalities. `InjOn` and `range` are relativized versions of global function properties. Classical inverse definitions need `[Inhabited α]` or nonemptiness plus choice; prove a specification lemma once and consume it thereafter. Cantor's theorem is a diagonal set construction: define the set of indices not belonging to their assigned image and derive the self-membership contradiction.

**4.3 The Schröder-Bernstein Theorem.** The proof introduces recursive sets `S₀, S₁, ...`, their union `A`, and a piecewise function selecting `f` on `A` and `invFun g` elsewhere. The visual diagrams in the source motivate the nested “rings” moved by `g ∘ f`. In Lean the proof turns that picture into membership lemmas, indexed-union witnesses, a helper right-inverse fact, case analysis, and symmetry (`wlog`). The construction is a model for formalizing diagrammatic arguments: encode the regions explicitly before proving the global map properties.

## Failure Recovery Notes

- If `simp` on sets stops early, add the exact `mem_*` lemma for the constructor involved rather than unfolding `Set` itself.
- If an image goal generates too many existential variables, search for an equivalent subset/preimage theorem such as `image_subset_iff`.
- If choice/inverse proofs become entangled with default cases, state and use a conditional specification theorem so later proofs only reason where a preimage exists.
- If a long construction uses repeated expressions, `set name := expression with hname` can make the state readable, but remember rewriting may need the defining equation explicitly.

## Worked Example
Schröder–Bernstein illustrates how formalization benefits from isolating definitions. Given injections `f : α → β` and `g : β → α`, define a sequence of subsets of `α`: first the elements outside the image of `g`, then repeatedly apply `g ∘ f`. Let `A` be their union. Define `h x = f x` on `A` and `h x = invFun g x` outside `A`. Prove a right-inverse lemma for `invFun g` on the complement of `A`; use it as a black box in the injectivity and surjectivity proofs. The formal argument uses `by_cases`, indexed unions, images, `set` abbreviations, and a symmetry step (`wlog`). The important operational lesson is to extract helper specifications before attacking the final bijection.

## Key Takeaways
1. Reduce set goals to element membership early.
2. Prefer extensionality for equality and subset proofs for directional reasoning.
3. Move to preimages when they eliminate existential bookkeeping.
4. Treat injective/surjective/bijective properties as composable interfaces.
5. Hide classical choice behind specification lemmas.
6. For a delicate construction, prove the local helper facts that make the final structural proof short.

## Connects To
- **Ch 3**: all membership proofs reuse quantifier/connective tactics.
- **Ch 8–10**: subobjects generalize set reasoning through `SetLike`, map/comap, and lattices.
- **Ch 11**: filters and topologies reuse direct/pullback ideas in more abstract ordered structures.
