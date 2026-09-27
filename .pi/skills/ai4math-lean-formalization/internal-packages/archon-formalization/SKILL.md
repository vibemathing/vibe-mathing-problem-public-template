---
name: archon-formalization
description: "Operational knowledge from the Archon v0.3.3 repository. Use for project-scale Lean 4 formalization with Archon: initializing or upgrading projects, building LeanBlueprint/LeanDag dependency graphs, running the plan→prove→review loop, choosing prover modes, configuring Claude/Codex harnesses and subagents, using safe mode and protected declarations, recovering with inner git, enabling multilane proving, coordinating peer projects, or diagnosing stalled Archon runs."
---

<!-- argument-hint: [project path, Archon command, failure symptom, or workflow question] -->

# Archon Formalization
**Source**: Archon v0.3.3 repository corpus | **Generated**: 2026-09-12 | **Coverage**: 116 documentation sources + code/test corroboration

## Use / Do Not Use
Use this skill when the work is repository-scale Lean 4 formalization, Archon configuration/operation, blueprint-DAG planning, autonomous proof orchestration, or Archon recovery/diagnostics.

For one isolated Lean theorem, a local tactic question, or generic Lean syntax, use the Lean 4 skill directly. For Coq/Isabelle/Agda or generic project management, route elsewhere.

## Routing
1. **No Archon project yet** → `ch02`; initialize, then validate setup.
2. **Dependencies or blueprint are unclear** → `ch03`; run DAG/doctor before expensive proving.
3. **Ready to formalize** → `ch04`; run plan → prove → deterministic checks → review → finalize.
4. **Need a proof strategy for one objective** → `ch05` then `ch06`.
5. **Loop is stalling** → `ch07` + `ch14`; classify churn, blocked deps, false completion, or infrastructure gap.
6. **Need engine/subagent choices** → `ch08`; backend and harness are separate knobs.
7. **Need stronger isolation or immutable surfaces** → `ch09`.
8. **Want provider races** → `ch10`.
9. **Need source-grounded math** → `ch11`.
10. **Need cross-project reuse** → `ch12`.
11. **Need status/cost/diagnostics** → `ch13`.

## Core Operating Model
- Treat the **blueprint DAG as the mathematical contract** and Lean files as executable realizations. Maintain one-to-one coverage; new helpers create blueprint debt until registered.
- Separate **strategic intent** from **proof execution**. The plan agent selects routes/objectives; provers own tactical decisions inside assigned files; review audits actual attempts and project state.
- Prefer deterministic gates over narrative confidence: Lean build, DAG/blueprint checks, `sync_leanok`, axiom sweep, plan validation, protected-surface checks, and inner-git state.
- Dispatch work from the **ready dependency frontier**. Downstream files with failed local imports are poor objectives unless the blocking file is also being fixed in the same iteration.
- Treat repeated partial work with flat sorry counts as a routing signal. Decompose the theorem, strengthen the blueprint, switch prover mode, build a missing local abstraction, or change strategy.
- Preserve intended statements. When proof work fails, keep the correct signature and a visible scoped gap; do not weaken the theorem to manufacture progress.
- Ground load-bearing mathematics in the actual reference files. Mark verified APIs separately from expected names and known gaps.
- Recovery is part of normal operation: resume interrupted phases; use Archon's inner git to fork before risky structural changes or return to a known-good timeline.

## Fast Decision Table
| Situation | Action |
|---|---|
| New repo or informal notes | `archon init .`; inspect `.archon/config.json`, protection, tools |
| Blueprint absent/incoherent | `archon dag`; repair until DAG gate passes |
| Empty Lean file with blueprint declarations | prover mode `formalize` |
| Normal compiling file with sorries | `prove` |
| Large theorem repeatedly stalls | `fine-grained`; atomize blueprint sentences |
| Verified missing Mathlib ingredient | `mathlib-build` |
| All proofs close; quality remains | `polish` |
| Want smaller proof terms | `golf` |
| Interrupted iteration | `archon loop --resume` |
| Bad agent timeline | inspect `archon log`; fork/switch with `archon branch` |
| Writes must stay inside workspace | `archon loop --safe` |
| Related projects duplicate work | `archon scope roadmap`, then extract/merge as appropriate |

## Failure Recovery
Before repeating the same attempt, identify the failure class: mathematical strategy, missing infrastructure, dependency blockage, blueprint debt, environment/toolchain, provider/quota, protection conflict, or orchestration state. Load `ch14` for the recovery ladder.

## Self Check
Before giving an Archon recommendation, verify: project-scale fit; current stage; blueprint/DAG readiness; protected surfaces; required inputs; chosen prover mode; local import blockers; whether source grounding is needed; whether the proposed success condition is mechanically testable; and which recovery path applies if the first route fails.

## Chapter Index
| # | Topic | File |
|---|---|---|
| 01 | Orientation & fit | [ch01](chapters/ch01-orientation-fit.md) |
| 02 | Bootstrap & state | [ch02](chapters/ch02-bootstrap-state.md) |
| 03 | Blueprint & DAG | [ch03](chapters/ch03-blueprint-dag.md) |
| 04 | Plan→prove→review | [ch04](chapters/ch04-loop.md) |
| 05 | Prover modes | [ch05](chapters/ch05-prover-modes.md) |
| 06 | Lean execution | [ch06](chapters/ch06-lean-execution.md) |
| 07 | Strategy & convergence | [ch07](chapters/ch07-strategy-convergence.md) |
| 08 | Engines & subagents | [ch08](chapters/ch08-engines-subagents.md) |
| 09 | Safety & recovery | [ch09](chapters/ch09-safety-recovery.md) |
| 10 | Multilane | [ch10](chapters/ch10-multilane.md) |
| 11 | References & provenance | [ch11](chapters/ch11-references.md) |
| 12 | Extract/merge/scope | [ch12](chapters/ch12-cross-project.md) |
| 13 | Observability | [ch13](chapters/ch13-observability.md) |
| 14 | Completion & failure playbook | [ch14](chapters/ch14-completion-failures.md) |

## Topic Index
- **archon-protected.yaml** → ch09
- **axioms / sorryAx** → ch06, ch14
- **backend / harness / Codex** → ch08
- **blueprint-doctor / LeanDag** → ch03, ch14
- **blocked dependencies / objectives** → ch07
- **branch / resume / rollback** → ch09, ch14
- **extract / merge / peers / scope** → ch12
- **fine-grained / formalize / mathlib-build / polish / golf** → ch05
- **multilane** → ch10
- **plan / prover / review** → ch04
- **references / anti-fabrication** → ch11
- **safe mode** → ch09
- **subagents** → ch08

## Supporting Files
- [glossary.md](glossary.md) — terminology
- [patterns.md](patterns.md) — reusable operational patterns
- [cheatsheet.md](cheatsheet.md) — decision rules and gates

## Scope & Limits
This skill captures Archon v0.3.3 as present in the supplied archive. Commands, model names, provider defaults, and product behavior may change in later releases. When working against a different installed Archon version, check `archon version`, local help, and the installed project prompts before applying version-specific details.
