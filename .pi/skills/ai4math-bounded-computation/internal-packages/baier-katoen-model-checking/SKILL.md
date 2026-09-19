---
name: baier-katoen-model-checking
description: "Model checking: TS, safety, LTL/CTL, TCTL/PCTL, POR, MDP."
---

<!-- argument-hint: [model-checking task, concept, logic, algorithm, or chapter number] -->

# Principles of Model Checking
**Authors**: Christel Baier, Joost-Pieter Katoen | **Primary source**: 994-page first-edition PDF | **Supplement**: selected exercise solutions | **Generated**: 2026-09-11

## How to Use This Skill

Use this file as the controller. Load only the chapter needed for the task.

1. Identify the user's verification goal and system class.
2. Route by model and property semantics using the rules below.
3. Read the linked chapter before applying a detailed algorithm, theorem condition, or reduction.
4. State modeling assumptions, fairness assumptions, and preservation conditions explicitly.
5. If a check fails, classify the failure before changing the model or property.
6. Finish with the `SELF_CHECK` at the end of this file.

### Inputs expected

Use whatever the user has: a transition/system model, program or protocol description, formal or informal requirement, property formula, counterexample, reduction question, or timed/probabilistic model. Ask for missing semantics only when they change the verification conclusion. In particular, identify the state variables/observations, transition or scheduler semantics, initial states, and the requirement to be checked.

### When not to use

Do not route unrelated programming, general mathematics, or post-book research surveys here. Do not use this skill as a complete decision procedure for arbitrary infinite-state/parameterized systems, or as a substitute for testing an implementation that lacks a validated formal model.

### Fast routing

- **Finite-state/concurrent modeling, atomicity, communication** → [ch02](chapters/ch02-modelling-concurrent-systems.md)
- **Deadlock, invariant, safety/liveness, fairness** → [ch03](chapters/ch03-linear-time-properties.md)
- **Regular or ω-regular monitors, product constructions, accepting cycles** → [ch04](chapters/ch04-regular-properties.md)
- **Trace-oriented temporal requirements** → [ch05](chapters/ch05-linear-temporal-logic.md)
- **Branching-time requirements, witnesses, symbolic BDD checking** → [ch06](chapters/ch06-computation-tree-logic.md)
- **Abstraction/equivalence/refinement** → [ch07](chapters/ch07-equivalences-and-abstraction.md)
- **Too many interleavings** → [ch08](chapters/ch08-partial-order-reduction.md)
- **Dense time, deadlines, clocks** → [ch09](chapters/ch09-timed-automata.md)
- **Probabilities, quantitative thresholds, MDP schedulers** → [ch10](chapters/ch10-probabilistic-systems.md)
- **Workflow, result diagnosis, verification vs validation** → [ch01](chapters/ch01-system-verification.md)
- **Notation/logic/graph/complexity prerequisites** → [ch11](chapters/ch11-preliminaries.md)

---

## Core Frameworks & Decision Logic

### 1. Verification loop: model → property → check → diagnose → revise

Use this loop for every verification task:

1. **Model** the system at an abstraction level that preserves the behavior relevant to the requirement.
2. **Sanity-check** the model with concrete simulations/scenarios.
3. **Formalize** the requirement independently of the model description.
4. **Run** the appropriate model-checking algorithm.
5. **Interpret the outcome**:
   - property holds → continue with other stated requirements;
   - property fails → replay the diagnostic and classify it as a **model error**, **design error**, or **property error**;
   - resource exhaustion → reduce the state space using a method whose preservation theorem covers the property class.
6. If the **model changes**, recheck earlier properties whose result depended on that model. A property-only correction on an unchanged valid model does not invalidate unrelated checks.

Keep verification separate from validation: verification asks whether the formal model satisfies the formal property; validation asks whether those formal artifacts represent the intended system and requirement.

### 2. Model semantics before property logic

Before choosing LTL, CTL, TCTL, or PCTL, establish what one transition means.

- Use **pure interleaving** only for independent component actions.
- Use **program-graph composition** when processes share variables.
- Use **handshaking** for synchronous interaction; a zero-capacity channel is synchronous message passing.
- Use **buffered FIFO channels** for asynchronous communication.
- Treat an action as atomic only when the implementation really excludes intermediate interleavings relevant to the property.
- Treat nondeterminism as unknown choice, scheduling, underspecification, or environment freedom. Do not infer probabilities from it.

### 3. Property routing

Ask how a violation can be witnessed:

- **Reachability / invariant / deadlock**: a finite reachable state suffices → graph search, [ch03](chapters/ch03-linear-time-properties.md).
- **Safety**: every violation has a finite bad prefix → bad-prefix reasoning; if regular, finite automaton + product, [ch04](chapters/ch04-regular-properties.md).
- **Liveness / recurrence**: no finite prefix alone proves failure → infinite-behavior/accepting-cycle methods; inspect fairness, [ch03](chapters/ch03-linear-time-properties.md) and [ch04](chapters/ch04-regular-properties.md).
- **LTL**: property is about traces and temporal order along executions → [ch05](chapters/ch05-linear-temporal-logic.md).
- **CTL**: requirement quantifies over branching alternatives inside temporal operators → [ch06](chapters/ch06-computation-tree-logic.md).
- **CTL\***: both kinds of nesting are genuinely needed and the extra complexity is justified → [ch06](chapters/ch06-computation-tree-logic.md).
- **TCTL**: truth depends on dense-time bounds → [ch09](chapters/ch09-timed-automata.md).
- **PCTL/PCTL\***: truth depends on probability thresholds → [ch10](chapters/ch10-probabilistic-systems.md).

LTL and CTL are incomparable. Do not translate between them by merely changing notation.

### 4. Automata-product pattern

Use this pattern when a property can be recognized by an automaton:

1. Build an automaton for **undesired behavior** or for the needed acceptance condition.
2. Form the product with the system.
3. Convert the property question into a graph question:
   - finite accepting state reachable → regular safety violation;
   - reachable accepting cycle → ω-regular/LTL violation.
4. Project the product witness back to a system execution.

For LTL, translate the negated formula to a GNBA/NBA and use nested DFS or another accepting-cycle algorithm. For probabilistic ω-regular analysis, use a **deterministic** ω-automaton such as a DRA and reason about recurrent components.

### 5. Fairness policy

Add fairness only when it models a scheduling guarantee or admissible environment behavior.

- **Unconditional**: an action/process must occur infinitely often.
- **Strong**: enabled infinitely often ⇒ taken infinitely often; useful for repeated contention.
- **Weak**: continuously enabled from some point ⇒ eventually/repeatedly taken; useful for persistent enabledness.

Check realizability. A nonrealizable fairness assumption can make a liveness claim vacuously true. Realizable fairness does not repair a genuine safety defect.

### 6. State-space explosion: preserve first, reduce second

Route by the source of growth and target logic:

- Boolean regularity → **ROBDD symbolic checking** ([ch06](chapters/ch06-computation-tree-logic.md)).
- Behaviorally equivalent states → **bisimulation/simulation quotienting** ([ch07](chapters/ch07-equivalences-and-abstraction.md)).
- Independent interleavings → **partial-order reduction** ([ch08](chapters/ch08-partial-order-reduction.md)).
- Dense clocks → **region abstraction** ([ch09](chapters/ch09-timed-automata.md)).

Record the preservation condition before reducing. Next-step operators are a common boundary: stutter-based abstraction and standard ample-set reductions target next-free logics.

### 7. Timed and probabilistic branches

**Timed systems:** model clocks, guards, resets, and location invariants; distinguish time divergence, timelock, and zeno behavior. TCTL checking reduces to CTL over a finite region transition system; region count is exponential in clocks/constants, and TCTL model checking is PSPACE-complete.

**Markov chains:** preprocess probability-0/1 regions with graph algorithms, then solve reachability probabilities by linear equations. **MDPs:** schedulers resolve nondeterminism; min/max reachability uses Bellman equations, value iteration, or linear programming. For unbounded reachability in finite MDPs, optimal memoryless schedulers exist, but a Bellman tie must still be chosen so reachability progress is preserved.

### 8. Failure recovery

When a result looks wrong or the algorithm fails:

- **Counterexample contradicts intended system** → model error; repair model, then regression-check prior properties.
- **Counterexample is a legal system behavior** but contradicts requirement → design error.
- **Counterexample exposes a mismatch in the formula** → property error; fix the formula and recheck it.
- **Only unfair starvation causes failure** → justify and validate an enforceable fairness assumption.
- **Out of memory/time** → select a sound abstraction/symbolic/POR route based on the property class.
- **Insufficient information** → return that the claim cannot yet be established; list the missing model semantics, requirement, or scheduler assumptions.

---

## Chapter Index

| # | Title | Operational focus |
|---|---|---|
| [ch01](chapters/ch01-system-verification.md) | System Verification | verification loop, validation, result diagnosis, limits |
| [ch02](chapters/ch02-modelling-concurrent-systems.md) | Modelling Concurrent Systems | TS, program graphs, interleaving, channels, atomicity |
| [ch03](chapters/ch03-linear-time-properties.md) | Linear-Time Properties | reachability, safety/liveness, fairness |
| [ch04](chapters/ch04-regular-properties.md) | Regular Properties | NFA/NBA/GNBA, products, nested DFS |
| [ch05](chapters/ch05-linear-temporal-logic.md) | Linear Temporal Logic | LTL specification and automata-based checking |
| [ch06](chapters/ch06-computation-tree-logic.md) | Computation Tree Logic | CTL/CTL*, fixed points, fairness, ROBDDs |
| [ch07](chapters/ch07-equivalences-and-abstraction.md) | Equivalences and Abstraction | bisimulation, simulation, stutter relations |
| [ch08](chapters/ch08-partial-order-reduction.md) | Partial Order Reduction | independence, ample sets, dynamic/static POR |
| [ch09](chapters/ch09-timed-automata.md) | Timed Automata | clocks, TCTL, regions, timelock/zeno behavior |
| [ch10](chapters/ch10-probabilistic-systems.md) | Probabilistic Systems | MCs, PCTL, costs, MDPs, schedulers, MECs |
| [ch11](chapters/ch11-preliminaries.md) | Preliminaries | logic, languages, graphs, complexity |

## Topic Index

- **Abstraction** → ch07; **accepting cycle** → ch04, ch05
- **Atomicity** → ch02; **bad prefix** → ch03, ch04
- **Bisimulation** → ch07; **probabilistic bisimulation** → ch10
- **Büchi automata / GNBA** → ch04, ch05; **Rabin automata** → ch10
- **Channels / handshaking / interleaving** → ch02
- **Counterexamples / witnesses** → ch01, ch04, ch06
- **CTL / CTL\*** → ch06; **LTL** → ch05
- **Deadlock / invariant / reachability** → ch03
- **Fairness** → ch03, ch05, ch06, ch10
- **Markov chains / PCTL** → ch10; **MDPs / schedulers / MECs** → ch10
- **Nested DFS** → ch04, ch05
- **Partial-order reduction / ample sets** → ch08
- **ROBDD / symbolic model checking** → ch06
- **Safety / liveness** → ch03
- **Simulation / refinement** → ch07
- **State-space explosion** → ch01, ch02, ch06–ch09
- **Stutter equivalence** → ch07, ch08
- **Timed automata / TCTL / regions / zenoness** → ch09
- **Trace equivalence** → ch03, ch07
- **Value iteration / linear programming** → ch10

## Supporting Files

- [glossary.md](glossary.md) — compact terminology with chapter pointers
- [patterns.md](patterns.md) — reusable verification/model-checking procedures
- [cheatsheet.md](cheatsheet.md) — decision rules, preservation boundaries, and failure smells
- `provenance.json` — source-to-capability traceability and synthesis labels
- `evals.json` — representative trigger, routing, recovery, and negative cases

---

## Scope & Limits

This skill operationalizes the content of *Principles of Model Checking* and the provided selected-solution supplement. It covers finite-state qualitative model checking, timed automata, finite Markov chains and MDPs, and the book's reduction/abstraction methods. It does not establish correctness of an implementation absent a faithful model, does not cover unstated requirements, and gives no general decision procedure for arbitrary infinite-state or parameterized systems. Testing, simulation, theorem proving, and implementation review remain complementary techniques.

## SELF_CHECK

Before finalizing an answer or verification plan, confirm:

- The user's actual requirement has been separated from the model encoding.
- The model semantics, atomicity, observables, and nondeterministic choices are explicit.
- The chosen logic can express the requirement with the intended quantifier scope.
- Any fairness assumption is justified and realizable.
- Any abstraction/reduction preserves the exact property fragment being checked.
- Counterexamples are projected back to meaningful system behavior and classified before repair.
- A model change triggers re-verification of results that depended on the old model.
- Numerical probability claims have an error/tolerance story when thresholds are close.
- If evidence is insufficient, the answer states what is missing instead of manufacturing a proof.
