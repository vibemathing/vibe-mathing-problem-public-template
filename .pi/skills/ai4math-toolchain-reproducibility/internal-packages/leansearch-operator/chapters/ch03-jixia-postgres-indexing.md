# Chapter 3: jixia and PostgreSQL Indexing

## Core Idea

Indexing extracts Lean modules, symbols, declarations, and dependency edges into PostgreSQL, then computes dependency levels that later control informalization order.

## Choose module prefixes deliberately

The indexing command accepts comma-separated Lean module prefixes:

```bash
python -m database jixia <project-root> Init,Lean,Mathlib
```

A module is included when its module name starts with any supplied prefix. Use the helper before a costly run:

```bash
python -m prefix --project_root <project-root> --prefixes Init.Grind,Init.Control.Lawful
```

`prefix.py` prints all discovered modules and the subset matched by the prefixes. Prefer the smallest prefix set that covers the user's actual search domain.

## Extraction procedure

`load_data()` in `database/jixia_db.py` processes both:

- the target project root, and
- `<LEAN_SYSROOT>/src/lean`.

For each base directory it asks jixia for `module`, `declaration`, and `symbol` plugins.

### Modules

Store module name, raw file bytes, and module docstring. Existing module rows are left unchanged with `ON CONFLICT DO NOTHING`.

### Symbols

Skip internal symbols. Store formal type and proposition metadata. Add dependency edges for type references and, when available, value references. An edge `source → target` means the source depends on the target.

### Declarations

Read original module bytes so source ranges can recover pretty-printed signatures/values. Skip internal declarations and `proofWanted`. Visibility is false for private declarations and examples. Named declarations link to `symbol`; examples have `name = NULL` and are filtered out by the current insertion condition.

## Dependency-level computation

The code starts level 0 with symbols having no outgoing dependency edges. It repeatedly inserts any unassigned symbol whose direct dependency targets all have levels, using:

`level(source) = max(level(target)) + 1`.

This is a dependency-first ordering: foundational symbols receive smaller levels and can be informalized before symbols that depend on them.

### Cycle caveat

A dependency cycle with no resolvable base can remain without a level. `generate_informal()` iterates only integer levels up to `MAX(level)`, so unlevelled symbols can be skipped indefinitely. If declaration counts and informal counts diverge unexpectedly, check for symbols absent from `level`.

## Validation queries

Use simple SQL checks after indexing:

```sql
SELECT COUNT(*) FROM module;
SELECT COUNT(*) FROM symbol;
SELECT COUNT(*) FROM declaration;
SELECT COUNT(*) FROM dependency;
SELECT COUNT(*) FROM level;

SELECT COUNT(*)
FROM symbol s
LEFT JOIN level l ON l.symbol_name = s.name
WHERE l.symbol_name IS NULL;
```

Also inspect distribution by level and visibility before paying for informalization:

```sql
SELECT level, COUNT(*) FROM level GROUP BY level ORDER BY level;
SELECT visible, COUNT(*) FROM declaration GROUP BY visible;
```

## Recovery rules

- **No tables/types** → run `python -m database schema` in the same database.
- **`invalid header`** → align jixia and target Lean toolchains.
- **Unexpectedly few modules** → inspect prefix matching, project root, and jixia module discovery.
- **Symbols but few declarations** → inspect internal/proofWanted filtering and symbol-link condition.
- **Many symbols without level** → inspect dependency cycles or missing dependency targets before informalization.
- **Need a clean rebuild** → recreate PostgreSQL and Chroma state together; stale cross-store data is harder to diagnose than a deterministic rebuild.

## Why this stage matters downstream

The informalization prompts rely on module headers, neighbor declarations, and already-informalized dependencies. A malformed graph can degrade description quality even if the LLM endpoint itself is healthy.

## Connects To

- Ch 1 for schema relationships.
- Ch 4 for level-ordered translation.
- Ch 8 for rebuild and cycle diagnostics.
