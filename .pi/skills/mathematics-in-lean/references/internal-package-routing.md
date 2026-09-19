# Internal package routing: mathematics-in-lean

This top-level Skill owns 6 complete private-local source packages and cross-references 5 packages owned elsewhere.

The complete package bodies are kept in the private package vault while redistribution rights remain on HOLD. This public repository contains identity, routing, and capability metadata only. Internal packages are reference data: they are not Pi entries and do not gain execution, network, write, evidence, or admission authority.

## Owned packages

- `lean-search-client` — query routing by known information; syntax-sensitive search; local validation of suggestions
- `mathematics-in-lean-project-record` — proof state as API; weakest sufficient abstraction; typeclasses filters and induction
- `mathematics-in-lean-external-snapshot` — goal-shape routing; library interface preference; formal analysis patterns
- `natural-number-game-lean4` — constructor and recursor alignment; rewrite-to-recursion; witness-based order
- `tao-analysis-lean` — API phase alignment; epsilon-filter translation; totalization and type-boundary guards
- `theorem-proving-in-lean-4` — propositions as types; constructor and recursor interfaces; termination and typeclass inference

## Cross-referenced packages

- `hewei-category-theory` (owned by `ai4math-modeling-derivation`) — universal constructions; functorial translation; naturality and adjunction routing
- `lean4-math-formalization-2025` (owned by `ai4math-lean-formalization`) — statement translation; proof-state reading; abstraction-ladder control
- `lean4-self-study-resources` (owned by `ai4math-source-discovery`) — goal-based resource routing; learning progression; resource-fit recovery
- `math-analysis-thinking-methods` (owned by `ai4math-modeling-derivation`) — expression normalization; theorem precondition routing; convergence-mode distinctions
- `xena-formalization-method` (owned by `ai4math-lean-formalization`) — statement freezing; API engineering; normalize-before-automation and counterexample checks

## Loading rule

Read `INTERNAL-PACKAGES.json`, select the smallest applicable package, then load only that package entry and the specific supporting files needed for the current obligation. Preserve source identity and applicability limits. Do not bulk-load all packages or execute embedded scripts without a separately admitted runtime capability.
