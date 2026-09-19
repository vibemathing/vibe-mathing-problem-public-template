# Evaluation Cases

These cases test discoverability, routing, negative triggers, failure recovery, and the source-specific trust boundary. `scripts/validate_skill.py` performs structural checks over this file and the skill tree; semantic expectations are documented here for fresh-agent review.

## Expected positive routes

1. `zero_add` in Addition World → Chapter 2; induction aligned with `add_succ`.
2. `a ≤ b` exists goal → Chapter 7; existential gap witness with `use`.
3. multiplication cancellation → Chapter 8; verify nonzero guard first.
4. NNG `rw`/`rfl` behavior → tactic-semantics reference.
5. `xyzzy`/FLT → Chapter 4; disclose axiom-backed escape hatch.

## Expected negative routes

General programming, unrelated mathematics, weather, and arbitrary Lean/Mathlib topics should not trigger this skill solely because they mention proof or code. A standard Lean theorem may use this skill only when the user explicitly asks to transfer NNG4/MyNat methods or the theorem has the same Peano/curriculum context.

## Fresh-agent representative simulations

### Simulation A — rewrite failure
Goal has multiple products and `rw [mul_comm]` changes the wrong one. A fresh agent should consult proof routing/tactic semantics, then target explicit theorem arguments or `nth_rewrite`, without randomly repeating commutativity.

### Simulation B — induction failure
`mul_left_cancel` proof reaches a step where the IH is fixed at one `c`. The agent should diagnose IH specialization and restart with `generalizing c` rather than adding unrelated rewrites.

### Simulation C — invalid cancellation
User has `a*b=a*c` but no `a≠0`. The agent should refuse unconditional cancellation, explain the zero countercase, and either derive nonzero from other hypotheses or return that the assumptions are insufficient.

### Simulation D — order transitivity
Given `a≤b` and `b≤c`, the agent should unpack both existential gaps and use their sum as the new witness.

### Simulation E — final boss
The agent should never claim earlier NNG lemmas establish FLT. It should identify the source's `xyzzy` mechanism when the question is about game completion.
