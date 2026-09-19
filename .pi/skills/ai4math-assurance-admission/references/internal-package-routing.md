# Internal package routing: ai4math-assurance-admission

This top-level Skill owns 1 complete private-local source packages and cross-references 6 packages owned elsewhere.

The complete package bodies are kept in the private package vault while redistribution rights remain on HOLD. This public repository contains identity, routing, and capability metadata only. Internal packages are reference data: they are not Pi entries and do not gain execution, network, write, evidence, or admission authority.

## Owned packages

- `lean-eval-comparator` — pristine-versus-edited comparison; isolated elaboration; pin and security audit

## Cross-referenced packages

- `baier-katoen-model-checking` (owned by `ai4math-bounded-computation`) — model/property separation; abstraction soundness; state-space control
- `danus-proof-orchestration` (owned by `ai4math-proof-refutation`) — producer/verifier separation; fact-graph memory; falsification before persistence
- `harrison-automated-reasoning` (owned by `ai4math-proof-refutation`) — logic-fragment routing; rewriting and decision-procedure scope; LCF trust boundary
- `rethlas-math-reasoning` (owned by `ai4math-proof-refutation`) — persistent proof state; retrieval applicability checks; strict verification and degraded-mode honesty
- `welleck-informal-formal-reasoning` (owned by `ai4math-lean-formalization`) — verifier hard boundary; retrieval before brute force; reasoning-proving interleaving
- `xena-formalization-method` (owned by `ai4math-lean-formalization`) — statement freezing; API engineering; normalize-before-automation and counterexample checks

## Loading rule

Read `INTERNAL-PACKAGES.json`, select the smallest applicable package, then load only that package entry and the specific supporting files needed for the current obligation. Preserve source identity and applicability limits. Do not bulk-load all packages or execute embedded scripts without a separately admitted runtime capability.
