# Chapter 5: Linear Temporal Logic

## Core Idea

LTL specifies properties of individual infinite traces using temporal operators, while system satisfaction quantifies over all traces. Model checking turns `TS |= φ` into an automata-emptiness problem for the product of the system with an automaton recognizing `not φ`.

## Frameworks Introduced

### LTL syntax and semantics
Use atomic propositions and Boolean connectives plus:

- `X φ` — next: `φ` holds at the next position;
- `φ U ψ` — until: `ψ` eventually holds, and `φ` holds before that point;
- `F φ` — eventually (derived from until);
- `G φ` — always (derived by duality);
- `φ W ψ` — weak until: `φ U ψ` or `G φ`;
- `φ R ψ` — release: dual of until.

An LTL formula is interpreted on a trace. A transition system satisfies it when **all relevant initial traces** satisfy it.

### Property-specification patterns
Use these shapes as starting points and instantiate with domain propositions:

| Intent | LTL pattern |
|---|---|
| invariant | `G p` |
| eventual goal | `F p` |
| response | `G(req -> F grant)` |
| persistence | `F G p` |
| recurrence | `G F p` |
| precedence/order | `not q U p` or a requirement-specific variant |
| mutual exclusion | `G not(crit1 and crit2)` |
| starvation freedom | `G(wait_i -> F crit_i)` |

Always validate a pattern on example traces; similar English sentences can require different quantifier scope or release/until structure.

### Equivalence and positive normal form
LTL equivalences let a formula be simplified or converted to a normal form that supports automata construction. The book develops weak-until and release forms so negation can be pushed inward to atomic propositions.

**Use when**:
- preparing a formula for a specific construction;
- proving two specifications equivalent;
- reducing the number of temporal subformulae before automata generation.

Key semantic warning: `U` requires the right operand eventually; `W` allows the left operand to remain forever. Confusing them converts a progress obligation into a safety-like permissive condition.

### Fairness in LTL
Fairness constraints can themselves be written as LTL and combined with the property semantics.

Typical forms:
- unconditional fairness: `G F Ψ`;
- strong fairness: `G F Φ -> G F Ψ`;
- weak fairness: `F G Φ -> G F Ψ`.

There is a general reduction from fair satisfaction to ordinary checking, but a naive implication construction can enlarge the translated automaton. For implementation, use fairness-aware automata/persistence techniques when available rather than blindly nesting a large fairness formula into every property.

### Automata-based LTL model checking
**When to use**: finite TS + LTL property.

Pipeline:
1. normalize/simplify `φ` as useful;
2. negate it to obtain `not φ`;
3. construct a GNBA whose states are consistent **elementary sets** of subformulae from the closure of `not φ`;
4. encode each `U` obligation in generalized Büchi acceptance so an indefinitely postponed until is rejected;
5. convert GNBA to NBA if needed;
6. construct the product `TS ⊗ A_notφ`;
7. run Büchi emptiness / nested DFS;
8. no accepting run → property holds; accepting lasso → project it to a violating system trace.

### LTL → GNBA construction intuition
The automaton state represents which subformulae are currently true. Transitions enforce temporal consistency:
- a next-formula determines what must hold in the successor state;
- an until-formula is either already fulfilled by its right operand or persists to the next state while the left operand holds;
- the acceptance set for each until-formula prevents an obligation from being postponed forever without fulfillment.

This construction is exponential in formula size in the worst case.

## Key Concepts

- **Words(φ)**: the set of infinite words satisfying LTL formula `φ`.
- **Closure of a formula**: finite set containing the formula's relevant subformulae and negations used to build automaton states.
- **Elementary set**: maximally consistent subset of the closure satisfying Boolean/temporal local consistency conditions.
- **Positive normal form (PNF)**: equivalent formula with negation restricted to atomic propositions, using suitable temporal duals.
- **Until obligation**: requirement that the right-hand operand eventually occur; acceptance conditions track that it is not deferred forever.
- **LTL model-checking complexity**: linear in the transition-system size and exponential in formula length for the standard automata-based algorithm; the decision problem is PSPACE-complete.
- **Satisfiability**: whether some infinite word satisfies a formula; checked via automaton nonemptiness.
- **Validity**: whether all infinite words satisfy a formula; reduce to unsatisfiability of its negation.
- **Expressiveness boundary**: LTL defines ω-regular properties but does not express every ω-regular language.

## Mental Models

- **Read LTL from the trace outward**: temporal operators move along one execution; the system-level universal trace quantification comes outside the formula.
- **Treat every `U` as a debt**: either pay it now (`ψ`) or carry it to the next position while `φ` holds. Büchi acceptance ensures debt cannot remain forever.
- **Write the violation first when easier**: for “nothing bad can happen,” the automaton is often simpler for the bad behavior, which is exactly what the product needs.
- **Use formula size as an algorithmic resource**: a small model with a large, nested formula can still be expensive because translation is exponential in the formula.
- **Avoid `X` unless exact next-step timing is semantically required**: next-free LTL is preserved by stuttering and supports important reductions in Ch 7–8.

## Anti-patterns

- **Using `F p` when the requirement is repeated service**: “eventually once” differs from `G F p`.
- **Using `G F p` when the requirement is eventual permanence**: recurrence differs from `F G p`.
- **Replacing strong until with weak until**: drops the guarantee that the goal ever occurs.
- **Treating a formula over one trace as an existential system claim**: ordinary LTL model checking checks all system traces.
- **Embedding unjustified fairness as an implication**: can hide starvation behavior and increase automaton size.
- **Writing formulas before fixing atomic propositions**: a proposition such as `request` must have an unambiguous state interpretation.
- **Overusing `X`**: makes specifications sensitive to stuttering/internal-step refinement.

## Reference Tables

### Temporal operators

| Operator | Fails when… | Typical diagnostic |
|---|---|---|
| `G p` | some finite position violates `p` | finite prefix |
| `F p` | `p` never occurs | infinite suffix/cycle avoiding `p` |
| `G F p` | eventually `p` stops occurring | suffix cycle without `p` |
| `F G p` | violations of `p` recur forever | cycle containing `not p` |
| `p U q` | `q` never occurs, or `p` fails before first `q` | finite prefix or infinite deferral |
| `p W q` | `p` fails before a `q` and `q` has not released it | finite prefix |

### LTL checking route

`requirement -> AP -> LTL φ -> not φ -> GNBA/NBA -> product -> accepting-cycle search -> projected counterexample`

## Worked Example: request–grant with starvation

Requirement: every waiting request must eventually enter its critical section.

1. Atomic propositions: `wait1`, `crit1`.
2. Formula: `G(wait1 -> F crit1)`.
3. Negation describes a trace where process 1 reaches a waiting condition and, from some point, never reaches `crit1`.
4. Translate the negation to a Büchi monitor.
5. Product search finds a lasso when the system can cycle forever while `wait1` remains relevant and `crit1` never occurs.
6. Inspect the cycle:
   - if process 1 is continuously enabled but never scheduled, a justified weak fairness constraint may remove the path;
   - if it is enabled only intermittently due contention, strong fairness may be relevant;
   - if it loses eligibility because of protocol state, fairness does not automatically repair the design.

The selected solutions repeatedly use this style of counterexample to distinguish a genuine protocol liveness failure from an unfair scheduling artifact.

## Worked Example: checking a response property automata-first

Let `φ = G(a -> F b)`.

A violation means: there is some position with `a`, after which `b` never appears. The negation can be understood operationally as a monitor that:
1. waits nondeterministically for a position where `a` starts a pending obligation;
2. enters a state requiring `not b` forever;
3. accepts if that “no b” state is visited forever.

The product with the system therefore needs only to find a reachable cycle compatible with `not b` after a triggering `a`. This mental construction is often easier to debug than an opaque large automaton generated from syntax.

## Failure Recovery

### Formula produces surprising counterexample
- Re-evaluate each atomic proposition on the trace.
- Manually check the formula at the trigger position and on the cycle.
- Compare the English requirement with `F G` versus `G F`, strong versus weak until, and scope of implication.

### Automaton too large
- simplify equivalent subformulae;
- minimize the AP vocabulary;
- generate the product on-the-fly;
- use POR for next-free LTL when independence conditions hold;
- use property-specific monitors when they are easier than the generic translation.

### Fairness dominates the formula
Move to a fairness-aware checking method and document the scheduling assumption separately from the functional property.

## Key Takeaways

1. LTL is trace-oriented; system satisfaction is universal over the model's traces.
2. Use `G`, `F`, `U`, `W`, and `R` with their distinct progress commitments.
3. Automata-based checking searches for an accepting run of an automaton for the negated property.
4. Until obligations explain the generalized Büchi acceptance construction.
5. LTL-to-automaton translation can be exponential; model size and formula size affect complexity differently.
6. Fairness is expressible in LTL but still needs an independent modeling justification.
7. Avoid next-step sensitivity when stutter-invariant semantics are sufficient.

## Connects To

- **Ch 3**: safety/liveness/fairness classification tells you what an LTL formula is trying to express.
- **Ch 4**: supplies Büchi automata, products, persistence, and nested DFS.
- **Ch 6**: contrasts linear-time semantics with CTL/CTL* branching-time semantics.
- **Ch 7–8**: next-free LTL is preserved by stuttering and standard POR conditions.
- **Ch 10**: probabilistic LTL/ω-regular analysis uses deterministic ω-automata with MC/MDP products.
