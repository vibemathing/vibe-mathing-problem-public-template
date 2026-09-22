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
