# Chapter 7: Recursive Proving & Re-planning

## Core Idea
Recursive work is an escalation step for plans that survived meaningful direct screening. Each plan gets a focused agent with shared failure context; if all routes fail, their common obstructions become structured input to a new planning round.

## Frameworks Introduced

- **One agent per screened plan**
  - **When to use**: all current plans have been directly attempted and none solves the target.
  - **How**: assign each plan to a sub-agent together with the full theorem, its own stuck points, and important stuck points from the other plans.
- **Continuity-preserving recursion**
  - **When to use**: a plan-specific agent discovers new evidence.
  - **How**: permit local refinement or extension while keeping the assigned plan as the starting architecture; recursively spawn help only when it advances that route.
- **Shared-state recursive work**
  - **When to use**: every recursive round.
  - **How**: all agents use the same problem identifier and write progress/failures to shared memory.
- **Key-failure synthesis**
  - **When to use**: every plan fails in the recursive round or a family of routes repeatedly stalls.
  - **How**: compare plan-local stuck points, recurring counterexamples, broken decompositions, and search gaps; write a common-failure summary and use it to constrain the next set of plans.

## Key Concepts

- **Recursive round** — parallel plan-focused proof work after direct screening.
- **Shared stuck points** — cross-plan constraints each sub-agent should know.
- **Successful plan** — route from which a complete proof can be assembled.
- **Key failures summary** — cross-plan diagnosis stored in `failed_paths`.
- **Re-planning loop** — failure synthesis followed by materially new decomposition plans.

## Mental Models

- Spend parallelism on **diverse, pre-screened routes**, not speculative duplicates.
- Give every recursive agent **negative knowledge** from sibling plans so the group does not relearn the same obstruction.
- Treat recursive failure as a **dataset for model selection**: common failure modes say which proof architecture to avoid next.
- Open-problem status is a **difficulty signal**, not proof of impossibility; keep exploring while maintaining a strict success standard.

## Anti-patterns

- **Launching recursive agents before direct screening**.
- **Letting each agent restart from zero** and ignore the assigned plan.
- **Hiding one plan's decisive obstruction from the others**.
- **Repeating the same failed plan family after recursive failure** without a synthesis step.
- **Declaring success because a hard problem looks open**.

## Reference Table

| Recursive outcome | Action |
|---|---|
| one plan succeeds | assemble full proof from that route |
| several plans make partial progress | preserve all useful steps; compare compatibility |
| all plans fail | synthesize common failures |
| failure synthesis reveals missing background | targeted retrieval or new examples |
| synthesis reveals structural obstruction | design new decomposition family |

## Worked Example

Three plans all fail, but for different surface reasons. Plan A needs a missing compactness argument, Plan B's induction cannot control a boundary term, and Plan C's reduction recreates the same boundary term under another name. The synthesis records “uncontrolled boundary behavior” as the common obstruction. The next planning round should attack or bypass that obstruction explicitly instead of generating more reductions with the same hidden dependency.

## Key Takeaways

1. Recursive proving starts after direct screening.
2. Parallelize by plan, preserving each route's continuity.
3. Share stuck points across agents.
4. Persist all recursive outcomes under one problem identity.
5. Convert collective failure into constraints for the next planning round.
6. Keep attempting hard/open problems while withholding success until verification passes.

## Connects To

- **Ch 2**: recursive agents coordinate through shared memory.
- **Ch 6**: direct screening supplies plan-specific starting points.
- **Ch 9**: a successful recursive route still faces the same strict verifier.

## Source Provenance

Primary source files: `agents/generation/.agents/skills/recursive-proving/SKILL.md`, `agents/generation/.agents/skills/identify-key-failures/SKILL.md`, `agents/generation/.codex/agents/subgoal-prover.toml`, `agents/generation/.codex/config.toml`, and `agents/generation/AGENTS.md`.
