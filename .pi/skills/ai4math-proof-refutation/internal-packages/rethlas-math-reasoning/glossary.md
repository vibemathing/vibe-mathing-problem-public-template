# Glossary

**Applicability check** — Explicit comparison of an external result's definitions, hypotheses, ambient objects, and terminology with the current proof setting (Ch 5, Ch 9).

**Blueprint** — Complete candidate proof in `results/<problem_id>/blueprint.md`; it remains provisional until verification passes (Ch 8).

**Branch state** — Persisted status of an active, dead, or recursive proof route (Ch 2, Ch 7).

**Critical error** — Verification finding such as invalid logic, theorem misuse, contradiction, or incorrect external-result application (Ch 9).

**Counterexample** — Example satisfying a claim's assumptions while falsifying its conclusion (Ch 4).

**Decomposition plan** — Material proof architecture with an ordered set of subgoals, motivation, evidence used, and status (Ch 6).

**Failed path** — Persisted proof route with a concrete reason it failed; reused to constrain future planning (Ch 2, Ch 4, Ch 7).

**Fragile conclusion** — Immediate consequence judged risky enough to require counterexample pressure (Ch 3, Ch 4).

**Gap** — Missing or vague derivation, unsupported existence/property claim, suspicious assumption use, or unresolved definition/formula issue (Ch 9).

**Immediate conclusion** — Direct consequence obtained from definitions, calculations, known facts, or logical equivalence before deeper search (Ch 3).

**Key failures summary** — Cross-plan synthesis of repeated obstructions and implications for the next planning round (Ch 7).

**Memory channel** — Append-only JSONL stream for one reasoning artifact type, such as counterexamples, subgoals, or proof steps (Ch 2).

**Migration failure** — Exact reason a known proof idea or construction fails to transfer to the current subgoal (Ch 6).

**Partial-result diagnosis** — Analysis of extra hypotheses, their role in a source proof, and the obstruction revealed when they are absent (Ch 5).

**Problem ID** — Sanitized data-relative problem path without `.md`, preserved across memory, results, logs, and recursive agents (Ch 1, Ch 2).

**Proof migration** — Explicit adaptation of a searched proof technique, construction, or reduction to a current subgoal (Ch 5, Ch 6).

**Recursive proving round** — Parallel, plan-specific proof work launched only after direct screening has failed to solve the current plan set (Ch 7).

**Reference check** — Independent verification that a cited external result exists, matches its stated form, uses compatible definitions, and supports the downstream deduction (Ch 9).

**Rethlas-verified** — A full blueprint that has passed the strict verification service with no critical errors and no gaps (Ch 9).

**Statement check** — Sequential audit of a proof item and its small deductions in textual order (Ch 9).

**Toy example** — Small, concrete case satisfying both assumptions and conclusion, used to expose hypothesis roles and proof mechanisms (Ch 3).

**Verified blueprint** — `blueprint_verified.md`, created only after the strict verification gate passes (Ch 8, Ch 9).
