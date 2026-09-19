# Benchmark and evaluation guide

## Snapshot warning

The source is dated July 2026. Its benchmark table mixes controlled results, live/provisional results, corrected variants, and different inference budgets. Preserve those qualifiers.

## Routing by evaluation need

- **Classical MWP / robustness**: AI2/AddSub, SingleEQ, Alg514, MAWPS, ASDiv, Math23K, AQuA, MathQA, SVAMP, ParaMAWPS, GSM-Symbolic.
- **Competition / olympiad**: GSM8K, MATH, OlympiadBench, Omni-MATH, AIME-derived evaluations, IMO-ProofBench.
- **Multilingual**: MGSM, HAWP, ArMATH, CMATH, MathOctopus, HRM8K, PatiGonit, BMWP, PolyMath, MathMist, M3Kang.
- **Tabular**: TabMWP, FinQA, TAT-QA, MultiHiertt, MultiTabQA.
- **Geometry / multimodal**: GEOS family, Geometry3K, GeoQA/GeoQA+, UniGeo, PGPS9K, MathVista, MathVerse, MATH-Vision, MV-MATH, We-Math.
- **Formal proving**: MiniF2F, ProofNet, PutnamBench, Lean Workbook, DeepTheorem.
- **Frontier / live**: FrontierMath, HLE, MathArena, GPQA-family, LiveBench.
- **Verifier/process data**: PRM800K, Math-Shepherd, OmegaPRM, MetaMathQA, NuminaMath.
- **Scientific adjacent**: SciBench, SciEval, ScienceQA.

## Saturation implications from the source

- GSM8K and MATH are described as effectively saturated by 2025, so use them as regression/coverage checks rather than decisive frontier evidence.
- AIME, FrontierMath, PutnamBench, and formal proving show more discrimination in the reasoning-model era, but protocols differ sharply.
- Formal proving improved rapidly, yet results can depend on benchmark variant, search budget, and TTRL; compare like with like.

## Required report fields

For every benchmark result, record:

1. exact dataset/split/version,
2. metric (accuracy, Pass@1, Pass@k, proof compilation, etc.),
3. sampling/search budget,
4. tool/verifier access,
5. test-time RL or repeated-search budget,
6. whether the result is controlled, self-reported, live, or provisional,
7. contamination/freshness status if known.

## Process-sensitive evaluation

When final-answer accuracy can hide invalid reasoning, report at least one process-sensitive measure: proof compilation, step verification, perturbation robustness, path validity/optimality, or tool execution success.
