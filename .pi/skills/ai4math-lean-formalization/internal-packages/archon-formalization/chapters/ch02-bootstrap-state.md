# Chapter 2: Bootstrap and Project State

## Core Idea
Initialization creates a project-local control plane around the Lean repository. Treat that control plane as durable state, not disposable prompt scaffolding.

## Procedure
1. Back up important work before upgrade/re-init.
2. Run `archon setup` for system/toolchain checks when needed.
3. Run `archon init <project>` on an empty directory, existing Lean repo, or directory containing informal material.
4. Inspect `.archon/config.json` and `.archon/.env`; keep provider secrets in the gitignored env file.
5. Inspect `archon-protected.yaml` before autonomous edits.
6. Confirm project-local Lean skill/LSP wiring and run `archon doctor` when setup is uncertain.
7. Re-run `archon init` after Archon upgrades to refresh bundled prompts/skills, choosing the offered keep/merge/overwrite policy intentionally.

## State Ownership
- Plan agent owns `PROGRESS.md` and `STRATEGY.md`.
- `USER_HINTS.md` is user-authored input captured by the loop.
- Provers write assigned Lean files and their task result files.
- Review owns proof-journal synthesis and project-status knowledge.
- `TO_USER.md` is a shared notice surface.
- Inner git tracks agent-phase state independently of the user's outer git history.

## Invariant
Project-local prompts and skills take precedence over global copies. Recommendations should therefore inspect the initialized project when behavior seems inconsistent with the repository defaults.

## Common Upgrade Cases
Legacy projects may need a re-init to gain newer prompts/config/state conventions. Version mismatches and prompt drift should be treated as diagnostic signals before debugging agent behavior.

## Validation
A healthy initialized project has a readable `.archon/` state directory, usable Lean project/toolchain, local agent tooling, inner git, and config/protection files consistent with the intended workflow.

## Source Provenance
Primary: `README.md`, `docs/MIGRATION.md`, `src/archon/.archon-src/archon-template/AGENTS.md`, `src/archon/commands/init/**`, `tests/test_init_*`, `tests/test_state_layout.py`.

## Frameworks Introduced
- **Project-local authority**: initialized project prompts, rules, skills, and config are the operative environment. Inspect them before assuming global defaults.
- **State ownership matrix**: each role owns specific files. Use ownership to diagnose accidental writes and to decide where new information belongs.
- **Re-init as controlled migration**: after upgrades, refresh bundled assets while preserving deliberate local modifications through the offered merge/keep/overwrite path.

## Key Concepts
- **`.archon/config.json`**: project preferences for loop, harness, subagents, and multilane.
- **`.archon/.env`**: gitignored provider/API configuration.
- **`PROGRESS.md`**: current stage/objective state.
- **`STRATEGY.md`**: long-horizon mathematical route.
- **`USER_HINTS.md`**: user-authored steering captured into planning.
- **`AUTO_NOTES.md`**: loop-generated deterministic feedback for the next planner.
- **Inner git**: phase-by-phase agent history independent of outer git.

## Mental Models
- Treat `.archon/` like **runtime state plus a control database**: hand-edit only surfaces intended for the user.
- Treat re-initialization like a **schema migration**: refresh machinery, preserve authored mathematical state.

## Anti-patterns
- **Copying secrets into versioned config**: credentials belong in `.archon/.env` or external secret storage.
- **Debugging stale prompts as model failure**: version/prompt drift can explain behavior changes.
- **Deleting inner state to “clean things up”**: destroys the evidence and rollback surface needed to diagnose a bad iteration.

## Worked Example
An older project runs v0.3.3 CLI but still has pre-0.3 project prompts. The prover ignores current mode semantics and review output looks inconsistent. Check `archon version` and drift warnings, back up, re-run `archon init .`, merge new bundled prompts while preserving strategy/progress, then run `archon doctor`. Only after project-local assets match the intended version should you attribute residual failures to strategy or model quality.

## Key Takeaways
1. Verify local state before debugging higher layers.
2. Keep user hints, automatic validation notes, strategy, and execution results on their intended surfaces.
3. Preserve inner-git history across normal operations.
4. Re-init after upgrades when bundled prompts/skills changed.

## Connects To
- **Ch 08**: config precedence for harnesses/backends/subagents.
- **Ch 09**: secrets, protection, and recovery.
- **Ch 13**: diagnostics for version and prompt drift.
