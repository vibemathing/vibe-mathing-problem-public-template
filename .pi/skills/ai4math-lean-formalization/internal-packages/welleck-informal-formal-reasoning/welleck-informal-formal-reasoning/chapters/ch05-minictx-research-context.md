# Chapter 5: Research-Level Formalization — LLMLean, miniCTX, and Long Context

## Core Idea
Research-level theorem proving differs from isolated benchmark problems because the theorem may depend on new definitions, lemmas, comments, file structure, and cross-file project context unseen during training. miniCTX turns this into an explicit evaluation target: proving with novel, long context.

## Frameworks Introduced
- **Context-first proving**: construct the dependency context before treating the current proof state as sufficient.
  - When to use: the target comes from a real Lean repository, recent mathlib, a textbook formalization, or a project with custom definitions.
  - How: collect preceding file content and imports; identify definitions/lemmas the theorem can legally use; rank the most relevant context; make it available to the prover/search loop.
  - Why it works: miniCTX baselines show that conditioning on preceding context can outperform state-only approaches in context-dependent settings.
  - Failure mode: indiscriminately dumping long files can bury useful dependencies and waste model context.
- **Blueprint + dependency graph**: the lecture's manual research-level workflow begins with an informal blueprint and an explicit graph of definitions, lemmas, and theorems to formalize.
  - When to use: large formalization projects where the target theorem sits inside a network of prerequisites.
  - How: write the high-level theorem plan, enumerate prerequisite nodes, topologically order missing formalizations, and verify each node before using it downstream.
- **miniCTX evaluation frame**: test theorem provers on real projects with context that can be new and long, including future mathlib and other recent sources.
  - When to use: evaluating whether a system can transfer beyond self-contained competition benchmarks.
  - How: ensure the target's required context was not trivially present in training; expose repository context; measure verified proving success.
- **LLMLean interface idea**: keep the interface between Lean and a language model simple enough to work with local models and interactive experimentation.
  - When to use: prototyping theorem-proving agents without depending on a closed, expensive end-to-end system.

## Key Concepts
- **In-file dependency**: a definition/lemma available earlier in the same file.
- **Cross-file dependency**: a relevant fact imported from elsewhere in the project/library.
- **Novel context**: facts not seen during model training but available in the current repository.
- **Long context**: repository material spanning many thousands of tokens.
- **Future mathlib**: miniCTX-style evaluation using theorems added after a time cutoff to reduce training overlap.
- **Context selection**: choosing the subset of available project material most useful for the current theorem.
- **Benchmarking gap**: strong results on self-contained problems can fail to predict real repository performance.

## Mental Models
- **A theorem lives in a repository, not a vacuum**: treat file structure and local declarations as part of the problem instance.
- **Dependency discovery precedes tactic search**: if the needed lemma is absent from the model's view, sophisticated search still cannot use it.
- **Measure transfer under novelty**: evaluation should include context introduced after training or in unseen projects.

## Anti-patterns
- **Competition-benchmark overconfidence**: assuming miniF2F/IMO-style success implies research-project success.
- **Context dump**: giving the model the entire repository without relevance filtering.
- **Hidden dependency**: using a theorem unavailable at the target source location or only introduced later.
- **Closed-system dependency**: designing a workflow that cannot run locally or cannot expose intermediate states/debugging signals when accessibility matters.

## Reference Table
| Context source | Why it matters | Common mistake |
|---|---|---|
| Current proof state | immediate goals/hypotheses | treating it as complete world state |
| Earlier file content | local definitions and helper lemmas | truncating it away |
| Imported project files | reusable domain-specific facts | ignoring cross-file dependencies |
| Library/mathlib | standard theorems | retrieving globally without local facts |
| Informal blueprint | strategic dependency order | losing it during low-level tactic search |

## Worked Example
A theorem in a new Lean project refers to a custom object defined two files earlier and relies on a helper lemma proved near the top of the current file. A state-only model sees the goal's surface syntax but not the explanation and helper fact. The context-first workflow first resolves imports, extracts the custom definition and accessible helper lemma, ranks them with other candidates, and only then begins proof search. If the proof succeeds after context injection, the original bottleneck was context availability, not tactic capability.

## Procedure
1. Record repository/commit or snapshot, target file, theorem location, imports, and Lean version.
2. Build a dependency candidate set from preceding declarations and imported modules.
3. Separate **required** context from merely nearby text; prioritize types, definitions, lemmas, and local notation used by the target.
4. Create a compact context package; preserve exact formal identifiers and signatures.
5. Run proof search with the package; track which premises are actually used.
6. If search fails, test the context hypothesis: add missing dependencies before increasing sampling budget.
7. Formalize prerequisites in dependency order when the target relies on unformalized blueprint nodes.
8. Evaluate with verified success and record whether the model used unseen/new context.

## Failure Recovery
- **Unknown identifier/type mismatch** → context/import/toolchain issue; fix before reasoning.
- **Model suggests theorem unavailable at source point** → enforce temporal/file accessibility.
- **Long prompt degrades behavior** → retrieve/rank smaller context; preserve only relevant declarations plus minimal comments.
- **Competition-tuned prover performs poorly** → treat domain/context adaptation as the hypothesis, not proof difficulty alone.
- **A prerequisite is genuinely absent** → return to blueprint/dependency graph and formalize that node first.

## Key Takeaways
1. Real theorem proving is a context-management problem as well as a search problem.
2. In-file and cross-file dependencies must be first-class inputs.
3. New-context evaluation reveals capabilities hidden by static self-contained benchmarks.
4. Context selection and premise selection are complementary: one builds the available world, the other narrows facts for a subgoal.
5. For research projects, formalize the dependency graph in a valid order instead of attacking the final theorem monolithically.

## Connects To
- **Ch 4**: premise selection acts inside the broader context assembled here.
- **Ch 3**: an informal blueprint can become DSP-style sketches for individual dependency nodes.
