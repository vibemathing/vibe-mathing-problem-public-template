# Vibe Mathing Problem Research Template

This GitHub template contains the complete fixed Pi-native research Harness, its bounded Web transport profile, and one explicit non-admitted placeholder ProblemContract.

## Do not research the placeholder

`problem-library/records/canonical-problems.jsonl` in the template contains `problem:template-placeholder` with `lifecycle=draft` and `admission=preview_unadmitted`. It is only a physical-template fixture.

## Generate one concrete problem repository

1. Select the template matching the target repository visibility.
2. Admit exactly one reviewed ProblemContract with `lifecycle=active` in the problem library.
3. Create a repository named from its `problem_id`.
4. Read back GitHub database ID, node ID, visibility, and default branch.
5. Rebuild with verified repository identity and the exact canonical contract digest.
6. Validate the standalone snapshot before the first research operation.

The fixed suite is copied into every concrete problem repository. Its project Skills live under `.pi/skills/` and the exact Pi loading allowlist lives in `.pi/settings.json`; no user-global Skill is vendored into the repository. Eight top-level mathematical Skills contain all 31 audited source packages under repository-relative `internal-packages/` directories, with one physical copy per package and registry-based cross-references. Rights remain HOLD until source-specific publication admission. Only the ProblemContract and that problem's records vary. Issue, PR, merge, CI, checkpoint, and model output remain research transport/activity rather than mathematical evidence or Result admission.
