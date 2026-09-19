# Patterns

## Starter-Smoke Isolation
**When to use**: a real benchmark proof fails and the cause may be environment-related.  
**How**: run `lake exe lean-eval check-comparator-installation` on the known-good `two_plus_two` path before inspecting theorem tactics. If it fails, stay in environment diagnosis. If it passes, focus on the target workspace.  
**Trade-offs**: adds one end-to-end run but sharply reduces mixed-layer debugging.

## Capability-First Landrun Check
**When to use**: validating or upgrading landrun.  
**How**: verify required flags, exact pin, and actual execution of the active Lean toolchain under the sandbox. Treat version text as secondary evidence.  
**Trade-offs**: more work than `landrun --version`; catches tagged builds lacking required behavior.

## Authority-Ladder Pin Resolution
**When to use**: README, security docs, workflows, and executable constants disagree.  
**How**: prefer active CI/security pin table and executable enforcement over setup prose; report the conflict and repair all sites.  
**Trade-offs**: snapshot-specific; for a newer checkout always re-read its authority files.

## Baseline-Diff Scoring
**When to use**: interpreting `run-eval`.  
**How**: determine `attempted` from workspace mismatches against regenerated expected files; run `lake test` only for attempted problems; interpret exit zero as succeeded.  
**Trade-offs**: an unchanged copied workspace is intentionally unattempted.

## Invocation-Time Nanoda Enforcement
**When to use**: config appears to disable nanoda.  
**How**: follow `WorkspaceTest`: parse committed config, force `enable_nanoda=true`, write a temp config, invoke comparator with it.  
**Trade-offs**: committed JSON alone does not reveal final runtime setting.

## One-Untrusted-Elaboration Boundary
**When to use**: security review of setup/evaluation code.  
**How**: trace every command before comparator's `safeLakeBuild Solution`; none should elaborate Submission. Use `lake_env_probe` after toolchain behavior changes.  
**Trade-offs**: must be re-established after relevant Lake/Lean changes.

## Pin-Bump Re-audit
**When to use**: changing comparator, landrun, Lean, lean4export, or nanoda.  
**How**: update pins in lockstep, run immutable-pin audit, mandatory sandbox/env probes, one-shot Lake/artifact probes, starter smoke, and workflow smoke; update security documentation if verdicts change.  
**Trade-offs**: slower dependency upgrades; preserves evidence behind trust claims.

## Semantic Constraint Check for Definition Holes
**When to use**: any `def`/`instance` appears in `definition_names`.  
**How**: identify trusted theorem statements that constrain the flexible implementation. Try to construct a trivial type-correct implementation mentally/test-wise; if it satisfies all obligations, strengthen the spec or explicitly accept the weak target.  
**Trade-offs**: partly human judgment; automated syntax checks cannot infer author intent.

## Same-Reproduction Repair Loop
**When to use**: any failed command.  
**How**: capture command/output, change one layer, rerun the exact command, then run one adjacent invariant check.  
**Trade-offs**: disciplined and slower than shotgun changes; preserves causal evidence.

## Security-Skip Guard
**When to use**: running Python probes outside CI.  
**How**: pass `--require-tools` whenever a security conclusion is desired. Treat a missing-tool skip as unknown.  
**Trade-offs**: may block on local environment; avoids false assurance.
