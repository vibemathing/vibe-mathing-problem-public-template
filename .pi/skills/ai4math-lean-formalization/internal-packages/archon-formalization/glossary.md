# Glossary

**AUTO_NOTES.md** — loop-managed feedback from deterministic validation to the next plan pass.

**Backend** — the launch mechanism for Claude Code; separate from the harness/engine choice.

**Blueprint** — LeanBlueprint mathematical specification containing statements, proofs, labels, Lean mappings, dependencies, and source provenance.

**Blueprint debt** — Lean declarations/helpers lacking corresponding blueprint representation or dependency edges.

**Blueprint doctor** — deterministic lint for orphan chapters, references, malformed annotations, axioms, and coverage structure.

**Blocked dependency** — a local imported Lean file whose build failure prevents a downstream file from elaborating reliably.

**DAG / LeanDag** — dependency graph used to reason about declaration readiness, ancestry, gaps, and cross-project overlap.

**Fine-grained mode** — prover mode that converts informal proof sentences into atomic Lean sublemmas and attempts each separately.

**Harness** — execution engine used for an Archon role/subagent, such as Claude Code or Codex.

**Inner git** — Archon-managed repository under `.archon/git-dir` recording agent-phase history independently of the user's outer git.

**Lane** — isolated prover configuration/worktree used in multilane execution.

**Objective** — a file-scoped unit selected by the planner for a prover iteration.

**Plan agent** — role that owns strategy, blueprint-aware routing, and objective selection; it does not write Lean proofs.

**Protected surface** — user-defined declarations, blueprint blocks/files, or arbitrary paths frozen by `archon-protected.yaml`.

**Prover** — role that edits assigned Lean files, makes tactical proof decisions, compiles, and logs actual attempts.

**Review agent** — role that audits attempt evidence, synthesizes proof-journal/project status, and checks blueprint/Lean consistency.

**Safe mode** — workspace-write sandbox mode requested with `archon loop --safe`.

**Scope** — a group of peer Archon projects analyzed together for unblock opportunities, duplication, leverage, and reuse.

**`sorryAx` laundering** — a declaration appears proved while its proof depends transitively on Lean's sorry axiom.

**Subagent** — descriptor-scoped focused agent with explicit read/write/spawn constraints.

**`sync_leanok`** — deterministic compilation-based synchronization of blueprint proof markers.
