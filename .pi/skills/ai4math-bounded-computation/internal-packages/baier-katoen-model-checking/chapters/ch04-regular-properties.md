# Chapter 4: Regular Properties

## Core Idea

Automata turn behavioral properties into executable monitors. Regular safety checking becomes reachability in a product with a finite-word automaton; ω-regular checking becomes search for a reachable accepting cycle in a product with a Büchi-style automaton.

## Frameworks Introduced

### Finite-word automata for bad prefixes
For a regular safety property, build an NFA/DFA that accepts its finite bad prefixes.

**When to use**: a safety requirement depends on a finite history rather than only the current state.

**How**:
1. Choose the alphabet `2^AP` (or a propositionally represented equivalent).
2. Construct an automaton `A` whose accepted finite words are exactly the bad prefixes.
3. Form the product `TS ⊗ A` so the automaton reads the system's state labels.
4. Search the product for an accepting automaton state.
5. If found, project the product path onto the system component; its trace is a bad prefix.

This reduces a history-dependent safety check to ordinary reachability/invariant checking.

### Automata on infinite words
A nondeterministic Büchi automaton (NBA) accepts an infinite word when **some run** visits an accepting state infinitely often. The class of NBA-recognizable languages is exactly the class of ω-regular languages.

Related forms:
- **DBA**: deterministic Büchi automaton; strictly less expressive than NBA for infinite words.
- **GNBA**: generalized Büchi automaton with multiple accepting sets; every accepting run must visit each accepting set infinitely often. GNBAs and NBAs have the same expressive power.

**Decision rule**: use NBA/GNBA as the standard nondeterministic monitor. Do not assume every ω-regular language has an equivalent deterministic Büchi automaton.

### Product for ω-regular model checking
**When to use**: unwanted behavior is represented by an NBA `A`.

The product combines system state and automaton state. A violating system behavior exists exactly when the product has a reachable infinite path that satisfies the Büchi acceptance condition.

For a single Büchi accepting set, this becomes:

> Is there a reachable cycle that contains an accepting product state?

This is the basis of the LTL checking pipeline in Ch 5.

### Persistence reduction
A Büchi emptiness problem can be phrased as failure of a persistence property: after some point, the product would need to avoid accepting states to prove there is no accepting run. Searching for a reachable cycle containing an accepting state refutes that persistence condition.

### Nested depth-first search (NDFS)
**When to use**: on-the-fly Büchi emptiness/model checking with linear worst-case graph complexity.

Conceptual procedure:
1. Run an **outer DFS** from the product's initial states.
2. When the outer search finishes exploring an accepting state, start an **inner DFS** from that state over the already relevant reachable graph.
3. If the inner search can return to the accepting seed (or detect the corresponding back edge under the algorithm's formulation), an accepting cycle exists.
4. Reconstruct a lasso: a finite prefix from an initial product state to the accepting cycle plus the cycle itself.
5. If every accepting seed is discharged without a cycle, the Büchi language of the product is empty.

The two searches share marking information carefully; incorrect sharing can make the algorithm miss cycles.

## Key Concepts

- **Regular language**: finite-word language recognized by a finite automaton.
- **NFA/DFA**: nondeterministic/deterministic finite automaton; same finite-word expressive power, although determinization can cause exponential state growth.
- **ω-word**: infinite sequence over an alphabet.
- **ω-regular language/property**: infinite-word language recognized by an NBA and equivalently describable by ω-regular expressions/other standard ω-automata.
- **Büchi acceptance**: an accepting state occurs infinitely often along a run.
- **Generalized Büchi acceptance**: every accepting set is visited infinitely often.
- **Product state**: pair of a system state and automaton-monitor state.
- **Accepting cycle**: reachable cycle witnessing an infinite accepting run.
- **Lasso counterexample**: finite prefix followed by a repeating cycle; sufficient to represent a violating infinite behavior in a finite product graph.
- **Persistence**: an LT property of the form “eventually always Φ.”
- **On-the-fly checking**: generate product states only as exploration requires them instead of materializing the whole product first.

## Mental Models

- **Turn temporal memory into automaton state**: if the property needs to remember history, add that memory in the monitor rather than bloating the system model.
- **Finite bad history → accepting finite state; infinite bad recurrence → accepting cycle.** This single distinction routes most of the chapter.
- **Think of a product as synchronized observation**: every system step updates both the system configuration and the property monitor.
- **Search recurrence structurally**: a liveness violation in a finite graph eventually repeats states, so strongly connected/cycle reasoning replaces reasoning over literally infinite paths.

## Anti-patterns

- **Using a finite automaton for a non-regular bad-prefix language**: no finite monitor can remember unbounded information such as unrestricted counting relationships.
- **Assuming NFA determinization is free**: subset construction can create exponentially many DFA states.
- **Using a DBA for every ω-regular property**: deterministic Büchi automata do not capture all ω-regular languages.
- **Forgetting the first observed label when initializing a product**: an off-by-one in monitor input can create false results.
- **Searching only for an accepting state in Büchi checking**: acceptance requires infinite recurrence, so reachability alone is insufficient.
- **Returning a product trace without projection**: users need the corresponding system execution and labels, not monitor internals alone.
- **Treating any cycle as a counterexample**: the cycle must satisfy the relevant acceptance condition.

## Reference Tables

### Automaton choice

| Property representation | Automaton | Acceptance | Verification reduction |
|---|---|---|---|
| regular safety bad prefixes | NFA/DFA on finite words | final state reached at end of prefix | reachability in `TS ⊗ A` |
| ω-regular unwanted behavior | NBA | accepting state infinitely often | reachable accepting cycle |
| generalized Büchi property | GNBA | each accepting set infinitely often | convert to NBA or track acceptance sets |

### Product-validation checklist

1. Alphabet matches the system's observable labels.
2. Initial product states consume the initial system label according to the chosen product definition.
3. Every product edge corresponds to a legal system transition and a legal monitor update.
4. Accepting product states are determined only by the automaton component.
5. Counterexample projection preserves the system-state sequence/trace.

## Worked Example: regular safety monitor

Requirement: after proposition `a` becomes true, proposition `b` must continue to hold until `c` occurs.

A compact bad-prefix monitor needs states representing roughly:
- no active obligation;
- obligation active (`a` has occurred and `c` has not released it);
- violation seen (`b` failed while obligation active).

Checking procedure:
1. label each system state with truth values of `a`, `b`, `c`;
2. update the monitor on each label;
3. search the product for the violation monitor state;
4. if reachable, return the projected prefix ending at the first irreversible violation.

The monitor captures history that is not expressible as a single current-state invariant.

## Worked Example: nested DFS result shape

Suppose an NBA for unwanted behavior is composed with a transition system. The outer DFS reaches product state `(s4, q_accept)` through a finite prefix. The inner DFS started there discovers a path back to `(s4, q_accept)`.

Return:

`initial ... (s4,q_accept) ... (s4,q_accept) ...`

and project to:

`initial-system-state ... s4 ... s4 ...`

The first segment is the prefix; the second is a repeatable cycle. The monitor's accepting state on the cycle ensures an infinite product run violating the original property.

If the inner DFS reaches cycles that never include the required accepting condition, they do not witness Büchi acceptance.

## Failure Recovery

### Product explodes
- Generate on-the-fly.
- Simplify the property automaton.
- Apply sound state-space reduction to the system first.
- For LTL without next, partial-order reduction in Ch 8 may preserve the property.

### NDFS reports a suspicious counterexample
Validate three layers separately:
1. projected system prefix/cycle is executable;
2. monitor run follows its transition relation on the trace;
3. acceptance condition is actually met infinitely often by the repeated cycle.

### Safety automaton hard to construct
First write minimal bad-prefix examples and non-bad prefixes. If no finite memory appears sufficient, reassess regularity or move to a richer temporal logic.

## Key Takeaways

1. Regular safety = finite bad-prefix automaton + product reachability.
2. NBA-recognizable languages are exactly ω-regular languages.
3. DBA is weaker than NBA; GNBA and NBA are equally expressive.
4. ω-regular/LTL checking reduces to reachable accepting-cycle detection.
5. NDFS supports on-the-fly linear-time exploration of the product graph.
6. A useful infinite counterexample is a finite lasso, then projected back to system behavior.
7. Validate property automata independently before trusting the product result.

## Connects To

- **Ch 3**: supplies safety, bad-prefix, persistence, and fairness semantics.
- **Ch 5**: compiles LTL into GNBA/NBA, then uses exactly this product/cycle machinery.
- **Ch 10**: probabilistic ω-regular checking uses deterministic ω-automata and recurrent components rather than plain NBA nondeterminism.
