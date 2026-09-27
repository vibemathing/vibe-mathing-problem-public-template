# Chapter 7: Equivalences and Abstraction

## Core Idea

State-space reduction is sound only relative to an observation/preservation criterion. This chapter supplies a hierarchy of relations—bisimulation, simulation, trace equivalence, and stutter variants—and shows which temporal-logic properties survive quotienting or one-way abstraction.

## Frameworks Introduced

### Bisimulation
A bisimulation relates states with the same observable labels such that each transition of either state can be matched by a transition of the other into related states.

**When to use**:
- behavioral equivalence of two transition systems;
- quotienting a model while preserving full branching structure;
- a strong default when later property needs are broad or uncertain.

**How**:
1. partition states by observable labels;
2. repeatedly refine a block when states inside it have different transition behavior toward current blocks;
3. stop when every block is stable;
4. use blocks as quotient states and lift transitions between blocks.

For finite transition systems without terminal states, bisimulation equivalence coincides with equivalence with respect to CTL* (and CTL) over the observed propositions.

### Action-based bisimulation
When transition labels are observable, match actions rather than only state labels. The book relates action-based and state-based formulations through a transformation that inserts action information into states.

**Use when**: protocol/API behavior distinguishes *which action* occurred, not only the resulting state propositions.

### Partition refinement
Naive pairwise equivalence checking is avoidable. A quotient can be computed by refining an initial partition (usually grouped by labels) until every block is stable with respect to predecessor/transition behavior.

**Operational principle**: start with the coarsest partition allowed by observation, then split only when a transition mismatch proves states distinguishable. This computes the largest bisimulation consistent with the labels.

### Simulation preorder
Simulation is one-way matching. If state `B` simulates state `A`, each step of `A` can be matched by `B`, but `B` may have additional behavior.

**When to use**:
- refinement/implementation ordering;
- proving universal properties via a more behaviorally permissive abstraction;
- a coarser relation than bisimulation when mutual matching is unnecessary.

**Preservation direction**: if `B` simulates `A`, then universal CTL*/CTL properties that hold in `B` also hold in `A` (under the chapter's observation/semantic assumptions). With no terminal states, simulation also implies trace inclusion from `A` into `B`, so universal linear-time properties proven on `B` transfer to `A`.

Do not reverse this implication.

### Relation hierarchy
The chapter compares:
- bisimulation equivalence;
- simulation equivalence (mutual simulation, not necessarily one shared bisimulation);
- trace equivalence.

Bisimulation is finer than simulation equivalence, which is generally finer than trace equivalence under the relevant finite/no-terminal assumptions. Simulation order and trace order are not interchangeable in full generality, especially when terminal-state behavior matters.

### Stutter trace equivalence
Two traces are stutter-equivalent when finite repetitions of identical observations may be compressed/expanded without changing the sequence of observation changes.

**Preservation**: stutter trace equivalence preserves LTL **without the next operator `X`**.

**Use when**: internal implementation steps only repeat the current observable label and the property does not care about exact step counts.

### Stutter bisimulation
Branching-time analogue of stutter equivalence: a step may be matched by a finite path fragment that remains within related observational classes before reaching the matching target class.

A **divergence-sensitive** variant distinguishes the ability to stutter forever. For finite transition systems without terminal states, divergence-sensitive stutter bisimulation coincides with equivalence for CTL*/CTL without `X`.

**Use when**: abstracting internal steps while retaining next-free branching properties.

### Normed bisimulation
The chapter refines stutter reasoning with a norm that ensures matching progress rather than permitting circular proof obligations. Operationally, a norm can certify that a stutter-matching process decreases toward a genuine matching transition.

**Use when**: proving stutter-bisimulation relations compositionally or algorithmically where unrestricted finite matching is awkward.

## Key Concepts

- **Equivalence relation**: reflexive, symmetric, transitive relation suitable for quotienting into classes.
- **Bisimulation quotient**: transition system whose states are equivalence classes of the largest/selected bisimulation.
- **Stable partition**: no block needs further split under the equivalence's transition criterion.
- **Simulation**: one-way transition matching with label agreement.
- **Simulation equivalence**: each state simulates the other; weaker than requiring one bisimulation relation.
- **Trace inclusion/equivalence**: observable linear behaviors included/equal.
- **Stuttering**: finite repetition of the same observable state label.
- **Divergence**: possibility of an infinite sequence of stuttering/internal steps.
- **Logical characterization**: a relation coincides with indistinguishability by a logic fragment under stated conditions.
- **Property-preserving abstraction**: reduced model whose relation to the original supports a theorem transferring the target property.

## Mental Models

- **Choose the weakest relation that still preserves the target logic.** Stronger relations reduce less; weaker relations demand narrower property classes.
- **Think in observations, not raw states**: the labeling/AP set determines which distinctions an equivalence must preserve.
- **Use simulation as an over-approximation proof discipline**: prove a universal property on a model with at least the original behaviors, then transfer it downward.
- **Treat next-step sensitivity as an abstraction tax**: `X` prevents collapsing stuttering steps that would otherwise be semantically invisible.
- **Separate linear and branching preservation**: equal traces do not imply equal branching structure.

## Anti-patterns

- **Quotienting by trace equivalence as if it were automatically compositional**: trace equivalence does not provide the same straightforward state quotient guarantees as bisimulation.
- **Reversing simulation preservation**: a universal property holding in the smaller/implementation model need not hold in a simulator with extra behaviors.
- **Ignoring labels when merging states**: distinguishable atomic propositions must remain distinguishable.
- **Using stutter equivalence for a property containing `X`**: adding/removing repeated states can change next-step truth.
- **Ignoring infinite stuttering**: ordinary stutter matching may identify states whose divergence behavior matters to next-free branching formulas.
- **Assuming terminal states are harmless**: several trace/simulation characterizations rely on no-terminal-state assumptions or explicit terminal handling.
- **Selecting an abstraction before selecting the property class**: preservation theorem comes first.

## Reference Table: relation vs. property class

| Relation/order | Main preservation use | Important condition/boundary |
|---|---|---|
| bisimulation | CTL*/CTL equivalence; broad branching preservation | finite/no-terminal for stated logical coincidence |
| simulation `B simulates A` | universal CTL*/CTL from `B` to `A`; trace inclusion under conditions | direction matters |
| trace equivalence | all LT properties | observes labels only |
| finite-trace equivalence | safety properties | finite behavior only |
| stutter trace equivalence | LTL without `X` | next-free |
| divergence-sensitive stutter bisimulation | CTL*/CTL without `X` | divergence-aware; chapter conditions |

### Reduction selection

1. **Need full branching equivalence?** Use bisimulation.
2. **Need one-way universal proof/refinement?** Consider simulation.
3. **Only linear-time properties matter?** Trace relation is semantically sufficient, though quotient construction may be harder/more expensive.
4. **Internal repeated observations dominate and formulas are next-free?** Use stutter relations.
5. **Divergence/livelock is observable to the property?** Use divergence-sensitive stutter bisimulation.

## Worked Example: why trace equivalence is too coarse for CTL

Two systems can generate the same set of traces while branching at different points. In one system, after observing `a`, a single state may still offer both a path to `b` and a path to `c`. In another system, the choice between the `b`-future and `c`-future may already have been committed by entering two different `a`-labeled states.

Their linear traces can match, so LTL cannot distinguish them. A CTL property of the form “whenever `a` holds, there exists a path eventually reaching `b` and there exists a path eventually reaching `c`” can distinguish the branching structures.

Operational lesson: if the requirement talks about alternative futures from the **same current state**, trace equivalence is too weak a preservation criterion.

## Worked Example: abstraction by bisimulation partition refinement

Suppose a finite TS has thousands of states but only a handful of observable labels.

1. Initial partition: group all states with identical `L(s)`.
2. Pick a block `B` and inspect transitions to current blocks.
3. If some states in `B` can reach block `C` while others cannot match that behavior, split `B`.
4. Repeat until no splitter refines any block.
5. Construct one quotient state per final block.
6. Run CTL/LTL checks on the quotient when the corresponding preservation theorem applies.

This gives a principled reduction: every split is justified by a distinguishable behavior, and every retained merge has survived all such tests.

## Worked Example: simulation as conservative proof

You have implementation model `I` and abstraction `A`. Suppose `A` simulates `I`: every `I` step can be matched in `A`, while `A` may contain extra behaviors introduced by abstraction.

If the universal property `G safe` (or a corresponding universal CTL* formula) holds on `A`, it also holds on `I`, because every behavior of `I` is represented by a behavior allowed in `A`.

If `A` violates the property, the abstract counterexample may be spurious: extra behavior introduced by abstraction can create a failure not realizable in `I`. Refine the abstraction before concluding a design defect.

## Failure Recovery

### Quotient changes a property result
Check:
1. relation actually holds after the latest model change;
2. AP/observability set includes every proposition in the property;
3. theorem covers the logic fragment (`X` is a frequent boundary);
4. terminal/divergence assumptions hold.

### Abstract model has a counterexample
Determine whether the trace/path concretizes to the original model. If not, refine the abstraction by splitting the states responsible for the spurious behavior.

### Simulation direction is unclear
Write one sentence: “Every step/behavior of ___ is matched by ___.” Universal-property transfer goes from the **simulator/over-approximation that satisfies the property** to the **simulated system**.

## Key Takeaways

1. Abstraction is sound only with an explicit relation and property-preservation theorem.
2. Bisimulation is the robust branching-time equivalence; compute it by partition refinement.
3. Simulation supports one-way conservative reasoning; its direction must be stated.
4. Trace equivalence captures linear-time behavior but loses branching information.
5. Stutter relations enable aggressive abstraction when exact next steps are unobservable.
6. Divergence sensitivity matters when infinite internal stuttering/livelock can change a branching property.
7. Property vocabulary (`AP`) is part of the abstraction boundary.

## Connects To

- **Ch 3**: trace/finite-trace equivalence and safety/LT preservation.
- **Ch 5–6**: logic fragments characterized by the relations in this chapter.
- **Ch 8**: ample-set reduction is justified via stutter trace/bisimulation relations.
- **Ch 9**: clock-region equivalence is proved as a bisimulation, enabling finite timed abstraction.
- **Ch 10**: probabilistic bisimulation adapts the same quotienting idea to probability mass over classes.
