# Chapter 7: Structures

## Core Idea
Use structures to bundle mathematical data with named fields and invariants, then expose a small API of constructors, projections, extensionality lemmas, and instances. For new algebraic objects, define operations componentwise and prove the standard structure through extensionality rather than unfolding users of the object.

## Frameworks Introduced

- **Structure interface design**
  - When to use: an object consists of multiple data fields, possibly with proofs depending on those fields.
  - How: declare the structure, give meaningful field names, add `@[ext]` when equality should be determined by data fields, and write constructors/helpers that preserve invariants.
  - Benefit: callers depend on projections and invariants instead of representation details.

- **Structure versus subtype/product/Sigma**
  - Structure: best when fields have semantic names and the object deserves its own API.
  - Subtype: best for one carrier value plus a property.
  - Product: best for two unrelated anonymous components.
  - Sigma: best for a dependent pair where the second component's type depends on the first.

- **Operation-instance construction**
  - When to use: make a custom type participate in Mathlib notation and algebraic APIs.
  - How: define `Zero`, `One`, `Add`, `Neg`, `Mul` operations; prove projection simplification lemmas; install a higher structure such as `CommRing` by extensionality and componentwise simplification.

- **Euclidean-domain implementation by measure**
  - When to use: a custom ring such as Gaussian integers supports division with remainder.
  - How: define norm/conjugation/quotient/remainder; prove the remainder norm strictly decreases; supply a well-founded relation based on a natural-valued measure; then use the generic `EuclideanDomain` API.

## Key Concepts

- **Projection**: field accessor automatically generated for a structure.
- **Structure literal**: construct with named fields, useful when many fields/proofs are involved.
- **Extensionality theorem**: equality of structures reduced to equality of relevant fields.
- **Instance**: registered structure value synthesized by typeclass inference.
- **Notation class**: small class such as `Add`, `Mul`, `Zero`, `One` supplying syntax before stronger laws are assumed.
- **Invariant field**: proposition stored alongside data, e.g. a simplex coordinate-sum condition.
- **Gaussian integer**: pair of integers with complex-like arithmetic, used as a worked algebraic construction.
- **Well-founded measure**: natural-valued quantity that decreases on recursive steps and justifies termination.

## Mental Models

- A structure is a public interface plus a representation. Once instances are installed, downstream proofs should use the interface.
- Build algebraic structures bottom-up: operations first, simplification lemmas next, laws last.
- Extensionality is the standard way to prove equality of structured values; it prevents proof scripts from depending on constructor layout.
- The cost of formalizing a new object is often front-loaded; once the standard typeclasses are satisfied, a large generic library becomes available.

## Anti-patterns

- **Encoding semantically rich records as nested products**: projection-heavy code becomes hard to read and refactor.
- **Installing strong instances before component lemmas simplify**: structure-law proofs become verbose.
- **Reimplementing generic algebra theorems for the new type**: prove the typeclass once and inherit the library.
- **Choosing a Euclidean algorithm without a proven decreasing measure**: termination and `mod_lt` obligations become disconnected from the mathematical norm.

## Code Examples

```lean
@[ext] structure Point where
  x : ℝ
  y : ℝ

namespace Point

def add (a b : Point) : Point := ⟨a.x + b.x, a.y + b.y⟩

end Point
```

- **What it demonstrates**: named fields plus an extensionality interface.

```lean
@[ext] structure GaussInt where
  re : ℤ
  im : ℤ

instance : Add GaussInt where
  add x y := ⟨x.re + y.re, x.im + y.im⟩
```

- **What it demonstrates**: separate operation data from later algebraic laws.

```lean
example (x y : GaussInt) : (x + y).re = x.re + y.re := rfl
```

- **What it demonstrates**: projection simplification should be definitionally or simplifier-friendly.

## Reference Table

| Object shape | Prefer |
|---|---|
| named independent fields | `structure` |
| value + proposition | subtype `{x // P x}` |
| anonymous pair | product `α × β` |
| second component depends on first | sigma `Σ a, β a` |
| custom algebraic object | structure + operation instances + law instance |
| equality of structures | extensionality |
| recursive division algorithm | norm/measure + well-founded relation |

## Worked Example

For Gaussian integers, represent `a + bi` by integer fields `re` and `im`. Define zero, one, addition, negation, and multiplication componentwise. Prove `[simp]` lemmas for each projection. A commutative-ring instance then reduces every law to two integer equalities; `ext <;> simp <;> ring`-style proofs become available. For Euclidean division, use the norm `re^2 + im^2`, choose integer approximations to the real/complex quotient, define the remainder, and prove its norm is smaller. Once the Euclidean-domain instance is installed, generic irreducible/prime and gcd machinery applies to the custom type.

## Key Takeaways

1. Structures are abstraction boundaries; downstream code should use their API.
2. Install notation-level operation data before proving stronger algebraic laws.
3. Extensionality plus componentwise simplification is the default structured-equality method.
4. New algebraic structures unlock generic Mathlib only after coherent instances are supplied.
5. Recursive algebraic algorithms need an explicit mathematical decrease measure.

## Connects To

- **Ch 8**: turns individual structure instances into carefully designed inheritance hierarchies.
- **Ch 9**: uses bundled morphisms/subobjects/quotients built on these structural ideas.
- **Ch 10–12**: linear and topological structures compose through typeclasses.
