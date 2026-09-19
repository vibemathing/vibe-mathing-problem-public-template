# Consolidated core: mathematical modeling and derivation

## Purpose

Convert a frozen problem statement into explicit mathematical objects, relations, invariants and candidate consequences while keeping every translation auditable. A model is a representation, not the original statement; a derivation is candidate reasoning until its obligations are checked.

## Representation record

For each model record:

- source object and target representation;
- domain and codomain;
- encoding/decoding maps when applicable;
- preserved properties and deliberately forgotten structure;
- totality, injectivity, surjectivity or equivalence claims;
- boundary cases and undefined/totalized operations;
- approximation regime and error notion;
- proof obligations needed to transfer a result back.

Never say two formulations are “equivalent” without both directions or an explicit one-way reduction.

## Definition audit

A useful definition must state:

1. carrier/domain;
2. data fields or constructors;
3. admissibility predicates;
4. equality or equivalence notion;
5. operations and closure conditions;
6. degenerate and boundary cases.

Test the definition on the smallest legal objects, extreme objects and known examples. If changing a definition repairs a conjecture, record that as a new statement rather than retroactively altering the old one.

## Abstraction ladder

Move deliberately among levels:

- concrete examples and coordinates;
- combinatorial or algebraic encoding;
- invariant/structural formulation;
- universal-property or categorical interface;
- computational representation;
- formal type.

At each move list what becomes easier, what becomes invisible and how to return. Prefer the weakest abstraction that exposes the needed operation or invariant.

## Derivation ledger

Write candidate derivations as typed edges:

`premises + definitions + transformation -> conclusion`

Each edge records:

- rule/theorem used;
- discharged side conditions;
- open side conditions;
- direction of implication;
- exact versus approximate status;
- reversible versus irreversible transformation;
- dependence on classical logic, choice or external facts.

A long derivation is a graph, not a paragraph. Shared intermediate facts should be named once; circular dependencies must be rejected.

## Invariant-guided modeling

Before exploring, identify quantities or structures expected to survive the allowed transformations: parity, degree, order, dimension, rank, measure, topology, symmetry, conservation law, monotonicity, compactness, convexity or logical polarity. Then test:

- whether the invariant is genuinely preserved;
- whether it is complete enough to distinguish desired cases;
- whether an apparent invariant is only empirical;
- whether a quotient or abstraction introduces spurious solutions.

Use broken invariants as diagnostic evidence for a bad model or a promising obstruction.

## Structural translations

### Algebraic/combinatorial

Specify orientation, multiplicity, loops, labels, indexing and finite/infinite assumptions. Audit whether counting arguments double-count or omit symmetry factors.

### Analytic

State topology, norm/measure, convergence mode and regularity. Keep pointwise, uniform, almost-everywhere and distributional claims distinct. Record limiting interchange conditions.

### Probabilistic

Freeze probability space, random variables, dependence assumptions and event quantifiers. Distinguish expectation, high probability, almost sure and existence conclusions.

### Categorical/universal

Name objects, morphisms, variance and commuting diagrams. Use a universal property only after existence and uniqueness hypotheses are established. Natural isomorphism is not literal equality.

### Formal/computational

Specify data representation, normalization and decidability. Prove that executable predicates correspond to mathematical predicates before treating output as relevant.

## Countermodel pressure

Every model should face adversarial tests:

- empty, singleton and minimal nontrivial cases;
- extremal parameter values;
- disconnected, singular or non-generic inputs;
- changed quantifier order;
- nonconstructive witness assumptions;
- encoding collisions;
- objects valid in the model but illegal in the source problem.

A failed pressure test yields a revised model, a restricted claim, or a counterexample candidate—not an exception to ignore.

## Approximation discipline

For approximation record the metric, tolerance, stability argument, scaling regime and error propagation. Numerical closeness does not imply symbolic identity. An asymptotic model must state which variables tend where and which constants are uniform.

## Failure recovery

- **Derivation stalls:** inspect missing side conditions and try a representation exposing them.
- **Expression explosion:** introduce typed intermediate objects and quotient irrelevant symmetry only with a recovery map.
- **Model too weak:** identify the exact property not represented before adding structure.
- **Model too strong:** find which assumption excludes legal source instances.
- **Equivalent-form claim fails:** retain the valid direction and register the reverse as an open obligation.
- **Repeated reformulation:** require a new preserved invariant, new transfer lemma, new falsifier or new computational affordance.

## Output contract

Return model definitions, representation maps, a dependency graph, tested edge cases, candidate derivations, open transfer obligations and evidence ceiling. Do not report a model-derived claim as a root result until transfer and admission gates close.
