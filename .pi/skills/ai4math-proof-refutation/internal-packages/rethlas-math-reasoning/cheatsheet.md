# Rethlas Decision Cheatsheet

## Main routing loop

| If the current state looks like… | Do this next | Why |
|---|---|---|
| new problem / branch / subgoal | immediate conclusions | cheapest structural information |
| hypotheses feel opaque | toy example | expose where assumptions act |
| claim or subgoal feels fragile | counterexample test | prune false routes early |
| old obstruction may already exist | narrow memory query | avoid repeating work |
| missing theorem/background | statement-first retrieval | ground the next move |
| useful external theorem found | read context + proof; applicability audit | statement similarity can mislead |
| external result has extra hypotheses | diagnose why they are needed | reveals the real obstruction |
| enough constraints accumulated | several materially different plans | diversify proof architecture |
| a plan was just created | direct-screen every subgoal | earn escalation cost |
| direct subgoal is blocked | counterexample test before more proof effort | distinguish false/too-strong from hard |
| all plans screened, none solved | recursive agent per plan | parallelize informed routes |
| recursive routes all fail | synthesize key failures → re-plan | prevent repetition |
| complete whole-target proof exists | strict verification | only full proofs enter acceptance gate |
| verifier finds any error/gap | repair → re-verify full proof | zero-tolerance verdict rule |
| retrieval repeatedly adds no guidance | stop search; reason independently | search is support, not the engine |

## Hard gates

- **Rethlas-verified** requires a complete proof plus verifier verdict `correct`, `critical_errors=[]`, and `gaps=[]`.
- **A failed counterexample search is not a proof.**
- **A similar external theorem is not applicable until definitions, hypotheses, ambient objects, and downstream deduction match.**
- **A partial external result is diagnostic:** explain the role of extra hypotheses before trying to use it.
- **The final target statement stays complete and faithful to the input.**
- **External proof dependencies carry their complete statement and source identifiers when available.**
- **All important progress and failure information is persisted under one stable problem ID.**

## Fast smells

| Smell | Likely problem | Recovery |
|---|---|---|
| same plan keeps reappearing | failure memory not influencing planning | query/synthesize failed paths |
| many searches, little proof progress | retrieval overuse | switch to examples, counterexamples, direct reasoning |
| “known theorem” with no context | black-box literature use | read source proof + definitions |
| verifier keeps finding local gaps | draft assembled too early or dependency order weak | rebuild supporting lemmas first |
| recursive agents repeat each other | poor plan diversity/shared context | assign distinct screened plans + shared stuck points |
| assumptions never appear in proof | possible missing argument or redundant input | audit each assumption explicitly |
| proof claims success without verified file | acceptance boundary bypassed | run strict verifier before promotion |
