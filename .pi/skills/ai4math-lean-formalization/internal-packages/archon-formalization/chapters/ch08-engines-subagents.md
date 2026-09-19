# Chapter 8: Engines, Backends, and Subagents

## Core Idea
Archon separates *which engine runs a role* from *how Claude Code is launched*. Keep harness and backend concepts distinct, then use descriptor-scoped subagents only when focused fresh-context work adds value.

## Harness vs Backend
- **Harness** selects the execution engine for plan/prover/review/subagents (for example Claude Code or Codex).
- **Claude backend** selects the launch path for Claude Code (default, VS Code/desktop entrypoint, `claude-p`, or interactive mode).

Role-specific settings override loop-wide settings. Subagent-specific harnesses can override the loop harness. Interactive Claude mode forces serial behavior and disables multilane.

## Subagent Model
Descriptors declare purpose, write domain, read-only status, spawn permission, defaults, and optional recommended phase. The dispatcher enforces write-domain relationships. Enabled subagents are injected into plan/review context so the parent need not rediscover them.

Useful roles include blueprint reviewer/writer/cleaner, DAG walker, effort breaker, strategy/progress critics, Mathlib analogist, reference retriever, refactor, Lean auditor, and Lean-vs-blueprint checker.

## Dispatch Discipline
Subagent dispatch is synchronous. Consume a result only after its report exists. To run independent subagents concurrently, launch the wave together and wait for the whole wave. Serialize agents that write the same files.

## When to Spawn
Spawn when the task benefits from isolation: unbiased strategy critique, whole-blueprint audit, source retrieval, per-file blueprint comparison, structural refactor, or focused decomposition. Avoid subagent fan-out when one direct check is cheaper and sufficient.

## Failure Cases
A missing provider/model/key should not silently rewrite the intended workflow. Diagnose the configured harness/backend and available credentials. In multilane mode a missing lane key can disable that lane while remaining lanes continue.

## Source Provenance
Primary: `docs/CONFIGURATION.md`, `AGENTS.md`, subagent descriptors, harness router and registry tests.

## Frameworks Introduced
- **Orthogonal engine configuration**: harness answers “which engine?”, backend answers “how is Claude launched?”. Keep the dimensions separate.
- **Scoped fresh-context delegation**: subagents receive narrow directives and explicit write domains, reducing context contamination and write conflicts.
- **Blocking result discipline**: a parent must not act on a child result until the dispatch returns and the report exists.

## Key Concepts
- **Role override**: plan/prover/review can select different harnesses.
- **Descriptor**: subagent metadata for name, purpose, write domain, read-only flag, spawn capability, defaults, and phase recommendation.
- **Write-domain subset**: spawned children cannot exceed parent authority.
- **Interactive backend**: foreground human-driven mode that forces serial execution.

## Mental Models
- Treat harness selection like **choosing a compiler/runtime** and backend like **choosing the launcher**.
- Treat subagents like **typed function calls with filesystem effects**, not free-roaming parallel conversations.

## Anti-patterns
- **Bare string confusion**: role strings and subagent model aliases have different semantics; follow config schema/precedence.
- **Parallel writers to the same file**: creates races and invalidates focused review.
- **Non-blocking monitoring as waiting**: parent may finish before the subagent result exists.
- **Enable every subagent by default**: extra context/cost can exceed the value of fresh critique.

## Worked Example
Use Claude for planning but Codex for proving. Set the loop harness or per-role override so `plan` resolves to Claude Code and `prover` to Codex. Enable `strategy-critic` and `blueprint-reviewer` for planning. Dispatch both in one parallel wave only because each writes its own report. If two blueprint writers target the same chapter, serialize them. If Claude runs through the interactive backend, expect serial execution and no multilane regardless of prover intent.

## Key Takeaways
1. Resolve config precedence before debugging model behavior.
2. Give subagents the narrowest useful write scope.
3. Parallelize independent reports; serialize conflicting writers.
4. Treat missing reports as unfinished work.

## Connects To
- **Ch 09**: permission boundaries and safe mode.
- **Ch 10**: multilane adds provider-level parallelism.
- **Ch 13**: logs reveal which harness/subagent actually ran.
