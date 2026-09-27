# Chapter 4: Informalization and Translation

## Core Idea

LeanSearch makes formal declarations semantically searchable by generating an informal name and informal mathematical description. Translation is context-aware and dependency-ordered; output is parsed from a strict text format and stored in PostgreSQL.

## Inputs to translation

`TranslationInput` carries:

- formal Lean name;
- signature/type;
- optional value/body;
- docstring;
- declaration kind;
- module header/docstring;
- nearby declarations in the same module;
- dependencies referenced by the item.

Nearby and dependent items include prior informal names/descriptions when available. This makes dependency ordering operationally important.

## Template routing

`TranslationEnvironment.translate()` chooses one of three templates:

- `instance.md.j2` for instances;
- `definition.md.j2` when the declaration kind has a semantically meaningful value/body (`classInductive`, `definition`, `inductive`, `structure`);
- `theorem.md.j2` for the remaining theorem-like items.

The templates tell the model to preserve mathematical meaning, use human-readable notation, exploit docstrings/context, and avoid introducing claims not present in the formal statement.

## Output contract

The response is parsed with regular expressions for two markers:

- `**Informal statement:** ... **End of informal statement**`
- `**Informal name:** ...`

If parsing fails, the call is retried up to five times. JSON decoding failures are also retried after a short sleep. Other API/network exceptions are not caught by this layer.

When all attempts fail, translation returns `None` and the caller logs a warning without inserting an `informal` row.

## Batch execution

`generate_informal()`:

1. determines the highest dependency level;
2. walks levels from 0 upward;
3. selects symbols at that level that do not already have an `informal` row;
4. fetches neighbors and dependencies;
5. translates a batch concurrently with `asyncio.gather`;
6. inserts successful results;
7. closes the async OpenAI client for the batch.

Useful diagnostic flags:

```bash
python -m database informal --batch-size 10 --limit-level 2 --limit-num-per-level 5
```

## Dry-run behavior

With `DRY_RUN=true`, no LLM request is made. Each item receives a fake name/description containing diagnostic material. This is useful for validating the database traversal and insertion path, but those fake descriptions must not be treated as search-quality content.

## Quality checks before vectorizing

Sample rows at several dependency levels and verify:

- the informal name states a recognizable mathematical relationship;
- the informal description preserves the formal claim without extra reasoning;
- LaTeX/math notation is intelligible;
- docstring implementation notes have not leaked in as mathematical claims;
- dependencies are helping rather than causing circular or irrelevant explanation.

If translation coverage is low, compare:

```sql
SELECT COUNT(*) FROM symbol;
SELECT COUNT(*) FROM informal;
SELECT COUNT(*) FROM record;
```

Then find missing informal rows by joining `symbol` to `informal` and `level`.

## Failure recovery

- **Repeated format parse failures** → inspect raw model responses and template/output-marker compatibility before changing the database.
- **API JSON decode retries** → verify service stability and compatibility.
- **Hard network/auth errors** → fix OpenAI-compatible endpoint/key; the code does not convert all exceptions into retries.
- **Some symbols never attempted** → inspect missing dependency levels.
- **Descriptions look context-poor** → verify dependencies/neighbors already have informal rows and ordering is working.

## Connects To

- Ch 3 explains dependency levels and source context.
- Ch 5 consumes the bilingual formal+informal text.
- Ch 8 catalogs retry and coverage caveats.
