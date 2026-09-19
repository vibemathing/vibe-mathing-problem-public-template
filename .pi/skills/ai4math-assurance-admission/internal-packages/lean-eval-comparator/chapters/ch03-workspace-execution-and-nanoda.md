# Operational Section 3: Workspace Execution and Nanoda

## Core Idea
A solver workspace is a mostly trusted generated Lake project with a narrow editable surface. `lake test` invokes `WorkspaceTest`, which forces nanoda on and passes an enforced temporary config to comparator.

## Frameworks Introduced

- **Editable-surface rule**
  - **When to use**: deciding where solver changes belong or diagnosing a workspace that diverged unexpectedly.
  - **How**: edit `Submission.lean`, `Submission/Helpers.lean`, or additional Lean modules under `Submission/`. Treat Challenge, Solution, config, lakefile, toolchain, and test harness as fixed inputs for normal solving.

- **Invocation-time policy override**
  - **When to use**: a user notices `enable_nanoda: false` and assumes the second kernel is disabled.
  - **How**: inspect `WorkspaceTest.lean`: it parses `config.json`, sets `enable_nanoda` to true in memory, writes a temporary config, and runs `lake env <comparator> <temporary-config>`.

- **Binary indirection**
  - **When to use**: comparator lives outside `PATH`.
  - **How**: set `COMPARATOR_BIN=/path/to/comparator`; remember comparator still needs its own dependencies such as landrun and lean4export available where it expects them.

## Normal Solver Procedure

```bash
# from repository root
lake exe lean-eval start-problem <problem-id>
cd workspaces/<problem-id>
lake update
# edit Submission.lean / Submission/*.lean
lake test
```

For an off-PATH comparator:

```bash
COMPARATOR_BIN=/path/to/comparator lake test
```

## Execution Path

1. Lake builds/runs `WorkspaceTest` (trusted harness importing Lean).
2. Harness reads committed `config.json`.
3. Harness overrides `enable_nanoda := true`.
4. Harness writes an enforced temporary config.
5. Harness spawns `lake env comparator <temp-config>` or the `COMPARATOR_BIN` override.
6. Comparator separately builds/exports Challenge and Solution under landrun.
7. Building Solution transitively elaborates solver-controlled Submission inside the sandbox.
8. Comparator performs graph/axiom checks and kernel replay.
9. Nanoda checks the exported Solution environment as the independent-kernel gate.

## Key Concepts

- **`COMPARATOR_BIN`**: optional environment override for comparator executable path.
- **Committed config**: generated `config.json`; may show nanoda false because the harness enforces it later.
- **Enforced config**: temporary config passed to comparator with nanoda enabled.
- **Pristine workspace**: generated source-of-truth workspace used as baseline for scoring/integrity.
- **Workspace copy**: solver-editable local copy under `workspaces/`.

## Reference Table: Solver Ownership

| Path | Solver may change? | Typical reason |
|---|---:|---|
| `Submission.lean` | Yes | primary proof/definitions |
| `Submission/Helpers.lean` | Yes | helper lemmas/code |
| additional `Submission/*.lean` | Yes | multi-file solution |
| `Challenge.lean` | No | trusted statement |
| `Solution.lean` | No | trusted bridge |
| `config.json` | No | comparator policy/targets |
| `lakefile.toml` | No | generated project definition |
| `WorkspaceTest.lean` | No | evaluation harness |

## Worked Example: Why `enable_nanoda: false` Is Not a Bypass

A generated workspace contains `"enable_nanoda": false`. A user proposes flipping or relying on that value to skip nanoda. The correct reasoning is to follow the call site: the harness reads that JSON and overwrites the field to true before comparator sees it. Therefore the committed value does not control the final invocation. If nanoda is absent, the correct fix is to install/expose `nanoda_bin`; changing the committed config does not satisfy LeanEval's evaluation model.

## Anti-patterns

- **Editing trusted project files to make local tests easier**: creates a result that does not represent benchmark evaluation.
- **Treating committed config as the final comparator invocation**: misses the harness override.
- **Assuming `COMPARATOR_BIN` replaces all external tools**: it only chooses comparator; comparator still relies on its execution environment.
- **Broadening imports casually**: a broader import header can affect elaboration of fixed statements. Keep changes compatible with the generated workspace.

## Key Takeaways

1. Keep solver modifications inside Submission paths.
2. Follow runtime call sites when config files and behavior appear inconsistent.
3. Nanoda is a global requirement enforced by the harness.
4. `lake test` is the authoritative per-workspace evaluation command.
5. A custom comparator path does not remove its dependencies.

## Connects To

- **ch01**: trust roles of Challenge/Submission/Solution.
- **ch04**: how workspace changes become attempted/succeeded scores.
- **ch07**: exact point where untrusted Lean is elaborated.
