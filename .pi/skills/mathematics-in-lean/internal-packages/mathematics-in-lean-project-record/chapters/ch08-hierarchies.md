# Chapter 8: Hierarchies

## Core Idea
Mathlib's mathematical hierarchy works because structure inheritance, typeclass search, bundled morphisms, and bundled subobjects are designed so richer objects reuse poorer data definitionally. The chief engineering hazard is duplicating mathematical data along different inheritance paths and expecting propositional equality to be enough.

## Frameworks Introduced
- **Data class → law class hierarchy**
  - When to use: designing reusable overloaded mathematical structure.
  - How: put raw data (`one`, operation, scalar action) in small classes; extend them with law-carrying classes; expose parent fields as instances so notation/theorems resolve automatically.
- **`extends` for forgetful inheritance**
  - When to use: every object of a richer structure canonically has a poorer structure.
  - How: `extends Parent α`; ensure the parent data is the same data, not a separately reconstructed equivalent operation.
  - Why it works: typeclass inference often depends on definitional equality, especially around diamonds.
- **Bad-diamond diagnostic**
  - When to use: two paths through the hierarchy yield apparently identical operations but elaboration fails.
  - How: trace the instance paths. If both routes produce data (for example two scalar actions) separately, redesign the hierarchy so one route forgets existing data. Redundant fields with canonical defaults may be preferable to a duplicated construction.
- **Multi-parameter class discipline**
  - When to use: modules/actions/heterogeneous structures involve multiple carrier types.
  - How: only extend parent classes whose parameters expose all required types to inference; keep other structures as explicit instance parameters when necessary.
- **Bundled morphism + morphism class**
  - When to use: maps must carry structure-preservation proofs and generic theorems should work over several morphism types.
  - How: bundle the function with laws (`MonoidHom`, etc.); provide coercion to function; abstract generic behavior with a `*HomClass` built on `DFunLike`.
- **`outParam` for codomain/source inference**
  - When to use: a morphism class's source/target should be determined after the morphism type is known.
  - How: mark those parameters as output parameters in the class interface; avoid asking typeclass search to guess arbitrary domains from a bare function.
- **SetLike subobject hierarchy**
  - When to use: submonoids, subgroups, submodules, ideals, or similar “set + closure” structures.
  - How: bundle carrier set and closure data, coerce to a set/type, and use `SetLike`/subobject classes for generic membership/extensionality lemmas.

## Key Concepts
- **Instance-implicit argument**: bracketed argument synthesized by typeclass resolution.
- **Parent projection**: field taking a richer structure to a parent structure.
- **Definitional equality**: essential when multiple synthesis paths must compute to exactly the same data.
- **Diamond**: two hierarchy paths from one class to a common ancestor.
- **Forgetful inheritance**: rich-to-poor conversion drops laws/data but does not invent alternate operations.
- **Bundled morphism**: structure containing a function plus preservation laws.
- **`DFunLike`**: shared function-like interface for bundled morphisms.
- **`SetLike`**: shared set-like interface for bundled subobjects.
- **Subobject lattice**: infimum is intersection; supremum is generated closure, usually larger than union.
- **Quotient**: type obtained from an equivalence relation/setoid, with a universal mapping principle.

## Mental Models
- Typeclass inference is a **graph search over constructors and parent projections**. Design the graph, not only individual classes.
- A sound hierarchy should have **one canonical source for each piece of data**.
- Bundling a morphism turns a property about a function into a **first-class mathematical object** that can carry notation, composition, coercions, and instances.
- Subobjects are **structured sets**; quotient objects are **structured identifications**. Both deserve dedicated APIs rather than raw set/equivalence manipulation.

## Anti-patterns
- **Typeclass on a bare higher-order function**: search may require higher-order unification and become unreliable; bundle the map.
- **Duplicate operation instances through different parents**: even provably equal operations can fail to unify.
- **Extending a parent class that cannot reveal all type parameters**: inference can get stuck on metavariables.
- **Treating supremum of subobjects as ordinary union**: closure under operations must be restored.
- **Unfolding quotient implementation**: use the quotient constructor/lift/universal property.

## Code Examples
```lean
class One1 (α : Type*) where
  one : α

class Dia1 (α : Type*) where
  dia : α → α → α

class Semigroup1 (α : Type*) extends Dia1 α where
  dia_assoc : ∀ a b c : α, dia (dia a b) c = dia a (dia b c)
```
- **What it demonstrates**: a data class promoted to a law-carrying class through inheritance.

## Reference Tables
| Design problem | Preferred mechanism |
|---|---|
| richer structure canonically contains poorer | `extends` |
| bundled function-like structure | `DFunLike` |
| bundled subobject | `SetLike` |
| infer source/target after morphism type | `outParam` |
| generic theorem across morphism bundles | `*HomClass` |
| structured subset hierarchy | `Sub*Class` + coercions |
| quotient construction | `Setoid`/quotient + `lift` |

## Section-by-Section Operational Map

**8.1 Basics.** The chapter starts below groups/rings with tiny data classes to make instance synthesis visible. `class` differs from merely marking a structure with `[class]` because its own class parameter is instance-implicit in fields. `extends` simultaneously includes parent fields and installs the parent projection as an instance. As the hierarchy grows, the key invariant is that multiple inheritance paths to the same data class compute to the same thing. Multi-parameter structures such as modules require care: inherited classes should expose the type parameters needed to solve synthesis.

Natural/integer scalar multiplication is the canonical bad-diamond example. A semiring can obtain `nsmul` both from additive recursion and from multiplication by natural-number casts. Mathlib arranges canonical fields/defaults so these routes are definitionally compatible. The engineering lesson is stronger than “prove the operations equal”: instance resolution needs a unique computational path.

**8.2 Morphisms.** An unbundled predicate like “is a monoid homomorphism” is useful for local statements but unsuitable as the sole typeclass abstraction over arbitrary functions. Bundled `MonoidHom` values carry a function and laws, coerce to functions, and compose. To state generic lemmas over several bundled morphism types, Mathlib uses morphism classes with `DFunLike`; source/target can be `outParam`s so they are recovered from the morphism type rather than guessed independently. Some properties such as continuity/monotonicity remain intentionally unbundled because the property itself is the primary notion.

**8.3 Sub-objects.** `SetLike` plays for subobjects the role `DFunLike` plays for morphisms. A bundled subobject carries a set plus closure laws and coerces both to a set and to a subtype with inherited structure. The collection of subobjects forms a complete lattice; infimum is intersection while supremum is generated closure. Quotients complete the dual picture: bundle an equivalence relation/setoid, use quotient notation, then define maps by the universal lift.

## Failure Recovery Notes

- If `infer_instance` loops or selects an unexpected path, print/check the relevant parent projections and reduce the hierarchy to the smallest reproducer.
- If a class parameter stays as `?m`, supply the type that determines it; do not add arbitrary global instances to force progress.
- If a generic morphism theorem cannot coerce the morphism to a function, check that the morphism class extends the appropriate `DFunLike` interface.
- If subobject sup membership is hard, avoid assuming it is a union; use closure/induction lemmas associated with the generated supremum.

## Worked Example
Suppose a ring should also be an additive group and carry natural/integer scalar actions. If the ring hierarchy separately derives a `SMul Nat R` instance from multiplication while the additive-group route derives another by repeated addition, Lean may encounter two definitionally different values for the same class. The mathematical equality of those actions does not repair instance unification. The hierarchy fix is architectural: store the scalar action at an earlier canonical point (possibly as a redundant field with a default implementation) and make every richer structure inherit that exact data. This “bad diamond” lesson generalizes to any multi-parent class hierarchy.

## Key Takeaways
1. Hierarchy correctness depends on definitional identity of inherited data, not only mathematical equivalence.
2. Use `extends` when inheritance is truly forgetful.
3. Bundle morphisms and subobjects so they can participate cleanly in coercions and typeclasses.
4. Use `DFunLike`, `SetLike`, morphism classes, and `outParam` to make generic APIs scale.
5. Expect subobject suprema and quotients to use closure/universal constructions, not naive set operations.
6. When typeclass synthesis fails unexpectedly, inspect the instance graph before adding more local annotations.

## Connects To
- **Ch 7**: introduces classes, instances, and custom algebraic structures.
- **Ch 9**: uses the production Mathlib hierarchy for groups, rings, homomorphisms, subobjects, and quotients.
- **Ch 10–13**: the same patterns govern linear maps, topological structures, normed spaces, and measures.
