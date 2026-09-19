# Chapter 5: Symbol Analysis

## Core Idea
Symbol analysis operates on Lean's elaborated environment after the target module is available. It classifies constants, renders their types, detects proposition-valued symbols, and builds separate reference sets for statements and definitions/proofs.

## Frameworks Introduced
- **Statement-vs-value dependency split**
  - When to use: building graphs or ML features from Lean constants.
  - How: traverse the symbol's type for `typeReferences`; traverse its optional value for `valueReferences`.
- **Environment-scoped extraction**
  - When to use: avoid reporting imported dependency symbols as if defined in the target file.
  - How: import the target module, find its module index, and keep constants whose module index equals that target index.
- **Robust type rendering**
  - When to use: human-readable output can fail.
  - How: attempt full/readable pretty printing and always retain `dbgToString` fallback.

## Key Concepts
- **`references Expr`**: recursive constant-name collector with visited-expression-data deduplication.
- **`SymbolKind`**: axiom, definition, theorem, opaque, quotient, inductive, constructor, recursor.
- **`isProp`**: determined by checking whether the symbol type itself has sort `Prop`.
- **`getSrcSearchPath` + sysroot source path**: establishes module lookup paths.
- **`searchModuleNameOfFileName`**: maps file path to Lean module name.
- **`importModules`**: loads the compiled target environment with extensions.

## Mental Models
- Treat symbol analysis as **compiled-environment analysis**, while declaration analysis is **source-command analysis**.
- Treat reference edges as **semantic constant dependencies**, not textual identifier occurrences.
- Treat module-index filtering as the boundary between **target-owned symbols** and imports.

## Anti-patterns
- **Running Symbol before the target is built**: module import can fail or load stale artifacts.
- **Ignoring exact Lean version**: compiled headers and environment internals are version-sensitive.
- **Merging type/value references without labeling them**: erases the distinction between statement vocabulary and proof/definition dependencies.
- **Assuming all constants are from the target**: imported constants must be filtered out.

## Code Examples
```lean
let typeReferences := references info.type
let valueReferences := info.value?.map references
```
- **What it demonstrates**: the two dependency graphs are intentionally separate and `valueReferences` preserves absence.

## Reference Tables

| Question | Prefer |
|---|---|
| What concepts are needed to state theorem `T`? | `typeReferences` |
| What lemmas/definitions does `T`'s proof or body use? | `valueReferences` |
| Is the constant proposition-valued? | `isProp` |
| Need a readable type? | `typeReadable`, then fallback |
| Need fully qualified/expanded rendering? | `typeFull`, then fallback |

## Worked Example
You want training data for theorem-premise prediction from one target file.

1. Build the project using the target's exact Lean toolchain.
2. Run jixia with symbol output enabled under `lake env`.
3. Keep target module symbols only; jixia already filters by module index.
4. For each theorem, use `typeReferences` as statement context and `valueReferences` as observed proof dependencies.
5. Preserve `none` for symbols without a value rather than converting it silently to an empty proof set.
6. Join source-level declaration ranges from declaration output if training examples also need source coordinates.

## Key Takeaways
1. Symbol analysis needs a real Lean environment, so build/version problems surface here first.
2. Reference collection is semantic over `Expr` constants.
3. Target-module filtering prevents imported-library contamination.
4. Statement and value graphs serve different downstream tasks.
5. Keep rendering fallbacks available to robust consumers.

## Connects To
- **Ch 1**: environment preparation and exact-version recovery.
- **Ch 2**: `SymbolInfo` field semantics.
- **Ch 4**: combine symbol semantics with source declaration ranges.
