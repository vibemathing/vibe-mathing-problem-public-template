# Chapter 8: Partial Order Reduction

## Core Idea

Concurrent systems contain many executions that differ only in the order of independent actions. Partial-order reduction (POR) explores selected representatives of those interleavings while preserving a target temporal-logic fragment. The central discipline is the **ample-set conditions**: reduction is allowed only when dependence, visibility, and cycle obligations are respected.

## Frameworks Introduced

### Independence of actions
Two actions are independent when, whenever both are enabled in a state:
1. executing one does not disable the other; and
2. executing them in either order leads to the same resulting state.

**When to use**: the global state space is dominated by interleavings of local actions that do not affect one another.

Independence creates a commuting diamond: `α;β` and `β;α` represent the same essential behavior. POR keeps enough orders to preserve the property instead of enumerating all permutations.

### Ample set
At each state `s`, choose `ample(s)`, a subset of currently enabled actions. Only transitions labeled by actions in `ample(s)` are expanded in the reduced transition system.

The reduction is sound only when the ample sets satisfy provisos matched to the logic.

### Ample-set conditions for linear-time next-free properties
The book uses four core constraints for stutter-trace preservation of LTL without `X`.

#### A1 — Nonemptiness
If a state has enabled actions, `ample(s)` must be nonempty.

**Purpose**: reduction may not invent a deadlock by ignoring every enabled transition.

#### A2 — Dependency condition
Along any full-system path starting at `s`, an action dependent on an action in `ample(s)` may not occur before some action from `ample(s)` occurs.

**Purpose**: prevents the reduction from postponing the chosen action past a competing dependent action whose order could change behavior.

A2 is the hardest condition to check exactly. Practical algorithms use conservative sufficient conditions based on static process/action dependence.

#### A3 — Invisibility / stutter condition
If `ample(s)` is a proper subset of all enabled actions, every action selected in `ample(s)` must be invisible with respect to the atomic propositions relevant to the property.

**Purpose**: reduced early steps may be reordered/hidden only when they do not change the observable state label; the resulting traces then differ at most by stuttering.

#### A4 — Cycle condition / cycle proviso
A cycle in the reduced graph may not postpone an enabled action forever. Operationally, for every action enabled at a state on a reduced cycle, that action must occur in an ample set at some state on the cycle (under the chapter's formulation).

**Purpose**: local reduction choices that look safe on acyclic prefixes can otherwise create an infinite reduced cycle that permanently ignores an enabled action.

The book's core correctness theorem assumes an **action-deterministic, finite transition system without terminal states**. Under those conditions, A1–A4 make the reduced system stutter-trace equivalent to the full system, which preserves LTL without `X`. If a model has terminal states or a different action semantics, handle that boundary explicitly before applying the theorem.

### Dynamic POR during DFS
**When to use**: explicit-state on-the-fly model checking.

Conceptual procedure:
1. at state `s`, compute a candidate ample set using enabled processes/actions;
2. check conservative A2/A3 conditions;
3. enforce the cycle proviso with DFS stack information;
4. if a reduction could create a back edge to an active DFS state and violate A4, fully expand the state instead;
5. explore only ample transitions when all conditions hold.

Dynamic POR can exploit the currently reached state and enabledness, often reducing more than purely static preprocessing.

### Static POR and sticky actions
A static approach identifies actions that must never be postponed by reduction. **Sticky actions** include actions needed to preserve visibility and to break cycles that could violate the cycle proviso.

**When to use**: dependence and control structure can be analyzed before state-space exploration and the resulting static ample choices remain useful across runs.

Static analysis tends to be more conservative but can make reduction decisions cheaper during verification.

### Branching-time ample sets
For next-free CTL*/CTL, linear-time stutter-trace preservation is insufficient: branching structure matters. Add:

#### A5 — Singleton condition
Whenever reduction occurs (`ample(s)` is a strict subset of enabled actions), the ample set contains exactly one action.

With A1–A5, the reduced and full systems are related strongly enough (via the chapter's divergence-sensitive stutter-bisimulation result) to preserve next-free branching-time properties.

## Key Concepts

- **Dependent actions**: actions whose enabledness/effect can interfere; their order cannot be freely exchanged.
- **Independent actions**: commuting, non-disabling actions whose order is observationally redundant.
- **Enabled action**: action with at least one outgoing transition from the current state.
- **Invisible action**: action whose execution does not change the state labeling relevant to the property.
- **Ample set**: chosen enabled subset explored from a state.
- **Reduction state**: a state where `ample(s)` is a strict subset of enabled actions.
- **Cycle proviso**: global condition preventing permanent postponement on reduced cycles.
- **Dynamic POR**: ample sets computed during state-space exploration.
- **Static POR**: reduction choices derived from precomputed control/dependence information.
- **Sticky action**: action forced into relevant ample choices because visibility/cycle constraints make postponement unsafe.
- **Stutter preservation**: reduced/full traces may differ by finite repetitions of identical observations.

## Mental Models

- **POR removes schedules, not behaviors that matter to the property**. Every omitted ordering needs an independence argument.
- **A1 protects deadlock, A2 protects causality, A3 protects observation, A4 protects fairness-like cycle progress, A5 protects branching.**
- **Think locally, verify globally**: ample selection is local, but cycles make soundness global; DFS stack checks bridge that gap.
- **Property AP controls visibility**: an action can be invisible for one property and visible for another, so POR may be property-specific.
- **When uncertain about dependence, expand more**. Conservative reduction costs performance; unsound reduction costs correctness.

## Anti-patterns

- **Calling actions independent because they are in different processes**: shared variables/channels can couple them.
- **Ignoring A4 because every local ample choice satisfies A1–A3**: a reduced cycle can still starve an omitted action forever.
- **Reducing visible actions under next-free preservation without justification**: the reduced trace can change observably.
- **Applying A1–A4 to CTL and assuming branching is preserved**: branching-time reduction needs A5 in the chapter's ample-set method.
- **Using POR on formulas containing `X` while relying on stutter preservation**: exact next-state structure can change.
- **Making independence asymmetric**: the commuting/non-disabling relation used here is a symmetric behavioral condition.
- **Proving A2 with reachability-heavy exact analysis when a conservative static condition suffices**: can erase the performance gain.

## Reference Tables

### Ample-set decision table

| Check | Question | If it fails |
|---|---|---|
| A1 | enabled actions exist but ample is empty? | include at least one enabled action |
| A2 | could a dependent action occur before any ample action? | enlarge ample / fully expand |
| A3 | does a reduced ample action change relevant AP labels? | fully expand or change property visibility |
| A4 | could a reduced cycle ignore an enabled action forever? | fully expand cycle-closing/back-edge state |
| A5 | branching-time case: is reduced ample size > 1? | choose singleton or fully expand |

### Logic boundary

| Property fragment | Required ample conditions | Preservation intuition |
|---|---|---|
| LTL without `X` | A1–A4 | stutter trace equivalence |
| CTL*/CTL without `X` | A1–A5 | divergence-sensitive stutter bisimulation |
| formulas using `X` | these stutter rules are insufficient | exact next step is observable |

## Worked Example: two independent assignments

Processes perform:

- `α: x := x + 1`
- `β: y := y - 2`

with no shared variables between the assignments. If both are enabled, `α;β` and `β;α` end in the same valuation and neither disables the other. Exploring both orders produces redundant behavior.

A POR implementation can select only `α` at the initial state provided:
1. no dependent action can intervene before `α` (A2);
2. `α` is invisible for the checked AP when reducing (A3);
3. the choice cannot participate in a reduced cycle that ignores `β` forever (A4).

If the property observes `x` at every next state, `α` is visible and this reduction cannot be justified by the next-free stutter argument.

## Worked Example: why the cycle proviso matters

Suppose a loop repeatedly executes an invisible local action `α`, while independent action `β` remains enabled. A local ample selector always chooses `{α}`. A1 holds; `α` may be independent and invisible, so A2/A3 can also look satisfied.

The reduced graph now contains an `α`-cycle that never explores `β`. The full system has behaviors where `β` eventually occurs, and a liveness property about `β` can change. A4 forces a state on that reduced cycle to include/expand `β`, breaking the permanent postponement.

This is why DFS implementations commonly fully expand states whose reduced successors touch the active search stack.

## Failure Recovery

### Reduction changes a result
- Confirm the property is next-free if relying on stutter preservation.
- Recompute the set of relevant AP; a formerly “invisible” action may have become visible after the property changed.
- Audit dependence on shared variables, guards, and channels.
- Disable reduction at cycle-closing states and retest A4.
- For branching-time formulas, verify A5.

### Ample set is always the full enabled set
Reduction opportunity is absent under the current dependence/visibility analysis. Improve static independence information only if it can be proven sound; otherwise accept the full expansion or use another reduction technique.

### A2 is too expensive to test directly
Use the chapter's conservative static/process-level sufficient conditions: treating extra actions as dependent reduces less but preserves soundness.

## Key Takeaways

1. POR exploits commutativity of independent actions to avoid redundant interleavings.
2. The ample set is a semantic choice constrained by A1–A4 for next-free LTL.
3. A4 is essential because infinite cycles can invalidate otherwise local reasoning.
4. Dynamic POR uses current enabledness and DFS stack information; static POR uses precomputed dependence/sticky actions.
5. Branching-time preservation adds A5, typically forcing a singleton reduced choice.
6. Visibility is property-dependent, so reduction may need recomputation when AP/formulas change.
7. Unsure means expand: POR must fail conservatively.

## Connects To

- **Ch 2**: interleaving and action independence are the raw source of POR opportunities.
- **Ch 5**: next-free LTL is the principal linear-time target.
- **Ch 6**: branching-time properties require stronger preservation.
- **Ch 7**: stutter trace equivalence and divergence-sensitive stutter bisimulation supply the preservation theory behind the ample-set conditions.
