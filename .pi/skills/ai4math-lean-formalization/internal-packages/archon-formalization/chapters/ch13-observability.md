# Chapter 13: Observability and Diagnostics

## Core Idea
Archon exposes enough state to distinguish mathematical failure from orchestration, toolchain, provider, or bookkeeping failure. Use the dashboard and deterministic reports as debugging instruments.

## Dashboard Views
The dashboard can surface iteration logs, plan/prover/review streams, per-file/lane activity, token/cost information, git history, proof journal, an interactive DAG, and rendered blueprint content. Use it to answer: what ran, what changed, where the current dependency frontier is, and whether cost is buying progress.

## Diagnostic Sources
- `archon doctor` for setup/toolchain health;
- loop `meta.json` and phase logs for interrupted/resume state;
- task result files for prover-specific blockers;
- proof journal for cross-iteration attempt history;
- blueprint-doctor reports for structural debt;
- axiom-sweep reports for hidden assumptions;
- `sync_leanok-state.json` for marker attribution;
- inner-git log/diffs for exact agent changes.

## Debugging Order
1. Reproduce the symptom and identify the failing layer.
2. Check version/prompt drift and project-local configuration.
3. Check deterministic build/DAG/doctor reports.
4. Inspect the exact agent stream/task result for the failure.
5. Change one configuration/strategy variable at a time.

## Cost Visibility
High token use with flat proof/DAG progress is a routing signal. Use cost/log data together with convergence metrics; do not treat activity volume as progress.

## Source Provenance
Primary: README dashboard sections, dashboard commands/UI, session logging/cost state, doctor and resume tests; visual inspection of supplied dashboard screenshots.

## Frameworks Introduced
- **Layered diagnosis**: classify environment, orchestration, structural math, proof execution, and provider failures before changing strategy.
- **Evidence triangulation**: combine dashboard event streams, deterministic reports, task results, and git diffs rather than trusting one summary.
- **Cost-to-progress check**: compare token/USD/turn activity with proof and DAG movement.

## Key Concepts
- **Iteration metadata**: phase/session state used for resume and chronology.
- **Proof journal**: review-derived record of actual proof attempts and reusable outcomes.
- **DAG view**: dependency visualization for frontier/coverage investigation.
- **Blueprint view**: rendered source-aware mathematical plan and proof markers.
- **Static export**: self-contained dashboard build for publishing/inspection where configured.

## Mental Models
- Use observability as a **debugger for an autonomous system**: reconstruct causality from events and state transitions.
- A large log is a **trace**, not a verdict. Correlate it with repository diffs and deterministic gates.

## Anti-patterns
- **Debug by prompt editing first**: environment/version/config failures can mimic reasoning failures.
- **Read only the final assistant summary**: it may omit the exact tool error that explains the blocker.
- **Optimize token cost without progress context**: cheaper churn is still churn.

## Worked Example
A loop appears frozen after a prover session. Dashboard shows no review event. Inspect iteration metadata: prover finished but the process was interrupted before deterministic sync. Task results exist and inner git contains the prover commit. Use `--resume` rather than restarting the entire iteration. If the dashboard instead shows repeated prover sessions with identical sorry counts and rising cost, route to convergence analysis rather than resume logic.

## Key Takeaways
1. Diagnose the layer before changing the plan.
2. Correlate logs with state and diffs.
3. Use resume metadata for interruptions.
4. Treat cost without proof progress as a routing signal.

## Connects To
- **Ch 04**: phase artifacts explain loop chronology.
- **Ch 07**: progress metrics classify convergence.
- **Ch 09**: git history gives exact reversible state.
