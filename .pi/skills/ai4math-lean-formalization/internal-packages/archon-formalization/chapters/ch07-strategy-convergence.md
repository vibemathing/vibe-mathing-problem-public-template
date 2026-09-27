# Chapter 7: Strategy, Objectives, and Convergence

## Core Idea
An Archon iteration should spend proof budget on a dependency-ready frontier and produce measurable Lean progress. Objective count, build blockers, and repeated failure patterns are control signals.

## Objective Selection
Prefer files whose dependencies are ready and whose completion advances the goal cone. The planner may propose many objectives, but validation enforces a bounded dispatch and carries deferred work forward as automatic notes.

## Blocked Dependency Rule
If the previous build failed in a local Lean file, downstream files importing that failure transitively are poor objectives. Drop them unless the blocking file is itself scheduled to be fixed in the same iteration; that exception allows a blocker and its dependents to be assigned together.

## Convergence Signals
- **CONVERGING** — sorry count falls, meaningful proof branches close, or reusable compiling helpers appear.
- **CHURNING** — helpers/comments multiply while target sorries stay flat; repeated partial verdicts recycle the same routes.
- **STUCK** — a named blocker persists despite appropriate attempts and decomposition.
- **UNCLEAR** — evidence is too weak or noisy; improve logging/measurement before choosing a strategy.

## Corrective Routes
For churn: reduce objective breadth; strengthen the blueprint proof; split high-effort claims; run fine-grained mode; ask a strategy critic to challenge sunk-cost choices; verify Mathlib analogies; or reroute around a false premise. For blocked build chains: fix the earliest blocker first. For a load-bearing claim that may be false, test small countermodels or assumptions before spending large proof budget.

## Progress Accounting
Lean code changes count: closed sorries, compiling helper lemmas, or a partial tactic body that reaches a precise stuck state. Comments and task-result prose are evidence, not proof progress.

## Source Provenance
Primary: plan prompt, progress/strategy critics, `plan_validate.py`, `blocked_deps.py`, and their tests.

## Frameworks Introduced
- **Bounded ready-frontier dispatch**: keep each iteration's objectives small enough to generate interpretable feedback.
- **Blocked-import filter**: use prior build failures plus local import closure to remove objectives that cannot compile yet.
- **Convergence classification**: use quantitative and qualitative signals to label routes CONVERGING, CHURNING, STUCK, or UNCLEAR.
- **Falsification before investment**: challenge load-bearing mathematical claims with small cases/source checks before allocating large proof budgets.

## Key Concepts
- **Dispatch cap**: deterministic upper bound on concurrently selected objectives; overflow is deferred into automatic notes.
- **Presumed-being-fixed exception**: a blocked file scheduled this iteration does not automatically block its downstream co-assigned objective.
- **Helper churn**: accumulating auxiliary declarations without reducing the target blocker.
- **Throughput drift**: actual progress falling materially behind strategy expectations.

## Mental Models
- View objective selection as **critical-path scheduling** on a dependency graph.
- View repeated partials as **data about the route**, not an instruction to retry indefinitely.

## Anti-patterns
- **Wide fan-out on a broken base**: burns agents on downstream files that cannot elaborate.
- **Sunk-cost strategy**: keeps the same route because many iterations already invested in it.
- **Cosmetic progress accounting**: treats renamed sorries, comments, or task prose as equivalent to compiled proof advances.

## Worked Example
The previous build fails in `Core.lean`. Planner proposes `Core.lean`, `Algebra.lean`, and eight downstream files. Import-graph validation sees `Algebra` and six files depend on `Core`. Because `Core` is co-assigned, `Algebra` may stay if ordering supports it; unrelated downstream work over the cap is deferred. After two rounds, `Core` still has the same two sorries while five helpers were added. Mark CHURNING, run a fresh strategy critique, strengthen/decompose the blueprint, and dispatch one smaller route instead of increasing parallelism.

## Key Takeaways
1. Schedule dependency-ready work.
2. Bound each feedback cycle.
3. Separate measurable Lean progress from documentation activity.
4. Switch routes when evidence says a path is churning.

## Connects To
- **Ch 03**: graph quality determines frontier quality.
- **Ch 05**: mode changes are one response to churn.
- **Ch 14**: failure classifier turns signals into recovery actions.
