# Chapter 1: Orientation & Routing

## Core Idea
LeanSearchClient is a thin Lean 4 integration layer over three search services. Correct use begins by routing the user's information—natural-language intent, current proof state, or structural pattern—to the matching service and then choosing the Lean syntax context.

## Frameworks Introduced
- **Signal-to-backend routing**
  - When to use: before writing any search command.
  - How: natural-language description → LeanSearch; current goal → LeanStateSearch; structural/name/type pattern → Loogle.
- **Context-preserving output**
  - When to use: whenever the user is already inside a declaration or proof.
  - How: distinguish command, term, and tactic position before emitting a snippet.

## Key Concepts
- **`#search`**: common entry point. String queries currently route to LeanSearch; no-string tactic use delegates to StateSearch.
- **`#leansearch`**: explicit natural-language LeanSearch entry point.
- **`#statesearch`**: explicit current-goal StateSearch tactic.
- **`#loogle`**: structural search entry point with Lean-like filter syntax.
- **Infoview suggestions**: results are surfaced through Lean's `TryThis` mechanism so users can click or apply code actions.
- **Backend option**: `leansearchclient.backend`; this source supports `leansearch` for string-based `#search`.

## Mental Models
- Use **intent first, syntax second**: pick the search family from available information, then adapt to command/term/tactic context.
- Treat `#search` as a convenience router with two behaviors: string → configured LeanSearch backend; no string in tactic → StateSearch.
- Think of each remote backend as retrieval and the client as the layer that turns retrieval into locally usable Lean suggestions.

## Anti-patterns
- **Using natural language when the exact type shape is known**: Loogle can express structural constraints directly.
- **Using `#statesearch` without a proof goal**: it is a tactic built around the current main goal.
- **Assuming multiple selectable `#search` string backends**: the option exists, yet this snapshot rejects values other than `leansearch`.
- **Ignoring context**: a declaration name valid as a term may need `apply` or `rw` in tactic position.

## Code Examples
```lean
#search "If a natural number n is less than m, then the successor of n is less than the successor of m."

example : 3 ≤ 5 := by
  #search
  sorry

#loogle List ?a → ?a
```
- **What it demonstrates**: three routing modes—natural language, current goal, and structural type pattern.

## Reference Table
| Need | Preferred form | Why |
|---|---|---|
| Describe theorem in English | `#search "... ."` | LeanSearch is natural-language oriented |
| Search from proof state | tactic `#search` or `#statesearch` | goal is serialized as query |
| Match type/name/subexpression | `#loogle ...` | query language encodes structure |
| Force LeanSearch explicitly | `#leansearch "... ?"` | bypasses common alias |

## Key Takeaways
1. Route by query signal before composing syntax.
2. Preserve command/term/tactic context in the answer.
3. No-string tactic `#search` is a StateSearch shortcut.
4. The current configurable string backend is effectively fixed to LeanSearch.
5. Remote result content can vary; local routing semantics come from this source snapshot.

## Decision Procedure
1. Ask what information is available: prose description, active goal, or formal shape.
2. Ask where the snippet will live: top-level command, term position, or tactic block.
3. Select the backend before formatting the final syntax.
4. If the user says only “search”, prefer `#search` for natural language or current-goal tactic use; prefer explicit `#loogle` when structural constraints are present.
5. State any remote-service dependency when the user expects a particular hit.

## Connects To
- **Ch 2**: natural-language query details.
- **Ch 3**: current-goal routing and revision handling.
- **Ch 4**: structural Loogle grammar.
- **Ch 5**: how raw results become context-specific suggestions.

Prefer the explicit backend command when teaching or debugging, because it makes the intended route visible.
