# Chapter 6: Search, Retrieval, and Query Augmentation

## Core Idea

Search embeds natural-language queries, asks Chroma for nearest neighbors, then hydrates full Lean declaration records from PostgreSQL. Query augmentation is a separate LLM step that can expand underspecified mathematical language before search.

## CLI search

```bash
python search.py "rank-nullity theorem"
python search.py -n 20 "Haar measure"
python search.py --json "Cayley-Hamilton theorem"
```

`search.py` loads `.env`, connects to PostgreSQL with autocommit, creates `Retriever`, and calls `batch_search` for one or more query strings.

Human output includes distance, declaration kind/name/signature, elaborated type, and informal name/description. JSON output serializes the nested `QueryResult` list.

## Retrieval procedure

`Retriever` opens a persistent Chroma client and existing `leansearch` collection, then uses `MistralEmbedding` with `prompt/retrieve_instruction.txt`.

For each query:

1. embed query text;
2. `collection.query(..., n_results=N, include=["distances"])`;
3. for each vector hit, parse the document ID;
4. fetch SQL record by module and declaration index;
5. return `QueryResult(result=<Record>, distance=<float>)`.

This makes the vector-ID compatibility check mandatory.

## Direct fetch

`batch_fetch()` accepts Lean names and queries the `record` view by declaration name. It is useful when the caller already knows exact declarations and wants their enriched records without semantic search.

The function assumes each name resolves. A missing record can produce `None` even though the declared return type is `list[Record]`; callers should treat absent informalized records as a possible cause.

## Query augmentation

`Augmentor` loads `augment_prompt.j2` and an assistant persona. It asks the model to paraphrase a short mathematical search query into a richer natural-language description without mathematical symbols/LaTeX.

The expected response contains:

```text
Paraphrase: "..."
```

The parser returns the quoted paraphrase when matched; if the marker is missing, it returns the full model answer. After repeated JSON-decode failures, it falls back to the original user input.

Augmentation can improve recall for vague user phrases, but it changes the query distribution. Compare raw and augmented queries when diagnosing relevance.

## Decision rules for ranking problems

1. **No results / exceptions**: verify collection presence, embedding service, then ID hydration.
2. **Results exist but look unrelated**: compare raw query vs augmented query; inspect informal descriptions and embedding service/model.
3. **Formal names found but record hydration missing**: inspect `record` view/informal coverage and vector IDs.
4. **Only some declaration types appear**: remember vectorization includes visible declarations with informal rows; private/examples are excluded.
5. **Distances look plausible but semantics are poor**: sample the actual document text that was embedded before changing `n_results`.

## Validation experiment

Use 5–10 known mathematical concepts with known Lean declarations. For each, record:

- raw query;
- optional augmented query;
- top-k declaration names;
- distances;
- whether the expected declaration appears;
- whether failures come from corpus coverage or ranking.

Do this on a small prefix before indexing all of Mathlib.

## Connects To

- Ch 5 defines embedding/index assumptions.
- Ch 7 exposes these operations over HTTP.
- Ch 8 diagnoses hydration and augmentation failures.
