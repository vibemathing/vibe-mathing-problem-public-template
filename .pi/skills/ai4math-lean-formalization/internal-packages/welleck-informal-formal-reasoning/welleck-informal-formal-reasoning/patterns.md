# Operational Patterns

## Think → Tactic → Verify
**When to use**: the local proof state is clear but the next formal action is uncertain.  
**How**: write one compact strategic thought; generate a tactic conditioned on state+thought; run Lean; retain accepted state; branch/backtrack on rejection.  
**Trade-offs**: adds reasoning tokens and search control; value disappears if thoughts do not track the actual state.

## Verifier-Grounded Expert Iteration
**When to use**: training/improving a prover with cheap formal verification.  
**How**: sample complete proof trajectories → verify → keep successes → add them to training data → retrain → repeat.  
**Trade-offs**: success-only data can narrow diversity; requires enough successful exploration to bootstrap.

## Draft → Sketch → Prove
**When to use**: a high-level mathematical route exists but direct end-to-end formal proof generation is brittle.  
**How**: produce one or more informal drafts → translate major claims into a formal skeleton → leave small explicit gaps → close gaps with automation → verify complete proof.  
**Trade-offs**: quality depends on semantic alignment and gap granularity; bad drafts create unprovable sketches.

## Strategy-Level Sampling
**When to use**: low-level search has huge branching and candidate tactics are semantically repetitive.  
**How**: sample qualitatively different informal proof strategies/sketches first; allocate tactic/hammer budget only to promising decompositions.  
**Trade-offs**: higher setup cost; worthwhile when strategy diversity dominates syntax diversity.

## Neural Premise Retrieval
**When to use**: the goal should follow from known facts but the available library/project context is large.  
**How**: build query from current state → include global and local candidate premises → retrieve/rank top candidates → run automated prover → inspect missing-premise failures → rerank.  
**Trade-offs**: top-k can omit a crucial fact; retrieval quality depends on training objective and representation.

## Hammer with Stage Diagnosis
**When to use**: a local gap appears automatable.  
**How**: goal → premise selection → translation/Lean-native automation → ATP/search → reconstruction → Lean verification. On failure, identify the stage before retrying.  
**Trade-offs**: strong for local routine obligations; poor fit when the global proof idea is missing.

## Context-First Research Proving
**When to use**: theorem sits inside a real repository with custom definitions or long dependencies.  
**How**: capture imports/file position → collect preceding and cross-file declarations → rank relevant context → package exact identifiers/signatures → run proof search → record used dependencies.  
**Trade-offs**: full context can exceed budgets; aggressive pruning can hide the necessary fact.

## Blueprint Dependency Formalization
**When to use**: a research theorem depends on several unformalized prerequisites.  
**How**: create informal blueprint → build dependency DAG of definitions/lemmas/theorems → topologically formalize nodes → verify each → attack target only after prerequisites exist.  
**Trade-offs**: front-loads planning; prevents expensive search on an impossible target.

## Verified Metric-Driven Rewrite
**When to use**: a valid proof must become shorter, clearer, more declarative, or more modular.  
**How**: freeze verified baseline → define metric/constraints → rewrite one region → verify → score only valid candidate → keep strict improvement → repeat.  
**Trade-offs**: bad metrics are gameable; every accepted rewrite needs re-verification.

## Escalation Router
**When to use**: the first method fails.  
**How**: invalid tactic loops → change thought/branch; broad tactic explosion → DSP; routine gap + huge library → hammer; unknown identifiers/context dependence → miniCTX-style context build; correct-but-poor proof → ImProver.  
**Trade-offs**: routing adds discipline and prevents wasted retries; classification can be wrong, so re-evaluate after each distinctive failure signal.
