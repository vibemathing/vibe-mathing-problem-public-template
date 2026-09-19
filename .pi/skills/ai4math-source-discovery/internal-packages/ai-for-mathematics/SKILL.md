---
name: ai-for-mathematics
description: "AI-for-math: discovery, proof, counterexamples, PDEs, PINNs."
---

<!-- argument-hint: [research goal, method, concept, or chapter number] -->

# Lectures on AI for Mathematics
**Authors**: Xiaoyang Chen & Xiang Jiang | **Version**: 1.0 | **PDF pages**: 159 | **Chapters**: 6 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task is about *doing* AI-assisted mathematical research or choosing an AI method for a mathematical objective. Start with the routing rules below, then load the relevant chapter only when detail is needed.

Do not invoke it merely because a prompt contains mathematics. Routine symbolic manipulation, a standard textbook proof, or a conventional numerical calculation can proceed directly unless the user asks for an AI-for-math workflow or method comparison.

### Minimum intake
Capture, or explicitly mark unknown:
- mathematical objective and success criterion;
- object/search space and constraints;
- whether candidates can be checked mechanically or formally;
- available data, simulator, theorem prover, evaluator, or numerical reference;
- scale/dimension and computational budget;
- required confidence: exploratory clue, conjecture, verified construction, formal proof, or numerical evidence.

If a missing item changes the method choice, request it. If progress is still possible, state an assumption and continue.

## Core Routing Logic

**1. Classify the mathematical activity.**

| Goal | First route | Load |
|---|---|---|
| Discover a hidden relation or conjecture from structured examples | supervised prediction → interpretability → mathematical synthesis → stress test | [ch03](chapters/ch03-discovering-patterns.md) |
| Discover an algorithm in a discrete structured space | object-level RL when a compact game/state/action representation exists; program evolution when executable programs can be scored | [ch03](chapters/ch03-discovering-patterns.md) |
| Prove a theorem | formalize → neural/LLM guidance → proof search → kernel verification | [ch04](chapters/ch04-proving-theorems.md) |
| Construct a counterexample or extremal object | search with a scalar violation/quality score; choose CEM, PatternBoost, or generator-verifier agents by structure | [ch05](chapters/ch05-counterexamples.md) |
| Solve or invert a PDE | establish a classical baseline first; use PINNs where meshless physics/data fusion, inverse problems, or dimensional structure justify them | [ch06](chapters/ch06-pdes.md) |
| Train/evaluate a model used in mathematical work | data/model/algorithm decomposition; held-out evaluation; engineering controls | [ch02](chapters/ch02-machine-learning.md) |

**2. Ask whether correctness is cheaply checkable.** If a candidate can be verified by Lean/Coq, a symbolic algebra system, executable tests, an exact combinatorial checker, or a reliable numerical residual, put that checker outside the generator and use it as the gate. Strong generators with weak verification create persuasive errors.

**3. Match the search representation to the object.** Prefer a compact representation that preserves useful mathematical structure. Use explicit states/actions for sequential discrete construction, programs when behavior is naturally executable, and structured numerical features when learning relations. Representation errors can dominate model choice.

**4. Separate exploration from certification.** Treat prediction scores, model explanations, near-misses, and generated candidates as evidence for where to look. Convert them into a mathematical object or proposition, then test or prove it independently.

## Global Operating Principles

### Problem → AI technology → implementation
Keep the mathematical problem as the main thread. Define what would count as progress before selecting a model. Then choose the smallest AI machinery that attacks the bottleneck.

### Verification-first research loop
1. Specify the object, constraints, objective, and validator.
2. Produce diverse candidates or hypotheses.
3. Reject invalid outputs automatically whenever possible.
4. Preserve high-quality or informative failures.
5. Interpret recurring structure.
6. Turn that structure into a human-readable conjecture, construction family, proof tactic, or numerical hypothesis.
7. Stress-test on shifted, constructed, adversarial, or higher-scale cases.
8. Escalate the surviving claim to proof/formal verification or independent numerical validation.

### Use interpretability as a bridge
High predictive accuracy alone is weak mathematical evidence. Use saliency, feature ablation, low-dimensional projections, or other diagnostics to identify which inputs drive the prediction. Re-express those signals as mathematical quantities a researcher can reason about, then retrain/retest with the reduced set.

### Preserve informative failure
A failed search can still reveal structure. If top candidates repeatedly converge toward the same motifs, parameterize those motifs and analyze the family directly. In counterexample work, this can be more valuable than another undirected round of sampling.

### Match specialist methods to their preconditions
- **Deep cross-entropy search**: discrete sequential object, fast scalar reward, elite examples useful for imitation.
- **PatternBoost**: strong local improver plus global regularities shared by good solutions.
- **AlphaTensor-style RL**: mathematically natural game formalization and specialized high-volume search.
- **AlphaEvolve-style program evolution**: executable candidate programs and a trusted automated evaluator.
- **Formal proof search**: theorem and library context can be represented in a proof assistant.
- **PINNs**: differential equation residual is differentiable and physics/data constraints can be expressed in a loss; validation remains available.

## Failure Recovery

When the first route stalls, diagnose before adding compute:

- **No useful signal in supervised discovery** → inspect representation/data coverage; add deliberately constructed boundary cases; reconsider target variable. Do not mine explanations from a model that fails held-out prediction.
- **High prediction but no stable interpretation** → run feature ablation and distribution-shift tests; prefer a smaller feature set that retains performance; withhold a conjecture if explanations are unstable.
- **RL/CEM collapses to one motif** → raise exploration/diversity, change encoding, seed with structurally different examples, or switch to a local/global hybrid.
- **Search finds only near-misses** → cluster elite constructions, identify recurring motifs, parameterize a family, and analyze that family mathematically.
- **Program evolution games the evaluator** → harden tests, add invariants, stage evaluation from cheap filters to full verification, and keep a diverse archive.
- **Formal proof search explodes** → improve formalization, lemma retrieval, subgoal ordering, or curriculum; prioritize the hardest subgoal when the proof tree is bottlenecked there.
- **LLM agent repeats invalid attempts** → give verifier feedback in actionable form, retain attempt history, decompose only where dependencies are clear, and require final independent verification.
- **PINN loss decreases while solution is wrong** → diagnose approximation, optimization, and generalization/discretization error separately; rebalance loss terms, resample difficult regions, and compare with a classical reference.
- **Evidence cannot be certified** → return the strongest supported status (candidate, empirical pattern, numerical indication) and say what verification is missing.

## SELF_CHECK

Before finalizing an answer or research plan:
- Did I identify the user's mathematical objective and required confidence level?
- Did I choose a method whose preconditions hold?
- Is the representation faithful to the mathematical structure?
- Is generation separated from verification where feasible?
- Did I protect held-out or stress-test data from optimization leakage?
- Did I inspect exceptions, adversarial cases, and informative failures?
- For proofs/constructions, is the claim independently checkable?
- For PINNs, did I test all three error sources and compare to a classical method where feasible?
- Did I avoid presenting a model score, reward, or training loss as mathematical truth?
- Would a different route provide a meaningful cross-check?

## Chapter Index

| # | Title | Key operational content |
|---|---|---|
| [ch01](chapters/ch01-overview.md) | Overview | discovery–proof–refutation loop; problem-first formulation; reproducibility |
| [ch02](chapters/ch02-machine-learning.md) | Introduction to Machine Learning | representations, training, evaluation, RL/LLMs, engineering controls |
| [ch03](chapters/ch03-discovering-patterns.md) | AI for Discovering Mathematical Patterns | prediction-to-conjecture; AlphaTensor; AlphaEvolve |
| [ch04](chapters/ch04-proving-theorems.md) | AI for Proving Mathematical Theorems | neuro-symbolic proof search; AlphaProof; research agents; creativity limits |
| [ch05](chapters/ch05-counterexamples.md) | AI for Constructing Counterexamples | deep cross-entropy; PatternBoost; generator-verifier agents |
| [ch06](chapters/ch06-pdes.md) | AI for PDEs | FDM/FEM/FVM/spectral selection; PINNs; error diagnosis and validation |

## Topic Index

- **AlphaEvolve / program evolution** → ch03
- **AlphaProof / formal theorem proving** → ch04
- **AlphaTensor / TensorGame** → ch03
- **counterexamples / extremal constructions** → ch05
- **deep cross-entropy method** → ch05
- **formal verification / Lean** → ch04, ch05
- **GRPO / RLHF / DPO** → ch02, ch04
- **interpretability / saliency / feature ablation** → ch03
- **LLM agents / generator-verifier loops** → ch04, ch05
- **matrix multiplication algorithms** → ch03
- **model evaluation / train-validation-test** → ch02
- **PatternBoost** → ch05
- **PCA / gradient descent / neural networks** → ch02
- **PDE numerical methods** → ch06
- **physics-informed neural networks (PINNs)** → ch06
- **proof search / MCTS** → ch04
- **representation / inductive bias** → ch02, ch03, ch05, ch06
- **reinforcement learning / MDP / reward design** → ch02, ch03, ch05
- **stress testing / constructed data** → ch03, ch05
- **Transformer / attention / LLM training** → ch02

## Supporting Files

- [glossary.md](glossary.md) — compact definitions and chapter pointers
- [patterns.md](patterns.md) — reusable research procedures with preconditions and fallbacks
- [cheatsheet.md](cheatsheet.md) — routing tables, decision rules, smells, and validation gates

## Scope & Limits

This skill operationalizes the content of *Lectures on AI for Mathematics*, version 1.0. It does not certify new mathematics by itself. For research claims, couple its search workflows with domain-specific proof assistants, exact checkers, symbolic tools, or independent numerical solvers. For implementation details beyond the book, use current project/library documentation.
