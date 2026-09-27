---
name: danus-proof-orchestration
description: "Operational knowledge base derived from Danus: Orchestrating Mathematical Reasoning Agents with Fact-Graph Memory. Use when operating or troubleshooting Danus/FrenzyMath, designing verifier-gated multi-agent mathematical research, routing work between main agents, proof workers and verifiers, managing local/global/fact-graph memory, recovering failed proof-search routes, producing human progress reports, or turning verified fact graphs into papers."
---

<!-- argument-hint: [project, workflow stage, failure symptom, or Danus concept] -->

# Danus Proof Orchestration

Source: **Danus: Orchestrating Mathematical Reasoning Agents with Fact-Graph Memory** (repository snapshot supplied by the user; 2026). This skill encodes its operational contracts, recovery logic, and quality gates.

## When to use

Use this skill when a request concerns one or more of these tasks:

- operate, diagnose, resume, or explain a Danus project or worker swarm;
- design a mathematical-agent workflow with a separate correctness authority;
- decide what belongs in local memory, global memory, or the verified fact graph;
- choose a proof-search move: direct consequences, examples, counterexamples, decomposition, direct proof, literature transfer, or failure synthesis;
- verify and repair a candidate mathematical fact before it becomes trusted;
- create a human-facing progress report from verified results;
- curate verified results into a paper and run its citation, compile, leak, and mathematics gates;
- reason about Danus permissions, trust boundaries, content addressing, revocation, or recovery.

Do not auto-invoke for an ordinary mathematics question that asks only for a proof, generic multi-agent coding, generic note-taking, or generic academic writing with no Danus/fact-graph workflow. If the user explicitly asks to apply Danus principles to another system, use the architecture and decision rules while labeling implementation-specific commands as Danus-specific.

## First classify the request

| Route | Signals | Load |
|---|---|---|
| Architecture / trust | roles, authority, truth, memory, fact DAG, permissions | [ch01](chapters/ch01-orientation-and-trust-model.md), [ch02](chapters/ch02-memory-and-fact-graph.md), [ch10](chapters/ch10-security-and-permissions.md) |
| Main-agent strategy | route choice, worker allocation, synthesis, heartbeat, stalled program | [ch03](chapters/ch03-main-agent-strategy-loop.md) |
| Worker proof search | prove a subgoal, examples, counterexamples, decomposition, stuck proof | [ch04](chapters/ch04-worker-proof-search-loop.md), [ch07](chapters/ch07-literature-reconnaissance.md) |
| Verification | candidate fact, rejection, gap, reference application | [ch05](chapters/ch05-verification-and-fact-submit.md) |
| Operations | setup, start/status/stop/finalize, services, resume, runtime failure | [ch06](chapters/ch06-operations-and-recovery.md) |
| Human report | operator update, progress PDF/report, clean audience-facing summary | [ch08](chapters/ch08-human-summary.md) |
| Paper | verified facts to LaTeX, references, revision, paper math gate | [ch09](chapters/ch09-write-paper-pipeline.md) |
| Implementation details | hashes, schemas, modules, deterministic boundaries | [ch11](chapters/ch11-implementation-contracts.md) |

## Global invariants

1. **Fact graph = correctness source.** Local memory is private scratch. Global memory is shared awareness. Only a verifier-accepted fact may support downstream proof as established mathematics.
2. **Authority is structural.** Main agents steer and may revoke; workers may submit facts; verifiers judge and write nothing to shared state. Never simulate a permission a role does not have.
3. **Verification is a write gate.** A candidate moves into the fact graph only after a fresh verifier returns `correct`. Rejection starts a repair-and-resubmit loop.
4. **The verifier is an LLM judge.** Treat acceptance as Danus-verified, not formal proof-assistant certification. Escalate high-stakes claims to human review when appropriate.
5. **Unverified reasoning stays labeled.** Subagent reports, plans, directions, obstacles, elaborations, and global-memory claims can steer search; they cannot serve as proved premises.
6. **Text-only mathematical reasoning is a Danus contract.** Main agents, subagents, workers, and verifiers do not use computational experiments, solvers, symbolic engines, brute force, or proof assistants for the mathematical argument.
7. **Operator gates consequential outward actions.** Final target selection, destructive revocation, and external publication remain explicit operator decisions.
8. **Preserve the fixed goal.** Strategy may change; the mathematical target does not silently weaken.

## Operational procedure

### 1. Establish state and authority

Identify the project, requested outcome, current stage, available Danus tools/CLI, verified facts, global findings, worker state, and any explicit operator decision. If Danus is unavailable in the current environment, give an exact runbook and state that commands were not executed.

### 2. Route by evidence maturity

- **Fresh problem:** normalize the statement, extract immediate consequences, inspect memory for related work, build toy examples, probe fragility with counterexamples, then propose materially different decompositions.
- **Active proof route:** try the full plan before polishing; adapt relevant known proofs; verify any intermediate result that downstream work will rely on.
- **Blocked route:** counterexample first. After at least two genuine direct attempts with no refutation, record a concrete obstacle/dead end and change the plan rather than grinding.
- **Program-level stall:** main agent reviews the entire approach portfolio, including parked routes and return conditions; run targeted literature reconnaissance; replenish non-duplicative investigations; publish revised guidance only when synthesis materially changes.
- **Candidate theorem obtained:** submit a self-contained statement and proof with real predecessor fact ids and defined notation. Repair every verifier error/gap before reuse.
- **Verified target ready:** operator records the paper target; workers may be stopped when all intended targets are verified and the dependency route is credible.
- **Communication / publication:** use the isolated human-summary or write-paper pipeline; never repurpose internal memory as reader-facing prose.

### 3. Choose the smallest trustworthy store

Use private local memory for rough process notes. Use typed global memory for formed findings plus evidence and for shared dead ends. Use the fact graph only for verifier-accepted, self-contained mathematical units. Search global memory for awareness; search the fact graph before proving to avoid duplicate established work.

### 4. Apply failure recovery

| Failure | Diagnose | Next move |
|---|---|---|
| no fact can be submitted | verify service unavailable or role lacks tool | restore verify service / use a worker role; do not bypass gate |
| verifier says wrong | logical error, gap, vague citation, unproved premise, or bad reference | repair all findings; resubmit the same substantive claim |
| same plan repeatedly stalls | subgoal false/too strong, missing interface, poor decomposition | counterexample search → failure synthesis → new decomposition |
| fact revoked | descendants depend on invalid premise | treat cascade as invalid; re-prove from surviving facts or switch route |
| workers appear idle/stuck | inspect status, round age, assignment, deadline/failure count | sharpen assignment, restart from persisted stores, or stop deliberately |
| paper target unset | no operator-approved target | finalize/select target; writer must not guess |
| paper closure large | writer context would become flat or overflow | curate a support layer; recursively split deep results into separately written pieces |
| citation unresolved | offline audit cannot confirm metadata | keep blocker; run online reference verification; never fill from memory |
| paper compile fails | local LaTeX error | targeted patch + recompile; quarantine persistent failure |
| paper math gate finds must-fix gaps | rendered paper lost a load-bearing derivation | add selected verified facts or precise confirmed citations, revise, and reverify |
| human report leaks internal identifiers | scrub/isolation failed | quarantine output and regenerate; do not deliver leaked report |

### 5. Self-check before answering or acting

- Is the user's actual outcome clear, and is this the correct route?
- Which statements are verified facts, which are shared findings, and which are fresh hypotheses?
- Are all method preconditions met, including role permissions and service availability?
- Did any step silently depend on global memory, a subagent report, or a problem statement as if it were proof?
- Were counterexamples tested before declaring a resistant subgoal merely difficult?
- Are important route changes, parked alternatives, and revisit conditions preserved?
- Does every downstream-used intermediate result have verifier acceptance?
- For reports/papers, did internal identifiers, fabricated citations, compile errors, or must-fix mathematical gaps survive?
- If evidence is insufficient, return that limitation and the next discriminating check.

## Core frameworks

### Produce → share → verify → trust

A raw idea starts private, becomes a typed shared finding when useful to others, and becomes trusted only through verifier acceptance. This prevents social consensus among agents from becoming mathematical truth.

### Portfolio strategy, not local momentum

The main agent maintains a **route portfolio** of several credible routes, their frontiers, decisive obstacles, evidence, assignments, and revisit conditions. A 30-minute control beat refreshes the global view; a roughly four-hour macro audit forces explicit comparison of routes and resource allocation.

### Falsification before persistence

A blocked subgoal is stress-tested for falsity or missing hypotheses before more proof effort. Repeated failures become reusable shared knowledge, then feed a new planning round.

### Curate before rendering

Human reports and papers are separate authoring systems fed by verified mathematics. Paper generation begins with an explicit target and a curated support layer; citation, compilation, leak, and whole-document mathematics checks remain hard gates.

## Supporting files

- [Glossary](glossary.md) — Danus terms and role vocabulary.
- [Patterns](patterns.md) — reusable operational patterns and anti-patterns.
- [Cheatsheet](cheatsheet.md) — routing decisions, thresholds, commands, and recovery rules.
