---
name: lean-eval-comparator
description: "Operational knowledge from the Lean Eval repository snapshot for diagnosing comparator setups, validating LeanEval workspaces, interpreting scores, auditing landrun/nanoda security, handling multi-hole problems, and checking dependency-pin drift. Use when a task mentions LeanEval, comparator, lake test in generated/workspaces, check-comparator-installation, run-eval, landrun, lean4export, nanoda, or comparator pin/security changes."
---

<!-- argument-hint: [install | diagnose | score | security | pins | authoring | problem-id] -->

# Lean Eval Comparator Operations

**Source**: uploaded Lean Eval repository snapshot | **Corpus**: 3,977 readable files | **Operational sections**: 10 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill for LeanEval's comparator-based evaluation path. Start with the task router, load only the chapter needed, then apply the self-check before reporting success.

| User goal / signal | Load |
|---|---|
| Comparator install, `lake test`, missing binary, olean header error | [ch02](chapters/ch02-installation-and-preflight.md), then [ch06](chapters/ch06-failure-diagnosis.md) |
| Why a workspace counts as attempted/passed/failed; `run-eval` output | [ch04](chapters/ch04-scoring-and-eval-semantics.md) |
| What `Challenge` / `Submission` / `Solution` mean | [ch01](chapters/ch01-architecture-and-trust-boundary.md) |
| Nanoda or `WorkspaceTest` behavior | [ch03](chapters/ch03-workspace-execution-and-nanoda.md) |
| Add/edit a benchmark problem; manifest or generated-workspace drift | [ch05](chapters/ch05-authoring-generation-and-catalog-integrity.md) |
| Sandbox, permitted axioms, threat model | [ch07](chapters/ch07-security-model-and-invariants.md) |
| Run or interpret security probes | [ch08](chapters/ch08-security-probes-and-regression-gates.md) |
| Bump comparator/landrun/lean4export/nanoda; reconcile pins | [ch09](chapters/ch09-pin-governance-and-drift.md) |
| `def`/`instance` holes, `definition_names`, spec-strength review | [ch10](chapters/ch10-multi-hole-and-spec-quality.md) |

## Core Frameworks & Decision Rules

### 1. Three-artifact proof boundary
Treat every generated problem as three roles: **Challenge** is the trusted statement, **Submission** is solver-controlled proof code, and **Solution** is the fixed bridge that references the submission. Use this model before diagnosing any acceptance question. Editing trusted files invalidates the normal solver workflow.

Comparator separately builds/exports Challenge and Solution, compares the reachable constant graph, checks reachable axioms against the allowlist, then kernel-replays the result. For definition-hole targets, body equality is relaxed to type compatibility; this shifts part of correctness to the benchmark specification.

### 2. Installation truth is a capability test
A version string alone is weak evidence. For `landrun`, verify required flags and that it can execute the active Lean toolchain under the policy. The canonical happy-path check is:

```bash
lake exe lean-eval check-comparator-installation
```

It validates landrun, copies the generated `two_plus_two` workspace, replaces the starter proof with a known-good proof, runs `lake update`, fetches the cache, and runs `lake test` end to end.

### 3. Prefer runtime authority over example prose
When pins conflict inside a snapshot, use this order for operational advice:

1. Exact immutable pin used by CI and the security pin table.
2. Executable validation code tied to that pin.
3. README setup examples.

This snapshot contains a real drift: the README's lean4export checkout differs from `SECURITY.md` and CI. Flag the inconsistency and use the security/CI pin for reproducible setup.

### 4. Scoring is pristine-vs-edited first, comparator second
`run-eval` renders the expected workspace, compares it with the selected workspace, and calls a problem **attempted** only when mismatches exist. For an attempted workspace, success means `lake test` exits zero. A directory can exist and still be unattempted if it matches the generated baseline.

### 5. Nanoda is enforced at invocation
Do not infer that `"enable_nanoda": false` in committed `config.json` disables the independent kernel. `WorkspaceTest.lean` reads the config, overrides that field to true in a temporary config, then invokes comparator. Treat nanoda as a global evaluation requirement.

### 6. One untrusted elaboration boundary
For security reasoning, locate the only intended elaboration of solver code: comparator's sandboxed `safeLakeBuild Solution`, which transitively builds Submission. If a change causes user-controlled Lean to elaborate earlier on the runner, classify it as a security regression until proven otherwise.

### 7. A pin bump is a security re-audit
Changing comparator, landrun, Lean, lean4export, or nanoda can change sandboxing, export semantics, process lifetime, environment visibility, or kernel checking. Update lockstep pin sites, run mandatory probes, rerun one-shot probes, and revise the security model when a probe verdict changes.

### 8. Definition holes need semantic specification
Comparator's `definition_names` path requires matching types, not identical bodies. For every `def` or `instance` hole, ask whether trusted theorem statements sufficiently constrain the intended semantics. If they do not, comparator can accept a type-correct but semantically trivial replacement. This requires author/reviewer judgment.

## Standard Operating Procedure

1. **Classify**: installation, proof/workspace, scoring, authoring, security, or pin governance.
2. **Collect minimum evidence**: repo root, problem id if relevant, exact failing command, exit code, and error tail. For scoring, prefer `run-eval --json`.
3. **Check source authority**: compare the active toolchain/pins with `SECURITY.md` and CI before repeating setup commands.
4. **Run the narrowest canonical check**: single workspace before catalog-wide checks; install smoke test before debugging a real theorem.
5. **Separate environment from proof**: prove the starter problem pipeline works before blaming user proof code.
6. **Apply recovery**: follow [ch06](chapters/ch06-failure-diagnosis.md) and change one layer at a time.
7. **Validate**: rerun the same failing command plus one adjacent invariant check.
8. **Report evidence**: state commands actually executed, outputs observed, and anything that could not be tested.

## Fast Command Map

```bash
# install / full comparator smoke
lake exe lean-eval check-comparator-installation

# one workspace
cd workspaces/<problem-id>
lake test

# score locally
lake exe lean-eval run-eval --json

# repo-level workflow smoke
lake exe lean-eval check-eval-workflow

# contributor regeneration/build
lake exe lean-eval generate --problem <problem-id>
lake exe lean-eval check-generated-builds --problem <problem-id>
```

## Failure Recovery

- **Missing tool** → verify `PATH`; install the immutable project pin; rerun the starter smoke test.
- **Landrun looks new enough but fails** → inspect flags and run the functional Lean-toolchain probe; do not trust the displayed version alone.
- **`incompatible header` reading an olean** → treat as Lean/olean version mismatch or stale build artifacts; rebuild lean4export/comparator against the repository toolchain and clear the affected `.lake/build`.
- **Nanoda missing** → fix `nanoda_bin` visibility; editing `config.json` is not a bypass because the harness forces nanoda on.
- **`run-eval` says unattempted** → inspect workspace mismatches; an unchanged copy is intentionally unattempted.
- **Proof rejected after starter smoke passes** → move from environment diagnosis to theorem/import/submission diagnosis.
- **Security probe cannot execute** → report the platform/tool blocker. Never convert a skip into a security pass.
- **Pin sources disagree** → report drift, use CI/security authority for the current snapshot, then reconcile documentation.

## SELF_CHECK

Before finalizing an answer or change:

- Did I classify the task and load the relevant chapter?
- Did I distinguish trusted benchmark files from solver-owned files?
- Did I verify the source of any pin I quoted?
- Did I distinguish an environment failure, workspace drift, proof rejection, and security regression?
- Did I remember that `WorkspaceTest` forces nanoda on?
- For `def`/`instance` holes, did I check semantic constraints rather than only types?
- For security claims, did I account for the writable-`.lake` persistent-child limitation?
- Did I say which tests really ran and which were blocked/skipped?
- If the user's checkout may be newer than this snapshot, did I request/inspect current repo files before treating these pins as current?

## Chapter Index

| # | Operational section | Main capabilities |
|---|---|---|
| [ch01](chapters/ch01-architecture-and-trust-boundary.md) | Architecture & trust boundary | Challenge/Submission/Solution, comparator checks, authority |
| [ch02](chapters/ch02-installation-and-preflight.md) | Installation & preflight | pins, landrun validation, starter smoke |
| [ch03](chapters/ch03-workspace-execution-and-nanoda.md) | Workspace execution & nanoda | file ownership, invocation, independent kernel |
| [ch04](chapters/ch04-scoring-and-eval-semantics.md) | Scoring & eval semantics | attempted/succeeded, workspace preference, JSON |
| [ch05](chapters/ch05-authoring-generation-and-catalog-integrity.md) | Authoring & generation | manifests, holes, regeneration, build checks |
| [ch06](chapters/ch06-failure-diagnosis.md) | Failure diagnosis | symptom routing and recovery |
| [ch07](chapters/ch07-security-model-and-invariants.md) | Security model | sandbox boundary, axioms, known limitation |
| [ch08](chapters/ch08-security-probes-and-regression-gates.md) | Security probes | probe matrix, verdict interpretation |
| [ch09](chapters/ch09-pin-governance-and-drift.md) | Pin governance | lockstep updates, drift detection |
| [ch10](chapters/ch10-multi-hole-and-spec-quality.md) | Multi-hole/spec quality | `definition_names`, named instances, author review |

## Topic Index

- **attempted vs succeeded** → ch04
- **axioms / `sorryAx` / `native_decide`** → ch07
- **Challenge / Submission / Solution** → ch01, ch03
- **COMPARATOR_BIN** → ch03, ch06
- **definition holes / instance holes** → ch10
- **generated workspace stale** → ch05, ch06
- **incompatible olean header** → ch02, ch06
- **landrun flags / version** → ch02, ch07
- **nanoda** → ch03, ch07, ch09
- **pin bump / dependency drift** → ch09
- **sandbox / environment allowlist** → ch07, ch08
- **security probes** → ch08
- **`run-eval --json`** → ch04

## Supporting Files

- [glossary.md](glossary.md) — LeanEval/comparator terminology
- [patterns.md](patterns.md) — reusable operational procedures
- [cheatsheet.md](cheatsheet.md) — compact decision tables and defaults

## Scope & Limits

This skill captures the uploaded Lean Eval repository snapshot, with emphasis on comparator evaluation. It can diagnose and guide operations from the snapshot without the original archive. It does not replace the current upstream repository for future pin changes, and it does not solve arbitrary Lean mathematics by itself.
