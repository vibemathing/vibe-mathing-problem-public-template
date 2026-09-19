# Chapter 3: Linear-Time Properties

## Core Idea

Linear-time verification views a system through its execution traces. The chapter separates properties that can be refuted by finite evidence (**safety**) from properties that constrain only infinite continuation (**liveness**), then adds fairness to rule out unrealistic schedules when analyzing progress.

## Frameworks Introduced

### Reachability and deadlock analysis
**When to use**: “Can this state happen?”, “Can the system halt?”, or any invariant whose violation is state-local.

**How**:
1. start from every initial state;
2. explore `Post` successors with DFS or BFS;
3. mark visited states to avoid repeated work;
4. test each visited state against the target/predicate;
5. keep predecessor pointers when a diagnostic path is required.

A deadlock is a reachable terminal state when termination is not part of intended behavior. Do not classify every terminal state as a defect: terminating sequential programs naturally end in terminal states.

### Invariant checking
An invariant is a state formula `Φ` that must hold in every reachable state.

Operational rule:

`TS |= invariant Φ` exactly when every state in `Reach(TS)` satisfies `Φ`.

Use DFS for linear-time exploration with low bookkeeping. Use BFS when the **shortest counterexample** matters; the selected-solution supplement gives a breadth-first variant that stores predecessor pairs and reconstructs the shortest path to the first violating state.

### Paths, traces, and LT properties
A **path** is an infinite state sequence following transitions (with standard treatment of terminal states in the text). A **trace** projects a path to the sequence of state labels. An LT property over `AP` is a set of infinite words over `2^AP`.

**Decision implication**: two transition systems with the same traces satisfy exactly the same LT properties. If a verification claim depends only on traces, internal action/state distinctions not visible in `AP` may be abstractable.

### Safety via bad prefixes
A property is safety when every violating infinite trace has a finite prefix after which no continuation can recover into the property.

**How to reason**:
1. describe the set of bad finite prefixes;
2. ask whether the current execution prefix has already entered that set;
3. if bad prefixes form a regular language, route to Ch 4 and monitor them with a finite automaton.

Finite trace inclusion is the key semantic order for safety preservation: if every finite trace of one system is a finite trace of another, safety properties transfer in the appropriate direction.

### Liveness and safety–liveness decomposition
A liveness property does not rule out any finite behavior: every finite prefix still has some infinite continuation satisfying the property. Typical examples are eventual response and recurrence.

Every LT property can be decomposed into a safety component and a liveness component. Use this conceptually when a requirement mixes “bad never happens” with “good eventually happens”: verify the finite-refutable part and the progress part with the methods suited to each.

### Fairness constraints
Fairness removes paths that model unacceptable scheduling behavior.

| Fairness type | Informal obligation | Typical use |
|---|---|---|
| unconditional | selected action/process occurs infinitely often | explicit periodic/progress guarantee |
| strong | enabled infinitely often ⇒ taken infinitely often | repeated contention where enabledness comes and goes |
| weak | continuously enabled from some point ⇒ taken infinitely often | persistent enabledness / independent interleaving |

The text's practical rule of thumb is to associate strong fairness with recurring contention and weak fairness with independent activities that remain enabled.

**Realizability check**: do not accept a fairness assumption merely because it proves the property. From the relevant reachable states, fair behavior must actually be possible under the modeled scheduling contract.

## Key Concepts

- **State graph**: directed graph induced by the transition relation when action names are ignored.
- **Trace**: sequence of observable label sets generated along a path.
- **Trace equivalence**: equality of trace sets; characterizes equivalence for all LT properties.
- **Finite trace**: observable label sequence of a finite initial execution fragment.
- **Invariant**: special safety property expressible as a propositional condition on each reachable state.
- **Bad prefix**: finite trace after which every infinite extension violates a safety property.
- **Minimal bad prefix**: bad prefix with no proper bad prefix; useful for compact diagnostics/monitor design.
- **Closure of an LT property**: the safety property containing exactly the infinite words whose every finite prefix is extendible to a word in the original property.
- **Starvation**: a process waits indefinitely despite global progress.
- **Fair trace/path**: a behavior satisfying the chosen fairness constraints.
- **Realizable fairness**: fairness constraints that admit fair continuations as required by the model.

## Mental Models

- **Ask “could a finite witness settle failure?”** to route safety versus liveness.
- **Use traces as the observable contract** when internal states/actions are implementation detail.
- **Treat liveness counterexamples as recurrence structures**: a finite prefix followed by a cycle often demonstrates endless deferral.
- **Use fairness to model the scheduler, not to rescue the design**.
- **Think of safety as prefix-closed evidence of failure** and liveness as permission for every finite prefix to recover.

## Anti-patterns

- **Calling “eventually responds” a safety property**: no finite delay proves that response will never arrive.
- **Checking a liveness claim only with bounded simulation**: passing many steps provides no proof about infinite continuation.
- **Adding fairness before inspecting the raw counterexample**: the trace may reveal a genuine design starvation mechanism.
- **Using nonrealizable fairness**: an impossible scheduling assumption can eliminate all problematic paths.
- **Treating safety and liveness as mutually exclusive categories for whole requirements**: mixed properties can contain both components.
- **Assuming trace equivalence preserves action-sensitive claims**: traces observe state labels, not necessarily action names.

## Reference Tables

### Property triage

| Requirement shape | Class | Diagnostic shape | First method |
|---|---|---|---|
| “state `bad` is unreachable” | invariant/safety | finite path to `bad` | DFS/BFS |
| “mutual exclusion always holds” | invariant/safety | finite state with both critical | DFS/BFS |
| “after request, grant eventually occurs” | liveness | infinite deferral/lasso | LTL/ω-regular + cycle search |
| “resource used infinitely often” | liveness | suffix avoiding use | recurrence/cycle reasoning |
| “under fair scheduling, request is served” | fair liveness | fair lasso violating response | fairness-aware checking |

### Fairness test

1. Identify the action/process alleged to starve.
2. Determine its enabledness pattern on the counterexample.
3. Continuously enabled after some point → weak fairness may rule it out.
4. Enabled infinitely often with gaps → strong fairness may be needed.
5. Verify that the implementation/scheduler can enforce the chosen condition.
6. Confirm at least one fair continuation where required.

## Worked Example: mutual exclusion vs starvation

A semaphore-based two-process protocol can satisfy mutual exclusion while still permitting a path where process 2 waits forever and process 1 repeatedly acquires the critical section. The finite-state graph contains no state with both processes critical, so the safety property holds. Yet a cyclic path can keep process 2 in `wait2` indefinitely, violating absence of starvation.

Operational lesson:

1. prove the invariant `not(crit1 and crit2)` separately;
2. state starvation freedom as a progress property such as `wait_i -> eventually crit_i`;
3. inspect whether a failing cycle is enabled by an unrealistic scheduler;
4. add fairness only if the actual scheduling discipline warrants it.

This prevents a common error: reporting a lock as “correct” after proving only mutual exclusion.

## Worked Example: invariant counterexample search

Suppose `Φ` is a propositional formula describing a safe operating region.

**DFS version**:
- push an initial state;
- visit successors until either all reachable states have been marked or `not Φ` is found;
- maintain a predecessor map if a trace is needed.

**BFS version**:
- enqueue all initial states at distance 0;
- explore layer by layer;
- stop at the first state violating `Φ`;
- follow predecessor pointers backward to reconstruct a shortest violating path.

Choose BFS when diagnostic brevity matters enough to justify the queue/memory cost.

## Failure Recovery

### A liveness property fails
- Inspect the lasso/cycle.
- If an action is perpetually or repeatedly enabled but never selected, identify which fairness class would exclude it.
- Validate realizability and implementation enforceability.
- If no justified fairness rule applies, retain the failure as a design issue.

### Safety proof succeeds but system still feels wrong
Check for a missing liveness requirement. Safety can allow a system that does nothing forever.

### Trace abstraction seems too coarse
If the claim depends on branching structure, action identity, exact next steps, or probabilities, move to the corresponding semantics in Ch 6, Ch 7, or Ch 10.

## Key Takeaways

1. Reachability turns many state-local verification questions into graph search.
2. Safety violations have finite bad prefixes; liveness violations require infinite-behavior reasoning.
3. Finite traces characterize safety preservation; full traces characterize all LT properties.
4. Verify safety and liveness components independently when a requirement mixes them.
5. Fairness is a modeling assumption about admissible schedules and must be realizable.
6. Mutual exclusion says nothing about starvation freedom.
7. Use BFS for shortest finite counterexamples and DFS when simple linear exploration is preferred.

## Connects To

- **Ch 4**: regular bad prefixes and ω-regular liveness become automata-checking problems.
- **Ch 5**: LTL provides a concise syntax for many LT properties and fairness conditions.
- **Ch 7**: trace inclusion/equivalence becomes a basis for abstraction and refinement.
- **Ch 8**: stutter-preserving POR relies on the observable trace semantics developed here.
- **Ch 10**: probabilistic models replace universal trace inclusion with probability measures while retaining safety/liveness ideas.
