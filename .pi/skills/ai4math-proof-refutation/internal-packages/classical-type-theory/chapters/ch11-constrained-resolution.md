# Chapter 11: Constrained Resolution

**Source coverage**: §3.2, printed pp. 992-994.

## Core Idea
Resolution can be extended to higher-order logic by postponing expensive/non-unitary unification. Instead of choosing one unifier at each resolution step, carry equations as constraints and require a satisfying substitution only when the refutation closes.

## Frameworks Introduced
- **Constrained clause**
  - When to use: when resolving higher-order literals for which no unique mgu is available.
  - How: represent a clause together with a set of constraints; a substitution satisfies a constraint when all formulas in that constraint become identical after substitution/normalization.
- **Constrained resolution/factoring**
  - When to use: to perform clause inference before fully solving higher-order equations.
  - How: resolve or factor the logical literals and append the would-be unification equation as a new constraint.
- **Splitting rules for predicate variables**
  - When to use: when necessary instantiations cannot arise by unifying formulas already present.
  - How: force an atom headed by a predicate variable to match a logical form whose head is a connective or quantifier, introducing fresh variables and constraints.
- **Constraint maintenance**
  - When to use: continuously during search.
  - How: delete clauses with unsatisfiable constraints; merge overlapping constraints; when a manageable general set of unifiers is available, branch on it and remove the solved singleton constraint.

## Key Concepts
- **constraint**: a set of same-typed formulas that must be made identical by a substitution.
- **constraint satisfaction**: simultaneous unification of every constraint set.
- **constrained clause**: a logical clause paired with its pending unification requirements.
- **splitting rule**: an inference that introduces logical structure for a variable-headed atom.
- **deferred unification**: postponing commitment to a particular higher-order unifier.

## Mental Models
- Treat unification obligations as **debt attached to clauses**: inference can proceed while the debt is carried, simplified, merged, or later paid by a substitution.
- Use splitting as a **term-shape generator inside resolution**: it addresses the same missing-instantiation problem that expansion search handles with primitive substitutions.

## Anti-patterns
- **Enumerating all higher-order unifiers before resolving**: the search tree can be infinite and an mgu may not exist.
- **Keeping clauses whose constraints are already impossible**: prune them immediately.
- **Ignoring clause proliferation**: delayed unification trades one explosion risk for another; clause-generation controls are mandatory.
- **Assuming completeness from resolution/factoring alone**: splitting rules are needed because some required higher-order instantiations cannot be obtained from existing terms.

## Reference Tables

| Operation | Effect |
|---|---|
| constrained resolution | combine two clauses; add a constraint equating resolved literals |
| constrained factoring | merge same-polarity literals; add their equality constraint |
| splitting | introduce connective/quantifier structure for a variable-headed atom |
| unsatisfiable-constraint pruning | delete the entire constrained clause |
| overlap merge | union constraints sharing a formula |
| bounded unifier expansion | apply each manageable candidate substitution and simplify constraints |

## Worked Example
Suppose higher-order clauses contain complementary literals `N` and `not M`, but unifying `N` and `M` has many incomparable solutions. A first-order resolver would choose the mgu immediately. Constrained resolution instead forms the resolvent from the remaining literals and attaches `{N, M}` as a pending constraint. Later inference may make this constraint simpler, merge it with related constraints, or show it unsatisfiable. If the empty logical clause is eventually reached with a satisfiable constraint set, any satisfying substitution completes the refutation.

## Key Takeaways
1. Postpone higher-order unifier choice when no canonical mgu exists.
2. Carry equations explicitly as constraints through resolution and factoring.
3. Add splitting rules to generate missing higher-order logical structure.
4. Prune unsatisfiable constraints early and merge overlapping ones.
5. Treat clause proliferation as a primary failure mode requiring search controls.

## Connects To
- **Ch 8**: explains why higher-order unification cannot be handled like first-order mgu computation.
- **Ch 10**: splitting and primitive substitutions solve analogous instantiation-generation problems.
- **Ch 12**: extensional resolution turns constraints into clause literals and adds extensionality-aware inference.
