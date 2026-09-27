# Chapter 9: The Need for Arbitrarily High Types

**Source coverage**: §2.5, printed pp. 986-987.

## Core Idea
The order of types needed inside a proof cannot be bounded from the type orders appearing in the theorem alone. Any practical cap on generated type order can therefore improve search but risks losing completeness.

## Frameworks Introduced
- **Type-order bound diagnostic**
  - When to use: before adding a fixed maximum type order to a prover or instantiation generator.
  - How: classify the bound as a resource heuristic; document that it may exclude valid proofs even for low-order statements.
- **Consistency-speedup argument**
  - When to use: to understand why proof-internal types can outrun theorem syntax.
  - How: encode consistency statements for stronger arithmetic systems as low-order sentences; proving each consistency statement requires moving to higher logical strength, creating a sequence whose proofs require unbounded type orders.

## Key Concepts
- **type order**: the level induced by nested function/predicate types.
- **nth-order arithmetic**: arithmetic formalized with resources up to a given type order plus an infinity principle.
- **consistency statement**: a low-order syntactic statement asserting that a proof system does not derive contradiction.
- **Gödel's Second Theorem**: the barrier preventing a sufficiently strong consistent system from proving its own consistency.

## Mental Models
- Distinguish **input complexity** from **proof complexity**: the theorem's visible type order does not reveal the highest type order a proof may require.
- Treat type-order widening as **iterative deepening**: start low for efficiency, then raise the bound when search evidence warrants it.

## Anti-patterns
- **Fixing maximum type order to the theorem's maximum order**: this has no general completeness justification.
- **Reporting "unprovable" after bounded type-order search**: the correct result is "not found under this bound".
- **Letting type-order growth be completely unconstrained in practice**: logical completeness does not remove the need for resource management.

## Reference Tables

| Bound policy | Benefit | Risk |
|---|---|---|
| theorem-order only | very small search | incomplete in general |
| fixed global ceiling | predictable resources | can miss arbitrarily high-type proofs |
| iterative deepening | controlled search with recovery path | repeated work / scheduling complexity |
| no ceiling | avoids this incompleteness source | potentially explosive search |

## Worked Example
The source's proof sketch considers a family of low-order consistency statements for increasingly strong finite-order arithmetic systems. Each statement can be expressed in a low-order syntax, yet proving the consistency of the `n`th system requires reasoning in a stronger system. As `n` grows, the required proof machinery reaches unboundedly high type orders even though the statements themselves remain low-order.

## Key Takeaways
1. Never derive a completeness-safe type-order ceiling from the theorem syntax.
2. Label all practical type-order caps as heuristics.
3. Prefer iterative widening over a single hard bound when completeness matters.
4. Separate "search exhausted under bounds" from semantic unprovability.

## Connects To
- **Ch 8**: unification already requires bounded search in practice.
- **Ch 10**: expansion-term generation may introduce new higher-order variables.
- **Ch 14**: prover architecture must expose resource bounds and recovery strategies.
