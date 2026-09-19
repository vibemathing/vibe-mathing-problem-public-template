# Failure modes and recovery

| Failure mode | Early signal | Diagnostic | Recovery |
|---|---|---|---|
| Spurious correlations / shortcut learning | large drop after paraphrase, distractor, or number/name change | SVAMP/GSM-Symbolic-style perturbations | strengthen semantic representation; train/evaluate on counterfactual variants |
| Metric mismatch / path invalidity | answer correct while steps fail | process verifier, execution, proof compilation | report process metric alongside answer accuracy |
| Benchmark contamination / saturation | near-ceiling legacy scores, older test >> fresh test | live/fresh benchmark; date split | shift to MathArena/frontier/robustness/live settings |
| Reward hacking in RLVR | reward rises while human/formal validity stalls | adversarial verifier tests; alternate checkers | improve reward/verifier, constrain exploitable channels |
| Multimodal non-use | model improves when image is removed | image ablation / perturbation | stronger grounding, symbolic geometry formalization |
| Hallucinated derivation/proof | fluent unsupported steps | executable/symbolic/formal check | localize invalid step and regenerate under verifier feedback |
| Language/localization gaps | sharp performance drop outside English | multilingual matched tests | multilingual training/evaluation and locale-specific error analysis |
| Multi-agent correlated error | fast unanimous consensus, repeated shared premise | independent first-pass answers; heterogeneous agents/tools | enforce diversity, external verifier, dissent role, termination rule |
| Multi-agent non-termination | endless debate/refinement | iteration and novelty counters | cap rounds; switch to checker or escalate to human/tool |
| False rigor from formatting | polished LaTeX masks invalid logic | strip formatting; check claims/execution | validate semantics, not presentation |
| Compute/access bias | gains require huge search/TTRL budget | report compute/search budget | compare under equal budget; separate capability from resource scaling |
| Stale snapshot | user asks for later-than-July-2026 latest/SOTA | compare request date to source snapshot | retrieve fresh evidence; do not extrapolate |

## Stop conditions

Return “insufficient to judge” when the claim needs a paper-internal detail absent from the source index, a current result beyond the snapshot, or a formal/domain check that has not been run. The skill should surface the missing evidence instead of inventing it.
