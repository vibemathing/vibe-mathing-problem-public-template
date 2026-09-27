# Lean4 Self-Study Routing Cheatsheet

## Fast decisions

| If you need to… | Use first | Then / fallback |
|---|---|---|
| install Lean | Installation tutorial | After setup, choose a foundation track |
| learn Lean programming | leanprover.cn → *Functional Programming in Lean* | Move to theorem proving/formal math as needed |
| learn proving | leanprover.cn → *Theorem Proving in Lean* | Natural Number Game for optional beginner practice |
| study formal mathematics | *Mathematics in Lean* | Use ch02 tools when lookup blocks progress |
| learn metaprogramming | leanprover.cn → *Metaprogramming in Lean* | Stay within source coverage for extra details |
| follow lectures | NUS Lean minicourse | Pair with other listed resources by goal |
| get a quick reference | Terence Tao's Lean cheatsheet | Mathlib docs for declaration-level detail |
| run Lean online | official Lean online compiler | Installation tutorial if local setup is needed |
| inspect Mathlib/API | Mathlib4 docs | Theorem search if the declaration name is unknown |
| find a theorem | LeanSearch or Moogle | Try the other; then Zulip if still blocked |
| ask for help | Zulip | Bring the smallest Lean context you can |
| try automated formalization | Quokka | Validate the result in Lean; fall back to search/help |
| suspect a ReasLab/Quokka service bug | Reproduce and separate code error from service defect | If still a service bug, use only a feedback path the current service exposes |

## Routing rules

- **Formal-math goal → prioritize *Mathematics in Lean*** because the archive explicitly marks it as strongly recommended.
- **Unknown theorem name → search; known area/name → docs.**
- **Search result → compile/check before relying on it.**
- **Automation output → Lean validation before acceptance.**
- **Resource mismatch → reclassify the goal, then switch within the archived list.**
- **Archive has no evidence → state the limit.**
