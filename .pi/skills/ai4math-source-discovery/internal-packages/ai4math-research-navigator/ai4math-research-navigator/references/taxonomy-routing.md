# Taxonomy and routing

| Axis | Use when the target is | Typical artifact | Preferred verifier | Typical source families |
|---|---|---|---|---|
| Informal text-only | MWPs, competition QA, chain/tool reasoning | numeric/text answer, reasoning trace, code | exact answer parser; process/outcome verifier; executable tool | CoT, self-consistency, least-to-most, ToT/GoT, PAL/PoT/ToRA, PRMs, reasoning models, RL, multi-agent |
| Multimodal & geometry | diagram + text reasoning, geometry construction/proof | grounded relations, construction, proof sketch | symbolic geometry solver, formalized constraints, stepwise grader | GEOS/InterGPS, AlphaGeometry family, TongGeometry, VLM math systems |
| Formal proving | Lean/Coq/Isabelle statements and proofs | tactic script, proof term | proof-assistant kernel | retrieval-augmented proving, whole-proof generation, RL provers, autoformalization, compiler repair |
| Mathematical discovery | open problems, improved bounds, constructions, algorithms | program, construction, theorem, empirical candidate | domain evaluator + formal kernel where possible + expert audit | FunSearch, AlphaEvolve, Erdős workflows, co-mathematician workbenches |

## Cross-cutting concerns

- **Training/supervision**: outcome rewards, process rewards, self-improvement, preference/RL algorithms.
- **Evaluation**: benchmark saturation, protocol mismatch, live/frontier tests, process-sensitive metrics.
- **Robustness**: perturbation, distractors, paraphrase, language transfer, diagram ablation.
- **Coordination**: multi-agent diversity can help search but requires external checking because agents may share errors.

## Ambiguous tasks

When a request spans axes, route by the **highest-stakes artifact**. Example: an LLM writes an informal proof that is then translated into Lean; treat the final correctness stage as formal proving and use the kernel as the decisive verifier, while still using informal-method references for proposal generation.
