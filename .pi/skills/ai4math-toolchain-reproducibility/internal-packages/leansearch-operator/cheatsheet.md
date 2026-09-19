# LeanSearch Decision Cheatsheet

## Build sequence

| Goal | Command / check |
|---|---|
| Create DB schema | `python -m database schema` |
| Inspect module coverage | `python -m prefix --project_root <root> --prefixes <prefixes>` |
| Load Lean data | `python -m database jixia <root> <prefixes>` |
| Small informalization | `python -m database informal --limit-level 2 --limit-num-per-level 5` |
| Full informalization | `python -m database informal` |
| Build vectors | `python -m database vector-db` |
| Search | `python search.py -n 10 "<query>"` |
| JSON search | `python search.py --json "<query>"` |

## Symptom → first check

| Symptom | First check | Next action |
|---|---|---|
| `invalid header` | Lean versions | Match jixia and target `lean-toolchain` |
| missing SQL relation/type | schema | Run schema in correct DB |
| very few modules | prefixes/project root | Run prefix helper |
| symbols lack informal rows | `level` coverage | Find unlevelled/cyclic symbols |
| LLM parse retries | raw response markers | Align prompt/output format |
| `EMBEDDING_URL` KeyError | env | Add compatible endpoint |
| embedding HTTP/JSON failure | direct endpoint probe | Validate service/shape/dimension |
| Chroma collection exists | target path | Clean/repoint or implement update |
| Chroma hit → SQL miss/error | vector IDs | Reconcile writer/reader ID contract |
| no vectors in dry run | `DRY_RUN` | Expected; disable for real build |
| poor search relevance | corpus text first | Inspect informal text + raw/aug query |
| feedback lacks session | search mode | Do one single-query `/search` |
| HTTP 429 | rate limit | Respect default/endpoint limits |
| concurrency-only API anomaly | shared retriever connection | Use request-scoped connection design |

## Required env by stage

| Stage | Variables |
|---|---|
| jixia indexing | `CONNECTION_STRING`, `JIXIA_PATH`, `LEAN_SYSROOT` |
| informalization | above DB + `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `DRY_RUN` |
| vector build | DB + `CHROMA_PATH`, `EMBEDDING_URL`, `DRY_RUN` |
| CLI search | DB + `CHROMA_PATH`, `EMBEDDING_URL` |
| API | DB + Chroma/embedding + OpenAI vars for `/augment` |

## Before scaling to Mathlib

1. Tiny prefix indexes cleanly.
2. `symbol`, `declaration`, `level` counts make sense.
3. Sample informalizations are mathematically faithful.
4. Embedding endpoint is stable.
5. Vector IDs round-trip to SQL records.
6. Known queries retrieve expected declarations.
7. Only then expand prefixes and batch sizes.
