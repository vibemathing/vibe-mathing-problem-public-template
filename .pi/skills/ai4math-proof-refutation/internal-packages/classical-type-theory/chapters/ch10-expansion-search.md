# Chapter 10: Searching for Expansion Proofs

**Source coverage**: §3 introduction and §3.1, printed pp. 987-992.

## Core Idea
The difficult higher-order search step is often inventing instantiation terms that unification of existing subformulas cannot produce. Build typed candidate expansions, search manageable subtrees, and use mating/connection plus higher-order unification to test whether a propositional core can become tautological.

## Frameworks Introduced
- **Primitive substitutions and projections**
  - When to use: to seed an expansion variable with one layer of logical structure determined largely by its type.
  - How: generate lambda terms whose bodies introduce a connective, quantifier, or projected argument, leaving auxiliary variables for later solving.
- **General substitutions (gensubs)**
  - When to use: when one connective at a time is too weak or when the target proof requires a richer predicate shape.
  - How: generate normalized bodies such as prenex forms with conjunction/disjunction matrices to avoid enumerating equivalent formulas repeatedly.
- **Theorem-specific abbreviation injection**
  - When to use: when a named concept in the goal is likely to appear inside the needed instantiation.
  - How: allow generated terms to mention selected abbreviations from the theorem or from heuristic relevance analysis.
- **Master expansion tree + bounded subtree search**
  - When to use: when the space of expansion options is too large to realize eagerly.
  - How: represent options lazily, choose a manageable subtree, and search for substitutions making its deep formula tautological.
- **Mating / connection search**
  - When to use: to avoid brute-force propositional enumeration of the deep formula.
  - How: progressively connect complementary literals until paths are spanned; use higher-order unification to ensure connection compatibility.
- **Component search**
  - When to use: when path enumeration is expensive.
  - How: build larger matings breadth-first from stored smaller matings; reuse unifier DAGs and test unspanned paths infrequently.

## Key Concepts
- **auxiliary variable**: a free variable introduced inside a partially specified expansion term for later solution.
- **primitive substitution**: a minimal typed candidate introducing one structural form.
- **projection**: a candidate that returns one of its arguments.
- **gensub**: a richer generated substitution, often normalized to control duplication.
- **expansion option**: an expansion node paired with a candidate term.
- **master expansion tree**: the conceptual tree containing all generated options.
- **mating / connection**: a relation pairing complementary literals so all relevant paths are spanned.
- **unification tree/DAG**: structure storing compatible substitutions for connections.

## Mental Models
- Search in two intertwined spaces: **which term shape to introduce** and **how its free variables should be solved**.
- Use types as a **candidate grammar** for primitive substitutions.
- Treat search bounds as **schedulers**: if one subtree or unification branch exceeds its allocation, backtrack and try another option.

## Anti-patterns
- **Assuming unification alone will invent every higher-order term**: many crucial instantiations must be seeded structurally.
- **Generating every rich term eagerly**: bodies with many connectives/quantifiers grow combinatorially.
- **Exploring one nonterminating unification branch indefinitely**: higher-order unification needs explicit bounds or fair scheduling.
- **Recomputing unifiers for every combination**: component search shows the value of storing and merging reusable DAG structure.

## Reference Tables

| Search symptom | Candidate response |
|---|---|
| no useful predicate/function emerges | add primitive substitutions or projections |
| candidate forms too shallow | use gensubs with controlled normal forms |
| theorem-specific concept missing | allow selected abbreviations in candidates |
| tree too large | search a bounded subtree / lazy master tree |
| path enumeration dominates | component search / mating decomposition |
| unification branches too long | cap branch work, preserve alternatives, backtrack fairly |

## Worked Example
In the chapter's X5310 example, simpler expansion options fail within the allocated search time. A richer gensub is then tried for the crucial higher-order expansion variable. The mating search supplies substitutions for the gensub's auxiliary variables; after lambda reduction and a normalization step, the resulting term collapses to the instantiation needed by the natural-deduction proof. The lesson is procedural: generate a structured template, let unification fill its holes, normalize, then rebuild the expansion proof with the completed term.

## Key Takeaways
1. Treat higher-order instantiation generation as a first-class search problem.
2. Start with type-driven primitive candidates, then escalate to richer gensubs.
3. Normalize candidate bodies to reduce equivalent-search duplication.
4. Combine expansion-term generation with mating/connection and higher-order unification.
5. Bound local search and retain a path to other subtrees/options.
6. Reuse partial unifier structures whenever possible.

## Connects To
- **Ch 6**: the target artifact is an expansion proof.
- **Ch 8**: higher-order unification fills auxiliary variables and tests connection compatibility.
- **Ch 7**: once found, the expansion proof can be reconstructed into natural deduction.
