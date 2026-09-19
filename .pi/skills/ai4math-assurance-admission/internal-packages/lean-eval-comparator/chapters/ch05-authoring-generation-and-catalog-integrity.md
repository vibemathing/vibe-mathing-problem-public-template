# Operational Section 5: Authoring, Generation, and Catalog Integrity

## Core Idea
The manifest and tagged Lean declarations are the source of truth; generated comparator workspaces are derived artifacts. Authors validate the source, regenerate locally for fast feedback, and let CI enforce catalog/workspace consistency.

## Frameworks Introduced

- **Manifest-reachability rule**
  - **When to use**: adding a benchmark module or diagnosing `validate-manifest` failures.
  - **How**: every `@[eval_problem]` declaration must be owned by exactly one problem manifest, and LeanEval source modules must be reachable from manifest-named modules/imports.

- **One-file-per-problem manifest**
  - **When to use**: creating/editing a benchmark problem.
  - **How**: `manifests/problems/<id>.toml` has top-level fields, filename stem equals `id`, and `holes` lists every owned tagged declaration.

- **Generated-artifact discipline**
  - **When to use**: contributor workflow or stale workspace diagnosis.
  - **How**: edit trusted source/manifests, run targeted generation/build checks, and avoid hand-maintaining `generated/` as primary source.

## Required Manifest Core

Each problem supplies:

- `id`
- `title`
- `group`
- `status`
- `visible`
- `statement_revision`
- `tags`
- `module`
- `holes`
- `submitter`

Optional metadata may include notes, source, informal solution, and lifecycle history. `holes` is always an array, including the single-theorem case.

## Author Procedure

1. Add/edit a trusted theorem/definition/instance under `LeanEval/` and mark owned declarations with `@[eval_problem]`.
2. Add/update the matching manifest.
3. For every instance hole, assign a stable explicit name.
4. Validate source/catalog:

```bash
lake exe lean-eval validate-manifest
lake exe lean-eval check-problem-build
```

5. Reproduce CI's generation/build path for the affected problem:

```bash
lake exe lean-eval generate --problem <problem-id>
lake exe lean-eval check-generated-builds --problem <problem-id>
```

6. Before claiming repository health, use the broader chain when appropriate:

```bash
lake exe lean-eval validate-manifest
lake exe lean-eval check-problem-build
lake exe lean-eval generate --check
lake exe lean-eval check-generated-builds
lake exe lean-eval run-eval
```

## Generated Workspace Integrity

A generated workspace includes Challenge, Submission starter, Solution bridge, comparator config, Lake files/toolchain, helper directory, README, and `WorkspaceTest`. `check-generated-builds` enumerates generated subdirectories with a real `lakefile.toml`, optionally filters by requested problem ids, and runs `lake build` in each selected workspace.

Signals:

- **Unknown generated workspace** → requested id does not exist in the generated set.
- **No generated workspaces found** → wrong root or missing generation output.
- **`generate --check` mismatch** → generated artifacts have drifted from current source/template/manifest.

## Worked Example: Multi-hole Manifest

A problem that owns a definition `foo` and theorem `foo_def` sets `holes = ["foo", "foo_def"]`. Generation puts `foo` under `definition_names` and `foo_def` under `theorem_names`, then creates Submission placeholders for both and a Solution bridge. This is why `holes` must list every owned tagged declaration and why hole kind matters downstream.

## Anti-patterns

- **Anonymous instance holes**: Lean-generated instance names can be unstable; comparator/generator needs stable names.
- **Hand-editing generated trusted files as source**: the next regeneration overwrites them and can hide source-of-truth drift.
- **Adding a LeanEval module with no manifest/import reachability**: CI intentionally rejects orphaned problem source.
- **Treating a successful generation as full correctness**: build, comparator, and security properties are separate gates.

## Key Takeaways

1. Authoritative inputs live in trusted Lean source + manifests + templates.
2. Generated workspaces are deterministic evaluation artifacts.
3. Run targeted regeneration/build checks before expensive catalog-wide checks.
4. Every hole must be named and represented in the manifest.
5. Multi-hole kind influences comparator semantics; continue to ch10 for spec review.

## Connects To

- **ch10**: def/instance-hole semantic risk.
- **ch04**: scorer re-renders expected workspace from the same source of truth.
- **ch09**: pin changes can invalidate generated/evaluation assumptions.
