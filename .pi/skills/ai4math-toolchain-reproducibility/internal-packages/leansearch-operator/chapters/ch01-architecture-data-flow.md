# Chapter 1: Architecture and Data Flow

## Core Idea

LeanSearch converts formal Lean declarations into a searchable bilingual corpus. PostgreSQL stores structured source facts and generated informal text; ChromaDB stores vectors for the visible declarations. Search joins the two stores through a vector document ID.

## System map

```text
Lean project + Lean sysroot
        |
        v
      jixia
        |
        v
PostgreSQL: module -> symbol/declaration -> dependency -> level
        |
        v
LLM translation (formal + docstring + neighbors + dependencies)
        |
        v
PostgreSQL: informal + record view
        |
        v
Embedding HTTP service
        |
        v
ChromaDB collection "leansearch"
        |
 query -> embedding -> nearest vector IDs
        |                    |
        +--------------------+
                 |
                 v
       hydrate Record from PostgreSQL
```

## Persistent schema

`database/create_schema.py` creates:

- `module`: Lean module name, raw content bytes, module docstring.
- `symbol`: named Lean symbols with kind, type, proposition flag.
- `declaration`: source-level declaration metadata keyed by `(module_name, index)`; a named declaration can reference `symbol`.
- `dependency`: `source → target` edges, tagged by whether the dependency appears in the type or value.
- `level`: dependency-derived integer used to order informalization.
- `informal`: generated natural-language name and description per symbol.
- `record` view: joins declaration + informal + symbol and is the retrieval-facing SQL record.
- `leansearch.query`: stored search query/session rows.
- `leansearch.feedback`: feedback action keyed by query and declaration.

The `record` view uses inner joins to `informal` and `symbol`, so a declaration is not retrievable through that view until informalization exists.

## Data invariants

1. jixia and target project must agree on the Lean toolchain format.
2. `declaration.name` links to `symbol.name` for named declarations. Examples are deliberately represented without a name and are not inserted by the current `WHERE EXISTS` insert path.
3. Dependency levels should be available before `database informal`; informalization iterates levels in ascending order.
4. Only `declaration.visible = TRUE` rows are vectorized.
5. Every Chroma ID used by retrieval must deterministically map back to one SQL declaration.

## Operational reasoning

Use the persistent boundaries to localize failures:

- If module/symbol/declaration counts are wrong, stay in jixia/PostgreSQL.
- If `record` is sparse while declarations exist, inspect `informal` generation.
- If `record` is healthy but Chroma is empty, inspect embedding/vector build.
- If Chroma returns IDs but SQL hydration fails, inspect the ID contract.
- If CLI search works but HTTP behavior fails, inspect server/session/rate-limit logic rather than rebuilding indexes.

## Failure mode to remember

The source snapshot violates its own vector-ID invariant: `database/vector_db.py` writes IDs from the Lean declaration name, while `retrieve.py` parses each ID as `module_name:index`. Treat this as a first-class compatibility check before diagnosing ranking quality.

## Connects To

- Ch 3: how structured rows and levels are built.
- Ch 4: why informalization is dependency-aware.
- Ch 5: vector corpus and ID contract.
- Ch 6: retrieval hydration.
- Ch 8: source-specific mismatches and repairs.
