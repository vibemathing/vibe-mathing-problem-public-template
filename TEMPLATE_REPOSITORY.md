# Vibe Mathing Problem Research Template

This is the **generic public template**. It contains the complete fixed
Pi-native research Harness, its bounded Web transport profile, and one explicit
inert placeholder ProblemContract. The template is not a research repository
and must not be bound to, or start an actor for, any mathematical problem. Root
`VERSION` is the only suite-version truth; builder, source manifest and snapshot
must match it exactly or fail closed.

## Placeholder policy

`problem-library/records/canonical-problems.jsonl` contains
`problem:template-placeholder` with `lifecycle=draft` and
`admission=preview_unadmitted`. It is a physical-template fixture only. The
placeholder is intentionally retained in the generic template; C05 is not
applicable to this repository role. A concrete problem repository must replace
it with exactly one independently reviewed, canonical-admitted ProblemContract
before research starts.

## Generate one concrete problem repository

1. Select the template matching the target repository visibility.
2. Admit exactly one reviewed ProblemContract with `lifecycle=active` in the problem library.
3. Create a repository named from its `problem_id`.
4. Read back GitHub database ID, node ID, visibility, and default branch.
5. Rebuild with verified repository identity and the exact canonical contract digest.
6. Validate the standalone snapshot before the first research operation.

The fixed suite is copied into every concrete problem repository. Its project
Skills live under `.pi/skills/` and the exact Pi loading allowlist lives in
`.pi/settings.json`; no user-global Skill is vendored into the repository.
Eight top-level mathematical Skills contain 31 project-authored internal
reference packages under repository-relative `internal-packages/` directories,
with one physical copy per package and registry-based cross-references. The
packages are released under MIT and bound to the owner attestation and
immutable tree digests recorded in
`governance/control-plane/project-authored-package-rights-attestation.v1.json`.
Issue, PR, merge, CI, checkpoint, and model output remain research
transport/activity rather than mathematical evidence or Result admission.

## Local actor continuation: Pi Goal extension

`.pi/settings.json` pins MIT-licensed `npm:pi-goal-x@0.31.9` (Node >=22.15;
this patch has been checked with Pi 0.99.2, not asserted portable to every Pi version).
The upstream package plus the MIT review patch/lock in `governance/control-plane/pi-goal-*`
produce an exact 72-file package; plain npm/Pi upstream installation is **not**
the reviewed patched runtime. This is a **continuation extension**, not a mathematical
Skill. The ten method Skills remain the actor's only project Skill allowlist.
An explicitly loaded [maintainer Skill](.pi/opt-in-skills/README.md) covers
Goal operations without entering the actor's mathematical context. This generic
template's ProblemContract is a draft: **do not start an actor or Goal here**.

### Before the first Goal

1. In a **concrete, independently admitted** single-problem repository, verify
   the frozen ProblemContract digest, cwd, one canonical actor, exact session
   and lease, live checkpoint, independent write protection and root `OPEN`
   state. Do not infer identity from a pane title or Goal objective.
2. In an isolated trusted install process (not an actor), run
   `pi install --local --approve npm:pi-goal-x@0.31.9` (only after reviewing the project), then
   `python3 scripts/install_goal_patch.py --project-root . --apply`, then the
   same command with `--check`. This replays only the locked diff against the
   exact official 71-file preimage and verifies the entire 72-file output;
   unknown preimages fail **without overwrite** and a successful install keeps
   the old upstream tree under Git-ignored `.pi/npm/`. Re-running is read-only
   when already patched. Do not start an actor between upstream install and
   patch verification. `pi list` proves only a declaration; after checks,
   confirm `/goal-status` and `/goal-snapshot` really register in an isolated
   Pi process. A fresh offline clone without the project package cache lacks
   those commands. `.pi/npm/` is Git-ignored, never a snapshot member. Run
   `make check-full` and `make check-release`: the builder/release scanner only
   excludes a verified patched cache. If Pi update resets it to upstream,
   repeat the **verified** patch; if bytes differ from either lock state,
   stop and investigate rather than silently reinstalling or weakening checks.
3. Set `PI_GOAL_ROOT` in the actor's trusted launch environment to an existing,
   problem-specific **absolute directory outside the Git repository**, owned by
   the actor user with `0700` permissions. Resolve and reject symlink aliases;
   keep that exact root and session through recovery. A separate diagnostic Pi
   pointed at another root cannot prove the original actor has no Goal. The
   default `.pi/goals/`
   holds objectives, ledger, checkpoints and recovery backups: `.gitignore`
   reduces accidental Git staging but is **not** an access-control boundary.
   The public Harness validator rejects unlisted in-repository runtime files;
   never relax the snapshot to publish them. Do not put a local root, session
   locator or token in the template or in a Git-tracked settings file.
4. Read `/goal-list`, `/goal-status verbose`, `/goal-status health` and
   `/goal-recovery` before any mutation. `/goal-focus` can arm continuation and
   is **not read-only**. Confirm effective setting provenance: project defaults
   in `.pi/pi-goal-x-settings.json` disable Goal-created task lists, prevent
   automatic single-goal focus and limit provider-error retries to three.
   Environment overrides take precedence over project settings; global
   `maxAutonomousRuns` may still impose a cap or `0` (off). Unset means
   unlimited extension-started runs, **not** process survival or proof.

For the original admitted actor, only if no Goal already exists and the old
continuation scheduler is durably stopped, send **once**, in its Pi TUI:

```text
/goal-direct 自主推进当前已准入且冻结的 ProblemContract，直到根问题通过独立验证与数学准入而可信闭合；数学路线由 canonical actor 自主决定，候选与 Goal 状态不能代替 Evidence、Result 或 Solution。
```

Use `/goal-direct` (regular goal), **not** `/sisyphus` or a numbered lemma/route
plan. `/goal-direct` creates a new Goal; it is not a resume command. A Goal
already in the pool must be reconciled rather than recreated. Plugin tasks are
disabled to preserve the research actor's mathematical strategy; the plugin's
optional completion auditor, goal status and finite checks still cannot admit
a mathematical result.

### Pause, failure and recovery

- `/goal-pause` stops autonomous continuation. Never treat it as a completed
  problem. When a resumed Pi session prompts to resume a paused Goal, **decline
  until** session/lease/Goal ID/storage root/checkpoint/write boundaries are
  verified; then use `/goal-resume` for that same Goal in the reconciled actor.
  A `claimed/running/interrupted` dispatch is not replayed after restart.
  `/goal-recovery` is read-only; `/goal-recovery repair` mutates storage and is
  not a routine inspection command.
- `networkRecovery.maxAttempts=3` bounds *transport* retries only. When
  exhausted the Goal may remain `active` without a running continuation; root
  remains `OPEN`. Check the provider and checkpoint before an explicit resume.
  No fixed run count, token ceiling, elapsed time or Goal self-assessment is a
  mathematical stopping condition.
- If Goal or its auditor says `complete` but independent root admission is
  missing, keep the mathematical root `OPEN`, record the inconsistency and
  assess recovery **in the same actor**. Do not blindly create a new Goal or
  another canonical actor. Do not use `/goal-clear` to erase an open mission.
- For a **legacy** actor, durably pause HookLoop dispatch before Goal owns
  continuation. Keep the Hook loaded while its write guard or history filtering
  remains necessary; replace and verify those functions in an independent
  canary before any online switch. On failure, park the Goal and restore just
  one verified scheduler. Pausing a Hook does not prove safe uninstallation.

### Bounded, read-only checkpoint status

For an explicitly identified local actor, a separate maintainer can run
`python3 scripts/report_local_checkpoint.py --checkpoints-dir <private-runtime/checkpoints> --problem-id <frozen-id> --problem-contract-sha256 <frozen-sha256>`.
This optional standard-library command only inventories checkpoint JSON metadata:
the latest by modification time, its adjacent predecessor when available, the
reported candidate/root and admission fields, and directory byte/file counts.
A persisted `infrastructure_update.recorded_at_sequence` identifies a **historical
record**, not automatically the current mathematical delta; comparisons refer
only to two adjacent, identity-matched checkpoint states. Every reported
admission flag is **unverified**, not a Result or closure receipt. Invalid or
oversized files fail closed; the report never reads Pi sessions, deletes,
compacts, or rotates an active checkpoint. Capacity remediation first requires
an independent recovery replay and a bounded retention policy. The generic
template has no admitted local actor, so never run it on the placeholder as
research evidence.

### Display, compaction and sealed-pair shadow (opt-in boundaries)

- Patched Goal defaults to `hideDashboard=true`: only the widget/status hint is
  hidden. `/goal-settings` toggles display via its normal project/global/inherited
  menu; scheduler, pause/resume, usage and Esc interrupt continue to use their
  native owners. Do not confuse a hidden panel with a paused Goal.
- `.pi/extensions/goal-context.ts` auto-discovers under the **trusted project**
  but does nothing when `VIBE_GOAL_CONTEXT_CONFIG` is absent. To opt in, point
  that environment variable at a private `0600` JSON object with exactly
  `schema_version: "goal-context.v1"`, `session_id` and absolute `repository_root`
  (the actual cwd). Only that trusted session's native context/compaction events
  project Pi's exact tail file list into a digest reference; the originals stay
  in the session compaction entry. It uses native `compact`, model stream, signal,
  retry settings and token accounting; no new provider request is launched when
  unconfigured. Never put the config, session or history in Git.
- `/goal-snapshot` is a thin offline bridge **only** for an explicitly emitted
  `sealed-pair-shadow.v1` candidate-only checkpoint/index pair. The standard
  `report_local_checkpoint.py` reports unconstrained metadata and is **not** a
  compatible owner. A real owner must write a checkpoint `schema_version=1.0.0`
  with frozen `problem_id`/`problem_contract_sha256`/`statement_sha256`, positive
  `sequence`, `state_vector.claim_boundary=candidate_only`, an `artifact_manifest`
  of one real repo-relative artifact (`locator`, `bytes`, `sha256`, `files=1`,
  optional bounded `supplementary`) and `integrity` with
  `commit_marker=OPEN-PROBLEM-CHECKPOINT-COMMIT-V1` plus a SHA-256 of the
  canonical compact JSON of the payload excluding integrity. A same-identity
  index with `schema_version=sealed-candidate-pair-index.v1`, identical sequence,
  `candidate_only=true`, `claim_ceiling=candidate_only`, and
  `latest_checkpoint=runtime/<checkpoint-relative-to-runtime_root>` completes
  the pair. Unknown owner formats explicitly fail; the bridge never writes or
  re-signs owner data. A SHA-256 is an accidental-change checksum, **not an
  authenticity signature**.
- Private `0600` JSON config: exactly `schema_version=sealed-pair-shadow.v1`,
  the three frozen identity fields above, absolute real `repository_root`,
  `runtime_root`, `checkpoint`, `index`, and pre-existing owner-only `0700`
  `shadow_root` and `restore_root`. The roots must be separate; source paths
  must be inside their designated roots; shadow/restore must be outside both.
  To explicitly enable the command for one trusted session, set
  `VIBE_GOAL_SNAPSHOT_CONFIG`, `VIBE_GOAL_SNAPSHOT_SESSION_ID` and the SHA-256
  of `scripts/goal_shadow_bridge.py`, `scripts/goal_snapshot_store.py`, the
  real `/usr/bin/python3`, and `/usr/bin/zstd` as the four corresponding
  `VIBE_GOAL_SNAPSHOT_{CLI,STORE,PYTHON,ZSTD}_SHA256` environment variables.
  Obtain digests from the **current reviewed installation**, not this document.
  The command checks project trust, session/cwd, owner permissions and runtime
  bytes before launching isolated `python3 -I -S -B`; Python checks the same
  config bytes again before reading and before SQLite commit. `status`,
  `save <id> [parent]`, `restore <id> <new-directory-name>` never call a model.
  Default unset means zero research-source scans, zero child processes and zero
  storage writes. Restore only creates a new directory outside the source;
  it copies **checkpoint/index only** and does not archive artifacts, change
  the research recovery head or qualify as complete research recovery. The
  attachment's byte digest is checked on save; a non-cooperating writer can
  still race the last source re-read and SQLite commit. Owner-side read freeze
  or immutable generation is required for strict atomic capture.

The optional [local write guard](.pi/opt-in-extensions/README.md) is not loaded
by this template and refuses `bash/powershell` without independent filesystem
confinement. It cannot schedule research. Goal does not replace write isolation,
process supervision or mathematical admission. No template build modifies an
existing actor.
