# Chapter 11: The Conversion Tactic Mode

## Core Idea
`conv` gives a focused rewrite environment for navigating to a precise subexpression. Use it after ordinary `rw`/`simp` becomes ambiguous, especially when the desired occurrence is nested, repeated, or under a binder.

## Frameworks Introduced
- **Navigation-first rewriting**
  - When to use: the rewrite lemma is correct but ordinary rewriting targets the wrong occurrence.
  - How: enter `conv`, navigate with `lhs`, `rhs`, `congr`, `arg`, or `intro`, then perform the local rewrite.
- **Pattern-focused conversion**
  - When to use: a syntactic pattern identifies the subexpression better than positional navigation.
  - How: use `conv in pattern => ...`, including wildcards when suitable.
- **Local normalization inside conversion**
  - When to use: the selected subterm needs simplification or weak-head reduction before the next proof step.
  - How: run `simp`, `whnf`, or an embedded ordinary tactic at the focused location.

## Key Concepts
- **Conversion mode**: tactic context focused on a selected subexpression rather than the whole target.
- **`lhs` / `rhs`**: focus the left/right side of a relation such as equality.
- **`congr`**: descend through congruent structure, creating navigation targets/obligations as appropriate.
- **`arg i`**: focus a particular function argument.
- **`intro`**: descend beneath a binder by introducing the bound variable for the conversion context.
- **`conv in pattern`**: find subterms by pattern.
- **`whnf`**: reduce focused expression to weak-head normal form.
- **`done`**: assert that no conversion goals remain.
- **`trace_state`**: inspect conversion state during development.

## Mental Models
- Treat `conv` as a **cursor inside the syntax tree** of the goal/hypothesis.
- Use the normal equality toolkit first; `conv` adds value when the problem is **where**, not **which equality theorem**.
- Rewriting beneath a binder requires maintaining the local bound variable; `intro` exposes that context safely.

## Anti-patterns
- **Using `conv` for every rewrite**: it adds navigation ceremony when `rw` is already unambiguous.
- **Broad pattern wildcards that focus multiple unintended locations**.
- **Forgetting to inspect state while developing a long navigation path**: one wrong `congr`/`arg` can put the cursor elsewhere.

## Code Examples
```lean
example (a b c : Nat) (h : a = b) : a + c = b + c := by
  conv =>
    lhs
    arg 1
    rw [h]
```
- **What it demonstrates**: navigate to a specific argument on one side of an equality before rewriting.

```lean
example (f g : Nat → Nat) (h : ∀ x, f x = g x) :
    (fun x => f x + 1) = (fun x => g x + 1) := by
  funext x
  conv =>
    lhs
    arg 1
    rw [h x]
```
- **What it demonstrates**: exact subterm targeting after introducing a function argument; confirm navigation details in the active Lean version if syntax evolves.

## Reference Tables
| Symptom | First try | `conv` route |
|---|---|---|
| only one clear occurrence | `rw [h]` | unnecessary |
| simplification throughout target | `simp` | focus first only if global simp is too broad |
| left side only | `rw [...]` may support occurrence targeting | `conv => lhs; ...` |
| nth/nested function argument | awkward occurrence specification | `arg i`, `congr` |
| expression under binder | `funext`/ordinary tactic may help | `intro` inside conversion |
| recognizable syntactic subterm | direct rewrite may hit all matches | `conv in pattern => ...` |

## Worked Example
A target contains the same expression three times, but only the occurrence inside the right side of a nested application should change.
1. Confirm the equality lemma itself is correct with `#check`.
2. Attempt `rw` only if its occurrence behavior is predictable.
3. Enter `conv`; use `rhs` to select the right side.
4. Descend through the application with `congr`/`arg` until `trace_state` shows the intended term.
5. Apply `rw` or `simp` at that focused location.
6. Exit conversion mode and finish the global proof normally.

The proof now documents which occurrence is semantically relevant.

## Failure Recovery
- focus lands on wrong term → back up and use explicit `lhs`/`rhs`/`arg` navigation.
- pattern matches too broadly → add surrounding syntax or fewer wildcards.
- binder navigation is awkward → use `funext`/ordinary introduction first, then `conv` on the simpler goal.
- rewrite still fails at focus → inspect definitional shape with `whnf` or check lemma direction/type.

## Key Takeaways
1. `conv` solves precision problems in rewriting and simplification.
2. Navigation and rewriting are separate: first focus the right term, then transform it.
3. Binder-aware navigation makes subterm rewriting possible inside dependent/function expressions.
4. Pattern-based focus can be clearer than positional navigation when the subterm has a distinctive shape.
5. Keep `conv` as an escalation from simpler equality tools.

## Connects To
- **Ch 4**: supplies equality, congruence, and calculational reasoning.
- **Ch 5**: ordinary `rw`/`simp` are the first-line tactics before conversion mode.
- **Ch 6**: `trace_state` and term inspection help debug navigation.
