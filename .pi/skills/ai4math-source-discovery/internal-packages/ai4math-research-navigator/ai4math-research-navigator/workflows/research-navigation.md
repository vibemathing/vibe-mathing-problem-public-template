# Workflow — Literature / resource navigation

1. Restate the research question in 3–8 search terms.
2. Classify axis and subtopic.
3. Run `python scripts/query_catalog.py --query "<terms>" --limit 12`.
4. Prefer records from the most specific matching subsection.
5. Return a short set grouped by role: foundational, method, benchmark/data, verifier, recent snapshot.
6. Do not summarize unbundled paper internals from title alone. If the user needs details, retrieve the linked paper next.
7. Mention the July 2026 snapshot boundary for “latest” requests.
