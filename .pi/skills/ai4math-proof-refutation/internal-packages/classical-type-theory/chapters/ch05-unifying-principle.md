# Chapter 5: The Unifying Principle

**Source coverage**: §2 introduction and §2.1, printed pp. 977-978.

## Core Idea
The Unifying Principle turns completeness of a proof procedure into a local closure argument. Define "not refutable by this procedure" as a property of finite sets of formulas, prove that property satisfies the abstract-consistency conditions, and consistency follows; any theorem's negation must therefore be refutable.

## Frameworks Introduced
- **Abstract consistency property**
  - When to use: to prove completeness of a search procedure for elementary type theory.
  - How: show closure under the logical decomposition/instantiation cases for negation, disjunction, universal quantification, and their negations, while excluding atomic contradictions.
- **Unifying Principle completeness pattern**
  - When to use: when a procedure `M` has operational refutation rules and you want a semantic completeness theorem.
  - How: let `T(S)` mean "`S` is not refutable by `M`"; verify abstract-consistency conditions; conclude `T(S)` implies consistency; apply the contrapositive to the negation of a theorem.

## Key Concepts
- **abstract consistency property**: a local closure property on finite sets of formulas designed to imply actual consistency.
- **cut elimination / Hauptsatz**: the proof-theoretic lineage that justifies restricting proof search without losing completeness.
- **completeness proof**: a proof that every valid theorem can be found/refuted by the search system under its rules.
- **elementary type theory J**: the main target system for the chapter's basic Unifying Principle.

## Mental Models
- Use the Unifying Principle as a **completeness adapter**: operational rules become semantic completeness once their failure-to-refute relation has the required closure behavior.
- Think **local closure before global completeness**: each logical constructor gets a small proof obligation.
- Treat extensionality as a separate layer: the basic principle is extended by later work for extensional systems.

## Anti-patterns
- **Claiming completeness from successful examples**: completeness needs a global argument such as the abstract-consistency closure proof.
- **Forgetting one polarity of a connective/quantifier**: the closure conditions distinguish positive and negated forms.
- **Using the elementary Unifying Principle unchanged for extensional systems**: extensionality requires the extended treatment referenced by the source.

## Reference Tables

| Goal-set shape | Closure obligation (conceptual) |
|---|---|
| contains `A` and `not A` for atomic `A` | property must fail |
| contains `not not A` | reduce to `A` |
| contains `A or B` | at least one branch preserves the property |
| contains `not (A or B)` | add both negated disjuncts |
| contains universal formula | every legal instance must preserve the property |
| contains negated universal | introduce a fresh witness/parameter instance |

## Worked Example
To prove a refutation procedure `M` complete, define `T(S)` as "`M` cannot refute finite set `S`". Suppose the operational rules of `M` guarantee all abstract-consistency closure clauses. If `A` is a theorem, `{not A}` is inconsistent. Were `M` unable to refute `{not A}`, then `T({not A})` would hold, and the Unifying Principle would imply `{not A}` is consistent, a contradiction. So `M` must refute `{not A}`.

## Key Takeaways
1. Separate the search algorithm from its completeness proof.
2. Encode "search failure" as a candidate abstract consistency property.
3. Prove local closure cases systematically.
4. Use the resulting theorem to convert inconsistency into guaranteed refutability.
5. Revisit the principle when adding extensionality or other logical strength.

## Connects To
- **Ch 6**: Miller's Expansion Proof Theorem plays a Herbrand-like role for proof certificates.
- **Ch 11**: constrained resolution can be analyzed as a complete higher-order search calculus.
- **Ch 12**: extensional systems require an extended unifying principle.
