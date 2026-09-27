# Chapter 8: Hierarchies

## Core Idea
Typeclass design is graph design. Separate operation data from laws, make inheritance paths coherent, ensure every instance-search parameter is determined, bundle morphisms with hom-classes when many morphism types share laws, and model subobjects through `SetLike` plus lattice structure.

## Frameworks Introduced

- **Data/law hierarchy separation**
  - When to use: designing reusable algebraic classes.
  - How: place raw operations near the bottom (`One`, `Mul`, etc.), laws in richer classes, and use `extends` so shared parent data is flattened/coherent.
  - Why: notation becomes available with minimal assumptions while stronger theorems request the exact laws they need.

- **Diamond audit**
  - When to use: multiple inheritance can synthesize the same parent instance through more than one path.
  - How: identify whether the shared parent contains data. If so, require the resulting operations to be definitionally equal or redesign the inheritance so richer structures forget to poorer ones along one coherent route. Proposition-only diamonds are much less dangerous because proofs are irrelevant.
  - Failure signal: identical notation elaborates to different operations depending on instance path.

- **Parameter-determinacy check**
  - When to use: a class has multiple type parameters such as scalar and carrier types.
  - How: every parent instance included in `extends` should mention enough parameters for typeclass search to recover them. If one result type is intended to be determined by inputs, use an `outParam` pattern similar to Mathlib hom classes.

- **Hom-class abstraction**
  - When to use: many bundled morphism types share a common “coerce to function + preserves operation” API.
  - How: give each bundle a function coercion, factor common laws into a `...HomClass`, inherit from `DFunLike` to get coherent coercion/injectivity behavior, and mark source/target types as output parameters only when synthesis can determine them.

- **SetLike subobject pattern**
  - When to use: submonoids, subgroups, subrings, submodules, or custom subobjects.
  - How: bundle a carrier set with closure laws; implement `SetLike` so membership/coercion/extensionality are uniform; inherit algebra on the subtype; equip the collection of subobjects with inf/sup/complete-lattice operations.

## Key Concepts

- **`class`**: structure intended for typeclass synthesis; fields may be instance-implicit.
- **`extends`**: inheritance mechanism that reuses parent fields and registers parent instances.
- **Bad diamond**: two non-definitionally-equal data instances for the same parent typeclass.
- **Proof irrelevance**: proofs of the same proposition do not create meaningful data conflicts.
- **`outParam`**: marks a typeclass parameter as output-like for synthesis.
- **`DFunLike`**: common basis for structures that coerce to dependent functions and are extensional by that function.
- **`SetLike`**: common basis for structures that coerce to sets and are extensional by membership.
- **Complete lattice of subobjects**: intersections give infima; generated closures give suprema.
- **Setoid / quotient**: equivalence relation plus quotient type used to build quotient algebra.

## Mental Models

- Instance search is a logic program over the class graph. Unknown parameters and alternate data paths directly affect elaboration.
- A class hierarchy should have forgetful maps from rich structures to poor structures; derived operations should not be independently reintroduced along competing paths.
- Bundled morphisms are values; hom classes are interfaces over families of such values.
- A subobject is simultaneously a set-like predicate and a structured subtype. The `SetLike` abstraction exposes both views coherently.

## Anti-patterns

- **Independent parent instances that re-create the same operation**: causes bad diamonds and non-definitional equality.
- **Parent class omits a relevant type parameter**: instance synthesis searches for an unconstrained type and may loop/fail.
- **Typeclass “is a morphism” predicate on arbitrary functions**: higher-order unification and instance search become fragile; bundle the morphism or use a hom class.
- **Hand-building separate APIs for every subobject kind**: misses the reusable `SetLike`/lattice pattern.
- **Quotienting without identifying the congruence relation**: operations may not be well-defined.

## Code Examples

```lean
class Dia (α : Type*) where
  dia : α → α → α

class OneD (α : Type*) where
  one : α

class DiaOneClass (α : Type*) extends Dia α, OneD α
```

- **What it demonstrates**: parent data is shared through inheritance rather than recreated ad hoc.

```lean
class MonoidHomClassLike (F M N : Type*) [Monoid M] [Monoid N]
    extends DFunLike F M (fun _ => N) where
  map_one : ∀ f : F, f 1 = 1
  map_mul : ∀ f : F, ∀ a b, f (a * b) = f a * f b
```

- **What it demonstrates**: abstract over several morphism bundles through their common function-like interface. Production code should use Mathlib's existing hom classes rather than redefining them.

## Reference Table

| Symptom / design need | Diagnosis / pattern |
|---|---|
| same operation reachable by two instance paths | bad-diamond audit |
| instance search leaves unknown scalar/index type | parent omitted parameter; add annotation or redesign class |
| many morphism bundles share lemmas | hom class + `DFunLike` |
| bundled subobject needs set coercion/ext | `SetLike` |
| subobjects need intersections/generated joins | complete lattice |
| quotient operation needs well-definedness | setoid/congruence + quotient lift |

## Worked Example

A module-like class depends on both a scalar ring `R` and an additive carrier `M`. If its inherited additive-group parent mentions only `M`, that is fine; if an intermediate parent is meant to determine both types but drops `R`, a later instance query can leave the scalar unknown. Diagnose the failure by writing the desired instance type explicitly and checking which parameters are constrained. Mathlib's hierarchy solves related problems by making rich structures forget data to poorer structures and by marking suitable morphism-class source/target parameters as output parameters.

For a custom submonoid, store `carrier : Set M`, `one_mem`, and `mul_mem`. Implement set-like coercion so `x ∈ N` works, give the subtype a monoid instance using closure, and prove extensionality by membership. Intersection is pointwise membership; arbitrary suprema require generated closure. This pattern scales to groups, rings, ideals, and submodules.

## Key Takeaways

1. Typeclass hierarchy design determines elaboration behavior.
2. Data-bearing diamonds must be definitionally coherent.
3. Unknown class parameters are a primary instance-synthesis failure mode.
4. Hom classes let generic theorems range over many bundled morphism types.
5. `SetLike` plus complete-lattice structure is the reusable architecture for subobjects.

## Connects To

- **Ch 7**: supplies the structure/instance building blocks.
- **Ch 9**: shows mature Mathlib hierarchies for homs, subgroups, ideals, and quotients.
- **Ch 10–12**: module, linear-map, topology, and continuous-map APIs rely on the same hierarchy principles.
