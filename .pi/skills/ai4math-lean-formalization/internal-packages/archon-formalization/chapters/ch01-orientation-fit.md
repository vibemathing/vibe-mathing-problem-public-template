# Chapter 1: Orientation and Fit

## Core Idea
Archon is an orchestration system for long-running, repository-scale Lean 4 formalization. Its advantage appears when mathematical planning, dependency structure, many Lean files, repeated proof attempts, and review state must stay coherent across iterations.

## When to Use
Use Archon when several of these are true: many interdependent declarations; informal source material must become LeanBlueprint; the proof graph matters; work spans multiple iterations or agents; you need reproducible state/history; multiple project variants share proof work.

Avoid adding Archon overhead to a single local theorem unless that theorem belongs to a larger Archon project. For an isolated goal, use Lean LSP/search/tactic workflows directly.

## Operating Layers
1. **Mathematical model** — strategy + blueprint prose + dependency DAG.
2. **Execution model** — Lean declarations, prover objectives, local helpers.
3. **Control loop** — plan, prove, deterministic checks, review, finalize.
4. **State/history** — `.archon/`, proof journal, iteration sidecars, inner git.
5. **Optional scaling** — subagents, alternative harnesses, multilane races, peer scope.

## Typical Entry Flow
`archon setup` → enter project → `archon init .` → optional/recommended `archon dag` → `archon loop` → `archon discuss` for human steering → `archon dashboard` for inspection.

## Decision Rule
If the bottleneck is **proof search inside one goal**, reach for Lean tooling. If the bottleneck is **coordinating the mathematical route, dependency graph, many proof goals, and repeated attempts**, reach for Archon.

## Failure Smell
A weaker model or poorly grounded blueprint can make orchestration overhead harmful. If agents keep rephrasing plans without Lean progress, treat that as a convergence failure and change routing, decomposition, or model/harness rather than increasing iteration count blindly.

## Source Provenance
Primary: `README.md`, `src/archon/cli.py`; corroborated by the loop, DAG, dashboard, and test suites.

## Frameworks Introduced
- **Scale-fit routing**: Use Archon when the unit of work is a project graph rather than a single goal. The decision input is coordination cost: dependencies, source material, repeated attempts, multi-file state, and cross-iteration memory.
  - When to use: a repository has several interdependent declarations or a research text must be formalized progressively.
  - How: classify the task as local proof, project orchestration, or cross-project orchestration; load only the corresponding layer.
- **Separation of strategic and tactical context**: planning carries long-horizon mathematical intent; prover sessions stay file/objective focused. This reduces context explosion while keeping tactical sessions accountable to a global route.

## Key Concepts
- **Project-level formalization**: formalization where progress depends on a graph of declarations and files.
- **Orchestration overhead**: the state, prompts, reviews, and graph maintenance required to coordinate autonomous work.
- **Ready frontier**: dependency-ready work that can produce useful proof progress now.
- **Control plane**: `.archon/` state plus prompts, config, history, and reports used to steer Lean execution.

## Mental Models
- Think of Archon as a **proof-program build system with strategic scheduling**: mathematical dependencies are the build graph; provers are workers; review and deterministic checks are CI.
- Use the **coordination-cost test**: if keeping agents aligned costs more than proving the next local goal, Archon can repay its overhead.

## Anti-patterns
- **Archon for every Lean question**: adds graph/state cost where direct LSP and tactic search would solve the problem faster.
- **Activity as progress**: many agent turns or long logs can coexist with a flat sorry count and unchanged dependency frontier.
- **Model substitution for structure**: changing the model cannot repair a false theorem, broken DAG, or missing source provenance.

## Worked Example
A user has `Topology/A.lean`, `Topology/B.lean`, and `Main.lean`, plus a paper with an informal proof. `Main` depends on both modules and previous single-session proving repeatedly loses why helper lemmas exist. Route to Archon: initialize; encode the paper in blueprint chapters; build the DAG; prove dependency-ready files; review actual blockers. For a separate question “why does this `simp` fail in `A.lean`?”, route directly to Lean tooling inside the project rather than invoking a new Archon orchestration cycle.

## Key Takeaways
1. Trigger on coordination complexity, not on the word “Lean”.
2. Build project state when long-horizon context and reversibility matter.
3. Measure progress using proof/build/DAG evidence.
4. Fix structural causes before paying for more agent attempts.

## Connects To
- **Ch 02**: bootstraps the control plane.
- **Ch 03**: turns mathematical structure into a dependency graph.
- **Ch 07**: measures whether orchestration is converging.
