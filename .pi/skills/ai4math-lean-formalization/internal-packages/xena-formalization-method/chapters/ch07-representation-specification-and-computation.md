# Chapter 7: Representation, Specification, Choice, and Computation

## Core Idea

The representation best for proving theorems may differ from the representation best for computation or for exposing a special property. Isolate representations behind specifications and proved bridges. Be explicit when moving from existence in `Prop` to concrete data.

## Specification versus implementation

Clients usually care that reals form the expected complete ordered field, that a quotient has its universal property, or that a completion satisfies a characterization. They rarely need the exact foundational construction. Prove reusable client results against such interfaces when practical.

Concrete models still matter when they expose information the abstract specification does not. A second model can make injectivity, computation, element structure, or a special theorem transparent. The correct response is often “keep both and prove the bridge,” rather than declaring one representation universally superior.

### Bridge checklist

For representations `A` and `B`:
1. define conversions in the needed directions;
2. prove round-trip/equivalence or the precise weaker relationship;
3. prove operations/relations commute with conversion;
4. transfer theorems through those compatibility lemmas;
5. keep clients from depending on raw implementation fields.

## Proof-friendly versus compute-friendly

Unary naturals support clean induction yet are unsuitable for huge kernel reduction. Efficient binary/computer representations may calculate well but be less pleasant for proofs. Use an efficient computation to obtain a result, then produce a certificate/proof connecting it to the mathematical representation.

“Computable” in mathematics does not imply “efficient by reduction in the prover.” A tactic can execute an optimized algorithm and return a proof which the kernel checks, separating performance from trust.

## Prop-to-data boundary

A proof that an object exists is logically different from carrying the object as data. Examples include:

- a proof that a finite basis exists versus an actual selected basis;
- a proof that a bijection exists versus a computable inverse;
- finite-dimensionality as a proposition versus a stored dimension/basis.

When a theorem needs a concrete witness from existence, decide explicitly:

- **Theorem-proving context:** use classical choice/noncomputable construction if acceptable, then prove the result is independent of the choice.
- **Executable context:** strengthen the input to include constructive data or an algorithm.

Do not promise executable code merely because existence and uniqueness were proved in `Prop`.

### Unique does not mean definitional

Truncations/subsingleton data can have at most one term propositionally while different terms remain non-definitionally equal. Expect small transport/equality obligations; use uniqueness theorems or conversion rather than relying on `rfl`/`exact`.

## Totalizing Partial Operations

Lean functions are total. Libraries may assign conventional values to division by zero, natural subtraction below zero, square roots outside an intended domain, and similar cases. Theorems recover mathematical meaning through preconditions. When a result fails at an edge case, inspect the theorem contract before blaming the operation's implementation.

## Anti-patterns

- Treating choice-produced data as computational.
- Using one representation for every theorem because it is “the definition.”
- Depending on the junk value of a totalized operation as if it were semantic mathematics.
- Replacing a stable interface theorem with reduction through implementation details.

## Validation Checkpoint

For every representation choice, label the required operations as proof-facing, computation-facing, or both. If a representation is excellent for one side and poor for the other, define a conversion and prove the facts clients need about that conversion before optimizing. When extracting data from an existence theorem, identify whether the construction crosses from `Prop` into data and whether classical choice makes it noncomputable. For totalized partial operations, audit every theorem for the domain condition under which the returned value has the intended mathematical meaning.

## Key Takeaways

Representations are tools. Specifications stabilize reasoning; concrete models expose extra facts; bridges let both coexist. Crossing from propositions to data and from partial mathematics to total functions must be visible in the API contract.

## Connects To

Equality/transport: [04](ch04-equality-rewriting-and-normalization.md). Trusted computation: [08](ch08-automation-reflection-and-trust.md). Definition engineering: [06](ch06-definition-api-and-library-engineering.md).
