# Glossary

**Aesop** — Lean proof-search/tactic framework that can combine structured search with automation; referenced in hammer-style workflows. (Ch 4)

**ATP (Automated Theorem Prover)** — external symbolic prover used to solve translated formal subproblems. (Ch 4)

**Backtracking** — returning to an earlier accepted proof state after a later action fails. (Ch 2)

**Chain-of-States** — ImProver technique that exposes symbolic Lean state/context during proof rewriting. (Ch 6)

**Context selection** — choosing the subset of repository/file material most useful for the current theorem. (Ch 5)

**Draft** — informal proof candidate that supplies the high-level route for DSP. (Ch 3)

**Draft-Sketch-Prove (DSP)** — draft an informal proof, map it to a formal sketch, then fill formal gaps with automation. (Ch 3)

**Expert iteration** — sample candidate proofs, verify them, add successful trajectories to training data, and retrain. (Ch 2)

**Formal proof** — proof artifact accepted by a proof assistant under explicit rules and context. (Ch 1)

**Formal sketch** — formal proof skeleton that mirrors high-level reasoning while leaving explicit local gaps. (Ch 3)

**Future mathlib** — time-split evaluation idea using later mathlib theorems to test generalization to newer context. (Ch 5)

**Gap** — explicit unproven local obligation inside a formal sketch. (Ch 3)

**Hammer** — tool that combines premise selection, automated reasoning, and proof reconstruction to close formal goals. (Ch 4)

**ImProver** — agent framework for rewriting already-correct Lean proofs to optimize user-defined metrics. (Ch 6)

**Informal reasoning** — human-style mathematical strategy/explanation that is flexible but not mechanically certified. (Ch 1)

**Lean-STaR** — framework that generates informal thoughts before formal proof steps and improves via verifier-grounded expert iteration. (Ch 2)

**LLMLean** — lightweight interface concept connecting Lean with language models, including local models. (Ch 5)

**miniCTX** — benchmark/framework for theorem proving with new, long context from real Lean projects and textbooks. (Ch 5)

**miniF2F** — formalized mathematical-problem benchmark used to evaluate neural theorem provers, including Lean-STaR. (Ch 2)

**Premise** — theorem, lemma, definition, or local fact that may be needed to prove a goal. (Ch 4)

**Premise selection** — ranking and selecting a small relevant subset from a large available fact library. (Ch 4, Ch 5)

**Proof reconstruction** — translating an external prover result back into a proof the original assistant can check. (Ch 4)

**Proof state** — current formal goals plus local hypotheses/context in an interactive prover. (Ch 1, Ch 2)

**Proof optimization** — rewriting a verified proof to improve a metric while preserving correctness. (Ch 6)

**Retriever** — learned or symbolic component that ranks premises/context for a current goal. (Ch 4)

**Tactic** — formal action that transforms a proof state. (Ch 1, Ch 2)

**Verifier feedback** — acceptance, rejection, error, or next formal state returned by the proof assistant. (Ch 1, Ch 2, Ch 6)
