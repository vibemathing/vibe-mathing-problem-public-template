# Workflow — Multimodal geometry

1. Parse problem text and diagram independently.
2. Ground named points, lines, angles, lengths, incidence, and visual relations.
3. Convert grounded relations into a symbolic/formal constraint representation when feasible.
4. Generate construction/proof candidates with neural, symbolic, or hybrid methods.
5. Verify steps with a geometry solver or rule checker.
6. Run diagram ablation/perturbation: remove or alter the diagram to test genuine visual use.
7. If ablation improves performance, diagnose visual grounding as a failure before scaling reasoning.
