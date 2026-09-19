# Vibe Mathing Single-Problem Research Repository

This repository contains one canonical ProblemContract plus a fixed, self-contained Vibe Mathing Harness snapshot.

The repository is Pi-native: after you trust the project, Pi discovers only the project Skill entries declared in [`.pi/settings.json`](.pi/settings.json). Eight top-level mathematical Skills bundle and route all 31 complete source packages through repository-relative internal-package registries. Rights remain HOLD, so repository bundling does not itself authorize public redistribution. Start `pi` from the repository root, verify that the `.pi/skills/` entries are visible, and then choose one research mode:

- **T1–T9 coordinator (one ChatGPT Project, one problem):** read `AGENTS.md`, then [`WEB_COORDINATOR.md`](WEB_COORDINATOR.md). The coordinator performs fresh-state preflight and emits nine bounded worker prompts; it is not a tenth mathematical lane.
- **Issue-bound research worker:** read `AGENTS.md`, `WEB_BOOTSTRAP.md`, `HARNESS_SNAPSHOT.json`, `WEB_CONTEXT_BUNDLE.md`, and the Issue-bound Attempt/Route/Obligation.
- **Local canonical Pi researcher:** read `AGENTS.md`, the frozen ProblemContract, current failed-route memory, and the relevant project Skill only. Local candidate work still has no Evidence/Result admission authority.

After one-time repository admission, the Web GPT GitHub channel owns the routine candidate flow end to end: Issue, `web/attempt-*`, candidate file revisions, commits, PR creation/review, check monitoring/rerun, merge, and checkpoint. It cannot create the repository, direct-write protected/truth paths, or admit Evidence, Results, or Solutions. Machine gates and independent mathematical verification remain required for mathematical closure; routine human handoffs do not.

A repository URL by itself is not a complete bootstrap. The user must direct the coordinator to `WEB_COORDINATOR.md` or the worker to `WEB_BOOTSTRAP.md` so the model reads the frozen contracts instead of guessing from chat memory.
