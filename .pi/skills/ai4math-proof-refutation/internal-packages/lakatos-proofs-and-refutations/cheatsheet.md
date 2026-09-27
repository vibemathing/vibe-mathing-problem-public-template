# Cheatsheet

## Counterexample Router

| Observation | Meaning | Move |
|---|---|---|
| main claim false + lemma false | localized failure | Rule 2: lemma incorporation |
| main claim false + all lemmas true | incomplete proof analysis | expose hidden lemma; restore falsity transfer |
| main claim true + lemma false | proof too narrow/weak | Rule 4: replace lemma or deepen proof |
| theorem survives but example strains explanation | heuristic counterexample | Rule 5: seek deeper theorem |

## Fast Decision Rules

- **Have a conjecture?** Prove and refute it in parallel; list non-trivial lemmas.
- **Adding a restriction?** Demand the proof step that motivates it. No proof link → mark as provisional exception-barring.
- **Saying “that is not really an X”?** Suspect monster-barring; record the definition change and retest.
- **Recounting/reinterpreting the counterexample?** Suspect monster-adjusting; require independent structural support.
- **Local failure only?** Preserve the conjecture; repair the lemma before shrinking the theorem.
- **Patches keep shrinking scope?** Switch to a deeper proof or deductive guess.
- **Two proofs disagree on conditions?** Compare scope, depth, concepts generated, and counterexample productivity.
- **Formal proof checks, application fails?** Audit translation/model assumptions before deduction.
- **Definition looks magical?** Find its proof-ancestor: which failed step does it repair?
- **Counterexample known but flaw unknown?** Expand dependencies/quantifiers; counterexample discovery and hidden-lemma discovery are separate tasks.

## Smells

| Smell | Likely diagnosis |
|---|---|
| ever-longer “real X means…” clauses | monster-barring / semantic drift |
| safe but unrelated condition | exception-barring |
| theorem saved by unusual counting convention | monster-adjusting |
| conclusion fails, explicit proof untouched | hidden lemma |
| correct theorem, failed proof | local-only counterexample |
| formal certainty claimed for messy source world | translation-certainty leakage |
| textbook definition has no visible motivation | deleted proof-ancestor |

## Output Skeleton

`claim → lemma map → counterexample class → method diagnosis → revised claim/proof → discriminating next tests → remaining scope limits`
