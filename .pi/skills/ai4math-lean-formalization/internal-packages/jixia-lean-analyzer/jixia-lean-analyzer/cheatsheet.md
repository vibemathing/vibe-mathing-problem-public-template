# jixia Decision Cheatsheet

## Pick the output

| Need | Flag | Why |
|---|---|---|
| imports / module docs | `-m` | file-level module context |
| source declaration ranges, binders, scope | `-d` | pre-lowering source semantics |
| elaborated constants and dependency graph | `-s` | compiled-environment semantics |
| tactics, terms, goals, simp usage | `-e` | InfoTree execution trace |
| proof state at source positions | `-l` | editor-style view |
| raw parsed commands | `-a` | parser-level syntax |
| initializers required | `-i` | permits initializer execution |

## Run route

- **Standalone file** → compile `.olean` first → run jixia.
- **Lake project file** → build project → run from project root with `lake env`.
- **mathlib-like project** → obtain/build cached dependencies as the project requires → use `lake env`; add `-i` when initialization is required.

## Failure triage

| Symptom | Do first | Then |
|---|---|---|
| `Unknown module prefix` | use `lake env` from project root | verify project build/search paths |
| initializer evaluation failure | add `-i` | verify project-specific initialization requirements |
| `invalid header` | compare exact `lean-toolchain` | rebuild jixia + target |
| Symbol cannot import target | build target | verify `lake env` + exact version |
| sparse tactics/line goals | check InfoTrees and `Elab.async=false` | check requested `-e`/`-l` flag |
| source positions misalign | use byte offsets | avoid character-index joins |
| pretty type/syntax missing | use fallback/optional handling | do not fabricate text |

## Extend or special-case?

**Use the registry** when the feature has:
- optional setup before command processing;
- a final `getResult` in command elaboration context;
- ordinary JSON output.

**Use a special `Main.lean` path** when it needs:
- target file path + compiled module import (Symbol-shaped), or
- raw final frontend state (AST-shaped).

## Output interpretation rules

- `typeReferences` = dependencies of the statement/type.
- `valueReferences` = dependencies of proof/body; may be absent.
- `before`/`after` = tactic goal state transition.
- tactic `references` = names in tactic syntax, not guaranteed proof dependencies.
- simp `usedTheorems` = stronger provenance for `simp`/`simp_all`/`dsimp`.
- `range` / line `start` = byte positions.

## Patch checklist

1. Match target Lean version.
2. Choose lifecycle route.
3. Define/modify schema.
4. Add JSON serialization.
5. Implement extraction.
6. Register or special-case.
7. Add CLI flag.
8. Add representative `Example.lean` coverage.
9. Build and inspect JSON.
10. Test one failure path.
