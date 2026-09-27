# METHOD_DEPENDENCY_GRAPH

## Informal reasoning

`problem parse -> semantic decomposition -> candidate reasoning -> optional tool execution -> answer/process verification -> robustness perturbation`

Escalate from plain prompting to tools when computation is brittle; to process verification when lucky final answers are plausible; to reasoning/RL or search when single-pass generation is the bottleneck.

## Multimodal & geometry

`text parse + diagram parse -> entity/relation grounding -> geometric constraint representation -> construction/proof search -> symbolic or stepwise verification`

If the system improves when the diagram is removed, treat that as a grounding failure and test modality dependence explicitly.

## Formal theorem proving

`informal/formal statement -> autoformalization (if needed) -> library retrieval -> tactic/whole-proof proposal -> proof search -> kernel compilation -> compiler-guided repair loop`

Kernel acceptance is a hard dependency for proof correctness. Retrieval and repair are supporting methods, not substitutes for compilation.

## Mathematical discovery

`problem formalization -> candidate generator/program search/agent workbench -> domain evaluator -> adversarial/counterexample search -> formal verification where feasible -> expert audit of novelty/significance`

A candidate can be correct yet uninteresting, or novel-looking yet invalid. Keep correctness and research significance as separate gates.

## Evaluation

`capability claim -> benchmark fit -> protocol choice -> compute/search budget -> verifier definition -> metric -> robustness/contamination checks -> comparable report`

Do not rank systems from incomparable Pass@k, tree-search, corrected-variant, TTRL, or self-reported live-leaderboard results without normalization.
