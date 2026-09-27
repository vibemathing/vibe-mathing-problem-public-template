# Patterns and Techniques

## Stage-Boundary Diagnosis
**When to use**: Any failure in a multi-stage index/search pipeline.  
**How**: Identify the first missing/invalid persisted artifact; verify the previous stage; change only the owning stage.  
**Trade-offs**: Slower than random tweaking for trivial issues, much faster for cross-store failures.

## Module-Prefix Scoping
**When to use**: Before indexing large Lean projects such as Mathlib.  
**How**: Use `prefix.py` to enumerate modules; choose the smallest prefixes covering the intended domain; expand only after a successful small run.  
**Trade-offs**: Smaller corpus lowers cost and speeds iteration but can reduce recall outside selected modules.

## Dependency-First Informalization
**When to use**: Translating formal declarations that reference other formal concepts.  
**How**: Compute dependency levels; translate prerequisites first; feed their informalizations plus local neighbors into later prompts.  
**Trade-offs**: Improves context continuity but unresolved cycles can block coverage.

## Bilingual Vector Record
**When to use**: Semantic retrieval must bridge natural mathematical language and formal Lean syntax.  
**How**: Embed a record containing kind/name/signature plus informal name/description.  
**Trade-offs**: More semantic signal, but generated text quality becomes part of retrieval quality.

## Stable Hydration Key
**When to use**: A vector store only holds IDs/embeddings while SQL holds authoritative records.  
**How**: Define one deterministic ID encoding shared by vector writer and retriever; validate sample round trips before bulk indexing.  
**Trade-offs**: Requires rebuild if the encoding changes. In this snapshot, this pattern is violated and must be repaired.

## Query Enrichment
**When to use**: User queries are short, colloquial, or omit mathematical context.  
**How**: Ask an LLM for a richer paraphrase, then compare retrieval with raw query.  
**Trade-offs**: Can increase recall but can also introduce query drift; keep raw-query baselines.

## Limited-Cost Smoke Test
**When to use**: Before expensive full-corpus informalization.  
**How**: Use small module prefixes, `--limit-level`, `--limit-num-per-level`, and optionally `DRY_RUN=true`; inspect rows and prompts before scaling.  
**Trade-offs**: Dry run cannot validate actual embeddings or semantic ranking.

## Paired Store Rebuild
**When to use**: Changing vector IDs, embedding model, or corpus semantics.  
**How**: Treat PostgreSQL source snapshot and Chroma index as a paired version; rebuild downstream artifacts consistently and validate one round trip.  
**Trade-offs**: More compute, fewer stale-state ambiguities.

## Feedback Sessioning
**When to use**: Recording relevance feedback for a specific search.  
**How**: Perform a single-query `/search`, retain the `session` cookie, then send declaration/action to `/feedback`; use cancel to delete.  
**Trade-offs**: Current API does not issue one session cookie for multi-query search.
