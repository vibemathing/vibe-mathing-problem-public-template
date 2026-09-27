# AI4M Decision Cheatsheet

## First decision: what is blocked?

| Bottleneck | First move | Evidence standard |
|---|---|---|
| Cannot find/learn relevant theory | knowledge navigation / library search | source relevance + assumption match |
| Need a proof or correctness guarantee | formalize + verifier | checker pass or explicit human proof audit |
| Need a new pattern/conjecture | special-purpose data-driven discovery | interpretable signal + mathematical testing |
| Need repeated multi-step reasoning | agent prototype | checkable intermediate outputs |
| Need to improve an existing candidate | evolve-style search | trustworthy quantitative evaluator |
| Have a checked proof but little insight | understanding extraction | explanation of mechanism + connections |

## Special-purpose vs general/formal route

- Narrow mathematical bottleneck + usable data + strong domain insight → **special-purpose tool**.
- Reusable class of reasoning/formalization tasks + strong engineering interest → **general/formal model**.
- Need both discovery and certainty → **discover with special tool, certify with formal route**.

## Formal route decision tree

1. Need strict correctness?
   - Yes → formalize.
2. Formalization blocked?
   - Can't find existing facts → semantic mathlib search.
   - Informal-to-formal translation is slow → assisted autoformalization + semantic audit.
3. Proof blocked?
   - Use proof search/completion or a Lean-oriented prover/tactic.
4. Candidate produced?
   - Run the checker; feed errors back into the next iteration.

## Agent eligibility

Use an agent early when all are mostly true:
- strong base model;
- multi-step task;
- useful tools/retrieval exist;
- intermediate states are observable;
- success can be checked.

If rigor is non-negotiable, add a formal verifier to the critical path.

## Evolve eligibility: 3-gate rule

Proceed only if:
- **Goal**: clear;
- **Score**: quantifiable and trustworthy;
- **Seed**: usable initial solution.

Missing goal → clarify objective. Missing score → build evaluator. Missing seed → create baseline first.

## Evidence ladder

`model correlation < interpreted pattern < tested conjecture < convincing informal proof < machine-checked formal proof`

Do not report a result at a stronger level than the evidence supports.

## Failure smells

| Smell | Likely problem | Recovery |
|---|---|---|
| high predictive score, no mathematical story | artifact/confounder | inspect features/data assumptions |
| Lean work dominated by searching names | library navigation bottleneck | semantic search / reuse abstractions |
| formal statement compiles but feels wrong | semantic drift | map each assumption/conclusion manually |
| agent repeats similar attempts | weak checkpoints/termination | smaller goals + evaluators + retry cap |
| evolve loop improves score but worsens mathematics | evaluator gaming | independent metric + constraint audit |
| verified proof teaches nothing | automation stopped too early | extract invariants, mechanism, generalizations |

## Final check

Goal understood → method prerequisites satisfied → evidence level labeled → failure route included → rigor checked → insight preserved.
