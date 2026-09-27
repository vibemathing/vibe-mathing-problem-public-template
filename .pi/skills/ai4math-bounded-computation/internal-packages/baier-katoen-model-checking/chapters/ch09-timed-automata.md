# Chapter 9: Timed Automata

## Core Idea

Timed automata add dense real time to finite control by using clocks, guards, resets, and location invariants. Their concrete semantics is infinite, but a finite **region transition system** quotients clock valuations by a bisimulation fine enough for the automaton and TCTL formula, reducing timed verification to CTL-style checking.

## Frameworks Introduced

### Timed automaton
A timed automaton extends a program-graph-like control structure with real-valued clocks that advance uniformly with time.

**Use when**: a requirement depends on elapsed time, deadlines, minimum/maximum delays, timeout windows, or race timing that an untimed interleaving model cannot express.

Core elements:
- **locations**: control states;
- **clocks**: nonnegative real variables that all increase at the same rate;
- **guards**: clock constraints controlling when a discrete edge may fire;
- **resets**: selected clocks set to zero on an edge;
- **location invariants**: constraints limiting how long the system may remain in a location;
- **actions/AP**: discrete labels/observations as in transition-system models.

Concrete transitions are of two kinds:
1. **delay transition**: let time `d >= 0` pass while the location invariant remains valid;
2. **discrete transition**: take an enabled guarded edge, reset its clock set, and land in a state satisfying the target invariant.

### Model timing at the right semantic boundary
Use a clock to measure the time since an event only if later decisions/properties depend on that duration.

Modeling recipe:
1. identify control events that start timing intervals;
2. reset a clock on those events;
3. encode earliest/latest firing constraints as guards;
4. encode upper residence bounds as location invariants;
5. keep untimed data/communication structure from Ch 2;
6. compose timed components so **time passage is synchronized globally** while discrete actions synchronize/interleave according to the chosen composition.

### Time divergence, timelock, and zenoness
A timed path is **time-divergent** when elapsed time grows without bound.

A state is a **timelock** when no time-divergent path can continue from it. Timelock freedom therefore means every reachable state has at least one time-divergent continuation.

A **zeno path** performs infinitely many discrete actions in only bounded elapsed time. A non-zeno timed automaton has no initial zeno paths under the chapter's definition.

**Sufficient non-zeno criterion**: if every control cycle necessarily lets at least one time unit elapse, zeno executions are excluded. This is sufficient, not a characterization of all non-zeno models.

Operational difference:
- **timelock**: no admissible time-divergent future from a state;
- **zeno behavior**: an infinite action sequence can compress into finite time.

Check both when progress depends on real time.

### TCTL
Timed CTL extends CTL with clock constraints and time-bounded until modalities. Path quantifiers range over **time-divergent paths**, analogous to fair CTL restricting quantification to admissible paths.

Use TCTL for requirements such as:
- “a response is reached within `k` time units”;
- “a bad state cannot occur during the next interval `J`”;
- “from every state, a deadline is eventually met along all time-divergent executions.”

### Eliminate timing parameters with fresh clocks
For a timed-until subformula with interval `J`, introduce a fresh clock `z`, reset it to zero when evaluating the subformula, and replace the bounded-until obligation by an untimed CTL-style until whose goal additionally requires `z in J`.

This produces a formula where timing appears as atomic clock constraints. Repeat recursively for timed subformulae as needed.

**Why it matters**: it separates time measurement from the branching-time fixed-point algorithm.

### Clock-region equivalence
Infinite clock valuations are grouped into finitely many equivalence classes based on the clock constants appearing in the timed automaton and formula.

Two valuations are region-equivalent when they agree on the information that can affect those constraints, including:
- which bounded integer interval/value each clock occupies, or whether it exceeds its largest relevant constant;
- whether relevant fractional parts are zero;
- the ordering of fractional parts among clocks below/within the relevant bounded ranges.

The resulting clock equivalence:
1. preserves all relevant clock constraints;
2. yields equivalent future timed behavior;
3. has finitely many classes;
4. is a bisimulation over the relevant propositions/clock constraints.

### Region transition system (RTS)
A region state combines a control location with a clock region. Discrete/reset steps and successor-time-region steps define a finite transition graph.

**Use when**: applying the book's basic TCTL decision procedure or checking timelock freedom.

Correctness result: for a non-zeno timed automaton and the transformed timing-parameter-free TCTL formula, TCTL satisfaction in the concrete infinite timed semantics agrees with CTL satisfaction in the region transition system.

### TCTL model checking
Basic procedure:
1. ensure the timed model assumptions needed by the algorithm are explicit (the chapter's basic algorithm uses non-zeno/timelock-free conditions where stated);
2. recursively transform timed subformulae using fresh clocks;
3. build the region transition system determined by the automaton and formula constants;
4. compute satisfaction sets bottom-up as in CTL;
5. label region states with each solved subformula;
6. check whether all initial region states satisfy the full formula;
7. map a region-level witness/counterexample back to a timed behavior.

The checking time is linear in formula length and the size of the region graph. Region count grows exponentially with the number of clocks and their maximal relevant constants. The TCTL model-checking problem is PSPACE-complete.

## Key Concepts

- **Clock valuation**: mapping from clocks to nonnegative real values.
- **Clock constraint**: comparison of clock values with constants, used in guards/invariants/formulae.
- **Reset set**: clocks assigned zero on a discrete transition.
- **Delay transition**: passage of real time without changing location.
- **Time-divergent path**: path on which accumulated delay is unbounded.
- **Timelock**: state without a time-divergent continuation.
- **Zeno path**: infinitely many actions in bounded total time.
- **TCTL**: timed branching-time logic with interval-constrained temporal operators.
- **Clock region**: equivalence class of valuations indistinguishable by relevant clock constraints and region behavior.
- **Region transition system**: finite quotient used for verification.
- **Formula-dependent quotient**: the constants in the property can refine the needed region partition, so changing a property can change the region graph.

## Mental Models

- **Separate ordering from timing**: Ch 2 interleaving tells what order actions can take; timed automata add how much time may/must pass between them.
- **Guards say “may leave now”; invariants say “may stay this long.”** Use the two roles deliberately.
- **Treat time-divergence as admissibility**: a path that performs forever while time stops may be mathematically present but excluded from TCTL path quantification under the chapter's semantics.
- **Regions remember only clock facts future guards/formulas can distinguish**. This is a bisimulation quotient, not arbitrary discretization.
- **Clock count is expensive**: every unnecessary clock and large constant can multiply regions.

## Anti-patterns

- **Encoding a real-time requirement in an untimed TS with arbitrary interleaving**: cannot prove a deadline such as “gate closes before train arrives.”
- **Using guards where an invariant is required**: a guard constrains an edge but does not by itself force departure before time exceeds a bound.
- **Ignoring timelocks**: a property can look vacuously satisfied if time cannot progress from problematic states.
- **Ignoring zeno behavior**: infinitely many actions in finite time can invalidate intended physical interpretations.
- **Adding one clock per syntactic convenience**: region count can become unmanageable.
- **Treating region abstraction as approximate rounding**: region equivalence is constructed to preserve relevant constraints and is proved as a bisimulation.
- **Quoting TCTL complexity only as “linear”**: it is linear in the explicit RTS size, while the RTS may be exponential; the decision problem is PSPACE-complete.

## Reference Tables

### Modeling construct decision

| Timing need | Construct |
|---|---|
| wait at least `a` before action | guard such as `x >= a` |
| action must occur before/at `b` | location invariant `x <= b` plus appropriate enabled exit |
| measure time since event | reset `x := 0` at event |
| enforce a window `[a,b]` | combine guard lower bound + invariant/guard upper bound |
| component clocks share physical time | synchronized delay transitions |

### Failure check

| Symptom | Diagnose |
|---|---|
| no outgoing discrete edge | may still allow delay; inspect invariant |
| time cannot progress and no useful action | timelock candidate |
| infinite action loop with shrinking/no delay | zeno candidate |
| RTS enormous | too many clocks/constants; property-induced fresh clocks also count |

## Worked Example: railroad crossing timing flaw

The untimed railroad-crossing model from Ch 2 can reach a state where the train has signaled “approaching” and the controller is starting to lower the gate, yet interleaving still lets the train enter the crossing before the gate transition completes. The untimed model cannot express the physical assumption “closing the gate takes less time than the train needs to reach the crossing.”

Timed-model repair:
1. introduce a train clock reset when the approach signal is sent;
2. constrain the train's transition into the crossing with its travel-time bound;
3. introduce gate timing if lowering is not instantaneous;
4. make the safety property observe `train_in_crossing -> gate_down`;
5. use TCTL/region checking to determine whether all time-divergent behaviors respect the timing relationship.

The example demonstrates that an untimed counterexample may reveal a missing timing assumption rather than a wrong control protocol.

## Worked Example: region intuition with one clock

Suppose only comparisons to constant `1` matter. Instead of infinitely many values `x = 0.13`, `0.14`, …, region reasoning distinguishes a finite set of cases such as:

- `x = 0`;
- `0 < x < 1`;
- `x = 1`;
- `x > 1`.

All values inside `(0,1)` satisfy the same comparisons with `0` and `1` and can mimic one another's relevant timed behavior at the region level. With several clocks, the ordering of their fractional parts adds distinctions because it determines which clock crosses the next integer boundary first.

## Failure Recovery

### Region graph is too large
- remove clocks that never affect guards/invariants/properties;
- reduce unnecessarily large constants if the model semantics permit;
- isolate timing properties so formula-introduced clocks stay minimal;
- use more advanced symbolic timed representations such as zones only as an extension beyond the book's basic region algorithm, and label that extension explicitly.

### Counterexample seems physically impossible
Check whether the model omitted a minimum delay, upper invariant, synchronization, or environment timing constraint. Do not dismiss the counterexample until the missing physical assumption has been formalized.

### TCTL result depends on pathological time behavior
Check non-zenoness, time-divergence semantics, and timelock freedom before accepting the conclusion.

## Key Takeaways

1. Timed automata model dense time with clocks layered over finite control.
2. Guards constrain when edges may fire; invariants constrain how long locations may persist.
3. Time divergence, timelock, and zenoness are distinct and must be analyzed explicitly.
4. TCTL quantifies over time-divergent paths and adds interval-constrained temporal obligations.
5. Clock-region equivalence yields a finite bisimulation quotient suitable for CTL-style checking.
6. Region size is exponential in clock structure/constants; TCTL model checking is PSPACE-complete.
7. Counterexamples often diagnose a missing timing assumption, which must be added to the model rather than hand-waved away.

## Connects To

- **Ch 2**: timed automata extend program-graph/concurrency models with clocks and globally synchronized delay.
- **Ch 6**: TCTL checking reuses CTL satisfaction-set algorithms on the region graph.
- **Ch 7**: clock-region equivalence is justified as a bisimulation.
- **Ch 10**: real time and probability are separate extensions in this book; do not infer stochastic timing from nondeterministic delays.
