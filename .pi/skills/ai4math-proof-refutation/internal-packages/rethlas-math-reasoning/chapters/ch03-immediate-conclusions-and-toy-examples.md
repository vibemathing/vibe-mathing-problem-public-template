# Chapter 3: Immediate Conclusions & Toy Examples

## Core Idea
Before expensive proof search, harvest cheap logical consequences and inspect simple valid cases. This exposes notation, necessary conditions, assumption roles, likely invariants, and fragile claims early.

## Frameworks Introduced

- **Immediate-conclusion pass**
  - **When to use**: at a new problem, branch, or subgoal.
  - **How**: normalize notation; restate equivalent forms; derive definition-level, algebraic, and logical consequences; split necessary conditions from candidate sufficient conditions; mark confidence and fragility.
- **Fragility annotation**
  - **When to use**: for every derived consequence.
  - **How**: decide whether the claim is likely to fail in edge cases. If fragile, record why and route it to counterexample construction.
- **Toy-example analysis**
  - **When to use**: when reasoning stalls or the mechanism behind the theorem is unclear.
  - **How**: choose low degree, small dimension, special form, or canonical objects; verify all assumptions and the conclusion; locate where each assumption is used; record the observed pattern.

## Key Concepts

- **Normalization** — rewriting the target into equivalent forms that make structure visible.
- **Necessary condition** — must hold if the target conclusion holds.
- **Candidate sufficient condition** — a stronger condition that may make a proof route easier.
- **Fragile conclusion** — plausible direct inference that deserves falsification pressure.
- **Toy example** — concrete small case satisfying both assumptions and conclusion.
- **Assumption tracing** — identifying the exact mechanism through which each hypothesis matters.

## Mental Models

- Treat immediate conclusions as **low-cost probes** that shape later search.
- Treat toy examples as **mechanism microscopes**: the goal is to see why the conclusion works, not merely to confirm another case.
- Treat fragile consequences as **queued falsification tasks**.

## Anti-patterns

- **Mistaking a clean reformulation for progress sufficient to prove the theorem**.
- **Keeping toy cases that violate an assumption**: they cannot diagnose the intended mechanism.
- **Recording only the example outcome**: save where assumptions take effect and what proof pattern it suggests.
- **Letting confidence replace justification type**: record the reason a consequence follows.

## Reference Table

| Situation | Cheap move | Evidence produced |
|---|---|---|
| Fresh theorem | normalize + direct consequences | immediate conclusions |
| Unclear hypothesis role | toy example | assumption-use map |
| Suspicious deduction | fragility mark | counterexample follow-up |
| Stuck but no clear falsifier | canonical/small cases | patterns and invariants |

## Worked Example

For the bundled claim that every group of prime order is cyclic, a cheap pass notes that any nonidentity element has order dividing the prime group order. A toy example such as a small prime-order cyclic group shows the intended mechanism and focuses the proof on the order of a nonidentity element. The example guides the route; it does not substitute for the general argument.

## Key Takeaways

1. Begin new proof states with cheap consequences.
2. Annotate fragility explicitly.
3. Verify toy examples against every hypothesis and the conclusion.
4. Extract mechanisms and invariants from examples.
5. Route suspicious claims into falsification before building plans around them.

## Connects To

- **Ch 4**: fragile claims become counterexample targets.
- **Ch 6**: plans should use the constraints discovered here.

## Source Provenance

Primary source files: `agents/generation/.agents/skills/obtain-immediate-conclusions/SKILL.md`, `agents/generation/.agents/skills/construct-toy-examples/SKILL.md`, and the example problem files under `agents/generation/data/`.
