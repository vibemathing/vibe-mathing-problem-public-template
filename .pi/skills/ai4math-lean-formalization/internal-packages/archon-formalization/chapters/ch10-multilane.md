# Chapter 10: Multi-Lane Proving

## Core Idea
Multilane proving races multiple provider configurations on the same assigned Lean files in isolated inner-git worktrees, then combines results at declaration granularity.

## When to Use
Use when provider diversity is valuable enough to justify extra cost and concurrency. Single-lane remains the simpler baseline.

## Setup
1. Place provider credentials in `.archon/.env`.
2. Enable `multilane` and list lanes in `.archon/config.json`.
3. Run `archon loop`; no separate lane command is required.

Each lane gets an isolated worktree under `.archon/lanes/<lane>`. Assignment results and reports are stored under `.archon/multilane/` and surfaced in dashboard logs.

## Clean Winner Rule
A lane can be considered a clean early finisher only when the assigned file builds, has no remaining target sorries/new axioms, and only permitted file changes occurred. Other lanes for that file receive the configured grace window (default 10 minutes) before cancellation. The merge agent then picks the best proof per declaration from completed lanes.

## Failure Recovery
If a lane lacks its required key, disable that lane and continue others. Treat auth/rate-limit/provider failures as lane-specific unless evidence shows shared infrastructure failure. Setting `multilane.enabled` false returns to normal single-lane behavior; stale worktrees remain until explicitly removed.

## Decision Rule
Multilane helps when proof approaches are uncertain and provider/model diversity is likely to produce different successes. It is wasteful when the blocker is a deterministic blueprint error, broken dependency, or wrong theorem statement—fix those first.

## Source Provenance
Primary: `docs/MULTILANE.md`, `src/archon/multilane/**`, multilane tests.

## Frameworks Introduced
- **Isolated proof race**: run lane×file assignments in separate worktrees so candidates cannot overwrite one another.
- **Clean-finisher grace policy**: once a candidate proves the file cleanly, give slower lanes a bounded window to beat it, then stop wasting compute.
- **Declaration-level merge**: choose the strongest candidate proof per declaration rather than accepting an entire lane wholesale.

## Key Concepts
- **Lane**: provider/harness/model configuration plus isolated worktree.
- **Grace window**: time allowed for other lanes after a clean finish; default documented value is 10 minutes.
- **Assigned-file-only**: candidate safety condition that rejects unrelated edits.
- **Promotion candidate**: lane result classified for safe/review-needed/unsafe promotion.

## Mental Models
- Treat multilane as **speculative execution**: pay extra compute to reduce uncertainty in hard proof search.
- Merge is **proof selection under fixed signatures**, followed by a build gate.

## Anti-patterns
- **Race a deterministic failure**: multiple models will not fix a broken `\\uses`, missing import, or false statement.
- **Share one working tree among lanes**: destroys candidate isolation.
- **Accept fastest result without quality checks**: speed does not imply no sorries/axioms/unrelated edits.

## Worked Example
Two lanes, Anthropic and Moonshot, receive `Algebra/WLocal.lean`. Moonshot finishes first with a clean build and no sorries; Anthropic is still running. Start the configured grace window. If Anthropic later produces a shorter/cleaner proof for one declaration while Moonshot remains better for another, the merge stage can select per declaration, then run the final build. If Moonshot lacks its key, disable it and continue Anthropic instead of failing the round.

## Key Takeaways
1. Only race after structural prerequisites are sound.
2. Isolate candidate worktrees.
3. Require clean verification before early-winner logic.
4. Verify the merged result, not only each lane in isolation.

## Connects To
- **Ch 06**: proof/build quality gates.
- **Ch 08**: provider/harness configuration.
- **Ch 09**: worktree/history safety.
