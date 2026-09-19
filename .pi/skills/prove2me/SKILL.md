---
name: prove2me
description: Candidate workflow for discovering, decomposing, formalizing, and independently verifying Lean theorems through Prove2me. Use for theorem or mission inspection, proof sketches, reusable definitions, and submission preparation when network and publication actions are explicitly authorized.
---

# Prove2me Candidate Workflow

Use Prove2me as an external formalization and verification surface, not as automatic authority over this repository's ProblemContract or Result ledger.

## Workflow

1. Read the current platform statement and identifiers; never infer them from a title or stale transcript.
2. Compare the platform theorem type with the frozen local obligation and record every difference.
3. Develop and replay the Lean candidate locally when the pinned environment is available.
4. For decomposition, make child lemmas explicit and preserve the parent-to-child dependency graph.
5. Before any network submission or publication, require explicit authorization, fresh competition/identity checks where applicable, and a secret-safe transport path.
6. Bind any server verdict to the exact submitted source, theorem identifier, toolchain, and returned receipt.

A Prove2me `Proved` verdict establishes only the exact server theorem under its recorded environment. It does not by itself establish local statement faithfulness, independent replay, novelty, or Result admission.
