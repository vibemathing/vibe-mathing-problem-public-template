# Chapter 10: Runner & Operations

## Core Idea
The bundled runner turns the proof method into a repeatable local loop: validate the problem path, prepare references, verify service health, reuse one agent session, alternate independent and search-enabled continuation, stop only on a verified blueprint, and preserve logs/results for inspection.

## Frameworks Introduced

- **Service-first startup**
  - **When to use**: local Rethlas execution.
  - **How**: install verification dependencies, start the local verifier service, then run generation with its MCP dependencies.
- **Safe problem selection**
  - **When to use**: runner invocation.
  - **How**: require a relative markdown path under `data/`, reject parent traversal, derive the data-relative problem ID, and compute a sibling reference directory.
- **Reference pre-processing**
  - **When to use**: a problem-specific reference directory exists.
  - **How**: read markdown/LaTeX/text directly; pre-extract PDFs to text when the extraction utility is available; reason over extracted text instead of binary PDFs.
- **Alternating continuation loop**
  - **When to use**: the first proof turn does not finish.
  - **How**: resume the same agent session; alternate a search-disabled deep-reasoning turn with a search-enabled turn; check for the verified artifact before every new iteration.
- **Result projection**
  - **When to use**: browsing many proof outputs.
  - **How**: prefer verified blueprints over drafts, mirror category directories into a static site, and transform math delimiters for reliable rendering.

## Key Concepts

- **`MAX_ITERATIONS`** — positive runner bound; default source value is 10.
- **Session reuse** — continuation turns resume the initial agent session rather than reinitializing proof state.
- **Verification health check** — warning signal that a verified artifact may be impossible to produce until the service is reachable.
- **Iteration log** — per-turn trace kept under the problem's logs directory.
- **Result site** — local Zola/MATbook projection of draft or verified markdown results.

## Mental Models

- Alternate **retrieval and independent reasoning** to prevent a run from becoming search-only.
- Treat the verified file as the **runner's stop signal**, not the generator's prose claim.
- Treat local logs and persistent memory as **post-mortem material** when a bounded run exhausts its iterations.
- Keep rendering as **presentation infrastructure** separate from proof correctness.

## Anti-patterns

- **Running generation before the verifier is available when verified output is required**.
- **Passing absolute or parent-traversing problem paths**.
- **Starting a new reasoning session every iteration** and losing continuity.
- **Assuming PDFs were read when extraction failed**.
- **Displaying a draft as if it were verified**: the site prefers the verified file when present, otherwise clearly remains on the draft artifact.

## Commands & APIs

Source deployment sequence, abstracted:

```text
1. Create/install verification environment and start local API on port 8091.
2. Create/install generation MCP environment.
3. Run the generation test runner with PROBLEM_FILE=data/<path>.md.
4. Inspect memory/, logs/, and results/; serve the optional result site separately.
```

## Reference Table

| Operational signal | Interpretation | Action |
|---|---|---|
| verifier health unavailable | strict promotion cannot complete | start/fix verifier service |
| runner cannot find session ID | continuation state unavailable | inspect first iteration log |
| max iterations reached | bounded run made no verified artifact | inspect failure memory; re-plan or raise bound deliberately |
| PDF refs + no extractor | those PDF refs are unavailable to agent | install extractor or supply text |
| verified file appears | strict stop condition met | end loop and publish result |

## Worked Example

A problem at `data/algebra/p.md` with optional `data/algebra/p.refs/` is launched through the runner. The first turn creates the proof state. If no verified file exists, the same session resumes first without search, then with search, repeating up to the configured iteration bound. Every turn writes a log; the run exits successfully only when `results/algebra/p/blueprint_verified.md` exists.

## Key Takeaways

1. Start verification before generation when strict output matters.
2. Validate problem paths and preserve category structure.
3. Pre-extract binary references into readable text.
4. Reuse the reasoning session across iterations.
5. Balance search with independent reasoning.
6. Use the verified artifact as the stop condition.
7. Keep the result site as a view layer over proof artifacts.

## Connects To

- **Ch 1**: runner paths implement the architecture's isolation rules.
- **Ch 2**: persistent memory survives the continuation loop.
- **Ch 9**: verifier service defines proof acceptance.

## Source Provenance

Primary source files: `README.md`, `agents/generation/tests/run_example.sh`, `agents/generation/site/*`, `agents/verification/api/server.py`, `agents/verification/scripts/test_verify_endpoint.py`, and dependency/configuration files on both agent sides.
