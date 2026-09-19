# Chapter 13: Other Higher-Order Instantiation Techniques

**Source coverage**: §§3.4-3.5, printed pp. 996-998.

## Core Idea
When standard expansion or resolution search struggles to invent a higher-order term, use context-driven instantiation generators and representation-level search reducers. The source highlights incremental Z-match, construction from existing expressions, sorts/subtypes, and rippling/coloring.

## Frameworks Introduced
- **Z-match incremental elaboration**
  - When to use: in backward sequent-style search when a set/predicate variable must be instantiated so a branch becomes axiom-like.
  - How: choose a substitution that immediately solves the current sequent while leaving fresh variables inside the new term; propagate the substitution globally; later Z-match steps refine those fresh variables on other branches.
- **Bledsoe-style construction from existing expressions**
  - When to use: when likely set/predicate instantiations can be assembled from terms already present in the theorem.
  - How: apply domain-specific basic generation rules and combining rules rather than enumerating arbitrary lambda terms.
- **Sort/subtype restriction**
  - When to use: when many candidates are excluded by domain categories stronger than the base simple types.
  - How: add sort/subtype information to make representations shorter and reduce search, while using a compatible unification treatment.
- **Rippling / coloring**
  - When to use: especially around inductive proofs where syntactic differences between goal and hypothesis should guide transformations.
  - How: annotate occurrences with structural information and use the annotations to direct rewriting/unification choices.

## Key Concepts
- **Z-match**: a rule that incrementally constructs a predicate/set instantiation from a sequent context.
- **meta-variable**: a placeholder for an expression that later search will instantiate.
- **simple Z-match**: special Z-match cases where the contextual predicate has a particularly direct lambda form.
- **sort/subtype**: a refined category used to constrain terms beyond coarse base types.
- **rippling**: a proof-search heuristic driven by syntactic differences.
- **coloring**: attaching annotations to symbol occurrences so unification/search respects structural information.

## Mental Models
- Use **branch-local progress with global substitution**: Z-match chooses a term to close one branch but leaves knobs that other branches can tune.
- Prefer **theorem vocabulary before invented vocabulary**: expressions already present in the goal are high-value ingredients for instantiations.
- Treat sorts/annotations as **search indexes** that reduce candidate ambiguity.

## Anti-patterns
- **Generating arbitrary higher-order terms without using context**: the candidate space becomes unmanageable.
- **Applying a Z-match substitution only to the current branch**: the substitution must be propagated to all occurrences of the variable.
- **Adding sorts without updating unification/search semantics**: a restriction that the solver ignores gives no pruning and can be unsound if interpreted inconsistently.

## Reference Tables

| Problem | Method |
|---|---|
| need to refine a set/predicate incrementally across proof branches | Z-match |
| theorem contains expressions likely to build the missing set/function | Bledsoe-style generation |
| too many terms are type-correct but semantically irrelevant | sorts/subtypes |
| inductive rewriting needs directional guidance | rippling / coloring |

## Worked Example
A Z-match branch contains a predicate variable `f` in a position where replacing `f(T)` with a term built from a known predicate `P(T)` would make the sequent immediately tautological. The rule instantiates `f` with a lambda body containing `P` plus fresh predicate/equality variables. This closes the current branch while preserving degrees of freedom. Because the same `f` occurs elsewhere, the substitution is propagated globally; later branches instantiate the fresh variables to satisfy their own constraints. The target predicate is therefore assembled incrementally rather than guessed in one shot.

## Key Takeaways
1. Use context-driven term generation before unconstrained enumeration.
2. Propagate higher-order substitutions globally across the proof state.
3. Leave auxiliary variables when one branch does not determine the full instantiation.
4. Add sorts/subtypes when they meaningfully reduce the term language.
5. Use annotations such as rippling/colors to preserve structural information that plain syntax loses.

## Connects To
- **Ch 10**: primitive substitutions/gensubs are another structured instantiation generator.
- **Ch 12**: projection/imitation solve a related term-shape problem inside unification.
- **Ch 14**: these techniques are search-control modules chosen by failure diagnosis.
