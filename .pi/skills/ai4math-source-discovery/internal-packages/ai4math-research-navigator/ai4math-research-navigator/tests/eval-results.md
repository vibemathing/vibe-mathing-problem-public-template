# Eval results

Evaluation method: manual application of the packaged routing rules plus live smoke queries against `scripts/query_catalog.py`. No claim is made that a separate model instance executed these cases.

| ID | Type | Verdict | Observed route / behavior |
|---|---|---|---|
| T01 | trigger | PASS | informal + cross-cutting; multilingual datasets + robustness + benchmark fit |
| T02 | negative trigger | PASS | excluded as ordinary math solving |
| T03 | method selection | PASS | formal; retrieval → generation/search → kernel compile → compiler repair |
| T04 | method selection | PASS | multimodal; diagram grounding + ablation/perturbation + symbolic verification |
| T05 | method selection | PASS | discovery; candidate search → domain evaluation → counterexample search → formal/expert checks |
| T06 | method selection | PASS | training; reward source first, then PRM/outcome/RL family with reward-hacking audit |
| T07 | failure recovery | PASS | localize failing Lean goal, retrieve lemmas, regenerate smallest region, recompile |
| T08 | failure recovery | PASS | correlated-agent error; independent proposals, diversity, external checker |
| T09 | trigger | PASS | saturation warning; migrate beyond GSM8K to harder/live/frontier/process-sensitive evidence |
| T10 | freshness | PASS | July 2026 cutoff detected; fresh retrieval required |
| T11 | negative trigger | PASS | excluded as unrelated creative writing |
| T12 | trigger | PASS | literature navigation; catalog smoke query returned ToRA, PAL, PoT, process-feedback/PRM records |

## Catalog smoke tests

- `tool integrated process verification` returned ToRA, PAL, PoT, Chameleon, process/outcome feedback, OmegaPRM, and related records.
- `Lean compiler repair retrieval` returned LeanDojo, APOLLO, Lean Copilot, Baldur, Lean-STaR, PDA, and Lean Workbook.
- `multilingual benchmark Korean Bengali Arabic` returned ArMATH, HRM8K, PatiGonit, BMWP, MGSM, and other multilingual rows.

All required eval categories passed.
