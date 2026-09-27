# Operational Section 6: Failure Diagnosis

## Core Idea
Route failures by layer before changing code. LeanEval has distinct source/catalog, workspace, toolchain, comparator, nanoda, proof, and security layers; changing the wrong layer creates misleading symptoms.

## Frameworks Introduced

### Diagnostic Router

### A. Does the starter comparator smoke pass?

Run:

```bash
lake exe lean-eval check-comparator-installation
```

- **No** → environment/integration problem. Stay in this chapter + ch02.
- **Yes** → environment baseline is credible; move to target-workspace/proof diagnosis.

### B. Common environment symptoms

| Symptom | Likely layer | First action |
|---|---|---|
| `landrun` not found | PATH/install | install exact landrun pin; fix PATH |
| landrun missing required flags | wrong landrun build | reinstall exact pin; inspect `--help` |
| landrun toolchain probe fails | sandbox/dynamic loader | verify `--ldd`/`--add-exec`, exact pin, active Lean prefix |
| comparator executable missing | PATH/override | fix PATH or `COMPARATOR_BIN` |
| `nanoda_bin` missing | independent kernel | build/expose pinned nanoda |
| `incompatible header` | Lean/olean mismatch | rebuild lean4export + comparator coherently; clear `.lake/build` |
| stale generated smoke workspace | generation | regenerate `two_plus_two`; rerun smoke |

### C. Does only the target workspace fail?

1. From target workspace, run `lake test` and preserve stderr.
2. From repo root, run `lake exe lean-eval run-eval --json` and locate the problem.
3. Inspect `mismatches`:
   - solver-owned changes only → proceed to proof/import diagnostics.
   - trusted/generated files changed → restore/regenerate baseline.
4. If broad imports were added, test whether they changed elaboration of the fixed statement or bridge build.
5. Compare a minimal solver proof path before adding helpers.

### D. Is the problem reported unattempted?

An unchanged workspace is intentionally unattempted. Add a legitimate Submission change and rerun. If you did change Submission but mismatches remain empty, verify you are editing the same workspace root that `run-eval` selected.

### E. Unknown id / no generated workspaces

- `Unknown problem id(s)` → check the manifest id, not display title.
- `Unknown generated workspace` → generate/check the correct id.
- `No generated workspaces found` → confirm repository root and generation state.

## Failure-Recovery Patterns

### Environment before proof
If a hard theorem fails and the starter check also fails, do not inspect theorem tactics yet. Repair the shared environment first.

### One change, same reproduction
After every repair, rerun the exact command that first failed. Then run one adjacent check:

- install fix → starter smoke + target `lake test`
- generation fix → `generate --check` + target build
- proof fix → target `lake test` + `run-eval --json`
- security/pin fix → required probes + one-shot probes when relevant

### Use output ownership
`runProblemTest` streams child stdout/stderr to stderr so JSON stdout stays parseable. If consuming `run-eval --json`, keep diagnostic stderr separately from JSON stdout.

## Worked Example: “My proof fails after upgrading Lean”

1. Run starter comparator smoke.
2. If it reports incompatible olean headers, classify as toolchain mismatch.
3. Read `lean-toolchain`; align lean4export with it and rebuild comparator at its pin.
4. Clear target workspace `.lake/build`.
5. Rerun starter smoke.
6. Only after it passes, retry the target proof.
7. If the proof still fails, inspect target-specific comparator output and imported dependencies.

This sequence prevents a toolchain failure from being misdiagnosed as a theorem failure.

## Anti-patterns

- **Shotgun reinstall**: changes several variables and destroys causal evidence.
- **Editing `config.json` to make a check easier**: changes trusted evaluation inputs and does not bypass harness-enforced nanoda.
- **Calling a skipped security probe “pass”**: missing tool behavior is explicitly a skip unless `--require-tools` is used.
- **Assuming all nonzero comparator exits mean proof rejection**: dependency, sandbox, exporter, and kernel layers can fail first.

## Key Takeaways

1. Starter smoke separates global environment from target proof issues.
2. Preserve the failing command/output before changing anything.
3. Use `mismatches` to distinguish solver work from trusted drift.
4. Repair one layer at a time and rerun the same reproduction.
5. Treat skipped/unavailable tests as unknown, never success.

## Connects To

- **ch02**: installation preflight details.
- **ch04**: score fields used for diagnosis.
- **ch08**: security-specific probe verdicts.
