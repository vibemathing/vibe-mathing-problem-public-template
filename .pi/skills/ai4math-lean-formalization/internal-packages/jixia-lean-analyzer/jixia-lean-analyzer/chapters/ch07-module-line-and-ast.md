# Chapter 7: Module, Line, and AST Views

## Core Idea
jixia exposes three complementary structural views around the deeper declaration/symbol/elaboration data: module metadata, proof states sampled by source position, and the raw parsed command AST.

## Frameworks Introduced
- **View-selection rule**
  - When to use: decide between coarse project context, IDE-like proof state, and raw syntax.
  - How: imports/docs → module; proof state at positions → line; exact parser tree → AST.
- **Position-to-goal projection**
  - When to use: build editor/teaching interfaces that need the proof state at each source position.
  - How: enumerate file positions, query InfoTrees for goals at that position, convert each to the common `Goal` schema.
- **Raw-vs-semantic separation**
  - When to use: consumers need parser fidelity alongside semantic products.
  - How: keep AST as raw parsed commands and use declaration/elaboration/symbol outputs for semantic interpretation.

## Key Concepts
- **`ModuleInfo.imports`**: imported Lean module names from the environment header.
- **`ModuleInfo.docstring`**: main module documentation strings.
- **`InfoTree.goalsAt?`**: source-position query used for line states.
- **`LineInfo.start`**: byte position in the source file.
- **`state.commands`**: parsed command array serialized by AST output.

## Mental Models
- Module output is a **file-level dependency header**.
- Line output is an **IDE projection of elaboration state**.
- AST output is **parser structure**, useful when semantics are intentionally postponed.

## Anti-patterns
- **Using AST identifiers as a semantic reference graph**: prefer Symbol/Elaboration data.
- **Using line state without byte-offset awareness**: position joins can be wrong in Unicode-heavy files.
- **Expecting line goals with InfoTrees disabled**: the line processor depends on them.
- **Assuming module imports reveal declaration-level usage**: imports are coarse file dependencies.

## Code Examples
```lean
fileMap.positions.mapM fun p => do
  return {
    start := p,
    state := ← trees.flatMapM fun tree => getGoalsAt tree fileMap p
  }
```
- **What it demonstrates**: line output projects shared InfoTree data onto source positions.

## Reference Tables

| Output | Granularity | Best for |
|---|---|---|
| module | file/module | import graph, module docs |
| line | source positions | editor proof state, tutoring traces |
| AST | parsed commands | syntax research, parser/debug tooling |
| declaration | source declarations | IDE navigation, source metadata |
| symbol | elaborated constants | dependency graphs, semantic ML features |
| elaboration | execution tree | tactic/term understanding |

## Worked Example
You are building a Lean-aware editor sidebar.

1. Use module output to show direct imports and module documentation.
2. Use declaration output to provide navigation ranges for definitions/theorems.
3. Use line output to show proof state at cursor/source positions.
4. Load elaboration output only when the user asks why a tactic changed the state.
5. Use AST output for parser-oriented features such as command-tree inspection, not as a replacement for semantic records.

## Key Takeaways
1. These views answer different questions and compose well.
2. Line analysis is built on the same goal/InfoTree machinery as elaboration analysis.
3. AST is deliberately special-cased in `Main.lean`.
4. Module imports are useful context, not a fine-grained reference graph.
5. Byte source positions remain the joining key for line/source features.

## Connects To
- **Ch 2**: shared JSON and range conventions.
- **Ch 6**: line goals reuse `Goal.fromTactic` and InfoTrees.
- **Ch 8**: choose the right view before inventing a new plugin.
