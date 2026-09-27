# Chapter 4: Declaration Analysis

## Core Idea
Declaration analysis reconstructs source-level intent before Lean's normal declaration elaborator runs: declaration kind, full name, binders, signature, type/value syntax, constructor structure, and surrounding scope.

## Frameworks Introduced
- **Intercept-then-defer pattern**
  - When to use: collect source information while preserving Lean's normal elaboration behavior.
  - How: a custom command elaborator records declaration info, then signals unsupported syntax so downstream/default elaboration can continue.
- **Binder normalization**
  - When to use: convert Lean binder syntax variants into one `BinderView` representation.
  - How: handle explicit, implicit, strict implicit, instance, hole, default-value, and tactic-generated binders.
- **Scope snapshot**
  - When to use: declaration meaning depends on surrounding variables/namespaces/open scopes.
  - How: capture variable declarations, include/omit sets, universe levels, current namespace, open declarations, and active scoped namespaces.

## Key Concepts
- **`getFullname`**: resolves current namespace, `_root_` prefix, macro scopes, and private naming.
- **`toBinderViews`**: reconstructs a normalized binder array.
- **`getScopeInfo`**: captures command-scope context.
- **`getDeclarationInfo`**: handles def-like declarations plus axiom/inductive/structure cases.
- **`getConstructorInfo`**: extracts constructor names, binders, types, modifiers, and source refs.
- **`declRef`**: process-level accumulator for declaration records.
- **`proof_wanted`**: special command rewritten as an axiom for elaboration, then relabeled in captured info.

## Mental Models
- Think of declaration output as **source semantics before lowering**, enriched by namespace/scope context.
- Think of binder handling as **syntax normalization with Lean-specific modifiers**, not string parsing.
- Think of private names as **environment-dependent identities** that need Lean's own private-name constructor.

## Anti-patterns
- **Deriving declaration names by concatenating source tokens**: fails for `_root_`, current namespace, macro scopes, and private declarations.
- **Ignoring scope metadata**: loses implicit context needed to interpret source-level declarations.
- **Treating inductive constructors as unrelated declarations**: jixia nests them under the inductive record.
- **Consuming `type`/`value` as guaranteed strings**: they are optional pretty-syntax records.

## Code Examples
```lean
-- Handler shape: collect source information, then let normal elaboration continue.
def handleDeclaration (stx : Syntax) : CommandElabM Unit :=
  withEnableInfoTree false do
    let info ← getDeclarationInfo stx
    declRef.modify fun a => a.push info
    throwUnsupportedSyntax
```
- **What it demonstrates**: collection is layered into Lean's command-elaborator dispatch without replacing the normal declaration implementation.

## Reference Tables

| Binder form | Normalized binder info |
|---|---|
| `(x : T)` | explicit/default |
| `{x : T}` | implicit |
| `⦃x : T⦄` | strict implicit |
| `[inst : C]` | instance implicit |
| `_` | fresh canonical identifier |
| default/tactic modifier | wrapped as `optParam` / `autoParam` syntax |

## Worked Example
For a namespaced inductive declaration with implicit parameters and scoped notation:
1. Resolve the parent declaration's full name under the current namespace.
2. Normalize all binders into `BinderView` records.
3. Capture the current scope, including active scoped namespaces.
4. Record the inductive declaration's signature/type.
5. For each constructor, derive its name relative to the parent and capture constructor-local binders/type.
6. Emit one inductive JSON record containing its constructors rather than flattening them into unrelated entries.

## Key Takeaways
1. Declaration analysis is source-aware and scope-aware.
2. Lean's own naming/binder utilities are reused or mirrored where private APIs force it.
3. The handler records data without taking over normal declaration elaboration.
4. Constructors belong to the inductive record.
5. Scope snapshots are essential for downstream IDE/ML consumers.

## Connects To
- **Ch 2**: declaration structures and JSON representation.
- **Ch 3**: `onLoad` installs the command-elaborator interception.
- **Ch 8**: source-level plugins can reuse the intercept-then-defer pattern.
