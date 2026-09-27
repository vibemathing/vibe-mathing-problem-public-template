# Chapter 4: Loogle Structural Search

## Core Idea
Loogle is the right backend when the user can describe the syntactic or type structure of a wanted declaration. LeanSearchClient exposes Loogle filters directly inside Lean and converts success, empty, and failure responses into actionable Infoview feedback.

## Frameworks Introduced
- **Structural-filter search**
  - When to use: constants, lemma-name fragments, subexpressions, type patterns, or conclusion shapes are known.
  - How: compose one or more filters; comma-separated filters are conjunctive.
- **Progressive constraint**
  - When to use: results are too broad or empty.
  - How: start with one strong filter, add filters to narrow; remove filters when over-constrained.
- **Server-assisted repair**
  - When to use: Loogle returns an error with suggestions.
  - How: surface the error/usage guidance and offer the server-provided query suggestions through `TryThis`.

## Key Concepts
- **Constant filter**: e.g. `Real.sin`.
- **Name-substring filter**: quoted text such as `"differ"`.
- **Subexpression pattern**: e.g. `_ * (_ ^ _)`.
- **Metavariable**: `?a` links repeated occurrences within a filter; parameters can match hypotheses in varying order.
- **Main-conclusion filter**: prefix with `|-` or `⊢` to constrain the conclusion after leading binders/arrows.
- **Combined filters**: comma separation means all filters must match.
- **Endpoint**: default `https://loogle.lean-lang.org/json`; override with `LEANSEARCHCLIENT_LOOGLE_API_URL`.
- **Result count**: `loogle.queries`, default 6.

## Mental Models
- Choose Loogle when the target is easier to **draw as a type pattern** than describe in English.
- `_` is an unconstrained hole; `?a` is a reusable variable that expresses equality/relationship across positions.
- Multiple filters form an AND query, so each added filter trades recall for precision.

## Anti-patterns
- **Over-constraining immediately**: a long multi-filter query can hide which condition eliminated results.
- **Treating `?a` as an independent wildcard every time**: repeated metavariable occurrences encode the same matched expression within a filter.
- **Ignoring empty-query behavior**: empty `#loogle` in tactic form prints usage guidance rather than performing search.
- **Embedding comments as if they were query content**: the implementation trims block-comment suffixes before sending the request.

## Code Examples
```lean
#loogle List ?a → ?a
#loogle "differ"
#loogle _ * (_ ^ _)
#loogle |- tsum _ = _ * tsum _
#loogle Option ?a → ?a, "get!"
```
- **What it demonstrates**: type shape, name substring, subexpression, main conclusion, and conjunctive filters.

## Reference Table
| What you know | Filter form |
|---|---|
| a constant occurs | `Real.sin` |
| part of lemma name | `"differ"` |
| subexpression shape | `_ * (_ ^ _)` |
| repeated same expression | `?a ... ?a` |
| desired main conclusion | `|- <pattern>` or `⊢ <pattern>` |
| several conditions | `<filter1>, <filter2>, ...` |

## Failure Recovery
- Empty input → read the emitted usage guide and add a filter.
- No hits → remove the weakest/most restrictive filter, then retry.
- Server error with suggestions → try the suggested corrected query.
- Command/term result wanted as tactic → allow the client to generate and locally validate tactic candidates.

## Key Takeaways
1. Loogle is structural search, not natural-language search.
2. Comma-separated filters are conjunctive.
3. Use `|-`/`⊢` to target the main conclusion.
4. Use server-provided suggestions for malformed/failed queries.
5. Query cleanup strips block-comment suffixes and flattens newlines before sending.

## Decision Procedure
Start from the strongest single fact you know. Use a constant when vocabulary is known, a quoted substring when the declaration name is partly known, a shape when the type/subterm structure is known, and `|-`/`⊢` when only the conclusion shape matters. Add comma-separated filters one at a time so an empty result can be traced to the constraint that caused it.

## Connects To
- **Ch 1**: selecting Loogle over the other backends.
- **Ch 5**: shared `SearchResult` and tactic-suggestion machinery.
