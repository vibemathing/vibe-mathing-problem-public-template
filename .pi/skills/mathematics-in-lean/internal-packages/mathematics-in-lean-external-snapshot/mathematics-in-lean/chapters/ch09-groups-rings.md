# Chapter 9: Groups and Rings

## Core Idea
Work through bundled morphisms, bundled subobjects, and universal properties. For quotients and isomorphism theorems, route through kernel/range, `map`/`comap`, and library `lift`/equivalence constructions instead of manipulating representatives manually.

## Frameworks Introduced

- **Bundled-hom workflow**
  - When to use: maps preserving monoid/group/ring operations.
  - How: use `G →* H`, `R →+* S`, equivalences such as `MulEquiv`/`RingEquiv`, and their `.comp`, kernel, range, map, and comap APIs. Coercions let the bundle act as a function while keeping the preservation laws attached.

- **Subobject lattice + Galois transport**
  - When to use: subgroups/subrings/ideals under a morphism.
  - How: express direct transport with `map`, inverse transport with `comap`; use monotonicity and map/comap adjunctions. Intersection/infimum is literal intersection; supremum is generated closure.

- **Quotient universal property**
  - Group quotient: require a normal subgroup; define maps out of the quotient when the normal subgroup lies in the kernel.
  - Ring quotient: quotient by an ideal; define ring maps by proving the ideal lies in the kernel.
  - Prefer supplied first-isomorphism and correspondence theorems to handcrafted quotient bijections.

- **Action-as-homomorphism**
  - When to use: a group acts on a type.
  - How: treat `MulAction` as a homomorphism into permutations; use orbit/stabilizer APIs and quotient/orbit constructions. This makes counting and equivalence arguments compositional.

- **Algebra / polynomial evaluation routing**
  - When to use: a ring `A` receives scalars from `R` and polynomials act on elements or endomorphisms.
  - How: use `Algebra R A`, `algebraMap`, `AlgHom`, and `aeval` for structure-preserving evaluation. Use `eval₂` when evaluation is relative to an arbitrary ring homomorphism.

## Key Concepts

- **Monoid vs group**: many multiplicative proofs need no inverses, so `Monoid` broadens reuse across groups and rings.
- **`MonoidHom`**: bundled multiplicative morphism.
- **Subgroup**: set-like bundled subobject whose subtype inherits group structure.
- **Normal subgroup**: compatibility condition for quotient groups.
- **Kernel / range**: canonical subobjects measuring injectivity/surjectivity.
- **Group action**: typeclass describing multiplicative action; induces permutation representation.
- **Ideal**: quotient-compatible ring subobject in the commutative-ring setting used here.
- **Chinese remainder map**: map from quotient by an intersection/infimum of ideals to a product of quotient rings.
- **Algebra**: coherent scalar embedding of one commutative semiring/ring into another.
- **Polynomial `X`, coefficients, degree/natDegree**: core polynomial API; zero polynomial is a special edge case for natural degree.

## Mental Models

- Morphism equality should be proved through extensionality on underlying functions, not by unpacking structure fields.
- Quotient maps are governed by what their kernels kill. Check the kernel/ideal/subgroup containment first.
- `map`/`comap` are algebraic analogues of image/preimage, with the same variance and Galois behavior.
- Isomorphic quotients may have different underlying types. Use an equivalence rather than seeking definitional equality.
- Algebraic evaluation is a homomorphism, so prove polynomial identities at the homomorphism level and inherit preservation automatically.

## Anti-patterns

- **Using raw function composition on bundled homomorphisms**: drops structure; use the bundle's `.comp`.
- **Trying to quotient a group by an arbitrary subgroup**: normality is the missing condition.
- **Rewriting quotient representatives by hand**: obscures well-definedness; use `lift`, `mk`, map, or an isomorphism theorem.
- **Assuming two quotient presentations are definitionally equal**: construct/use the canonical equivalence.
- **Using `natDegree` of the zero polynomial as if it encoded `-∞`**: handle zero separately or use the degree API suited to the theorem.

## Code Examples

```lean
variable {G H K : Type*} [Group G] [Group H] [Group K]

example (φ : G →* H) (ψ : H →* K) : G →* K :=
  ψ.comp φ
```

- **What it demonstrates**: structure-preserving composition remains bundled.

```lean
variable {R S : Type*} [CommRing R] [CommRing S]

example (φ : R →+* S) : Ideal R := RingHom.ker φ
```

- **What it demonstrates**: kernel is already the quotient-compatible subobject.

```lean
variable {R A : Type*} [CommRing R] [Ring A] [Algebra R A]

example (a : A) (P : R[X]) : A :=
  aeval a P
```

- **What it demonstrates**: polynomial evaluation is routed through the algebra structure.

## Reference Table

| Goal | Preferred abstraction |
|---|---|
| compose multiplicative maps | `MonoidHom.comp` |
| equality of bundled maps | extensionality on values |
| subgroup/ideal transport | `map` / `comap` |
| injectivity | kernel bottom/trivial |
| surjectivity | range top |
| map from quotient | `lift` + kernel containment |
| quotient isomorphism | first isomorphism theorem |
| group acts on set | `MulAction`, orbit/stabilizer |
| ring scalar extension | `Algebra`, `AlgHom` |
| polynomial acts on algebra element | `aeval` |

## Worked Example

For the Chinese remainder theorem, construct the product map by sending a class modulo the infimum/intersection of ideals to its classes modulo each ideal. Injectivity reduces to the fact that lying in every ideal means lying in their infimum. Surjectivity is the mathematical core: pairwise coprimality supplies coefficients/representatives that interpolate each component. Keep these obligations separated—map definition, kernel/injectivity, CRT construction/surjectivity—so quotient well-definedness is handled by the library rather than repeated in every coordinate.

For a quotient group homomorphism, start with `φ : G →* H` and normal `N`. Prove `N ≤ ker φ`; then the quotient lift gives `G ⧸ N →* H`. If `N = ker φ`, combine the lift with range information to obtain the first-isomorphism equivalence. This is more stable than choosing representatives and proving independence manually.

## Key Takeaways

1. Bundled homomorphisms preserve structure through composition and extensionality.
2. Subobject `map`/`comap` plus kernel/range form the routing backbone for homomorphism theorems.
3. Quotient proofs should use universal properties and canonical equivalences.
4. Group actions are homomorphisms into permutation groups, unlocking orbit/stabilizer APIs.
5. `Algebra` and `aeval` provide the correct abstraction for polynomial evaluation beyond the base ring.

## Connects To

- **Ch 8**: explains the hom-class and subobject architecture behind these APIs.
- **Ch 10**: repeats kernel/range/map/comap/quotient patterns for linear maps and submodules.
- **Ch 11**: `map`/`comap` Galois thinking reappears for filters and topologies.
