# Chapter 10: Research Blueprints and Target-Driven Library Growth

## Core Idea

Large formalizations succeed by turning a headline theorem into a dependency graph and allowing the graph to drive reusable library work. The precise theorem statement can be a major milestone; the first project in an area often spends more effort on missing infrastructure than on the final few lines.

## Research Blueprint

Build a graph with these node types:

- definitions required to state the theorem;
- interface/API lemmas for those definitions;
- known reductions from the target to intermediate theorems;
- reusable background mathematics already in the library;
- missing reusable infrastructure;
- delicate core lemmas where correctness risk concentrates;
- temporary assumptions/sorries;
- final target and human-facing exposition.

Mark each node **done**, **ready**, **blocked**, or **assumed-temporarily**. An edge means one node cannot be completed without another. This creates natural parallel workstreams.

### Code-first and blueprint-first can coexist

A blueprint need not be a one-way specification written before coding. In the Liquid Tensor experience, formalizers sometimes attacked the next paper lemma directly; Lean exposed hidden steps, and the now-understood argument was written back into a human blueprint. Use whichever direction reduces uncertainty. Keep the code and exposition synchronized.

## Target-Driven Library Growth

A real theorem is a stress test for definitions and APIs. The procedure:

1. state the target as far as current definitions allow;
2. trace the first blocked dependencies;
3. distinguish project-specific lemmas from generally useful infrastructure;
4. design the reusable pieces at appropriate generality;
5. immediately test them in the target proof;
6. upstream or centralize stable infrastructure so it receives maintenance.

This avoids building entire MSc courses “just in case” while still producing broad library value.

## Staged Assumptions

During architecture work, an unavailable theorem may be temporarily represented as an axiom or `sorry`. Keep it safe by recording:

- exact statement;
- reason it is believed true;
- all downstream nodes that use it;
- whether a weaker assumption would suffice;
- owner/plan for discharge.

If a placeholder is discovered false, analyze whether the downstream proof only used a nearby true statement. Never let a temporary assumption disappear into the final trust story.

## Literature Repair

When formalization conflicts with a source:
1. localize the exact failure;
2. check for a “mathematical typo”: omitted smallness/nonempty hypothesis, flipped inequality, non-attained minimum, quantifier dependency;
3. consult another proof/reference or the authors/experts;
4. make the smallest repair preserving the conceptual argument;
5. document the correction.

A mature literature's successful applications are evidence, not a formal proof that every foundational lemma is correctly documented.

## Project Selection

High-value targets often combine:

- mathematical importance;
- a nontrivial correctness risk or poorly checked technical core;
- reusable missing infrastructure;
- a statement clear enough to validate;
- enough parallelism for collaboration.

A “complex theorem about complex objects” is feasible when the graph can be decomposed and the library is allowed to grow under pressure from the target.

## Anti-patterns

- Measuring progress only by whether the headline theorem is green.
- Treating thousands of prerequisite lines as wasted overhead; they are often the reusable result.
- Creating a detailed blueprint that blocks experimentation instead of reflecting it.
- Assuming a famous reference is immune to local errors.

## Validation Checkpoint

Audit the dependency graph from the target backward. Every blocked node should have one stated reason: missing definition, missing reusable API, missing theorem, disputed mathematics, or unfinished proof. For temporary assumptions, make sure their exact statements and downstream consumers are searchable. Periodically remove one assumed node and ask what actually breaks; this reveals whether a weaker theorem suffices. Progress should be measurable as reduced uncertainty and reusable infrastructure as well as closed goals. Before release, require the graph to contain no silent assumptions and reconcile the blueprint with the code that was actually proved.

## Key Takeaways

State, graph, unblock, reuse, and document. Large formalization is dependency engineering plus mathematics. Target pressure validates the library and makes later projects faster.

## Connects To

Definition quality: [06](ch06-definition-api-and-library-engineering.md). AI suitability: [12](ch12-ai-autoformalization-and-semantic-audit.md). Recovery/release: [14](ch14-failure-recovery-version-drift-and-self-check.md).
