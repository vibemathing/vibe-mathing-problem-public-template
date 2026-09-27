# Workflow — AI4Math system design

1. Define target task, input modality, output artifact, and correctness standard.
2. Route axis using `taxonomy-routing.md`.
3. Build a CGV table:
   - Comprehension: representation/grounding/decomposition.
   - Generation: model/search/tool/agent strategy.
   - Verification: external checker and feedback loop.
4. Select baseline first; add complexity only for identified bottlenecks.
5. Choose training/supervision compatible with the verifier.
6. Design evaluation before optimization; include one robustness or process-sensitive check.
7. Define fallback when the verifier rejects or the benchmark saturates.
8. Run SELF_CHECK from `SKILL.md`.
