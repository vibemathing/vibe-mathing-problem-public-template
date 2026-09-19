# Glossary

**Augmentation** — LLM-based expansion of a short mathematical query into a richer natural-language paraphrase before retrieval (Ch 6).

**ChromaDB** — persistent vector store used for the `leansearch` collection and cosine nearest-neighbor search (Ch 5–6).

**Declaration** — source-level Lean item stored with module/index, visibility, kind, signature, optional value, and range (Ch 1, 3).

**Dependency** — directed edge from a symbol to a symbol used by its type or value; drives translation order (Ch 3–4).

**Dependency level** — integer assigned so prerequisite symbols receive lower levels than symbols depending on them (Ch 3–4).

**DRY_RUN** — string environment flag; when `true`, informalization inserts fake text and vectorization exits before embedding (Ch 2, 4–5).

**Embedding instruction** — retrieval task description prepended to every document/query before calling the embedding service (Ch 5–6).

**EMBEDDING_URL** — HTTP endpoint required by `MistralEmbedding`; absent from the source `.env.example` (Ch 2, 5, 8).

**Informal description** — generated natural-language mathematical statement stored per symbol and used in the vector document (Ch 4–5).

**Informal name** — concise generated human-readable name for a formal declaration (Ch 4).

**Internal symbol** — jixia symbol excluded by `is_internal` filtering during SQL ingestion (Ch 3).

**jixia** — Lean static-analysis tool used to extract modules, declarations, symbols, and references (Ch 2–3).

**LeanName** — structured Lean identifier representation used by jixia and persisted as JSONB (Ch 1, 3, 6).

**Module prefix** — Lean name prefix controlling which modules jixia indexes (Ch 3).

**Neighbor** — declarations near the current item in the same module, supplied as context to translation (Ch 4).

**Record** — Pydantic retrieval model backed by the SQL `record` view, combining declaration, symbol, and informal fields (Ch 1, 6).

**`record` view** — inner-join SQL view exposing only declarations with matching `informal` and `symbol` rows (Ch 1, 4).

**Session cookie** — UUID cookie set by a single-query `/search` request and used to associate `/feedback` with its query (Ch 7).

**Symbol** — named Lean entity with formal type, kind, and proposition metadata (Ch 1, 3).

**Vector ID contract** — encoding that lets a Chroma hit map back to a PostgreSQL declaration; inconsistent in this source snapshot (Ch 5, 8).

**Visible declaration** — declaration that is not private and not an example; only visible declarations are selected for vectorization (Ch 3, 5).
