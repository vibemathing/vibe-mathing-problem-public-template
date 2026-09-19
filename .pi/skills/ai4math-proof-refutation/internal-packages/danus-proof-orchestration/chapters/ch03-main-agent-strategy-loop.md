# 03 — Main-Agent Strategy Loop

## Purpose

The main agent maintains a live model of the whole research program. Its success metric is progress of credible routes toward the fixed theorem, not worker activity, fact count, or proof length.

## Persistent control loop

Keep each active unsolved project under persistent goal continuity. Run an initial control beat immediately. While active, perform a global control beat about every 30 minutes of wall-clock time and a macro audit about every four hours. These are decision cycles, not reporting rituals.

A control beat should:

1. Re-read the fixed problem, global memory, verified fact graph, and worker status.
2. Inventory every credible approach, including parked routes.
3. For each route, record mechanism, mathematical frontier, decisive obstacle, evidence for/against, assigned resources, and revisit condition.
4. Synthesize finished speculative subagent work as hypotheses.
5. Continue independent high-level mathematical reasoning.
6. Update the elaboration when the synthesis materially changed.
7. Write new `master_guidance` only when the steering decision materially changed.
8. Inspect each worker's actual assignment/progress; continue, sharpen, redirect, or stop deliberately.
9. Refill useful speculative capacity with non-duplicative investigations.

A macro audit compares routes explicitly and records why to continue, complement, park, or resume each one. Recent context must not erase earlier serious alternatives.

## Elaboration contract

The elaboration is a high-signal synthesis built only from shared stores. It keeps the fixed goal intact and uses seven calibrated statuses:

`CLOSED`, `SUBSTANTIAL`, `PARTIAL`, `DANGEROUS`, `FALSE AS STATED`, `OBSOLETE`, `UNKNOWN`.

`CLOSED` requires a verified fact on the actual construction with no remaining hypothesis match. A conditional theorem package with an unmatched interface is `SUBSTANTIAL` or weaker.

A mature elaboration includes:

- mathematical verdict;
- status dashboard and per-subtask status;
- approach portfolio;
- current best proof skeleton;
- central missing lemma;
- signed-closed components;
- failed/obsolete routes;
- interface contracts with exact missing hypothesis matches;
- dangerous heuristic lines;
- missing bridge lemmas.

The most important diagnostic is the interface contract: what the next step requires, what the current result guarantees, which verified facts apply, what remains unmatched, and what breaks if ignored.

## Literature reconnaissance

Before heavy commitment to a new route, and when a new central obstruction appears, search literature with multiple formulations and technique names. Extract mechanisms and exact hypotheses. Store source-identified notes in global memory as awareness. A search result is never a fact by itself.

## Assignment design

Give workers differentiated mathematical questions, not generic “try harder” prompts. Useful assignments include:

- attack the central bridge lemma directly;
- search for a counterexample to a fragile hypothesis;
- adapt a specific literature technique and identify the first non-transferable step;
- prove an interface condition on the actual construction;
- audit a parked route's revisit condition;
- reconstruct an external theorem's exact assumptions for the current model.

Every subagent assignment should restate the text-only mathematics boundary.

## Failure recovery

### Local progress, global stagnation

If many facts are accumulating while no route advances, re-run the portfolio audit. Find whether the work is proving irrelevant lemmas, failing to close interfaces, or duplicating prior directions.

### Dominant route keeps failing

Preserve its failure evidence and revisit condition, then activate a materially different route. Do not let sunk effort determine strategy.

### No obvious follow-up for a free speculative slot

Perform a route-level review and formulate the best non-duplicative question. Idle only when complete, paused, or genuinely blocked on the operator.

### A proposition may be false

Distinguish method failure from proposition failure. Keep the original goal fixed and seek a verified counterexample rather than silently weakening the target.

## Hard boundaries

- no direct fact submission by the main agent;
- no worker-local memory inspection;
- no mathematical computation or proof-assistant experiments;
- no external publication or destructive revocation without the required operator decision;
- no stopping merely because work is hard or slow.

## Quality test

A good strategy update changes at least one decision: which route is live, which bridge matters, which evidence is missing, which worker does what, or what would cause a route to be revisited. A status recital with no decision value should not be stored as new guidance.
