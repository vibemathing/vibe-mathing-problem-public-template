# Chapter 4: LeanHammer — Premise Selection plus Automated Reasoning

## Core Idea
A hammer automates tedious local reasoning by selecting a small relevant premise set from a huge library, translating/solving the resulting problem with automation, and reconstructing a proof accepted by the interactive theorem prover. The central bottleneck is often premise selection, not raw prover strength.

## Frameworks Introduced
- **Hammer pipeline**: goal → premise selection → automated reasoning → proof reconstruction → checked proof.
  - When to use: a subgoal looks routine given the right library facts, but the available premise space is too large for naive search.
  - How: gather accessible premises; rank/retrieve a compact candidate set; invoke the prover; reconstruct the result in Lean; verify.
  - Why it works: external automation is far more effective when irrelevant library material is removed.
  - Failure mode: omitting one crucial premise can make a solvable goal look impossible; including too many can explode search.
- **Neural premise selection as retrieval**: embed proof state/query and candidate premises, rank by similarity/learned relevance, then pass top candidates downstream.
  - When to use: the environment has a large standard library plus project-local facts.
  - How: encode state and premises; retrieve top candidates; include local context; optionally combine neural and symbolic selectors; inspect failures and rerank.
- **LeanHammer architecture**: the lecture notes describe premise selection feeding Lean-side automation/external prover components and proof reconstruction, with Aesop-style tree search available to combine attempts.
  - When to use: interactive Lean work where a gap may be closable by reusable automation.
  - How: call the hammer at the current proof state; if it succeeds, retain the reconstructed Lean proof; if it fails, inspect premises and search traces before changing theorem strategy.

## Key Concepts
- **Premise**: a theorem, lemma, definition, or local fact that may help prove the current goal.
- **Premise selection**: reducing a huge available library to a small likely-relevant subset.
- **Retrieval model**: ranks premises for a query/proof state; training can use positive/negative premise pairs and contrastive objectives.
- **ATP**: automated theorem prover used to solve a translated subproblem.
- **Proof reconstruction**: converting an external prover result into a proof object/tactic sequence the original proof assistant accepts.
- **Duper / Zipperposition / Lean-auto / Aesop**: components or search tools associated with Lean hammer-style pipelines; exact deployment is toolchain-specific.
- **Local context adaptation**: retrieving premises newly introduced in the user's project, not just facts seen during model training.

## Mental Models
- **Retrieve before you search**: make the symbolic prover's problem smaller before spending compute.
- **A failed hammer is ambiguous**: it may mean “goal is hard,” “premise missing,” “translation failed,” or “reconstruction failed.” Diagnose the stage.
- **Local premises matter**: real formalization introduces new definitions and lemmas; a selector restricted to global training-era facts will miss them.

## Anti-patterns
- **Library dump**: forwarding thousands of vaguely related facts to the prover.
- **Static-context assumption**: assuming all useful premises were present in training data.
- **Binary failure diagnosis**: treating “hammer failed” as one undifferentiated outcome.
- **Unverified external proof**: trusting the ATP result without successful reconstruction/checking in Lean.

## Reference Table
| Failure point | Evidence to inspect | Corrective action |
|---|---|---|
| Premise selection | retrieved top-k lacks obvious local lemma | add/rerank local context; hybrid selector |
| Translation | selected facts cannot be represented as expected | simplify goal/premises; use Lean-native path |
| ATP search | relevant premises present but timeout | reduce set, change prover/search, decompose goal |
| Reconstruction | ATP succeeds but Lean rejects reconstruction | inspect proof certificate/minimized premises; use alternate reconstruction |
| Tree search | automation solves nearby states but not root | combine hammer calls with structured tactics/Aesop |

## Worked Example
A DSP sketch leaves a subgoal that follows from a project lemma introduced earlier in the file plus a standard arithmetic theorem. Sending the entire library to an ATP wastes search. A hammer-style agent first builds the candidate pool from imported library facts and current-file lemmas, retrieves a small set including the project lemma, runs automation, reconstructs the proof, and checks it in Lean. If the project lemma is missing from top-k, the failure is retrieval-related; increasing tactic sampling elsewhere is misallocated effort.

## Procedure
1. Freeze the exact current goal and local hypotheses.
2. Enumerate accessible premise sources: current theorem context, current file/project, imported libraries.
3. Retrieve/rank candidate premises; ensure newly introduced local facts are eligible.
4. Run the hammer/ATP path and capture stage-specific logs if possible.
5. On success, use the reconstructed Lean proof and re-check the surrounding theorem.
6. On failure, change one stage at a time: premises → search → reconstruction → decomposition.
7. If the goal is strategically hard rather than routine, return it to DSP/Lean-STaR instead of forcing the hammer.

## Key Takeaways
1. Premise selection is the main interface between neural retrieval and symbolic proof automation.
2. Good hammers expose a small trusted surface: selected facts in, reconstructed checked proof out.
3. Context adaptation is essential for user-specific projects.
4. Failure should be attributed to pipeline stage before retry.
5. Use a hammer for local obligations; use higher-level reasoning when the global proof idea is missing.

## Connects To
- **Ch 3**: hammers close formal-sketch gaps.
- **Ch 5**: miniCTX explains why local/cross-file context selection becomes central in real repositories.
