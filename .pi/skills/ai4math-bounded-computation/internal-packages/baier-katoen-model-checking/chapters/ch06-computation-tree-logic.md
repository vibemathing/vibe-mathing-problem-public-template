# Chapter 6: Computation Tree Logic

## Core Idea

CTL reasons about a **branching computation tree** from each state: temporal operators are paired with existential or universal path quantifiers. Its finite-state model-checking algorithm computes satisfaction sets bottom-up, using predecessor operations and least/greatest fixed points. The chapter extends this to fairness, evidence generation, symbolic ROBDDs, and CTL*.

## Frameworks Introduced

### CTL state/path semantics
CTL separates state formulae from path choices. Conventional notation:

- `EX Φ`: some successor satisfies `Φ`.
- `AX Φ`: every successor satisfies `Φ`.
- `E(Φ U Ψ)`: some path reaches `Ψ`, with `Φ` beforehand.
- `A(Φ U Ψ)`: every path reaches `Ψ`, with `Φ` beforehand.
- `EF Φ`, `AF Φ`: existential/universal eventuality.
- `EG Φ`, `AG Φ`: existential/universal always.

**When to use**: the requirement refers to branching alternatives such as “from every reachable state there exists a recovery path” or “every possible continuation eventually reaches a stable state.”

**Routing warning**: LTL and CTL are incomparable. A formula that looks syntactically similar after dropping/adding quantifiers can have different truth conditions.

### Bottom-up CTL model checking
For every state subformula `Ψ`, compute:

`Sat(Ψ) = { s in S | s |= Ψ }`.

**How**:
1. evaluate atomic propositions from `L(s)`;
2. combine Boolean operators using set complement/intersection;
3. compute existential next using predecessors;
4. compute existential until as a least fixed point;
5. compute existential always as a greatest fixed point;
6. derive universal operators via duality or direct algorithms;
7. the system satisfies `Φ` when all initial states are in `Sat(Φ)`.

For a finite TS, time is linear in formula length and graph size, conventionally `O(|Φ| * (|S| + |→|))` for the basic algorithm.

### Least fixed point: `E(Φ U Ψ)`
Start with `T = Sat(Ψ)`. Repeatedly add any state in `Sat(Φ)` that has a successor already in `T`. Stop when no state can be added.

This computes the **smallest** set satisfying:

`T = Sat(Ψ) ∪ (Sat(Φ) ∩ Pre_exists(T))`.

A predecessor map can simultaneously store a witness path to `Ψ`.

### Greatest fixed point: `EG Φ`
Start with `T = Sat(Φ)` and remove states that cannot remain in `T` through at least one successor (with appropriate treatment of terminal states under the chapter's path semantics). Iterate to stability.

Intuition: keep exactly the states from which some infinite path can stay inside `Φ` forever.

The same fixed-point viewpoint underlies weak-until variants and symbolic implementations.

### Fair CTL
Under fairness, path quantifiers range only over fair paths. The workflow is:
1. encode/check the fairness condition;
2. identify states from which fair paths exist;
3. adapt the recursive CTL computations so existential/universal operators consider only fair continuations;
4. generate fair witnesses/counterexamples where needed.

Fairness changes liveness/branching conclusions and must be realizable. It should remain an explicit model assumption, not hidden in the formula.

### Counterexamples and witnesses
CTL evidence can be richer than one trace:

- existential claims naturally have **witness paths**;
- a violated universal eventuality often has one infinite counterexample path;
- formulas combining universal branching and nested existential requirements can require a **tree-like counterexample/witness structure**.

Operational rule: return the smallest evidence structure that demonstrates the relevant quantifier obligations; do not promise a single trace for every CTL failure.

### Symbolic CTL model checking with ROBDDs
Represent sets of states and transition relations as Boolean switching functions and store them as **reduced ordered binary decision diagrams (ROBDDs)**.

**How**:
1. encode a state with Boolean variables `x` and a successor with primed/next variables `x'`;
2. encode the transition relation `R(x,x')` as a Boolean function;
3. encode `Sat(Ψ)` as a Boolean function over current-state variables;
4. compute symbolic predecessor/image using conjunction with `R` and existential quantification over next variables;
5. perform the same CTL fixed-point iterations, now on BDD-represented sets.

**Critical implementation variable**: the ROBDD variable order. Reduced OBDDs are canonical for a fixed order, but size can change dramatically with the order. Interleaving strongly related current/next variables is a useful starting heuristic for transition relations; measure rather than assume.

### CTL*
CTL* permits arbitrary mixing of state/path formulae and subsumes both CTL and LTL.

Model-checking route:
1. recursively identify maximal proper state subformulae inside a path formula;
2. compute their satisfaction sets and relabel states with fresh propositions;
3. reduce the remaining path formula to LTL-style checking;
4. continue until the outer state formula is evaluated.

The added expressiveness costs more: CTL* model checking is PSPACE-complete in the formula dimension.

## Key Concepts

- **Computation tree**: unfolding of all possible continuations from a state; CTL talks about this branching structure.
- **State formula**: evaluated at a state.
- **Path formula**: evaluated along a path; CTL restricts how path quantifiers and temporal operators combine.
- **Existential normal form (ENF)**: uses a small existential basis plus Boolean operators, allowing universal forms to be handled by duality.
- **Satisfaction set**: set of model states satisfying a subformula.
- **Predecessor operation**: core graph primitive used for `EX`, until, and fixed-point computations.
- **Least fixed point**: captures finite-progress reachability such as `EU`.
- **Greatest fixed point**: captures indefinite maintenance such as `EG`.
- **ROBDD**: canonical reduced representation of a Boolean function under a fixed variable order.
- **Symbolic state set**: set represented by a Boolean formula/BDD rather than enumerated state IDs.
- **Witness/counterexample**: evidence for existential truth or formula falsity; may be path- or graph/tree-shaped.
- **CTL***: branching-time logic that permits fuller nesting than CTL.

## Mental Models

- **Read CTL as “choose paths at every temporal step.”** Quantifier placement is semantics, not decoration.
- **Compute truth from the leaves upward**: every compound subformula becomes a set of states, so the model-checking problem is set algebra plus graph predecessors.
- **Until grows; always prunes**: least fixed points add states that can reach a goal, while greatest fixed points remove states that cannot remain in a condition.
- **Symbolic model checking changes representation, not semantics**: the same fixed-point equations run over Boolean functions rather than explicit sets.
- **Treat BDD ordering as a first-class algorithm parameter**: a poor order can erase the expected symbolic advantage.

## Anti-patterns

- **Using `EF goal` when the requirement says every execution eventually reaches `goal`**: `EF` proves possibility; `AF` states universal inevitability.
- **Assuming `AF(a or b)` means `AF a or AF b`**: branching semantics can make such distributive intuitions invalid.
- **Translating CTL to LTL by deleting path quantifiers**: the logics are not interchangeable.
- **Returning one trace for a structurally branching counterexample**: it may fail to witness all nested obligations.
- **Ignoring terminal-state assumptions**: path semantics and fixed-point algorithms must agree on how termination is handled.
- **Expecting ROBDD canonicality to imply small size**: canonicality is per order; a bad order can be huge.
- **Building the entire explicit state graph before switching to symbolic checking**: loses much of the reason to use a symbolic method.

## Reference Tables

### CTL operator routing

| Requirement | CTL shape | Computation idea |
|---|---|---|
| some next state has `p` | `EX p` | existential predecessor |
| all next states have `p` | `AX p` | dual/universal predecessor |
| some path eventually `p` | `EF p` | `E(true U p)` least fixed point |
| every path eventually `p` | `AF p` | dual of an existential avoidance condition |
| some path stays in `p` | `EG p` | greatest fixed point |
| all reachable path positions satisfy `p` | `AG p` | dual of `EF not p` |

### Evidence expectations

| Formula result | Typical evidence |
|---|---|
| `EF p` true | finite path to `p` |
| `EG p` true | lasso staying in `p` |
| `AG p` false | finite path to `not p` |
| `AF p` false | lasso that avoids `p` |
| nested branching formula | proof/counterexample graph may be required |

## Worked Example: `EU` by backward growth

Goal: compute `Sat(E(a U b))`.

1. Initialize `T = Sat(b)`.
2. Find predecessors of `T` that satisfy `a`; add them.
3. Repeat using predecessors of newly added states.
4. Stop at a fixed point.

A newly added state gets a pointer to a successor already in `T`. Following these pointers yields a witness path that remains in `a` until reaching `b`.

This same structure is useful when explaining why a state satisfies the formula: do not merely report membership; show the chain of predecessor additions.

## Worked Example: fairness changes a liveness result

The selected solutions model a mutual-exclusion protocol in NuSMV. Without scheduling fairness, a counterexample to eventual critical-section entry can consist of an infinite loop where the framework repeatedly schedules an unrelated process and leaves the requesting process idle. Adding a per-process fairness condition requiring each process to be scheduled infinitely often removes that computation, after which the progress property succeeds for the analyzed model.

Operational lesson:
1. inspect the loop in the counterexample;
2. identify whether enabled process steps are omitted only by scheduling;
3. add fairness only if the actual execution platform guarantees it;
4. rerun the model checker and retain the fairness assumption in the result provenance.

## Failure Recovery

### CTL formula is unexpectedly true/false
- Expand abbreviations (`AF`, `AG`, etc.) to the primitive semantics.
- Compute the satisfaction sets of immediate subformulae manually on a small model.
- Check quantifier scope: “all paths have some future” differs from “there exists one future shared by all paths.”

### Explicit checking runs out of memory
- Use ROBDD-based symbolic state sets if the transition relation has exploitable Boolean structure.
- Revisit variable order when BDD nodes explode.
- Apply bisimulation/stutter quotient or POR when their preservation boundaries fit the formula.

### Fair CTL has no meaningful paths
Check fairness realizability before reporting vacuous success.

## Key Takeaways

1. CTL is branching-time: quantifier placement determines which alternatives must or may exist.
2. Basic CTL model checking is a bottom-up satisfaction-set computation linear in graph size times formula size.
3. `EU` is naturally a least fixed point; `EG` is naturally a greatest fixed point.
4. Fairness restricts the path domain and must be justified separately.
5. CTL evidence may need branching structure, not one counterexample trace.
6. ROBDDs can compactly represent huge state sets, but variable ordering is decisive.
7. CTL* combines CTL/LTL expressiveness and can be checked by recursive relabeling plus LTL machinery.

## Connects To

- **Ch 3**: reachability, fairness, and path/trace foundations.
- **Ch 5**: LTL forms the path-formula engine used in CTL* checking.
- **Ch 7**: bisimulation and divergence-sensitive stutter bisimulation characterize important CTL*/CTL preservation classes.
- **Ch 8**: branching-time POR adds an extra ample-set constraint to preserve next-free CTL*/CTL.
- **Ch 9**: TCTL checking reduces to CTL checking over a finite region transition system.
