# Chapter 9: Tactics

## Core Idea
A tactic is a proof-state program. `TacticM` provides the current goal list on top of term elaboration/meta capabilities; correct tactics maintain the invariant that removed goals are solved or deliberately replaced by valid successor goals.

## Frameworks Introduced
- **Goal transformation pattern**:
  1. Read the main goal.
  2. Enter its local context.
  3. Inspect target/local declarations.
  4. Use `MetaM` to construct/assign a proof or create successor goals.
  5. Replace/close the main goal in the tactic state consistently.
- **Lift a meta tactic**: if an operation naturally maps one `MVarId` to a list of resulting goals, expose it through `liftMetaTactic` rather than hand-editing state.
- **Context extension**: operations such as introduce/assert/define change a goal's local context and return a new goal representing the remainder.

## Key Concepts
- **`TacticM`**: tactic monad combining tactic context/state with `TermElabM`/`MetaM` capabilities.
- **Goal list**: ordered list of current metavariable goals; the first is the main goal.
- **`getMainGoal` / `getGoals`**: read tactic state.
- **`setGoals` / `replaceMainGoal`**: update goal list.
- **`closeMainGoal`**: remove the main goal after it has been solved appropriately.
- **`withMainContext`**: execute under main goal's local context.
- **`liftMetaTactic`**: integrate a low-level goal transformation into tactic state management.
- **`MVarId.define` / `assert`**: extend a goal with local declarations under different proof/value conditions.
- **`intro1P` and related intro APIs**: introduce binders while controlling naming behavior.
- **`evalTactic`**: execute tactic syntax programmatically.

## Mental Models
Think of a goal as a metavariable plus a local environment. Solving the goal means assigning that metavariable a proof term of its target. The visible goal list is scheduling state, not the proof itself.

Think of tactic combinators as programs that can call other tactic syntax, while semantic tactic implementations are usually clearer when they delegate the proof-term work to `MetaM`.

For “assumption”-style behavior, search local declarations, compare each declaration type to the target using definitional equality under the goal context, assign the goal to the matching free variable, then close the main goal.

## Anti-patterns
- **Deleting a goal from the list without assigning it**: visually hides work while leaving the proof hole unsolved.
- **Inspecting a main goal outside its context**: free variables/targets may not be meaningful in the ambient context.
- **Implementing state plumbing manually when `liftMetaTactic` matches the abstraction**.
- **Treating `isExprDefEq`/`isDefEq` as pure**: equality may solve metavariables and affect later tactic behavior.
- **Using low-level Meta tactic APIs when an elaboration-aware tactic API is needed for syntax/user interaction**.

## Code Examples
```lean
-- Distilled semantic tactic shape.
elab "my_assumption" : tactic => withMainContext do
  let goal ← getMainGoal
  let target ← goal.getType
  for decl in ← getLCtx do
    if ← isDefEq decl.type target then
      goal.assign decl.toExpr
      closeMainGoal
      return
  throwTacticEx `my_assumption goal m!"no matching local hypothesis"
```
- **What it demonstrates**: context-aware local search, definitional equality, proof assignment, and coherent goal closure.

## Reference Tables
| Need | API family |
|---|---|
| Current main/all goals | `getMainGoal`, `getGoals` |
| Main goal context | `withMainContext` |
| Replace result goals | `replaceMainGoal` |
| Whole goal list control | `setGoals` |
| Meta goal transformer integration | `liftMetaTactic` |
| Run tactic syntax | `evalTactic` |
| Introduce binder | `intro*` family |
| Extend context with named local | `MVarId.assert` / `define` |

## Exercise-backed Validation
The tactic solutions compare hand-written goal-list updates with `liftMetaTactic` and exercise `setGoals`/`replaceMainGoal`. They also show naming differences among `intro`, `intro1`, `intro1P`, `introN`, and `introNP`. The engineering lesson is to choose the highest-level goal-state helper that exactly matches the intended transformation, then verify naming semantics separately.

## Key Takeaways
1. A tactic's real output is a set of metavariable assignments and successor goals.
2. Always work under the goal's local context.
3. Use `MetaM` for semantic proof construction and `TacticM` for scheduling/user-facing tactic state.
4. Keep goal-list changes synchronized with metavariable solutions.
5. Prefer `liftMetaTactic` for ordinary one-goal-to-many-goals transformations.

## Connects To
- **Ch 4**: goals, contexts, unification, and assignment are MetaM concepts.
- **Ch 6**: tactic macros provide lightweight syntax expansion.
- **Ch 7**: tactic elaboration inherits the elaboration model.

## Operational Procedure
For each tactic branch, account for the main goal explicitly. There are only a few valid outcomes: assign it and remove it; transform it into one or more successor metavariables; leave it unchanged while reporting a controlled failure; or delegate to another tactic. After any context-extending operation, continue with the returned goal because it owns the updated local context. When trying several local hypotheses or proof strategies, isolate stateful unification if rejected candidates must not constrain later candidates.
