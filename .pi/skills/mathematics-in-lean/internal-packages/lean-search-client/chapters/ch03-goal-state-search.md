# Chapter 3: Goal-State Search

## Core Idea
LeanStateSearch uses the current pretty-printed Lean goal as the remote query. It is available explicitly as `#statesearch` and implicitly when tactic `#search` is used without a string.

## Frameworks Introduced
- **Goal-as-query**
  - When to use: the user is inside a proof and wants theorem/tactic candidates without describing the goal in prose.
  - How: pretty-print the main goal, send it with result count and revision, normalize results, then validate tactic forms locally.
- **Revision-aware retrieval**
  - When to use: server compatibility matters across Lean versions.
  - How: set `statesearch.revision`; treat server rejection as an explicit compatibility failure.
- **Suggestion fallback**
  - When to use: search returns declarations but every generated tactic form fails local validation.
  - How: fall back to command-style `#check` suggestions so useful declarations are still visible.

## Key Concepts
- **`#statesearch`**: tactic-only goal-state search.
- **No-string `#search`**: tactic alias that evaluates `#statesearch`.
- **Endpoint**: default `https://premise-search.com/api/search`; override with `LEANSEARCHCLIENT_LEANSTATESEARCH_API_URL`.
- **Parameters**: escaped goal query, `results`, and `rev` are encoded in the GET URL.
- **Result count**: `statesearch.queries`, default 6.
- **Revision**: `statesearch.revision`, default `v{Lean.versionString}`.
- **Cache**: key is `(goal-query, result-count, revision)`.

## Mental Models
- Use StateSearch when the **formal state already contains the best query**.
- Treat revision as part of the semantic request; changing revision can change validity and results, so it belongs in the cache key.
- A failed tactic projection does not erase a useful search hit: the client can downgrade to declaration inspection.

## Anti-patterns
- **Hard-coding a historical revision from an example**: test data shows one revision can be rejected by the service.
- **Assuming local Lean version guarantees remote support**: server support is an external constraint.
- **Interpreting no validated tactic as no search results**: declarations may still be shown through fallback suggestions.

## Code Examples
```lean
set_option statesearch.queries 1
set_option statesearch.revision "v4.22.0"

example : 0 < 1 := by
  #statesearch
  sorry

example : 0 < 1 := by
  #search
  sorry
```
- **What it demonstrates**: explicit and implicit goal-state search with configurable result count/revision.

## Reference Table
| Situation | Action |
|---|---|
| Want suggestions from current goal | `#statesearch` |
| Prefer common alias | tactic `#search` with no string |
| Too many/few hits | set `statesearch.queries` |
| server says revision unsupported | change `statesearch.revision` to a supported revision |
| results exist but tactics fail | inspect fallback `#check` suggestions |

## Key Takeaways
1. StateSearch is driven by the current main goal, not a natural-language string.
2. Revision is a first-class compatibility parameter.
3. No-string tactic `#search` delegates here.
4. Candidate tactics are checked locally before display.
5. When tactic projection fails, declaration-level fallback preserves useful results.

## Decision Procedure
1. Confirm there is an active main goal and the user wants the goal itself to drive retrieval.
2. Use `#statesearch` for explicitness, or tactic `#search` with no string for the common alias.
3. Start with the configured/default result count and revision; change them only when volume or compatibility requires it.
4. If the server rejects the revision, treat that as a remote-index compatibility problem and select a supported revision.
5. If hits return but every generated tactic is rejected locally, inspect the fallback declarations instead of concluding that StateSearch found nothing.
6. When debugging repeated results, remember that revision participates in the cache key.

## Reliability Boundary
The source test suite demonstrates successful queries with one revision and explicit rejection of another. Those examples establish the failure mode, not a timeless list of supported revisions. The remote service decides revision availability. An agent should therefore describe a tested revision as an example from this source snapshot unless it has current service evidence.

## Connects To
- **Ch 5**: tactic generation and validation details.
- **Ch 6**: revision diagnostics and endpoint configuration.
