# Chapter 5: Embeddings and ChromaDB

## Core Idea

The vector index represents each visible declaration with both its formal signature and generated informal description, then stores embeddings in a persistent Chroma collection named `leansearch`.

## Embedding contract

`MistralEmbedding` reads a retrieval instruction and transforms every input into:

```text
Instruct: <retrieval instruction>
Doc: <content>
```

The source truncates each Python string to 4096 characters before sending it to `EMBEDDING_URL` via HTTP POST. The response body is expected to be JSON containing embeddings directly.

The class defines `DIMENSION = 4096`, but does not validate returned vector length. Validate service compatibility outside the class before indexing a large corpus.

## Vector corpus construction

`create_vector_db()` selects visible declarations that already have informal text:

- symbol name/kind;
- declaration module and index;
- signature or fallback type;
- informal name;
- informal description.

The embedded document combines formal and informal information, which helps semantic queries bridge natural mathematical language and Lean declarations.

Only `d.visible = TRUE` rows are included.

## Critical ID contract

Retrieval needs each vector hit to identify a SQL declaration. `retrieve.py` parses a Chroma ID as:

```text
<module-name>:<declaration-index>
```

then executes a SQL lookup on `(module_name, index)`.

However, this snapshot's `vector_db.py` writes the ID as the declaration's Lean name joined with spaces. These formats are incompatible.

### Preferred repair

Make the writer satisfy the reader's existing contract, for example conceptually:

```python
batch_id.append(f"{pp_name(module_name)}:{index}")
```

`vector_db.py` already imports `pp_name`, which supports this intended direction. After patching, rebuild the Chroma collection so every stored ID uses the new format. Label this as a repair to the supplied snapshot.

An alternative is to change retrieval to query SQL by declaration name, but that changes the hydration contract and must handle naming/JSON conversion consistently.

## Build procedure

1. Verify `record`/visible declarations exist.
2. Verify `EMBEDDING_URL` with a one-item call.
3. Reconcile the vector ID contract.
4. Use a clean `CHROMA_PATH` or delete the old collection intentionally.
5. Run:

```bash
python -m database vector-db --batch-size 8
```

6. Inspect Chroma count and sample IDs before running search.

## Rebuild semantics

The code calls `client.create_collection(...)`. If `leansearch` already exists at the chosen path, creation can fail. This implementation does not perform an incremental update or get-or-create. Prefer an intentional rebuild path when changing embeddings or ID format.

## Failure recovery

- **Missing `EMBEDDING_URL`** → add it; the sample env file is incomplete for this source.
- **HTTP/non-JSON error** → probe the embedding service directly; the code has no timeout/status validation or retry wrapper.
- **Dimension mismatch** → confirm embedding model/service output before Chroma add/query.
- **Search hit cannot hydrate** → inspect stored Chroma IDs first.
- **Collection exists** → clear/repoint `CHROMA_PATH` or modify code for an intentional update.
- **No vectors** → ensure informal rows exist and visible declarations are selected; `DRY_RUN=true` exits vector creation early.

## Connects To

- Ch 4 produces informal text.
- Ch 6 embeds search queries with the same instruction class.
- Ch 8 provides repair sequencing.
