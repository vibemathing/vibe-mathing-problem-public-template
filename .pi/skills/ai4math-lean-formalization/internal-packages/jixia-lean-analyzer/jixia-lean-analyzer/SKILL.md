---
name: jixia-lean-analyzer
description: "Operate, debug, and extend jixia for Lean 4 static analysis."
license: Apache-2.0
---

<!-- argument-hint: [task, output type, error, plugin, or chapter] -->

# jixia Lean 4 Static Analyzer

**Source**: uploaded `jixia` repository snapshot | **Lean toolchain**: v4.29.0 | **Source units**: 21 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task involves operating, understanding, debugging, or extending **jixia**, the Lean 4 static analyzer.

Route first:

| User goal | Load |
|---|---|
| Build or run jixia; analyze a standalone/project file | [ch01](chapters/ch01-build-and-run.md) |
| Understand JSON fields or source ranges | [ch02](chapters/ch02-data-model-and-json.md) |
| Understand lifecycle, CLI wiring, or plugin dispatch | [ch03](chapters/ch03-pipeline-and-plugin-lifecycle.md) |
| Work with declaration/source-level output | [ch04](chapters/ch04-declaration-analysis.md) |
| Work with symbol types or dependency graphs | [ch05](chapters/ch05-symbol-analysis.md) |
| Work with tactics, terms, goals, simp usage, InfoTrees | [ch06](chapters/ch06-elaboration-and-goals.md) |
| Work with imports, line states, or AST output | [ch07](chapters/ch07-module-line-and-ast.md) |
| Add/change an analyzer feature or test it | [ch08](chapters/ch08-extension-and-testing.md) |

For fast decisions, load [cheatsheet.md](cheatsheet.md). For exact terms, load [glossary.md](glossary.md). For implementation patterns, load [patterns.md](patterns.md).

## Core Operating Model

### 1. Match the Lean toolchain before debugging anything else
jixia loads compiled Lean artifacts and elaboration internals. Use the **exact** Lean version of the target project. A nearby version can fail with `invalid header`, missing constants, or internal elaboration errors.

**Procedure**
1. Read the target project's `lean-toolchain`.
2. Build a jixia branch/tag with that same Lean version.
3. Build the target before symbol-aware analysis.
4. Run inside the target project's Lake environment when project search paths are required.

### 2. Choose the data product from the question
- **Module/import metadata** → `-m`
- **Source-level declarations** → `-d`
- **Elaborated symbols and reference graph** → `-s`
- **Terms, tactics, goal transitions, simp usage** → `-e`
- **Proof state by source position** → `-l`
- **Raw parsed commands / AST** → `-a`
- **Initializer execution when required** → add `-i`

Only requested outputs are produced.

### 3. Treat the analyzer as two execution paths
The general plugin registry contains **module**, **declaration**, **elaboration**, and **line**. `Process.lean` generates option fields, on-load hooks, and result dispatch from that registry.

**Symbol** and **AST** are special cases in `Main.lean`:
- Symbol analysis imports the built module/environment after file processing and computes constant/reference data.
- AST output serializes the final parsed command array from frontend state.

When extending jixia, decide which path matches the data dependency before editing the registry.

### 4. Preserve semantic distinctions in the output
- Source positions/ranges are **byte offsets**.
- `typeReferences` means names needed by a symbol's **statement/type**.
- `valueReferences` means names used by its **definition/proof**; it may be absent when a symbol has no value.
- Tactic output records **before** and **after** goals, plus dependency metadata and optional tactic-specific extras.
- Pretty-printed syntax/types can fail; nullable fields and fallback strings are part of the design.

### 5. Keep InfoTrees intact for tactic/line analysis
Declaration, elaboration, and line analysis install pre-processing hooks. Elaboration and line output depend on InfoTrees. jixia defaults `Elab.async` to false when the caller has not set it, because asynchronous elaboration can omit tactic nodes needed by the analyzer.

## Failure Recovery

| Symptom | First diagnosis | Recovery |
|---|---|---|
| `Unknown module prefix ...` | jixia lacks project search paths | Run from the project root with `lake env` |
| `... cannot evaluate [init] declaration` | Initializers disabled | Add `-i` |
| `invalid header` | Lean binary/artifact mismatch | Rebuild jixia with the target's exact `lean-toolchain`; rebuild target artifacts |
| Symbol output cannot load the module | Target not built or wrong environment | Build target first; run under project `lake env`; re-check exact Lean version |
| Elaboration/line data is unexpectedly sparse | Missing InfoTree nodes | Keep `Elab.async=false`; avoid disabling info trees |
| Pretty-readable field is absent | Pretty-printer failure | Use the available fallback field; do not infer missing text |
| Source range appears off with non-ASCII text | Character offset assumption | Interpret positions as bytes |

If two diagnoses remain plausible, check **toolchain → build state → Lake environment → requested flags → InfoTree availability** in that order.

## Extension Decision

Use the registry pattern when a feature fits:
1. optional `onLoad : CommandElabM Unit`,
2. `getResult`,
3. normal JSON output after command processing.

Use a special `Main.lean` path when the feature fundamentally needs post-run file/environment handling or raw frontend state, as Symbol and AST do.

For a general plugin:
1. define result structures in `Analyzer/Types.lean`;
2. add `ToJson` support in `Analyzer/Output.lean`;
3. implement the processor;
4. register its names in `Analyzer.Process.plugins`;
5. expose the CLI flag in `jixiaCommand`;
6. add an `Example.lean` case that exercises the new data;
7. run the relevant output and inspect JSON shape and failure behavior.

## SELF_CHECK

Before answering or proposing a patch, verify:
- Did I identify whether the target is standalone or in a Lake project?
- Did I check exact Lean-version compatibility before chasing downstream errors?
- Did I select the smallest output/plugin set that answers the question?
- Did I keep byte ranges, optional pretty fields, and type/value references distinct?
- If the task concerns tactics or lines, is InfoTree collection available?
- If extending the analyzer, does the feature belong in the registry or a special post-run path?
- Did I preserve current JSON conventions and test with a representative `Example.lean` construct?
- If evidence is insufficient, did I state the missing prerequisite instead of inventing output?

## Chapter Index

| # | Title | Key frameworks |
|---|---|---|
| [ch01](chapters/ch01-build-and-run.md) | Build and Run | exact-toolchain rule, standalone vs project flow, failure triage |
| [ch02](chapters/ch02-data-model-and-json.md) | Data Model and JSON | schema layers, byte ranges, rendering fallbacks |
| [ch03](chapters/ch03-pipeline-and-plugin-lifecycle.md) | Pipeline and Plugin Lifecycle | registry-generated dispatch, accumulation, special paths |
| [ch04](chapters/ch04-declaration-analysis.md) | Declaration Analysis | binder reconstruction, scope capture, elaborator interception |
| [ch05](chapters/ch05-symbol-analysis.md) | Symbol Analysis | module import, constant classification, dependency graph |
| [ch06](chapters/ch06-elaboration-and-goals.md) | Elaboration and Goals | goal snapshots, dependency tracing, simp provenance |
| [ch07](chapters/ch07-module-line-and-ast.md) | Module, Line, and AST | import metadata, proof state by position, raw command AST |
| [ch08](chapters/ch08-extension-and-testing.md) | Extension and Testing | extension checklist, route selection, fixture design |

## Topic Index

- **AST** → ch03, ch07, ch08
- **byte source ranges** → ch02, ch04, ch07
- **declaration JSON** → ch02, ch04
- **Elab.async** → ch01, ch03, ch06
- **elaboration tree** → ch02, ch06
- **exact Lean version** → ch01, ch05
- **goals / local context** → ch02, ch06, ch07
- **initializers / `-i`** → ch01
- **InfoTree** → ch03, ch06, ch07
- **Lake environment / `lake env`** → ch01, ch05
- **plugin registry** → ch03, ch08
- **proof state by line** → ch07
- **scope info** → ch02, ch04
- **simp used theorems** → ch06
- **symbol reference graph** → ch02, ch05
- **typeReferences / valueReferences** → ch05

## Supporting Files

- [glossary.md](glossary.md) — exact project terms and output fields
- [patterns.md](patterns.md) — reusable implementation and diagnostic patterns
- [cheatsheet.md](cheatsheet.md) — output-selection, failure, and extension decision tables

## Scope & Limits

This skill covers the uploaded repository snapshot and its documented/code-visible behavior. The snapshot pins Lean v4.29.0, while the README emphasizes that jixia must match the target project's exact Lean version. Validate branch-specific API details against the source when working on another jixia release. The build itself was not compiled in this environment because Lean/Lake are unavailable here; code-level guidance is source-derived and installability validation applies to this skill package.
