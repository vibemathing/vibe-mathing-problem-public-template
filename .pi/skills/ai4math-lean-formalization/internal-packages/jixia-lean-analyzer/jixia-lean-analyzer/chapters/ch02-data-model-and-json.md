# Chapter 2: Data Model and JSON

## Core Idea
jixia normalizes Lean's syntax, declarations, symbols, goals, elaboration nodes, module metadata, and line states into explicit structures, then serializes them with predictable JSON conventions and graceful fallbacks.

## Frameworks Introduced
- **Layered schema model**
  - When to use: interpreting output or designing a new plugin result type.
  - How: source syntax → semantic record → optional/fallback renderings → JSON.
- **Dual-representation rule**
  - When to use: when exact source location and human-readable text both matter.
  - How: preserve source range/originalness while separately storing pretty-printed text.
- **Fallback-first rendering**
  - When to use: any consumer that reads type/syntax strings.
  - How: treat pretty output as optional; use fallback strings or raw range metadata when rendering fails.

## Key Concepts
- **`PPSyntax`**: `original`, optional byte `range`, optional pretty-printed `pp?`.
- **`PPSyntaxWithKind`**: `PPSyntax` plus syntax `kind`.
- **`ScopeInfo`**: variables, include/omit sets, universe level names, namespace, open declarations, scoped opens.
- **`BaseDeclarationInfo`**: declaration kind, source ref, name syntax, full name, modifiers, signature, parameters, optional type/value, scope.
- **`InductiveInfo`**: declaration info plus constructor records.
- **`SymbolInfo`**: symbol kind, renderings, type/value references, `isProp`.
- **`Variable`**: local declaration with binder/type/value/proposition/let/reference-later metadata.
- **`Goal`**: tag, local context, metavariable id, type, proposition flag, pretty form, optional extra JSON.
- **`ElaborationTree`**: recursive info node + source syntax ref + children.
- **`LineInfo`**: source start byte plus visible goal state.

## Mental Models
- Think of source ranges as **byte coordinates**, especially with Unicode source text.
- Think of `typeReferences` and `valueReferences` as **statement dependencies vs implementation/proof dependencies**.
- Think of `Goal.extra?` and tactic `extra?` as **extension points** that preserve the stable core schema.

## Anti-patterns
- **Treating byte positions as Unicode character indices**: shifts source mapping for non-ASCII files.
- **Assuming every pretty-printed field exists**: source code explicitly catches rendering failures.
- **Flattening Name values to one string without checking consumer expectations**: jixia serializes Lean `Name` as JSON path components.
- **Treating a missing `valueReferences` as an empty proof graph**: absence can mean the symbol has no value.

## Code Examples
```lean
structure SymbolInfo where
  kind : SymbolKind
  name : Name
  typeFull : Option String
  typeReadable : Option String
  typeFallback : String
  typeReferences : HashSet Name
  valueReferences : Option (HashSet Name)
  isProp : Bool
```
- **What it demonstrates**: high-value fields separate robust fallback data from optional renderings and separate type/value dependency edges.

## Reference Tables

| JSON concept | Meaning | Reliability note |
|---|---|---|
| `range: [start, stop]` | source byte interval | byte-based |
| `original` | syntax originates from source head info | macros/expansion can change it |
| `pp` / readable text | human-facing pretty form | may be absent |
| `typeFallback` | debug representation | use when pretty type fails |
| `context` | local variables visible in a goal/term | implementation details filtered |
| `before` / `after` | tactic goal snapshots | depends on InfoTree coverage |
| `extra` | plugin-specific metadata | optional by design |

## Worked Example
Suppose a symbol JSON item has a readable type, two `typeReferences`, three `valueReferences`, and `isProp=true`.

Interpret it as follows:
1. The item is proposition-valued, so it likely represents a theorem/axiom-like statement or proposition definition.
2. The two type references are the named constants needed to state its type.
3. The three value references are the constants used in its proof/definition body.
4. When constructing a theorem-dependency graph, choose the edge set based on the question: statement vocabulary, proof dependencies, or both.
5. When linking back to source, use declaration/source range records rather than searching by rendered text.

## Key Takeaways
1. jixia outputs are structured around semantic distinctions, not one generic syntax dump.
2. Preserve optionality when consuming JSON.
3. Byte offsets are a hard interface detail.
4. Use statement and value dependency graphs for different questions.
5. Extend schemas through explicit structures and `ToJson` instances.

## Connects To
- **Ch 4**: declaration records are the main source-level schema.
- **Ch 5**: symbol fields form dependency graphs.
- **Ch 6**: goals and elaboration trees reuse these schema conventions.
