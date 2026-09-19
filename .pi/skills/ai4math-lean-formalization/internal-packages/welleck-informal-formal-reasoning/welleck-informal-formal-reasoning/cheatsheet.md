# Decision Cheatsheet

## Route by Bottleneck
| Signal | Choose | Because |
|---|---|---|
| Next tactic unclear; verifier available | Lean-STaR | informal thought can guide a local formal action |
| Whole proof branches wildly; strategy is the issue | Draft-Sketch-Prove | move search to proof structure and smaller gaps |
| Gap looks routine but library is huge | LeanHammer | premise selection reduces symbolic search |
| Target uses new/custom repository facts | miniCTX-style context-first workflow | state-only view is incomplete |
| Verified proof exists; quality is poor | ImProver | optimize under a hard correctness constraint |

## Composition Default
**Research repository target** → collect context/dependency graph → draft high-level route → formal sketch → hammer routine gaps → Lean-STaR for stubborn local steps → verify complete theorem → optimize only afterward.

## Failure Smells
- Same rejected tactic shape ≥ several attempts → branch/thought is stale; change method or premise set.
- Sketch has one hole nearly as hard as original theorem → decomposition failed; refine the sketch.
- Hammer fails while an obvious lemma exists locally → premise selector/context pool is incomplete.
- Model proposes unavailable/later declaration → context legality bug; fix file/dependency boundary.
- Bigger context makes output worse → retrieve/rank instead of dumping.
- More samples stop finding new proofs → strategy diversity has plateaued; change abstraction/model.
- Proof rewrite is shorter but no longer readable → metric is mis-specified.

## Hard Gates
1. A formal action counts only after verifier acceptance.
2. A DSP result counts only after all gaps close and the whole proof checks.
3. An ATP result counts only after reconstruction/checking in the target prover.
4. A proof optimization candidate competes only if it remains valid.
5. If verification cannot run, report **candidate/unverified**, never certified.

## Inputs to Capture Before Search
- theorem statement / current proof state
- proof assistant + version/toolchain
- local hypotheses and imports
- relevant in-file/cross-file declarations
- available automation/retrieval tools
- search/compute budget
- output objective: prove, formalize, repair, explain, or optimize

## Stop / Switch Rules
- **Switch to DSP** when local action search is the dominant combinatorial problem.
- **Switch to LeanHammer** when the proof idea is known and the missing piece is factual/library support.
- **Switch to context-first** when failures mention unknown identifiers/types or project-local facts.
- **Switch to optimization** only after a stable verified proof exists.
- **Stop with insufficient evidence** when the statement, dependencies, or verifier environment cannot be validated.
