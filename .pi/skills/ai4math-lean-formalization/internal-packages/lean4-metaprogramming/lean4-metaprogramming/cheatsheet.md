# Lean 4 Metaprogramming Cheat Sheet

## Route the Task
| If the task needs... | Use |
|---|---|
| grammar, precedence, syntax category | `syntax`, ch05 |
| pure `Syntax → Syntax` sugar | macro, ch06 |
| expected type/context/type classes | term elaborator, ch07 |
| top-level environment effect | command elaborator, ch07 |
| term construction/unification/reduction | `MetaM`, ch04 |
| proof-goal transformation | `TacticM` + `MetaM`, ch09 |
| custom surface language | syntax + elaboration, ch08 |
| custom printed notation | delab/unexpander, ch12 |
| configurable behavior | options, ch11 |

## Safe Expression Inspection
`goal/context → instantiateMVars → whnf if needed → match`

- `Expr`: low-level term tree; raw construction assumes invariants.
- `mvarId.withContext` / `withMainContext`: enter the right local context.
- `instantiateMVars`: view current solutions.
- `whnf`: expose head form cheaply.
- `isDefEq`: equality + unification; **may assign metavariables**.
- `reduce`: full normalization; use only when needed.

## Construction
| Need | Prefer |
|---|---|
| inferred application | `mkAppM` |
| selectively inferred args | `mkAppOptM` |
| lambda/forall | local `fvar`s + `mkLambdaFVars` / `mkForallFVars` |
| open binders | `forallTelescope*`, lambda telescope helpers |
| raw structural node | `Expr.*` constructors, with manual invariant checks |

## State / Failure
- `try/catch` does **not** roll back meta state.
- Use `withoutModifyingState`, `saveState`/`restoreState`, or an appropriate observing/commit helper for speculation.
- Delayed metavariable assignments can defeat a naive `isAssigned` check.
- Raw `MVarId.assign` assumes the assigned expression is valid for the target/context.

## Syntax / Macro
- Custom grammar: `declare_syntax_cat`, `syntax`.
- Prefer category-aware quotations and antiquotations to manual `Syntax.node` surgery.
- Macro = transparent, context-free desugaring.
- Hygiene is default; use explicit identifiers only for deliberately user-visible names.
- Unsupported macro/elab shape: yield to other handlers when overloading is intended.

## Elaboration
- Term elaborator shape: `Syntax → Option Expr → TermElabM Expr`.
- Meaning needs unknown expected type → postpone.
- Known incompatible expected type → targeted error.
- Ordinary nested Lean term → delegate to `elabTerm`.

## Tactics
- Read: `getMainGoal`, `getGoals`.
- Context: `withMainContext`.
- Update: `replaceMainGoal`, `setGoals`, `closeMainGoal`.
- Ordinary goal transformer: `liftMetaTactic`.
- Removed goal must be solved/assigned or deliberately replaced.

## Printing
`Expr → delaborator/unexpander → Syntax → parenthesizer → formatter`

Custom printed syntax must re-elaborate to equivalent meaning. Unexpanders run before parenthesization, so nested patterns cannot rely on already-inserted parentheses.
