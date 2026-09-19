---
name: rethlas-math-reasoning
description: "Operational knowledge distilled from the Rethlas repository. Use for research-level mathematical proof search that needs persistent reasoning memory, theorem retrieval, toy or counterexample exploration, multiple decomposition plans, direct or recursive proving, external-result applicability checks, strict proof verification, verifier-driven repair, or Rethlas-style deployment and auditing."
license: Apache-2.0
---

<!-- argument-hint: [problem, proof-search state, workflow question, or chapter number] -->

# Rethlas Math Reasoning
**Source**: Rethlas repository archive | **Content type**: technical | **Operational chapters**: 10 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when a task benefits from Rethlas's research-math workflow: persistent state, deliberate falsification, literature grounding, multiple proof plans, recursive work, and a strict verifier/repair loop.

- **Given a new theorem** — start with the routing loop below; load ch03 and ch05 as needed.
- **Given a stuck subgoal or fragile claim** — load ch04, then ch02 if prior failures may help.
- **Given several candidate proof plans** — load ch06; escalate to ch07 only after direct screening.
- **Given a complete proof draft** — load ch08 and ch09 before calling any verifier.
- **Asked to deploy or audit Rethlas** — load ch01 and ch10.
- **Asked for a named subsystem** — use the Topic Index to load the smallest relevant chapter.

For a simple arithmetic exercise, a routine textbook proof, or a generic math explanation that does not need this workflow, do not invoke the full Rethlas process unless the user asks for it.

## Self-Check

Before committing to a route or presenting a result, verify:

1. **Goal** — Is the original theorem/task understood in full, including all hypotheses and the requested output?
2. **State** — Which proof-state class applies now: fresh, intuition-poor, fragile, retrieval-blocked, plan-ready, directly screened, recursive, or verification-ready?
3. **Prerequisites** — Does the selected method have the context it requires? In particular, recursive proving needs direct-screened plans; strict verification needs a full proof.
4. **Memory** — Have important progress, failures, counterexamples, source results, and branch changes been persisted under the stable problem ID?
5. **External results** — Are complete statements, identifiers, paper-local definitions, hypotheses, and proof applicability checked before use? For nontrivial subgoals/key claims, ground the work with theorem search when that capability is available; stop repeating retrieval once it no longer adds guidance.
6. **Exceptions** — Did any counterexample, missing hypothesis, definition mismatch, or verifier finding invalidate the current route?
7. **Output** — Does the assembled proof cover the whole original target, order dependencies before use, and preserve the complete target statement?
8. **Acceptance** — Has a full strict verification pass returned zero critical errors and zero gaps? If the dedicated verifier was unavailable, is that limitation stated explicitly?

## Failure Recovery

- **Immediate-conclusion pass stalls** → build toy examples or retrieve focused background.
- **Toy examples stay inconclusive** → change example family or test a fragile claim directly.
- **Counterexample space is unclear** → refine assumptions/search space; store the inconclusive attempt.
- **Retrieval is vague or repetitive** → broaden once if useful, then switch to independent reasoning.
- **A direct subgoal is blocked** → counterexample-test it before escalating.
- **Every direct-screened plan fails** → recursive plan-specific work.
- **Every recursive plan fails** → synthesize common failures and generate a genuinely new plan family.
- **Verifier rejects the proof** → repair critical errors first, then gaps; backtrack or change architecture when local edits cannot fix the cause; re-run the full verifier.
- **Evidence remains insufficient** → return an explicit unresolved status and preserved partial progress; never manufacture a proof or a verification claim.

## Core Frameworks & Mental Models

### 1. Adaptive proof-state routing
At every meaningful iteration, classify the current state before choosing a method. Prefer the cheapest useful move, then escalate only when evidence says it is needed.

1. **Fresh problem / branch / subgoal** → derive immediate consequences.
2. **Need intuition** → build toy examples that satisfy assumptions and conclusion.
3. **Claim feels fragile or a subgoal stalls** → try to falsify it with a counterexample.
4. **Need external context** → search for mathematically close results and read enough source context to judge applicability.
5. **Enough constraints collected** → propose several materially different decomposition plans.
6. **A plan exists** → screen every subgoal directly before spending on recursive agents.
7. **All current plans fail** → run plan-specific recursive work, synthesize shared failures, then re-plan.
8. **A full proof exists** → verify the whole proof; repair every critical error and gap; repeat until the strict gate passes.

External retrieval supports reasoning. If retrieval repeatedly yields weak guidance, stop spending effort on more search and continue with independent reasoning, examples, counterexamples, and new decompositions.

### 2. Memory as proof infrastructure
Persist intermediate artifacts instead of relying on conversation recall. Keep stable channels for immediate conclusions, toy examples, counterexamples, major decisions, decomposition plans, proof steps, failed paths, verifier reports, branch states, and events. Search only the smallest relevant channel set. A failed route becomes reusable evidence, not discarded work.

Use the same data-relative problem identifier throughout a run. Preserve category subdirectories. Reject parent traversal and keep memory/results inside the working tree.

### 3. Falsification before commitment
A failed counterexample search is weak positive evidence; it never proves a claim. A genuine counterexample invalidates the affected claim or branch immediately and should be stored for later reuse. When direct proof gets stuck on a subgoal, test whether the subgoal is false, too strong, or missing hypotheses before labeling it merely difficult.

### 4. Literature as methods plus applicability checks
Search with a complete mathematical statement when possible. For a useful paper result, preserve the complete statement and source identifiers, expand paper-local definitions, inspect how its proof works, and test the ambient hypotheses against the current problem. Treat partial results with extra hypotheses as diagnostic evidence: identify why the proof needs those hypotheses and where the method breaks without them.

### 5. Plan diversity plus direct screening
Generate decomposition plans that differ materially in mechanism, not wording. Each plan records ordered subgoals, motivation, relevant examples/counterexamples/failures/search findings, and status. Try the entire plan directly before diagnosing failure. When adapting a known proof, record both successful migrations and exact migration failures.

### 6. Recursive escalation with continuity
Recursive agents start from assigned plans and known stuck points. They may refine a plan when new evidence justifies it, while retaining continuity with the assigned route. Share failure information across plan agents. If all recursive routes fail, aggregate common obstructions into the next planning round.

### 7. Strict verification gate
Call the verifier only on a full proof of the entire target. Verify statements in textual order, check every small deduction, audit existence/property assumptions, compare exact definitions and formulas, and separately validate external references. The acceptance rule is strict: success requires zero critical errors and zero gaps. Any failure triggers repair and re-verification. A verified artifact is published only after that gate passes.

### 8. Honest degraded mode
This skill can guide an agent even when Rethlas services are absent. Emulate memory with local structured files and emulate theorem retrieval with available scholarly/web search. If the dedicated verifier is unavailable, perform the strongest local audit available and label the result as unverified by the Rethlas verifier. Never upgrade a local self-check into a verifier-passed claim.

## Chapter Index

| # | Title | Key frameworks |
|---|---|---|
| [ch01](chapters/ch01-architecture-and-boundaries.md) | Architecture & boundaries | two-agent pipeline, workspace isolation, problem IDs |
| [ch02](chapters/ch02-memory-and-state.md) | Memory & state | append-only channels, BM25 retrieval, branch state |
| [ch03](chapters/ch03-immediate-conclusions-and-toy-examples.md) | Cheap inference & toy examples | immediate consequences, assumption tracing |
| [ch04](chapters/ch04-counterexamples-and-failure-memory.md) | Counterexamples & failure memory | falsification, failed-path reuse |
| [ch05](chapters/ch05-retrieval-and-applicability.md) | Retrieval & applicability | theorem search, context expansion, partial-result diagnosis |
| [ch06](chapters/ch06-decomposition-and-direct-proving.md) | Decomposition & direct proving | plan diversity, direct screening, proof migration |
| [ch07](chapters/ch07-recursive-proving-and-replanning.md) | Recursive proving & re-planning | plan agents, shared stuck points, failure synthesis |
| [ch08](chapters/ch08-proof-assembly-and-output-contract.md) | Proof assembly | paper-like blueprint, citation contract, stopping rule |
| [ch09](chapters/ch09-strict-verification.md) | Strict verification | sequential checks, reference checks, schema gate, repair |
| [ch10](chapters/ch10-runner-and-operations.md) | Runner & operations | service order, iteration runner, references, result site |

## Topic Index

- **Append-only memory** → ch02
- **Applicability of external theorems** → ch05, ch09
- **BM25 memory search** → ch02
- **Branch backtracking** → ch02, ch07
- **Counterexamples** → ch04
- **Decomposition plans** → ch06, ch07
- **External citations** → ch05, ch08, ch09
- **Failed paths** → ch04, ch07
- **Immediate conclusions** → ch03
- **Open problems** → ch07, ch08
- **Partial results / extra hypotheses** → ch05, ch06
- **Problem ID / workspace paths** → ch01, ch10
- **Proof blueprint format** → ch08
- **Recursive sub-agents** → ch07
- **Reference directories** → ch01, ch10
- **Search fallback** → ch05
- **Strict verdict** → ch09
- **Toy examples** → ch03
- **Verification service** → ch09, ch10
- **Verifier repair loop** → ch09
- **Web result site** → ch10

## Supporting Files

- [glossary.md](glossary.md) — key terms and exact Rethlas concepts
- [patterns.md](patterns.md) — operational procedures and failure-recovery patterns
- [cheatsheet.md](cheatsheet.md) — compact routing and decision rules

## Scope & Limits

This skill captures the operational knowledge in the supplied Rethlas repository archive: proof generation, persistent reasoning state, retrieval, proof assembly, verification, and local operation. It does not bundle the original MCP/HTTP services or Codex runner. Tool names such as `memory_search`, `search_arxiv_theorems`, and `verify_proof_service` describe the source architecture; use equivalent host capabilities when those tools are unavailable. Preserve the source's verification semantics: only a successful strict verifier run supports a claim of Rethlas verification.
