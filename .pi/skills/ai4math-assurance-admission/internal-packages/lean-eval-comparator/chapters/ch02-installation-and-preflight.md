# Operational Section 2: Installation and Preflight

## Core Idea
Prove the toolchain works with the repository's starter problem before interpreting failures from a real submission. Exact pins, capabilities, and toolchain compatibility matter more than friendly version labels.

## Frameworks Introduced

- **Capability-first preflight**
  - **When to use**: first setup, CI parity work, or any environment-looking `lake test` failure.
  - **How**:
    1. Confirm the Lean repository itself builds enough to expose `lean-eval`.
    2. Confirm `landrun`, `lean4export`, `comparator`, and `nanoda_bin` are discoverable.
    3. Check landrun's required flags: `--best-effort`, `--ro`, `--rw`, `--rox`, `--rwx`, `--ldd`, `--add-exec`.
    4. Confirm landrun can execute the active Lean toolchain, not merely print a plausible version.
    5. Run `lake exe lean-eval check-comparator-installation`.

- **Toolchain-coherent olean rule**
  - **When to use**: errors mentioning incompatible olean headers or inability to read `Challenge.olean`.
  - **How**: build lean4export against the same Lean toolchain used by the workspace; rebuild comparator at the pinned commit; clear stale workspace `.lake/build` artifacts.

- **Pin authority hierarchy**
  - **When to use**: README setup commands disagree with security/CI.
  - **How**: prefer `SECURITY.md` plus `.github/workflows/ci.yml`, then executable validation code, then prose examples.

## Runtime Pins in This Snapshot

| Component | Snapshot authority value | Why it matters |
|---|---|---|
| Lean | `v4.33.0` | olean/toolchain format |
| landrun | `5ed4a3db3a4ad930d577215c6b9abaa19df7f99f` | sandbox flags/behavior |
| lean4export | `15f6055e299ad5b89345e533cc2192f4cc00f659` | export format aligned to Lean 4.33 |
| comparator | `71b52ec29e06d4b7d882726553b1ceb99a2499e0` | verifier semantics / def-hole support |
| nanoda | `68d5ca9db226849b41a6fff59d796ff19d0a8840` | independent kernel |

**Snapshot drift warning:** `README.md` checks out lean4export at `4e791520...`, while the security pin table and CI use `15f6055e...`. For this snapshot, treat the latter as authoritative and flag the README for repair.

## Procedure

```bash
# from repository root
lake exe lean-eval check-comparator-installation
```

That check performs more than a binary presence test:

1. Inspect landrun on `PATH`.
2. Reject missing comparator-required landrun flags.
3. Reject clearly old semantic versions, while acknowledging version strings cannot uniquely identify the required commit.
4. Run a landrun probe that executes the active toolchain's `lean --version` under sandbox flags.
5. Copy `generated/two_plus_two` into a temporary workspace.
6. Replace its first starter `sorry` with `norm_num`.
7. Run `lake update`, `lake exe cache get`, and `lake test`.
8. Report `Comparator check passed.` only after all stages succeed.

## Diagnostic Signals

| Signal | Interpretation | Recovery |
|---|---|---|
| `landrun` not found | sandbox executable missing from `PATH` | install exact project pin; fix `PATH` |
| missing `--ldd` / `--add-exec` | unsuitable landrun build even if version says 0.1.15 | install exact pinned commit |
| landrun Lean probe fails | dynamic-toolchain execution blocked | inspect flag support/pin; avoid trusting version text |
| `incompatible header` | Lean/olean mismatch or stale `.lake` artifacts | rebuild lean4export/comparator coherently; clear build artifacts |
| comparator cannot be run | binary absent or wrong `COMPARATOR_BIN` | fix binary path, then rerun starter smoke |
| nanoda missing | independent checker unavailable | install pinned nanoda and expose `nanoda_bin` |

## Worked Example: Incompatible Header

Symptom: comparator builds `Challenge.olean`, then lean4export reports it cannot read the file because the header is incompatible.

Reasoning:

1. Do not modify the proof; the failure happens before theorem quality is relevant.
2. Read the repository `lean-toolchain` and ensure lean4export was built with that exact release.
3. Rebuild lean4export at the authoritative pin after aligning its toolchain.
4. Rebuild comparator at its authoritative pin.
5. Remove the affected workspace's `.lake/build` so old oleans cannot survive the toolchain switch.
6. Rerun the starter installation check; only then retry the target workspace.

## Anti-patterns

- **Installing `landrun@main`**: mutable and may differ from audited behavior.
- **Using a version string as commit identity**: landrun's version text does not reliably distinguish needed revisions.
- **Debugging a hard theorem before the starter smoke passes**: mixes environment and proof failures.
- **Following a stale README pin when CI disagrees**: reproducibility requires the audited runtime source.

## Key Takeaways

1. The starter smoke is the environment/proof boundary test.
2. Exact olean toolchain compatibility is mandatory.
3. For landrun, capability and exact pin beat the displayed version.
4. Pin drift across docs is itself a diagnostic finding.
5. Re-run the same smoke after every environment repair.

## Connects To

- **ch06**: symptom-to-recovery tree.
- **ch09**: pin governance and drift reconciliation.
- **ch08**: security probes that must accompany dependency changes.
