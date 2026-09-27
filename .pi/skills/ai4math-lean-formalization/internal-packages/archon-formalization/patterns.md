# Patterns

## Dependency-Ready Frontier
**When to use**: selecting prover objectives.
**How**: build the DAG; identify open declarations whose prerequisites are ready; remove downstream files with failed local imports unless their blocker is also being fixed; rank work by impact on the goal cone.
**Trade-offs**: maximizes useful parallelism but may defer attractive high-level goals.

## Blueprint-First Decomposition
**When to use**: a theorem is large, vague, or repeatedly stalls.
**How**: strengthen the informal proof; split it into explicit dependency-linked subclaims; map each to Lean; run fine-grained proving; recurse on the remaining hard subclaims.
**Trade-offs**: creates more declarations and blueprint maintenance, but turns opaque failures into local obligations.

## Evidence-Gated Completion
**When to use**: before declaring a phase/project complete.
**How**: build; count sorries; synchronize earned proof markers; run blueprint doctor and axiom sweep; reconcile unmatched Lean/blueprint declarations; review actual attempt logs.
**Trade-offs**: costs extra checks but prevents cosmetic completion and hidden assumptions.

## Churn Breaker
**When to use**: repeated iterations add prose/helpers while target metrics stay flat.
**How**: classify the blocker; reduce objective breadth; switch mode; request fresh-context strategy/progress critique; falsify load-bearing assumptions; choose a materially different route.
**Trade-offs**: abandons sunk work sooner, which is desirable when evidence says the route is not converging.

## Missing-Library Gradient
**When to use**: a needed Mathlib theorem/API appears absent.
**How**: verify via Lean search; try informal guidance when configured; implement a small local helper if feasible; formalize a precise gap; route substantial missing infrastructure through `mathlib-build`.
**Trade-offs**: local infrastructure increases maintenance but is better than repeated search for a nonexistent theorem.

## Protected Refactor
**When to use**: structural changes are needed around user-owned declarations.
**How**: load protection rules; preserve protected names/signatures/bodies according to level; move declarations only under allowed semantics; update path keys when required; use inner-git snapshots.
**Trade-offs**: may constrain the cleanest refactor; user intent wins.

## Multilane Race
**When to use**: provider/model diversity may solve hard proofs differently.
**How**: isolate lanes in worktrees; race the same assignments; accept clean candidates; apply grace window; merge best proof per declaration; verify final build.
**Trade-offs**: higher cost and merge complexity; do not use for deterministic structural blockers.

## DAG-Driven Reuse
**When to use**: related projects share declarations.
**How**: build peer DAGs; compute overlap/unblock/duplication; extract common cones or merge declaration versions; preserve names/signatures; verify dependency closure and builds.
**Trade-offs**: shared naming/blueprint discipline becomes more important.
