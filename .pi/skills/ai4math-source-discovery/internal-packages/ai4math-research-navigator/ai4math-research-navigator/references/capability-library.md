# Atomic Capability Library

Each capability is a reusable behavior. `SOURCE_DERIVED` means directly grounded in the uploaded index; `STRUCTURAL_SYNTHESIS` means an engineering composition of source-grounded ideas.

## CAP-01 — Axis Router
- **Purpose**: classify an AI4Math request before selecting methods.
- **Trigger**: any system-design, literature, benchmark, or evaluation request.
- **Inputs**: target task, expected artifact, modality, correctness requirement.
- **Procedure**: identify informal / multimodal / formal / discovery; add cross-cutting flags.
- **Decision**: if multiple axes apply, route by the final artifact/verifier.
- **Output**: axis + rationale + downstream references.
- **Failure**: axis chosen from model name instead of task.
- **Fallback**: classify by artifact and verifier.
- **Validation**: task, artifact, verifier all align.
- **Provenance**: SOURCE_DERIVED — “The Four Axes”.

## CAP-02 — CGV Pipeline Designer
- **Purpose**: force explicit comprehension, generation, and verification stages.
- **Trigger**: system/pipeline design.
- **Inputs**: problem representation, generator, verifier.
- **Procedure**: specify C, G, V; define feedback loops and failure signals.
- **Output**: staged pipeline.
- **Failure**: verification is only a final cosmetic check.
- **Fallback**: move verifier signals earlier into selection/training.
- **Validation**: every stage has inputs/outputs and a checking mechanism.
- **Provenance**: SOURCE_DERIVED — TL;DR CGV triad.

## CAP-03 — Verifier / Supervision Selector
- **Purpose**: match evidence strength to artifact.
- **Trigger**: correctness, reward, or validation design.
- **Procedure**: choose answer parser → process/outcome verifier → symbolic/domain checker → proof kernel → domain + formal + expert audit.
- **Decision**: use the strongest practical verifier that directly checks the artifact's claim.
- **Failure**: treating model self-critique as an independent verifier.
- **Fallback**: add external executable/symbolic/formal checks.
- **Validation**: verifier failure is observable and changes system behavior.
- **Provenance**: SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — supervision ladder, four-axis verifier table, formal/discovery sections.

## CAP-04 — Informal Method Selector
- **Purpose**: choose among prompting, decomposition, tools, self-improvement, reasoning models, RL, and multi-agent methods.
- **Trigger**: text-only math reasoning design.
- **Procedure**: diagnose bottleneck (understanding, computation, search, verification, training) and route to the matching family.
- **Failure**: selecting a fashionable method without identifying the bottleneck.
- **Fallback**: baseline with simple decomposition + executable verification, then escalate.
- **Validation**: method addresses the identified failure mode.
- **Provenance**: SOURCE_DERIVED — Sections I–II.

## CAP-05 — Benchmark Selector
- **Purpose**: choose evaluation data that matches capability and difficulty.
- **Trigger**: benchmark/evaluation planning.
- **Procedure**: match axis, difficulty, modality, language, formality, contamination risk, and saturation level.
- **Output**: benchmark set + rationale.
- **Failure**: relying on saturated GSM8K/MATH alone for frontier claims.
- **Fallback**: add harder/live/frontier/robustness/formal benchmarks.
- **Validation**: each benchmark maps to a claim.
- **Provenance**: SOURCE_DERIVED — benchmark saturation + Section VI.

## CAP-06 — Metric / Protocol Normalizer
- **Purpose**: prevent invalid leaderboard comparisons.
- **Trigger**: comparing reported scores.
- **Inputs**: split, Pass@k, search budget, TTRL, corrected variants, self-reported/live status.
- **Procedure**: enumerate protocol differences before ranking systems.
- **Failure**: treating incomparable protocols as a single scale.
- **Fallback**: report results separately or normalize under a common protocol.
- **Validation**: comparison table includes protocol fields.
- **Provenance**: SOURCE_DERIVED — benchmark notes + failure-mode metric mismatch.

## CAP-07 — Robustness & Contamination Auditor
- **Purpose**: test whether accuracy reflects reasoning rather than shortcuts or leakage.
- **Trigger**: high benchmark scores, suspicious gains, or deployment reliability questions.
- **Procedure**: paraphrase/reorder/distractor perturbations; symbolic substitutions; live/fresh tests; process-sensitive metrics.
- **Failure**: only in-distribution accuracy reported.
- **Fallback**: add SVAMP/GSM-Symbolic-style probes and live benchmarks.
- **Validation**: performance remains stable under meaning-preserving perturbations or degradations are explained.
- **Provenance**: SOURCE_DERIVED — Section I robustness + Section VII.

## CAP-08 — Multimodal Geometry Pipeline Designer
- **Purpose**: design systems that truly use diagrams and geometry structure.
- **Trigger**: geometry or visual math.
- **Procedure**: parse text/diagram separately; ground entities; formalize constraints; run symbolic/neural reasoning; test diagram ablation; verify steps.
- **Failure**: model gains when the diagram is removed.
- **Fallback**: strengthen grounding/formalization or add a symbolic geometry solver.
- **Validation**: diagram perturbations have sensible, explainable effects.
- **Provenance**: SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — Section III + MathVerse failure note.

## CAP-09 — Formal Proving Pipeline Designer
- **Purpose**: build Lean/Coq/Isabelle proving workflows.
- **Trigger**: theorem formalization, proof generation, or proof repair.
- **Procedure**: formalize statement; retrieve library context; generate/search; compile; localize compiler errors; repair; recompile.
- **Failure**: fluent proof text without kernel acceptance.
- **Fallback**: reduce to failing subgoal, retrieve lemmas, regenerate locally.
- **Validation**: proof assistant accepts the artifact.
- **Provenance**: SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — Section IV.

## CAP-10 — Discovery Workbench Designer
- **Purpose**: structure AI-assisted open-problem research.
- **Trigger**: new constructions, bounds, algorithms, or open conjectures.
- **Procedure**: formalize objective; generate candidates; domain-evaluate; search for counterexamples; formalize important claims; expert-audit significance.
- **Failure**: novelty rhetoric outruns validation.
- **Fallback**: downgrade claim and strengthen domain/formal/expert gates.
- **Validation**: correctness, novelty, and significance have separate evidence.
- **Provenance**: SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — Section V and four-axis discovery verifier.

## CAP-11 — Literature Navigator
- **Purpose**: locate indexed systems, datasets, methods, and surveys.
- **Trigger**: “find papers/resources about …”.
- **Procedure**: query `catalog.jsonl`; filter by section/subsection/year; return source links and source line provenance.
- **Failure**: inferring paper details from titles.
- **Fallback**: retrieve the actual linked paper for deeper claims.
- **Validation**: every returned item maps to a catalog record.
- **Provenance**: IMPLEMENTATION_DECISION over SOURCE_DERIVED catalog.

## CAP-12 — Failure Diagnostician & Recovery Router
- **Purpose**: respond when the first method fails.
- **Trigger**: unstable results, rejected proofs, false consensus, modality failure, or stale evidence.
- **Procedure**: identify failure class → choose diagnostic → choose alternate route → re-validate.
- **Output**: diagnosis + next action + stop condition.
- **Failure**: repeating the same method with more tokens.
- **Fallback**: switch verifier, representation, benchmark, or method family.
- **Validation**: recovery changes at least one causal component.
- **Provenance**: SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — Section VII plus method sections.

## CAP-13 — Training / Reward Strategy Selector
- **Purpose**: choose process/outcome supervision and RL family based on available feedback.
- **Trigger**: training a math reasoner.
- **Procedure**: decide whether reward can be checked at final answer, intermediate step, preference pair, or formal/domain execution; then select compatible methods/data.
- **Failure**: reward hacking or weak proxy optimization.
- **Fallback**: strengthen verifier and diversify checks before scaling RL.
- **Validation**: reward correlates with task-valid evidence under adversarial probes.
- **Provenance**: SOURCE_DERIVED — process/outcome reward models + RL algorithms + Section VII reward hacking.

## CAP-14 — Dataset Locale / Modality Selector
- **Purpose**: choose multilingual, tabular, geometry, formal, frontier, or adjacent-science data.
- **Trigger**: domain transfer or specialized evaluation.
- **Procedure**: filter by language/modality/representation/level; add a robustness set.
- **Failure**: English text-only benchmarks used for multilingual/multimodal claims.
- **Fallback**: use the corresponding Section VI families.
- **Validation**: evaluation set matches deployment distribution.
- **Provenance**: SOURCE_DERIVED — Section VI.
