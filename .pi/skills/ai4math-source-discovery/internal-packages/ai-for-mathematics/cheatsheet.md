# AI for Mathematics — Decision Cheatsheet

## Route by objective

| Situation | Prefer | Require before trusting output | Switch when |
|---|---|---|---|
| Hidden relation in labeled invariant data | supervised predictor + interpretability | held-out accuracy + stable feature importance + stress test | model has no generalization or explanations are unstable |
| Discrete object with exact sequential moves | RL / deep CEM | exact scorer/terminal check | policy collapses or representation hides useful structure |
| Good solutions share global motifs and local repair is strong | PatternBoost | exact repair/scorer | elite objects show little shared pattern |
| Candidate is naturally executable code | program evolution | hardened evaluator/tests | evaluator is gameable or search homogenizes |
| Formal theorem | LLM/policy-guided proof search | proof-assistant kernel acceptance | formalization/library bottleneck dominates search |
| Open-ended construction with external checker | generator–verifier agent | independent final verifier | verifier feedback repeats with no plan change |
| Low-dimensional regular PDE | FDM/FEM/FVM/spectral | grid/mesh/order convergence | geometry/dimension/inverse structure becomes the bottleneck |
| Inverse/high-dimensional/data-fusion PDE | PINN or hybrid | independent points + physics checks + classical/reference comparison | loss falls without accuracy or conditioning is poor |

## Fast method tells

- **High-dimensional predictive pattern + interpretable features** → use ML to *locate* a conjecture, then do mathematics.
- **Cheap exact verifier** → spend model capacity on exploration; keep verification independent.
- **Easy inverse construction, hard forward search** → generate synthetic demonstrations for policy training.
- **Repeated near-optimal motif** → parameterize the motif; it may encode the missing human theorem/construction family.
- **Conservation is the scientific contract** → favor FVM or enforce conservation explicitly.
- **Smooth solution + simple domain + extreme accuracy** → spectral methods are a strong baseline.
- **Complex geometry + standard variational PDE** → FEM baseline first.
- **PINN training loss looks excellent but independent residual/solution error does not** → suspect discretization/generalization or loss imbalance.

## Validation gates

1. **Data gate** — separate train/validation/test; keep constructed stress cases outside tuning.
2. **Representation gate** — check that encoding preserves symmetries, constraints, and meaningful neighborhoods.
3. **Search gate** — log diversity, not only best score; detect collapse and evaluator exploitation.
4. **Mathematical gate** — convert model output into a precise proposition/object/program.
5. **Verifier gate** — exact/formal checker where possible; otherwise independent numerical/empirical checks.
6. **Reproducibility gate** — preserve code, data provenance, model/version, seeds, evaluator, hyperparameters, and successful trajectory.

## Failure smells

| Smell | Likely cause | Next action |
|---|---|---|
| Great training score, weak held-out behavior | overfit/leakage | restore clean holdout; simplify/regularize |
| Feature importance changes across runs | unstable explanation | ablate/retrain; do not promote to conjecture |
| RL reward rises but objects are invalid | reward misspecification | put hard validity in verifier/environment |
| Evolution finds bizarre high scores | evaluator exploit | adversarial tests + invariant checks |
| Formal search visits huge shallow tree | weak tactic prior/retrieval | improve formal context and lemma selection |
| LLM keeps repairing the same failure | no memory or wrong decomposition | persist diagnostics; revise plan granularity |
| PINN satisfies BC/IC but violates PDE | loss-term imbalance | rebalance by magnitude/gradient; resample residuals |
| PINN misses shocks/high frequency | spectral bias/sampling | adaptive dense sampling, feature mapping, decomposition |

## Numeric/default cues from the book

- Momentum commonly uses `β ≈ 0.9` as a starting point.
- Deep CEM elite retention is described around **5–20%**.
- PINN loss terms should start at comparable *effective* scales when practical; all-ones weights can be misleading.
- Increasing residual-point density should be treated like a convergence study, not a cosmetic training tweak.
