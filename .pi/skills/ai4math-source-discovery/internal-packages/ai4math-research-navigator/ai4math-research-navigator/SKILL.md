---
name: ai4math-research-navigator
description: Route and design AI-for-mathematical-reasoning research from a July 2026 survey-index snapshot. Use for choosing methods, verifiers, datasets, benchmarks, evaluation protocols, formal-proving pipelines, multimodal-geometry systems, reasoning-model/RL strategies, mathematical-discovery workflows, failure diagnostics, or indexed literature. Do not use merely to solve an ordinary math exercise unless the user asks about research methodology, evaluation, system design, literature, or proof-tool architecture.
---

# AI4Math Research Navigator

Operational research skill distilled from the uploaded companion index for *Artificial Intelligence for Mathematical Reasoning: An Integrated Survey of Language Models, Neuro-symbolic Systems, and Verified Discovery*.

## Scope and freshness

- Source snapshot: **July 2026**. Treat later “latest/SOTA/current” claims as requiring fresh external evidence.
- The uploaded archive contains a companion `README.md`, three knowledge-bearing figures, and an MIT license. It does **not** contain the full linked survey paper or the 238 linked papers. Never imply those external papers were read by this skill compiler.
- Use the source catalog as a routing and evidence index. When a claim depends on a linked paper's internal details beyond the source annotation, retrieve that paper before asserting them.

## Fast route

1. **Identify the goal**: literature navigation, system design, training, benchmark selection, evaluation, failure diagnosis, formalization/proving, multimodal geometry, or discovery.
2. **Classify the task** using `references/taxonomy-routing.md`:
   - informal text-only,
   - multimodal & geometry,
   - formal proving,
   - mathematical discovery,
   - plus cross-cutting evaluation/training concerns.
3. Apply **CGV**: specify how the system performs **Comprehension → Generation → Verification**. Verification must be designed at the same time as generation, not bolted on at the end.
4. Pick a method family from `references/capability-library.md` and `references/method-dependency-graph.md`.
5. Pick a verifier/supervision level appropriate to the artifact:
   - answer parser / exact match,
   - process or outcome verifier,
   - symbolic/domain solver,
   - proof-assistant kernel,
   - domain evaluator + formal check + expert audit for discovery.
6. Select datasets/benchmarks using `references/benchmark-guide.md`. Always state protocol details that affect comparability (for example Pass@1 vs Pass@k, tree search, TTRL, corrected variants, or live/provisional leaderboards).
7. Run failure checks from `references/failure-modes.md` before concluding.
8. For paper/resource lookup, run `python scripts/query_catalog.py --query "<terms>"` or search `references/catalog.jsonl`.

## Routing rules

### Informal text-only
Use for MWPs, competition QA, reasoning-model design, prompting, tool use, reward modeling, RL, or multi-agent reasoning. Start with semantic decomposition when problem structure is fragile; add executable tools when arithmetic/symbolic execution is a bottleneck; add process verification when final-answer accuracy can hide invalid paths.

### Multimodal & geometry
Separate **diagram comprehension** from **symbolic/geometric reasoning**. Test whether the model actually uses the diagram. Prefer a formalized constraint representation or symbolic geometry layer when correctness matters.

### Formal proving
Treat kernel acceptance as the correctness gate. Typical route: statement formalization → library retrieval → tactic/whole-proof generation → proof search → compile → compiler-guided repair. Never accept fluent informal reasoning as proof validity.

### Mathematical discovery
Separate candidate generation from validation. Use program/search agents to propose constructions, then evaluate with domain-specific tests, formalize important claims where possible, and reserve expert audit for research significance and hidden assumptions.

## Failure recovery

- **Answer correct, reasoning suspect** → add step/process verification or perturbation tests.
- **Benchmark looks saturated** → move to harder, live, frontier, robustness, multilingual, or process-sensitive evaluation.
- **Results are not comparable** → normalize protocol, split, compute budget, and verifier/search settings before ranking methods.
- **Diagram reasoning collapses** → compare with diagram-removed/perturbed conditions; strengthen multimodal parsing or symbolic grounding.
- **Lean/Coq/Isabelle proof fails** → use compiler feedback, retrieve missing lemmas, localize the failing subgoal, regenerate only the affected segment, then recompile.
- **Multi-agent consensus forms too easily** → force independent proposals, diversify roles/models/tools, and validate against an external checker.
- **Discovery candidate is exciting but weakly validated** → downgrade the claim; run domain evaluation, adversarial search, formal verification where feasible, and expert review.
- **Source snapshot is stale for the question** → explicitly require fresh retrieval instead of extrapolating beyond July 2026.

## Progressive loading

Load only what the task needs:

- orientation/routing → `references/taxonomy-routing.md`
- operational methods → `references/capability-library.md`
- dependencies and escalation → `references/method-dependency-graph.md`
- evaluation/data → `references/benchmark-guide.md`
- risk/recovery → `references/failure-modes.md`
- source-wide structure → `references/book-map.md`, `references/concept-graph.md`
- literature lookup → `references/catalog.jsonl`, `scripts/query_catalog.py`
- provenance → `provenance/provenance_map.json`

## SELF_CHECK

Before finalizing an answer or plan, verify all of the following:

- The user's real research goal and target artifact are explicit.
- The task axis is correct; cross-axis dependencies were not ignored.
- Comprehension, generation, and verification are all specified.
- Method prerequisites and compute/tool assumptions are stated.
- The benchmark measures the intended capability and is not treated as decisive when saturated or contaminated.
- Reported comparisons use compatible protocols.
- Robustness, hallucination, localization, multimodal grounding, reward hacking, and correlated-agent errors were considered where relevant.
- Any formal proof claim is tied to proof-assistant acceptance.
- Any discovery claim separates correctness from novelty/significance.
- Claims beyond the July 2026 snapshot are marked for fresh retrieval.

## Output contract

For substantive research-design requests, return:

1. **Task classification** and why.
2. **Recommended pipeline** in executable stages.
3. **Verifier/evaluation plan** with benchmark protocol.
4. **Failure signals and recovery path**.
5. **Relevant indexed resources** with source locations/links when useful.
6. **Confidence boundary**: what comes from the snapshot, what is synthesis, and what requires fresh evidence.
