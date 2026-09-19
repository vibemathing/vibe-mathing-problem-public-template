# AI4Math Skill consolidation map

This file records the conceptual consolidation behind the nine project Skills. It is not a redistribution of the audited source packages.

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
