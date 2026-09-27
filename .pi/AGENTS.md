# Pi Mathematical Skills Guide

This directory contains the fixed, project-local Skills available to the single-problem Pi research workflow. Pi loads them only after project trust is granted. The repository does not vendor user-level Skills, activate upstream repositories, or grant any Skill authority over Evidence, Result, or Solution admission.

## Mandatory reasoning discipline

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

Every selected Skill inherits `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md`: definition/scope freeze precedes derivation; dependencies and explicit witnesses must be reviewable; candidates must face counterexamples, invariants, monovariants/termination, extremal/symmetry/probability assumptions, scale/boundary checks, and evidence ceilings. Finite testing is not induction, and contraposition cannot reverse or invert an implication.

Pi discovers only the exact mathematical Skill entries declared in `.pi/settings.json`. That file also pins `npm:pi-goal-x@0.31.9` as a **Pi extension**, not an extra Skill; its `.pi/npm/` project install cache is Git-ignored and checked against reviewed package bytes, never vendored into the public snapshot. Project defaults in `.pi/pi-goal-x-settings.json` disable Goal-created task lists and bound transport retries, but loading the extension neither creates a Goal nor starts template research. The opt-in maintainer Skill in `.pi/opt-in-skills/` is not auto-loaded and must never be injected into the mathematical actor. Only a concrete, admitted actor may use `/goal-direct` after checking `/goal-status`, session, lease, repository-external private `PI_GOAL_ROOT`, write boundary and old scheduler ownership; see `TEMPLATE_REPOSITORY.md`. The optional `.pi/opt-in-extensions/local-write-guard.ts` is **not** a Skill and is not auto-activated: it needs an explicit trusted local launch with a private policy, and it cannot schedule research. Legacy HookLoop and Goal must not both own continuation. The canonical research actor may select or combine the relevant mathematical Skills without surrendering route choice to a router:

```text
ai4math-source-discovery
ai4math-modeling-derivation
ai4math-proof-refutation
ai4math-bounded-computation
ai4math-lean-formalization
mathematics-in-lean
prove2me
ai4math-toolchain-reproducibility
ai4math-assurance-admission
```

Bounded computation and Lean execution are constrained by runtime availability and receipts. Prove2me network/submission actions require explicit authorization. Assurance output is a candidate-only recommendation and cannot sign or admit Evidence, Results, or Solutions. `continuous-research-takeover`, `pi-session-fleet-manager`, `nvidia-private-compute`, `auto-goal`, `auto-tmux`, compute-node orchestration, and session control are excluded from single-problem research repositories.

Search registered mathematical knowledge sources before inventing new machinery. Respect exact versions, licenses, source maturity, operational status, external effects, and evidence ceilings. A Skill is a method contract, not a strategy authority, verifier identity, or evidence level.
