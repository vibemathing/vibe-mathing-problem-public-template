# Workflow — DIAGNOSE → PATCH → RETEST

1. Name the failure class from `references/failure-modes.md`.
2. Identify which component failed: representation, generator/search, verifier, metric, data, coordination, or freshness.
3. Change one causal component rather than simply increasing token budget.
4. Retest on the smallest discriminating case.
5. If fixed, rerun representative evaluation.
6. If still failing, switch method family or verifier level.
7. Stop and report insufficient evidence when validation cannot be executed.
