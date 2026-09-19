# Chapter 1: Overview

## Core Idea
Mathematical research can be organized around a loop of **discovery, proof, and refutation**. Each activity contains a search problem: find meaningful structure, find a valid proof path, or find a candidate violating a conjecture. AI becomes useful when the scale, dimension, or branching factor overwhelms ordinary human search, while mathematical judgment remains responsible for formulation, interpretation, and certification.

The chapter's control principle is **Mathematical Problem → Suitable AI Technology → Specific Implementation Process**. Keep that order when designing any AI-for-math project.

## Frameworks Introduced

### Discovery–Proof–Refutation Loop
- **When to use**: To identify what kind of help an AI system should provide.
- **How**:
  1. **Discovery**: search examples/data for regularities that might deserve a definition, conjecture, or construction.
  2. **Proof**: search a logical space of definitions, lemmas, tactics, and deductions for a certified path.
  3. **Refutation**: search candidate objects under constraints for one that violates the proposed general statement.
  4. Feed outcomes around the loop: counterexamples refine conjectures; proof obstacles suggest new concepts; discovered patterns produce new proof/refutation targets.
- **Why it works**: It converts the vague question “How can AI help mathematics?” into distinct search structures with different verifiers and representations.

### Problem-First AI Selection
- **When to use**: Before choosing a model, benchmark, or training recipe.
- **How**:
  1. State the mathematical bottleneck in domain language.
  2. Specify what output would change mathematical knowledge or practice.
  3. Identify why human/manual methods struggle: combinatorial explosion, high dimension, long formal chains, data volume, or numerical cost.
  4. Choose AI machinery targeted at that bottleneck.
  5. Define how output will be interpreted and verified before optimization begins.
- **Failure mode**: Starting from a fashionable model and searching for a mathematical use case produces demos whose scores have little mathematical meaning.

### Human–AI Division of Labor
- **When to use**: When assigning responsibility in a research workflow.
- **How**: Use machines for large-scale search, high-dimensional pattern detection, repeated evaluation, and formal checking. Use human/domain reasoning for defining valuable questions, selecting representations, creating concepts, interpreting repeated structures, and deciding which results deserve proof.
- **Validation**: The final artifact should be readable as a mathematical proposition, construction, proof, or numerical result rather than as an unexplained model score.

## Key Concepts
- **Discovery**: extracting a mathematically meaningful hypothesis or structure from examples or phenomena.
- **Proof**: converting a conjectural statement into a deductively certified result.
- **Refutation**: establishing failure of a universal claim by constructing a valid counterexample.
- **Search space**: candidate patterns, proof paths, or mathematical objects over which exploration occurs.
- **Neuro-symbolic integration**: combining learned heuristic guidance with a symbolic/formal checker.
- **Formal verification**: checking proof steps in a trusted logical system such as Lean, Coq, or Isabelle.
- **Human–machine collaboration**: assigning exploration and checking tasks according to their comparative strengths rather than assuming full automation.
- **Reproducibility**: preserving enough data, code, model, parameters, and procedure for others to independently repeat a computational result.

## Mental Models

### AI as a Search Amplifier
Use this model when the candidate space is too large or unintuitive for manual exploration. The model's value is its ability to prioritize regions of a search space, not an automatic right to declare truth.

### Verifier as Epistemic Boundary
Use this model whenever a learned system generates a mathematical claim. The generator can be probabilistic and creative; the boundary between “candidate” and “accepted result” should be governed by a stronger independent check when available.

### Cognitive Map Before Tooling
Think of AI-for-math as a map connecting mathematical objectives to representations, search algorithms, and validators. If one of these links is missing, implementation should pause for reformulation rather than hide the gap under more compute.

## Anti-patterns
- **Technology-first problem selection**: choosing a neural architecture before identifying the mathematical bottleneck. It optimizes technical novelty rather than mathematical value.
- **Model output as conclusion**: treating a high probability/reward as proof. Learned scores are evidence for search prioritization only.
- **Opaque irreproducibility**: reporting AI-assisted results without enough code/data/model/evaluation detail for independent checking.
- **Replacement framing**: designing the workflow around eliminating mathematicians. The book repeatedly frames productive systems as combinations of machine search/checking and human formulation/interpretation.
- **Ignoring new epistemic questions**: AI-generated conjectures/proofs create issues of attribution, verification, trust, and research education that should be handled explicitly.

## Worked Example
Suppose a researcher has millions of structured mathematical objects with computed invariants and suspects an unknown relation. The chapter's logic yields this plan:

1. **Problem**: discover a stable relation among invariants, not merely predict one invariant.
2. **Bottleneck**: the joint feature space is too high-dimensional for reliable human visualization.
3. **AI role**: train a predictor to test whether the information needed for one invariant appears in the others and use interpretability to identify candidate variables.
4. **Human role**: translate important variables into a natural mathematical expression or conjecture.
5. **Verifier role**: stress-test on deliberately constructed examples, then prove or refute the precise statement.

A model that predicts well but yields no stable mathematical formulation is useful exploratory evidence, yet it has not completed the research loop.

## Key Takeaways
1. Route every AI-for-math task through a clear mathematical objective first.
2. Discovery, proof, and counterexample construction require different search spaces and verification mechanisms.
3. AI is strongest where high dimension, scale, or branching defeats unaided intuition.
4. A probabilistic model can guide exploration while a formal/exact component protects rigor.
5. Reproducibility and independent verification become more important as model autonomy increases.
6. Education for AI-assisted mathematics should emphasize formulation, judgment, verification, and cross-domain connections, not only model operation.

## Connects To
- **Ch 2**: supplies the machine-learning primitives used by the later research workflows.
- **Ch 3**: operationalizes discovery as prediction, interpretation, and search.
- **Ch 4**: operationalizes proof as neuro-symbolic search with formal checking.
- **Ch 5**: operationalizes refutation as candidate construction plus verification.
- **Ch 6**: shows the same problem-first principle when choosing classical solvers versus PINNs.
