# Patterns

## Outer-Constructor Proof
**When to use**: The target begins with `∀`, `→`, `∃`, `∧`, `↔`, `∨`, equality, or set equality.
**How**: Match the constructor/destructor: `intro`; `use`/`refine ⟨...⟩`; `constructor`; `left`/`right`; `rcases`; `rw`/`calc`; `ext`. Reinspect the new goals after every structural move.
**Trade-offs**: Deterministic and readable; can expose lower-level obligations that later need domain tactics.

## Normalize Then Automate
**When to use**: A solver should work mathematically but fails syntactically.
**How**: Use `change`/`dsimp` to expose definitions, focused `rw` to orient equalities, and small `simp only` sets. Then dispatch a suitable fragment: `ring`, `linarith`, `norm_num`, `omega`, `tauto`, or `group`/`abel`.
**Trade-offs**: Stable if normalization is targeted; broad `simp` can erase the structure needed for diagnosis.

## Structural-Lemma First
**When to use**: Proving a fact in a ring, lattice, group, module, order, metric, or topology abstraction.
**How**: Search for the law at the weakest sufficient typeclass; compose it with `calc`, `apply`, or dot notation. Add stronger concrete assumptions only when necessary.
**Trade-offs**: Produces reusable proofs; may require learning library naming and typeclass hierarchy.

## Witness / Destructure Cycle
**When to use**: Existentials, divisibility, images, surjectivity, fibers, nonempty objects.
**How**: On assumptions use `rcases`/`obtain` to expose witnesses. On goals use `use` or `refine ⟨w, ...⟩`. For equations that merely identify a witness, `rcases ... with ⟨rfl, ...⟩` can substitute immediately.
**Trade-offs**: Makes proof data explicit; witness choice determines later proof complexity.

## Induction Strength Selection
**When to use**: Recursive natural-number or inductive-data proof.
**How**: Use ordinary induction when recursive calls are on the immediate predecessor; strong induction when any smaller value may be needed; structural induction for lists/trees/formulas; well-founded recursion for custom decreasing measures. Generalize variables that change across recursive calls.
**Trade-offs**: A stronger induction hypothesis simplifies recursion but increases local context.

## Image-to-Preimage Switch
**When to use**: A set/morphism proof becomes clogged with existential witnesses from direct images.
**How**: Look for an adjunction/Galois statement such as image-subset iff subset-preimage, or use `comap`/preimage to move the condition to the source. Return to the image only after the core inclusion is proven.
**Trade-offs**: Removes witness bookkeeping; requires knowing the library's transport API.

## Finite Representation Switch
**When to use**: A proof mixes computable finite sets, finite types, cardinalities, and membership.
**How**: Use `Finset` for explicit operations/cardinality, `Fintype` for “all elements of a finite type,” and subtype coercions to turn a finite set into a finite type. Supply `DecidableEq` only where computation needs it.
**Trade-offs**: Choosing the wrong layer creates coercion and decidability noise.

## Universal-Property Construction
**When to use**: Defining maps from spans, quotients, free objects, basis-generated spaces, or quotient/induced structures.
**How**: Find the library constructor or `lift`; give values on generators/representatives; prove compatibility; use the corresponding extensionality/uniqueness theorem for equality of maps.
**Trade-offs**: Requires interface discovery but avoids representation-dependent proofs.

## Map / Comap + Kernel / Range
**When to use**: Subgroup, ideal, submodule, or linear-map inclusion/isomorphism problems.
**How**: Express transported subobjects with `map` and `comap`; reduce injectivity to kernel bottom and surjectivity to range top when available; use first-isomorphism/correspondence theorems instead of rebuilding quotient bijections.
**Trade-offs**: Highly compositional; coercions may need explicit type annotations.

## Typeclass Diagnosis
**When to use**: Instance synthesis fails or selects surprising operations.
**How**: Identify all carrier/scalar/index types; add type ascriptions/named arguments; check whether a parent class omits a type parameter; examine multiple inheritance for data-bearing diamonds; use `outParam`/hom-class patterns only when the result type is functionally determined.
**Trade-offs**: Fixes architecture rather than symptoms; can reveal that a custom hierarchy needs redesign.

## Filter Algebra
**When to use**: Limits, eventual properties, restricted convergence, continuity, cluster points.
**How**: Recast convergence as `Tendsto`; use `map`, `comap`, `inf`, products, and order lemmas. Combine eventual facts with `.and`, `.mono`, or `filter_upwards`. Use a `HasBasis` theorem only when concrete epsilon/ball inequalities are required.
**Trade-offs**: Initial abstraction cost; eliminates large families of near-duplicate epsilon arguments.

## Evidence-Bearing Analysis
**When to use**: Derivatives or integrals whose totalized functions can hide failure cases.
**How**: Prove `HasDerivAt`/`HasFDerivAt`/`DifferentiableAt` or `Integrable`/measurability first. Derive equations for `deriv`, `fderiv`, or integrals afterward. For local domains use Within/AtFilter variants.
**Trade-offs**: More premises up front; prevents proofs that succeed only through default-zero conventions.
