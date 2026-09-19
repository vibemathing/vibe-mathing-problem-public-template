# Chapter 1: Build and Run

## Core Idea
jixia is tightly coupled to Lean's compiled artifacts and elaborator internals. Successful analysis starts with exact toolchain alignment, a built target, and the correct Lake environment.

## Frameworks Introduced
- **Exact-toolchain rule**
  - When to use: before every build/run investigation.
  - How: read the target `lean-toolchain`; build the matching jixia branch/tag; rebuild target artifacts under the same Lean version.
  - Why it works: imported `.olean` files and internal APIs are version-sensitive.
- **Standalone vs project route**
  - When to use: deciding how to prepare and invoke a target file.
  - How: standalone file → compile its `.olean` first; project file → build from project root and invoke jixia through `lake env`.
- **Output-minimization rule**
  - When to use: every run.
  - How: request only the JSON products needed for the current question; omitted flags skip their output path.

## Key Concepts
- **`lean-toolchain`**: the authoritative Lean version for a project.
- **Lake environment**: the search path and package context made available by `lake env`.
- **`.olean`**: compiled Lean module artifact needed by module-aware loading.
- **Initializer execution**: optional runtime behavior enabled by jixia's `-i` flag.
- **`-D` option**: Lean option accepted by jixia as `-Dkey=value` or `-Dkey`.
- **`Elab.async`**: Lean elaboration option that jixia defaults to false when unset to preserve tactic data.

## Mental Models
- Treat jixia as a **version-matched compiler companion**, not a generic text parser.
- Treat `lake env` as **dependency-path injection** for the analyzed project.
- Treat each output flag as a **data contract**: ask for the minimum contract needed.

## Anti-patterns
- **Reusing a nearby-version jixia binary**: can yield `invalid header`, missing constants, or internal elaboration failures.
- **Running a project file outside its Lake environment**: commonly produces unknown-module errors.
- **Skipping the target build before symbol analysis**: leaves no reliable compiled module for environment import.
- **Enabling asynchronous elaboration while expecting complete tactic trees**: can reduce InfoTree coverage.

## Code Examples
```sh
# Standalone target: create compiled artifact first
lake env lean -o Example.olean Example.lean

# Request declaration, symbol, elaboration, and line outputs
/path/to/jixia -d Example.decl.json -s Example.sym.json \
  -e Example.elab.json -l Example.lines.json Example.lean
```

```sh
# Project target: execute inside the project's Lake environment
lake env /path/to/jixia -d Example.decl.json -s Example.sym.json Example.lean
```

- **What it demonstrates**: target preparation differs; the analyzer flags stay the same.

## Reference Tables

| Flag | Output | Use when |
|---|---|---|
| `-m` / `--module` | module JSON | imports and module docstrings |
| `-d` / `--declaration` | declaration JSON | source-level declaration structure |
| `-s` / `--symbol` | symbol JSON | elaborated types and reference graph |
| `-e` / `--elaboration` | elaboration JSON | tactics, terms, goal transitions |
| `-l` / `--line` | line JSON | proof state by source position |
| `-a` / `--ast` | AST JSON | raw parsed command syntax |
| `-i` / `--initializer` | no file; execution mode | target requires initializers |

## Worked Example
A project file fails with `Unknown module prefix Mathlib`.

1. Confirm the target is inside a Lake project.
2. From the project root, fetch/build dependencies as the project normally requires.
3. Re-run jixia through `lake env`, keeping output flags unchanged.
4. If the next failure is `invalid header`, compare target and jixia `lean-toolchain` exactly and rebuild jixia for that version.
5. If mathlib or another package needs initializers, add `-i` only after environment/version checks.

## Key Takeaways
1. Version alignment comes before code-level diagnosis.
2. Build the target before asking for environment-derived symbol data.
3. Use `lake env` for project files.
4. `-i` fixes initializer-specific failures; it is not a general compatibility fix.
5. Keep `Elab.async=false` when complete tactic data matters.

## Connects To
- **Ch 3**: the CLI flags become plugin options and lifecycle decisions.
- **Ch 5**: symbol analysis depends most strongly on built-module/environment correctness.
- **Ch 6**: elaboration completeness depends on InfoTree availability.
