# Chapter 3: Pipeline and Plugin Lifecycle

## Core Idea
jixia centralizes the normal plugin lifecycle in a registry and uses Lean metaprogramming to generate option fields and dispatch code, while keeping Symbol and AST as deliberate special paths.

## Frameworks Introduced
- **Registry-generated plumbing**
  - When to use: a plugin has normal on-load + result behavior.
  - How: register `(name, {getResult, onLoad?})`; generated code derives `Options`, on-load hooks, result dispatch, and CLI-option parsing logic tied to the same names.
- **Two-phase plugin lifecycle**
  - When to use: reasoning about why a plugin needs setup before elaboration.
  - How: `onLoad` hooks run first; commands are processed; `getResult` runs after the file state has accumulated.
- **State-accumulation guard**
  - When to use: whole-file InfoTrees/messages must survive command-by-command elaboration.
  - How: save previous trees/messages, process one command, append old state, recurse until done.
- **Special-path escape hatch**
  - When to use: a feature needs file-path/environment import or raw frontend state beyond the normal registry contract.

## Key Concepts
- **`PluginOption.ignore`**: plugin disabled.
- **`PluginOption.json path`**: plugin enabled and serialized to the path.
- **`Process.plugins`**: array of general plugin registrations.
- **`impl_onLoad`**: generated function that invokes hooks only for enabled plugins.
- **`impl_process`**: generated function that computes/outputs enabled plugin results.
- **`processCommandsAccum`**: custom frontend loop that preserves InfoTrees and messages across commands.
- **`run`**: lifecycle coordinator: setup → process → result collection.
- **`runCommand`**: CLI-facing entry: load file, set main module, run general plugins, then AST/Symbol special outputs.

## Mental Models
- Treat `Process.plugins` as a **single source of truth for routine plugin plumbing**.
- Treat `onLoad` as **instrumentation installation** and `getResult` as **post-file extraction**.
- Treat Symbol/AST as evidence that **not every feature should be forced into one abstraction**.

## Anti-patterns
- **Adding a general plugin in multiple handwritten switch statements**: defeats the registry's code-generation purpose and creates drift.
- **Putting Symbol into the registry without preserving its module-import requirements**: risks changing semantics.
- **Dropping accumulated InfoTrees/messages between commands**: breaks whole-file elaboration and line analysis.
- **Running output actions for ignored plugins**: wastes work and violates the optional-output contract.

## Code Examples
```lean
protected def plugins : Array (Name × Plugin) := #[
  (`module,      ⟨ ``Module.getResult, none ⟩),
  (`declaration, ⟨ ``Declaration.getResult, ``Declaration.onLoad ⟩),
  (`elaboration, ⟨ ``Elaboration.getResult, ``Elaboration.onLoad ⟩),
  (`line,        ⟨ ``Line.getResult, ``Line.onLoad ⟩)
]
```
- **What it demonstrates**: names drive routine lifecycle generation; Symbol is absent because it is handled separately.

## Reference Tables

| Feature | General registry? | Setup requirement | Result timing |
|---|---:|---|---|
| module | yes | none | after command processing |
| declaration | yes | command-elaborator hook | after command processing |
| elaboration | yes | enable InfoTree | after command processing |
| line | yes | enable InfoTree | after command processing |
| symbol | no | built module + import environment | special post-run path |
| AST | no | frontend command state | special post-run path |

## Worked Example
You want a new `diagnostics` output that collects information during elaboration and returns one JSON array at the end.

1. Decide whether data can be captured through a pre-processing hook and read after the file runs.
2. Define its result types and JSON encoding.
3. Implement `Diagnostics.onLoad` if instrumentation must be enabled.
4. Implement `Diagnostics.getResult`.
5. Add one registry entry; let generated option/dispatch code follow the plugin name.
6. Add a CLI flag with the same logical name.
7. If the implementation instead requires reopening the compiled module from the target file path, follow Symbol's special path design.

## Key Takeaways
1. Registry entries eliminate repetitive option and dispatch plumbing.
2. Hooks must be installed before command processing.
3. Whole-file state accumulation is deliberate compatibility behavior.
4. Symbol and AST define the boundary of the general abstraction.
5. Preserve the same name across registry, CLI, and output expectations.

## Connects To
- **Ch 6**: InfoTree-dependent plugins rely on this lifecycle.
- **Ch 8**: extension routing starts by choosing registry vs special path.
