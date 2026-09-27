# Release checklist

A release is complete only when every gate below has a fresh receipt bound to
this exact commit and generated snapshot. Whole-template upgrades use a
`maintenance/template-release-<VERSION>` PR from a trusted publisher and an
incremented, rebuilt snapshot/history (`--continue-snapshot-history` retains the
verified old entries for the same repository). This route never relaxes `web/attempt-*`
candidate validation or authorizes mathematical truth changes. A prior PR's
one-time override is not a new release receipt.

- [ ] Every bundled source has an official URL and immutable revision.
- [ ] LICENSE/NOTICE and attribution are verified for every source family.
- [ ] Every package has a rights-holder receipt and
      `public_redistribution_admitted=true`.
- [ ] Public privacy, path, symlink, mode, binary, dependency and secret scans
      pass.
- [ ] For a concrete problem repository, the canonical ProblemContract and source ledger are exact and admitted. For this generic template, C05 is explicitly not applicable because the inert placeholder is intentionally retained.
- [ ] Harness snapshot, history, source manifest and generated output are
      regenerated atomically; no unlisted files remain.
- [ ] `make check-full` passes in a clean independent checkout.
- [ ] For a concrete problem repository, Web repository identity, visibility,
      default branch, protection rules and required checks have fresh live-object
      receipts. For this generic template, C08 is explicitly not applicable
      because no live research repository is bound.
- [ ] Candidate, Evidence, Result, Solution and mathematical admission remain
      separate; no PR or CI result is described as a solution.
- [ ] An independent maintainer reviews this checklist and records the commit,
      snapshot digest, release mode and decision.

The builder must fail closed when any applicable item is missing. The 31
project-authored packages are MIT-licensed and require the owner attestation
plus immutable tree digests. Run `make audit-release` for a machine-readable
C01–C10 decision. A generic template may pass C05/C08 as not-applicable; a
concrete problem repository may not.
