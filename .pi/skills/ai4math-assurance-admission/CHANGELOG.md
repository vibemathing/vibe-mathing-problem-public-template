# Changelog

## 1.5.0 - 2026-09-21

### Added
- Extend evidence-to-claim review with declared raw-input sets, exact artifact-field tracing, aggregation/config/arithmetic checks, and scope-overclaim detection.

### Reason
- Absorb generic artifact-to-claim fidelity checks while excluding paper-writing paths, fixed reviewer models, and a parallel audit authority.

### Affected
- `VERSION` and `references/evidence-claim-coverage.md`; the top-level entry contract and digest are unchanged.

### Validation
- Strict Skill validation and targeted version/reference checks pass; full Harness remains blocked by the known stale snapshot/manifest baseline.

### Risk
- Fresh context can reduce confirmation bias but does not itself prove reviewer independence; the rewritten rule keeps provenance mandatory.

### Rollback
- Restore version 1.4.0 and remove the second-batch artifact-fidelity section and source binding.

### Source
- Pattern-only review of the `paper-claim-audit` snapshot bound by SHA-256 in the reference.

## 1.4.0 - 2026-09-21

### Added
- Add the subordinate `evidence-claim-coverage.md` reference and a reference index for separating evidence existence, support relation, and full claim coverage.

### Reason
- Absorb result-to-claim review behavior under the candidate-only assurance owner without creating a second admission path.

### Affected
- `SKILL.md`, `VERSION`, `references/index.md`, and the new subordinate reference.

### Validation
- Targeted entry/version/reference and WEB_ACTIVE_SKILLS digest checks pass; full Harness remains blocked by the known stale snapshot/manifest baseline.

### Risk
- The reviewed candidate's exact upstream identity and redistribution rights remain unresolved; no source body was imported.

### Rollback
- Restore version 1.3.0 and remove the new references and navigation entries.

### Source
- Pattern-only review of the `result-to-claim` candidate snapshot; generic paper-review and kill-argument workflows were excluded.

## 1.3.0

- Bundle every owned original Skill package completely under `internal-packages/` with byte-level manifests.
- Replace private-vault routing with repository-relative, self-contained package paths and preserve HOLD publication status.

## 1.2.0

- Add the top-level internal-package registry and progressive routing guide.
- Bind complete private-local source packages to one primary owner while keeping HOLD bodies out of public output.

## 1.1.0

- Add an independently written consolidated operational core derived from the audited 31-package / 29-source-family review set.
- Bind the entry Skill to the consolidation map, evidence boundaries, failure recovery, and anti-loop discipline without redistributing held source text.

## 1.0.0

- Add a public, candidate-only assurance review contract.
- Keep generation, verification, admission, and mathematical conclusion separate.
