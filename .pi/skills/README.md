# Project Pi Skills

This directory is the self-contained, project-local mathematical Skill suite for a single-problem repository. Pi loads only the exact entries declared in `../settings.json` after the project is trusted.

| Skill | Responsibility | Status |
|---|---|---|
| `solve` | Cross-domain operator selection, bounded method application, switching, and stopping | active |
| `mathematics-in-lean` | Lean 4/Mathlib proof engineering | active |
| `prove2me` | External Lean theorem workflow | constrained |
| `ai4math-source-discovery` | Sources, prior art, and statement comparison | active |
| `ai4math-modeling-derivation` | Modeling, definitions, and derivations | active |
| `ai4math-proof-refutation` | Proofs, refutations, and adversarial audit | active |
| `ai4math-bounded-computation` | Bounded exact/numeric experiments | constrained |
| `ai4math-lean-formalization` | Statement-faithful Lean candidates | constrained |
| `ai4math-assurance-admission` | Candidate-only assurance recommendation | constrained |
| `ai4math-toolchain-reproducibility` | Tool/source identity and reproducibility planning | constrained |

The suite contains the restored full `solve` operator library, `prove2me`, and eight top-level mathematical capability Skills. See [`INTERNAL-PACKAGE-ARCHITECTURE.md`](INTERNAL-PACKAGE-ARCHITECTURE.md) for the complete packaging, loading, authority, deduplication, and publication model. The eight top-level Skills classify all 31 audited packages from 29 source families through [`INTERNAL-PACKAGE-CLASSIFICATION.json`](INTERNAL-PACKAGE-CLASSIFICATION.json), per-Skill `INTERNAL-PACKAGES.json` registries, and `references/internal-package-routing.md`. Complete HOLD package bodies are preserved only in the private-local package vault; this public repository carries identity and routing metadata until rights admission. [`CONSOLIDATION-MAP.md`](CONSOLIDATION-MAP.md), [`SOURCE-ABSTRACTION-MAP.json`](SOURCE-ABSTRACTION-MAP.json), and each `references/consolidated-core.md` preserve the project-authored cross-source synthesis.

The canonical research actor owns mathematical strategy and may select, combine, change, or ignore these capabilities. Skill output is candidate-only unless an independent verifier and admission gate establish more. No Skill may create its own authority, call self-review independent, or turn runtime/transport success into a Result.

Do not add user-global, controller, session-fleet, compute-node, credential-bearing, or private-only Skills here. A new public Skill requires source and license review, bounded dependencies, pressure tests, explicit failure semantics, and snapshot/validator updates.
