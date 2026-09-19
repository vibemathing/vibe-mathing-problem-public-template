# Archon Decision Cheatsheet

| Signal | Decision |
|---|---|
| One isolated Lean goal | Use direct Lean workflow; skip Archon orchestration |
| Multi-file project + informal mathematics | Initialize Archon and build/repair blueprint DAG |
| Blueprint route has broken `\uses` / unmatched declarations | Repair DAG before prover budget |
| Lean file lacks declarations described by blueprint | `formalize` |
| Compiling file has ordinary sorries | `prove` |
| Same complex theorem stalls across passes | `fine-grained` + blueprint decomposition |
| Library ingredient verified absent | local helper / `mathlib-build` |
| Sorries closed | `polish`; `golf` only for explicit minimization |
| Prior build failed in imported file | Fix blocker before downstream objective, unless blocker is co-assigned |
| Objective fan-out is large | Keep a bounded ready frontier; defer the rest |
| Comments/helpers increase, sorry count flat | Mark churn; switch route/mode or critique strategy |
| Need automatic commands with workspace write boundary | `archon loop --safe` |
| Must freeze theorem signature | `archon-protected.yaml`: Lean `signature` |
| Must freeze declaration body too | protection level `all` |
| Iteration interrupted | `archon loop --resume` |
| Agent change went bad | `archon log`; fork known-good commit with `archon branch ... --from ...` |
| Multiple providers worth racing | enable multilane; preserve isolated worktrees |
| Multiple projects duplicate declarations | `archon scope roadmap`; extract/merge from DAG facts |
| Completion claimed with sorries | return to prover; do not accept COMPLETE |

## Completion Checklist
- `lake build` / configured integration build passes.
- No target `sorry` remains.
- No unacceptable axiom or `sorryAx` laundering.
- `sync_leanok` state matches compilable declarations.
- Blueprint doctor has no blocking findings.
- Lean↔blueprint coverage is reconciled.
- Protected surfaces are unchanged.
- Review evidence explains the last blockers/closures.

## Recovery Order
State/orchestration → dependency/build → blueprint/math → prover mode → library gap → model/provider → strategy fork. Fix the earliest causal layer first.
