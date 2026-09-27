---
name: dongbin-ai4m
description: "Operational AI-for-Mathematics knowledge from Dong Bin's 2025 learning guide. Use for AI4M study/research planning, choosing special-purpose data-driven tools vs general formal-reasoning models, deciding when to use Lean/autoformalization/verifier feedback, agents or evolve-style search, and checking rigor, failure recovery, and mathematical insight."
---

<!-- argument-hint: [goal, AI4M task, method, tool family, or chapter] -->

# AI for Mathematics 从入门到前沿的学习指南

**Author**: 董彬，北京大学 | **Source date**: 2025-09-28 | **Chapters**: 3 functional units | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task concerns AI-assisted mathematical research, AI4M learning plans, formal mathematics, Lean, autoformalization, theorem proving, verifier-guided reasoning, mathematical agents, data-driven conjecture discovery, or evolve-style optimization.

Do not use it as a Lean syntax manual, a generic machine-learning textbook, or a source of current model rankings. For fast-changing tool/model status, verify current information externally before acting.

1. Identify the user's real mathematical goal and required level of rigor.
2. Classify the task with the routing table below.
3. Check the chosen method's prerequisites before execution.
4. Load the linked chapter or `patterns.md` when the task needs detail.
5. Produce a concrete research/learning plan, decision, diagnostic, or validation procedure.
6. Run `SELF_CHECK` before finalizing.

## Core Frameworks & Mental Models

### 1. Three-capability diagnostic
Classify the bottleneck before choosing technology:

- **Knowledge navigation** — the researcher needs to locate, learn, compare, or retrieve theory, tools, definitions, prior results, or formal-library facts.
- **Proof & verification** — the researcher needs proof construction, proof completion, counterexample checks, or correctness guarantees.
- **Insight & connection** — the researcher needs patterns, conjectures, structural relations, useful representations, or mathematically meaningful interpretation of data.

A real project can need all three. Route the immediate bottleneck first; use the other two as supporting capabilities.

### 2. Interest-and-task fork: special-purpose tool vs general model
Use two signals together: the researcher's comparative advantage and the task shape.

| Signal | Prefer special-purpose data-driven tool | Prefer general/formal reasoning model |
|---|---|---|
| Main interest | mathematical structure and conjectures | algorithms, programming, model/agent design |
| Problem shape | narrow bottleneck with usable mathematical data | reusable class of reasoning/formalization tasks |
| Desired output | feature, pattern, candidate conjecture, interpretable clue | formalization, proof step, verified solution, reusable reasoning system |
| Main prerequisite | mathematical sensitivity + enough ML to build/interpret the tool | LLM foundations + formal mathematics/Lean + engineering |

If both columns fit, decompose the project: use the special-purpose route for discovery and the formal/general route for verification or scalable automation.

### 3. Data-driven mathematical discovery loop
Use when a mathematical problem contains a concrete subproblem that can be represented by data.

1. Define the mathematical bottleneck precisely.
2. Decide whether data-driven treatment can expose useful structure.
3. Generate or curate mathematically meaningful data.
4. Choose a model that matches the signal and available data.
5. Train/evaluate for predictive or structural signal.
6. Interpret the result in mathematical terms.
7. Convert the signal into a candidate relation, invariant, conjecture, or proof direction.
8. Test mathematically; discard patterns that do not survive interpretation and checking.

A high score without mathematical interpretation is an intermediate artifact, not a research conclusion.

### 4. Mathematical digitization and formalization stack
Treat formalization as a conversion pipeline from ordinary mathematical language to a machine-checkable representation. In the book's recommended ecosystem, Lean is the primary route.

Use the stack progressively:

`natural-language mathematics → definitions/statement in Lean → library search → assisted/automatic formalization → proof search/completion → kernel verification`

Formalization is useful for pure mathematics even without model training: the checker can certify proof correctness. It also enables rigorous benchmark construction and creates high-quality feedback signals for learning and inference.

### 5. Verifier-feedback loop
When correctness can be checked mechanically, feed verification back into search/training instead of treating generated text as final.

`candidate → formal checker → accept / error signal → revise/search → recheck`

Use this loop for proof generation, proof completion, formalization quality control, and model/agent evaluation. The key property is cheap, precise feedback relative to human proof review.

### 6. Agent-first heuristic
As base models become stronger, an agent that orchestrates decomposition, retrieval, checking, iteration, and tool use can be the first implementation to try for many multi-step problems.

Choose an agent when:
- the task naturally decomposes into observable steps;
- intermediate outputs can be checked;
- the base model already has substantial mathematical competence;
- orchestration may unlock capability faster than training a bespoke model.

If the task demands absolute proof correctness, pair the agent with a formal verifier or route the final artifact through Lean.

### 7. Evolve-agent eligibility rule
Use an AlphaEvolve-like search loop only when three conditions hold:

1. the mathematical objective is clearly defined;
2. quality can be measured automatically or quantitatively;
3. there is a usable initial solution to improve.

If any condition fails, first improve the objective, evaluator, or seed. Evolutionary iteration without a trustworthy score can optimize the wrong target.

### 8. Understanding-over-proof objective
Treat proof and verification as instruments for mathematical understanding. Automate tedious or mechanical proving where possible, then reinvest human attention in explanations, structural connections, generalization, and new viewpoints.

When a task asks only for “a proof,” also ask internally: what insight should remain after the proof is checked?

## Routing & Decision Logic

| User/task signal | Route | Load |
|---|---|---|
| “How should I enter AI4M?” / learning roadmap | baseline AI + interest fork + three-capability diagnostic | [ch01](chapters/ch01-orientation.md) |
| Need patterns/conjectures from a narrow mathematical dataset | data-driven discovery loop | [ch02](chapters/ch02-research-paths.md), `patterns.md` |
| Need strict correctness, proof checking, formal benchmark | Lean/formalization + verifier feedback | [ch02](chapters/ch02-research-paths.md) |
| Natural-language statement is hard to formalize | library search → assisted autoformalization → manual repair | [ch02](chapters/ch02-research-paths.md), `patterns.md` |
| Strong model, multi-step task, tool orchestration useful | agent-first heuristic + explicit evaluators | [ch02](chapters/ch02-research-paths.md) |
| Quantifiable objective + seed solution | evolve-agent loop | [ch02](chapters/ch02-research-paths.md), `cheatsheet.md` |
| Technically correct result lacks mathematical meaning | understanding-over-proof review | [ch03](chapters/ch03-understanding-over-proof.md) |

## Failure Recovery

- **Special-purpose tool finds correlation but no mathematical interpretation**: inspect features, data-generation assumptions, symmetries, invariants, and confounders. Do not promote the signal to a conjecture until it has a mathematical reading.
- **Formalization stalls on library/API discovery**: search mathlib semantically, restate the goal using existing definitions/lemmas, then use assisted formalization; split the theorem if the statement is too monolithic.
- **Generated proof looks plausible but rigor is required**: formalize/check it; withhold a correctness claim until the checker passes or a human proof audit is complete.
- **Agent loops without progress**: add checkable intermediate goals, tighten termination criteria, expose verifier feedback, or reduce the task to a smaller formalized subproblem.
- **Evolve search drifts**: audit the scoring function and constraints; strengthen the evaluator before further iteration.
- **Automation succeeds but insight is lost**: extract the decisive lemmas, patterns, invariants, and explanatory structure; present these as the human-facing result.
- **Evidence is insufficient**: return “insufficient to judge,” list the missing mathematical inputs, and state the next validation step.

## SELF_CHECK

Before answering or executing a plan, verify:

- [ ] I identified the mathematical objective, not just the requested tool.
- [ ] I classified the current bottleneck as navigation, proof/verification, insight/connection, or a combination.
- [ ] I selected a method whose prerequisites are actually present.
- [ ] I separated discovery evidence from proof-level evidence.
- [ ] I included a verifier/human audit when correctness claims require it.
- [ ] I checked special cases: library-search friction, formalization overhead, weak evaluators, noisy data, and non-interpretable model signals.
- [ ] I gave a fallback route if the first method fails.
- [ ] The output preserves mathematical insight, not merely task completion.
- [ ] For fast-changing model/tool claims, I verified current status externally.

## Chapter Index

| # | Title | Key capabilities |
|---|---|---|
| [ch01](chapters/ch01-orientation.md) | Orientation and AI4M foundations | three-capability diagnostic, interest fork, baseline preparation |
| [ch02](chapters/ch02-research-paths.md) | Research paths and operational methods | special-purpose discovery, Lean/formalization, verifier feedback, agents, evolve search |
| [ch03](chapters/ch03-understanding-over-proof.md) | Understanding as the research objective | proof automation as leverage, insight preservation |

## Topic Index

- **Agent / 智能体** → ch01, ch02
- **AI Scientist / AlphaEvolve-style search** → ch02
- **autoformalization / 自动形式化** → ch02
- **FATE / FATE-X** → ch02
- **formal verification / 形式化验证** → ch02
- **insight / 洞察** → ch01, ch03
- **knowledge navigation / 知识导航** → ch01
- **Lean / mathlib / LeanSearch** → ch02
- **mathematical digitization / 数学数字化** → ch02
- **proof & verification / 证明与验证** → ch01, ch02, ch03
- **reap / REAL-Prover** → ch02
- **special-purpose AI tools / 专用工具** → ch02
- **verifier feedback / 验证器反馈** → ch02

## Supporting Files

- [glossary.md](glossary.md) — key terms and systems with chapter references
- [patterns.md](patterns.md) — procedures, diagnostics, recovery strategies, and validation rules
- [cheatsheet.md](cheatsheet.md) — compact decision trees and trade-off rules

## Scope & Limits

This skill operationalizes the source guide's methodology and examples. It does not replace a Lean tutorial, ML textbook, or up-to-date survey of AI4M systems. The compiler had complete access to the readable textual body used for this skill, while the original PDF binary, authoritative pagination, and page-layout/image layer were unavailable in the execution environment. No claims here depend on unseen page graphics.
