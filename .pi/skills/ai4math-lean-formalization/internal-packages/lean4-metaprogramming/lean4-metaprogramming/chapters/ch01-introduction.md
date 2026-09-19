# Chapter 1: Introduction

## Core Idea
Lean 4 metaprogramming is ordinary Lean code that manipulates the structures used to parse, elaborate, prove, and print Lean programs. Choose the layer whose available information matches the task.

## Frameworks Introduced
- **Meta level vs object level**: object-level code is the program/proof being represented; meta-level code constructs or transforms its syntax, expressions, environment, or proof state.
  - When to use: whenever it is unclear whether a value is data in the user's program or a Lean representation of that program.
  - How: identify the representation (`Syntax`, `Expr`, goal/metavariable) and the monad that provides its context.
- **Dependency path through the book**: Expressions support `MetaM`; Syntax supports Macros; Syntax + `MetaM` support Elaboration; Elaboration supports embedded DSLs; Macros + Elaboration support tactics.
  - When to use: when deciding prerequisite knowledge for an implementation.

## Key Concepts
- **Metaprogram**: Lean code that operates on Lean programs/proofs or Lean's compilation/proof infrastructure.
- **Reflection**: representing program structure as data that can be inspected or transformed.
- **Custom notation**: a surface-language extension, often implemented with syntax and macros.
- **Custom command**: a top-level command with an elaborator that can inspect or modify the environment.
- **Embedded DSL**: a custom syntax whose elaborator builds ordinary Lean terms.
- **Tactic**: a metaprogram that transforms proof goals.

## Mental Models
Use the book as a capability graph. If a tactic implementation feels opaque, reduce it to `TacticM` goal management plus `MetaM` expression/proof construction. If an elaborator feels opaque, separate parsing (`Syntax`) from contextual interpretation (`Expr`).

Treat final proof terms as the trust boundary: metaprograms may be partial or buggy, yet the kernel validates the terms they produce before accepting proofs.

## Anti-patterns
- **Starting at the highest-level feature without its prerequisites**: tactic code becomes difficult to debug if `Expr`, metavariables, or local contexts are still mysterious.
- **Confusing host and represented values**: a Lean `Nat` in the metaprogram and an `Expr` representing an object-level `Nat` are different values with different operations.
- **Assuming metaprogramming bypasses proof checking**: tactics automate proof construction; kernel checking remains decisive.

## Code Examples
```lean
-- A distilled shape: a metaprogram constructs or transforms Lean data.
def inspectExpr (e : Expr) : MetaM Unit := do
  logInfo m!"{e}"
```
- **What it demonstrates**: metaprograms are Lean functions whose inputs are Lean's internal representations and whose monads provide compiler/prover context.

## Reference Tables
| Goal | Likely layer |
|---|---|
| New concrete notation | Syntax + macro |
| Type-directed term meaning | Term elaborator |
| New top-level semantic command | Command elaborator |
| Automatic proof step | Tactic + `MetaM` |
| Custom display of a term | Delaborator/unexpander |

## Key Takeaways
1. Locate the representation you need before choosing an API.
2. Learn `Expr` and `MetaM` before building semantic tactics/elaborators.
3. Learn Syntax before macros; combine Syntax and `MetaM` for elaboration.
4. Kernel validation lets metaprograms be engineering tools without becoming trusted proof checkers.

## Connects To
- **Ch 2**: turns the capability graph into a staged compiler pipeline.
- **Ch 3–4**: supply expression and meta-level foundations.
- **Ch 5–9**: implement concrete extensions at successively richer layers.

## Operational Procedure
When receiving an unfamiliar Lean metaprogramming request, first identify the user's visible artifact: new surface syntax, a term whose meaning must be inferred, a top-level command, a tactic, or custom output. Next identify the internal representation that must change. If the artifact is syntax-only, stay in the syntax/macro branch. If the result must be a typed term, plan for `Expr` and `MetaM`; if Lean must infer meaning from context, include elaboration. If goals are involved, add `TacticM` only for goal scheduling and interaction. This decomposition prevents a feature from accumulating unnecessary compiler layers.

A useful diagnostic is to ask what evidence will establish correctness. For syntax, parse-tree shape is evidence. For a macro, expansion shape plus hygiene is evidence. For an elaborator, the resulting typed expression and diagnostics are evidence. For a tactic, solved metavariables and successor goals are evidence. For pretty printing, re-elaboration to equivalent meaning is evidence.
