# Chapter 6: Elaboration, Tactics, and Goals

## Core Idea
Request elaboration output with `-e`. It turns Lean InfoTrees into a recursive execution trace: terms, macros, tactics, local contexts, goals before/after each tactic, dependency changes, and tactic-specific metadata such as simp theorem usage.

## Frameworks Introduced
- **Goal snapshot model**
  - When to use: understand proof-state changes caused by tactics.
  - How: capture a sanitized local context and target for each metavariable before and after the tactic.
- **Dependency-delta tracing**
  - When to use: identify which new goals/hypotheses arise from solving or assigning a prior goal.
  - How: follow delayed/assigned metavariables until unresolved descendants and dependent free variables are found.
- **Tactic-specific augmentation**
  - When to use: a tactic exposes valuable internal statistics beyond generic before/after goals.
  - How: store extra JSON without changing the common tactic schema; current source augments `simp`, `simp_all`, and `dsimp` with used theorem names.
- **InfoTree completeness rule**
  - When to use: elaboration/line data looks sparse.
  - How: ensure InfoTree collection is enabled and asynchronous elaboration is not dropping tactic nodes.

## Key Concepts
- **Sanitized local context**: local declarations with implementation details removed and names sanitized for display.
- **`isReferencedLater`**: whether a local variable still appears in the remaining local context.
- **Goal `extra?`**: optional metadata such as type/value metavariable usage.
- **Tactic `references`**: names appearing in the tactic syntax.
- **`before` / `after`**: goal arrays evaluated in the tactic's pre/post contexts.
- **`newGoals` / `newHypotheses`**: dependency metadata for assigned goals.
- **`special?` term value**: direct constant or free-variable identity when the elaborated term has that simple form.

## Mental Models
- Treat a tactic node as a **state transition with provenance**, not just syntax.
- Treat InfoTrees as **the execution trace substrate** for IDE-like analysis.
- Treat simp theorem extraction as **replaying the tactic's simplifier context to recover actual used origins**.

## Anti-patterns
- **Inferring tactic effect from syntax alone**: use before/after goals and dependency metadata.
- **Assuming every syntax identifier is a theorem dependency**: tactic syntax references include constants and local hypotheses; simp usage provides stronger evidence for simplification tactics.
- **Discarding contexts to save space before analysis**: local hypotheses are often the data needed for proof-state understanding.
- **Ignoring InfoTree availability**: no postprocessing can reconstruct omitted tactic nodes reliably.

## Code Examples
```lean
let before ← TacticM.runWithInfoBefore ci ti <| Goal.fromTactic ...
let after  ← TacticM.runWithInfoAfter  ci ti <| Goal.fromTactic ...
```
- **What it demonstrates**: tactic semantics are captured in the correct Lean context on both sides of the transition.

## Reference Tables

| Elaboration node | Captured payload |
|---|---|
| tactic | syntax references, before/after goals, optional extras |
| term | context, inferred type, expected type, value, optional constant/fvar identity |
| macro | expanded pretty syntax + kind |
| command/field/option/etc. | lightweight node kind marker |

| Simp-family tactic | Used theorem extraction |
|---|---|
| `simp` | simplifier stats from normal simp context |
| `simp_all` | simp-all context/statistics |
| `dsimp` | definitional simplification stats |

## Worked Example
A `simp` tactic closes one goal but the user wants to know which lemmas mattered.

1. Locate the tactic node in elaboration output.
2. Read `before` to capture the original target and local context.
3. Read tactic `references` for explicit names in the syntax.
4. Read `extra.usedTheorems` for theorem origins the simplifier actually used.
5. Read `after` to confirm the goal was solved or transformed.
6. If new subgoals/hypotheses appear, inspect dependency metadata attached to the originating goal.
7. If tactic nodes are missing, verify InfoTree collection and `Elab.async=false` before interpreting absence as semantic evidence.

## Key Takeaways
1. Before/after goal state is the primary unit of tactic behavior.
2. Metavariable dependency tracing explains how goals split or depend on generated hypotheses.
3. Simp-family metadata adds actual theorem usage beyond syntax references.
4. Term nodes preserve expected vs inferred type.
5. Complete InfoTrees are a prerequisite, not an optional enhancement.

## Connects To
- **Ch 2**: goal and elaboration schemas.
- **Ch 3**: InfoTree hooks and command-state accumulation.
- **Ch 7**: line output reuses goal extraction at source positions.
