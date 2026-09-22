# AI4Math Skill consolidation map

This file records the conceptual consolidation behind the ten configured project Skills. It is not a redistribution of the audited source packages.

## Boundary

- The review set contains **31 packages from 29 source families**; two pairs are duplicate-source variants.
- The audited source packages remain non-publication inputs unless their own source and license gates pass.
- The public Skill suite contains the restored complete `solve` operator library plus nine independently written operational abstractions: decision rules, failure semantics, evidence boundaries, and reusable workflows. It does not copy chapters, examples, or package text from a source whose redistribution status is unresolved.
- A source being reviewed here does not make it installed, activated, trusted, evidence-capable, or verifier-admitted.
- The canonical research actor chooses mathematical routes. Skills expose capabilities; they do not prescribe a mandatory route or phase plan.

## Internal-package architecture

All 31 audited packages have one primary owner among the eight top-level mathematical Skills. A complete package tree is physically bundled once under that owner's `internal-packages/` directory and may be referenced through repository-relative paths by other top-level Skills. Redistribution rights remain on HOLD even though the repository is self-contained. Internal packages are inert source material and are never additional Pi entries.

## Target capability layers

| Target Skill | Consolidated responsibility |
|---|---|
| `solve` | cross-domain operator catalog, bounded method selection, outcome logging, switching and stopping |
| `ai4math-source-discovery` | statement/source identity, research navigation, retrieval, applicability and provenance |
| `ai4math-modeling-derivation` | definitions, representations, abstraction, invariant-preserving translation and derivation audits |
| `ai4math-proof-refutation` | proof search, counterexample analysis, conjecture repair, proof obligations and failed-route memory |
| `ai4math-bounded-computation` | exact/symbolic/numeric experiments, falsification, resource bounds and replayable observations |
| `ai4math-lean-formalization` | informal-to-Lean translation, theorem search, proof engineering, diagnostics and kernel-facing checks |
| `mathematics-in-lean` | Mathlib-oriented proof patterns, abstraction selection, tactic/term design and domain routing |
| `prove2me` | Prove2me mission discovery, local replay, submission identity and external-verdict handling |
| `ai4math-assurance-admission` | independent review, statement faithfulness, evidence capabilities, conflict and closure gates |
| `ai4math-toolchain-reproducibility` | pinned environments, capability maturity, execution plans, security and reproducibility |

## Source-family abstraction ledger

| Source family | Core concepts retained in the project-authored synthesis | Primary target Skills |
|---|---|---|
| AI for Mathematics lectures | problem-to-method fit; verifier-first experimental loops; informative failure; specialist preconditions | source discovery, bounded computation, proof/refutation |
| AI4Math Research Navigator | route by artifact and modality; compare datasets/evaluators; distinguish informal, formal, multimodal and discovery systems | source discovery, toolchain |
| Archon formalization | dependency-aware formalization; plan/prove/review separation; protected declarations; stalled-run diagnosis | Lean formalization, toolchain |
| Principles of Model Checking | model/property separation; transition semantics; product checks; abstraction soundness; state-space control | modeling, bounded computation, assurance |
| Mathematical logic methodology | expose assumptions; vary definitions; move between representation levels; test truth under changed rules | modeling, proof/refutation |
| Classical type theory | types as search constraints; dependency-preserving Skolemization; higher-order unification limits; extensionality audits | proof/refutation, Lean formalization |
| Danus proof orchestration | producer/verifier separation; fact-graph memory; route diversity; falsify before persistence; curate before exposition | proof/refutation, assurance |
| Dongbin AI4Math guide (two variants) | capability diagnosis; specialist-vs-general tool choice; formalization stack; verifier feedback; understanding over ritual | source discovery, toolchain |
| Harrison automated reasoning | SAT/FOL/equality/rewriting/QE/SMT routing; decision-procedure scope; LCF-style trust boundaries | proof/refutation, assurance |
| Category theory guide | universal constructions; functorial translation; naturality; adjunction/limit routing; abstraction interfaces | modeling, mathematics-in-Lean |
| Mathematical thinking | statement parsing; proof language; method selection; examples and counterexamples; proof communication | modeling, proof/refutation |
| Jixia Lean analyzer | toolchain match; declaration/InfoTree products; semantic output distinctions; static-analysis failure diagnosis | Lean formalization, toolchain |
| Lakatos proofs and refutations | counterexample triage; lemma incorporation; domain/definition repair; proof-content comparison; heuristic reconstruction | proof/refutation, modeling |
| Lean Eval comparator | pristine-vs-edited comparison; isolated elaboration; score semantics; security and pin-drift audits | assurance, toolchain |
| LeanSearch client | query by known information; syntax-sensitive requests; local validation; cache and backend instability | Lean formalization, mathematics-in-Lean |
| Lean 4 mathematical formalization | statement translation; proof-state reading; abstraction ladder; analysis/topology routing; complexity control | Lean formalization, mathematics-in-Lean |
| Lean 4 metaprogramming | syntax/elaboration/kernel stages; expression invariants; metavariable state; rollback; tactic and printer validation | Lean formalization, toolchain |
| Lean 4 study resources | goal-based resource routing; beginner-to-project progression; fallback when a resource does not fit | source discovery, mathematics-in-Lean |
| LeanSearch operator | parse/index/embed/search pipeline; schema and revision pinning; service and dependency diagnostics | Lean formalization, toolchain |
| Mathematical-analysis methods | normalize expressions; theorem preconditions; limits/continuity/integration/series applicability; convergence distinctions | modeling, mathematics-in-Lean |
| Mathematics in Lean (two variants) | proof state as API; weakest sufficient abstraction; structural-vs-algebraic work; interfaces, typeclasses, filters and induction | mathematics-in-Lean, Lean formalization |
| Natural Number Game | constructor/recursor alignment; rewrite-to-recursion; induction choice; witness-based order; tactic preconditions | mathematics-in-Lean, Lean formalization |
| Polya problem solving | understand/plan/execute/review; work backward; transform the problem; separate heuristic progress from proof | proof/refutation, modeling |
| Rethlas reasoning | persistent proof state; retrieval and applicability checks; diverse plans; falsification; strict verification; degraded-mode honesty | proof/refutation, source discovery, assurance |
| Elements of Style | concise proof exposition; paragraph unity; explicit relations; separate editing from mathematical validation | source discovery, proof/refutation |
| Tao Analysis Lean companion | API/phase alignment; totalization and index guards; epsilon/filter translation; type-boundary diagnosis | mathematics-in-Lean, Lean formalization |
| Theorem Proving in Lean 4 | propositions-as-types; constructors/recursors; elaborator information flow; termination; typeclass inference; logic/computation boundary | mathematics-in-Lean, Lean formalization |
| Informal–formal reasoning systems | verifier as hard boundary; retrieval before brute force; interleave reasoning and proving; optimize only after correctness | Lean formalization, assurance |
| Xena formalization method | freeze statements; API engineering; proof-state loop; normalize before automation; dependency-scale planning; counterexample checks | Lean formalization, mathematics-in-Lean, assurance |

## Duplicate-source handling

- The two Dongbin packages contribute one conceptual family, not two independent votes.
- The two Mathematics in Lean packages contribute one conceptual family, cross-checked for overlap.
- Duplicate packages never inflate source count, confidence, or evidence strength.

## Material intentionally not absorbed

- exact source prose, chapter summaries, worked examples, and book-specific wording;
- private paths, internal receipts, session state, credentials, or unpublished runtime facts;
- tool commands that were not revalidated against this repository;
- claims that a third-party package is installed, safe, licensed, current, or verifier-admitted;
- route portfolios or mandatory research sequences that would override the canonical actor.

## Research-method candidate intake (2026-09-21)

This intake adds no top-level Skill and no internal source package. Only independently rewritten, candidate-only operating rules are placed under existing owner `references/`. The reviewed snapshots are identified by content digest because their exact upstream identity and redistribution rights are not yet independently resolved; no source prose, script, installer, scheduler, service configuration or dependency was copied.

| Reviewed candidate | SHA-256 | Disposition | Existing owner / target |
|---|---|---|---|
| `research-lit` | `0a263919812b1135b26e5901af3076395baf03833d0f73c57fe4f11528161453` | pattern distilled | `ai4math-source-discovery/references/literature-citation-memory-audit.md` |
| `citation-audit` | `72714bbb165803f918281123a8b50eb15cd28db526e053dfb8f0d9835d28e246` | pattern distilled | same source-discovery reference |
| `research-wiki` | `93d66229579cb6180c06b661eac022e3784ea770e6793eb3661ba6dc0158f308` | bounded memory projection only | same source-discovery reference; never a Claim/Result ledger |
| `novelty-check` | `e1dc8d5e068ffec8ab1fda4fd379394e0f0798ab0f18d0fda3135449f1799a10` | bounded novelty pattern only | same source-discovery reference |
| `proof-checker` | `49a2ddedb11747f88c416c19abde151f7591530032d976d4f8ba7d40d3083205` | pattern distilled | `ai4math-proof-refutation/references/microclaim-proof-audit.md` |
| `experiment-audit` | `2fbb1e132c38ff451bbfdb0680caba4033a33e7c7b048fc535fb332a8fcb2e4c` | pattern distilled | `ai4math-bounded-computation/references/experiment-integrity-audit.md` |
| `result-to-claim` | `e7b742b06b8af6e3864b759ac32343535c2ad93cb6e39e42bd719c84909a969a` | pattern distilled | `ai4math-assurance-admission/references/evidence-claim-coverage.md` |
| `formula-derivation` | `3f1ce5b87c4b2d561efa2f3262471a7ad158fe8d2fd02e57cdf77aa27e0764d2` | no import: duplicate capability | existing `ai4math-modeling-derivation` contract |
| `proof-writer` | `6d7b3094711f609814680ded62e19b8dd61801511a7d98b96c033894c939babe` | no import: duplicate capability | existing `ai4math-proof-refutation` contract |
| `research-review` | `f7a6d18516229043fb879a033c1a5d144fc6226909261dbb1740065b1ea90a13` | excluded | publication/referee workflow is not mathematical admission |
| `kill-argument` | `796294cecca665b23e666c00438c8b323dfe74271add31d06e49ea02459e165b` | excluded | kill framing can conflate route failure with Claim refutation |

The four owner references remain subordinate to their existing top-level activation entries. They cannot run loops, schedule verdicts, create evidence, admit Results, or override canonical actor strategy.

## Research-method candidate intake, batch 2 (2026-09-21)

The second batch was reclassified after reading each candidate in full. The apparent `claims-drafting` match was rejected because it is a patent-claim drafting workflow, not a mathematical Claim contract. The remaining useful methods strengthen three existing owners; no new entry, package, executor, reviewer identity, queue, profiler, cloud dependency or paper workflow is added.

| Reviewed candidate | SHA-256 | Disposition | Existing owner / target |
|---|---|---|---|
| `claims-drafting` | `506ebbdafa7b66c0433e15f5230f6db6f2ccd306e5a397ce366ced18d90e6082` | excluded after full read | patent scope, jurisdiction rules and legal claim drafting are outside mathematical modeling |
| `experiment-plan` | `c5b53692ff95b0b55e80702e33afc79d9fe8d4f55a69e2a39714013f97ac595e` | domain-neutral pattern distilled | `ai4math-bounded-computation/references/experiment-integrity-audit.md` |
| `ablation-planner` | `262c824b0ea0521e8eb7f3814ee17bbad27f3c05256f49afa61619ae2641069e` | domain-neutral pattern distilled | same bounded-computation reference |
| `analyze-results` | `d35c7641a092024551f8a353d5f6cf5f2a49f83df2eac98cebfa8b8783355de3` | domain-neutral pattern distilled | same bounded-computation reference |
| `paper-claim-audit` | `a24db1ed7d0ccbdf39607e157a2393017dcfc2f49360677295d0a1f8f03b4f3b` | artifact-fidelity pattern distilled | `ai4math-assurance-admission/references/evidence-claim-coverage.md` |
| `system-profile` | `1d65767447a6c381ae2edb674b6c2b1f9c57d14a2ca96858d513c9f135255369` | planning-only pattern distilled | `ai4math-toolchain-reproducibility/references/runtime-profile-plan.md` |

Excluded details include patent-law formats, fixed reviewer models, paper tables/figures as required outputs, automatic revision/run loops, W&B/server assumptions, direct instrumentation, profiler execution, GPU/cloud control and dynamic runtime facts. Mathematical strategy and execution remain outside these references.

## Research-method candidate intake, batch 3 and full-inventory closure (2026-09-21)

The final pass classified all 89 directories containing `SKILL.md` in the reviewed research corpus. It found no missing top-level AI4Math owner. Four snapshots contained narrow reusable mechanisms; they were independently rewritten under two existing owners. No external body, script, reviewer backend, scheduler, runtime service, cloud/GPU control, model binding, paper workflow or self-modification applier was imported.

| Reviewed candidate | SHA-256 | Disposition | Existing owner / target |
|---|---|---|---|
| `idea-creator` | `421777d4ceb35641d0789004fdc9ca61609e21def4417332869b53a4fc8ceee3` | bounded candidate-generation/falsifier pattern distilled | `ai4math-modeling-derivation/references/problem-anchor-and-minimal-route-audit.md` |
| `idea-evaluator` | `718426dc2d9527e8728b030e667f42379197bcbf693c81c6d38b3a4e8317f385` | fatal-constraint and resource-fit pattern distilled | same modeling reference |
| `research-refine` | `410bb34a9cd796fa8c9b834627a92cfacc768a31af0152a32f856de87f2879b8` | Problem Anchor, minimal mechanism and drift pattern distilled | same modeling reference |
| `experiment-bridge` | `9d9994e578802760fa60a56bd87cad9df376cae97e0afa31311ef037bd599ea8` | oracle provenance, sanity-first and scale-up gate distilled | `ai4math-bounded-computation/references/experiment-integrity-audit.md` |

The full 89-entry closure is partitioned exactly once below:

- **Pattern distilled across batches 1–3 (16):** `ablation-planner`, `analyze-results`, `citation-audit`, `experiment-audit`, `experiment-plan`, `experiment-bridge`, `idea-creator`, `idea-evaluator`, `novelty-check`, `paper-claim-audit`, `proof-checker`, `research-lit`, `research-refine`, `research-wiki`, `result-to-claim`, `system-profile`.
- **Already covered, compositional, or separately implemented (7):** `formula-derivation`, `proof-writer`, `idea-discovery`, `research-refine-pipeline`, `research-pipeline`, `vibe-research-workflow`, `research-os`. The first two duplicate existing mathematical owners; the next four compose existing stages without a new atomic capability; Research OS is already implemented as a candidate-only metadata plane rather than an AI4Math truth owner.
- **Source/search frontends or broad empirical catalogs (11):** `Auto-Empirical-Research-Skills`, `academic-research-suite`, `alphaxiv`, `arxiv`, `comm-lit-review`, `deepxiv`, `exa-search`, `gemini-search`, `openalex`, `semantic-scholar`, `wiki-enrich`. Existing source-discovery abstractions cover their useful routing/provenance behavior without importing provider coupling or license-constrained corpora.
- **Autonomous review/revision loops (6):** `auto-paper-improvement-loop`, `auto-review-loop`, `auto-review-loop-llm`, `auto-review-loop-minimax`, `kill-argument`, `research-review`. Excluded because repeated self/reviewer cycles do not establish independent mathematical assurance and may conflate route failure with Claim refutation.
- **Runtime, remote compute, monitoring, or notification control (10):** `dse-loop`, `experiment-queue`, `feishu-notify`, `monitor-experiment`, `overleaf-sync`, `qzcli`, `run-experiment`, `serverless-modal`, `training-check`, `vast-gpu`. These require runtime authority, credentials, external services, queues or cost-bearing infrastructure and are not portable mathematical methods.
- **Publication, grant, rebuttal, presentation, or venue templates (20):** `benchmark-paper-template`, `grant-proposal`, `intro-drafter`, `paper-compile`, `paper-figure`, `paper-illustration`, `paper-illustration-image2`, `paper-plan`, `paper-poster`, `paper-poster-html`, `paper-slides`, `paper-talk`, `paper-write`, `paper-writing`, `pre-submission-reviewer`, `rebuttal`, `resubmit-pipeline`, `slides-polish`, `tech-paper-template`, `writing-systems-papers`. Publication quality is not mathematical evidence or admission.
- **Patent workflow (10):** `claims-drafting`, `embodiment-description`, `figure-description`, `invention-structuring`, `jurisdiction-format`, `patent-novelty-check`, `patent-pipeline`, `patent-review`, `prior-art-search`, `specification-writing`. Legal scope and jurisdictional drafting are outside AI4Math Claim semantics.
- **Visual, rendering, or interview utilities (6):** `figure-designer`, `figure-spec`, `interview-cheatsheet`, `mermaid-diagram`, `pixel-art`, `render-html`. These are presentation utilities, not missing research capabilities.
- **Domain-specific workflow (1):** `idea-discovery-robot`; robotics-specific orchestration adds no domain-neutral mathematical owner.
- **Self-modification governance (2):** `meta-optimize`, `meta-apply`. The propose/apply privilege separation is a useful software-governance pattern, but this template has no self-modifying Skill corpus runtime; importing an applier would add authority and ownership surface without a present requirement.

This closure preserves ten configured top-level entries. Any future candidate must demonstrate an atomic capability not expressible by those owners; a different provider, document format, model, venue, scheduler or workflow composition is not such a capability.
