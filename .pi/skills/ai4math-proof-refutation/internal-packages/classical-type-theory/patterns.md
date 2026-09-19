# Patterns

## Normalize After Higher-Order Substitution
**When to use**: after substituting a lambda term, unfolding a definition, or comparing higher-order expressions.
**How**: perform capture-safe substitution; alpha-rename when needed; beta-normalize before matching, equality checks, or unification.
**Trade-offs**: eager full normalization may be expensive, but comparing unnormalized terms can miss obvious equivalences.

## Dependency-Safe Skolemization
**When to use**: refutational search where Choice is not intended.
**How**: record each Skolem symbol's fixed arity and necessary arguments; retain those arguments on every occurrence; prevent variables free in necessary arguments from being captured later. Consider a dependency relation instead of explicit terms when expressions grow too large.
**Trade-offs**: more bookkeeping than naive Skolemization; avoids silently strengthening the logic.

## Expansion-Proof Certification
**When to use**: to validate a compact higher-order proof object.
**How**: compute the deep formula from quantifier instances; verify propositional tautology (or contradiction for a dual proof); construct the dependency graph and verify acyclicity.
**Trade-offs**: concise and proof-format independent; requires correct dependency tracking.

## Structured Expansion-Term Generation
**When to use**: unification of existing subformulas cannot invent the required higher-order term.
**How**: generate projections and primitive substitutions from the variable's type; escalate to gensubs; normalize candidate bodies; optionally inject relevant theorem abbreviations; leave auxiliary variables for unification.
**Trade-offs**: richer templates increase branching; normal forms and staged escalation control duplicate candidates.

## Bounded Mating Search
**When to use**: searching a deep formula for a tautological connection structure.
**How**: add complementary connections progressively; maintain higher-order unification compatibility; bound work per unification branch/subtree; backtrack fairly on incompatibility or exhausted budgets.
**Trade-offs**: resource bounds can make search incomplete for a run; they prevent one branch from monopolizing the prover.

## Component Search with Reused Unifiers
**When to use**: path enumeration and repeated unification dominate mating search.
**How**: precompute smaller mating components; store connection unifiers as DAGs; merge component/unifier structures to build larger candidates; check unspanned paths infrequently.
**Trade-offs**: memory for reusable components; reduces repeated expensive work.

## Deferred-Unification Resolution
**When to use**: resolution needs higher-order unification with no unique mgu or a potentially infinite search tree.
**How**: resolve/factor while appending equality constraints; prune unsatisfiable constraints; merge overlaps; solve/branch only when a manageable unifier set becomes available; add splitting rules to create missing logical structure.
**Trade-offs**: can cause clause proliferation; avoids premature unifier enumeration.

## Flex-Rigid Projection/Imitation
**When to use**: a variable-headed application must equal a rigid constant-headed application.
**How**: produce well-typed projection candidates that return an argument and imitation candidates that copy the rigid head with fresh helper functions; propagate resulting constraints.
**Trade-offs**: branching can be large; type and occurs checks are essential.

## Incremental Z-Match Elaboration
**When to use**: backward sequent search needs a predicate/set instantiation that can be inferred from current branch context.
**How**: choose a lambda substitution that closes or simplifies the current branch; include fresh auxiliary variables for unresolved structure; apply the substitution globally; refine auxiliaries on later branches.
**Trade-offs**: branch-local choices constrain the entire proof, so bad early structure may require backtracking.

## Proof-Core Reconstruction
**When to use**: a machine search returns a correct but opaque derivation.
**How**: derive/retain the expansion proof; merge redundant instances; reconstruct natural deduction with tactics guided by the expansion data; use the reconstructed proof as a readability and correctness check.
**Trade-offs**: extra post-processing; sharply improves inspection and semi-automatic workflows.
