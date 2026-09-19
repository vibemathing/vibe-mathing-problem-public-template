# CONCEPT_GRAPH

## Core nodes

- **Four-axis taxonomy** → classifies target work into informal text-only, multimodal/geometry, formal proving, and mathematical discovery.
- **CGV triad** → every system can be inspected through comprehension, generation, and verification.
- **Supervision ladder** → stronger external feedback moves from answer checks and hand-built schemas toward process verifiers, symbolic/domain checkers, proof kernels, and expert-audited verified discovery.
- **Reasoning-model era** → combines prompting/tool use with RL, test-time scaling, process supervision, and agentic search.
- **Benchmark saturation** → high scores on legacy tests shift evaluation toward frontier, live, process-sensitive, multilingual, robustness, and formal benchmarks.
- **Formal proof** → converts mathematical correctness into kernel-checkable proof artifacts.
- **Verified discovery** → treats candidate generation, domain evaluation, formal verification, and expert significance review as separate stages.

## Key edges

1. `four-axis taxonomy -> task routing -> verifier choice`
2. `comprehension -> generation -> verification` with feedback from verification back into generation/training.
3. `process reward models -> reasoning training` by moving supervision from final outcomes toward intermediate steps.
4. `tool-integrated reasoning -> executable checks` when arithmetic, code, or symbolic execution can externalize brittle steps.
5. `multimodal parsing -> formalized geometry -> symbolic/neural solver -> verification`.
6. `autoformalization -> library retrieval -> proof search/generation -> kernel`.
7. `compiler feedback -> localized repair -> recompile`.
8. `program search / agentic research -> candidate construction -> domain evaluator -> formal proof where feasible -> expert audit`.
9. `benchmark saturation + contamination -> migrate evaluation` toward harder/live/frontier/robustness settings.
10. `multi-agent diversity -> potential quality gain`, constrained by `correlated errors / false consensus / non-termination`.

## Global synthesis

The most reusable design principle is to decide the **artifact** and its **verifier** together. A numeric answer, a geometric construction, a Lean proof term, and an open-problem construction demand different evidence standards even when the same language model participates in generation.
