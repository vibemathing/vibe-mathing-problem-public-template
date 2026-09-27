# Operational Section 7: Security Model and Invariants

## Core Idea
LeanEval's security target is twofold: solver-controlled Lean should remain bounded by the comparator/landrun sandbox, and comparator should only grant credit for a Solution that actually proves the trusted Challenge under the permitted axioms and kernel checks.

## Frameworks Introduced

### Threat Model

Assume the submitter controls `Submission.lean` and modules under `Submission/`. In the intended evaluation path they do not control Challenge, Solution, lakefile, toolchain, config, WorkspaceTest, or immutable upstream pins.

Two primary failures matter:

1. Untrusted solver Lean escapes its sandbox or reaches sensitive runner capabilities.
2. Comparator accepts a Solution that does not establish the exact trusted Challenge.

## Security Invariants

### 1. Untrusted elaboration occurs only inside sandboxed Solution build
The intended first elaboration of Submission is comparator's `safeLakeBuild Solution`, which transitively builds Submission inside landrun. Host-side setup operations should not elaborate solver code.

### 2. Constant graph integrity
Reachable constants from named theorem targets must match Challenge/Solution, except explicitly configured definition-hole semantics. Any comparator pin change that alters this walk requires review.

### 3. Axiom allowlist
Generated configs permit exactly:

- `propext`
- `Quot.sound`
- `Classical.choice`

The omission of `sorryAx` and `Lean.ofReduceBool` is deliberate.

### 4. Filesystem policy is fail-checked
The sandbox probe expects writes outside the allowed workspace `.lake` area to fail and a designated inside-`.lake` write to succeed. This detects landlock fail-open or policy drift.

### 5. Environment is allowlist-checked
Submission elaboration should see a subset of `{PATH, HOME, LEAN_ABORT_ON_PANIC, LEAN_PATH, LD_LIBRARY_PATH}` and must include the first three. Unknown leaked variables are a security failure.

### 6. Dual-kernel acceptance
WorkspaceTest forces nanoda and comparator also replays through Lean's kernel. A claim of acceptance requires both paths in the intended harness.

## Known Limitation: Writable `.lake` Persistence

Comparator must allow writes to workspace `.lake` during builds. The source security model records a concern: a child process started during Submission elaboration may survive the per-build landrun process and race later reads of build artifacts. No working false-credit exploit is claimed in the snapshot, and substituted artifacts remain subject to kernel/external-kernel checks. The current comparator pin does not include the proposed upstream PID-namespace mitigation cited by the source.

Operational consequence: do not state that process lifetime or artifact identity is proven solely because individual build commands are sandboxed. Re-run the artifact-tamper probe after landrun/comparator/toolchain changes and preserve this limitation in security reviews until the pinned implementation changes and tests support a stronger claim.

## Mental Models

- **Sandboxing is a property of a concrete invocation**: verify policy and probes on the actual runner/kernel.
- **A clean logical comparison does not replace process isolation**: proof integrity and host containment are separate defenses.
- **Independent kernels reduce correlated soundness risk**: they do not eliminate shared exporter/comparator/process risks.
- **Security claims are pin-scoped**: a new dependency commit invalidates assumptions until re-audited.

## Worked Example: Reviewing a Comparator Pin Bump

A PR changes comparator to add a feature. Review in layers:

1. Re-read comparator changes affecting `compareAt`, axiom checking, safe build/export, executable/environment policy, and nanoda invocation.
2. Update all pin sites in lockstep.
3. Run the action pin audit.
4. Run sandbox-engaged and env-allowlist probes with required tools.
5. Run `lake_env_probe` and `artifact_tamper_probe` on Linux.
6. Run starter comparator smoke and workflow self-check.
7. If any security probe verdict changes, update the security model before merge.

## Anti-patterns

- **Claiming landrun is safe because it started**: `--best-effort` can degrade on unsupported kernels; the probe must prove the expected write policy.
- **Spot-checking a few secret variable names**: use the allowlist model so unknown future variables are also caught.
- **Treating nanoda as a complete sandbox mitigation**: it checks proof/kernel soundness, not process containment.
- **Ignoring `definition_names` when reviewing proof integrity**: body relaxation can create specification weaknesses.

## Key Takeaways

1. Security has host-containment and proof-integrity dimensions.
2. Only sandboxed Solution build should elaborate Submission.
3. Axiom and constant-graph checks are transitive.
4. Nanoda is mandatory defense-in-depth.
5. Preserve the writable-`.lake` limitation until a pinned fix plus probes justify changing the claim.

## Connects To

- **ch08**: exact probes and verdict interpretation.
- **ch09**: why pin changes force re-audit.
- **ch10**: specification risk created by definition holes.
