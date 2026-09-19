# 09 — Write-Paper Pipeline

## Goal

Turn a selected verified result and its fact-graph support into a publishable LaTeX manuscript through explicit target selection, curation, citation verification, compilation, leakage control, and whole-paper mathematical re-verification.

## Stage 0 — Paper intent and target

A paper needs an operator-owned `PROJECT_BRIEF`: title/working title, audience/venue, human authors/affiliations, scope, headline facts, style overrides, deadline/status. Never invent authorship or operator preferences.

The mathematical target comes from, in precedence order, an explicit call, the brief's `headline_fact_ids`, or a finalized `TARGET.md`. If no target is recorded, the writer returns `needs_target`. Terminal facts may be suggested; they are never auto-selected. The operator owns target selection; the writer must not guess a target from recent activity or memory.

A non-default `paper_id` gets its own isolated paper workspace while sharing the project fact graph.

## Stage 1 — Reference ledger

Seed `REFERENCE_LEDGER.md` from `external_refs` attached to the target's transitive predecessor closure. Use the same closure the writer will use. This prevents unrelated side-lemma citations from becoming phantom bibliography entries. Seeded references start unverified.

## Stage 1a — Optional style anchors

Generic `STYLE_GUIDE.md` and `PAPER_STRUCTURE.md` are sufficient. If the operator has supplied their own papers under style anchors and the anchors are stale, the style distiller proposes guide changes. The operator accepts/rejects; proposed style never auto-mutates future papers.

## Stage 2 — Curate, then write

Call `paper_subgraph` to get a compact statements-only skeleton of the target closure. The main agent selects the support layer: headline theorem(s) plus the load-bearing results that the manuscript should present in detail.

Binding curation rule: if the closure has 10 or more facts, do not pass the entire closure and do not omit `fact_ids`. Select a smaller support layer. Apply the same rule recursively to deep sub-results.

Then call `paper_write` with:

- target/headline;
- selected `fact_ids`;
- editorial instructions describing sectioning, emphasis, and granularity;
- optional `paper_id`.

The authoring system preserves mathematical content, avoids fact-id leakage, and keeps a provenance sidecar mapping rendered labels to source facts.

## Large-paper fallback

If even a curated writer prompt exceeds the context threshold, a chunked pipeline plans sections from statements, writes each section from only its facts plus statement-level cross-context, then stitches deterministically. Coverage is checked so every closure fact is assigned exactly once; plan imperfections can be normalized deterministically. Partial output is not shipped after a failed section.

For very large whole-paper mathematics verification, do not silently lower the bar. Decompose the manuscript by major results/papers or use an explicit operator override where supported.

## Stage 3 — Compile gate

Compile with a real LaTeX engine when available. A manuscript is not compile-clean if it has hard LaTeX errors or undefined citations/references. The reviser uses targeted patch edits and an in-tool compile-retry loop. Persistent failure is quarantined rather than overwriting the last good `main.tex`.

## Stage 4 — Offline reference audit

The auditor has no network. It identifies each citation/ledger inconsistency and leaves unresolved rows as `unverified`. It must not promote plausible metadata from model memory.

## Stage 4.5 — Online reference verification

`reference_verify` checks only flagged entries against authoritative sources. Outcomes include verified, corrected, rejected, unverifiable, or retarget-internal. Every verified/corrected entry carries the source used. Unreachable or ambiguous sources remain blockers.

## Stage 5 — Targeted revision

Apply verified citation fixes, compile errors, and operator notes with exact patch edits. Guardrails reject zero-edit patches, drastic manuscript shrinkage, identifier leaks, and repeated compile failure.

## Stage 5.5 — Whole-paper mathematics gate

A dedicated verifier reads the complete manuscript plus verified reference ledger and checks the paper's own argument sequentially. Findings are classified:

- `ignorable`: a mathematics undergraduate could fill/follow the omitted step unaided;
- `must-fix`: every gap that fails that bar.

Precise citations to confirmed literature are accepted as givens. Unproved, uncited, load-bearing steps become findings. Any `must-fix` blocks delivery.

When a gap appears, the main agent chooses verified facts that close it; `paper_revise` receives verifier feedback, main-agent guidance, and those fact bodies together. For standard published machinery, prefer a precise confirmed citation over re-proving it.

## Stage 6 — Delivery and outward publication

Deliver only after compile/citation/leak/math gates are satisfied, or after a documented operator override where the system supports one. Any external repository push/publication is a separate operator-gated action.

## Failure matrix

| Symptom | Fix |
|---|---|
| `needs_target` | operator selects/finalizes verified target |
| flat 100-fact draft | re-curate support layer; split deep result into its own written piece |
| citation blocker | online verify; correct/reject; keep flag until resolved |
| compile failure | localized patch and recompile; quarantine if exhausted |
| internal id leak | reject/quarantine and regenerate/revise |
| must-fix math gap | insert verified derivation or confirmed precise citation; rerun whole-paper verifier |
| oversized whole-paper verifier input | split by major results; do not claim pass |

## Editorial principle

Write well by shaping the dependency story. Present pivotal mathematics in adequate detail; cite standard machinery precisely; compress routine steps only when the verification bar still considers them independently fillable. Length is diagnostic evidence of shaping quality, not the target itself.
