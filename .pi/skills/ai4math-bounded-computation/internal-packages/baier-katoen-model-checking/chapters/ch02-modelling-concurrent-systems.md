# Chapter 2: Modelling Concurrent Systems

## Core Idea

A model checker can reason only about the transition semantics it receives. This chapter turns sequential, concurrent, shared-state, synchronous, and channel-based systems into transition systems, with special attention to nondeterminism and atomicity—the two modeling choices most likely to change verification results.

## Frameworks Introduced

### Transition system (TS)
A transition system is a tuple

`TS = (S, Act, ->, I, AP, L)`

with states `S`, actions `Act`, transition relation, initial states `I`, atomic propositions `AP`, and labeling function `L : S -> 2^AP`.

**When to use**: as the semantic target for qualitative model checking.

**How**:
1. Put behaviorally relevant storage/control information in a state.
2. Put possible system steps in the transition relation.
3. Mark all legal initial states.
4. Choose `AP` from the requirements you need to state; avoid exposing irrelevant state detail.
5. Preserve action labels only when action identity matters for communication/fairness/equivalence.

A state with no successor is **terminal**. `Reach(TS)` contains the states reachable by a finite execution from an initial state. An **execution** is an initial maximal execution fragment: infinite, or finite and ending in a terminal state.

### Program graph → transition system
A program graph separates control flow from data:

`PG = (Loc, Act, Effect, ->, Loc0, g0)`

Edges carry a guard and action. Its TS has states `(location, valuation)`; a guarded action becomes an unguarded transition only when its guard is true, and `Effect` updates the valuation.

**When to use**: data-dependent software/processes where explicit state enumeration should be derived from a compact guarded representation.

### Concurrency composition decision
Use the smallest semantic mechanism that actually matches the implementation:

| Interaction | Modeling route | Key rule |
|---|---|---|
| independent components | TS interleaving | choose one enabled component step nondeterministically |
| shared variables | program-graph interleaving | share one valuation; do not multiply inconsistent local copies |
| synchronous event | handshaking | matching action must occur together |
| asynchronous messages | FIFO channels | send enqueues when not full; receive dequeues when nonempty |
| zero-capacity channel | synchronous message passing | send and receive occur together with data transfer |
| clock-step hardware | synchronous product | components advance in lock-step |

### Atomicity boundary
**When to use**: every time a process edge represents multiple source-level operations.

A program-graph action is indivisible. If an edge is labeled with `read; compute; write`, then no other process can interleave inside it. This is a semantic claim, not a notation convenience.

**Decision rule**: if the real system can observe or interfere with an intermediate configuration relevant to the property, split the action into multiple transitions.

### NanoPromela semantics
The book introduces a small Promela-like guarded-command language as a bridge from textual process models to channel systems/TSs.

- `skip` terminates in one step without changing data.
- assignment changes a variable.
- `c?x` and `c!expr` receive/send through a channel.
- sequential composition executes left then right.
- `atomic{...}` suppresses interleavings inside the region.
- `if :: g1 -> s1 ... fi` nondeterministically selects an enabled guarded command; if none is enabled, it blocks.
- `do :: g1 -> s1 ... od` repeats enabled guarded commands; if none is enabled, the loop terminates.

The guard selection and first step use a test-and-set style atomic interpretation in the presented semantics.

## Key Concepts

- **Nondeterminism**: represents unknown scheduling, environment choices, underspecification, or competing enabled transitions. It does not assign likelihoods.
- **Action-determinism**: at most one initial state and at most one successor for each state/action pair.
- **AP-determinism**: observable next-state labels uniquely determine the successor under the chapter's definition.
- **Pre/Post**: direct predecessor/successor operators, later reused by reachability and temporal-logic algorithms.
- **Interleaving**: models concurrency as all admissible serial orders of atomic component steps.
- **Independence**: two actions can be reordered without changing the result; this becomes the basis of partial-order reduction in Ch 8.
- **Shared variable**: a variable accessed by multiple processes; critical actions may contend and their order can change the result.
- **Handshake set `H`**: actions that components must perform synchronously; actions outside `H` interleave independently.
- **Channel capacity**: `0` means synchronous transfer; positive finite/infinite capacity gives buffered asynchronous communication.
- **Environment nondeterminism**: an open system may receive arbitrary values from its declared input domain.
- **State-space explosion**: Cartesian products of components and valuations grow exponentially even when each component is small.

## Mental Models

- **Use AP as a property interface**: expose only what future formulas need to observe. A smaller observability vocabulary can support stronger reductions later.
- **Think of nondeterminism as a set of possible worlds**. Model checking must respect every world unless a later fairness/scheduler constraint excludes some.
- **Treat interleaving as an abstraction of real parallel timing**. It captures possible orderings, not physical processor speeds.
- **Model communication at the level where contention occurs**. Shared-variable conflicts disappear if each process incorrectly keeps its own copy.
- **Treat channel capacity as semantics**: capacity changes blocking and therefore reachable behavior.

## Anti-patterns

- **Cartesian-producting transition systems that each contain their own copy of a shared variable**: creates impossible global states.
- **Treating dependent actions as independent**: reordering can change values and invalidate the interleaving argument.
- **Assuming tests and assignments are automatically atomic**: a frequent source of missed concurrency bugs.
- **Hiding a blocking operation inside an atomic region**: can create semantics unlike the intended implementation and may distort liveness.
- **Reading nondeterministic alternatives as equally probable**: probabilities appear only in the probabilistic models of Ch 10.
- **Choosing an infinite variable domain without an abstraction plan**: the TS may become infinite and leave the core finite-state algorithms inapplicable.
- **Omitting unexpected protocol messages**: a receiver that handles only the expected case may deadlock after retransmission or delay.

## Reference Tables

### Execution vocabulary

| Term | Operational test |
|---|---|
| finite execution fragment | alternating states/actions following transitions |
| maximal fragment | infinite, or finite ending in terminal state |
| initial fragment | begins in an initial state |
| execution/run | initial + maximal |
| reachable state | terminates some finite initial fragment |

### Channel enabledness

| Action | Enabled when | Effect |
|---|---|---|
| buffered send `c!v` | channel not full | append `v` to rear |
| buffered receive `c?x` | channel nonempty | remove front value and assign to `x` atomically |
| zero-capacity send/receive | complementary actions are simultaneously enabled | synchronous data transfer |

## Worked Example: Peterson-style mutual exclusion and atomicity

Two processes share Boolean intent flags `b1`, `b2` and a turn variable `x`. A process sets its intent, gives the other process priority via `x`, waits until the other is not interested or the turn favors itself, enters the critical section, then clears its flag.

The model shows two separate lessons:

1. **Property check**: in the intended ordering, no reachable state has both processes in their critical sections, so mutual exclusion holds.
2. **Modeling sensitivity**: the multiple assignments can be modeled atomically for compactness only when that matches the intended implementation. If the assignments are split, their order matters. Setting the turn variable before setting the intent flag permits an interleaving where both processes enter. Setting the intent first preserves mutual exclusion in the analyzed variant.

Use this as a template when modeling lock algorithms:

1. list every shared read/write;
2. mark actual atomic instructions;
3. expand ambiguous compound statements into separate control locations;
4. generate reachable states;
5. check `not(crit1 and crit2)` as an invariant;
6. only compress transitions after proving the compression does not remove relevant interleavings.

## Worked Example: alternating-bit protocol modeling

A sender and receiver communicate over an unreliable data channel and a reliable acknowledgement channel. The sender retransmits after a timeout. The alternating control bit lets the receiver distinguish a retransmission from a new datum.

A robust model must include the path where:
1. data is delivered;
2. sender times out before seeing the acknowledgement;
3. sender retransmits the old data;
4. receiver has already advanced to the next expected bit;
5. receiver recognizes and ignores the duplicate while acknowledging appropriately.

If the receiver model omits that “unexpected old bit” transition, the modeled protocol can halt even though the real protocol should tolerate retransmission. This illustrates why environment/protocol corner cases belong in the transition relation rather than being dismissed as unlikely.

## State-Space Explosion Heuristic

Before generating the global TS, estimate the multiplicative structure:

- control locations multiply across processes;
- each finite-domain variable multiplies the valuation space;
- channel contents add sequence combinations up to capacity;
- interleavings multiply path count even when state count stays manageable.

If this estimate is already too large, preserve a compact structured model and plan symbolic checking, abstraction, or POR before brute-force enumeration.

## Key Takeaways

1. The semantics of a model are determined by states, transitions, composition, and atomicity choices.
2. Use transition systems as the common semantic target; use program graphs/channel systems to build them correctly.
3. Interleaving is sound for independent actions and must represent all relevant schedules.
4. Shared variables require one shared valuation, and synchronization/channel capacity affects reachability.
5. Nondeterminism expresses possible choice, not probability.
6. Keep AP property-focused and validate the model with concrete execution scenarios.
7. Expect global state spaces to grow multiplicatively; reduction choices come later with preservation proofs.

## Connects To

- **Ch 3**: paths, traces, reachability, safety/liveness, and fairness are defined over these models.
- **Ch 7**: equivalences depend on state labels/actions introduced here.
- **Ch 8**: action independence turns interleaving redundancy into a reduction opportunity.
- **Ch 9**: timed automata add clocks to the program-graph idea.
- **Ch 10**: Markov chains replace nondeterministic successor choice with probability; MDPs combine both.
