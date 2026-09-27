# Evals and Fresh-Agent Simulation

These tests evaluate the generated skill as an operational capability, not the LeanSearch application itself.

## Trigger tests — should use this skill

1. “I cloned this LeanSearch and get `invalid header` while indexing Mathlib. What do I check?”
   - Expected route: ch02/ch03/ch08; first check Lean/jixia toolchain match.
2. “My `python -m database vector-db` works partly, but search crashes parsing Chroma IDs.”
   - Expected route: ch05/ch08; identify writer/reader ID mismatch.
3. “How do I collect feedback through the FastAPI server?”
   - Expected route: ch07; require single-query search session cookie.
4. “I want to index only algebra-related modules before doing all of Mathlib.”
   - Expected route: ch03; use prefix helper and narrow prefix strategy.
5. “Declarations exist but `record` has far fewer rows.”
   - Expected route: ch01/ch04; check informal rows and level coverage.

## Negative trigger tests — should not use this skill as primary authority

1. “Prove the rank-nullity theorem in Lean 4.” — theorem proving task, not LeanSearch operation.
2. “How does LeanSearch v2 reasoning mode work?” — different repository/version.
3. “Recommend a vector database for my ecommerce search.” — generic vector-search selection.
4. “Explain FastAPI dependency injection.” — generic framework question unless specifically tied to this source.

## Method-selection tests

### Case A — setup failure
Prompt: “Fresh DB, `database jixia` says table `module` does not exist.”
Expected: schema creation, verify connection string; do not tune jixia or LLM.

### Case B — semantic quality failure
Prompt: “Search returns valid records but irrelevant math concepts.”
Expected: inspect corpus coverage, informal text, embedding model, raw vs augmented queries; do not start with SQL schema rebuild.

### Case C — hydration failure
Prompt: “Chroma returns IDs, PostgreSQL lookup fails.”
Expected: vector ID contract check before embedding quality changes.

## Failure-recovery simulation

Prompt: “I set `DRY_RUN=true`, informalization succeeded, then vector search has nothing.”
Expected reasoning path:
1. recognize dry-run behavior in translation/vector builder;
2. explain that vector builder returns before embedding/add;
3. recommend a tiny real embedding build after config validation;
4. keep dry-run DB rows separate from quality evaluation.

## Fresh-agent simulation

A fresh agent receives only this skill and asks:

> “Take a new Lean project, index a small prefix, validate the pipeline, then expose search over HTTP.”

Passing behavior:

1. load ch02 for prerequisites and schema;
2. load ch03 for prefix/indexing;
3. load ch04 for small informalization and coverage checks;
4. load ch05 and fix/validate vector ID contract before building Chroma;
5. load ch06 for known-query validation;
6. load ch07 for API and feedback session behavior;
7. use ch08 if any stage fails;
8. avoid claiming the source supports incremental Chroma updates or v2 features.

## Coverage audit

| Source capability | Skill location |
|---|---|
| setup/config | SKILL + ch02 + cheatsheet |
| schema/data model | ch01/ch03 |
| prefix selection | ch03 |
| jixia extraction/dependencies | ch03 |
| informal translation/prompts | ch04 |
| embedding/vector DB | ch05 |
| search/fetch | ch06 |
| query augmentation | ch06 |
| API/rate limits/feedback | ch07 |
| source mismatches/recovery | ch08 + implementation caveats |
| build/dev config | ch02 + source ledger |

## Hallucination guard

Any recommendation labeled as a repair must remain distinguishable from source behavior. Claims about LeanSearch v2, current hosted service, benchmark accuracy, or upstream fixes are outside this skill unless separately verified.
