# 01 — Orientation and Project Strategy

## Core Idea

Formalization work fails early when the mathematical target, representation, or library dependencies are too ambitious for the available time. Establish a **small executable core** first. Expand generality only after the core compiles.

## Project-selection framework

### 1. Choose a tractable representation

Prefer tasks whose objects and main operators already have simple Lean/Mathlib representations. Competition number theory and inequalities are often easier starting points than geometry, difficult combinatorics, or bespoke summation frameworks.

Before doing substantial proof work, answer:

- How will every object in the statement be represented?
- Which operators already exist in Mathlib?
- Which key lemmas already exist?
- Which definitions would have to be built locally?
- Is the resulting dependency chain still small enough to finish?

If the answer exposes a large missing framework, reduce the target or adopt a nearby Mathlib abstraction.

### 2. Start from a mathematical proof

For a proof problem, first obtain a correct natural-language proof. Then rewrite it into a form friendly to formalization:

1. state variables and domains explicitly;
2. name hypotheses;
3. separate logical steps from algebraic calculations;
4. identify lemmas that can be proved independently;
5. search Mathlib for each nontrivial operator/theorem.

This prevents Lean debugging from becoming mixed with discovering the mathematics itself.

### 3. Build a proof blueprint

Represent the proof as dependencies among intermediate facts and goals. The exact graphical format is optional; the useful information is:

- starting context;
- each intermediate lemma;
- which earlier facts feed each lemma;
- target transformation after each major step;
- independent branches that can be solved separately.

During early project construction, `sorry` can temporarily mark unfinished leaves of the blueprint. Remove those placeholders before claiming the theorem is proved.

### 4. Expand only after the core works

Useful expansion axes include:

- special case → general theorem;
- concrete type → abstract typeclass assumptions;
- one theorem → small reusable local API;
- direct definition → more general library-compatible definition.

Avoid generalizing merely because Mathlib often uses highly abstract formulations. A pedagogical or project-local development can deliberately choose a simpler framework when that makes the mathematics clearer.

## Task families

### Competition-problem formalization

Workflow:

1. select a problem with manageable representation;
2. verify the statement can be expressed with existing types/operators;
3. obtain a natural proof;
4. search Mathlib for key lemmas;
5. split into Lean lemmas;
6. scaffold and prove the pieces;
7. integrate and simplify.

Early warning signs: a core geometric object has no library representation, a combinatorial encoding dominates the proof, or basic notation requires a large custom theory.

### Research-math statement formalization

A full proof may be unrealistic. Deliver value by:

- formalizing the important definitions;
- locating their Mathlib equivalents;
- building a dependency chain among concepts;
- stating the key theorem family;
- proving selected foundational lemmas.

For an elementary statement with a short known proof, aim higher and complete the proof if feasible.

### Pedagogical formalization

Mathlib optimizes for reuse and generality. For teaching, it can be reasonable to rebuild a limited concept in a familiar language. Example: develop elementary epsilon-style limits over real numbers rather than forcing learners through topology before the learning objective requires it.

State clearly that the local framework is intentionally narrower so later users do not confuse it with Mathlib's canonical abstraction.

### Physics or custom-domain formalization

Representation design is the primary risk. Start with a tiny model and a small theorem. Custom inductive types can be powerful, but they increase the cost of every later theorem if the constructors are poorly chosen.

## Worked Example — triage a competition theorem

Suppose two candidate problems are available. One is an inequality over familiar numeric types with a short natural proof; the other needs a custom geometric encoding plus many basic incidence lemmas. First search Mathlib for the operators and key bridges of each. Select the inequality as the executable core, state the natural proof as a dependency chain, and reserve geometric infrastructure as a later expansion. This applies the course rule: representation and library support are part of problem difficulty.

## Failure recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Most time is spent defining infrastructure | target too far from existing libraries | narrow the scope or switch representation |
| A theorem appears simple mathematically but Lean statement is huge | abstraction/generalization chosen too early | prove a concrete version first |
| Team members block one another | monolithic proof | split independent lemmas and make interfaces explicit |
| Searches return nothing | vocabulary/abstraction mismatch | inspect nearby definitions; search a neighboring abstraction |
| Blueprint has many speculative nodes | mathematics or representation unresolved | stop coding; settle the natural proof and object model |

## Key Takeaways

- Optimize for a **completable core**, then generalize.
- Check Mathlib support before committing to representation.
- Separate mathematical proof discovery from Lean proof construction.
- Treat the blueprint as an engineering dependency map, useful for collaboration and debugging.

## Connects To

- Natural-language statement decomposition → [ch03](ch03-first-order-logic-formalization.md)
- Mathlib search and definition control → [ch04](ch04-mathlib-search-sets-blueprints.md)
- Inductive representation design → [ch05](ch05-dependent-types-term-construction.md)
