# Project Pi Skills

This directory is the self-contained, project-local mathematical Skill suite for a single-problem repository. Pi loads only the exact entries declared in `../settings.json` after the project is trusted.

| Skill | Responsibility | Status |
|---|---|---|
| `mathematics-in-lean` | Lean 4/Mathlib proof engineering | active |
| `prove2me` | External Lean theorem workflow | constrained |
| `ai4math-source-discovery` | Sources, prior art, and statement comparison | active |
| `ai4math-modeling-derivation` | Modeling, definitions, and derivations | active |
| `ai4math-proof-refutation` | Proofs, refutations, and adversarial audit | active |
| `ai4math-bounded-computation` | Bounded exact/numeric experiments | constrained |
| `ai4math-lean-formalization` | Statement-faithful Lean candidates | constrained |
| `ai4math-assurance-admission` | Candidate-only assurance recommendation | constrained |
| `ai4math-toolchain-reproducibility` | Tool/source identity and reproducibility planning | constrained |

The suite is backed by [`CONSOLIDATION-MAP.md`](CONSOLIDATION-MAP.md) and the machine-readable [`SOURCE-ABSTRACTION-MAP.json`](SOURCE-ABSTRACTION-MAP.json), which account for every item in the audited 31-package / 29-source-family review set. Every Skill routes to a substantial `references/consolidated-core.md`; unresolved-license source bodies are not redistributed.

The canonical research actor owns mathematical strategy and may select, combine, change, or ignore these capabilities. Skill output is candidate-only unless an independent verifier and admission gate establish more. No Skill may create its own authority, call self-review independent, or turn runtime/transport success into a Result.

Do not add user-global, controller, session-fleet, compute-node, credential-bearing, or private-only Skills here. A new public Skill requires source and license review, bounded dependencies, pressure tests, explicit failure semantics, and snapshot/validator updates.
