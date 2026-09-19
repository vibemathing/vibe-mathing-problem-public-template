# Operational Section 8: Security Probes and Regression Gates

## Core Idea
Security assumptions in LeanEval are executable. Use the probe suite to test concrete sandbox, environment, Lake, and artifact-lifetime claims, and interpret skips/failures literally.

## Frameworks Introduced

### Probe Matrix

| Probe | What it protects | Expected use |
|---|---|---|
| `scripts/action_pin_audit.py` | immutable CI/dependency selectors | every CI build |
| `scripts/sandbox_engaged_probe.py` | landrun filesystem write policy | CI and submission preflight |
| `scripts/security_probes/env_dump_probe.py` | environment allowlist | CI and submission preflight |
| `scripts/security_probes/lake_env_probe.py` | `lake env` must not elaborate Submission | one-shot after relevant toolchain changes |
| `scripts/security_probes/artifact_tamper_probe.py` | process lifetime / `.lake` artifact-race assumptions | one-shot after landrun/comparator/toolchain changes |

## Canonical Commands

```bash
python scripts/action_pin_audit.py
python scripts/sandbox_engaged_probe.py --require-tools
python scripts/security_probes/env_dump_probe.py --require-tools
python scripts/security_probes/lake_env_probe.py --require-tools
python scripts/security_probes/artifact_tamper_probe.py --phase both --require-tools
```

Run security-sensitive probes on the intended Linux environment with the pinned toolchain available. Without `--require-tools`, several probes deliberately return success after printing a skip when dependencies are absent. For audits, use `--require-tools` so missing prerequisites become visible failures/blockers.

## Verdict Semantics

### Sandbox-engaged probe
Creates a synthetic comparator workspace whose Submission tries allowed and forbidden writes. The probe expects only the designated inside-`.lake` write to succeed. Any forbidden allowed write or allowed write denial is a failure.

### Env-dump probe
Seeds the parent environment with decoy sensitive-looking variables and records what Submission can see. It fails if any variable outside the allowlist is visible or if required safe variables are missing.

### Lake-env probe
Checks ordinary and nested `lake env` invocations using a workspace containing top-level markers. Any marker output means project Lean was elaborated too early and is a security regression.

### Artifact-tamper probe
Has two independent questions:

- **Phase A**: can detached descendants survive comparator's per-build landrun child? Survival confirms attack surface and may yield a nonzero result even without a proven false-credit exploit.
- **Phase B**: can a prepared distinct Solution olean be substituted and accepted? A confirmed accepted substitution is severe and returns a distinct high-severity exit path in the probe.

Do not compress these into a single “tamper safe/unsafe” boolean. Record phase and exact verdict.

## Regression Workflow

1. Run the mandatory CI probes before changing pins to establish baseline.
2. Make the smallest dependency/template change.
3. Run mandatory probes again with required tools.
4. Run the one-shot Lake/artifact probes when process/toolchain assumptions could change.
5. Run `check-comparator-installation` and `check-eval-workflow` to ensure security hardening did not break normal evaluation.
6. Update `SECURITY.md` if actual behavior changed.

## Worked Example: Landrun Bump

After updating the landrun pin:

1. Confirm `action_pin_audit` still reports no mutable selector.
2. Run `check-comparator-installation`; this verifies required flags plus actual Lean execution under landrun.
3. Run sandbox-engaged with `--require-tools`; verify forbidden writes remain denied.
4. Run env-dump; verify environment visibility did not broaden.
5. Run artifact-tamper; compare Phase A/B with the documented limitation.
6. Only then claim the new pin preserves or improves the security posture.

## Anti-patterns

- **Running a probe without tools and recording “pass”**: default skip behavior can look superficially successful.
- **Only running `lake test` after a security-sensitive pin bump**: functional correctness does not prove sandbox invariants.
- **Ignoring a changed probe verdict because CI is green elsewhere**: the security document explicitly depends on those assumptions.
- **Treating artifact Phase A survival as a proven false-credit exploit**: it demonstrates process-lifetime risk; Phase B addresses artifact substitution separately.

## Key Takeaways

1. Use `--require-tools` for security conclusions.
2. Pair functional smoke tests with security probes.
3. Record phase-specific artifact-tamper results.
4. A pin bump that changes a security verdict must change the documented model too.
5. Probe results are environment- and pin-specific evidence.

## Connects To

- **ch07**: invariants the probes implement.
- **ch09**: mandatory probe set during pin governance.
- **ch02**: functional landrun/toolchain preflight.
