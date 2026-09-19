# Chapter 9: Groups and Rings

## Core Idea
Practical abstract algebra in Mathlib is organized around bundled morphisms, bundled subobjects, quotient universal properties, and hierarchy-aware theorem reuse. Many proofs become short once the objects are represented at the right abstraction level and the library's map/comap/ker/range APIs replace element chasing.

## Frameworks Introduced
- **Search the weaker structure first**
  - When to use: a theorem about groups/rings seems absent.
  - How: check whether the fact only needs a monoid/semigroup/additive analogue. Library declarations are often filed at the weakest assumptions.
- **Bundled homomorphism calculus**
  - When to use: composing or transporting structure-preserving maps.
  - How: use `MonoidHom` (`→*`), `AddMonoidHom` (`→+`), `RingHom` (`→+*`), equivalence counterparts, and `.comp`/composition operations. Use coercion to a function only at application sites.
- **Subobject lattice + map/comap**
  - When to use: subgroups/ideals and their images/preimages.
  - How: exploit `⊤`, `⊥`, `⊓`, `⊔`, `map`, `comap`, `ker`, `range`; prove equalities by extensionality. Prefer `comap` when membership reduces directly through a function.
- **Quotient via universal property**
  - When to use: defining homomorphisms out of a quotient group/ring.
  - How: state the compatibility condition, use quotient `lift`, then prove the induced map's properties. For groups, quotienting requires normality; for rings, quotients use ideals.
- **Isomorphism theorem pattern**
  - When to use: relate a morphism to quotient by its kernel and its range.
  - How: package kernel/range, build the canonical quotient map, then use the library equivalence (first-isomorphism style) rather than constructing representatives manually.
- **Algebra / polynomial evaluation**
  - When to use: a ring extension has a distinguished structure map and polynomials act by evaluation.
  - How: use `[Algebra R A]` and `algebraMap`; use `AlgHom` for structure-preserving maps over `R`; choose `eval`, `eval₂`, or `aeval` according to whether evaluation uses an element only, an arbitrary ring hom, or an algebra structure.

## Key Concepts
- **Monoid/group tactics**: `group` for multiplicative group identities; `abel` for additive commutative group identities.
- **`MulEquiv` / `RingEquiv`**: bundled bijective homomorphisms.
- **Subgroup**: bundled subset closed under group operations; inherits a group structure.
- **Normal subgroup**: requirement for quotient groups.
- **Ideal**: ring subobject suitable for quotient rings in the commutative setting used here.
- **Kernel / range**: canonical subobjects attached to a homomorphism.
- **Group action (`MulAction`)**: structured action with orbit/stabilizer APIs.
- **Units / `IsUnit`**: invertible ring elements.
- **`Algebra R A`**: an `R`-algebra structure with canonical structure map.
- **Polynomial `natDegree` vs `degree`**: natural degree is convenient but treats the zero polynomial specially; `degree` uses an extended order to represent that case faithfully.

## Mental Models
- Treat a homomorphism as an **object with algebra**, not a predicate on a function.
- Treat kernel/range as the **canonical subobjects for factorization questions**.
- View quotient theorems as **representative-free interfaces**: once compatibility is proved, the quotient handles equivalence classes.
- Think of group actions through the **action homomorphism into permutations**, making orbits/stabilizers conventional subgroup/quotient objects.
- Treat polynomial evaluation as a **universal construction specialized by the available ring/algebra map**.

## Anti-patterns
- **Elementwise quotient reasoning when a lift theorem exists**.
- **Using a ring theorem that secretly assumes commutativity**: inspect the exact typeclass requirements.
- **Expecting a quotient type to stay definitionally equal after replacing a normal subgroup by an equal one**: dependent quotient types may require an explicit equivalence.
- **Using coordinates/factors before trying kernel/range/map/comap**.
- **Confusing `degree` and `natDegree` at the zero polynomial**.

## Code Examples
```lean
example {G : Type*} [Group G] (a b : G) : a * b * b⁻¹ = a := by
  group
```
```lean
example {R : Type*} [CommRing R] (I J : Ideal R) : I * J ≤ I ⊓ J := by
  exact Ideal.mul_le_inf
```
- **What they demonstrate**: domain automation in groups and lattice-style ideal reasoning.

## Reference Tables
| Object | Bundled form | Common operations |
|---|---|---|
| monoid hom | `G →* H` | `comp`, `ker`, `range` |
| additive monoid hom | `A →+ B` | additive analogues |
| ring hom | `R →+* S` | `ker`, range, composition |
| monoid equivalence | `G ≃* H` | `.symm`, composition |
| ring equivalence | `R ≃+* S` | `.symm`, algebra transport |
| subgroup | `Subgroup G` | map/comap, normal quotient |
| ideal | `Ideal R` | map/comap, quotient, sum/product |
| algebra hom | `A →ₐ[R] B` | composition, polynomial evaluation |

## Section-by-Section Operational Map

**9.1 Monoids and groups.** Generic facts are frequently located at `Monoid` rather than `Group`. Bundled homomorphisms and equivalences provide composition, coercions, and structure-preservation theorems. Subgroups inherit group structure and form a complete lattice. `map`/`comap`, kernel, and range support isomorphism-style reasoning. The chapter surveys Lagrange/Sylow/cardinality APIs, permutations and cycles, free/presented groups through universal properties, and group actions. For actions, translate `g • x` to the homomorphism `G →* Equiv.Perm X`; orbit/stabilizer and quotient cardinality then become standard structured objects. Quotient groups require normal subgroups, and dependent quotient types may need explicit equivalences after subgroup equality rewrites.

**9.2 Rings.** The ring hierarchy distinguishes rings/commutative rings and semirings/commutative semirings; the `ring` tactic works in commutative semirings, so the tactic name is less restrictive than the class name suggests. Units and `IsUnit` package invertibility. Ring homomorphisms/equivalences mirror group morphisms. Ideals are the quotient-compatible subobjects for commutative rings; they form a lattice and a semiring-like structure, with ideal product below intersection. Chinese remainder reasoning is phrased through ideals, quotient rings, and coprimality. The algebra structure `[Algebra R A]` supplies `algebraMap`; `AlgHom` preserves that structure. Polynomial APIs distinguish univariate/multivariate, evaluation through an arbitrary ring hom versus an algebra structure, roots, and degree conventions.

## Failure Recovery Notes

- If a theorem name containing “group” is missing, search monoid-level declarations and additive/multiplicative aliases.
- If a quotient goal depends on proof objects/normality instances, use the library's quotient equivalences rather than rewriting dependent types by hand.
- If an ideal identity seems set-theoretic, check the lattice/ideal operation intended: sum is supremum, product is a stronger algebraic construction, intersection is infimum.
- If polynomial evaluation has too many arguments, decide first whether the coefficient map is identity (`eval`), arbitrary (`eval₂`), or supplied by an algebra (`aeval`).

## Worked Example
For a quotient group by a normal subgroup `N`, avoid choosing representatives to define a map. Start from a group homomorphism `f : G →* H` whose kernel contains `N`. The compatibility condition says equal cosets receive equal values. Use the quotient lift API to obtain `G ⧸ N →* H`; the induced map automatically respects multiplication. For the first isomorphism theorem, specialize `N` to `ker f` and target the bundled `range f`; Mathlib supplies the quotient–range equivalence. This route makes the universal property, not representative algebra, the proof's center.

## Key Takeaways
1. Search theorem APIs at the weakest parent structure.
2. Use bundled homomorphisms/equivalences as the default abstraction.
3. Use subobject lattices and map/comap instead of repeated elementwise proofs.
4. Use quotient lift/isomorphism APIs rather than representatives.
5. For actions, kernels, ranges, and quotients, move to the canonical bundled objects early.
6. Use `Algebra` and polynomial evaluation APIs to encode ring extensions uniformly.

## Connects To
- **Ch 8**: provides the hierarchy machinery these APIs rely on.
- **Ch 10**: linear maps/submodules/quotients repeat the same bundled patterns.
- **Ch 7**: Gaussian integers become useful precisely after entering the standard ring hierarchy.
