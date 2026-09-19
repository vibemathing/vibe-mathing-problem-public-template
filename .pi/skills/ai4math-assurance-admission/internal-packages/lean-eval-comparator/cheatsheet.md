# Comparator Evaluation Cheatsheet

## Route by Symptom

| If you see / need | Do first | Then |
|---|---|---|
| first setup or many workspaces fail | `lake exe lean-eval check-comparator-installation` | ch02/ch06 |
| `incompatible header` | align Lean + lean4export; clear `.lake/build` | rerun starter smoke |
| landrun 0.1.15 but comparator still fails | inspect required flags + functional probe | install exact pin |
| `nanoda_bin` missing | expose pinned nanoda binary | rerun `lake test` |
| `run-eval` says 0 attempted | inspect `mismatches` and selected workspace path | verify you edited `workspaces/<id>` |
| only one target fails after smoke passes | `lake test` + `run-eval --json` | proof/import/workspace diagnosis |
| `definition_names` present | review semantic constraints | ch10 |
| comparator/landrun/Lean pin bump | lockstep pins + security probes | ch09 |
| security claim with missing tools | rerun probes with `--require-tools` | report blocker if unavailable |

## Hard Invariants

- Solver edits: `Submission.lean`, `Submission/Helpers.lean`, extra `Submission/*.lean`.
- Trusted in normal solve: `Challenge.lean`, `Solution.lean`, `config.json`, `lakefile.toml`, `WorkspaceTest.lean`.
- Permitted axioms: `propext`, `Quot.sound`, `Classical.choice`.
- Nanoda: globally forced on by `WorkspaceTest` at invocation.
- Attempted: workspace mismatches expected rendering.
- Succeeded: attempted and `lake test` exit code 0.
- Untrusted elaboration: intended only inside comparator's sandboxed Solution build.

## Snapshot Runtime Pins

| Lean | landrun | lean4export | comparator | nanoda |
|---|---|---|---|---|
| v4.33.0 | `5ed4a3d…` | `15f6055…` | `71b52ec…` | `68d5ca9…` |

**Drift tell:** this snapshot's README quotes a different lean4export SHA. Prefer CI/security authority and fix documentation.

## Security Probe Set

```bash
python scripts/action_pin_audit.py
python scripts/sandbox_engaged_probe.py --require-tools
python scripts/security_probes/env_dump_probe.py --require-tools
python scripts/security_probes/lake_env_probe.py --require-tools
python scripts/security_probes/artifact_tamper_probe.py --phase both --require-tools
```

## Stop Conditions

Return “insufficient evidence” when:

- security probe skipped or cannot run on the intended platform;
- current checkout pins were not inspected and may differ from this snapshot;
- comparator output is missing and multiple layers can explain the failure;
- a def/instance hole's semantic constraints are unclear without author intent.
