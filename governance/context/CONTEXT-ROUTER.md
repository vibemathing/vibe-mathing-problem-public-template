# Context router

Use the smallest context that proves the current action.

1. Read `AGENTS.md` and `governance/INDEX.md`.
2. For maintenance, read `WEB_BOOTSTRAP.md`, the relevant control-plane schema,
   and the validator or builder being changed.
3. For candidate research, require a fresh active `ProblemContract`, Attempt,
   Route, ObligationGraph, and target Obligation. Read `WEB_CONTEXT_BUNDLE.md`
   only as bounded navigation data, then verify the referenced ledgers directly.
4. For evidence or Result work, read the candidate, verifier registry, receipt
   schema, EvidenceLink schema, and the independent replay output.
5. For release work, read `RELEASE-CHECKLIST.md`, the rights matrix, snapshot,
   dependency manifests, and current live repository receipts.

The following are not authority: old conversations, generated summaries,
model confidence, CI alone, PR text, finite experiments, or a completion event.
If an identity is ambiguous, stale, inactive, or missing, return a fail-closed
maintenance result instead of selecting by guess.
