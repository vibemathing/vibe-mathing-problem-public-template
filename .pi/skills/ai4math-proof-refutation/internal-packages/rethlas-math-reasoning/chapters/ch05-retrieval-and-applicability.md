# Chapter 5: Retrieval & Applicability

## Core Idea
Rethlas uses external mathematical literature as a source of exact statements, proof mechanisms, examples, and obstructions. Retrieval is complete only after context and applicability have been checked.

## Frameworks Introduced

- **Statement-first theorem search**
  - **When to use**: nontrivial subgoals, background gaps, examples/counterexamples, or a new problem needing context.
  - **How**: search the theorem index first with a complete mathematical statement when possible; fall back to broader web search if results are vague or irrelevant.
- **Paper-context expansion**
  - **When to use**: a useful theorem comes from a paper.
  - **How**: read the paper text around the theorem and its proof; expand definitions and terminology as used locally; record how the theorem's objects and hypotheses map to the current setting.
- **Proof-method extraction**
  - **When to use**: a theorem is close to the target.
  - **How**: read its proof and extract transferable constructions, reductions, invariants, and proof patterns rather than citing the statement as an unexplained black box.
- **Partial-result diagnosis**
  - **When to use**: the closest known result has extra hypotheses or proves only a special case.
  - **How**: identify where those hypotheses enter the proof, what fails without them, and what obstruction that exposes for the full target.

## Key Concepts

- **Complete statement** — exact theorem/lemma text preserved for later proof use.
- **Source identifiers** — paper ID, arXiv ID, theorem ID when available.
- **Applicability check** — explicit match of definitions, hypotheses, ambient objects, and terminology.
- **Proof insight** — a technique from the source proof that may migrate to the current problem.
- **Search intent** — theorem, construction, example, counterexample, or background.

## Mental Models

- Treat literature search as **retrieval plus semantic type-checking**.
- Treat a paper proof as a **method library**, not merely a citation source.
- Treat extra hypotheses as **diagnostic sensors** for the true hard point.
- When retrieval stops producing guidance, switch to **independent proof exploration**.

## Anti-patterns

- **Using a theorem from its title or search snippet**.
- **Assuming identical terminology implies identical definitions**.
- **Forcing the current object to satisfy an extra hypothesis without asking why the source proof needs it**.
- **Repeating low-value searches indefinitely**.
- **Citing an external theorem without its full statement and source identifiers in the proof record**.

## Reference Table

| Retrieval result | Required follow-up |
|---|---|
| close theorem | read statement, context, proof, applicability |
| useful construction/example | map assumptions and adaptation path |
| partial theorem | diagnose extra hypotheses and failure point |
| vague/off-topic result | switch query or broader search |
| repeated weak results | stop retrieval; reason independently |

## Worked Example

Suppose a retrieved theorem proves the desired conclusion only for compact objects. Read the proof far enough to find the exact use of compactness. If compactness supplies a finite subcover that the target setting lacks, record that mechanism and the resulting obstruction. A new proof plan may then seek an alternative finiteness principle rather than trying to relabel the target object as compact.

## Key Takeaways

1. Search with complete statements when possible.
2. Read source context and proof before relying on a result.
3. Expand definitions and check hypotheses explicitly.
4. Preserve complete statements and source IDs for downstream proof writing.
5. Turn partial results into obstruction analysis.
6. Stop low-yield retrieval and return to mathematical reasoning.

## Connects To

- **Ch 6**: direct proving adapts retrieved proof ideas.
- **Ch 8**: external results have a strict citation contract.
- **Ch 9**: verification independently checks referenced statements and downstream deductions.

## Source Provenance

Primary source files: `agents/generation/.agents/skills/search-math-results/SKILL.md`, `agents/generation/AGENTS.md`, `agents/generation/mcp/server.py`, and `agents/verification/.agents/skills/check-referenced-statements/SKILL.md`.
