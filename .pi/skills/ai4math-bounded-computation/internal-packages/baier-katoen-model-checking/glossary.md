# Glossary

**Acceptance condition** — condition an infinite automaton run must meet, such as visiting a Büchi accepting set infinitely often (Ch 4).

**Ample set** — selected subset of enabled actions explored by partial-order reduction at a state (Ch 8).

**Atomic proposition (AP)** — observable Boolean fact used to label states and write temporal properties (Ch 2).

**Bisimulation** — symmetric step-matching relation preserving state observations; supports branching-time quotienting (Ch 7).

**BSCC** — bottom strongly connected component: SCC with no outgoing graph edge; finite Markov chains almost surely settle in one (Ch 10).

**Büchi automaton (NBA)** — nondeterministic automaton on infinite words accepting when some run visits an accepting state infinitely often (Ch 4).

**Counterexample** — diagnostic behavior demonstrating property failure; may be a finite path, lasso, or branching structure depending on the logic (Ch 1, 4, 6).

**CTL** — branching-time temporal logic pairing path quantifiers with temporal operators (Ch 6).

**CTL\*** — branching-time logic subsuming CTL and LTL by allowing fuller nesting of state/path formulae (Ch 6).

**Deadlock** — reachable terminal state when system termination/progress cessation is undesired (Ch 3).

**DRA** — deterministic Rabin automaton, used for deterministic recognition of ω-regular properties in probabilistic products (Ch 10).

**End component** — strongly connected MDP region together with action choices that keep all probability mass inside; MEC means maximal end component (Ch 10).

**Execution** — initial maximal execution fragment of a transition system (Ch 2).

**Fairness** — restriction on admissible infinite behavior, e.g. unconditional, strong, or weak fairness (Ch 3).

**GNBA** — generalized Büchi automaton with multiple accepting sets that each must recur infinitely often (Ch 4–5).

**Invariant** — state predicate required to hold in every reachable state (Ch 3).

**Lasso** — finite prefix followed by a repeatable cycle, compactly representing an infinite behavior in a finite graph (Ch 4–5).

**Liveness property** — LT property for which every finite prefix still has some satisfying continuation (Ch 3).

**LTL** — linear temporal logic over traces, with operators such as next, until, always, and eventually (Ch 5).

**Markov chain (MC)** — state model with a fixed probability distribution over successors and no unresolved nondeterminism (Ch 10).

**Markov decision process (MDP)** — model combining nondeterministic action choice and probabilistic successor choice (Ch 10).

**Nested DFS (NDFS)** — two-level depth-first search used to detect reachable Büchi accepting cycles on the fly (Ch 4).

**Nondeterminism** — unresolved choice representing scheduling, environment behavior, underspecification, or competition; carries no probability by itself (Ch 2).

**PCTL** — probabilistic branching-time logic with probability-threshold temporal operators (Ch 10).

**Program graph** — guarded control-flow graph with actions/effects and variable valuations, unfolded into a transition system (Ch 2).

**Reachable state** — state ending some finite initial execution fragment (Ch 2).

**Region transition system** — finite quotient of a timed automaton induced by clock-region equivalence and relevant formula constants (Ch 9).

**ROBDD** — reduced ordered binary decision diagram; canonical Boolean-function representation for a fixed variable ordering (Ch 6).

**Safety property** — LT property where every violation has a finite bad prefix (Ch 3).

**Scheduler** — rule resolving nondeterministic MDP action choices, possibly using history or finite memory (Ch 10).

**Simulation** — one-way step-matching relation used for refinement and universal-property preservation in the correct direction (Ch 7).

**Stutter equivalence** — equivalence insensitive to finite repetition of identical observations; preserves next-free temporal fragments under the chapter's conditions (Ch 7).

**TCTL** — timed CTL with clock constraints and time-bounded temporal operators interpreted over time-divergent paths (Ch 9).

**Timed automaton** — finite-control model with real-valued clocks, guards, resets, and location invariants (Ch 9).

**Timelock** — timed state from which no time-divergent path can continue (Ch 9).

**Trace** — sequence of state-label sets observed along a path (Ch 3).

**Transition system (TS)** — tuple of states, actions, transitions, initial states, atomic propositions, and a labeling function (Ch 2).

**Value iteration** — iterative Bellman update for approximating extreme MDP reachability probabilities (Ch 10).

**Zeno path** — timed path with infinitely many discrete actions but bounded total elapsed time (Ch 9).
