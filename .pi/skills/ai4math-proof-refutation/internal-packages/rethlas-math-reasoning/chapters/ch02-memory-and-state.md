# Chapter 2: Memory & State

## Core Idea
Rethlas externalizes proof-state memory into append-only structured channels so discoveries, failures, and branch decisions survive long runs and recursive agents can reuse them.

## Frameworks Introduced

- **Channelized reasoning memory**
  - **When to use**: immediately at the start of a proof run.
  - **How**: initialize a run directory, create one JSONL channel per artifact type, append structured records after each meaningful action, and record branch state when direction changes.
- **Smallest-relevant-channel retrieval**
  - **When to use**: before repeating reasoning or when an old counterexample/failure may answer the current question.
  - **How**: form a concrete query, select only relevant channels, rank local records, inspect top hits, then state how the hits change the active proof state.
- **Failure as durable evidence**
  - **When to use**: whenever a branch, plan, or proof migration fails.
  - **How**: write a concrete reason and evidence to `failed_paths`; later planning must query and avoid repeating the same obstruction.

## Key Concepts

- **`immediate_conclusions`** — normalized direct consequences and fragility annotations.
- **`toy_examples`** — valid small cases and observed mechanisms.
- **`counterexamples`** — falsifiers or inconclusive falsification searches.
- **`big_decisions`** — major strategy choices.
- **`subgoals`** — decomposition plans and their statuses.
- **`proof_steps`** — direct proof attempts, used results, and migration outcomes.
- **`failed_paths`** — dead branches, blockers, and cross-plan failure summaries.
- **`verification_reports`** — every verifier response, including success.
- **`branch_states`** — branch lifecycle and recursive-round status.
- **`events`** — control-flow and retrieval traces.

## Mental Models

- Use memory as a **proof ledger**: every important state transition leaves a queryable artifact.
- Use retrieval as **state compression**: search the few channels that can answer the current question instead of rereading the run.
- Treat branch failure as **negative knowledge** that narrows the future search space.

## Anti-patterns

- **Keeping important failures only in chat context**: recursive agents can repeat them.
- **Searching every channel by default**: raises noise and weakens retrieval precision.
- **Mutating historical records in place**: destroys the sequence of decisions and repairs.
- **Changing `problem_id` between tools**: fragments one proof into multiple memory trees.

## Code Example

The source memory server tokenizes alphanumeric terms and scores stored JSON records with BM25-style ranking. Conceptually:

```python
hits = memory_search(problem_id, query, channels=["counterexamples", "failed_paths"], limit_per_channel=10)
```

Use equivalent local search if the MCP tool is unavailable.

## Reference Table

| Need | Read first | Usually write |
|---|---|---|
| Test a new claim against history | counterexamples, failed_paths | events |
| Re-plan after failure | failed_paths, branch_states | subgoals, events |
| Resume a partial proof | proof_steps, subgoals | proof_steps |
| Repair after verification | verification_reports, failed_paths | proof_steps, failed_paths |

## Worked Example

Suppose Plan B fails because a reduction requires compactness that the target setting lacks. Append that migration failure to `proof_steps`, summarize the dead route in `failed_paths`, and update the branch state. A later planning round queries `failed_paths` for “compactness” and rejects any new plan that quietly depends on the same missing structure.

## Key Takeaways

1. Initialize memory before mathematical work.
2. Append after each skill action and branch decision.
3. Query narrowly before repeating expensive reasoning.
4. Preserve failed paths as first-class knowledge.
5. Keep `problem_id` stable across all agents and tools.

## Connects To

- **Ch 4**: counterexamples and dead branches become durable memory.
- **Ch 7**: recursive agents share the same proof-state substrate.
- **Ch 9**: verifier findings are persisted and drive repair.

## Source Provenance

Primary source files: `agents/generation/AGENTS.md`, `agents/generation/mcp/server.py`, and `agents/generation/.agents/skills/query-memory/SKILL.md`.
