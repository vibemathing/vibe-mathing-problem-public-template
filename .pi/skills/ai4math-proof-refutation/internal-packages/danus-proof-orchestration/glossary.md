# Glossary

**approach portfolio** — Main agent's durable set of credible routes, each with mechanism, frontier, obstacle, evidence, resource allocation, and revisit condition. (Ch 3)

**cold-start verifier** — Fresh verifier process/session for one candidate, used to reduce producer-state contamination. (Ch 1, 5)

**control beat** — Roughly 30-minute main-agent whole-project review while an active problem remains unsolved. (Ch 3)

**dead end** — Shared global-memory finding describing a concrete route failure and evidence, so other workers avoid repeating it. (Ch 2, 4)

**elaboration** — Structured main-agent synthesis of mathematical state, interfaces, dangerous heuristics, and missing bridge lemmas. (Ch 3)

**external_refs** — Structured bibliography metadata attached to a fact; mutable without changing `fact_id`. (Ch 2, 5, 9)

**fact graph** — Content-addressed DAG of verifier-accepted facts; Danus's sole correctness source. (Ch 1, 2)

**fact_id** — 16-hex content-derived identifier over problem, predecessors, glossary, statement, and proof. (Ch 2)

**fact_submit** — Worker-only gateway operation that verifies a candidate and writes it iff accepted. (Ch 5)

**finalize** — Operator-facing action that records selected verified target fact(s) for a paper; it does not stop workers. (Ch 6, 9)

**global memory** — Project-shared typed findings and strategy; useful for awareness, never a correctness source. (Ch 2)

**glossary_introduces** — Symbol-definition map stored with a fact and merged into project terminology. (Ch 2)

**headline facts** — Operator-selected target results that define the paper's fact-graph closure. (Ch 9)

**ignorable finding** — Whole-paper verifier finding that a mathematics undergraduate could fill unaided; does not block delivery. (Ch 9)

**local memory** — Private per-worker rough notes/events used for continuity. (Ch 2)

**macro audit** — Roughly four-hour main-agent route comparison and resource-allocation review. (Ch 3)

**master_guidance** — Main-agent shared strategic direction consumed by workers; authoritative steering, still unverified mathematics. (Ch 2, 3)

**must-fix finding** — Whole-paper mathematical gap that fails the undergraduate-fillability bar and blocks delivery. (Ch 9)

**paper_id** — Identifier for an isolated paper workspace within one project/fact graph. (Ch 9)

**paper_subgraph** — Deterministic statements-only skeleton of the selected target closure used for curation. (Ch 9)

**predecessor** — Verified fact dependency named by a fact node; dependencies form a DAG. (Ch 2)

**proof migration** — Adapting the mechanism of a related theorem while analyzing where extra hypotheses enter. (Ch 4, 7)

**support layer** — Curated set of load-bearing facts a paper-writing call should present in detail. (Ch 9)

**target closure** — Selected headline fact(s) plus all transitive predecessor facts. (Ch 9)

**verification trace** — Global-memory record of an acceptance/rejection and repair information emitted around `fact_submit`. (Ch 2, 5)

**worker round** — One autonomous Codex continuation session; can be long-running and resumes through persisted stores. (Ch 6)
