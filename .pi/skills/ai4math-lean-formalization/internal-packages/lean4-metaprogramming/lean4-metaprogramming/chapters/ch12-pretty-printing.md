# Chapter 12: Pretty Printing

## Core Idea
Pretty printing is a semantic reverse pipeline: delaboration chooses syntax for an expression, parenthesization restores grouping, and formatting chooses layout. Extensions must preserve re-elaboratable meaning.

## Frameworks Introduced
- **Delaborator pattern**: register a handler for a recognizable expression shape, inspect the current subexpression/context, and return syntax representing the same meaning.
- **Unexpander pattern**: reverse a selected application form into user-facing syntax when the transformation is simple and syntax-driven.
- **Round-trip validation**: custom output is acceptable only when re-elaboration yields an equivalent expression in the intended context.

## Key Concepts
- **Delaboration**: `Expr → Syntax` under a `DelabM` context.
- **`DelabM`**: supports syntax quotation plus relevant meta/context operations and pretty-printer options.
- **Subexpression**: expression currently being delaborated.
- **Delaborator registration**: associates a handler with an expression head/shape such as an application of a constant.
- **Unexpander**: syntax-level reverse expansion associated with an application head.
- **Parenthesizer**: inserts parentheses after delaboration/unexpansion based on syntax precedence.
- **Formatter**: converts parenthesized syntax to concrete layout.

## Mental Models
Think of a delaborator as a semantics-preserving projection from internal terms back into a convenient surface language. Several surface forms may denote the same expression; choose a form that is stable, readable, and accepted by the ordinary elaborator.

Think of an unexpander as a lightweight inverse macro for a known application head. It sees syntax produced by lower-level delaboration before the parenthesizer has inserted grouping parentheses.

Treat handler failure as fallback, not catastrophe. If a custom printer cannot prove its shape assumptions, let a more general printer render the term.

## Anti-patterns
- **Returning attractive syntax that elaborates differently**: display becomes misleading and can break copy/paste workflows.
- **Matching parentheses inside an unexpander**: parenthesization runs later, so expected parentheses may not exist yet.
- **Overly broad delaborators**: a handler should recognize a precise semantic shape and fail cleanly outside it.
- **Reconstructing implicit arguments users normally should not see** when a higher-level notation is available.

## Code Examples
```lean
-- Distilled delaborator registration shape.
@[delab app.someHead]
def delabSomeHead : Delab := do
  let e ← getExpr
  -- inspect e; return quoted Syntax when the shape is supported
  ...
```
```lean
-- Distilled unexpander idea: match the application syntax and
-- return the surface notation, otherwise fail so fallback printing runs.
```
- **What it demonstrates**: printer extensions are partial handlers with semantic/fallback discipline.

## Reference Tables
| Layer | Transformation | Primary responsibility |
|---|---|---|
| Delaborator | `Expr → Syntax` | choose semantic surface form |
| Unexpander | application syntax → nicer syntax | reverse simple expansions |
| Parenthesizer | syntax → grouped syntax | precedence-safe grouping |
| Formatter | syntax → `Format`/text | layout and spacing |

## Key Takeaways
1. Validate custom printing by semantic round trip.
2. Use delaborators for context-aware expression-to-syntax choices.
3. Use unexpanders for simple inverse syntax patterns tied to a constant/application.
4. Remember unexpanders run before parentheses are added.
5. Fail cleanly and preserve fallback printing when assumptions do not hold.

## Connects To
- **Ch 2**: completes the reverse side of the compiler pipeline.
- **Ch 5–7**: printed syntax must parse and elaborate correctly.

## Operational Procedure
Start a printer extension from a concrete elaborated expression and the surface syntax you want users to see. Decide whether the rule is tied to a simple application head (candidate unexpander) or requires semantic/contextual inspection (candidate delaborator). Make the handler partial: verify the exact shape, construct syntax with quotations, and fail cleanly on all other forms. Then test nested occurrences, precedence-sensitive contexts, implicit arguments, and a parse/elaborate round trip. A rendering rule that works only at the top level is incomplete if nested forms can occur.

When several printer handlers could apply, prefer the most specific rule to claim only the expressions it can faithfully represent. Let general fallback printing preserve debuggability for edge cases.

A final check should compare nested and top-level renderings under ordinary printer options.
