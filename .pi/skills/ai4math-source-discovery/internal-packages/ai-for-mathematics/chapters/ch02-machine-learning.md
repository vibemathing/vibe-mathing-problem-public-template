# Chapter 2: Introduction to Machine Learning

## Core Idea
Machine learning for mathematics should be decomposed into **data/representation, model, and algorithm**, then evaluated on unseen cases. The chapter provides the technical vocabulary needed by the research workflows in later chapters: linear models, optimization, neural architectures, reinforcement learning, generative models, Transformers/LLMs, and engineering practices.

## Frameworks Introduced

### Data–Model–Algorithm Decomposition
- **When to use**: To diagnose or design any learning system.
- **How**:
  1. Define data and representation: inputs, targets, invariances, noise, and train/validation/test partition.
  2. Define a hypothesis/model family `f(x; θ)` whose inductive bias matches the data.
  3. Define a loss/reward and algorithm that changes `θ` using observed examples/interactions.
  4. Measure generalization rather than training fit.
- **Why it works**: Failures often originate in representation or evaluation rather than model capacity.

### Train–Validation–Test Discipline
- **When to use**: Any empirical claim about a learned method.
- **How**: optimize parameters on training data; tune hyperparameters/model choices on validation data or cross-validation; expose the test set only after choices are fixed. Preserve specially constructed stress cases as a further out-of-distribution check where appropriate.
- **Failure mode**: Repeated test-set inspection turns the test set into training feedback and invalidates the claimed generalization estimate.

### Reward-Driven Sequential Search
- **When to use**: Decisions affect future states and the desired object emerges through a sequence of actions.
- **How**: define the MDP `(S, A, P, R, γ)`, then choose value-based, policy-gradient, or actor–critic methods according to action space and optimization needs. Reward design must encode the real goal because the agent will optimize whatever is measurable.

### LLM Capability Pipeline
- **When to use**: Understanding or adapting a language model for mathematical reasoning.
- **How**:
  1. **Pretraining** learns broad statistical/language/code structure through next-token prediction.
  2. **Supervised fine-tuning (SFT)** teaches instruction-following and worked reasoning formats.
  3. **Preference/RL training** further aligns outputs with correctness or preference signals using approaches such as RLHF, DPO, or GRPO.
  4. Use external execution/verifiers where mathematical rewards can be made objective.
- **Boundary**: More reward optimization does not automatically produce creativity when novelty/taste cannot be captured by the reward.

## Key Concepts

### Linear and classical learning
- **Linear regression**: fits continuous targets under a linear model, commonly with squared loss.
- **Perceptron**: iteratively updates a linear classifier when examples are misclassified; finite convergence requires linear separability, and the resulting separator depends on data order and is not margin-optimal.
- **SVM**: maximizes classification margin; soft-margin slack/C handles nonseparable data; kernels introduce nonlinear boundaries implicitly.
- **PCA**: projects centered data onto leading covariance eigenvectors; maximizing retained variance is equivalent to minimizing linear reconstruction error.
- **K-means**: alternates assignment to nearest centers and center recomputation; useful as a simple unsupervised grouping model.

### Optimization and evaluation
- **Batch GD** uses all samples per update; stable but expensive.
- **SGD** uses one sample; cheap/noisy and can explore, but has high variance.
- **Mini-batch** balances throughput and noise.
- **Momentum** accumulates a velocity-like moving average of gradients; `β≈0.9` is a common starting cue in the text.
- **Adam** combines first/second gradient moments and bias correction to adapt effective learning rates per parameter.
- **Learning-rate scheduling**, initialization, normalization, clipping, regularization, dropout, curriculum, and early stopping shape trainability/generalization.

### Neural architectures and inductive bias
- **Logistic/Softmax regression** provide probabilistic classification via cross-entropy.
- **MLP**: flexible global function approximator; universal approximation is an existence guarantee and does not guarantee learnability or sample efficiency.
- **CNN**: locality + shared filters + hierarchical features; strong for grid/local translation structure.
- **RNN/LSTM/GRU**: sequence memory; recurrent designs address temporal dependencies but face gradient and parallelism issues.
- **Transformer**: self-attention provides direct long-range interaction; multi-head attention learns different relation subspaces; residuals, normalization, and feed-forward layers form blocks.

### Generative models
- **GANs** learn through adversarial generator/discriminator competition and can give sharp samples but suffer unstable training/mode collapse.
- **Diffusion models** learn reverse denoising from Gaussian-corrupted data; training is stable/diverse, with slower iterative sampling as a trade-off.
- For mathematical work, the practical lesson is to distinguish **candidate generation** from **candidate verification**.

## Mental Models

### Inductive Bias as Search-Space Compression
Use an architecture when its built-in assumptions remove implausible functions while preserving the target. CNN locality, tensor symmetries, program structure, and separability are all forms of search-space compression.

### Empirical Risk Is a Proxy
Treat low training loss as evidence about sampled data only. The object of interest is expected/generalization performance, which requires honest held-out evaluation.

### Reward as a Baton
In RL, reward design directs the entire search. If validity, cost, or mathematical constraints are absent from the environment/checker, the policy can optimize a shortcut unrelated to the intended mathematics.

## Engineering Procedure

### Data preparation for mathematical models
1. Normalize symbolic formats and LaTeX conventions.
2. Remove noise, duplicates, OCR artifacts, and irrelevant web boilerplate.
3. Select a representation preserving mathematical structure.
4. Use augmentation that respects true symmetries/equivalences; e.g. transformations that preserve the underlying problem should alter surface form without changing labels.
5. For SFT, include explicit reasoning/process examples when the goal requires intermediate reasoning.

### Initialization and training control
- Prefer Xavier-like initialization for saturating activations and He-like initialization for ReLU families; use orthogonal initialization where useful for recurrent stability.
- Clip exploding gradients by norm rather than allowing a single update to destabilize the run.
- Use curriculum when the target distribution contains very hard cases and easier examples can teach reusable structure first.
- Use L1/L2, dropout, or early stopping according to the failure mode. Early stopping monitors validation performance and halts before optimization starts fitting training-specific noise.

### LLM math training checks
- Keep mathematical corpora clean and deduplicated.
- In RL stages, prefer objective executable/formal rewards when available.
- Constrain policy drift from an SFT/reference policy when using RLHF-style optimization.
- In GRPO-style sampling, compare multiple responses for the same prompt and reinforce above-group-average outcomes; the signal depends entirely on the quality of the reward/checker.

## Anti-patterns
- **Universal-approximation overclaim**: citing existence theory as evidence the selected network can be trained accurately with available data.
- **Unprotected test set**: repeatedly tuning on test outcomes.
- **Representation agnosticism**: using raw encodings that erase symmetry/topology and hoping model size repairs it.
- **Reward misspecification**: optimizing a proxy whose loopholes are easier than the mathematics.
- **All engineering knobs at once**: changing optimizer, architecture, data, and regularization simultaneously, making failure diagnosis impossible.
- **Assuming generative fluency equals correctness**: generation quality should be decoupled from mathematical validation.

## Reference Tables

### Model/method selection
| Need | First candidate | Main reason | Main caution |
|---|---|---|---|
| interpretable linear separation | SVM/logistic | explicit boundary/probabilities | nonlinear structure may need features/kernel |
| unsupervised linear compression | PCA | optimal linear reconstruction/variance retention | nonlinear manifolds not captured |
| image/grid locality | CNN | local/shared inductive bias | awkward irregular geometry |
| sequential state | RNN/LSTM/GRU | temporal recurrence | optimization/parallelism |
| long-range sequence dependencies | Transformer | direct attention paths | compute/memory cost |
| discrete sequential optimization | value/policy/actor–critic RL | learns action policy from reward | reward and exploration are hard |

### Optimizer cues
| Method | Strength | Weakness |
|---|---|---|
| Batch GD | stable direction | full-dataset cost |
| SGD | cheap/noisy exploration | high update variance |
| Mini-batch | hardware-efficient compromise | batch-size tuning |
| Momentum | accelerates consistent directions, damps oscillation | adds state/hyperparameter |
| Adam | adaptive per-parameter scaling, robust default | good training loss does not guarantee best generalization |

## Worked Example
For a mathematical classification task where the model predicts an algebraic invariant from geometric features:
1. split examples into train/validation/test and keep a separately constructed stress set;
2. standardize continuous features and preserve meaningful geometric components;
3. establish linear/logistic baselines before a deeper MLP;
4. train with mini-batch optimization and validation-based early stopping;
5. report held-out performance;
6. only then apply feature-importance/ablation analysis;
7. retrain on the reduced features to check whether the explanatory signal survives.

This turns Chapter 2's generic ML discipline into the foundation for Chapter 3's discovery workflow.

## Key Takeaways
1. Data/representation, model, and algorithm must be diagnosed separately.
2. Generalization requires a clean evaluation protocol.
3. Architecture should encode useful mathematical structure where possible.
4. RL succeeds or fails with state/action/reward design before it succeeds or fails with optimizer details.
5. LLM mathematical capability is staged: broad pretraining, task-form learning, then reward/preference optimization.
6. Engineering controls are part of the method; they should address observed failure modes rather than serve as ritual.

## Connects To
- **Ch 3**: supervised interpretability, RL, Transformers, and program search use these foundations.
- **Ch 4**: LLM/RL and policy/value models guide formal proof search.
- **Ch 5**: cross-entropy/RL and Transformer generation drive construction search.
- **Ch 6**: neural approximation, AutoDiff-compatible optimization, loss balancing, and generalization all reappear in PINNs.
