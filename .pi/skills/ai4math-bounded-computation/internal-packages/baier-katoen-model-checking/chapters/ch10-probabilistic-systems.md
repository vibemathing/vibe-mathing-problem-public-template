# Chapter 10: Probabilistic Systems

## Core Idea

Probabilistic model checking replaces “is a behavior possible?” with quantitative questions about the **measure** of behaviors. Markov chains contain probabilistic choice only; Markov decision processes (MDPs) add nondeterminism resolved by schedulers. Reachability reduces to graph analysis plus equations/optimization, while long-run ω-regular behavior reduces to recurrent components combined with deterministic automata.

## Frameworks Introduced

### Discrete-time Markov chain (MC)
An MC is `M = (S, P, iota_init, AP, L)` where each state's outgoing probabilities sum to `1`.

**When to use**: the next-state distribution is fixed by the model, with no unresolved nondeterministic scheduling/environment choice.

**Modeling discipline**:
- use probability only when a distribution is part of the system/environment model;
- keep probabilities normalized;
- distinguish probability-zero events from impossible paths: a path can exist in the underlying graph yet have probability zero as an infinite event;
- use the underlying transition graph (`P(s,t) > 0`) for qualitative reachability preprocessing.

The MC has the memoryless property: the successor distribution depends on the current state, not the history used to reach it.

### Reachability probability in an MC
Goal: compute `Pr_s(C U B)`—reach target set `B` while staying in constraint set `C` before the hit.

**Procedure**:
1. identify `S=1`: states with probability `1` for the event when computable by graph analysis;
2. identify `S=0`: states with probability `0`;
3. let `S?` be the remaining states;
4. for each `s in S?`, introduce `x_s` and write
   `x_s = sum_t P(s,t) * x_t`, with boundary values `1` on `S=1`, `0` on `S=0`;
5. solve the resulting linear system;
6. validate by substituting the solution back into the equations.

Use the largest sound `S=0`/`S=1` sets because every classified state removes an unknown from the numerical system.

For step-bounded reachability, start from the boundary vector and iterate the linear recurrence a fixed number of times. For unbounded finite-MC reachability, the appropriate fixed point/equation system has a unique solution once probability-zero regions are handled as in the chapter.

### Qualitative probabilistic properties
Bounds `0` and `1` often admit graph algorithms without solving general numeric equations.

Typical questions:
- is a bad state reached with probability `0`?
- is a goal reached almost surely (`1`)?
- is a state recurrent with positive/one probability?

For finite MCs, long-run behavior is organized by **bottom strongly connected components (BSCCs)**. Almost surely a run eventually enters a BSCC; once inside, every state in that BSCC is visited infinitely often almost surely.

This makes many recurrence/persistence probabilities reducible to: identify accepting BSCCs, then compute the probability of reaching them.

### PCTL model checking
PCTL adds probability-threshold operators around temporal path formulae.

**When to use**: requirements such as “the probability of reaching failure is at most `10^-6`” or “delivery succeeds with probability at least `0.999`.”

**How**:
1. compute satisfaction sets bottom-up as in CTL;
2. for a probabilistic subformula, compute the constrained reachability probability from each state;
3. compare each value with the threshold/operator (`<`, `<=`, `>`, `>=`);
4. label the resulting satisfaction set and continue recursion.

PCTL's qualitative fragment uses probability bounds 0/1. Do not equate `P>0(F p)` with a plain CTL existential claim in all infinite settings without checking the chapter's model/logic conditions; probability measure can distinguish graph existence from positive measure.

### Linear-time probabilistic properties and deterministic ω-automata
For an ω-regular/LTL-style property `P` in a finite MC:
1. construct a deterministic Rabin automaton (DRA) for the property or the needed complement according to the probability being computed;
2. form the product MC;
3. determine which BSCCs satisfy the Rabin acceptance condition;
4. union those accepting recurrent regions into a success set;
5. compute the probability of eventually reaching the success set.

**Why deterministic?** Automaton nondeterminism would introduce an additional choice not governed by the MC probability measure. Deterministic acceptance keeps each system trace mapped to one automaton run.

### Probabilistic bisimulation
States are probabilistically bisimilar when:
1. their atomic-proposition labels agree; and
2. for every equivalence class `T`, their one-step probability of entering `T` is equal.

**When to use**: quotienting a Markov chain before PCTL/PCTL* checking.

For the finite setting treated in the chapter, probabilistic bisimulation matches the relevant PCTL/PCTL* logical indistinguishability results. Use partition refinement over cumulative probability to classes, not merely equality of graph successors.

### Markov chains with costs/rewards
Attach a nonnegative reward/cost to states/transitions (the chapter develops Markov reward-style models) to ask:
- expected accumulated reward before hitting a target;
- cost-bounded reachability;
- long-run average/expected reward measures.

**Operational route**: derive equations from one-step conditioning, combine with reachability classification, and solve the linear system. For cost-bounded questions, add the accumulated-cost dimension/recurrence as required by the model.

### Markov decision process (MDP)
An MDP `M = (S, Act, P, iota_init, AP, L)` combines:
- nondeterministic action choice;
- probabilistic successor choice once an action is selected.

**Use when**: concurrency/interleaving, control decisions, abstraction, or unknown environment behavior remains nondeterministic while some transitions are stochastic.

### Schedulers
A scheduler resolves the MDP's nondeterministic choices, potentially using execution history. Under a fixed scheduler, the MDP becomes a Markov chain.

Classes include:
- memoryless/positional: choice depends only on current state;
- finite-memory: choice depends on state plus finite mode;
- history-dependent/general schedulers.

**Modeling meaning**: scheduler quantification represents all admissible resolutions of nondeterminism, not an implementation detail to ignore.

### Extreme reachability in MDPs
For target `B`, define `Pr_max(s |= F B)` and `Pr_min(s |= F B)` over all schedulers.

**Bellman route for maximum**:
- `x_s = 1` for `s in B`;
- `x_s = 0` for states from which `B` cannot be reached;
- otherwise
  `x_s = max_{alpha in Act(s)} sum_t P(s,alpha,t) * x_t`.

Use `min` for minimum probability.

**Computation options**:
- **value iteration**: repeatedly apply Bellman updates from boundary values until the desired convergence/tolerance criterion is met;
- **linear programming**: encode Bellman inequalities/equalities as the chapter's LP characterization;
- **qualitative graph algorithms**: compute probability-0/1 regions without numerical iteration when the threshold is qualitative.

For unbounded reachability in finite MDPs, optimal **memoryless** schedulers exist. A subtlety from the chapter: if multiple actions achieve the same Bellman value, selecting an arbitrary maximizer can create a self-loop that never reaches the target. Construct the scheduler so an optimal action also makes progress in the optimal-action subgraph (for example using shortest-distance-to-target structure there).

For step-bounded reachability, an optimal scheduler may use finite memory to track the remaining horizon.

### PCTL over MDPs
The probability operator is interpreted over schedulers.

Decision rule:
- upper-bound assertion `P<=p(φ)` must hold for **all schedulers**, so check `Pr_max(φ) <= p`;
- lower-bound assertion `P>=p(φ)` must hold for **all schedulers**, so check `Pr_min(φ) >= p`.

Strict bounds use the corresponding strict comparison.

### End components and long-run MDP behavior
A set of states plus a permitted action set forms an **end component** when the selected actions keep probability mass inside the set and the induced graph is strongly connected. A **maximal end component (MEC)** is not contained in a larger end component.

**Use when**: limiting behavior, recurrence, ω-regular objectives, or fairness.

Under a scheduler, long-run behavior almost surely settles into an end-component-like recurrent region. Therefore:
1. compute MECs/end components;
2. identify those satisfying the limiting/Rabin acceptance condition;
3. make their union a success set;
4. reduce the extreme long-run probability to reachability of that success set.

### ω-regular objectives in MDPs
For property `P`:
1. construct a DRA for `P`;
2. form product MDP `M ⊗ A`;
3. find end components satisfying a Rabin pair;
4. union them into success set `U_A`;
5. compute maximal/minimal probability of reaching `U_A`.

This also supports PCTL* by recursively replacing state subformulae, translating the remaining path formula, and computing extreme probabilities. The chapter notes polynomial dependence on MDP size with double-exponential dependence on the PCTL* formula in the general construction.

### Fairness in MDPs
Probabilistic branching is almost surely strongly fair in the sense developed for MCs, but MDP **nondeterministic action choice** can still starve a process.

A scheduler is fair with respect to an LTL fairness assumption when, from every state, it generates fair paths with probability `1`.

**Procedure**:
1. state the fairness assumption separately;
2. check realizability—some fair scheduler must exist;
3. restrict analysis to fair schedulers;
4. for finite MDPs and realizable fairness, exploit finite-memory fair schedulers/end-component structure.

Important reachability fact from the chapter: realizable fairness does **not reduce the supremal/maximal constrained reachability probability**; there exists a finite-memory fair scheduler attaining the same maximum. Other objective directions, especially minima/long-run constraints, still need fairness-aware component analysis.

## Key Concepts

- **Probability measure**: assigns probabilities to measurable sets of infinite paths; cylinder sets generated by finite prefixes form the basis.
- **Almost surely**: probability `1`; distinct from “all paths.”
- **Positive probability**: greater than `0`; distinct from mere graph reachability in general infinite-behavior questions.
- **BSCC**: strongly connected component with no outgoing transitions in an MC graph.
- **PCTL/PCTL***: branching probabilistic temporal logics with quantitative thresholds.
- **DRA**: deterministic Rabin automaton for ω-regular languages.
- **Reward/cost**: quantitative accumulation attached to stochastic behavior.
- **Scheduler**: resolver of MDP nondeterminism.
- **Value iteration**: iterative Bellman fixed-point approximation.
- **End component/MEC**: MDP recurrent region sustainable under selected actions.
- **Fair scheduler**: scheduler that produces fair paths almost surely.

## Mental Models

- **Graph first, numbers second**: compute impossibility/certainty regions before solving equations; this reduces numeric work and clarifies boundary conditions.
- **MC = probability only; MDP = nondeterminism + probability.** Never average over nondeterministic scheduler choices unless the model explicitly supplies a distribution.
- **A fixed scheduler turns an MDP into an MC**: use this to reason about evidence and synthesized policies.
- **Long-run probability lives in recurrent components**: BSCCs for MCs, end components/MECs for MDPs.
- **Use deterministic property automata in stochastic products** so monitor behavior adds no uncontrolled choice.
- **Almost surely is weaker than universally**: probability-0 paths may still exist in the graph.

## Anti-patterns

- **Treating nondeterminism as uniform probability**: changes an MDP into an unjustified MC.
- **Ignoring states with probability 0/1 before solving equations**: wastes computation and can obscure uniqueness conditions.
- **Using SCCs as MDP end components without checking action closure**: a scheduler may be unable to stay in the SCC with the chosen actions.
- **Picking any Bellman-maximizing action in a tie**: can synthesize a policy that fails to realize the computed reachability value.
- **Using an NBA directly in a probabilistic product where determinism is required**: automaton choice would contaminate the probability semantics.
- **Equating probability 1 with path-universal certainty**: measure-zero counterpaths can remain.
- **Applying fairness to probabilistic outcomes rather than scheduler nondeterminism**: stochastic successor selection already has its own almost-sure recurrence properties.
- **Comparing a numerically approximated value to a tight threshold without error bounds**: can flip a PCTL result.

## Reference Tables

### Quantitative routing

| Model | Question | Main method |
|---|---|---|
| MC | reach `B` | graph 0/1 classification + linear equations |
| MC | qualitative recurrence | BSCC analysis |
| MC | PCTL | recursive Sat sets + reachability probabilities |
| MC | ω-regular/LTL probability | DRA product + accepting BSCC reachability |
| MDP | max/min reachability | Bellman + value iteration/LP + scheduler |
| MDP | long-run/ω-regular | DRA product + accepting end components/MECs |
| MDP | fairness-sensitive liveness | fair scheduler + fair end-component analysis |

### PCTL threshold semantics on MDPs

| Formula shape | Extreme probability to compute |
|---|---|
| `P<=p(φ)` | `Pr_max(φ)` and require `<= p` |
| `P<p(φ)` | `Pr_max(φ)` and require `< p` |
| `P>=p(φ)` | `Pr_min(φ)` and require `>= p` |
| `P>p(φ)` | `Pr_min(φ)` and require `> p` |

## Worked Example: MC reachability equations

Suppose target `B` is absorbing, some states cannot reach `B`, and the remaining states are uncertain.

1. Set `x_s = 1` on `B` and on any proven almost-sure states.
2. Set `x_s = 0` where the underlying graph cannot reach `B` (or more generally where the constrained probability is proven zero).
3. For each unknown state `s`, write
   `x_s = Σ P(s,t) x_t`.
4. Solve all unknowns simultaneously.
5. Check every equation and `[0,1]` range.

This “one-step conditioning” is the reusable pattern behind many expected reward and constrained probability equations too.

## Worked Example: randomized mutual exclusion under an unfair scheduler

A randomized arbiter may choose fairly between competing processes, yet the surrounding interleaving can still be nondeterministic. An MDP scheduler can repeatedly select process 2's actions and ignore process 1 forever. The random choice inside the arbiter does not force the scheduler to schedule process 1.

Therefore:
1. distinguish probabilistic arbiter fairness from process-scheduling fairness;
2. state process fairness as a scheduler constraint;
3. check a fair scheduler exists;
4. evaluate liveness under fair schedulers.

The same distinction appears in randomized dining-philosopher examples: probability does not automatically resolve interleaving starvation.

## Worked Example: reachability-optimal memoryless scheduler

Compute maximal target probabilities `x_s` by Bellman equations. Let `Act_max(s)` contain actions achieving the Bellman maximum.

Bad synthesis rule: pick an arbitrary action in `Act_max(s)`. If one maximizing action self-loops forever and another moves toward the target, the first can preserve the equation value algebraically while failing to realize target reachability operationally.

Robust construction:
1. restrict to maximizing actions;
2. in the resulting optimal-action graph, compute a shortest path distance to the target for states that can reach it;
3. at each such state, choose a maximizing action with positive probability to a state of smaller distance;
4. choose arbitrary actions only where target reachability is impossible.

This yields the memoryless scheduler existence result constructively.

## Failure Recovery

### Probability result looks inconsistent with graph structure
- verify each outgoing distribution sums to `1`;
- compute graph reachability/BSCCs first;
- check boundary sets `S=0/S=1`;
- substitute values into equations and inspect residuals.

### Value iteration seems stalled or threshold is close
Use a tighter certified error bound, Gauss–Seidel/alternative numerical method, or LP/exact rational solving when feasible. Do not report a threshold verdict based only on a loose stopping delta.

### MDP counterexample depends on scheduler behavior
Return the scheduler/policy choices together with the probabilistic path evidence. A probability bound over all schedulers is incomplete without showing which adversarial/optimal scheduler attains or approaches the extreme.

### Long-run objective resists path-by-path reasoning
Move to BSCC/MEC analysis; infinite stochastic behavior is governed by recurrent components.

## Key Takeaways

1. Markov chains quantify fixed probabilistic branching; MDPs add scheduler-resolved nondeterminism.
2. Reachability probability is graph preprocessing plus linear equations; qualitative 0/1 cases are often graph-only.
3. PCTL recursively embeds these quantitative reachability computations.
4. ω-regular probabilities use deterministic property automata and recurrent components.
5. Probabilistic bisimulation preserves quantitative temporal behavior by matching probability mass to equivalence classes.
6. MDP max/min reachability is a Bellman optimization problem; value iteration and LP are core algorithms.
7. Finite unbounded reachability admits optimal memoryless schedulers, with care needed when breaking Bellman ties.
8. BSCCs/MECs are the right abstraction for long-run behavior.
9. Fairness constrains scheduler nondeterminism and must be realizable.
10. Probability `1` and universal path truth are distinct notions.

## Connects To

- **Ch 2**: MDP nondeterminism inherits interleaving/environment semantics; MC probability replaces nondeterministic successor choice only when justified.
- **Ch 3**: safety, liveness, fairness, and recurrence reappear in quantitative form.
- **Ch 4–5**: ω-regular/LTL property automata are reused, with determinism required for the probabilistic product route.
- **Ch 6**: PCTL follows a CTL-style recursive satisfaction-set structure.
- **Ch 7**: probabilistic bisimulation adapts quotienting to probability mass over equivalence classes.
