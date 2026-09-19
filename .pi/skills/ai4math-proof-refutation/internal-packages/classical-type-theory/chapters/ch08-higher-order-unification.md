# Chapter 8: Higher-Order Unification

**Source coverage**: §2.4, printed pp. 984-986.

## Core Idea
Higher-order unification finds substitutions that make typed lambda terms equal after normalization. It is powerful enough to invent mathematically meaningful objects, yet unlike first-order unification it can lack a most-general unifier and can require nonterminating search.

## Frameworks Introduced
- **Lambda-aware unification**
  - When to use: when proof progress requires making two higher-order expressions coincide.
  - How: substitute for free variables, normalize both sides, and require the normal forms to match.
- **Search-tree unification**
  - When to use: whenever the problem is genuinely higher-order.
  - How: preserve branching alternatives and resource bounds; do not assume a single mgu exists.
- **Diagonal-object discovery**
  - When to use: as a mental model for the constructive power of higher-order unification.
  - How: allow function/predicate substitutions rich enough to synthesize a set or predicate that realizes the proof idea.

## Key Concepts
- **higher-order unifier**: a substitution making both expressions share a lambda-normal form.
- **most general unifier (mgu)**: a unifier from which others factor; it may not exist in higher-order problems.
- **unification search tree**: the branching process explored by higher-order unification algorithms.
- **undecidability**: there is no general terminating decision procedure for higher-order unifiability.
- **diagonal set**: the self-referentially constructed set appearing in Cantor's theorem proof.

## Mental Models
- Treat unification as **term synthesis under equations**, not only variable matching.
- Separate **no unifier found within bounds** from **provably non-unifiable**.
- Let types constrain the synthesis grammar before exploring substitutions.

## Anti-patterns
- **Expecting a unique mgu**: higher-order unification can have incomparable unifiers or no mgu.
- **Equating timeout with failure**: a branch may simply be nonterminating or the required unifier may lie beyond current bounds.
- **Comparing raw syntax instead of normal forms**: beta/lambda conversion can expose equality hidden by surface notation.

## Reference Tables

| First-order expectation | Higher-order reality |
|---|---|
| mgu usually exists when terms are unifiable | an mgu may not exist |
| unification is decidable | higher-order unification is undecidable |
| substitutions are mostly structural term matching | substitutions can synthesize predicates/functions |
| one computation returns the answer | a search tree may be required |

## Worked Example
The source sketches an automatic proof of Cantor's theorem. After preprocessing and duplicating a useful quantifier, the proof state has two disjunctive components that need to collapse to a propositional contradiction. Higher-order unification chooses lambda terms for predicate variables and ultimately synthesizes the diagonal predicate corresponding to the set `{w | w notin G(w)}`. Once normalized, the instantiated formula has the contradiction pattern `E or E` together with `not E or not E` in the required positions. The important operational point is that the unifier creates the central mathematical construction rather than merely matching a term already present.

## Key Takeaways
1. Normalize before judging whether higher-order terms match.
2. Preserve alternatives because an mgu may not exist.
3. Use resource bounds as operational controls, never as logical refutations.
4. Expect higher-order unification to synthesize proof concepts absent from the original formula.
5. Route persistent unification obligations to constraint-based methods when immediate exploration is too expensive.

## Connects To
- **Ch 10**: mating search invokes higher-order unification to test connection compatibility.
- **Ch 11**: constrained resolution defers unification instead of enumerating all unifiers early.
- **Ch 12**: extensional resolution internalizes higher-order unification as inference rules.
