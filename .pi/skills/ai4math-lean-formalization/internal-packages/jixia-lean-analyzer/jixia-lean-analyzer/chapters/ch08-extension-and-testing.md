# Chapter 8: Extension and Testing

## Core Idea
Extend jixia by first locating the data's lifecycle: source-command interception, InfoTree instrumentation, post-run compiled environment, or raw frontend state. Then add the smallest schema/processor/CLI change and exercise it on representative Lean syntax.

## Frameworks Introduced
- **Lifecycle-first extension**
  - When to use: adding any analysis product.
  - How: classify when the data exists and which state owns it before choosing code location.
- **Schema → processor → registration → CLI → fixture pipeline**
  - When to use: routine feature work.
  - How: define stable output type; serialize it; implement extraction; wire lifecycle; expose flag; add representative fixture.
- **General-vs-special route test**
  - Registry route: optional setup + final `getResult` in command elaboration context.
  - Special route: needs target path/compiled import or frontend state not represented by the general contract.
- **Failure-oriented fixture design**
  - When to use: protect against silent data loss.
  - How: include constructs that force binders/scopes/tactics/macros/instances/inductives and verify both success data and known failure conditions.

## Key Concepts
- **`Example.lean`**: current broad fixture with theorem tactics, simp/simp_all/rw/rcases, structures, inductives, instances, namespaces, scoped notation, coercion, recursion.
- **`autoImplicit=false` / `relaxedAutoImplicit=false`**: project-level Lean options that make implicit naming behavior stricter.
- **`metalib`**: dependency used for file loading/info helpers.
- **`Cli`**: Lean CLI dependency used to define command flags and positional target file.
- **CI build**: GitHub workflow installs the toolchain from `lean-toolchain` and runs `lake build`.

## Mental Models
- Treat output JSON as an **external interface**: schema changes deserve deliberate compatibility review.
- Treat `Example.lean` as a **coverage seed**, then add targeted cases for every new branch.
- Treat a special path as a **semantic requirement**, not an architectural failure.

## Anti-patterns
- **Adding a field without JSON serialization**: the analyzer compiles but consumers never see the data.
- **Registering a plugin without a CLI flag**: implementation exists but users cannot request output.
- **Forcing post-import Symbol-like logic into `CommandElabM` registry plumbing**: obscures lifecycle requirements.
- **Testing only on a trivial theorem**: misses binders, namespaces, macros, scoped notation, and multi-goal tactics.
- **Changing Lean versions without rebuilding both analyzer and target**: invalidates runtime testing.

## Code Examples
```text
Extension checklist:
Types → ToJson → processor → lifecycle route → CLI flag → Example fixture → JSON inspection
```
- **What it demonstrates**: each feature should have one traceable path from internal data to user-visible output.

## Reference Tables

| Needed data | Best extension hook |
|---|---|
| source declaration syntax/scope | declaration-style command interception |
| tactic/term execution info | enable/traverse InfoTrees |
| proof state at source positions | line-style InfoTree projection |
| compiled constants/module environment | Symbol-style post-run special path |
| raw parsed command syntax | AST-style frontend-state special path |
| file-level imports/docs | normal module `getResult` |

## Worked Example
Add a hypothetical `diagnostics` JSON output for tactic nodes with extra quality metrics.

1. Define `DiagnosticInfo` in `Analyzer/Types.lean` using stable fields and optional extension data.
2. Add `ToJson DiagnosticInfo` in `Analyzer/Output.lean`.
3. If metrics come from InfoTrees, implement `Diagnostics.onLoad := enableInfoTree` and a `getResult` traversal.
4. Register `diagnostics` in `Process.plugins` so option/on-load/result plumbing is generated.
5. Add `x, diagnostics : String` (with the chosen short flag) to `jixiaCommand`.
6. Add an `Example.lean` proof that produces multiple tactic node shapes.
7. Build with the exact toolchain, run only the new flag plus one comparison output such as `-e`, and inspect JSON.
8. Test a failure case with asynchronous elaboration or a mismatched toolchain; confirm the diagnostic guidance is accurate.

## Key Takeaways
1. Choose the lifecycle before choosing the file to edit.
2. Preserve the registry's single-source-of-truth role for routine plugins.
3. Keep Symbol/AST-like special paths explicit when their requirements differ.
4. Treat JSON shape as a public contract.
5. Expand tests around syntax and failure modes, not only happy-path compilation.

## Connects To
- **Ch 3**: registry and special-path architecture.
- **Ch 4**: command interception pattern.
- **Ch 6**: InfoTree extension pattern.
- **Ch 5**: post-run environment pattern.
