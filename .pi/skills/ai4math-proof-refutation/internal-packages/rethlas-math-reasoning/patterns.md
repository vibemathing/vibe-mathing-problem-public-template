# Operational Patterns

## Fresh-Proof Bootstrap
**When to use**: a new theorem, branch, or subgoal.
**How**: initialize persistent state → normalize the statement → derive direct consequences → mark fragile claims → gather only the external background that can change the next move → build toy examples when hypothesis roles are unclear.
**Trade-offs**: cheap and information-dense; it does not by itself establish hard claims.

## Fragile-Claim Falsification
**When to use**: a claim feels unproved, a direct subgoal stalls, or a route depends on a strong lemma.
**How**: preserve all assumptions → try to violate the conclusion → classify refuted / not refuted / inconclusive → persist the example → kill dependent branches only after a real refutation.
**Trade-offs**: quickly removes false routes; failure to find a counterexample supplies only weak support.

## Narrow Memory Recall
**When to use**: prior reasoning may already contain a useful obstruction, example, or branch decision.
**How**: phrase a concrete query → choose the smallest relevant channels → retrieve top local hits → state how each useful hit changes the present proof state.
**Trade-offs**: reduces repeated work; broad queries can return noisy records.

## Context-Checked Literature Reuse
**When to use**: an external theorem, construction, or proof resembles the current target.
**How**: search with a complete statement → inspect source context → read the proof → expand definitions → map hypotheses → preserve identifiers → extract transferable methods.
**Trade-offs**: slower than citing a search result; greatly reduces false applicability.

## Partial-Result Obstruction Mining
**When to use**: the closest literature result assumes more than the target.
**How**: locate each extra hypothesis in the source proof → identify the step it enables → identify the failure without it → store that failure as information for new plans.
**Trade-offs**: may not solve the problem immediately; often reveals the true bottleneck.

## Diverse Plan Generation
**When to use**: examples, failures, and search results provide enough constraints for structured proof search.
**How**: produce several mechanism-level alternatives → list ordered subgoals → explain plausibility → name which prior failures each route avoids → persist plan status.
**Trade-offs**: adds breadth; plans that differ only in wording waste later screening.

## Whole-Plan Direct Screening
**When to use**: immediately after a decomposition plan exists.
**How**: attempt every subgoal → adapt relevant proof ideas → falsify blocked subgoals → record solved/partial/stuck state and migration failures → diagnose the plan only after a real end-to-end attempt.
**Trade-offs**: may spend time on a plan that ultimately fails; provides the evidence needed for efficient escalation.

## Recursive Plan Escalation
**When to use**: all current plans were directly screened and none solved the problem.
**How**: one sub-agent per plan → provide full theorem + own and shared stuck points → keep one `problem_id` → allow evidence-driven local revisions → collect all reports.
**Trade-offs**: parallelism raises cost; continuity and shared failure context prevent duplicated exploration.

## Failure-Synthesis Replanning
**When to use**: recursive work or a family of direct plans fails.
**How**: compare recurring obstructions, counterexamples, search gaps, and broken decompositions → write a key-failures summary → generate a new plan family that explicitly avoids or attacks those obstructions.
**Trade-offs**: requires disciplined failure records; without them re-planning can loop.

## Strict Verification & Repair
**When to use**: a complete proof of the original target is assembled.
**How**: verify sequential deductions → check external references separately → synthesize all findings → accept only with zero errors/gaps → repair critical errors first → close remaining gaps → re-run on the full proof.
**Trade-offs**: conservative and potentially iterative; supplies a clear acceptance boundary.
