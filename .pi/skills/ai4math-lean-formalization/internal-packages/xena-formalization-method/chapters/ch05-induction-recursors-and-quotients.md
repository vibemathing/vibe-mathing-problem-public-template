# Chapter 5: Induction, Recursors, and Quotients

## Core Idea

Inductive types and quotients should be used through their eliminators. Constructors explain how to build data; recursors explain how to consume it. Quotient universal properties replace ad hoc “choose a representative and prove well-defined” arguments with a stable map-out interface.

## Inductive Types

Every inductive definition provides:

- constructors, the legal ways to create terms;
- an eliminator/recursor, the legal way to define functions or prove propositions by inspecting those constructors;
- computation rules describing what the recursor does on each constructor.

For naturals, recursion into data and induction into propositions are two views of the same generated eliminator. Similar logic applies to `False`, disjunctions, structures, and custom inductive data.

### Induction procedure

1. Identify the inductive object the theorem is structurally about.
2. Inspect its constructors and the induction hypotheses Lean will provide.
3. State the motive clearly enough that the induction hypothesis has useful strength.
4. Prove constructor cases using the API rather than representation accidents.
5. If a proposition about constructors is hard, consider whether a simple data-valued discriminator/predecessor defined by recursion exposes the needed fact.

This last move matters because a proof may need to enter the “data world” to distinguish constructors, even though the final result is a proposition.

## Equality as an Inductive Type

Lean's equality starts from reflexivity. Eliminating an equality proof gives substitution: if `a = b` and `P a`, transport to `P b`. Many familiar equality laws are derived through this eliminator. In practice, concrete types often provide stronger characterizations—pair/component equality, function extensionality, set extensionality—that are better interfaces than raw equality induction.

## Quotients

Do not assume a quotient element *is* an equivalence class set. Treat the quotient as an abstract object characterized by how maps out of it work.

Given `r` on `X` and `f : X → Y`:
1. prove `f x = f y` whenever `r x y`;
2. use the quotient lift/eliminator to obtain `X/r → Y`;
3. use quotient induction to prove properties of arbitrary quotient elements;
4. prefer domain-specific `lift`/`map` APIs for quotient groups, rings, localizations, and similar objects.

The traditional “well-definedness” proof is exactly the invariance proof required by this universal property.

## Universal Property Boundary

Universal properties are excellent for constructing and comparing maps *out of* an object. They may be insufficient for element-level or “map into” properties. The Xena discussions around tensor products, trace, and explicit models show a general technique: maintain more than one construction when different facts are exposed by different representations, and prove them equivalent.

## Anti-patterns

- Pattern matching on an opaque quotient representation.
- Choosing representatives before checking whether a lift already expresses the construction.
- Applying induction with a motive too weak to carry the needed hypothesis.
- Treating “defined by quotient” as an excuse to unfold foundational internals.

## Validation Checkpoint

For inductive objects, check that the chosen eliminator exposes exactly the cases and induction hypotheses the mathematical argument needs. For quotients, avoid reasoning about arbitrary representatives until you have written the invariance obligation explicitly. A map out of a quotient should be justified by a lift/universal property; a property of quotient elements may require quotient induction. Test the construction on constructors or representative classes and verify that changing representatives cannot change the result. If element-level facts remain inaccessible, consider a second concrete representation with a proved bridge.

## Key Takeaways

Construct with constructors; eliminate with recursors. For quotients, invariant maps are the primary interface. Reach for concrete models only when the theorem genuinely asks for information the universal property does not expose.

## Connects To

Representation bridges: [07](ch07-representation-specification-and-computation.md). API design: [06](ch06-definition-api-and-library-engineering.md). Equality: [04](ch04-equality-rewriting-and-normalization.md).
