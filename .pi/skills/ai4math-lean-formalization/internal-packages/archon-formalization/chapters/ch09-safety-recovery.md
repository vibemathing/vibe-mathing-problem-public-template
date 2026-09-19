# Chapter 9: Safety, Protection, and Recovery

## Core Idea
Archon can run agents with broad shell capability, so write boundaries, immutable mathematical surfaces, secret handling, and reversible history are first-class controls.

## Safe Mode
The unrestricted default may bypass normal permission prompts. Use `archon loop --safe` when automatic commands are desired but writes must remain inside the active project. Tested behavior uses a workspace-only filesystem sandbox, keeps network access available, places temp files under project state, and fails if the sandbox is unavailable instead of silently dropping isolation.

Safe mode limits filesystem writes; it does not make commands harmless inside the workspace. Inner-git snapshots and protected rules still matter.

## Protected Surface
`archon-protected.yaml` supports:
- Lean declaration protection: signature-only or whole declaration;
- blueprint whole-file protection or label-block statement/all protection;
- arbitrary read-only file globs.

Signature protection permits filling a proof body while freezing name/type. Whole-declaration protection freezes body too. Use `archon protect-check` to inspect resolved rules.

## Secrets
Keep provider/API secrets in `.archon/.env` or external secret management. Do not commit them. Multilane summaries redact common key/token/secret/password environment names.

## Recovery with Inner Git
Each agent phase commits into `.archon/git-dir`. Use `archon log` to inspect history and `archon branch <name> --from <commit>` to fork a historical point. Branch switching guards against dirty outer/inner state; failed branch creation/switch attempts have rollback logic to restore prior HEAD and remove partial refs.

## Failure Strategy
- interrupted loop → `--resume`;
- bad refactor/route → fork known-good inner commit;
- dirty trees → resolve or consciously force only after understanding what will be overwritten;
- protected-surface conflict → change the plan, or have the user revise protection explicitly.

## Source Provenance
Primary: README security note, `agent.py`, `protect.py`, `branch.py`, safe-mode/protection/rollback tests.

## Frameworks Introduced
- **Defense in depth for autonomous writes**: workspace sandbox + protected surface + inner-git recovery address different failure modes.
- **Protection levels**: freeze a Lean signature while allowing proof fill, or freeze the whole declaration; protect blueprint statements/proofs/files independently.
- **Transactional branch switch**: refuse unsafe dirty-state transitions and roll back partial branch operations.

## Key Concepts
- **Workspace-only sandbox**: automatic commands can run while write paths are constrained to the project.
- **Fail closed**: safe mode requires the sandbox rather than silently running unsandboxed if it is unavailable.
- **Outer git vs inner git**: user repository history and Archon agent-phase history serve distinct purposes.
- **Protected path glob**: arbitrary file/blueprint protection using predictable glob matching.

## Mental Models
- Safe mode is a **write boundary**, not a correctness guarantee.
- Inner git is a **transaction log for agent work**; protection is an **authorization policy**; neither replaces the other.

## Anti-patterns
- **Assume sandbox prevents destructive in-project commands**: it confines writes, while destructive writes inside the allowed workspace can still happen.
- **Force branch switch through dirty state casually**: risks overwriting or corrupting in-flight work.
- **Let an agent weaken protection because the proof is inconvenient**: protection expresses user ownership and must shape the plan.

## Worked Example
A theorem signature is approved by the mathematician but its proof is open. Add a Lean `signature` protection rule: provers may fill the body but cannot re-type the theorem. A neighboring generated file is entirely user-owned, so protect it with a file glob. Run the loop with `--safe` on a machine containing unrelated secrets elsewhere. Before a risky refactor, inspect `archon log` and fork an inner branch. These controls together constrain blast radius and preserve a recovery point.

## Key Takeaways
1. Use sandbox, protection, and history together.
2. Keep secrets out of committed state.
3. Respect dirty-tree guards during time travel.
4. Protection conflicts require redesign or explicit user policy change.

## Connects To
- **Ch 02**: project-local state and secrets.
- **Ch 08**: engine behavior under safe mode.
- **Ch 14**: recovery ladder after crashes or bad changes.
