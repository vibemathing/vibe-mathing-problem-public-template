# Chapter 10: Lean 4 Cheat-sheet

## Core Idea
Use the cheat sheet as an API routing index after the abstraction layer is known. It consolidates the high-frequency operations from expressions, `MetaM`, syntax, elaboration, and tactics.

## Frameworks Introduced
- **Route first, API second**: identify whether the operation concerns syntax, expressions, metavariables/context, elaboration, or tactic state; then choose the narrow API family.
- **Context-sensitive default**: when an API operates on free variables, metavariables, expected types, or goals, assume context/state matters until proven otherwise.

## Key Concepts
- **Expression inspection**: match `Expr` constructors after required metavariable instantiation/reduction.
- **Expression construction**: prefer high-level meta builders when inference/context is involved.
- **Goal inspection**: obtain `MVarId`, enter context, inspect target.
- **Syntax matching**: use category-aware quotations.
- **Elaboration delegation**: use standard elaborators for ordinary subterms.
- **Tactic integration**: use goal-state helpers instead of ad hoc state edits.

## Mental Models
The cheat sheet is a navigation device, not a substitute for invariants. If an operation can assign metavariables, depend on local declarations, or unfold definitions, load the full `MetaM` chapter before relying on a one-line API memory.

When an API appears in several layers, prefer the layer already owning the task. For example, a tactic can call meta operations directly, yet tactic-state changes should still use `TacticM` helpers.

## Anti-patterns
- **API-name cargo culting**: calling a remembered function without checking its state/context assumptions.
- **Using a one-line helper as evidence that the operation is pure**.
- **Ignoring version drift**: exact names/signatures may change across Lean releases.

## Code Examples
```lean
-- Routing skeleton, not a complete implementation.
let goal ← getMainGoal
withMainContext do
  let target ← instantiateMVars (← goal.getType)
  let target ← whnf target
  ...
```
- **What it demonstrates**: common safe ordering for tactic/meta inspection.

## Reference Tables
| Goal | Common entry point |
|---|---|
| Read main goal | `getMainGoal` |
| Read local context | `getLCtx` / goal context helpers |
| Substitute solved holes | `instantiateMVars` |
| Expose expression head | `whnf` |
| Compare/unify | `isDefEq` |
| Build inferred application | `mkAppM` |
| Parse/match custom syntax | syntax quotation |
| Elaborate ordinary term | `elabTerm` |
| Replace tactic goal | `replaceMainGoal` |

## Key Takeaways
1. Use this file for recall after routing the problem.
2. Reopen ch04 for any stateful equality/metavariable/context issue.
3. Reopen the stage-specific chapter when exact invariants matter.
4. Verify exact APIs against the target Lean version before shipping version-sensitive code.

## Connects To
- **Ch 3–9**: expands every API family summarized here.

## Expanded API Routing
Use the API index as a sequence rather than a bag of names. For expression questions, decide first whether the input may contain assigned metavariables; if yes, instantiate. Decide whether the head is hidden by reducible computation; if yes, weak-head normalize. Only then inspect constructors. For construction, ask whether Lean should infer anything. Pure structural assembly may use raw constructors; inference or local dependencies point to `MetaM` builders.

For binder questions, avoid solving index arithmetic manually unless the transformation is explicitly low level. Open dependent binders through telescope helpers, operate on local free variables, and close the result. For goal questions, remember that `MVarId` APIs and tactic goal-list APIs solve different halves of the problem: the former change proof obligations, the latter schedule which obligations the user sees next.

For syntax questions, distinguish parser shape from semantic meaning. `syntax` declarations and quotations should be enough to prove the shape. Macro APIs should be enough to prove a context-free expansion. If code starts querying types, declarations, or local context, route to elaboration/meta. For display questions, route in reverse: inspect `Expr`, choose a surface form, then let parenthesization/formatting finish the job.

## Diagnostic Shortcuts
- Unexpected `mvar` after solving something → `instantiateMVars`.
- Free variable is “unknown” or invalid → wrong local context.
- Definitional-equality probe affects later work → stateful unification; isolate the probe.
- Application builder cannot infer an implicit → insufficient constraints; supply/control arguments.
- Custom syntax parses but cannot decide meaning → elaborator boundary.
- Tactic visually removes a goal yet proof fails → goal list changed without proof assignment.
- Printer extension produces confusing/copy-paste-invalid text → round-trip check failed.

The source cheat sheet is intentionally terse. In this skill, its role is routing: use it to recall a likely API, then load the substantive chapter whenever correctness depends on context, state, binder scope, or elaboration scheduling.
