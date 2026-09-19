# Chapter 6: Decomposition & Direct Proving

## Core Idea
Once examples, counterexamples, retrieval, and prior failures constrain the problem, Rethlas creates multiple genuinely different proof plans and screens each plan end-to-end with direct reasoning before escalating.

## Frameworks Introduced

- **Materially different decomposition plans**
  - **When to use**: enough information has accumulated to break the theorem into meaningful routes.
  - **How**: create several plans with distinct main mechanisms; list ordered subgoals, motivation, evidence used, and earlier failures/counterexamples each plan avoids.
- **Whole-plan direct screening**
  - **When to use**: immediately after a plan is proposed.
  - **How**: try every subgoal in order; use relevant search results/examples/counterexamples; carry the whole plan as far as possible before switching to failure diagnosis.
- **Proof migration audit**
  - **When to use**: a searched theorem has a similar proof.
  - **How**: adapt its construction/reduction explicitly; record what transfers and the exact point where migration fails.
- **Blocked-subgoal falsification**
  - **When to use**: any direct subgoal stalls.
  - **How**: test the subgoal by counterexample before assuming more proof effort is the right response.

## Key Concepts

- **Plan summary** — the mechanism tying subgoals together.
- **Ordered subgoals** — dependencies that must be resolved for the route to succeed.
- **Screening status** — proposed, screening, screened, selected, failed, or solved.
- **Direct attempt status** — solved, partial, or stuck.
- **Migration failure** — concrete reason a known proof idea does not transfer.
- **Plan-local stuck point** — decisive obstruction discovered during the first full attempt.

## Mental Models

- Think of decomposition plans as **competing proof architectures**.
- Use direct screening as a **cheap feasibility test** before parallel recursive investment.
- Treat proof migration like **porting code across environments**: hidden assumptions are compatibility constraints.
- Diagnose the entire plan only after it has received a real attempt.

## Anti-patterns

- **Generating several paraphrases of one plan**.
- **Abandoning a plan after the first hard subgoal** without learning whether later structure could help.
- **Citing a similar theorem as a black box** when the useful part is its proof method.
- **Reporting “does not work” without a missing hypothesis, broken construction, counterexample, or failed step**.

## Reference Table

| Direct-screen outcome | Next route |
|---|---|
| all subgoals solved | assemble full proof draft |
| one subgoal blocked and fragile | counterexample test |
| partial migration from known proof | record transfer + failure point; revise route |
| plan screened, unsolved | persist stuck points; compare with other plans |
| all plans screened, none solved | recursive proving |

## Worked Example

Plan A reduces the theorem to three lemmas. Lemma 1 follows from definitions; Lemma 2 can adapt a retrieved construction; Lemma 3 fails because the source construction uses a finiteness hypothesis absent here. Record Lemma 1 and 2 as progress, the finiteness dependency as a migration failure, test whether Lemma 3 is even true, then mark Plan A screened rather than silently discarding it.

## Key Takeaways

1. Build plans from accumulated evidence, not from a fixed preselected order.
2. Ensure plans differ by mechanism.
3. Attempt every subgoal before plan-level diagnosis.
4. Stress-test blocked subgoals.
5. Record migration failures precisely enough to inform later plans.
6. Escalate only after direct screening has earned the cost.

## Connects To

- **Ch 4**: blocked or fragile subgoals are falsification targets.
- **Ch 5**: searched proof methods feed direct attempts.
- **Ch 7**: screened failures define recursive-agent starting states.

## Source Provenance

Primary source files: `agents/generation/.agents/skills/propose-subgoal-decomposition-plans/SKILL.md`, `agents/generation/.agents/skills/direct-proving/SKILL.md`, and `agents/generation/AGENTS.md`.
