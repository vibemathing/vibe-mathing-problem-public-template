# Patterns

## Verification Loop
**When to use**: every new model-checking task.

**How**: validate system scope → build model → sanity-simulate → formalize property → run checker → classify result as satisfied, model/design/property error, or capacity failure → revise the correct artifact → reverify affected results.

**Trade-offs**: front-loads modeling work but prevents “proofs” about the wrong model/property.

## Reachability / Invariant Search
**When to use**: deadlock, forbidden state, local state predicate.

**How**: DFS/BFS reachable states; test predicate; keep predecessor pointers; BFS when shortest counterexample is preferred.

**Trade-offs**: explicit exploration is simple but can exhaust memory.

## Regular Safety Monitor
**When to use**: safety violation has a regular finite bad-prefix language.

**How**: build NFA/DFA for bad prefixes → product with TS → reachability of accepting monitor state → project path.

**Trade-offs**: monitor can add states; nonregular histories need another formalism.

## Büchi Product + NDFS
**When to use**: ω-regular or LTL violation search.

**How**: automaton for unwanted behavior → product → outer DFS → inner DFS from accepting states → accepting cycle gives lasso counterexample.

**Trade-offs**: formula/automaton translation may be exponential.

## LTL Model Checking
**When to use**: trace-oriented temporal requirements.

**How**: define AP → write/simplify `φ` → translate `not φ` to GNBA/NBA → product → accepting-cycle search → validate projected trace.

**Trade-offs**: PSPACE-complete; avoid unnecessary `X` to retain stutter-based reductions.

## CTL Fixed-Point Checking
**When to use**: branching-time requirements.

**How**: compute `Sat` sets bottom-up; `EX` via predecessor; `EU` by least fixed point; `EG` by greatest fixed point; derive universal forms by duality; initial states must satisfy formula.

**Trade-offs**: explicit graph can dominate memory; CTL itself checks efficiently on a finite graph.

## Fairness Validation
**When to use**: liveness fails due suspected scheduler starvation.

**How**: inspect enabledness pattern → choose unconditional/strong/weak fairness only if implementation supports it → check realizability → rerun fair semantics.

**Trade-offs**: justified fairness removes unrealistic paths; unjustified fairness can hide defects.

## ROBDD Symbolic Checking
**When to use**: large Boolean state spaces with regular transition structure.

**How**: encode current/next variables and transition function → BDD state sets → symbolic predecessor/image → fixed points → tune variable order.

**Trade-offs**: dramatic compression is possible; poor ordering can cause BDD explosion.

## Bisimulation Quotient
**When to use**: merge behaviorally indistinguishable states while preserving branching properties.

**How**: partition by labels → refine on transition behavior until stable → quotient classes → check property on quotient.

**Trade-offs**: strong preservation but may reduce less than weaker abstractions.

## Simulation Over-Approximation
**When to use**: one-way refinement/universal proof.

**How**: show abstraction `A` simulates implementation `I` (every `I` step matched by `A`) → prove universal property on `A` → transfer to `I`.

**Trade-offs**: abstract counterexamples can be spurious; direction matters.

## Ample-Set POR
**When to use**: state explosion is dominated by independent interleavings.

**How**: choose `ample(s)`; enforce A1 nonempty, A2 dependency, A3 invisibility, A4 cycle proviso; add A5 singleton for next-free branching-time preservation.

**Trade-offs**: conservative dependence reduces savings; unsound independence invalidates results.

## Timed Region Checking
**When to use**: dense-time deadlines/interval requirements.

**How**: timed automaton → validate timelock/zeno assumptions → eliminate timing parameters with fresh clocks → build region TS → CTL-style TCTL checking.

**Trade-offs**: finite but exponential region count; TCTL checking is PSPACE-complete.

## MC Reachability Equations
**When to use**: fixed probabilistic model and reachability/constrained reachability.

**How**: compute probability-0/1 states → equations for remaining states → solve/iterate → check residuals.

**Trade-offs**: numerical tolerance matters near thresholds.

## MDP Extreme Reachability
**When to use**: probabilities plus unresolved nondeterminism.

**How**: Bellman max/min equations → value iteration or LP → synthesize scheduler; for max ties, enforce progress in the optimal-action graph.

**Trade-offs**: step-bounded objectives may need finite memory; numeric convergence needs validation.

## Recurrent-Component Analysis
**When to use**: persistence, recurrence, LTL/ω-regular probability.

**How**: MC → accepting BSCCs; MDP → accepting end components/MECs; reduce long-run probability to reachability of the success components. Use a DRA for general ω-regular properties.

**Trade-offs**: component acceptance is exact, but deterministic automata can be expensive.
