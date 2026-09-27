# Chapter 11: References, Provenance, and Anti-Fabrication

## Core Idea
Load-bearing mathematical choices should come from actual sources, not plausible paraphrases. Archon separates source retrieval, blueprint synthesis, and proof implementation so provenance can survive the pipeline.

## Grounding Workflow
1. Register relevant papers/books/notes under `references/`.
2. When a plan or blueprint depends on a source, read the original material directly.
3. Cite the relevant source location in blueprint prose.
4. Distinguish verified Mathlib APIs from expected names and known gaps.
5. If a source is unavailable, mark that limitation rather than inventing a theorem/proof.

The reference-retriever subagent is designed to fetch original PDFs/TeX/online sources into the project. The strategy auditor compares strategy against actual references. Blueprint writers can spawn retrieval when a missing source blocks faithful drafting.

## Informal Agent Boundary
The informal agent returns model-generated proof sketches from its training/context; it is not a literature retriever. Use it as a brainstorming source, then verify mathematics and Lean. Do not cite it as documentary provenance.

## Anti-Fabrication Checks
- verify named external results before treating them as load-bearing;
- test suspicious claims with small examples/countermodels;
- record unavailable sources explicitly;
- keep source citations attached to blueprint blocks as the project evolves;
- preserve one-to-one blueprint/Lean mapping so provenance can be followed to implementation.

## Failure Recovery
If the blueprint relies on an unverified claim, pause downstream proving, retrieve/inspect the source, revise the proof route, and rebuild the DAG. If a guessed Mathlib lemma does not exist, switch from search to construction or `mathlib-build` rather than repeating name guesses.

## Source Provenance
Primary: reference-retriever/strategy-auditor/blueprint-writer descriptors, plan and DAG prompts, AGENTS tool notes.

## Frameworks Introduced
- **Source-first planning**: retrieve/read original material before turning a load-bearing claim into strategy or blueprint structure.
- **Provenance chain**: source → blueprint claim/proof → Lean declaration → verification evidence.
- **API confidence tags**: keep verified library facts distinct from expected names and known gaps.

## Key Concepts
- **Original source**: PDF, TeX, online text, or user-provided document that can support the mathematical claim.
- **Reference retriever**: subagent that stores original sources and lightweight registry metadata.
- **Strategy auditor**: fresh/deep reviewer that compares the plan against actual references.
- **Informal agent**: model-generated sketch provider; useful for ideas, unsuitable as documentary evidence.

## Mental Models
- Think of source provenance as **type information for mathematical claims**: without it, a plausible statement may flow far downstream before failing.
- Treat `[verified]`, `[expected]`, and `[gap]` as **confidence states**, each with a different next action.

## Anti-patterns
- **Cite a model sketch as literature**: it has no source guarantee.
- **Paraphrase drift**: successive agents summarize the same theorem until hypotheses disappear.
- **Invent missing citations**: unavailable source material must remain an explicit limitation.
- **Assume a likely Mathlib name exists**: verify before planning around it.

## Worked Example
The paper states a compactness lemma with a separability hypothesis. A planner's memory omits the hypothesis and designs a stronger Lean theorem. Before proving, the strategy auditor reads the actual PDF/TeX, detects the missing assumption, and the blueprint is corrected. The Lean statement now matches the source. A Mathlib analog is tagged `[expected]` until local semantic search confirms its exact name and hypotheses; only then is it `[verified]`.

## Key Takeaways
1. Read sources at the point where they determine structure.
2. Keep provenance attached to blueprint claims.
3. Separate brainstorming from evidence.
4. Verify library APIs before making them load-bearing dependencies.

## Connects To
- **Ch 03**: blueprint proof quality and citations.
- **Ch 06**: library search/verification.
- **Ch 12**: provenance should survive extract/merge transformations.
