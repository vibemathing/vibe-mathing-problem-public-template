# Chapter 2: Environment and Installation

## Core Idea

A working LeanSearch installation depends on four independently configured systems: Python, PostgreSQL, Lean/jixia, and an LLM + embedding service. Validate each boundary before running a full indexing job.

## Prerequisite checklist

### Python

Create an isolated environment and install the pinned requirements:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The source uses Python syntax with `X | None`; in practice use a modern Python version even though `ruff.toml` declares a Python 3.9 lint target.

### PostgreSQL

Create a database and set `CONNECTION_STRING`:

```bash
createdb <db-name>
python -m database schema
```

The README describes database creation but omits the explicit schema command in its manual sequence. The code and Makefile require the schema before `jixia` loading.

### jixia and Lean

Build jixia and point `JIXIA_PATH` at its built executable. Set `LEAN_SYSROOT` to the active Lean installation root. The jixia repository and the target Lean project must use matching Lean toolchains.

Use:

```bash
lake env
```

to find `LEAN_SYSROOT`. If indexing reports an invalid module header, compare both `lean-toolchain` files before reinstalling Python packages.

### LLM translation

The OpenAI client reads the standard OpenAI-compatible environment variables:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

The sample config recommends a DeepSeek-compatible endpoint/model, while the code itself accepts any compatible service that returns chat completions in the expected text format.

### Embedding service

`database/embedding.py` performs an HTTP `POST` to `EMBEDDING_URL` with a JSON array of instruction-prefixed strings. This variable is required by code but absent from `.env.example`.

Before vectorization, verify the service directly and confirm it returns one embedding per input. The source constants expect dimension 4096 conceptually, though the code does not enforce the dimension locally.

## Environment variables

| Variable | Used by | Required operationally | Notes |
|---|---|---:|---|
| `JIXIA_PATH` | `database/__main__.py` | yes for indexing | built jixia executable |
| `LEAN_SYSROOT` | `jixia_db.py`, `prefix.py` | yes | Lean installation root |
| `CONNECTION_STRING` | CLI/server/search | yes | PostgreSQL DSN |
| `OPENAI_API_KEY` | OpenAI client | yes for real informalization/augment | keep secret |
| `OPENAI_BASE_URL` | OpenAI client | service-dependent | sample points at DeepSeek |
| `OPENAI_MODEL` | translate/augment/server | yes | model name |
| `CHROMA_PATH` | vector/retrieval/server | yes | persistent Chroma directory |
| `EMBEDDING_URL` | embedding/retrieval | yes | missing from sample `.env` |
| `PROMPT_DIR` | prompt loaders | optional | defaults to `prompt` |
| `LOG_FILENAME`, `LOG_FILEMODE`, `LOG_LEVEL` | database entrypoint | yes as configured | sample values provided |
| `DRY_RUN` | translate/vector build | yes as string | `"true"` enables dry run |
| `EMBEDDING_DEVICE` | sample `.env` only | no in this snapshot | current Python code does not use it |

## Safe smoke-test sequence

1. `python -m database schema`
2. `python -m prefix --project_root <small-project> --prefixes <small-prefix>`
3. `DRY_RUN=true python -m database jixia ...`
4. `DRY_RUN=true python -m database informal --limit-level 1 --limit-num-per-level 5`
5. Inspect rows in `module`, `symbol`, `declaration`, `level`, `informal`.
6. Switch to real LLM mode for a tiny subset.
7. Validate embedding service separately before full Chroma build.

`DRY_RUN` does not create usable embeddings: `vector_db.py` returns before embedding/addition. Use it to validate extraction/translation wiring, not search quality.

## Common setup mistakes

- Running `database jixia` against a fresh empty database without schema.
- Pointing `JIXIA_PATH` at a jixia build for another Lean version.
- Assuming `EMBEDDING_DEVICE` configures the current embedding code; it does not.
- Copying `.env.example` and missing `EMBEDDING_URL`.
- Reusing a populated Chroma path with `create_collection` and expecting an in-place update.

## Connects To

- Ch 3 for indexing prerequisites and schema effects.
- Ch 5 for embedding service contract.
- Ch 8 for source/config mismatches.
