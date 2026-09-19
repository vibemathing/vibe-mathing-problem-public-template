# Implementation Caveats and Repair Notes

This file separates **source-derived behavior** from **recommended repairs** for the supplied snapshot.

## C1 — Vector ID mismatch

**Source-derived**

- `database/vector_db.py` creates Chroma IDs from the declaration Lean `name` by joining its components with spaces.
- `retrieve.py` expects an ID containing `module_name:index`, parses at `:`, converts the left side with `parse_name`, and queries `record` by `(module_name, index)`.

**Impact**: Search can retrieve vector neighbors yet fail to hydrate the corresponding SQL row correctly.

**Repair option A — preferred for current reader**

Change vector creation to emit module/index IDs, e.g. semantically `f"{pp_name(module_name)}:{index}"`, then rebuild Chroma.

**Repair option B**

Change retrieval to treat each vector ID as the declaration name and fetch by `record.name`. This requires a stable serialization accepted by Lean-name parsing/JSONB lookup.

**Validation**: inspect five stored IDs and manually resolve each to exactly one `record` row.

## C2 — Embedding configuration mismatch

**Source-derived**

- `.env.example` defines `EMBEDDING_DEVICE` but not `EMBEDDING_URL`.
- `database/embedding.py` ignores `EMBEDDING_DEVICE` and requires `EMBEDDING_URL`.
- README describes a locally downloaded e5-mistral model, while this code calls an HTTP endpoint.

**Repair**: document and set the embedding service URL. Validate its request/response shape and vector dimension before bulk use.

## C3 — Fresh database manual flow

**Source-derived**

`create_schema.py` defines all required SQL objects and `database` CLI has a `schema` command. The Makefile reset invokes it. README's manual indexing sequence does not explicitly call it.

**Repair**: run `python -m database schema` after database creation and before `database jixia`.

## C4 — Topological coverage

**Source-derived**

`topological_sort()` inserts base nodes then repeatedly inserts nodes whose dependencies already have levels. It stops when an insertion affects zero rows.

**Impact**: unresolved dependency cycles can remain absent from `level`, and `generate_informal()` only iterates existing integer levels.

**Repair choices**: detect/report unlevelled symbols; decide whether to collapse strongly connected components, assign a fallback level, or skip with explicit audit. Do not silently pretend full coverage.

## C5 — Embedding HTTP robustness

**Source-derived**

`requests.post(self.url, json=detailed_docs)` has no explicit timeout, `raise_for_status`, retry, or response-schema validation.

**Repair**: add bounded timeout, status check, retry policy for transient failures, and shape/dimension validation if production reliability matters.

## C6 — Chroma rebuild behavior

**Source-derived**

Vector build uses `create_collection(name="leansearch")` and `collection.add(...)`.

**Impact**: reruns against existing collection state are not an explicit incremental-update path.

**Repair**: intentionally clear/repoint the Chroma path for a rebuild, or implement a versioned/upsert workflow.

## C7 — API shared mutable connection

**Source-derived**

One `Retriever` object is stored on the FastAPI app. Middleware assigns `app.retriever.conn` for each request.

**Risk**: concurrent requests can contend over the mutable connection pointer.

**Repair**: pass connection explicitly to retrieval methods, create request-scoped retriever state, or otherwise avoid a shared mutable DB handle.

## C8 — Feedback session behavior

**Source-derived**

Only a single-query `/search` sets the `session` cookie. Multi-query search inserts query rows without returning one feedback session.

**Operational rule**: use a single-query search before `/feedback`, or redesign session semantics for batched queries.

## C9 — Missing rows from `record`

**Source-derived**

`record` is an inner join across declaration, informal, and symbol. `batch_fetch` and hydration paths assume a row exists.

**Operational rule**: when a formal declaration exists but fetch returns no enriched record, check `informal` coverage before treating it as a retrieval bug.

## C10 — Makefile environment differs from runtime `.env`

**Source-derived**

The Makefile expects shell variables `DBNAME`, `INDEXED_REPO_PATH`, `MODULE_NAMES`, and `CHROMA_PATH`; the application runtime uses `.env` variables such as `CONNECTION_STRING`. Its `informal`/`index` targets also call nested reset targets, causing redundant database/Chroma rebuild steps.

**Operational rule**: treat the Makefile as a developer convenience for destructive rebuilds. For controlled production/data-preserving operation, run the Python stage commands explicitly and version the stores.
