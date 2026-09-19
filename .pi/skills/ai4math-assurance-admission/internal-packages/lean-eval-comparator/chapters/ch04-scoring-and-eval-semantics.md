# Operational Section 4: Scoring and Eval Semantics

## Core Idea
LeanEval scoring first detects whether a workspace differs from the generated baseline, then runs comparator only for attempted problems. Interpret `attempted`, `succeeded`, and `mismatches` together.

## Frameworks Introduced

- **Baseline-diff attempt detection**
  - **When to use**: `run-eval` reports zero attempts despite a workspace directory, or the user wants to know what counts as an attempt.
  - **How**:
    1. Render expected workspace files from the manifest/source/template.
    2. Select `workspaces/<id>` if it exists; otherwise use `generated/<id>`.
    3. Compare selected workspace against expected files.
    4. `attempted = true` only when the mismatch list is non-empty.

- **Exit-code success rule**
  - **When to use**: an attempted problem has a result.
  - **How**: for attempted workspaces, run `lake test`; `succeeded = (exit_code == 0)`.

- **Validate full inventory before filtering**
  - **When to use**: `run-eval --problem <id>` seems like it should ignore unrelated catalog errors.
  - **How**: expect full manifest/inventory validation to occur before selected-problem filtering. A global catalog issue can block a targeted score.

## Commands

```bash
# human summary
lake exe lean-eval run-eval

# structured diagnosis
lake exe lean-eval run-eval --json
```

Use JSON when automating or diagnosing. Per-problem output contains:

- `id`
- `title`
- `visible`
- `attempted`
- `succeeded`
- `exit_code` (null for unattempted)
- `mismatches`
- `workspace_path`

Aggregate counts split attempted/succeeded by visible and hidden problems.

## Decision Logic

| `mismatches` | `lake test` | Score state | Meaning |
|---|---|---|---|
| empty | not run | unattempted | workspace is baseline-equivalent |
| non-empty | exit 0 | passed | modified workspace accepted |
| non-empty | nonzero | failed | modified workspace rejected or environment failed |

A failed score alone does not identify proof quality. Read the streamed `lake test` output to separate environment, comparator, nanoda, and theorem failures.

## Worked Example: Built-in Workflow Self-check

`check-eval-workflow` uses `two_plus_two` to assert three scoring states:

1. **Pristine** copy absent/unchanged → attempted 0, succeeded 0.
2. **Intentionally incorrect** edited proof → attempted 1, succeeded 0.
3. **Correct** edited proof (`norm_num`) → attempted 1, succeeded 1.

This is a strong regression test because it checks both attempt detection and comparator-backed success semantics.

Run:

```bash
lake exe lean-eval check-eval-workflow
```

If it says the generated `two_plus_two` workspace is stale, regenerate that problem first, then rerun.

## Mental Models

- **A workspace directory is location, not state**: existence does not imply attempted.
- **Mismatch list is provenance of attempt**: it explains why the scorer decided solver work exists.
- **Success is downstream of attempt**: unattempted problems deliberately have no test exit code.
- **Scoring output is a router**: use it to decide which deeper diagnostic chapter to load.

## Anti-patterns

- **Reading `succeeded=false` as “the proof is wrong”**: environment failures also produce nonzero `lake test`.
- **Assuming a copied starter workspace counts as an attempt**: if it is unchanged, mismatches remain empty.
- **Ignoring `mismatches`**: they are essential to diagnose stale/trusted-file edits.
- **Expecting `--problem` to bypass catalog integrity**: inventory validation intentionally precedes filtering.

## Key Takeaways

1. Attempted is a diff property, not a directory property.
2. Success is comparator-backed `lake test` exit zero.
3. JSON mode exposes the evidence needed for automation and diagnosis.
4. Use `check-eval-workflow` to regression-test score semantics.
5. Always inspect test output before attributing a failure to proof logic.

## Connects To

- **ch05**: expected workspace generation and stale checks.
- **ch06**: converting failed score output into a diagnosis.
- **ch03**: what `lake test` actually invokes.
