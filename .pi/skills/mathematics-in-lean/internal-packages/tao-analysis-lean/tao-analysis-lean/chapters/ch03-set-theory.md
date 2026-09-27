# Chapter 3: Set Theory, Functions, and Cardinality

## Core Idea

Chapter 3 builds a Zermelo–Fraenkel-style set theory with atoms inside Lean, develops functions and cardinality on top of it, then connects the custom universe to Mathlib's `ZFSet`. The central skill is representation discipline: a custom `Set` is also an `Object`, membership is part of the `SetTheory` structure, and many familiar operations have custom counterparts whose types differ from Mathlib `Set α`.

## Frameworks Introduced

- **Axiomatic set-theory layer**: `SetTheory` packages membership, object/set coercion, extensionality, empty/pair/union/specification/replacement/infinity-style constructions and regularity-related behavior. Use these axioms through the local API rather than assuming Lean's native set semantics.
- **Paradox as consistency constraint**: Russell-style universal specification is shown incompatible with the system. Regularity yields no self-membership and no two-set membership cycles. When an attempted construction resembles an unrestricted “set of all objects satisfying P,” check the available bounded/specification axiom.
- **Function-as-set construction**: early `Function X Y` is a custom notion; the chapter provides conversion to ordinary Lean functions and evaluation lemmas. Prove graph/function facts in the custom representation, then convert when composition or Mathlib APIs are easier there.
- **Set-operation bridges**: image, preimage, Cartesian product, and cardinal notions gain lemmas connecting them to Mathlib images, subtypes, equivalences, or cardinals. Type mismatches commonly expose an implicit subtype/coercion boundary.
- **Deprecation through epilogue**: the custom Chapter 3 set theory is educational infrastructure. Later chapters prefer Mathlib sets and types; the epilogue shows how the axioms relate to `ZFSet`.

## Key Concepts

- **extensionality** — equality of custom sets is proved from membership equivalence; use the local `[ext]` support.
- **specification vs universal specification** — predicates select elements from an existing set; unrestricted universe-wide selection triggers Russell's paradox.
- **replacement** — builds images while preserving the custom set universe.
- **custom functions** — carry domain/codomain information and need explicit conversion for ordinary function combinators.
- **image/preimage** — source definitions may permit arguments broader than textbook subset hypotheses; inspect the theorem signature rather than importing an unstated side condition.
- **Cartesian products and ordered pairs** — custom encodings require projection and coercion lemmas.
- **equal cardinality / finite / infinite** — eventually correspond to equivalences/cardinal concepts in Mathlib.

## Operational Procedure

1. Identify whether the goal uses `Chapter3.SetTheory.Set`, its `Object`, or Mathlib `Set α`.
2. For custom-set equality, start with extensionality and reduce to membership.
3. For existence, select the weakest local constructor: empty, singleton/pair, union, specification, replacement, power-set, or infinity machinery.
4. For a custom `Function`, use the chapter's evaluation/conversion lemmas before applying ordinary function theorems.
5. For image/preimage/product goals, normalize subtype coercions and membership statements first. `Subtype.val` is often the missing bridge.
6. For cardinality, look for a bijection/equivalence formulation; avoid counting representatives manually.
7. In later chapters, honor the project's explicit retirement of this custom theory and use Mathlib's set/cardinal APIs.

## Failure Modes and Recovery

- **“Expected Set α, got SetTheory.Set”**: you crossed universes; find the chapter's bridge or remain inside the custom universe.
- **Image/preimage theorem nearly matches**: inspect whether the function argument is custom and whether domain/codomain membership is carried by subtypes.
- **An extensionality proof loops**: unfold only the relevant constructor, then compare membership propositions.
- **Choice-like existence seems unavailable**: Chapter 3 does not supply the later Chapter 8 choice framework; distinguish finite/specified choice from unrestricted classical choice.
- **A proof depends on the custom theory in Chapter 8+**: migrate to Mathlib equivalents unless the task is explicitly historical.

## Reference Table

| Need | Preferred representation |
|---|---|
| custom set equality | membership extensionality |
| custom function computation | `Function.eval` / conversion API |
| image/preimage reasoning | membership lemmas + Mathlib bridge |
| product reasoning | ordered-pair/projection membership |
| cardinal equality | bijection/equivalence |
| later project code | Mathlib `Set`, `Equiv`, `Cardinal` |

## Source Map

`Analysis/Section_3_1.lean` through `Section_3_6.lean` cover fundamentals, Russell's paradox, functions, image/preimage, Cartesian products, and cardinality. `Analysis/Section_3_epilogue.lean` connects the custom theory with `ZFSet` and marks the boundary before later Mathlib-centric work.

## Key Takeaways

1. Namespace and representation checks come before theorem search.
2. Extensionality plus membership is the normal route for custom-set equality.
3. Unrestricted comprehension is forbidden; use bounded specification/replacement constructions.
4. Custom functions and products expose subtype/coercion boundaries that must be handled explicitly.
5. Treat the epilogue as a migration point: later chapters should use Mathlib set theory.

## Connects To

- **Chapter 8** reintroduces cardinality/countability with Mathlib-native types after the Chapter 3 layer has been deprecated.
- **Measure Theory supplement** uses ordinary Mathlib sets and measurable-space infrastructure, not the Chapter 3 universe.
