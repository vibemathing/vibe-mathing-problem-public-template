# LeanSearchClient Cheatsheet

## Pick a route
| Input signal | Use |
|---|---|
| English description | `#search "... ."` / `#leansearch "... ?"` |
| Current proof goal | tactic `#search` or `#statesearch` |
| Known Lean shape/name/type | `#loogle ...` |

## Context forms
```lean
#search "Find a theorem matching this description."
example := #search "Find a term matching this type."
example : P := by
  #search "Find a tactic/theorem for this goal."
  sorry
```

## Loogle filters
```lean
#loogle Real.sin                  -- mentions constant
#loogle "differ"                  -- lemma-name substring
#loogle _ * (_ ^ _)               -- subexpression shape
#loogle Real.sqrt ?a * Real.sqrt ?a
#loogle |- tsum _ = _ * tsum _    -- main conclusion
#loogle Option ?a → ?a, "get!"    -- AND filters
```

## Options
```lean
set_option leansearch.queries 6
set_option loogle.queries 6
set_option statesearch.queries 6
set_option statesearch.revision "v<supported-version>"
set_option leansearchclient.backend "leansearch"
set_option leansearchclient.useragent "LeanSearchClient"
```

## Endpoint overrides
- `LEANSEARCHCLIENT_LEANSEARCH_API_URL`
- `LEANSEARCHCLIENT_LEANSTATESEARCH_API_URL`
- `LEANSEARCHCLIENT_LOOGLE_API_URL`

## Fast diagnosis
| Symptom | Fix/check |
|---|---|
| LeanSearch punctuation warning | end string with `.` or `?` |
| invalid backend | use `leansearch` |
| unsupported StateSearch revision | choose server-supported revision |
| no tactic candidate | inspect returned declaration / fallback `#check` |
| no Loogle hits | remove filters; inspect usage/suggestions |
| live test changed | suspect ranking/import drift or rate limiting |
| parse/contact error | endpoint + remote JSON/schema |

**Remember**: validated tactic means it executes in the current state; it may leave goals.
