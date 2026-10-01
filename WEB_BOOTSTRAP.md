# Web Research Bootstrap

- Repository: `vibemathing/vibe-mathing-problem-public-template`
- Repository binding: `planned`
- Repository database ID: `pending`
- Repository node ID: `pending`
- Default branch: `main`
- Visibility: `public`
- Canonical Problem: `problem:template-placeholder`
- ProblemContract SHA-256: `f9236ddb5a3e6f9b9c0701df3ce6ddcab5391b930ee374a25b99207450f88027`
- Problem lifecycle: `draft`
- Problem admission: `preview_unadmitted`
- Harness suite: `harness-source:web-research-full` `2.3.5`
- Suite manifest SHA-256: `5936efe64b64a725e7014a70ffe7ed293ee52d5a905312cc2af099df8d5d3c5e`
- Harness snapshot SHA-256: `376f224ef96a4c0135767cd25b46ed5cb229aac46384e2231a28a93c8ef8633d`
- Channel: `chatgpt-web-github-issue-pr-writer`
- Project runtime: `Pi` with exact entries from `.pi/settings.json`

## Required read order

1. `AGENTS.md`
2. `.pi/settings.json`
3. `governance/control-plane/web-context-profile.v1.json`
4. `WEB_CHANNEL_PROFILE.json`
5. `HARNESS_SNAPSHOT.json`
6. `WEB_CONTEXT_BUNDLE.md`
7. `WEB_ACTIVE_SKILLS.json`
8. `problem-library/records/canonical-problems.jsonl`
9. `research/records/failed-routes.jsonl`
10. the current route and obligation packet named by the Issue
11. exactly the owner Skill files selected by `WEB_ACTIVE_SKILLS.json`
12. `WEB_OUTPUT_CONTRACT.json`

Return a `web-bootstrap-ack.schema.json` object before mathematical work. Hashes shown here are manifest-declared values; do not claim to have recomputed them in chat. The context profile is a hard budget and selector policy: an ambiguous or missing execution identity is catalog-only and fail-closed.

## Coordinator-only planning mode

If the user requests a one-problem T1–T9 coordination plan rather than Issue-bound mathematical work, read `WEB_COORDINATOR.md` and follow that contract. This mode does not create a research Issue, Attempt, Route, Obligation, session, branch, CandidateArtifact, Evidence or Result. It may emit runnable startup prompts only for nine matching lane packets already pre-admitted on the current default branch; otherwise it returns `BLOCK_PRE_ADMISSION` plus non-runnable planning drafts for a trusted maintainer. It is not a tenth mathematical lane. A human must create each worker conversation and copy only a freshly admitted runnable prompt; the coordinator must not claim that prompt generation launched any worker.

## Fresh-state gate precedence

At the start of every turn, refresh the default branch plus live Issue/branch/PR/check state. Current repository records outrank launch-prompt SHAs, and launch-prompt SHAs outrank old chat replies. A controlled merge may legitimately advance main or the Harness snapshot; use the fresh revision as the packet base after validating the new snapshot. Never repeat an old `BLOCK_PRE_ADMISSION` unless a fresh read proves that the exact Attempt/Route/Graph/Obligation is currently absent or mismatched.

Channel audit maturity is not repository admission. The current template profile is `synthetic_only_pending_permission_and_ruleset_smoke`; this blocks Issue/branch/PR research transport until fresh live repository-object receipts and an explicit admission update are present. Even after admission, the namespace remains candidate-only and grants no Evidence/Result authority.

Branch protection and automated required checks are transport controls, not demands for manual approval. Reuse the one Issue identified by `(problem_id, attempt_id, route_id, obligation_id)` and label `web-research-question`; search before create, including a second fresh search immediately before creation, so retries and concurrent turns stay idempotent.

One Web response ending is a runtime boundary, not a permission failure and not mathematical completion. Before the boundary, save the best bounded checkpoint when possible. The next turn must resume by rereading current main and live GitHub state rather than replaying a stale bootstrap decision.

## AI-native writable route

Only after the profile changes to an explicitly admitted state may the routine candidate transport run end to end without project-added human handoffs:

1. Reuse the unique Issue labeled `web-research-question` for the exact Problem/Attempt/Route/Obligation tuple; create one only after two fresh searches find none.
2. Create branch `web/attempt-<attempt-suffix>`.
3. Add, revise, or delete files only under `research/artifacts/web-inbox/**`, `research/artifacts/candidates/**`, or `research/artifacts/source-notes/**`.
4. Commit real changes and open a PR using the web candidate template.
5. Monitor required checks and, when needed, rerun the existing candidate workflow.
6. Review and revise the candidate PR; this AI review is not independent mathematical review.
7. After transport checks pass, merge the candidate PR and write the next checkpoint.

Do not create repositories, direct-push the default branch, modify workflow/truth paths, force-push, cancel/dispatch Actions, or sign Evidence/Result. Follow only platform-mandatory confirmation UI; no extra human approval is required for routine candidate operations. Issue, PR, review, merge, Actions status, command exit 0, or model self-review never closes a mathematical obligation.
