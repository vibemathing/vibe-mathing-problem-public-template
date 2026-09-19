# Chapter 4: AI for Proving Mathematical Theorems

## Core Idea
The most reliable modern route to AI theorem proving combines **learned intuition for search** with **symbolic/formal verification for rigor**. A language or policy model proposes promising proof actions, while an interactive theorem prover (ITP) executes them and a small trusted kernel certifies the final proof.

## Frameworks Introduced

### Neuro-Symbolic Proof Search
- **When to use**: The target theorem can be expressed in a proof assistant and useful library context is available.
- **How**:
  1. Formalize the statement and supporting definitions.
  2. Represent the current proof state (goals, hypotheses, context) as model input.
  3. Use a learned policy/LLM to generate candidate tactics or proof steps.
  4. Execute candidates inside the formal environment; invalid actions are rejected immediately.
  5. Use search guided by policy priors and a value estimate to allocate computation across branches.
  6. Treat multiple subgoals as an AND structure: all must close. Give special attention to the lowest-value/hardest subgoal because it bottlenecks the proof.
  7. Accept the result only when the proof kernel checks the complete term/script.
- **Why it works**: Learned models provide heuristic direction in an enormous logical search tree; the proof assistant prevents probabilistic fluency from becoming logical authority.

### Math-LLM Capability Pipeline
- **When to use**: Building/adapting a model whose role is mathematical reasoning or tactic generation.
- **How**:
  1. Pretrain on broad text/code/mathematics to learn syntax and common structures.
  2. Supervised fine-tune on instruction/reasoning/proof traces.
  3. Apply reinforcement learning with an objective rule-based reward where possible: answer equality, executable tests, or formal proof acceptance.
  4. Use test-time compute/search for hard items rather than relying on one-shot sampling.
- **Boundary**: Correctness rewards are easy to define relative to novelty, taste, or theory-building. Optimizing verifiable correctness does not solve creativity evaluation.

### AlphaProof-Style Training/Search Loop
- **When to use**: Competition-level or difficult formal theorem search with many candidate tactics.
- **How**:
  1. Train a proof network on formal state→tactic data from a library such as Mathlib.
  2. Use its policy to propose tactics and its value head to estimate future proofability.
  3. Search with an MCTS-like algorithm balancing policy-guided exploitation and unexplored branches.
  4. Execute every edge in Lean; failed tactics do not create valid child states.
  5. Backpropagate search outcomes to improve estimates.
  6. Expand data by automatically formalizing large amounts of natural-language mathematics, then prioritize promising formal problems.
  7. Feed successful trajectories back into training; on exceptionally hard problems, use test-time training/search focused on the single target.

### Research-Agent Loop
- **When to use**: Research questions require literature retrieval, long-horizon planning, computation, and repeated self-correction beyond a single formal theorem state.
- **How**:
  1. Plan and decompose the question.
  2. Retrieve potentially relevant literature/results, including obscure or cross-language sources.
  3. Use extended test-time reasoning and tools for symbolic/numerical checks.
  4. Generate candidate arguments/constructions.
  5. Verify each critical step using external tools or formal systems where possible.
  6. Revise from failures and synthesize a final research artifact.
- **Boundary**: A research agent can surface a previously published solution or produce a coherent manuscript; novelty and correctness still require independent review/certification.

## Key Concepts
- **Interactive theorem prover (ITP)**: environment in which a user/agent applies tactics while a trusted kernel checks logical validity.
- **Mathlib/formal library**: structured machine-readable body of definitions and proved theorems that supplies retrieval and training data.
- **Proof policy**: distribution over next tactics/actions conditioned on the current state.
- **Proof value**: estimate of a state's probability/proximity to eventual proof success.
- **Formalization**: translation of informal mathematical language into explicit types, definitions, hypotheses, and theorem statements.
- **Automated formalization**: model-assisted generation of formal statements/problems at scale; useful for creating training/search material but requires consistency/quality control.
- **Test-time compute**: additional search, sampling, verification, or even target-specific learning performed while solving a particular problem.
- **Aletheia**: LLM-based research-agent example described as combining deep reasoning, extended test-time computation, and tool use for research-level mathematical tasks.
- **DeepMath-Creative**: benchmark framing mathematical creativity along dimensions including new concepts, new methods, and new examples/constructions.

## Mental Models

### Learned Intuition + Mechanical Rigor
Model output functions like a mathematician's hunch about which tactic might work; the formal kernel functions like an uncompromising referee that checks every logical step.

### Proof as Bottlenecked AND-Search
If a tactic creates several subgoals, success requires all branches. A single hard subgoal can dominate total difficulty, so average progress can mislead. Prioritize the bottleneck rather than expanding already-easy branches.

### Formal Libraries as Executable Knowledge
A theorem library is both a knowledge base and an environment whose entries can be composed and machine-checked. Retrieval quality can matter as much as generative model scale.

### Creativity Is Not the Same Objective as Correctness
Formal proof acceptance provides a crisp reward. Mathematical novelty, elegance, depth, and long-term value are contextual and often delayed. Treat claims about creativity as a separate evaluation problem.

## Failure Modes and Recovery

### Formalization mismatch
**Signal**: The agent proves the formal theorem but the formal statement omitted an intended assumption or encoded the wrong concept.
**Recovery**: Review the statement with domain experts, test simple known cases/counterexamples, and compare with the natural-language intent before celebrating proof success.

### Sparse proof reward
**Signal**: Nearly all trajectories return zero because only complete proofs receive reward.
**Recovery**: Improve policy imitation, curriculum, lemma retrieval, value learning, search, and synthetic/formal problem generation. Avoid arbitrary intermediate rewards that can be gamed unless they preserve logical intent.

### Search explosion
**Signal**: Huge branching tree with little depth/progress.
**Recovery**: sharpen tactic priors, retrieve relevant lemmas, normalize/compact states, prioritize hard subgoals, and use a stronger value estimator or problem-specific fine-tuning.

### Conservative reward optimization
**Signal**: System produces long safe variants of familiar proofs and avoids novel routes.
**Recovery**: Separate correctness from novelty evaluation. Use diversity/search objectives for exploration while retaining proof-kernel acceptance as the final correctness gate.

### Literature rediscovery mistaken for novelty
**Signal**: A research agent “solves” an open problem but the argument matches a hard-to-find prior publication.
**Recovery**: perform explicit literature search and provenance comparison before making novelty claims. Rediscovery may still be valuable as retrieval/knowledge-integration success.

## Anti-patterns
- **Natural-language proof accepted on style**: fluent derivations can hide gaps; require formal or expert verification when rigor matters.
- **Rewarding length/difference as creativity**: superficial dissimilarity from common proofs can incentivize verbosity or errors.
- **Treating proof search and theorem formulation as the same task**: a perfectly solved formal statement can still formalize the wrong theorem.
- **Ignoring library bottlenecks**: model reasoning cannot invoke lemmas that are unavailable, badly encoded, or unretrieved.
- **Calling correctness “creativity”**: verifiable solution success is only one dimension of mathematical research ability.

## Reference Table: Proof-System Responsibilities
| Component | Primary job | What it must not be trusted to do alone |
|---|---|---|
| LLM/policy | propose tactics, plans, formalizations | certify logic |
| Value model | prioritize states/subgoals | decide theorem truth |
| Search | allocate compute and combine actions | repair a wrong formal statement |
| ITP executor | apply tactics under formal semantics | judge informal relevance/novelty |
| Kernel | final logical checking | discover proof strategy |
| Human/domain reviewer | verify intent, meaning, novelty, value | exhaustively search proof trees at scale |

## Worked Example
Given an olympiad-style theorem to prove in Lean:
1. formalize variables, domains, hypotheses, and conclusion;
2. run small examples to confirm the statement matches the intended problem;
3. retrieve relevant Mathlib lemmas;
4. ask the proof policy for candidate tactics;
5. execute each candidate in Lean and build a search tree only from valid successor states;
6. assign high compute to the hardest remaining subgoal;
7. continue until all branches close;
8. replay the final script from a clean environment;
9. separately explain the proof idea in human mathematics, preserving the formal proof as the certificate.

If the system cannot close the proof, the best partial tree can still reveal which lemma/subproblem is the true bottleneck; report that rather than hallucinating a final step.

## Key Takeaways
1. Learned models are most dependable as heuristic guides inside a formally checked loop.
2. The theorem statement/formalization itself needs validation before search.
3. Policy, value, search, executor, and kernel have distinct responsibilities.
4. Hard-subgoal prioritization is important in proof trees where every branch must close.
5. Objective verification enables strong RL/test-time search, but novelty and mathematical taste remain difficult to reduce to scalar rewards.
6. Research agents broaden the workflow to planning/retrieval/tools; their outputs need provenance and independent checking.

## Connects To
- **Ch 2**: supplies Transformers, RL, SFT/RLHF/GRPO, and evaluation principles.
- **Ch 3**: shares policy/value search and exact evaluator ideas.
- **Ch 5**: generator–verifier agents use the same division between creative proposals and rigorous checking.
