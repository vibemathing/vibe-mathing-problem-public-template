# Chapter 7: API, Feedback, and Operations

## Core Idea

`server.py` wraps retrieval and augmentation in FastAPI, manages PostgreSQL connections through a pool, records searches, issues a feedback session cookie for single-query searches, and applies endpoint/default rate limits.

## Lifespan and connection model

At startup the app:

1. loads `.env`;
2. creates a PostgreSQL `ConnectionPool` with autocommit;
3. constructs one `Augmentor`;
4. constructs one `Retriever` initially with `conn=None`;
5. stores the pool and helpers on the app.

HTTP middleware checks out a PostgreSQL connection for each request and assigns it to `app.retriever.conn` before calling the endpoint.

### Concurrency caveat

`app.retriever` is shared and its `.conn` field is mutated per request. With concurrent requests, this shared mutable connection pointer deserves scrutiny. If production concurrency causes cross-request behavior, prefer passing the request's connection explicitly or constructing request-scoped retrieval state.

## Start the server

With the repository root as the working directory and `.env` configured:

```bash
uvicorn server:app
```

The prompt loaders use relative paths by default, so starting from another working directory can break `prompt/...` file discovery unless `PROMPT_DIR` is set appropriately.

## Endpoints

### `POST /search`

Body parameters:

- `query: list[str]`
- `num_results: int`, constrained to 1–150, default 10.

Every query is logged in `leansearch.query`.

- For exactly one query, the generated query UUID is returned as a `session` cookie.
- For multiple queries, rows are inserted, but no session cookie is set.

Returns nested semantic-search results.

### `POST /fetch`

Accepts a list of Lean names and returns enriched records. Explicit rate limit: 10/second.

### `POST /augment`

Accepts one string body and returns the augmented/paraphrased query. Explicit rate limit: 15/minute.

### `POST /feedback`

Reads the `session` cookie and a `Feedback` object containing:

- `declaration` Lean name;
- `action` string;
- optional `cancel` boolean.

When `cancel` is true, the matching feedback row is deleted; otherwise an action row is inserted.

A valid session cookie is expected. The straightforward path is a prior single-query `/search` response.

## Rate limiting

The app installs SlowAPI with a default 1 request/second limit based on remote address. `/fetch` and `/augment` have endpoint-specific decorators; `/search` relies on the default app limit.

When load testing, distinguish legitimate rate-limit responses from database/embedding failures.

## Operational checks

- `/search` should record a query row and return hydrated results.
- Single-query `/search` should set `session` cookie.
- `/feedback` should insert/delete exactly one row keyed by session/declaration.
- `/fetch` should resolve a known informalized declaration.
- `/augment` should return a usable string even when the regex marker is absent.

The repository's `test_server.http` provides a multi-query `/search` example. It does not cover feedback, session-cookie behavior, or other endpoints.

## Failure recovery

- **422 on feedback / missing cookie** → first perform a single-query search and retain the cookie.
- **429 responses** → inspect configured rate limit before changing databases or models.
- **Search endpoint logs query but returns retrieval exception** → inspect embedding/Chroma/ID hydration path.
- **Concurrent anomalies** → investigate the shared mutable `Retriever.conn` design.
- **Fetch returns invalid/empty record** → check `record` view and informalization coverage.

## Connects To

- Ch 6 defines retrieval and augmentation behavior.
- Ch 8 catalogs production caveats and patch boundaries.
