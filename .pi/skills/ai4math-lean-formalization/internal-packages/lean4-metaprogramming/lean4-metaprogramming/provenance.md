# Provenance and Coverage Map

## Source Freeze
- Uploaded archive: `04_Metaprogramming_in_Lean_4.zip`.
- Frozen source: offline mirror labeled “Metaprogramming in Lean 4”, captured by `wget` on 2026-09-12 according to the archive README.
- Readable content units: 17 HTML pages — 10 main chapters, 2 extras, 5 solution pages.
- Extracted readable text: ~38,427 words; 264 code blocks; no HTML tables in content pages.
- Overview contains 4 external image references that are not bundled in the uploaded mirror. Their surrounding prose describes the pipeline/conversion concepts used in the skill.
- Author metadata was verified from the upstream repository `book.toml`; methodological content was derived from the uploaded mirror.

## Derivation Labels
- **SOURCE_DERIVED**: method/rule directly supported by book content.
- **STRUCTURAL_SYNTHESIS**: routing or grouping created by combining book concepts without adding a new technical claim.
- **IMPLEMENTATION_DECISION**: packaging/context-efficiency/test choice made by this compiler.

## Source Unit → Skill Coverage
| Source unit | Coverage | Main destination |
|---|---|---|
| 1. Introduction | SOURCE_DERIVED | ch01, SKILL router |
| 2. Overview | SOURCE_DERIVED | ch02, pipeline router |
| 3. Expressions | SOURCE_DERIVED | ch03, glossary |
| 4. MetaM | SOURCE_DERIVED | ch04, patterns, cheatsheet |
| 5. Syntax | SOURCE_DERIVED | ch05 |
| 6. Macros | SOURCE_DERIVED | ch06 |
| 7. Elaboration | SOURCE_DERIVED | ch07 |
| 8. Embedding DSLs By Elaboration | SOURCE_DERIVED | ch08 |
| 9. Tactics | SOURCE_DERIVED | ch09 |
| 10. Lean4 Cheat-sheet | SOURCE_DERIVED | ch10, cheatsheet.md |
| Extra: Options | SOURCE_DERIVED | ch11 |
| Extra: Pretty Printing | SOURCE_DERIVED | ch12 |
| Solutions: Expressions | SOURCE_DERIVED | ch03 Exercise-backed Validation |
| Solutions: MetaM | SOURCE_DERIVED | ch04 Exercise-backed Validation |
| Solutions: Syntax | SOURCE_DERIVED | ch05 Exercise-backed Validation |
| Solutions: Elaboration | SOURCE_DERIVED | ch07 Exercise-backed Validation |
| Solutions: Tactics | SOURCE_DERIVED | ch09 Exercise-backed Validation |

## Capability Provenance
| Capability | Derivation | Source |
|---|---|---|
| Stage-based routing: syntax → macro → elaboration → tactic | STRUCTURAL_SYNTHESIS | Introduction + Overview + Syntax/Macros/Elaboration/Tactics |
| Macro vs elaborator decision | SOURCE_DERIVED | Overview; Macros; Elaboration |
| Raw `Expr` invariant discipline | SOURCE_DERIVED | Expressions + expression solutions |
| `instantiateMVars` before structure-sensitive inspection | SOURCE_DERIVED | MetaM |
| Goal/local-context discipline | SOURCE_DERIVED | MetaM; Tactics |
| Prefer `whnf` for head inspection | SOURCE_DERIVED | MetaM computation section |
| Transparency-aware computation | SOURCE_DERIVED | MetaM computation section |
| Treat `isDefEq` as stateful/unifying | SOURCE_DERIVED | MetaM + MetaM solutions |
| Explicit rollback for speculative meta operations | SOURCE_DERIVED | MetaM backtracking section |
| Local-fvar binder construction | SOURCE_DERIVED | MetaM constructing expressions |
| `mkAppM` → `mkAppOptM` escalation | SOURCE_DERIVED | MetaM applications |
| Hygienic quotation-based macro rewrite | SOURCE_DERIVED | Macros |
| Postpone type-directed elaboration | SOURCE_DERIVED | Elaboration |
| Recursive DSL syntax-to-semantic-expression compilation | SOURCE_DERIVED | DSL chapter |
| Tactic goal-list/metavariable consistency | SOURCE_DERIVED | Tactics + tactic solutions |
| Round-trip-safe delaboration/unexpansion | SOURCE_DERIVED | Pretty Printing |
| Version-specific API verification | IMPLEMENTATION_DECISION | Technical maintenance safeguard; exact API stability is outside the frozen book |
| Progressive loading via 12 topic files | IMPLEMENTATION_DECISION | book-to-skill architecture + source dependency graph |

## Knowledge Graph
`Syntax → Macros`

`Expr → MetaM → Elaboration → DSLs`

`Syntax + MetaM → Elaboration`

`Macros + Elaboration + MetaM → Tactics`

`Expr + Syntax + Elaboration → Pretty Printing round-trip`

`Options → configurable behavior across elaboration/tactics/printing`

## Method Dependency Graph
1. Parse/design grammar before macro or elaborator implementation.
2. Use `Expr` fundamentals before raw term construction.
3. Use `MetaM` context/metavariable discipline before semantic elaborators or tactics.
4. Choose macro only when no semantic context is required.
5. Use elaboration for type/context-directed interpretation; add postponement when constraints are unresolved.
6. For tactics, preserve both metavariable assignments and tactic goal-list state.
7. For pretty printing, validate against the ordinary parse/elaboration pipeline.
