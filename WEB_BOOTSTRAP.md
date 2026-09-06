# Web Research Bootstrap

- Repository: `vibemathing/vibe-mathing-problem-public-template`
- Repository binding: `verified`
- Repository database ID: `1358726712`
- Repository node ID: `R_kgDOUPyGOA`
- Default branch: `main`
- Visibility: `public`
- Canonical Problem: `problem:template-placeholder`
- ProblemContract SHA-256: `e64cd03254e03dd661eade23243c3c21793fc2d8bffa2d33c172cf8ed2e7f940`
- Problem lifecycle: `draft`
- Problem admission: `preview_unadmitted`
- Harness suite: `harness-source:web-research-full` `1.1.0`
- Suite manifest SHA-256: `d99842bc4afd937a6fa171aa0ad244e5cae2a1ff7091c2c3d59b1dad765b7e31`
- Harness snapshot SHA-256: `fcc65ffb711a1cf524e042c854588fa84596d144c4f687a6f0e8b34f06488647`
- Channel: `chatgpt-web-github-issue-pr-writer`

## Required read order

1. `AGENTS.md`
2. `WEB_CHANNEL_PROFILE.json`
3. `HARNESS_SNAPSHOT.json`
4. `WEB_CONTEXT_BUNDLE.md`
5. `WEB_ACTIVE_SKILLS.json`
6. `problem-library/records/canonical-problems.jsonl`
7. `research/records/failed-routes.jsonl`
8. the current route and obligation packet named by the Issue
9. exactly the owner Skill files selected by `WEB_ACTIVE_SKILLS.json`
10. `WEB_OUTPUT_CONTRACT.json`

Return a `web-bootstrap-ack.schema.json` object before mathematical work. Hashes shown here are manifest-declared values; do not claim to have recomputed them in chat.

## AI-native writable route

After repository admission, perform the routine candidate transport end to end without project-added human handoffs:

1. Open or use one Issue labeled `web-research-question` for the bounded question.
2. Create branch `web/attempt-<attempt-suffix>`.
3. Add, revise, or delete files only under `research/artifacts/web-inbox/**`, `research/artifacts/candidates/**`, or `research/artifacts/source-notes/**`.
4. Commit real changes and open a PR using the web candidate template.
5. Monitor required checks and, when needed, rerun the existing candidate workflow.
6. Review and revise the candidate PR; this AI review is not independent mathematical review.
7. After transport checks pass, merge the candidate PR and write the next checkpoint.

Do not create repositories, direct-push the default branch, modify workflow/truth paths, force-push, cancel/dispatch Actions, or sign Evidence/Result. Follow only platform-mandatory confirmation UI; no extra human approval is required for routine candidate operations. Issue, PR, review, merge, Actions status, command exit 0, or model self-review never closes a mathematical obligation.
