# Chapter 2: LeanSearch Natural-Language Search

## Core Idea
LeanSearchClient sends natural-language queries to LeanSearch and maps returned declarations into Lean suggestions. The most important precondition is local: the query string must end in a period or question mark before any remote request is attempted.

## Frameworks Introduced
- **Punctuation-gated remote search**
  - When to use: diagnosing a `#leansearch` or string `#search` that only warns.
  - How: ensure the string ends in `.` or `?`; otherwise the client intentionally skips querying the server.
- **Context-specific result projection**
  - When to use: deciding how a LeanSearch result should appear.
  - How: command → `#check`; term → name; tactic → candidate tactics, later validated locally.

## Key Concepts
- **Endpoint**: default LeanSearch URL is `https://leansearch.net/search`; override with `LEANSEARCHCLIENT_LEANSEARCH_API_URL`.
- **Request**: HTTP POST via `curl`, JSON body containing a one-element `query` array and `num_results`.
- **Result count**: `leansearch.queries`, default 6.
- **User agent**: supplied from `leansearchclient.useragent`, default `LeanSearchClient`.
- **Cache**: response array keyed by `(query, num_results)`.
- **Normalization**: backend JSON is converted into `SearchResult` records with name, optional type/doc URL/docstring/kind.

## Mental Models
- Treat punctuation as a **trigger token**, not prose style. Missing punctuation means the server is never contacted.
- Separate **transport failure** from **suggestion failure**: JSON/HTTP parsing occurs before mapping to `SearchResult` and before tactic validation.
- Treat result ranking as **live service state**; exact top hits are unsuitable as stable local invariants.

## Anti-patterns
- **Debugging networking before checking punctuation**: the local guard can explain the behavior immediately.
- **Asserting exact live rankings in tests**: repository comments document ranking drift and environment-dependent elaboration.
- **Assuming a returned theorem becomes a valid tactic automatically**: tactic mode validates generated tactic forms against the current target.

## Code Examples
```lean
#leansearch "If a natural number n is less than m, then the successor of n is less than the successor of m."

example := #search "If a natural number n is less than m, then the successor of n is less than the successor of m."

example : 3 ≤ 5 := by
  #leansearch "If a natural number n is less than m, then the successor of n is less than the successor of m."
  sorry
```
- **What it demonstrates**: explicit/common entry points and command/term/tactic contexts.

## Reference Table
| Symptom | First check | Next layer |
|---|---|---|
| warning: query should end `.` or `?` | terminal punctuation | none until fixed |
| invalid `#search` backend | `leansearchclient.backend` | set to `leansearch` |
| server parse error | endpoint/response JSON | override URL or inspect service |
| no tactic suggestion | local tactic filtering | inspect declaration manually |
| live test changed | service ranking/import context | avoid exact-result assertion |

## Key Takeaways
1. End natural-language queries with `.` or `?`.
2. `#leansearch` and string `#search` share the same LeanSearch behavior in this snapshot.
3. Result count and endpoint are configurable without editing source.
4. Cache keys include query and result count.
5. Keep live-service output probabilistic in tests and explanations.

## Decision Procedure
1. Confirm the user wants semantic/natural-language retrieval.
2. Normalize the query into one complete sentence and add `.` or `?`.
3. Choose `#search` for the common entry point or `#leansearch` when explicit backend intent improves clarity.
4. Match command, term, or tactic context.
5. If no useful tactic survives local checking, separate “search hit exists” from “this hit is directly usable as a tactic” and inspect the declaration.

## Connects To
- **Ch 5**: `SearchResult` projection and tactic validation.
- **Ch 6**: options, endpoint overrides, service drift and rate limiting.

Preserve the user’s original mathematical intent when adding punctuation; the punctuation is only the trigger.
