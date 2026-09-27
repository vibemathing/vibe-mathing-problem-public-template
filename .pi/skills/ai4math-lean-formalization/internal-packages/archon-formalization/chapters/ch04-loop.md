# Chapter 4: Plan → Prove → Review

## Core Idea
Archon's loop separates strategic reasoning, file-scoped proof execution, deterministic verification, and retrospective review. Each stage has different write authority and should produce evidence for the next.

## Iteration Pipeline
1. **Plan** — read current state, user hints, prior review/doctor signals, references, and DAG; update strategy and current objectives.
2. **Plan validation** — parse objectives, cap/sanitize dispatch, and defer obviously blocked downstream work.
3. **Prover** — dispatch per-file work; provers own tactical choices inside their files.
4. **`sync_leanok`** — compile-check declarations and synchronize earned blueprint proof markers.
5. **Blueprint doctor** — surface structural blueprint debt.
6. **Axiom sweep** — detect `sorryAx` laundering and other non-standard axioms.
7. **Review** — read actual attempt logs, produce proof-journal summary, update status and semantic blueprint notes.
8. **Finalize** — run configured final checks/build and commit state.

## Stage Progression
The intended project stages are autoformalize → prover → polish → COMPLETE. Completion is conditional on real state: a project marked COMPLETE with remaining sorries is reset to prover.

## Plan Agent Rules
Plan chooses mathematical direction, files, modes, and dependencies. It should not write Lean proof code. Objectives should be ready, dependency-aware, and limited enough for useful feedback. A no-prover iteration needs an explicit rationale rather than an empty accidental dispatch.

## Prover Rules
A prover should execute inside assigned files, try viable tactics/lemmas directly, preserve correct theorem types, compile, and leave precise task-result evidence. Tactical decisions belong to the prover; routine proof choices should not be deferred back to planning.

## Review Rules
Review reads attempt logs as primary evidence. It distinguishes proof progress from prose/cosmetics, records blockers and reusable insights, and checks blueprint/Lean correspondence. It can update semantic blueprint markers, but deterministic `\leanok` ownership belongs to sync.

## Source Provenance
Primary: plan/review prompts, `src/archon/commands/loop/command.py`, loop phases, state tests, plan-validation tests.

## Frameworks Introduced
- **Evidence-producing phase loop**: every phase leaves artifacts or deterministic signals consumed by the next phase.
- **Role-separated authority**: plan owns strategy/objectives; prover owns tactical Lean edits in scope; review owns retrospective synthesis; deterministic phases own mechanical truth.
- **Stage machine**: autoformalize → prover → polish → COMPLETE, with guards that can move the project backward when evidence contradicts the label.

## Key Concepts
- **Plan validation**: deterministic normalization/capping/filtering after the planner writes objectives.
- **`sync_leanok`**: mechanical proof-marker synchronization.
- **Axiom sweep**: detects hidden dependencies on `sorryAx` and other non-standard axioms.
- **Finalize**: configured integration checks and history capture after review.
- **Intentional no-prover iteration**: explicit planner state used when proving should be skipped for a reason.

## Mental Models
- Treat the loop like **CI with a mathematician-planner ahead of it**: agents propose/execute, but mechanical gates decide what actually compiled.
- Treat the review phase as **learning from executed traces**, not as a second planner writing speculative proof ideas.

## Anti-patterns
- **Planner writes Lean**: mixes strategic and tactical context and makes ownership ambiguous.
- **Prover asks planner to choose routine tactics**: wastes the focused execution session.
- **Review reports only summaries**: ignoring raw attempt logs loses the strongest evidence about what failed.
- **COMPLETE as a string**: the label cannot override remaining sorries or failed gates.

## Worked Example
Iteration 12 plans `A.lean` and `B.lean`. The prior build says `B.lean` imports broken `A.lean`, so validation keeps `A` and may defer `B` unless both are intentionally co-assigned. The prover closes `A`'s key sorry. `sync_leanok` earns a blueprint marker; blueprint doctor finds a new helper without a blueprint block; axiom sweep is clean; review records the helper debt and the proof technique. Iteration 13's planner repairs coverage and dispatches `B` with a now-compilable dependency.

## Key Takeaways
1. Read each phase by its authority and output evidence.
2. Let deterministic checks override narrative claims.
3. Carry blockers forward through state, not memory alone.
4. A stage transition is earned by repository state.

## Connects To
- **Ch 07**: objective validation and convergence.
- **Ch 13**: logs and phase metadata.
- **Ch 14**: completion gate and failure classifier.
