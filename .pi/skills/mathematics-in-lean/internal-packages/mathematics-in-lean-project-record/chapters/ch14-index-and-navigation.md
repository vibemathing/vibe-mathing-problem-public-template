# Chapter 14: Index

## Core Idea
The source index adds no new mathematical method; it is a navigation layer over the earlier chapters. In this skill, the same function is split among the master Topic Index, glossary, patterns, cheatsheet, and chapter links.

## Frameworks Introduced
- **Index-to-capability lookup**
  - When to use: the user names a tactic, concept, or mathematical object without a goal.
  - How: resolve the term in [../glossary.md](../glossary.md) or the master Topic Index, then load the cited chapter before giving source-specific guidance.

## Key Concepts
The printed index emphasizes recurring entry points: `apply`, `calc`, `cases`, `change`, `congr`, `constructor`, `contrapose`, `convert`, `decide`, `dsimp`, `erw`, `exact`, `ext`, `field_simp`, `group`, `have`, `intro`, `linarith`, `norm_num`, `push_neg`, `rcases`, `ring`, `rintro`, `rw`, `simp`, `trans`, `use`; plus mathematical topics such as groups, lattices, linear maps, matrices, filters, topology, differential calculus, measure theory, and integration.

## Mental Models
- Treat the source index as a **reverse map from vocabulary to method location**.
- When a tactic name appears, first ask what **goal shape** or **mathematical structure** it is designed for; route to the chapter that explains that purpose.

## Anti-patterns
- **Using the index as a theorem-name encyclopedia**: it locates concepts; it does not replace checking the current Mathlib signature.
- **Answering from a keyword alone when source behavior is version-sensitive**: load the chapter context and verify in the active Lean environment.

## Reference Tables
| Index family | Skill destination |
|---|---|
| basic tactics / proof state | ch01–03 |
| sets / functions / extensionality | ch04 |
| induction / number theory | ch05 |
| Finset / counting / inductive types | ch06 |
| structures / instances | ch07–08 |
| groups / rings | ch09 |
| linear maps / matrices | ch10 |
| filters / topology / continuity | ch11 |
| differential calculus / normed spaces | ch12 |
| integration / measure theory | ch13 |

## Worked Example
A request such as “When should I use `convert`?” routes to ch03 because `convert` is an equality-adjustment tactic: apply a nearly matching theorem, then solve the equations that reconcile its conclusion with the current target. A request such as “Why is my group operation ambiguous?” routes to ch07–08 because it is usually a typeclass/hierarchy issue, not a basic tactic issue.

## Key Takeaways
1. Use the index as routing metadata, not as standalone instruction.
2. Load the explanatory chapter for semantics, preconditions, failure modes, and alternatives.
3. Verify API-sensitive names against the user's active Mathlib version.

## Connects To
- **SKILL.md Topic Index**: first routing layer.
- **glossary.md**: definitions and chapter references.
- **patterns.md / cheatsheet.md**: operational procedures and fast decisions.
