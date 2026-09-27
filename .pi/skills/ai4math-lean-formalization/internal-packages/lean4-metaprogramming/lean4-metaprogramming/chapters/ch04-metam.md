# Chapter 4: MetaM

## Core Idea
`MetaM` is the main semantic workbench for Lean metaprogramming: it gives access to local contexts, metavariables, reduction, definitional equality, and high-level expression construction. Its stateful operations make context and rollback discipline essential.

## Frameworks Introduced
- **Metavariable-as-obligation**: a metavariable pairs a local context with a target type; assigning it fills the hole.
  - When to use: tactic goals, postponed subproblems, unification-driven inference.
  - Procedure: enter its context → inspect target/context → construct compatible term → assign → instantiate metavariables before subsequent structural decisions.
- **Normalize-to-the-decision**: use `whnf` for head inspection; use deeper/full reduction only when the task demands it.
- **Speculate with explicit transaction boundaries**: probing unification/elaboration may mutate meta state.
  - Procedure: save state or use a no-modification helper → attempt operation → commit only on the desired outcome → restore otherwise.

## Key Concepts
- **Local context (`LocalContext`)**: declarations available to the current expression/goal.
- **`MVarId`**: identity of a metavariable; supports context, target, assignment, and goal operations.
- **`instantiateMVars`**: substitutes current metavariable assignments into an expression.
- **Delayed assignment**: an assignment relation that may not appear as a simple direct assignment yet.
- **Metavariable depth**: controls which metavariables may be assigned from a given context/depth.
- **`whnf`**: weak-head normalization; exposes the outer computational form.
- **Transparency**: policy controlling which definitions may unfold during reduction/unification.
- **`isDefEq`**: definitional-equality/unification procedure that can assign metavariables.
- **`mkAppM` / `mkAppOptM`**: application builders that infer omitted arguments.
- **Telescope**: opening a chain of foralls/lambdas into local free variables.

## Mental Models
Treat an expression containing metavariables as a snapshot with references, not a live mutable tree. Assignment changes the metavariable context; call `instantiateMVars` to obtain a view with current solutions substituted.

Treat a metavariable's local context as its lexical world. A free variable that is valid for one goal may be meaningless for another. Use `mvarId.withContext` before operations that inspect or construct terms for that goal.

Treat `isDefEq` as “try to make these terms definitionally equal under current unification state.” Success can include solving metavariables. It is unsuitable as a side-effect-free predicate unless state is isolated.

## Anti-patterns
- **Pattern matching before instantiation**: assigned metavariables can hide the actual head structure.
- **Using the ambient context for a foreign goal**: free-variable operations can become invalid or misleading.
- **Checking only `isAssigned`**: delayed assignments can make the state more subtle.
- **Full normalization by default**: it costs more and may unfold details irrelevant to the decision.
- **Bare `try/catch` as rollback**: catching an exception does not restore metavariable assignments.
- **Loose bound variables in high-level code**: use temporary free variables plus closure helpers.
- **Blind `mkAppM`**: implicit arguments may be underconstrained; use explicit/optional argument control.
- **Assuming `MVarId.assign` validates types**: low-level assignment expects the caller to maintain invariants.

## Code Examples
```lean
-- Distilled speculative equality check.
def probeDefEq (a b : Expr) : MetaM Bool := do
  withoutModifyingState do
    isDefEq a b
```
```lean
-- Distilled binder construction pattern.
withLocalDecl `x BinderInfo.default ty fun x => do
  let body ← buildBody x
  mkLambdaFVars #[x] body
```
- **What it demonstrates**: isolate stateful checks and use local free variables for binder construction.

## Reference Tables
| Need | Preferred API/idea |
|---|---|
| See solved metavariables | `instantiateMVars` |
| Operate on a goal | `mvarId.withContext` |
| Inspect outer normalized shape | `whnf` |
| Compare/unify terms | `isDefEq` with mutation awareness |
| Build application with inferred implicits | `mkAppM` |
| Control inferred positions | `mkAppOptM` |
| Open dependent function type | `forallTelescope*` |
| Close over local variables | `mkLambdaFVars`, `mkForallFVars` |
| Probe without committing | state-preserving helper/save-restore |

Transparency grows from very restrictive to increasingly permissive (e.g. `none`, `reducible`, instance-oriented/intermediate modes, `default`, `all`). Choose the weakest setting that supports the intended equality/reduction.

## Exercise-backed Validation
The solutions demonstrate two important edge cases. First, `isDefEq` may behave surprisingly on malformed or ill-typed raw expressions because many meta APIs assume their inputs are already well typed. Second, save/restore correctly reverts metavariable unifications in the intended meta state. These examples justify validating expression invariants before interpreting unification outcomes.

## Key Takeaways
1. Enter the correct metavariable context before inspecting or solving a goal.
2. Instantiate metavariables before structure-sensitive logic.
3. Use `whnf` and restrained transparency for most structural decisions.
4. Treat definitional equality as stateful unification.
5. Make speculative state changes transactional.
6. Build binders through local free variables and close them with helper APIs.
7. Escalate from `mkAppM` to `mkAppOptM` when inference lacks constraints.

## Connects To
- **Ch 3**: defines the expression structures manipulated here.
- **Ch 7**: elaborators run semantic operations in richer monads built on `MetaM`.
- **Ch 9**: tactics expose goals whose low-level representation is `MVarId`.
