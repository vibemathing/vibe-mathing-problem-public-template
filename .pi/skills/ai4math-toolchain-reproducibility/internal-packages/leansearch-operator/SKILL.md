---
name: leansearch-operator
description: "Operational knowledge base compiled from the FrenzyMath LeanSearch source repository. Use when installing or configuring this LeanSearch v1-style stack, indexing a Lean 4 project with jixia/PostgreSQL, generating informal theorem descriptions, building or querying the Chroma semantic index, operating its FastAPI service, or diagnosing failures in that pipeline. Do not use for LeanSearch v2, general Lean theorem proving, or unrelated vector-search systems."
---

<!-- argument-hint: [setup, index, informalize, embeddings, search, API, failure symptom, or chapter number] -->

# LeanSearch Operator

**Source**: FrenzyMath `LeanSearch` source snapshot (`17_frenzymath_LeanSearch.zip`)  
**Source type**: technical source collection | **Major sections**: 8 | **Generated**: 2026-09-12

## Use this skill when

Use it to operate or reason about the uploaded LeanSearch implementation: environment setup, module-prefix selection, jixia extraction, PostgreSQL schema/data flow, dependency-aware informalization, embedding/index creation, retrieval, query augmentation, API/feedback behavior, and source-specific troubleshooting.

Do not route here for LeanSearch v2, generic Chroma/OpenAI questions, writing Lean proofs, or claims about newer upstream behavior. This skill is scoped to the supplied source snapshot.

## Fast routing

| User goal / symptom | Load |
|---|---|
| Understand architecture or where data lives | [ch01](chapters/ch01-architecture-data-flow.md) |
| Install/configure from scratch | [ch02](chapters/ch02-environment-installation.md) |
| Choose prefixes, parse Lean, populate PostgreSQL | [ch03](chapters/ch03-jixia-postgres-indexing.md) |
| Generate natural-language theorem/definition descriptions | [ch04](chapters/ch04-informalization-translation.md) |
| Build embeddings / Chroma index | [ch05](chapters/ch05-embedding-vector-db.md) |
| Search, fetch, or augment a query | [ch06](chapters/ch06-search-retrieval-augmentation.md) |
| Run HTTP API / feedback / rate limits | [ch07](chapters/ch07-api-feedback-operations.md) |
| Something fails or README and code disagree | [ch08](chapters/ch08-failure-recovery-caveats.md) and [implementation caveats](references/implementation-caveats.md) |

For a narrow question, read the routed file before answering. For a full deployment, use the workflow below and load chapters 2→7 in order.

## Core operating model

LeanSearch is a staged semantic-search pipeline with two persistent stores:

1. **jixia → PostgreSQL**: parse Lean modules and declarations; store modules, symbols, declarations, dependencies, and dependency levels.
2. **LLM informalization → PostgreSQL**: translate formal items into concise natural-language names/descriptions using docstrings, nearby declarations, and dependencies as context.
3. **embedding service → ChromaDB**: embed visible declarations using a bilingual formal+informal representation.
4. **query → embedding → Chroma → PostgreSQL**: find nearest vector IDs, then hydrate full records from SQL.
5. **optional API layer**: expose search/fetch/query-augmentation/feedback endpoints with rate limits.

Treat the stages as a dependency chain. When a later stage fails, verify the immediately preceding persisted artifact before changing models or prompts.

## Full deployment workflow

### 1. Verify prerequisites

- Python environment installs `requirements.txt`.
- PostgreSQL database exists and is reachable.
- jixia is built against the **same Lean toolchain version** as the target project. A mismatch can produce `invalid header` errors.
- `.env` contains valid paths/credentials.
- An embedding HTTP service compatible with `database/embedding.py` is reachable; this source snapshot expects `EMBEDDING_URL` even though `.env.example` omits it.

### 2. Create schema before loading data

A fresh database needs:

```bash
python -m database schema
```

Then inspect module-prefix selection if needed:

```bash
python -m prefix --project_root <project-root> --prefixes Init,Lean,Mathlib
```

### 3. Parse the Lean project

```bash
python -m database jixia <project-root> <comma-separated-prefixes>
```

Verify PostgreSQL contains modules/symbols/declarations and that `level` is populated before informalization.

### 4. Generate informal descriptions

```bash
python -m database informal
```

Use `--limit-level` and `--limit-num-per-level` for small diagnostic runs. Translation proceeds in dependency levels; each item can use module context, nearby items, and dependencies.

### 5. Build the vector index

```bash
python -m database vector-db
```

Before trusting search, run the **vector-ID compatibility check** in chapter 8. In this snapshot, the writer and reader disagree about the ID format; fix or reconcile this first.

### 6. Search

```bash
python search.py "rank-nullity theorem"
python search.py --json -n 10 "Haar measure"
```

Query strings are embedded with the retrieval instruction, nearest neighbors are read from Chroma, and full records are fetched from PostgreSQL.

### 7. Optional server

Run the FastAPI app, for example with `uvicorn server:app`, then use `/search`, `/fetch`, `/augment`, and `/feedback` as described in chapter 7.

## Decision rules

- **`invalid header` while indexing** → compare jixia and target-project Lean toolchains before debugging SQL.
- **PostgreSQL relation/type missing** → schema was not created, was created in another database, or the connection string points elsewhere.
- **Informalization produces no work** → inspect `level`, existing `informal` rows, and cycle/unleveled symbols.
- **Chroma builds but search cannot hydrate results** → check vector ID format first.
- **Embedding call fails** → verify `EMBEDDING_URL`, HTTP response shape, service model/dimension, then network reachability.
- **Vector-db says collection already exists** → use a clean Chroma path or intentionally rebuild; this code calls `create_collection`, not get-or-create.
- **Feedback request lacks a usable session** → obtain the cookie from a single-query `/search`; multi-query search does not set one.
- **Need a cheap pipeline smoke test** → `DRY_RUN=true` validates much of extraction/informalization without API/embedding cost, but it cannot produce a searchable vector index.

## Global constraints

- Preserve exact Lean/toolchain/module-prefix semantics when giving commands.
- Distinguish source facts from recommended repairs. Source-specific repairs are catalogued in [implementation-caveats.md](references/implementation-caveats.md).
- Do not invent current upstream behavior. The source archive is the authority for this skill.
- Do not expose or request real API keys in logs or examples.
- Large Mathlib indexing can incur substantial LLM and compute cost; use prefix scoping and limited runs before full indexing.

## Self-check

Before finalizing an answer or operation:

1. Which pipeline stage owns the failing artifact: Lean/jixia, PostgreSQL, informalization, embedding/Chroma, retrieval, or API?
2. Are all prerequisites for that stage actually present?
3. Is the user operating this exact source snapshot or a newer/different LeanSearch?
4. Did I account for known snapshot caveats before recommending model/prompt changes?
5. Can I verify the preceding stage with a small query or row count?
6. If proposing a patch, did I label it as a repair rather than source behavior?
7. Does the final path leave the system with consistent PostgreSQL and Chroma state?

## Topic index

- **API / FastAPI / cookies / feedback** → ch07, ch08
- **ChromaDB / embeddings / vector IDs** → ch05, ch08
- **database schema / record view** → ch01, ch03
- **DeepSeek / OpenAI-compatible model** → ch02, ch04
- **dependency levels / topological order** → ch03, ch04, ch08
- **dry run** → ch02, ch04, ch05, ch08
- **informal names / descriptions** → ch04
- **jixia / Lean toolchain mismatch** → ch02, ch03, ch08
- **module prefixes** → ch03
- **query augmentation** → ch06
- **search / retrieval** → ch06

## Supporting files

- [glossary.md](glossary.md) — project-specific terms
- [patterns.md](patterns.md) — reusable implementation/operation patterns
- [cheatsheet.md](cheatsheet.md) — commands and decision tables
- [references/implementation-caveats.md](references/implementation-caveats.md) — source/code mismatches and repair options
- [references/provenance.md](references/provenance.md) — capability-to-source traceability
- [references/source-ledger.md](references/source-ledger.md) — processed source inventory
- [tests/evals.md](tests/evals.md) — trigger, routing, recovery, and fresh-agent evaluations

## Scope & limits

This skill encodes the supplied LeanSearch source snapshot and its operational implications. It does not bundle the original repository, external models, jixia, PostgreSQL, Chroma data, or credentials. It can guide a fresh agent without the source archive, while detailed implementation claims remain traceable through the provenance file.
