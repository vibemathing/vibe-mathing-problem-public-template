---
name: lean-search-client
description: Operational knowledge base for the LeanSearchClient Lean 4 library. Use when choosing or writing #search, #leansearch, #statesearch, or #loogle queries; configuring result counts, backend/revision/API URLs; interpreting TryThis suggestions; troubleshooting search warnings/errors; or extending the client implementation.
when_to_use: use #search in Lean, find a theorem with LeanSearchClient, use LeanSearch from Lean, search from the current proof goal, use LeanStateSearch, write a Loogle query, choose #leansearch vs #statesearch vs #loogle, #search query should end with a period, configure leansearch.queries, configure statesearch.revision, change LeanSearchClient API URL, troubleshoot no search results, understand TryThis search suggestions, filter invalid tactic suggestions, extend LeanSearchClient
allowed-tools: Read Grep
argument-hint: [query goal symptom backend option or implementation topic]
---

# LeanSearchClient
**Source**: LeanSearchClient repository | **Author**: Siddhartha Gadgil | **Source units**: 14 project/config/test files + license | **Generated**: 2026-09-12

## How to Use This Skill

Classify the request first, then load only the relevant chapter.

- Natural-language theorem/tactic search → use **LeanSearch**: read [ch02](chapters/ch02-leansearch-natural-language.md).
- Search directly from the current Lean goal → use **LeanStateSearch**: read [ch03](chapters/ch03-goal-state-search.md).
- Search by constant, name fragment, type/subexpression, or conclusion shape → use **Loogle**: read [ch04](chapters/ch04-loogle-structural-search.md).
- Explain Infoview/`TryThis`, caching, or tactic filtering → read [ch05](chapters/ch05-suggestions-validation-cache.md).
- Diagnose options, endpoints, unsupported revisions/backends, flaky tests, or live-service behavior → read [ch06](chapters/ch06-configuration-testing-failures.md).

For a concrete Lean snippet, preserve the user's command/term/tactic context. When a claim depends on a backend's live results, label it as service-dependent.

---

## Core Frameworks & Mental Models

### 1. Route by the information you already have
Use the backend that matches the query signal:

| You have | Route | Typical syntax |
|---|---|---|
| A natural-language description | LeanSearch | `#search "... ."` or `#leansearch "... ?"` |
| A live proof goal | LeanStateSearch | tactic `#search` with no string or `#statesearch` |
| Structural/type/name constraints | Loogle | `#loogle <filters>` |

Do not force every search through natural language. Loogle is stronger when the desired shape is known; StateSearch is stronger when the proof state itself is the query.

### 2. Treat syntax context as part of the request
LeanSearchClient supports **command**, **term**, and **tactic** use. The same search result is transformed differently:
- command context → `#check <name>` suggestions;
- term context → declaration-name suggestions;
- tactic context → tactic candidates derived from the declaration.

When answering, emit syntax for the user's current context. A correct declaration wrapped in the wrong context is still an unusable answer.

### 3. Tactic results are locally validated
For a result with a type, the client tries `apply`, a typed `have`, `rw`, and reverse `rw`. Each candidate is parsed and elaborated against a fresh metavariable with the current goal. Keep this distinction clear: validation checks that a tactic can elaborate/run in the current state; it does not prove that the suggestion closes every remaining goal.

### 4. `#search` has asymmetric routing
With a query string, `#search` consults `leansearchclient.backend`; the current implementation accepts only `leansearch`. In tactic position with **no string**, `#search` delegates to `#statesearch` and searches from the current goal. Missing strings in command/term LeanSearch forms only produce the incomplete-query warning.

### 5. LeanSearch uses a punctuation gate
A LeanSearch string triggers the remote call only when it ends in `.` or `?`. If the punctuation is absent, diagnose the warning before investigating networking or server behavior.

### 6. Cache keys follow semantic inputs
- LeanSearch cache: `(query, result-count)`.
- StateSearch cache: `(goal-query, result-count, revision)`.
- Loogle cache: `(query, result-count)`.

When extending or debugging caching, every parameter that can change the remote response belongs in the key.

### 7. Live search is inherently unstable
The test suite disables assertions that depend on LeanSearch ranking because live results drift and can elaborate differently as environments change. Treat exact rankings as observations, not contracts. Use deterministic tests for parser/routing/error behavior; isolate live-service checks.

---

## Decision Workflow

1. **Identify user intent**: natural language, current goal, or structural pattern.
2. **Identify Lean context**: command, term, or tactic.
3. **Choose backend** with the routing table above.
4. **Check preconditions**: LeanSearch punctuation; supported backend; StateSearch revision; non-empty Loogle filters.
5. **Produce the smallest useful snippet** plus any required `set_option`.
6. **Diagnose failure by layer**: syntax/precondition → local elaboration → backend configuration → network/remote response.
7. **Validate the explanation** against the relevant chapter and avoid promising a specific live result.

## Failure Recovery

- LeanSearch warning about query form → append terminal `.` or `?`.
- `Invalid backend ...` → set `leansearchclient.backend "leansearch"`; no other string backend is implemented in this source.
- StateSearch says revision unsupported → choose a revision supported by the service; do not infer support from the local Lean version alone.
- StateSearch returns declarations but no usable tactic → inspect fallback `#check` suggestions and apply/refine manually.
- Loogle empty/no-result/error → show Loogle usage, simplify filters, or use server-provided spelling/query suggestions.
- Live result mismatch or flaky test → suspect service drift, imported-environment differences, or rate limiting before changing parser logic.
- JSON/network parsing failure → verify endpoint override, connectivity, and server schema before debugging suggestion rendering.

## SELF_CHECK

Before finalizing an answer, verify: the route matches the query signal; the Lean context is correct; required punctuation/revision/options are present; no unsupported backend is implied; live rankings are not presented as deterministic; tactic-validity claims do not imply goal closure; and a failure path is provided when the remote service can reject or return nothing.

---

## Chapter Index

| # | Title | Key capabilities |
|---|---|---|
| [ch01](chapters/ch01-orientation-routing.md) | Orientation & routing | select backend, select Lean context, scope |
| [ch02](chapters/ch02-leansearch-natural-language.md) | LeanSearch natural-language search | query gate, command/term/tactic, HTTP/API behavior |
| [ch03](chapters/ch03-goal-state-search.md) | Goal-state search | `#statesearch`, no-string `#search`, revisions, fallback |
| [ch04](chapters/ch04-loogle-structural-search.md) | Loogle structural search | constants, name substrings, patterns, conclusions, combined filters |
| [ch05](chapters/ch05-suggestions-validation-cache.md) | Suggestions, validation & cache | `SearchResult`, `TryThis`, tactic filtering, cache keys |
| [ch06](chapters/ch06-configuration-testing-failures.md) | Configuration, testing & failures | options, URL overrides, drift, rate limiting, CI |

## Topic Index

- **API URL overrides** → ch02, ch03, ch04, ch06
- **backend selection** → ch01, ch06
- **caching** → ch02, ch03, ch04, ch05
- **command / term / tactic** → ch01, ch02, ch04, ch05
- **goal-state search** → ch03
- **Loogle filters** → ch04
- **natural-language search** → ch02
- **punctuation warning** → ch02, ch06
- **result count options** → ch06
- **revision errors** → ch03, ch06
- **tactic validation** → ch05
- **TryThis** → ch05

## Supporting Files

- [glossary.md](glossary.md) — key terms and source-specific meanings
- [patterns.md](patterns.md) — operational procedures and recovery patterns
- [cheatsheet.md](cheatsheet.md) — one-page command and troubleshooting reference

---

## Scope & Limits

This skill covers the supplied LeanSearchClient source snapshot. It can guide usage, diagnosis, and implementation reasoning for that snapshot. Remote LeanSearch, LeanStateSearch, and Loogle results can change independently. For proving a theorem, combine this skill with the actual project environment and Lean tooling.
