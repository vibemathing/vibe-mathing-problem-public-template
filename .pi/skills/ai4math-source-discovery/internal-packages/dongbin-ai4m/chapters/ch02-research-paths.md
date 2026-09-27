# Chapter 2: Research Paths and Operational Methods

## Core Idea
The guide separates AI4M research into two broad modes: special-purpose tools that expose mathematical structure and general models that solve reusable classes of mathematical tasks. Formal mathematics, especially Lean in the guide's ecosystem, links general reasoning systems to rigorous feedback.

## Frameworks Introduced

### A. Special-purpose data-driven discovery
**When to use**: a hard mathematical project has a concrete subproblem where examples/data can be generated and model-discovered structure can be interpreted mathematically.

**How**:
1. Isolate the mathematical subproblem.
2. Determine what data represents the underlying structure faithfully.
3. Generate or curate the data.
4. Select a model appropriate to the data and signal.
5. Train/evaluate it.
6. Inspect what the model has learned rather than stopping at predictive accuracy.
7. Translate features or regularities into mathematical language.
8. Form a conjecture, invariant, decomposition, or proof direction.
9. Test with mathematics; use formal verification where appropriate.

**Why it works / failure mode**: data can reveal regularities hidden in complex examples, but model success alone may reflect artifacts. Mathematical interpretation is the gate between a machine-learning result and a research insight.

### B. Mathematical digitization → formal reasoning
**When to use**: the goal requires machine-checkable correctness, scalable formal reasoning, rigorous evaluation data, or high-quality verifier feedback.

**How**:
1. Express definitions and the theorem in a formal language.
2. Reuse existing library objects where possible.
3. Search the formal library before reproving routine facts.
4. Use assisted/automatic formalization to reduce translation cost.
5. Run proof search or proof completion.
6. Send candidates to the formal checker.
7. Feed errors/success back into the next search step.

The source recommends Lean because of its ecosystem and mathematician adoption. It also highlights mathlib as the major reusable library and library search as a substantial practical cost.

### C. Semantic formal-library search
**When to use**: formalization time is being consumed by discovering existing lemmas, names, or definitions.

**How**: convert the mathematical intent into a semantic query, find candidate library facts, inspect assumptions/types, and restate the target so it composes with existing library structure. LeanSearch is the guide's representative example; LeanExplorer is mentioned as a related later system.

**Failure mode**: textual similarity can return a nearby but type-incompatible lemma. Always inspect the formal statement.

### D. Autoformalization
**When to use**: translation from ordinary mathematical language to formal statements/proofs is the bottleneck.

**How**: generate candidate formalizations, type-check them, compare semantic content with the source mathematics, repair definitions/assumptions, and iterate. Representative systems/datasets in the guide include work on Isabelle/HOL, ProofNet, multilingual autoformalization, TheoremLlama, Herald, and GAUSS.

**Validation**: a syntactically valid or type-correct artifact can still formalize the wrong theorem. Check semantic fidelity in addition to compilation.

### E. Verifier-guided reasoning
**When to use**: candidate reasoning can be checked by a formal system and repeated feedback is affordable.

**How**: generate a candidate → verify → convert the checker result into a search/training signal → revise → reverify. The guide places early systems such as GPT-f and HyperTree Proof Search, later olympiad systems, and Lean-based provers in this family.

**Why it works**: formal verification supplies precise, scalable feedback during both training and inference.

### F. Agent-first implementation
**When to use**: a capable base model can already solve many local steps, while the complete task needs decomposition, retrieval, proof/tool calls, iteration, and checks.

**How**: define subtasks, provide the necessary mathematical/formal tools, make intermediate artifacts observable, add evaluators/verifiers, set stop conditions, and iterate. The guide cites gold-level olympiad results from agent/model systems as evidence that orchestration can become a strong first option as base models improve.

### G. Evolve-style search
**When to use**: the objective is clear and quantifiable and a decent initial solution already exists.

**How**:
1. encode the candidate solution in a modifiable representation;
2. define a trustworthy score and hard constraints;
3. generate variations;
4. evaluate automatically;
5. retain/improve promising candidates;
6. periodically inspect whether the score still reflects the mathematical goal.

The guide points to AlphaEvolve and open implementations such as OpenEvolve/ShinkaEvolve as examples of this AI-Scientist style.

## Key Concepts
- **Mathematical digitization**: converting ordinary mathematical expression into a formal representation suitable for machine processing and checking.
- **Lean**: the formal language/ecosystem recommended by the guide.
- **mathlib**: Lean's major formalized mathematics library.
- **LeanSearch**: semantic search for mathlib, introduced by the author's team to reduce retrieval friction.
- **autoformalization**: automated or AI-assisted translation from informal mathematics to formal representations.
- **formal verifier**: a checker that accepts or rejects machine-formalized mathematical claims/proofs.
- **FATE / FATE-X**: difficult algebra evaluation sets mentioned as examples of formal or rigorous benchmarking work.
- **REAL-Prover / reap**: the author's team’s Lean-oriented prover and its tactic form for filling proof fragments.

## Landscape Anchors from the Source
Use named systems as examples of method families, not as a fixed leaderboard. The guide references the Awesome AI for Math list and Williamson/DeepMind’s 2021 data-driven mathematics work for special-purpose discovery; Lean/Mathlib, FATE/FATE-X, LeanSearch/LeanExplorer, ProofNet, TheoremLlama, Herald and GAUSS for formalization; GPT-f, HyperTree Proof Search, AlphaProof/AlphaGeometry, Goedel-Prover, Kimina Prover, REAL-Prover/reap, DeepSeek-Prover and Qwen2.5-math for verifier-oriented reasoning; and DeepThink, Aristotle, Seed Prover, AlphaEvolve, OpenEvolve and ShinkaEvolve as agent/evolutionary directions. Because this landscape moves quickly, use the names to locate a method family and verify current status before choosing a system.

## Mental Models
- **Discovery → interpretation → proof**: use models to discover; mathematics to interpret; formal systems to certify when needed.
- **Formalization as instrumentation**: formal representation does more than document a proof; it creates a feedback channel for AI systems.
- **Search before prove**: before generating a new Lean proof, determine whether mathlib already contains the needed fact.
- **Orchestration before retraining**: with a strong base model, test whether agent design unlocks the task before committing to bespoke model training.

## Anti-patterns
- **Predictive accuracy as mathematical insight**: a useful classifier/regressor does not by itself yield mathematics.
- **Natural-language confidence as correctness**: fluent proof prose should not be equated with verification.
- **Formal compilation as semantic fidelity**: an autoformalized statement can compile while encoding the wrong mathematical claim.
- **Repeatedly reproving library facts**: failing to search mathlib wastes formalization effort.
- **Evolve search with a weak score**: optimization amplifies evaluator errors.
- **Agent loops with no checkpoints**: orchestration without observable intermediate tests can consume effort without increasing reliability.

## Reference Table: Route Selection

| Situation | First route | Required check | Common fallback |
|---|---|---|---|
| Need a new pattern/conjecture from examples | special-purpose data-driven tool | mathematical interpretability | redesign data/features; reduce subproblem |
| Need strict proof correctness | Lean + formal verifier | kernel/checker pass | manual proof audit; formalize smaller lemmas |
| Informal theorem is hard to encode | autoformalization | semantic equivalence | manual definitions/assumptions; split statement |
| Lean proof blocked by missing fact/name | semantic library search | type/assumption compatibility | reformulate goal; inspect mathlib hierarchy |
| Multi-step problem with strong base model | agent | intermediate evaluators | decompose further; add formal verifier |
| Objective is measurable and seed exists | evolve loop | evaluator validity | improve score/constraints/seed first |

## Worked Example
Suppose a researcher has a combinatorial quantity with thousands of computable instances and suspects a hidden structural rule. The special-purpose route starts by defining features that preserve the mathematics, training a model to expose regularities, and inspecting which relations consistently matter. A stable relation becomes a candidate conjecture only after it has a mathematical interpretation. If the conjecture can be formalized, the project then switches routes: encode the statement in Lean, search mathlib for prerequisites, use assisted proof generation, and let the verifier decide whether the proof artifact is valid. This staged workflow combines discovery and certification without demanding that one model perform every role.

## Key Takeaways
1. Special-purpose tools are best when a narrow mathematical bottleneck can be represented through data and interpreted by a mathematician.
2. Formal mathematics creates both correctness guarantees and high-quality feedback for AI reasoning.
3. Library search and autoformalization target major practical costs in Lean workflows.
4. Strong base models make agent orchestration a sensible early experiment for many multi-step tasks.
5. Evolve-style methods require a measurable objective and a viable initial candidate.
6. Match validation strength to the claim: correlation, conjecture, informal argument, and formally checked proof are different evidence levels.

## Connects To
- **Ch 1**: uses the learner/task fork to choose a research route.
- **Ch 3**: keeps proof automation subordinate to the broader goal of mathematical understanding.
