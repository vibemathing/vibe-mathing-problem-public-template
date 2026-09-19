# Chapter 7: Structures

## Core Idea
Lean structures bundle data and laws behind named projections; classes and instances make those bundles discoverable automatically. Good formalization defines a stable interface first, proves component-level simp/ext lemmas, and then registers the structure so generic Mathlib notation and theorems become available.

## Frameworks Introduced
- **Bundle data + invariants**
  - When to use: an object consists of fields with properties tying them together.
  - How: declare `structure`; name fields; include proof-valued fields for invariants; use constructor syntax to build values. Mark `@[ext]` when componentwise equality should characterize structure equality.
- **Namespace + projection API**
  - When to use: definitions/theorems belong to a custom structure.
  - How: keep them in the structure's namespace; exploit dot notation; record simple projection equations as `[simp]` lemmas.
- **Structure vs subtype/product/Sigma choice**
  - When to use: deciding representation.
  - How: a product bundles anonymous independent data; a subtype bundles data + proposition; a Sigma type has dependent data; a custom structure is preferable when named fields and a stable interface matter.
- **Class/instance registration**
  - When to use: generic notation and theorems should apply automatically.
  - How: declare reusable algebraic interface as `class`; register concrete implementations with `instance`; use `[Class α]` instance-implicit parameters in generic definitions/theorems.
- **Concrete-to-generic promotion**
  - When to use: after defining operations on a custom type.
  - How: register notation-level classes (`Add`, `Mul`, etc.) and then higher algebraic structures (`CommRing`, `EuclideanDomain`, ...). Once valid, reuse all generic library theorems instead of continuing componentwise.
- **Adapt proof to available machinery**
  - When to use: a textbook mathematical proof relies on infrastructure that is expensive to formalize.
  - How: compare the cost of formalizing that machinery with adapting the argument to existing integer/algebra APIs; choose the path that produces reusable infrastructure or the fastest robust proof for the current goal.

## Key Concepts
- **Constructor**: function that builds a structure value from its fields.
- **Projection**: accessor such as `p.x`; dot notation can also call namespaced functions.
- **Extensionality**: equality follows from equality of observable fields.
- **Subtype**: `{x : α // P x}` bundles a value with proof of a property.
- **Sigma type**: dependent pair where the second component is data indexed by the first.
- **Class**: structure whose values participate in typeclass inference.
- **Instance**: registered class value used by synthesis.
- **Coercion/notation class**: lightweight structure such as `Add α` that interprets syntax generically.
- **Noncomputable section**: allows classical/noncomputable definitions without pretending code generation is available.
- **Euclidean domain**: ring with quotient/remainder and a well-founded decreasing measure.

## Mental Models
- A structure is an **interface boundary**: downstream proofs should depend on projections/theorems, not representation.
- Typeclass inference is **dependency injection for mathematical structure**.
- Registering a stronger instance is a **capability unlock**: generic notation and theorems become available automatically.
- Build custom arithmetic types in layers: **raw representation → operations → simp/ext API → algebraic instance → higher theorems**.

## Anti-patterns
- **Pattern matching on structures everywhere**: it exposes representation and creates messy goals; projections are usually cleaner.
- **Duplicate notation definitions after a higher instance exists**: competing instance paths can create ambiguity.
- **Proving every ring axiom from scratch without component simp lemmas**: first teach `simp` how operations act on fields.
- **Keeping a custom type isolated from Mathlib's hierarchy**: once laws are proved, register the standard structure and reuse generic theorems.

## Code Examples
```lean
@[ext]
structure Point where
  x : R
  y : R
  z : R
```
```lean
instance : Add Point where
  add p q := ⟨p.x + q.x, p.y + q.y, p.z + q.z⟩
```
- **What they demonstrate**: a named record with extensionality and an operation registered for generic notation.

## Reference Tables
| Need | Representation |
|---|---|
| named fields + invariants | `structure` |
| operation/theory auto-discovery | `class` + `instance` |
| value + proposition | subtype |
| dependent pair of data | Sigma type |
| equality by fields | `@[ext]` + `ext` |
| routine projection reduction | `[simp]` lemmas |
| generic `+`, `*`, `0`, `1` | notation classes / algebraic hierarchy |

## Section-by-Section Operational Map

**7.1 Defining structures.** `@[ext]` generates extensionality support; named-field and anonymous-constructor syntax offer different readability trade-offs. Projection equations often hold by `rfl`. Pattern matching on structures is legal but can make rewritten goals harder to read. Invariant-bearing examples such as simplices show how a constructor mixes data fields with proof fields, often combining concise proof terms and tactic blocks. Parameterized structures and structures containing only propositions broaden the same mechanism. Subtypes and Sigma types are alternatives when their generic interfaces are sufficient.

**7.2 Algebraic structures.** An algebraic structure is just a structure parameterized by its carrier, but generic notation/reuse requires implicit arguments and typeclass inference. `class` marks a structure as searchable; `instance` registers concrete evidence. Lightweight notation classes (`Add`, `Mul`, `One`, etc.) are themselves typeclasses. Instance search can chain: a group instance yields a multiplication instance, and a concrete group instance completes the chain. This power makes duplicate competing instances dangerous.

**7.3 Building the Gaussian Integers.** The case study proceeds in layers: define the carrier; define operations; record projection simp lemmas; prove a `CommRing` instance componentwise; establish nontriviality; define norm/conjugation; engineer integer quotient/remainder with a nearest-remainder estimate; define Gaussian division/remainder; prove norm decreases; finally build `EuclideanDomain`. The final generic theorem `irreducible_iff_prime` is the reward for integrating the custom object into Mathlib's hierarchy.

## Failure Recovery Notes

- If `ext` does not fire, check whether an extensionality theorem was generated/registered and whether the visible components characterize equality.
- If notation picks the wrong operation, inspect existing instances and remove/reduce competing declarations rather than forcing local rewrites everywhere.
- If a structure literal has many fields, ask the editor for a skeleton and fill the essential fields; many inherited/default fields may be synthesized.
- If a large instance proof repeats component reductions, add `[simp]` projection lemmas first so the laws collapse uniformly.

## Worked Example
The Gaussian integers are represented as pairs of integers with real and imaginary parts. Define `0`, `1`, addition, negation, and multiplication componentwise, then prove `[simp]` lemmas for the projections. To build `CommRing GaussInt`, each axiom reduces via `ext` and `simp` to integer ring identities, closed by `ring`. Next define a norm and rounded quotient/remainder; prove the remainder measure decreases and multiplication does not decrease the measure improperly; package these into `EuclideanDomain GaussInt`. The payoff is immediate: generic Mathlib theorems about Euclidean domains, irreducibility, and primality apply to the custom type.

## Key Takeaways
1. Design a representation with a stable projection API.
2. Add extensionality and simplification lemmas before proving large structure instances.
3. Use class/instance only for structure meant to be synthesized automatically.
4. Promote a custom type into Mathlib's hierarchy as soon as its laws are established.
5. Keep implementation-specific arithmetic behind generic structure boundaries.
6. When formalization infrastructure is missing, consciously choose between building reusable machinery and adapting the proof to what already exists.

## Connects To
- **Ch 8**: scales classes into inheritance hierarchies and generic morphism/subobject APIs.
- **Ch 9**: uses the resulting algebraic hierarchy for groups, rings, ideals, quotients, and polynomials.
- **Ch 10–13**: the same bundling/typeclass architecture underlies modules, topologies, normed spaces, and measure structures.
