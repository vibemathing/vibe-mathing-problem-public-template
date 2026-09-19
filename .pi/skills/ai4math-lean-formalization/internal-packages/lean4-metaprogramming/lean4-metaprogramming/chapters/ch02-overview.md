# Chapter 2: Overview

## Core Idea
The fastest way to design a Lean extension is to place it in the parse → macro expansion → elaboration → kernel pipeline, then use the earliest stage that has enough information.

## Frameworks Introduced
- **Staged transformation pipeline**:
  - Parse: source text → `Syntax`.
  - Macro expansion: `Syntax → Syntax`, repeatedly until no applicable expansion remains.
  - Elaboration: `Syntax` + context/expected type → `Expr`.
  - Evaluation/compilation: elaborated declarations become executable or kernel-checkable structures.
  - Printing reverses direction: `Expr → Syntax → Format`.
- **Macro vs elaboration rule**:
  - Use a macro for transparent, context-free syntactic sugar.
  - Use elaboration when behavior depends on types, names, coercions, local context, type classes, metavariables, or control flow that should not be hidden in expansion.

## Key Concepts
- **Syntax kind**: identifier used to dispatch syntax handlers.
- **Macro handler**: attempts to rewrite syntax and may decline unsupported forms.
- **Term elaborator**: interprets term syntax with an optional expected type.
- **Command elaborator**: interprets top-level command syntax and can affect environment/state.
- **Tactic elaborator**: interprets tactic syntax while manipulating proof goals.
- **Delaboration**: converts an expression to display syntax.
- **Formatter**: turns syntax into layout/text.

## Mental Models
Think of each stage as gaining semantic information while losing some direct surface structure. Syntax knows exactly how input was parsed but not its type. `Expr` knows the elaborated meaning but may no longer preserve the user's original notation. Pick the stage whose information trade-off fits the transformation.

Treat syntax dispatch as extensible pattern matching: multiple handlers can share a syntax kind, and an unsupported handler can allow the next one to run.

Use `logInfo` for normal metaprogram feedback that belongs in Lean's message system. Use tracing/debug output for developer diagnostics, not user-facing behavior.

## Anti-patterns
- **Semantic macros**: encoding type-dependent or context-sensitive meaning in a syntax rewrite makes errors and tooling worse.
- **Elaborators for trivial aliases**: an elaborator is unnecessary overhead when one hygienic macro expansion completely expresses the feature.
- **Assuming a partial metaprogram proves false statements**: nontermination/crashes can harm tooling, but accepted proof terms still pass the kernel.
- **Expecting one surface syntax form to survive elaboration**: multiple notations can elaborate to the same `Expr`; printing must choose a representation.

## Code Examples
```lean
-- Distilled signatures that reveal the information boundary.
abbrev TermElab := Syntax → Option Expr → TermElabM Expr
abbrev CommandElab := Syntax → CommandElabM Unit
```
- **What it demonstrates**: term elaboration receives an expected type, while command elaboration primarily produces effects.

## Reference Tables
| Stage | Input | Output | Knows types/context? |
|---|---|---|---|
| Parser | characters/tokens | `Syntax` | No |
| Macro | `Syntax` | `Syntax` | Normally no |
| Term elaborator | `Syntax`, expected type | `Expr` | Yes |
| Tactic | tactic `Syntax`, goals | new goals/proofs | Yes |
| Delaborator | `Expr` | `Syntax` | Can query meta context |

## Key Takeaways
1. Route by information needs, not by which API seems most convenient.
2. Prefer macros for visible syntactic sugar and elaborators for semantic interpretation.
3. Treat elaboration as more than parsing: it resolves names, implicit arguments, coercions, unification, and other context-sensitive structure.
4. Printing has its own reverse pipeline and must preserve re-elaboratable meaning.

## Connects To
- **Ch 5–7**: the parser/macro/elaborator stages in detail.
- **Ch 12**: the reverse `Expr → Syntax → Format` path.

## Operational Procedure
For a broken extension, trace one representative input through the stages instead of editing all layers at once. Confirm which parser rule matched and what `Syntax` tree it produced. If a macro owns the syntax kind, inspect the expansion until no more macros apply. At the elaboration boundary, record the expected type and the expression that is produced. If the failure appears only when displaying the result, start from the elaborated `Expr` and inspect delaboration separately. This stage-by-stage method distinguishes grammar ambiguity from macro bugs, elaboration constraints, and printing choices.

When designing a new feature, write the intended stage contract before the implementation: “this parser recognizes X,” “this macro rewrites X to Y,” or “this elaborator maps X under expected type T to expression E.” A contract that mentions information unavailable at the selected stage is a signal to move later in the pipeline.
