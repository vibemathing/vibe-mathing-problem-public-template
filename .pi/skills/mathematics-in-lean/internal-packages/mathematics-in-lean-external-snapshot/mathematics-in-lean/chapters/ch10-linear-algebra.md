# Chapter 10: Linear Algebra

## Core Idea
Linear algebra in Mathlib is organized around bundled linear maps and submodules. Use span, map/comap, kernel/range, quotients, bases, and linear equivalences through their universal properties; move to coordinates and matrices only when coordinates are genuinely the right interface.

## Frameworks Introduced

- **Bundled linear-map workflow**
  - When to use: maps preserving addition and scalar multiplication.
  - How: work with `V →ₗ[K] W`; use `.map_add`, `.map_smul`, `.comp`, and linear equivalences `V ≃ₗ[K] W`. Keep the scalar field explicit when a carrier admits multiple scalar structures, such as complex vector spaces over `ℝ` and `ℂ`.
  - Failure signal: Lean cannot infer which scalar structure or composition you intend; add type annotations or use the bundled combinator rather than plain function composition.

- **Submodule universal-property router**
  - When to use: generated spaces, sums/intersections, images/preimages, kernel/range.
  - How: for span inclusions use `span_le`; use `span_induction` only when a pointwise induction over linear combinations is necessary. For a linear map, route injectivity through `ker = ⊥`, surjectivity through `range = ⊤`, and transport with `map`/`comap`.

- **Linear quotient workflow**
  - When to use: maps out of `V ⧸ E` or isomorphism/correspondence theorems.
  - How: use the quotient projection (`mkQ`-style API), quotient lift/map constructors, and the first-isomorphism equivalence between quotient-by-kernel and range. Let the library handle representative independence.

- **Endomorphism algebra**
  - When to use: polynomial identities in a linear endomorphism.
  - How: view `Module.End K V` as an algebra whose multiplication is composition. Evaluate polynomials with `aeval`; use minimal/characteristic polynomial theorems for kernels, eigenvalues, and Cayley-Hamilton.

- **Basis universal-property workflow**
  - When to use: coordinate expansion or defining a linear map from basis values.
  - How: a basis `Basis ι K V` supplies `repr : V ≃ₗ[K] ι →₀ K`; use `Basis.constr` to define maps from values on basis vectors and verify them with the basis-characterization lemmas such as `B.constr_basis`. Use coordinates only when a theorem is naturally coefficientwise.

- **Matrix / coordinate boundary**
  - When to use: finite-dimensional calculations, explicit matrix identities, determinant/trace, or a coordinate representation of a linear map.
  - How: distinguish matrix multiplication from pointwise multiplication on the underlying function type; use `Matrix.mulVec`/`vecMul`, `LinearMap.toMatrix`, and basis-change identities. Treat `#eval` as exploration, not proof.

- **Dimension router**
  - Finite-dimensional theorem: `Module.finrank K V` plus `[FiniteDimensional K V]` when a nontrivial dimension statement is intended.
  - General theorem: `Module.rank K V` with cardinals; be prepared to use `Cardinal.lift` across universe levels.

## Key Concepts

- **Module**: additive commutative group with scalar multiplication by a semiring/ring/field satisfying module laws.
- **Linear map**: bundled structure `V →ₗ[K] W`.
- **Linear equivalence**: invertible linear map `V ≃ₗ[K] W`.
- **Submodule**: set-like linear subspace; submodules form a complete lattice.
- **Span**: least submodule containing a set.
- **Kernel / range**: canonical submodules associated to a linear map.
- **Quotient module**: `V ⧸ E`, with maps defined by a quotient universal property.
- **Endomorphism algebra**: `Module.End K V`, multiplication equals composition.
- **Eigenspace / eigenvalue**: kernel-based spectral notions tied to minimal and characteristic polynomials.
- **Matrix**: definitionally a two-variable function, with specialized typeclass instances for matrix operations.
- **Basis**: linear equivalence with finitely supported coordinates.
- **`Finsupp`**: finitely supported functions; model coordinate vectors for possibly infinite bases.
- **`finrank` / `rank`**: natural/cardinal dimension notions.

## Mental Models

- Work coordinate-free by default. Convert to a basis/matrix when coordinates simplify the theorem, then return through the linear equivalence.
- `span`, quotient, and basis each come with a universal property; that property is usually the shortest way to construct or compare maps.
- Submodule `map`/`comap` is the same image/preimage pattern seen for sets and groups, now with linear closure supplied by the structure.
- A matrix type is intentionally distinct from the raw function type so typeclass inference selects matrix multiplication rather than pointwise multiplication.
- Totalized inverses/dimensions can return artificial values outside intended hypotheses; check invertibility or finite-dimensionality before drawing semantic conclusions.

## Anti-patterns

- **Expanding span into explicit finite linear combinations too early**: use `span_le`; reserve `span_induction` for genuine element-level proofs.
- **Proving quotient-map well-definedness by representatives each time**: use quotient linear-map constructors.
- **Assuming `finrank > 0 ↔ Nontrivial V` without finite-dimensionality**: `finrank` returns zero for infinite-dimensional spaces.
- **Confusing `m → n → R` pointwise multiplication with `Matrix m n R` multiplication**: preserve the `Matrix` type or use `Matrix.of`.
- **Using matrix inverse as evidence of invertibility**: inversion is totalized; provide an `Invertible` instance or a nonzero determinant hypothesis when applying inverse laws.
- **Forcing every proof into coordinates**: basis representations add finite-support and index-type obligations that abstract linear facts avoid.

## Code Examples

```lean
variable {K V W : Type*} [Field K]
  [AddCommGroup V] [Module K V]
  [AddCommGroup W] [Module K W]

example (φ : V →ₗ[K] W) : Function.Injective φ ↔ LinearMap.ker φ = ⊥ :=
  LinearMap.ker_eq_bot.symm
```

- **What it demonstrates**: route injectivity through a canonical submodule.

```lean
variable (B : Basis ι K V) {W : Type*} [AddCommGroup W] [Module K W]

example (u : ι → W) : V →ₗ[K] W :=
  B.constr K u
```

- **What it demonstrates**: define a linear map by specifying basis-vector images.

```lean
open Matrix

#eval !![1, 2; 3, 4] *ᵥ ![1, 1]
```

- **What it demonstrates**: matrix-vector multiplication has dedicated operations and notation; raw function pointwise multiplication is a different instance.

## Reference Table

| Task | Preferred API / route |
|---|---|
| linear map | `LinearMap`, `→ₗ` |
| linear isomorphism | `LinearEquiv`, `≃ₗ` |
| show generated set lies in subspace | `span_le` |
| reason by generators | `span_induction` |
| map/preimage of subspace | `Submodule.map` / `comap` |
| injective / surjective linear map | `ker = ⊥` / `range = ⊤` |
| map out of quotient | quotient lift/map API |
| polynomial in endomorphism | `aeval` on `Module.End` |
| define map from basis values | `Basis.constr` |
| prove linear maps equal | compare values on a basis / use linear-map extensionality |
| linear map as matrix | `LinearMap.toMatrix` with source/target bases |
| finite dimension | `Module.finrank` + `FiniteDimensional` |
| arbitrary dimension | `Module.rank`, `Cardinal.lift` |

## Worked Example

Suppose `φ : V →ₗ[K] W` and you need a first-isomorphism statement. First identify `ker φ` and `range φ`. The quotient projection sends `V` to `V ⧸ ker φ`; the quotient lift is well-defined because the kernel is exactly what `φ` annihilates. The resulting linear map into `range φ` is injective by construction and surjective by definition of range, producing a linear equivalence. Each step corresponds to a library abstraction; no representative-level quotient algebra is needed.

For determinant invariance under change of basis, represent an endomorphism in bases `B` and `B'`. The change-of-basis matrices come from `toMatrix` applied to identity maps. Use composition identities to relate the two representations, then determinant multiplicativity and the fact that the two change-of-basis matrices multiply to identity. This is preferable to expanding matrix entries or coordinates.

## Key Takeaways

1. Linear maps, submodules, and quotients should stay bundled.
2. Span and basis universal properties are primary construction APIs.
3. Kernel/range translate injectivity/surjectivity into submodule equalities.
4. Coordinates and matrices are boundary tools, not default representations.
5. `finrank` needs finite-dimensional context for its usual mathematical interpretation; general dimension uses cardinals and universe lifts.

## Connects To

- **Ch 8–9**: reuses hom/subobject/map/comap/quotient architecture.
- **Ch 11**: topology adds continuity to linear maps and uses similar lattice/Galois abstractions.
- **Ch 12**: continuous linear maps become derivatives between normed spaces.
