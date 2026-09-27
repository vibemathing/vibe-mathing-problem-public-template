# Operational Section 9: Pin Governance and Drift

## Core Idea
LeanEval treats verifier dependencies and CI actions as supply-chain security inputs. A dependency update is complete only when every authoritative pin site agrees and the affected behavioral assumptions are re-tested.

## Frameworks Introduced

- **Immutable selector rule**
  - **When to use**: reviewing workflow/dependency changes.
  - **How**: use exact commit SHAs for source/action dependencies and exact patch/toolchain selectors where appropriate. Reject branch names, loose action tags, `stable`, and equivalent mutable selectors in workflow context.

- **Lockstep pin update**
  - **When to use**: bumping landrun, lean4export, comparator, nanoda, or benchmark commit dependencies.
  - **How**: update every documented CI/runtime site, then run automated audits and security probes before merge.

- **Cross-source drift detector**
  - **When to use**: setup instructions fail unexpectedly or two docs quote different SHAs.
  - **How**: extract component→SHA pairs from `SECURITY.md`, CI workflows, executable constants, and README examples; flag disagreement rather than silently choosing one.

## Snapshot Runtime Pin Table

| Component | Authoritative snapshot pin |
|---|---|
| Lean | `v4.33.0` |
| mathlib | `6f1ef4e5dd604a435bddba4747b13970cd65d2a1` |
| lean4-cli | `6130a47896ce867c6a4a55373441e59e565bad0f` |
| landrun | `5ed4a3db3a4ad930d577215c6b9abaa19df7f99f` |
| lean4export | `15f6055e299ad5b89345e533cc2192f4cc00f659` |
| comparator | `71b52ec29e06d4b7d882726553b1ceb99a2499e0` |
| nanoda | `68d5ca9db226849b41a6fff59d796ff19d0a8840` |

These values are snapshot facts. For a newer checkout, re-read its security table and workflows before quoting them as current.

## Lockstep Update Procedure

1. Resolve the new immutable SHA from the upstream repository/tag/branch head as appropriate.
2. Update every applicable site documented by LeanEval, including:
   - main CI workflow;
   - regeneration workflow where relevant;
   - submission pipeline workflow in the separate submissions repository;
   - README local setup examples;
   - `EvalTools/CheckComparatorInstallation.lean` for the landrun target;
   - leaderboard benchmark-commit pointer when changing the benchmark revision.
3. Add/update dated pin comments where the repository convention calls for them.
4. Run:

```bash
python scripts/action_pin_audit.py
python scripts/sandbox_engaged_probe.py --require-tools
python scripts/security_probes/env_dump_probe.py --require-tools
```

5. On Linux, rerun one-shot probes when relevant:

```bash
python scripts/security_probes/lake_env_probe.py --require-tools
python scripts/security_probes/artifact_tamper_probe.py --phase both --require-tools
```

6. Run comparator functional smoke and evaluation workflow smoke.
7. Update the security model if any assumption/verdict changed.
8. Merge only after lockstep consistency is restored.

## Worked Example: Drift Found in This Snapshot

The snapshot README's local lean4export command checks out `4e7915201d3f9f04470d9eae002fa695f7cdc589`. The security pin table and CI checkout `15f6055e299ad5b89345e533cc2192f4cc00f659` for Lean 4.33 compatibility. An operator following README alone can therefore build a tool that diverges from CI.

Correct handling:

1. Report the disagreement explicitly.
2. Use the CI/security value for reproducing this snapshot's evaluated environment.
3. Repair README so local instructions match CI.
4. Rerun installation smoke after rebuilding lean4export.

The drift is a documentation consistency defect even though the action pin audit remains clean, because that audit focuses on workflow mutability rather than prose examples.

## Anti-patterns

- **Bumping one file only**: creates local/CI/submission divergence.
- **Using action major tags or dependency branches for convenience**: upstream can change evaluation code without a reviewed LeanEval diff.
- **Assuming pin consistency because CI YAML is clean**: README/executable constants can still drift.
- **Reusing old security conclusions after a pin change**: verifier and sandbox behavior are pin-scoped.

## Key Takeaways

1. Immutable pins are part of the trust model.
2. Lockstep consistency spans code, workflows, docs, and a separate submission repository.
3. Automated pin audit catches mutable workflow refs, not every cross-document mismatch.
4. Security probes are required evidence for sensitive bumps.
5. Treat snapshot pin values as historical once the user's checkout changes.

## Connects To

- **ch02**: install failures caused by pin/toolchain mismatch.
- **ch07**: security assumptions tied to comparator/landrun pins.
- **ch08**: probe suite used for re-audit.
