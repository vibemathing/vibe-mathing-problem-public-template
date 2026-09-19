# Chapter 7: Elaboration

## Core Idea
Elaboration is where syntax acquires semantic meaning in a context. Term elaborators may depend on an expected type and must cooperate with metavariables/postponement; command elaborators perform top-level effects and environment changes.

## Frameworks Introduced
- **Command elaborator fallback**: macros expand first; registered command elaborators then try the resulting syntax, with unsupported handlers yielding to others.
- **Expected-type-directed term elaboration**: a term elaborator receives `Syntax` and `Option Expr` for its expected type.
  - When to use: literal/notation meaning varies with type or local context.
  - Procedure: inspect/instantiate expected type → postpone if semantically underdetermined → validate expected shape → elaborate children → build result expression.
- **Postponement**: delay elaboration when required information is represented by unsolved metavariables and may become available later.

## Key Concepts
- **`CommandElabM`**: elaboration monad for top-level commands; supports environment and messaging effects.
- **`TermElabM`**: term elaboration monad layered over semantic/meta capabilities.
- **Expected type**: type Lean currently wants the term to inhabit; may be absent or contain metavariables.
- **Synthetic metavariable**: metavariable whose solution is delegated to a specific elaboration mechanism.
- **Postponed elaboration**: synthetic work retried when more information is available.
- **`elabTerm`**: delegates ordinary subterm elaboration to Lean.
- **`tryPostponeIfNoneOrMVar`**: useful shape for elaborators whose meaning requires a known expected type.

## Mental Models
Think of elaboration as constraint solving with callbacks. Your elaborator should contribute only the logic unique to the custom syntax and reuse Lean's normal elaborator for nested ordinary terms.

Treat an unknown expected type as a scheduling problem, not immediately as an error. If the custom construct cannot choose a meaning yet, postponement lets other constraints solve first. Error only when enough information is known and incompatible.

Treat command elaboration as an environment transaction at the language-extension boundary. Commands can log, inspect declarations, create declarations, or perform IO; keep their effects explicit and diagnostics attached to source syntax.

## Anti-patterns
- **Guessing when expected type is a metavariable**: can lock the elaboration into a wrong interpretation before constraints are solved.
- **Reimplementing normal subterm elaboration**: delegate to `elabTerm` so name resolution, coercions, implicits, and standard errors remain consistent.
- **Hard-failing an overloaded elaborator on unsupported syntax**: prevents other registered elaborators from handling the form.
- **Ignoring macro expansion order**: command/term syntax may have been rewritten before an elaborator receives it.

## Code Examples
```lean
-- Distilled type-directed elaborator shape.
elab_rules : term
  | stx => do
      tryPostponeIfNoneOrMVar (← getExpectedType?)
      let expected ← instantiateMVars (← getExpectedType)
      -- validate expected, elaborate children, construct result
      ...
```
- **What it demonstrates**: semantic decisions wait until expected type is sufficiently known.

## Reference Tables
| Situation | Response |
|---|---|
| Expected type absent/unsolved and required | Postpone |
| Expected type known but incompatible | Produce targeted error |
| Child is ordinary Lean syntax | `elabTerm` |
| Top-level command has semantic effect | Command elaborator |
| Feature is pure syntax alias | Prefer macro |

## Exercise-backed Validation
The elaboration solutions implement equivalent behavior using several registration styles: explicit syntax plus attributes, `elab_rules`, and `elab`. The capability is the same; choose the declaration style that makes syntax ownership and handler dispatch clearest in the target codebase.

## Key Takeaways
1. Use elaboration when meaning depends on semantic context.
2. Read the expected type as an input constraint, not a guaranteed concrete expression.
3. Postpone when the required constraint is unresolved; report errors when incompatibility is established.
4. Delegate nested ordinary Lean terms back to the standard elaborator.
5. Use handler fallback deliberately when extending existing syntax kinds.

## Connects To
- **Ch 4**: supplies metavariables, normalization, and expression construction used inside elaborators.
- **Ch 8**: applies term elaboration to an embedded language.
- **Ch 9**: tactic elaboration specializes contextual interpretation for proof-state programs.

## Operational Procedure
Separate three expected-type states: unavailable, available but unresolved, and concrete enough to inspect. Only the third supports type-directed branching. Treat the first two as candidates for postponement when semantics truly depends on type. After resumption, instantiate current metavariable assignments before matching the expected type. Keep custom logic narrow: recognize the special construct, validate its semantic preconditions, and hand ordinary children back to Lean.
