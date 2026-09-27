# Chapter 11: Appendix — Preliminaries

## Core Idea

The model-checking algorithms rely on a small mathematical toolkit: set/sequence notation, formal languages and automata, propositional logic, directed graphs, and asymptotic complexity. Load this chapter when a proof or algorithm uses those foundations implicitly.

## Frameworks Introduced

### Formal-language toolkit
Use words, prefixes, concatenation, Kleene star, and infinite words to move between traces and automata.

- `Σ*`: all finite words over alphabet `Σ`.
- `Σ^ω`: all infinite words over `Σ`.
- `pref(w)`: finite prefixes of a word/trace.
- language operations: union, concatenation, complement (relative to the appropriate universe), finite/infinite repetition.

**When to use**: Ch 3–5 property semantics and automata constructions.

### Propositional-logic toolkit
A state label `L(s) ⊆ AP` induces a truth assignment for atomic propositions. Propositional formulas then denote sets of states/labels.

Operational uses:
- guards in program graphs;
- state predicates/invariants;
- symbolic state-set encodings;
- transition-relation Boolean functions;
- atomic clock/probability subformula labeling in richer logics.

Core transformations:
- Boolean equivalence and duality;
- satisfiability/tautology checks;
- normal forms when needed by algorithms.

### Graph toolkit
Most explicit-state model checking reduces to graph operations.

Key primitives:
- successor/predecessor sets;
- reachability and backward reachability;
- paths and cycles;
- strongly connected components (SCCs);
- bottom SCCs (no outgoing edge to another SCC);
- graph traversal by DFS/BFS.

Use SCCs for recurrence/accepting-cycle reasoning; use BSCCs in finite Markov chains; use end components/MECs as the MDP analogue.

### Complexity toolkit
The book reports both algorithmic time in terms of explicit graph size and decision-problem complexity classes.

Keep these dimensions separate:
- `O(|S|+|E|)` may be linear in an **already exponential** state graph;
- formula translation can be exponential while state exploration is linear;
- symbolic representation can avoid explicit enumeration in practice without changing worst-case complexity classes.

Use `P`, `NP`, `PSPACE` terminology only at the level justified by the corresponding theorem; do not infer practical runtime from the class alone.

## Key Concepts

- **Power set `2^AP`**: set of all proposition-label sets; alphabet for state-label traces.
- **Relation**: subset of a Cartesian product; transition relations, simulations, and equivalences are relations with additional properties.
- **Equivalence relation**: reflexive, symmetric, transitive; partitions a set into equivalence classes.
- **Function / valuation**: mapping used for variable assignments, labels, probability vectors, and Boolean encodings.
- **Finite/infinite sequence**: basis for execution fragments and paths.
- **Prefix**: finite initial segment; central to safety/bad-prefix definitions.
- **Language**: set of words; regular and ω-regular languages represent behavioral properties.
- **SCC**: maximal mutually reachable vertex set.
- **Topological condensation**: SCC graph is acyclic; useful for long-run decomposition.
- **Asymptotic complexity**: growth rate as model/formula parameters increase.

## Mental Models

- **Translate semantics into sets first**: a formula usually becomes a set of labels, traces, or states; algorithms manipulate those sets.
- **Graph structure is the common execution substrate**: reachability, temporal fixed points, Büchi acceptance, and probabilistic recurrence all reuse graph primitives.
- **Finite-state does not mean small**: a bit-vector model with `n` Boolean variables already admits `2^n` valuations.
- **Complexity has multiple parameters**: always ask whether an exponential comes from variables/states, property length, clocks/constants, or determinization.

## Anti-patterns

- **Using `2^AP` as arithmetic exponentiation in explanations**: it denotes a power set in this context.
- **Confusing path existence with positive probability**: graph theory and probability measure answer different questions in Ch 10.
- **Calling every SCC a recurrent closed class**: MC recurrence needs a BSCC; MDP recurrence needs an end component with action closure.
- **Using a big-O bound without naming its input representation**: “linear” in a region graph can still be exponential in the compact timed automaton.
- **Assuming equivalence-class quotienting preserves every property**: the specific relation and logic fragment determine preservation.

## Reference Tables

### Graph primitive → model-checking use

| Primitive | Use |
|---|---|
| DFS/BFS reachability | deadlock, invariant, counterexample prefix |
| backward reachability | CTL `EU`, probability 0/1 preprocessing |
| SCC | Büchi cycles, fairness, long-run structure |
| BSCC | finite-MC almost-sure recurrent class |
| partition refinement | bisimulation/simulation-style quotienting |
| predecessor operator | CTL fixed points, symbolic checking |

### Complexity interpretation

| Statement | Read it as |
|---|---|
| CTL basic algorithm linear in graph × formula | efficient once the finite graph is available |
| LTL translation exponential in formula | formula size can dominate even for moderate models |
| TCTL linear in region graph but PSPACE-complete | region construction can be exponentially large |
| PCTL reachability solves linear equations | numerical linear algebra enters verification cost |
| MDP PCTL* double-exponential in formula in general construction | expressiveness/automata determinization is expensive |

## Worked Example: why “linear-time algorithm” may still blow up

A concurrent model has `n` local components, each with `k` local states. The explicit global product may contain up to `k^n` combinations before reachability pruning. A CTL algorithm taking time proportional to the global graph can therefore be “linear” in its explicit input while still scaling exponentially in the compact compositional description.

Use this reasoning whenever a complexity statement seems inconsistent with observed state explosion: identify the representation whose size appears in the bound.

## Key Takeaways

1. Formal-language notation underpins trace and automata semantics.
2. Propositional logic turns labels/valuations into state predicates and symbolic functions.
3. Graph traversal and SCC decomposition are the computational backbone of many checkers.
4. Complexity statements must name their parameters and representation.
5. Equivalence relations create quotients; preservation requires a theorem tied to the logic/property class.

## Connects To

- **Ch 2–3**: sets, relations, graphs, and propositional formulas define transition-system behavior and properties.
- **Ch 4–5**: language/automata theory defines regular and ω-regular properties.
- **Ch 6–8**: fixed points, BDDs, equivalence relations, and graph algorithms implement checking/reduction.
- **Ch 9**: region counts show how a finite quotient can still be exponential.
- **Ch 10**: graphs combine with probability measures, linear equations, and optimization.
