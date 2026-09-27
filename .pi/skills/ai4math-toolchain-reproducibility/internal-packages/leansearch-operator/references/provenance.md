# Provenance Map

Classification: **SOURCE_DERIVED** = directly supported by supplied files; **STRUCTURAL_SYNTHESIS** = cross-file operationalization; **IMPLEMENTATION_DECISION** = recommended repair/workflow added by this skill.

| Capability / rule | Classification | Source locations |
|---|---|---|
| Four-stage extraction→informalization→vector→retrieval pipeline | STRUCTURAL_SYNTHESIS | `README.md`; `database/*.py`; `retrieve.py`; `search.py` |
| PostgreSQL schema and `record` view | SOURCE_DERIVED | `database/create_schema.py` |
| Match jixia and target Lean toolchain | SOURCE_DERIVED | `README.md` |
| Prefix-based module selection | SOURCE_DERIVED | `README.md`; `prefix.py`; `database/__init__.py`; `jixia_db.py` |
| Skip internal / proofWanted and mark private/examples invisible | SOURCE_DERIVED | `database/jixia_db.py` |
| Dependency-level ordering | SOURCE_DERIVED | `database/jixia_db.py`; `database/informalize.py` |
| Cycles can remain unlevelled | STRUCTURAL_SYNTHESIS | `jixia_db.py` topological loop + `informalize.py` level iteration |
| Translation uses header/docstring/neighbors/dependencies | SOURCE_DERIVED | `database/translate.py`; `database/informalize.py`; `prompt/*.md.j2` |
| Output marker parsing/retries | SOURCE_DERIVED | `database/translate.py`; `augment.py` |
| `DRY_RUN` fake informalization and no vector output | SOURCE_DERIVED | `.env.example`; `database/translate.py`; `database/vector_db.py` |
| HTTP embedding endpoint / instruction prefix / 4096-char truncation | SOURCE_DERIVED | `database/embedding.py`; `prompt/embedding_instruction.txt` |
| Bilingual vector text and visible-only vectorization | SOURCE_DERIVED | `database/vector_db.py` |
| Vector ID mismatch | SOURCE_DERIVED cross-file conflict | `database/vector_db.py`; `retrieve.py` |
| Repair vector ID to module:index | IMPLEMENTATION_DECISION | chosen to satisfy `retrieve.py` contract; `pp_name` already imported by vector writer |
| Add `EMBEDDING_URL` to runtime config | IMPLEMENTATION_DECISION required by code | `.env.example` vs `database/embedding.py` |
| Run schema before fresh manual indexing | STRUCTURAL_SYNTHESIS | `database/__init__.py`; `create_schema.py`; `Makefile`; README omission |
| CLI output / JSON mode | SOURCE_DERIVED | `search.py` |
| Query augmentation behavior | SOURCE_DERIVED | `augment.py`; `prompt/augment_prompt.j2`; `augment_assistant.txt` |
| API endpoints and rate limits | SOURCE_DERIVED | `server.py`; `test_server.http` |
| Shared `Retriever.conn` concurrency caveat | STRUCTURAL_SYNTHESIS | `server.py` lifespan + middleware |
| Paired-store rebuild discipline | IMPLEMENTATION_DECISION | derived from cross-store ID and corpus coupling |
| Stage-boundary diagnostic method | STRUCTURAL_SYNTHESIS | architecture across repository |
