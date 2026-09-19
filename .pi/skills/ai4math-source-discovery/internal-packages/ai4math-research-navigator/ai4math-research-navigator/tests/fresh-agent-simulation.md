# Fresh-agent simulation

Assume an agent has never read the source and only sees this skill package.

## Simulation A — Lean proof system
Prompt: “Design a Lean prover with retrieval and automatic repair.”
Expected behavior: route to formal; choose retrieval + generation/search + kernel compile + compiler-guided repair; refuse to call an informal proof valid without kernel acceptance; report benchmark protocol if evaluated on MiniF2F/PutnamBench.

## Simulation B — Geometry VLM
Prompt: “Our geometry model scores well, but I suspect it ignores diagrams.”
Expected behavior: route to multimodal; separate text/diagram parsing; propose diagram ablation/perturbation; add symbolic grounding or geometry solver; use MathVerse/geometry benchmark family where appropriate.

## Simulation C — Frontier benchmark claim
Prompt: “We beat 98% on GSM8K; can we claim frontier mathematical reasoning?”
Expected behavior: flag source-described saturation; keep GSM8K as regression evidence; add harder/live/frontier/process-sensitive/formal evaluations; require protocol and contamination notes.

## Simulation D — September 2026 update
Prompt: “Give me the newest September 2026 AI4Math SOTA.”
Expected behavior: identify July 2026 source cutoff and require fresh external retrieval; never synthesize a later result from the packaged snapshot.

## Simulation result
The routing file, benchmark guide, recovery table, and snapshot boundary are sufficient for a fresh agent to select a method, find supporting references, and know when the skill alone is insufficient.
