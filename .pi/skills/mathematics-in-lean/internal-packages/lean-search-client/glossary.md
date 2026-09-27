# Glossary

**Backend** — Remote search service selected or invoked by the client; string `#search` currently accepts only LeanSearch. (Ch 1, 6)

**Command context** — Top-level Lean command position; search hits become `#check` suggestions. (Ch 1, 5)

**Goal-as-query** — StateSearch pattern where the pretty-printed current main goal is sent to the remote service. (Ch 3)

**Infoview** — Lean UI surface where `TryThis` search suggestions appear. (Ch 1, 5)

**LeanSearch** — Natural-language theorem/tactic search service used by `#leansearch` and string `#search`. (Ch 2)

**LeanStateSearch** — Goal-state search service used by `#statesearch` and no-string tactic `#search`. (Ch 3)

**Loogle** — Structural Lean declaration search service with constant, name, type/subexpression, and conclusion filters. (Ch 4)

**Main-conclusion filter** — Loogle filter prefixed with `|-` or `⊢` to constrain the conclusion after hypotheses/binders. (Ch 4)

**Metavariable (`?a`)** — Loogle pattern variable whose repeated occurrences express a shared matched expression within a filter. (Ch 4)

**Punctuation gate** — LeanSearch rule requiring query strings to end in `.` or `?` before remote lookup. (Ch 2)

**Revision** — LeanStateSearch index/version selected through `statesearch.revision`. (Ch 3, 6)

**SearchResult** — Normalized record holding declaration name and optional type/documentation metadata across backends. (Ch 5)

**Tactic validation** — Non-destructive parse/elaboration of generated tactic candidates against a fresh metavariable for the current target. (Ch 5)

**Term context** — Expression position; search hits become declaration-name suggestions. (Ch 1, 5)

**TryThis** — Lean suggestion mechanism used to present clickable/code-action search results. (Ch 1, 5)

**Wildcard (`_`)** — Unconstrained hole in a Loogle structural pattern. (Ch 4)
