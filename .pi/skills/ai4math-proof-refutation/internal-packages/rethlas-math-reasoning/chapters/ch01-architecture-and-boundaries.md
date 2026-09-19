# Chapter 1: Architecture & Boundaries

## Core Idea
Rethlas separates proof generation from proof verification and makes filesystem boundaries part of correctness. Generation creates and repairs a proof blueprint; verification independently audits the complete draft through a local service.

## Frameworks Introduced

- **Two-agent proof pipeline**
  - **When to use**: research-level proof work where generation and checking should be separated.
  - **How**: start the verification service, run the generation agent, let generation submit only complete proof drafts, repair from structured verifier output.
- **Data-relative problem identity**
  - **When to use**: every run with persistent artifacts.
  - **How**: derive `problem_id` from the path below `data/`, remove the `.md` suffix, and preserve subdirectories. `data/algebra/p.md` maps to `algebra/p`.
- **Workspace boundary**
  - **When to use**: all file access during generation.
  - **How**: keep problems, references, downloads, logs, memory, results, skills, and scripts under the active working tree; reject parent traversal and absolute problem paths.

## Key Concepts

- **Generation agent** — reads the problem, explores proof routes, writes `blueprint.md`, and repairs it from verifier findings.
- **Verification agent** — checks a complete markdown proof and emits structured errors, gaps, verdict, and repair hints.
- **Problem file** — authoritative local theorem statement in markdown.
- **Reference directory** — sibling `<problem>.refs/` holding problem-specific user material.
- **User reference status** — useful context that remains unverified until checked.
- **Verified blueprint** — proof artifact promoted only after the strict verifier passes.

## Mental Models

- Treat **generation and verification as separate trust domains**: generation may be creative; acceptance is conservative.
- Treat **path discipline as state discipline**: a stable `problem_id` is the join key across memory, logs, results, and recursive agents.
- Treat **user-supplied references as leads**: cite their influence, then independently validate claims that matter to the proof.

## Anti-patterns

- **Flattening problem IDs**: two category paths can collide and memory becomes ambiguous.
- **Reading outside the working tree**: breaks the source's isolation invariant and makes runs harder to reproduce.
- **Calling the verifier on fragments**: verifier semantics assume a full proof of the whole target.
- **Treating the generator's confidence as acceptance**: the verified artifact exists only after the verifier gate.

## Commands & APIs

Typical local order:

```text
verification HTTP service → generation runner → generation MCP tools → verifier repair loop
```

The source defaults the verification API to local port `8091` and exposes a health endpoint plus a proof-verification endpoint.

## Reference Table

| Artifact | Canonical relative location | Purpose |
|---|---|---|
| Problem | `data/<problem>.md` | authoritative input statement |
| References | `data/<problem>.refs/` | optional local context |
| Draft | `results/<problem_id>/blueprint.md` | current full proof draft |
| Verified proof | `results/<problem_id>/blueprint_verified.md` | accepted proof artifact |
| Memory | `memory/<problem_id>/` | persistent reasoning state |
| Iteration logs | `logs/<problem_id>/iter/` | runner trace |

## Worked Example

For `data/modrep/modrep.md`, use `problem_id=modrep/modrep`. Read `data/modrep/modrep.refs/` before external search. All memory goes under `memory/modrep/modrep/`; the final draft and verified artifact live under the matching results directory. The path identity is preserved across generation and recursive work.

## Key Takeaways

1. Separate proof production from proof acceptance.
2. Keep one stable data-relative identifier through the entire run.
3. Keep file access inside the active workspace.
4. Read problem-specific references early while retaining their unverified status.
5. Submit only complete drafts to the verifier.

## Connects To

- **Ch 2**: problem identity scopes persistent memory.
- **Ch 9**: the verification agent defines the acceptance gate.
- **Ch 10**: the runner enforces input paths and service order.

## Source Provenance

Primary source files: `README.md`, `agents/generation/AGENTS.md`, `agents/generation/mcp/server.py`, `agents/verification/AGENTS.md`, `agents/verification/api/server.py`, and the generation/verification Codex configs.
