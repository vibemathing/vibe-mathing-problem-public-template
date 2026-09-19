# Patterns

## Choose Search Backend
**When to use**: Before composing a query.  
**How**: Natural language → LeanSearch; current proof goal → StateSearch; structural/type/name/conclusion pattern → Loogle. Then choose command/term/tactic syntax.  
**Trade-offs**: Natural language is flexible but service-ranked; structural search is precise but requires known shape; goal-state search requires an active goal and compatible revision.

## LeanSearch Query Gate
**When to use**: A `#search "..."` / `#leansearch "..."` call warns or appears inactive.  
**How**: End the query with `.` or `?`; then check backend, endpoint, and response parsing.  
**Trade-offs**: This is a local convention of the client, so natural-language strings without terminal punctuation intentionally do not query the server.

## Goal-State Search
**When to use**: The formal goal already captures the problem.  
**How**: Use `#statesearch` or tactic `#search` with no string; tune `statesearch.queries` and `statesearch.revision`.  
**Trade-offs**: Remote revision support can lag or differ from the local toolchain.

## Structural Loogle Query
**When to use**: You know a constant, lemma-name fragment, subexpression/type shape, or main conclusion.  
**How**: Compose filters with `_`, `?a`, quoted substrings, and `|-`/`⊢`; add comma-separated filters to narrow.  
**Trade-offs**: Added filters improve precision and can eliminate all hits; reduce constraints progressively when empty.

## Normalize Then Project
**When to use**: Explaining or extending backend integration.  
**How**: Parse remote JSON into `SearchResult`, then render per Lean context: command → `#check`; term → name; tactic → candidates.  
**Trade-offs**: Schema changes are isolated to parsers; context-specific behavior stays shared.

## Validate Tactic Candidates Locally
**When to use**: Turning a declaration hit into proof actions.  
**How**: Try `apply`, typed `have`, `rw`, reverse `rw`; parse/run each against a fresh goal without modifying state; keep successful candidates.  
**Trade-offs**: Successful execution may leave subgoals; validity does not mean proof closure.

## StateSearch Declaration Fallback
**When to use**: StateSearch returns hits yet no generated tactic validates.  
**How**: Surface command-style `#check` suggestions for the returned declarations.  
**Trade-offs**: Requires manual proof integration, but preserves useful retrieval.

## Layered Failure Diagnosis
**When to use**: Any warning/error/no-result condition.  
**How**: Check local syntax → options/revision → endpoint/network → JSON schema → local tactic elaboration → live ranking/import drift.  
**Trade-offs**: Prevents expensive debugging in the wrong layer; live-service failures can still require external recovery.

## Stable External-Service Testing
**When to use**: Writing regression tests.  
**How**: Assert deterministic parser/routing/error behavior; isolate live calls and avoid exact ranking as the oracle.  
**Trade-offs**: Less end-to-end certainty from unit tests, but far lower flakiness from ranking changes, imports, and rate limits.
