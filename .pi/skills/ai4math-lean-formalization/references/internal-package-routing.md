# Internal package routing: ai4math-lean-formalization

This top-level Skill owns 6 complete private-local source packages and cross-references 8 packages owned elsewhere.

The complete package bodies are kept in the private package vault while redistribution rights remain on HOLD. This public repository contains identity, routing, and capability metadata only. Internal packages are reference data: they are not Pi entries and do not gain execution, network, write, evidence, or admission authority.

## Owned packages

- `archon-formalization` — dependency-aware formalization; plan/prove/review separation; stalled-run diagnosis
- `jixia-lean-analyzer` — toolchain matching; InfoTree and declaration products; static-analysis diagnostics
- `lean4-math-formalization-2025` — statement translation; proof-state reading; abstraction-ladder control
- `lean4-metaprogramming` — syntax/elaboration/kernel staging; metavariable state and rollback; generated-term validation
- `welleck-informal-formal-reasoning` — verifier hard boundary; retrieval before brute force; reasoning-proving interleaving
- `xena-formalization-method` — statement freezing; API engineering; normalize-before-automation and counterexample checks

## Cross-referenced packages

- `classical-type-theory` (owned by `ai4math-proof-refutation`) — type-directed search; dependency-preserving Skolemization; higher-order unification limits
- `lean-search-client` (owned by `mathematics-in-lean`) — query routing by known information; syntax-sensitive search; local validation of suggestions
- `leansearch-operator` (owned by `ai4math-toolchain-reproducibility`) — parse/index/embed/search pipeline; schema and revision pinning; service diagnostics
- `mathematics-in-lean-project-record` (owned by `mathematics-in-lean`) — proof state as API; weakest sufficient abstraction; typeclasses filters and induction
- `mathematics-in-lean-external-snapshot` (owned by `mathematics-in-lean`) — goal-shape routing; library interface preference; formal analysis patterns
- `natural-number-game-lean4` (owned by `mathematics-in-lean`) — constructor and recursor alignment; rewrite-to-recursion; witness-based order
- `tao-analysis-lean` (owned by `mathematics-in-lean`) — API phase alignment; epsilon-filter translation; totalization and type-boundary guards
- `theorem-proving-in-lean-4` (owned by `mathematics-in-lean`) — propositions as types; constructor and recursor interfaces; termination and typeclass inference

## Loading rule

Read `INTERNAL-PACKAGES.json`, select the smallest applicable package, then load only that package entry and the specific supporting files needed for the current obligation. Preserve source identity and applicability limits. Do not bulk-load all packages or execute embedded scripts without a separately admitted runtime capability.
