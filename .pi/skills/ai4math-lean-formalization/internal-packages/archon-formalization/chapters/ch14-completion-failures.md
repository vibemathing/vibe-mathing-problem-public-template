# Chapter 14: Completion Gates and Failure Playbook

## Core Idea
A credible Archon success state requires executable proof evidence, structural blueprint integrity, and absence of hidden assumptions. Failure recovery begins by classifying the blocker.

## Completion Gate
Before accepting COMPLETE for the relevant scope:
1. project/modules build successfully;
2. target sorries are gone;
3. axiom sweep shows no `sorryAx` laundering or unacceptable new axioms;
4. earned `\leanok` state is synchronized from compilation rather than prose;
5. blueprint doctor has no unresolved structural failures for the completed cone;
6. Lean↔blueprint coverage is reconciled;
7. review/task logs do not reveal skipped load-bearing obligations.

If the state says COMPLETE while sorries remain, Archon resets to the prover stage. Treat this as a safety feature.

## Failure Classifier
| Failure | First response | Escalation |
|---|---|---|
| theorem too large / no proof movement | fine-grained decomposition | effort-breaker / strategy rewrite |
| guessed library lemma absent | verify search result | local helper / mathlib-build |
| local import fails / blocked dependency | fix earliest blocking file | shrink objective frontier |
| blueprint wrong/incomplete | repair chapter/DAG | fresh blueprint/strategy audit |
| repeated helpers, flat sorry count | mark churn | switch route/model/mode |
| crash mid-iteration | `--resume` | inspect phase metadata/logs |
| bad refactor/timeline | inner-git branch from known-good commit | re-plan structural change |
| provider/auth/quota | isolate provider issue | switch harness/backend or resume after quota |
| protection conflict | respect protected surface | user explicitly changes protection |
| source claim uncertain | inspect actual reference | revise mathematics/DAG |

## Stop Conditions
Return “insufficient evidence” when required source material, toolchain output, or project state is unavailable. Do not fabricate completion, API existence, or proof validity.

## Cross-Check
For a high-risk completion, inspect both directions: does every intended mathematical claim have Lean realization, and does every significant Lean helper have blueprint/provenance representation? Then run the deterministic build/doctor/axiom gates.

## Source Provenance
Primary: loop command/phases, plan/review prompts, bundled Lean4 quality gates, axiom/sync/doctor tests, branch/resume tests.

## Frameworks Introduced
- **Mechanical completion gate**: success requires builds, no unresolved target sorries, acceptable axiom footprint, synchronized blueprint proof state, structural health, and coverage reconciliation.
- **Earliest-cause recovery**: fix the lowest/earliest layer that invalidates downstream work rather than retrying symptoms.
- **Honest insufficiency**: when required state/source/tool output is absent, return an explicit uncertainty instead of inventing a verdict.

## Key Concepts
- **False completion**: stage metadata says COMPLETE while repository evidence contradicts it.
- **Axiom laundering**: apparent closed proof depends on `sorryAx` transitively.
- **Recovery fork**: inner-git branch from a known-good historical commit.
- **Infrastructure gap**: precise missing reusable theorem/API after verified search and local attempt, distinct from “proof is hard”.

## Mental Models
- Completion is a **conjunction of invariants**, not a confidence score.
- Recovery is a **causal graph**: state → dependency/build → blueprint/math → proof mode → library/provider/strategy. Downstream retries before upstream repair are usually waste.

## Anti-patterns
- **Declare success from a task result**: only repository checks can establish completion.
- **Hide a sorry behind a theorem**: axiom sweep should expose transitive laundering.
- **Retry after crash without checking state**: can duplicate or overwrite a recoverable in-flight iteration.
- **Escalate model strength for a false theorem**: mathematical impossibility needs backtracking.

## Worked Example
`PROGRESS.md` says COMPLETE, but a new helper reintroduced `sorry` and a blueprint chapter still has stale `\leanok`. The loop counts sorries, resets stage to prover, removes/updates markers through sync, and review records the regression. If the helper arose from a bad refactor, inspect inner-git commits and fork the last known-good point; if the helper is mathematically necessary, keep the new route and prove/decompose it. Completion returns only after build, sorry, axiom, doctor, and coverage gates agree.

## Key Takeaways
1. Completion is mechanically earned.
2. Classify failure before choosing recovery.
3. Repair upstream causes before downstream retries.
4. Preserve explicit uncertainty when evidence is missing.

## Connects To
- **Ch 04**: stage machine and deterministic phases.
- **Ch 06**: proof/axiom verification.
- **Ch 09**: rollback and protection.
- **Ch 13**: evidence needed to diagnose the failure class.
