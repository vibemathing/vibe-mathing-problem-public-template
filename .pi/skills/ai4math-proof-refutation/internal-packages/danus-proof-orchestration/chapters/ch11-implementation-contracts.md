# 11 — Implementation Contracts and Deterministic Boundaries

## Design principle

Danus wraps deterministic operations in code and leaves mathematical judgment to isolated agents. This separation makes state transitions, role permissions, hashing, filesystem integrity, authoring gates, and recovery testable without pretending that proof correctness is deterministic software logic.

## Core modules

- `danus.core`: local memory, global memory, fact graph, glossary, BM25 search, schemas.
- `danus.execution`: canonical project/worker layout, scaffolding, detached worker loop.
- `danus.orchestration`: CLI verbs over execution lifecycle.
- `danus.gateway`: role-gated MCP surface and `fact_submit` verification gate.
- `danus.verify`: HTTP service, deterministic prechecks, cold-start verifier launcher.
- `danus.integrations`: theorem-search integration.
- `danus.observability`: read-only dashboard over facts/memory.
- `danus.human_summary`: isolated scrubbed report authoring.
- `danus.write_paper`: target resolution, prompt assembly, curation, authoring, reference verification, revision, whole-paper math gate.
- `danus.authoring`: shared isolated subprocess and artifact-safety helpers.

## Deterministic boundaries worth preserving

### Fact identity

Hash only mathematical identity fields. Keep mutable citation metadata outside the hash. Deduplicate identical content and reject dependencies on revoked predecessors.

### Status/event persistence

Use append-only logs where historical transitions matter. Current global-memory status is folded from the latest status event. Worker status files are written atomically.

### Process isolation

Workers run in separate process groups. Authoring/verifier calls use isolated working contexts. Resumability comes from persisted stores, reducing coupling to process continuity.

### Role registration

Build the gateway's tool table from the role at call/start time. Unknown roles receive the read-only verifier-like surface.

### Target resolution

Paper target precedence is explicit call → brief → finalized target → unset. “Unset” is a real state and must yield refusal rather than heuristic selection.

### Paper curation

`paper_subgraph` returns a deterministic compact skeleton. Selected fact ids are checked for existence and target-closure relationship. The writer receives full bodies only for the curated presentation set when selection is used.

### Patch application

Paper revisions use unique exact find/replace blocks. Zero matches, multiple matches, no applied edits, large shrinkage, leaks, or compile failures fail honestly without overwriting the last clean paper.

### Leak scanning

Human reports and papers use deterministic patterns to block internal ids/machinery from reader-facing output. Quarantine is preferable to delivery of a suspect artifact.

## Test-derived behaviors

The supplied test suite verifies, among other things:

- fact content addressing, search, glossary coverage, external-reference mutability, and cascade revocation;
- worker loop stop/deadline/failure behavior and restartability;
- role-gated gateway surfaces and verification trace semantics;
- verifier prechecks, subprocess error handling, and strict verdict plumbing;
- target-closure paper scoping, per-paper workspaces, support-layer selection, citation ledgers, leak gates, compile retry, patch safety, and whole-document math verification;
- human-summary scrubbing and failure honesty;
- read-only observability behavior.

One source test expects `chmod(000)` to make a JSONL file unreadable. When tests run as root, root can still read that file, so that test fails due to privilege semantics rather than a Danus logic defect. Record this environment caveat instead of labeling the entire suite clean.

## Portability cautions

- MCP package availability is an environment dependency; core logic can be tested independently, while MCP-facing modules need the compatible package or an interface-faithful test stub.
- LaTeX compile gating is strongest when a supported engine is installed. If no engine exists, the paper tool reports that compilation was skipped.
- Model names, reasoning efforts, API endpoints, and ports are configuration, not enduring methodological rules.

## Implementation self-check

When extending Danus, ask:

1. Can this operation be deterministic? If yes, keep it out of a free-form agent prompt.
2. Does it cross a trust boundary? If yes, enforce the boundary through tool surface and validation.
3. Does failure leave a misleading partial artifact? If yes, quarantine or fail atomically.
4. Does mutable metadata participate in mathematical identity? Avoid unnecessary hash churn.
5. Can the process crash without losing verified state? Persist state before relying on process continuity.
6. Is a test failure caused by code semantics or execution-environment semantics? Separate them explicitly.
