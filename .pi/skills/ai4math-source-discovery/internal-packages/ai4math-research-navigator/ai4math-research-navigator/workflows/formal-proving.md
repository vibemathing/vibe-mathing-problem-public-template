# Workflow — Formal theorem proving

1. Determine whether the statement is already formal.
2. If informal, autoformalize and separately validate statement fidelity.
3. Retrieve relevant library lemmas/theorems.
4. Choose tactic-level search or whole-proof generation based on proof length and available model/tooling.
5. Compile in the proof assistant.
6. On failure, capture the exact failing goal/error; retrieve missing lemmas; regenerate the smallest affected region.
7. Recompile until accepted or until resource limits are hit.
8. Report kernel acceptance, search budget, and any unverified informal assumptions.
