# Chapter 8: Failure Recovery and Source Caveats

## Core Idea

Diagnose LeanSearch stage-by-stage. Several problems in this source snapshot are cross-file contract mismatches; rebuilding or tuning a model before checking those contracts wastes time.

## Triage tree

### A. Indexing fails before data appears

1. Does the database schema exist?
2. Does `CONNECTION_STRING` point to that database?
3. Do jixia and target project use the same Lean toolchain?
4. Do the chosen prefixes match real modules?
5. Can a tiny prefix be indexed?

### B. Declarations exist but informalization is incomplete

1. Compare `symbol`, `level`, and `informal` counts.
2. Find symbols without a level; inspect cycles.
3. Inspect raw LLM responses for output-marker parse failures.
4. Verify OpenAI-compatible endpoint/auth and model name.
5. Run limited levels/items before a full retry.

### C. Informal rows exist but vector build fails

1. Confirm `EMBEDDING_URL` is set and reachable.
2. Confirm response is JSON embeddings in expected batch order.
3. Confirm vector dimension/service model compatibility.
4. Use a clean Chroma collection/path if rebuilding.
5. Fix vector ID contract before trusting the index.

### D. Chroma returns hits but search fails

Inspect IDs immediately. The current writer stores declaration-name-derived IDs; the reader expects `module:index`. Rebuild after reconciling the contract.

### E. Search runs but quality is poor

1. Check whether expected declaration is present/visible/informalized.
2. Inspect its embedded bilingual text.
3. Compare raw and augmented queries.
4. Check embedding model/service consistency between index and query.
5. Only then tune top-k or prompts.

### F. API-specific failure

1. Reproduce through CLI search to isolate API from retrieval.
2. Check rate limits.
3. For feedback, obtain single-query session cookie.
4. For concurrency-only failures, inspect shared `Retriever.conn` mutation.

## Known source mismatches

### 1. Vector ID writer vs reader — blocking for reliable search

- Writer: declaration-name-derived string.
- Reader: parses `<module-name>:<index>` and queries SQL by `(module_name, index)`.
- Repair: change one side, rebuild Chroma, then test hydration on known items.

### 2. Missing `EMBEDDING_URL` in sample config — blocking for vector/search stages

The code requires the variable, but `.env.example` does not define it. Add a compatible embedding-service URL and document the service.

### 3. README local-embedding wording vs HTTP implementation

README describes a locally downloaded `e5-mistral-7b-instruct`; this snapshot's `MistralEmbedding` calls an HTTP service. Treat the code as operational truth for the snapshot.

### 4. README manual sequence omits schema creation

The Makefile reset path creates schema, but manual README steps can lead a new user directly to `database jixia`. On a fresh DB, run `python -m database schema` first.

### 5. `EMBEDDING_DEVICE` is unused by the current Python path

Do not diagnose HTTP embedding issues by changing this variable.

### 6. Dependency cycles can remain unlevelled

Topological insertion terminates when no new rows can be assigned. Cyclic unresolved symbols can remain outside `level` and never enter informalization's level loop.

### 7. Retry coverage is narrow

Translation/augmentation explicitly retry JSON decode and format parsing cases, but general HTTP/auth/timeouts are not comprehensively handled. Add service-level retries/timeouts only as an implementation repair, not as claimed source behavior.

### 8. Chroma collection creation is not incremental

`create_collection` assumes a clean target. Rebuilding embeddings, changing IDs, or rerunning against existing state may require deleting/repointing the collection.

## Repair discipline

When patching:

1. Save the exact source snapshot/commit identity if available.
2. Patch one contract at a time.
3. Rebuild only the downstream artifacts affected by that contract.
4. Keep PostgreSQL and Chroma versions paired.
5. Validate with a known declaration and one expected query before scaling.
6. Document each repair separately from source-derived behavior.

## When to return “insufficient to determine”

Do so when the user is running a different upstream version, the embedding service contract is unknown, or they provide an error from a stage that cannot be located from available logs/state. Ask for the smallest diagnostic artifact: exact command, exception, relevant env-variable names without secrets, row counts, or a sample Chroma ID.

## Connects To

- [implementation-caveats.md](../references/implementation-caveats.md) gives source locations and patch choices.
- [cheatsheet.md](../cheatsheet.md) provides symptom-to-action lookup.
