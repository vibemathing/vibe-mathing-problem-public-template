# Chapter 6: Configuration, Testing & Failure Modes

## Core Idea
Most operational failures can be classified before touching implementation code: local query preconditions, invalid options/revisions, endpoint/network/schema failures, or live-service drift. The source and tests encode concrete diagnostics for each layer.

## Frameworks Introduced
- **Layered diagnosis**
  - When to use: any warning, error, empty result, or changed test output.
  - How: check syntax/preconditions → options/revision → endpoint/network → JSON schema → suggestion validation → live ranking/environment drift.
- **Deterministic-vs-live test split**
  - When to use: designing tests around external search services.
  - How: keep parser/routing/error tests deterministic; avoid assertions on exact live ranking unless isolated and tolerant of drift.

## Key Concepts
- **`leansearch.queries`**: LeanSearch result count; default 6.
- **`loogle.queries`**: Loogle result count; default 6.
- **`statesearch.queries`**: StateSearch result count; default 6.
- **`statesearch.revision`**: target LeanStateSearch revision; defaults to local Lean version prefixed with `v`.
- **`leansearchclient.useragent`**: HTTP user agent; default `LeanSearchClient`.
- **`leansearchclient.backend`**: default string-query backend; current accepted value is `leansearch`.
- **Endpoint overrides**: `LEANSEARCHCLIENT_LEANSEARCH_API_URL`, `LEANSEARCHCLIENT_LEANSTATESEARCH_API_URL`, `LEANSEARCHCLIENT_LOOGLE_API_URL`.
- **Toolchain pin**: source snapshot uses `leanprover/lean4:v4.34.0-rc2`.
- **CI**: GitHub Actions checks the project with `leanprover/lean-action@v1`.

## Mental Models
- Diagnose the **cheapest local invariant first**: punctuation and option values beat network debugging.
- An external search ranking is data, not interface contract.
- A result can fail locally because the current imports/environment differ from the environment assumed by the remote index.

## Anti-patterns
- **Exact live-result golden tests**: repository comments disabled such a test after rankings/import requirements drifted.
- **Assuming more retries fix malformed queries**: punctuation/backend/revision errors are deterministic configuration issues.
- **Ignoring service pacing**: test comments explicitly used a sleep to avoid rate limiting.
- **Treating endpoint parse errors as tactic-elaboration failures**: keep transport/schema and Lean elaboration layers separate.

## Code Examples
```lean
set_option leansearch.queries 3
set_option loogle.queries 8
set_option statesearch.queries 4
set_option statesearch.revision "v4.22.0"
set_option leansearchclient.backend "leansearch"
```
- **What it demonstrates**: local control of result volume, StateSearch compatibility, and common-backend routing.

## Troubleshooting Table
| Symptom | Likely layer | Recovery |
|---|---|---|
| query warning before network | syntax | add terminal `.`/`?` for LeanSearch |
| `Invalid backend magic` | configuration | set backend to `leansearch` |
| StateSearch `Invalid parameter value` / revision unsupported | remote compatibility | select supported revision |
| server cannot be contacted / response cannot parse | network/schema | verify endpoint override and service response |
| no valid tactic displayed | local elaboration | inspect declaration results; try manually |
| expected live theorem vanished/reordered | remote ranking/environment | avoid exact-rank assertion, inspect imports |
| intermittent service failures | external service/rate limit | reduce repeated calls, retry later in an interactive workflow |

## Key Takeaways
1. Options and env vars cover most operational configuration without source edits.
2. Diagnose local deterministic failures before remote ones.
3. StateSearch revision support is a server constraint.
4. Exact live rankings should not be a hard test oracle.
5. Separate retrieval, schema parsing, suggestion projection, and Lean elaboration when debugging.

## Diagnostic Procedure
1. Reproduce the smallest failing form.
2. Check local preconditions and option values.
3. Confirm the selected endpoint and revision.
4. Distinguish “request failed” from “request succeeded but returned unusable declarations”.
5. For live-result regressions, compare imports/toolchain and service behavior before changing parser logic.
6. Keep exact-ranking checks out of ordinary regression tests; use guarded message tests for deterministic warnings/errors and a separate live-service check when needed.

## Connects To
- **Ch 2–4**: backend-specific symptoms and endpoints.
- **Ch 5**: local suggestion filtering after retrieval succeeds.

Record whether a failure is deterministic or live-service dependent before deciding what kind of test should cover it.
