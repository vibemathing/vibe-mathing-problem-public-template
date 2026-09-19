# Chapter 4: Counterexamples & Failure Memory

## Core Idea
Rethlas actively tries to break conjectures and intermediate claims. A refutation kills the affected route; a failed search merely leaves the claim unproved. Both outcomes are stored so future reasoning can use them.

## Frameworks Introduced

- **Assumptions-true / conclusion-false test**
  - **When to use**: a claim feels fragile, a direct proof is stuck, or a decomposition subgoal may be too strong.
  - **How**: list the assumptions that must remain true, identify the conclusion to violate, search standard obstructions/pathologies and stored examples, then classify the result as `refuted`, `not_refuted`, or `inconclusive`.
- **Branch-impact propagation**
  - **When to use**: a counterexample genuinely refutes a claim.
  - **How**: persist the counterexample, mark dependent lemmas/branches invalid, and add the dead route to `failed_paths`.
- **Useful non-refutation capture**
  - **When to use**: falsification search produces a concrete informative case that still satisfies the conclusion.
  - **How**: save it as a toy example with the assumptions it satisfies and the mechanism observed.

## Key Concepts

- **Refuted** — assumptions hold and claimed conclusion fails.
- **Not refuted** — no counterexample found in the attempted search; no proof follows from this status.
- **Inconclusive** — search space or assumptions remain insufficiently explored.
- **Counterexample reuse** — test future conjectures against stored falsifiers before investing in proof work.
- **Failed path** — a route with a concrete obstruction that future plans should remember.

## Mental Models

- Use counterexamples as a **proof-search unit test suite**.
- Treat a successful falsifier as a **hard branch prune**.
- Treat an unsuccessful falsifier search as **weak evidence only**.
- Let failed paths **shape the next hypothesis and plan**, not merely document history.

## Anti-patterns

- **Concluding truth from failure to find a counterexample**.
- **Testing a candidate that violates the original assumptions** and calling it a refutation.
- **Keeping a refutation local to one agent**: dependent branches can continue on a false claim.
- **Discarding informative non-refuting examples**: they may reveal the working mechanism.

## Reference Table

| Outcome | Meaning | Next action |
|---|---|---|
| `refuted` | claim false under its assumptions | kill impacted route; record failed path |
| `not_refuted` | attempted falsification found none | keep claim unproved; seek proof or stronger test |
| `inconclusive` | search coverage unclear | refine assumptions/search space |
| useful valid example | mechanism visible | store in toy examples |

## Worked Example

A direct plan proposes a lemma that needs an embedding to preserve a certain property. Before proving the lemma, construct a smallest plausible object satisfying the plan's assumptions. If the property fails after the embedding, the lemma is refuted, the plan is marked invalid, and the precise obstruction is written to `failed_paths`. The next planning round can demand a route that avoids that embedding.

## Key Takeaways

1. Falsify fragile claims before depending on them.
2. Preserve assumptions while trying to break the conclusion.
3. Distinguish refutation, no-refutation, and inconclusive search.
4. Propagate real refutations to every dependent branch.
5. Make failure knowledge queryable and reusable.

## Connects To

- **Ch 2**: counterexamples and failed paths live in persistent memory.
- **Ch 6**: blocked direct subgoals trigger this test.
- **Ch 7**: shared failures drive re-planning.

## Source Provenance

Primary source files: `agents/generation/.agents/skills/construct-counterexamples/SKILL.md`, `agents/generation/.agents/skills/direct-proving/SKILL.md`, and `agents/generation/.agents/skills/identify-key-failures/SKILL.md`.
