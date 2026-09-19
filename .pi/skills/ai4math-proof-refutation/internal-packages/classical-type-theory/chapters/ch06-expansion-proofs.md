# Chapter 6: Expansion Proofs

**Source coverage**: §2.2, printed pp. 978-982.

## Core Idea
An expansion proof is a compact certificate recording the quantifier instantiations that expose an underlying propositional tautology. It separates the essential instantiation/dependency structure from the surface sequence of proof steps.

## Frameworks Introduced
- **Expansion tree**
  - When to use: to represent a candidate higher-order proof or guide proof search.
  - How: start from the theorem as the shallow formula; expansion nodes receive finitely many instantiation terms; selection nodes receive one fresh selected parameter; definition nodes may unfold abbreviations.
- **Deep formula test**
  - When to use: to decide whether a completed expansion tree certifies the theorem.
  - How: replace an expansion node by the disjunction of the deep formulas of its instantiated branches (dually, conjunction for refutation trees); require the resulting deep formula to be a propositional tautology.
- **Dependency condition**
  - When to use: whenever expansion terms can contain parameters introduced under other quantifiers.
  - How: define dependencies through selected parameters occurring free in later expansion terms; require the transitive closure to be acyclic.
- **Dual expansion proof**
  - When to use: in refutational mode.
  - How: reverse the existential/universal expansion roles and require a contradictory deep formula plus the same dependency discipline.

## Key Concepts
- **shallow formula**: the formula represented directly by an expansion tree/node.
- **deep formula**: the quantifier-instantiated propositional core represented by the tree.
- **expansion node**: an essentially existential quantifier occurrence with one or more expansion terms.
- **selection node**: an essentially universal occurrence using a fresh selected parameter.
- **expansion term**: a term chosen to instantiate an expansion variable.
- **dependency relation**: the acyclicity constraint preventing circular witness dependence.
- **definition node**: a node recording selective unfolding of an abbreviation.

## Mental Models
- Think of an expansion proof as **higher-order Herbrand data**: the proof is in the right instances plus a propositional certificate.
- Use the dependency graph as an **occurs-check for witness chronology**: later choices may depend on earlier selected parameters, but cycles are forbidden.
- Treat definition nodes as **controlled abstraction boundaries** rather than preprocessing everything away.

## Anti-patterns
- **Calling a tautological deep formula sufficient**: the dependency relation must also be acyclic.
- **Applying a substitution locally to one occurrence**: free variables in expansion terms must be substituted uniformly across the tree.
- **Assuming all Skolemization can happen before search**: higher-order expansion terms may introduce fresh quantifiers later.

## Reference Tables

| Tree element | Proof role |
|---|---|
| expansion node | choose one or more witness/instantiation terms |
| selection node | introduce one suitably fresh parameter |
| definition node | selectively unfold an abbreviation |
| deep formula | propositional target after quantifier choices |
| dependency relation | checks that witness dependencies are well-founded |

**Acceptance criterion**: `deep formula is tautological` AND `dependency relation is acyclic`.

## Worked Example
For a formula with the shape `forall x. P(x) -> (P(a) and P(b))`, an expansion proof instantiates the universal premise at `a` and `b`. The resulting deep formula is propositionally equivalent to `(not P(a) or not P(b)) or (P(a) and P(b))`, a tautology. The tree records the two instances directly; a natural-deduction presentation can be reconstructed later.

In refutational form, the negation produces a dual expansion tree whose deep formula contains both `P(a) and P(b)` and `not P(a) or not P(b)`, yielding a contradiction.

## Key Takeaways
1. Search for the right instantiations, then check propositional validity.
2. Enforce acyclic dependencies in addition to tautology/contradiction.
3. Apply substitutions uniformly to the entire expansion structure.
4. Allow definition unfolding as an explicit, reversible proof-search choice.
5. Use expansion proofs as a bridge between diverse search procedures and readable proof formats.

## Connects To
- **Ch 3**: dependency-aware instantiation can replace unwieldy Skolem terms.
- **Ch 7**: expansion proofs translate to natural deduction without a second proof search.
- **Ch 10**: practical proof search is largely the problem of generating and testing expansion terms.
