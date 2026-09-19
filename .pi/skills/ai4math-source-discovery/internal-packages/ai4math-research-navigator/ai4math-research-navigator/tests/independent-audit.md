# Second-pass independent audit

Reviewer stance: assume this package is encountered cold and try to make it fail.

## Attacks and findings

1. **Summary-only risk** — Pass. The main file routes behavior; detailed capability, decision, benchmark, recovery, and catalog files are executable references rather than chapter summaries.
2. **Source overclaim risk** — Initial risk found because the uploaded archive cites a 238-paper survey corpus but does not bundle those papers. Patched by explicit scope statements in `SKILL.md` and `source-record.md`; literature workflow forbids paper-internal claims from titles alone.
3. **Missing chapter/section coverage** — Pass. Every top-level README section is mapped in `book-map.md`; all three figures are represented in `visual-findings.md`.
4. **Missing method prerequisites** — Pass after requiring target artifact, modality, verifier, compute/search assumptions, and protocol fields before method comparison.
5. **Missing exceptions / failure paths** — Pass. `failure-modes.md` and `workflows/recovery.md` include shortcut learning, contamination, metric mismatch, reward hacking, multimodal non-use, hallucination, localization, correlated agents, non-termination, false rigor, compute bias, and staleness.
6. **Weak routing** — Pass. Four axes plus cross-cutting flags are explicit; mixed tasks route by final artifact/verifier.
7. **Context bloat** — Pass. Catalog and detailed capabilities are outside `SKILL.md`; progressive loading is explicit.
8. **Contradictory rules** — No material contradictions found. Kernel acceptance remains decisive for formal proof; expert audit remains distinct from correctness for discovery.
9. **Over-triggering** — Patched with an explicit exclusion for ordinary math solving and negative trigger evals.
10. **Under-triggering** — Description covers literature, system design, training, benchmark/evaluation, formal proving, multimodal geometry, discovery, and failure diagnosis.
11. **Protocol-comparison error** — Patched with CAP-06, required benchmark-card fields, and warnings around Pass@k/search/TTRL/corrected/live results.
12. **Freshness failure** — Patched with a hard July 2026 snapshot boundary and a dedicated freshness eval.
13. **Independence from original archive** — Pass. The package contains its own distilled routing, method, benchmark, failure, visual, catalog, and provenance materials; the original ZIP is not required at invocation time.

## Result

No unresolved blocker found. Remaining limitation is intrinsic to the source: it is a companion index, so deeper paper-specific claims require retrieving the linked paper. The skill exposes that boundary instead of filling it with guesses.
