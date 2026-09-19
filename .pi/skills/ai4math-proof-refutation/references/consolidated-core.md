# Consolidated core: proof, refutation and conjecture repair

## Purpose

Search for a trustworthy closure path by developing proofs and falsifiers together. This capability proposes and audits mathematical arguments; it cannot admit its own conclusions.

## Proof-state model

Represent the current state as:

- frozen target and allowed assumptions;
- established dependencies;
- open decisive obligations;
- candidate lemmas and their dependency edges;
- counterexamples and near misses;
- failed routes with precise blockers;
- current evidence capabilities.

The number of obligations is not a progress score. Discovering a necessary missing obligation can be genuine progress.

## Route generation

The canonical actor may use any appropriate route. Common lenses include:

- direct construction or direct implication;
- contrapositive or contradiction, with polarity checked;
- induction/recursion aligned to object construction;
- minimal counterexample and descent;
- extremal choice;
- invariant or monovariant;
- symmetry, averaging or probabilistic existence;
- algebraic, analytic, topological or combinatorial translation;
- compactness, duality or universal properties;
- exhaustive finite check with a proved reduction.

These are options, not mandatory phases. A route must expose why its assumptions plausibly control the target.

## Lemma discipline

A candidate lemma is useful only when it has:

1. an exact statement and domain;
2. a clear parent obligation;
3. evidence that it is true or a plan to falsify it;
4. a transfer edge showing how it helps;
5. no hidden strengthening of the root assumptions.

Avoid “lemma laundering”: proving a polished auxiliary statement that does not close any dependency of the root claim.

## Proof construction

For each inferential step record premises, rule, side conditions and conclusion. Explicitly audit:

- quantifier introduction and witness choice;
- case coverage and disjointness;
- induction base, arbitrary hypothesis, successor/structural step and domain coverage;
- use of excluded middle, choice or external theorems;
- equality versus isomorphism/equivalence;
- finite versus infinite assumptions;
- limiting, continuity, compactness or measurability conditions;
- termination of recursive constructions;
- scale and boundary applicability.

A familiar phrase such as “standard”, “clearly” or “by symmetry” is a request to expose an obligation, not a discharge.

## Refutation loop

Test a conjecture before investing heavily:

1. enumerate smallest legal instances and boundary cases;
2. negate the exact statement, preserving quantifiers;
3. search for witnesses to the negation;
4. verify that the witness satisfies every premise;
5. minimize and independently replay it;
6. identify which proof step or hidden assumption it attacks.

Distinguish:

- **global counterexample:** refutes the frozen conjecture;
- **local counterexample:** refutes an auxiliary lemma or proof step;
- **monster:** exploits an intended-domain ambiguity;
- **near miss:** violates one premise and may reveal a useful boundary;
- **encoding artifact:** invalid in the original domain.

## Conjecture repair

When a candidate fails, possible responses are:

- restrict the domain with an independently justified hypothesis;
- weaken the conclusion;
- replace a false lemma while preserving the root statement;
- split exceptional cases;
- repair a definition or representation;
- abandon the route.

Never rewrite the original problem silently. Every repaired conjecture gets a new identity and a stated relation to the root.

## External theorem use

For each imported result verify exact statement, assumptions, version and direction. Record whether it supplies a theorem, method, analogy or heuristic. A theorem whose precondition is another open problem does not close the obligation.

## Automated reasoning

Route logic fragments carefully:

- propositional finite structure may use SAT with a checked encoding;
- first-order search needs explicit term/instantiation bounds or proof objects;
- equality reasoning needs orientation/termination/confluence awareness;
- SMT/QE conclusions are limited to supported theories and encodings;
- higher-order unification is search with dependencies, not a guaranteed most-general substitution;
- rewriting must preserve type and side conditions.

Treat solver output as candidate evidence until proof/certificate replay and statement-faithfulness checks pass.

## Failed-route memory and anti-loop rule

A failed route record contains target, assumptions, attempted mechanism, strongest intermediate result, blocker, falsifier, reusable facts and conditions under which retry is justified.

Retry only with substantive novelty:

- new premise legitimately derived;
- new representation or invariant;
- new counterexample information;
- stronger theorem/library capability;
- corrected proof obligation;
- changed target justified by explicit conjecture repair.

Restating the same hope, running the same search at a larger but unjustified bound, or renaming the same lemma is not novelty.

## Proof comparison

Compare arguments by dependency core, not prose similarity. Ask which lemmas, invariants and transfer steps are essential; whether one proof covers a larger domain; whether one hides nonconstructive or analytic assumptions; and whether the formalization matches the informal proof content.

## Completion boundary

A proof draft closes nothing by itself. Root closure requires the exact statement, dependency closure, applicable independent verification, statement faithfulness, conflict resolution and admission. If any decisive obligation remains, report it precisely and keep the outcome open.
