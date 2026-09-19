# Internal package routing: ai4math-toolchain-reproducibility

This top-level Skill owns 1 complete private-local source packages and cross-references 7 packages owned elsewhere.

The complete package bodies are kept in the private package vault while redistribution rights remain on HOLD. This public repository contains identity, routing, and capability metadata only. Internal packages are reference data: they are not Pi entries and do not gain execution, network, write, evidence, or admission authority.

## Owned packages

- `leansearch-operator` — parse/index/embed/search pipeline; schema and revision pinning; service diagnostics

## Cross-referenced packages

- `ai4math-research-navigator` (owned by `ai4math-source-discovery`) — artifact and modality routing; evaluation design; research-system comparison
- `archon-formalization` (owned by `ai4math-lean-formalization`) — dependency-aware formalization; plan/prove/review separation; stalled-run diagnosis
- `dong-ai4m-research-guide` (owned by `ai4math-source-discovery`) — capability diagnosis; specialist-versus-general tool choice; verifier feedback
- `dongbin-ai4m` (owned by `ai4math-source-discovery`) — capability diagnosis; formalization stack; understanding-over-ritual objective
- `jixia-lean-analyzer` (owned by `ai4math-lean-formalization`) — toolchain matching; InfoTree and declaration products; static-analysis diagnostics
- `lean-eval-comparator` (owned by `ai4math-assurance-admission`) — pristine-versus-edited comparison; isolated elaboration; pin and security audit
- `lean4-metaprogramming` (owned by `ai4math-lean-formalization`) — syntax/elaboration/kernel staging; metavariable state and rollback; generated-term validation

## Loading rule

Read `INTERNAL-PACKAGES.json`, select the smallest applicable package, then load only that package entry and the specific supporting files needed for the current obligation. Preserve source identity and applicability limits. Do not bulk-load all packages or execute embedded scripts without a separately admitted runtime capability.
