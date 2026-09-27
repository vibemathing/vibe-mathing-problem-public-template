# Chapter 14: Search Architecture and Research Agenda

**Source coverage**: §4 and the proof-search overview, printed pp. 987-999; bibliography/index were also reviewed for terminology and method cross-links.

## Core Idea
A practical classical higher-order prover must coordinate first-order search machinery with higher-order instantiation, unification, equality/extensionality, definitions, proof transformation, and explicit resource control. The chapter's conclusion is a design agenda: each missing capability can become a distinct failure mode in a prover.

## Frameworks Introduced
- **Two-added-problems diagnostic**
  - When to use: when extending a first-order prover to higher-order logic.
  - How: first ask how higher-order unification will be controlled; second ask how higher-order quantifiers will receive instantiation terms that unification of existing formulas cannot generate.
- **Modular proof-search architecture**
  - When to use: when designing or debugging a prover.
  - How: separate representation/typing, candidate generation, unification, logical inference, equality/extensionality, search control, and proof reconstruction so each can evolve independently.
- **Completeness-versus-resources discipline**
  - When to use: whenever practical bounds are added.
  - How: make bounds explicit, report bounded failure accurately, and provide widening or alternate-method recovery.
- **Normal-proof bias diagnostic**
  - When to use: when standard Herbrand/Gentzen/Beth-derived search repeatedly misses mathematically natural proof ideas.
  - How: recognize that many automatic methods preferentially find normal proofs; consider search procedures capable of non-normal proof structure when domain practice suggests it.

## Key Concepts
- **proof-search family**: resolution, matings/connections, semantic tableaux/partitions, combinatory reductions, proof planning.
- **search heuristic**: a method for guiding or restricting exploration without changing the underlying logic.
- **metatheorem**: a theorem used to justify pruning or a search transformation.
- **proof library**: reusable definitions, theorems, and theories that can supply proof knowledge.
- **semi-automatic proving**: combining human proof outlines/tactics with automated gap filling.

## Mental Models
- Build the prover as a **portfolio of controlled search regimes**, not one universal loop.
- Diagnose failures by layer: representation -> instantiation -> unification -> equality/extensionality -> search control -> proof reconstruction.
- Use **metatheorems to justify pruning** and heuristics to prioritize; do not confuse the two.

## Anti-patterns
- **Silent heuristic incompleteness**: hard bounds or restricted term generators must be visible in results.
- **One proof calculus for every problem**: extensional equality, induction, and higher-order instantiation may need specialized modules.
- **Discarding proof reconstruction as cosmetic**: readable proof transformations support validation and interactive workflows.
- **Assuming all useful proofs are normal**: mathematical practice may favor proof structures outside the normal forms targeted by standard automated methods.

## Reference Tables

| Failure signal | Likely layer | Escalation |
|---|---|---|
| no candidate predicate/function | instantiation | primitive/gensub, Z-match, theorem-expression generation |
| unification branch never settles | unification | bounds, fair scheduling, deferred constraints |
| equality dominates clauses | equality/extensionality | extensional resolution / specialized rewriting |
| too many type-correct candidates | representation/search | sorts, subtypes, annotations, better libraries |
| repeated redundant proof states | search control | component reuse, merging, caching, better heuristics |
| proof found but unusable | reconstruction | expansion-proof merge + natural deduction translation |
| bounded search fails repeatedly | resources/completeness | widen bounds or change calculus before declaring failure |

## Worked Example
A first-order-style prover is extended to higher-order goals. It can resolve clauses but repeatedly stalls because no term already in the goal unifies with a higher-order predicate variable. The architecture should classify this as an instantiation-generation failure, not a resolution failure. Add a typed candidate generator (primitive substitutions/gensubs or Z-match), then feed its partially specified terms into higher-order unification. If unification becomes nonterminating, move that obligation into constraints or bound it fairly. If the remaining obstacle is functional equality, route to extensional resolution. Once the proof core is found, reconstruct it for human inspection.

## Key Takeaways
1. Separate higher-order term generation from higher-order unification.
2. Add extensionality/equality handling as a deliberate module.
3. Make every resource bound explicit and recoverable.
4. Use libraries, subtypes, and structural annotations to shrink search.
5. Treat proof translation as part of correctness and usability.
6. Be prepared to explore non-normal proof strategies when standard methods systematically fail.

## Connects To
- **Ch 5**: completeness proofs justify which pruning/search transformations are safe.
- **Ch 9**: type-order bounds are necessarily heuristic.
- **Ch 10-13**: provide interchangeable search modules for different failure modes.
