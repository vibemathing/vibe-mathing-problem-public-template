# Chapter 6: Macros

## Core Idea
Macros are hygienic `Syntax → Syntax` rewrites. Use them when the meaning of a feature can be expressed completely as another Lean syntax form without consulting types or semantic context.

## Frameworks Introduced
- **Expansion by handler fallback**: several macro handlers may target the same syntax kind; a handler recognizes its supported shape or yields `throwUnsupported` so another handler can try.
- **Hygienic generation**: quoted identifiers receive macro scopes that distinguish generated names from user names and prevent accidental capture.
- **Quotation-driven rewrite**: match input with a syntax quotation, capture subtrees with antiquotations, then construct output with another quotation.

## Key Concepts
- **`Macro`**: function from syntax to syntax in `MacroM`.
- **`macro_rules`**: concise declaration of pattern-driven expansion rules.
- **Quotation category**: explicit category such as term, command, or a custom category.
- **Antiquotation**: splice captured syntax into a generated quotation.
- **Splice/repetition antiquotation**: inject arrays or optional/repeated syntax fragments.
- **Macro scope**: hygiene marker attached to generated identifiers.
- **`mkIdent`**: creates an identifier intentionally referring to a chosen surface name.
- **`withFreshMacroScope`**: generates a fresh hygiene scope for repeated/dynamic expansion work.
- **`withRef`**: controls source reference used for diagnostics.

## Mental Models
Use a macro as a transparent desugaring rule. A user reading the expansion should be able to see where the semantics come from in ordinary Lean constructs. If the macro would need to ask “what type is this?” or “which declaration does this name resolve to?”, move the decision to elaboration.

Think of hygiene as automatic alpha-renaming for generated names. It protects both sides: user variables should not capture macro internals, and macro-introduced binders should not accidentally capture user syntax.

Treat source references as part of usability. When generated syntax fails later, attach a meaningful source location so the error points to the user's construct.

## Anti-patterns
- **Hiding semantic algorithms in macros**: expansion loses access to the semantic information required to make robust decisions.
- **Generating a public/user-visible identifier hygienically by accident**: a fresh scope can prevent the name from being found as the user expects; explicitly construct such names when exposure is intentional.
- **Manual child-array surgery for regular syntax**: quotations and splices make expansion safer and clearer.
- **A handler throwing a hard error for a merely unsupported shape** when another registered handler should get a chance.

## Code Examples
```lean
-- Distilled syntax-sugar macro.
syntax "twice " term : term
macro_rules
  | `(twice $t) => `(($t, $t))
```
```lean
-- For an intentionally surface-visible identifier:
let userName := mkIdent `generatedName
```
- **What it demonstrates**: rewrite structure with quotations; bypass hygiene only as a deliberate interface decision.

## Reference Tables
| Question | Macro choice |
|---|---|
| Pure alias/desugaring? | Macro |
| Needs expected type/local context? | Term elaborator |
| Generated private binder? | Keep hygienic scoped identifier |
| Generated name must be user-addressable? | Consider explicit `mkIdent` |
| Dynamic list of syntax fragments? | Repetition/splice antiquotations |
| Handler does not own this shape? | `throwUnsupported` |

## Key Takeaways
1. Use macros for visible syntax-to-syntax transformations.
2. Preserve hygiene by default; break it only for intentional user-facing names.
3. Use quotation patterns and splices as the primary macro implementation technique.
4. Let unsupported handlers fall through when extension overloading is intended.
5. Attach useful source references to generated syntax for diagnostics.

## Connects To
- **Ch 5**: defines the syntax trees macros consume and produce.
- **Ch 7**: handles meaning that requires semantic context.
- **Ch 9**: tactic macros can expand into ordinary tactic syntax.

## Operational Procedure
Review a macro expansion along three axes. **Semantic transparency**: can the resulting ordinary Lean syntax fully express the intended meaning? **Hygiene**: which identifiers come from the user, which are generated, and which generated names must intentionally be addressable later? **Diagnostics**: if generated syntax fails to elaborate, will the source reference point back to the user's construct? If semantic transparency fails, promote the feature to an elaborator. If hygiene requires many deliberate scope escapes, reconsider whether the macro is defining an implicit interface that deserves explicit syntax.

For multiple macro handlers on the same syntax kind, make ownership conditions mutually intelligible. A handler should decline syntax it does not recognize instead of converting an ordinary fallback case into a fatal error.
