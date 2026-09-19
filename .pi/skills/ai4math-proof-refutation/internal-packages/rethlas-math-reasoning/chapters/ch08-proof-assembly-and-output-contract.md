# Chapter 8: Proof Assembly & Output Contract

## Core Idea
Rethlas promotes exploratory work into a paper-like markdown blueprint only when a route can cover the entire target. The output contract forces dependencies to appear before use, preserves the original target statement, and makes external citations auditable.

## Frameworks Introduced

- **Whole-target assembly gate**
  - **When to use**: after a plan's subgoals are sufficiently solved.
  - **How**: assemble a full proof draft for the original theorem; keep exploratory fragments in memory rather than passing them off as a complete proof.
- **Dependency-first exposition**
  - **When to use**: writing the blueprint.
  - **How**: state and prove supporting definitions/lemmas/propositions before statements that depend on them; place the main theorem last.
- **Original-statement preservation**
  - **When to use**: final theorem section.
  - **How**: reproduce the complete informal statement from the input problem as the theorem statement; do not shorten away hypotheses.
- **External-result citation contract**
  - **When to use**: any proof step relies on an external result.
  - **How**: include the complete cited statement plus paper/theorem/arXiv identifiers when available, and ensure applicability analysis exists in the proof-state record.

## Key Concepts

- **Blueprint** — current complete informal proof draft in markdown.
- **Verified blueprint** — draft promoted after strict verification succeeds.
- **Paper-like order** — prerequisites before dependent claims; target theorem at the end.
- **Complete target statement** — exact input theorem preserved at final acceptance.
- **Proof provenance** — external statement, IDs, and contextual applicability carried into proof use.

## Mental Models

- Treat assembly as a **compilation step** from proof-state artifacts into a coherent argument.
- Treat the original theorem statement as an **interface contract**: dropping a hypothesis or conclusion silently changes the task.
- Treat external results as **linked dependencies with versioned semantics**: exact statement and context matter.

## Anti-patterns

- **Submitting a partial branch as a whole proof**.
- **Placing a lemma after the theorem step that uses it**.
- **Paraphrasing the final theorem so aggressively that assumptions disappear**.
- **Using an external result without its complete statement/source identity**.
- **Renaming a draft “verified” before the verifier gate**.

## Code Example

The source's preferred markdown shape is intentionally simple:

```markdown
# lemma lem:aux
## statement
...
## proof
...

# theorem thm:main
## statement
<original complete target statement>
## proof
...
```

## Reference Table

| Stage | Artifact | Acceptance status |
|---|---|---|
| exploration | memory channels | partial / provisional |
| assembled proof | `blueprint.md` | candidate only |
| verifier passed | `blueprint_verified.md` | Rethlas-verified |

## Worked Example

If a proof depends on an external lemma, place the lemma or its cited complete statement before the main theorem, preserve the paper/theorem identifiers, explain the specialization to the target setting, then use it. A later verifier can inspect both the citation and the downstream deduction rather than seeing only “by a known result.”

## Key Takeaways

1. Assemble only when the whole target can be addressed.
2. Order supporting results before dependent steps.
3. Preserve the full original theorem statement.
4. Make external dependencies explicit and auditable.
5. Reserve the verified filename for a verifier-passed proof.

## Connects To

- **Ch 5**: retrieval supplies complete statements, context, and source IDs.
- **Ch 9**: the verifier consumes this full markdown proof.

## Source Provenance

Primary source files: `agents/generation/AGENTS.md`, `agents/generation/.agents/skills/verify-proof/SKILL.md`, and the generation runner/output conventions in `agents/generation/tests/run_example.sh`.
