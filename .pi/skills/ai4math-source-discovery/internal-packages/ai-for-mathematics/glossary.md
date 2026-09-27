# Glossary

**Actor–Critic** — reinforcement-learning family combining a policy (actor) with a value estimator (critic), balancing direct policy optimization with lower-variance feedback. (Ch 2)

**AlphaEvolve** — LLM-guided evolutionary program-search framework that mutates executable programs, evaluates them automatically, and retains high-quality/diverse candidates. (Ch 3)

**AlphaProof** — neuro-symbolic theorem-proving system combining a learned proof policy/value model, formal proof states, search, and Lean verification. (Ch 4)

**AlphaTensor** — reinforcement-learning system that casts low-rank tensor decomposition for matrix multiplication as a single-player game. (Ch 3)

**Automatic differentiation (AutoDiff)** — exact programmatic differentiation through a computation graph; used by PINNs to obtain PDE derivatives of the neural approximation. (Ch 6)

**CEM / Cross-Entropy Method** — iterative rare-event/optimization method that samples candidates, keeps an elite fraction, and updates the sampling policy toward elite trajectories. (Ch 5)

**CNN** — neural architecture using local connectivity and shared filters; useful when translation/locality are valid structural priors. (Ch 2)

**Counterexample search** — construction task where candidate objects are scored by how strongly they violate a conjectured inequality/property, then independently checked. (Ch 5)

**DPO** — Direct Preference Optimization; preference-training approach that directly fits preferred over dispreferred outputs without a separately trained reward model in the usual RLHF pipeline. (Ch 2)

**Empirical risk minimization (ERM)** — minimizing average loss on observed training samples as a proxy for minimizing unknown population risk. (Ch 2)

**FEM** — Finite Element Method; solves weak/variational forms with local basis functions on meshes, especially effective for complex geometries. (Ch 6)

**FDM** — Finite Difference Method; approximates derivatives on a grid with difference stencils; simple and efficient on regular low-dimensional domains. (Ch 6)

**FVM** — Finite Volume Method; integrates conservation laws over control volumes and balances interface fluxes, preserving discrete conservation. (Ch 6)

**Formal proof state** — machine-readable representation of current goals, hypotheses, and context in a proof assistant; the state on which a proof policy acts. (Ch 4)

**Generalization error** — gap between learned behavior on sampled/training data and performance on unseen examples or unsampled parts of a continuous domain. (Ch 2, Ch 6)

**Gradient clipping** — limits gradient norm to prevent explosive parameter updates in deep/recurrent/Transformer training. (Ch 2)

**GRPO** — Group Relative Policy Optimization; reinforces completions according to their reward relative to other responses sampled for the same prompt, avoiding a separate critic in the described setup. (Ch 2)

**Inductive bias** — architectural or representational constraint encoding assumptions such as locality, symmetry, tensor structure, or separability. (Ch 2, Ch 3, Ch 6)

**Injectivity radius** — geometric quantity measuring a bottleneck scale in a hyperbolic knot complement; one feature relevant in the book's knot-invariant discovery case. (Ch 3)

**Interpretability bridge** — use of feature importance/ablation to convert a successful predictor into a shortlist of mathematical quantities for human synthesis and proof. (Ch 3)

**KAN** — Kolmogorov–Arnold Network family with learnable activation/function components; discussed as an exploratory PINN architecture with potential interpretability/parameter benefits. (Ch 6)

**Kernel trick** — evaluates inner products in an implicit feature space, enabling nonlinear SVM decision boundaries without explicit high-dimensional coordinates. (Ch 2)

**Loss balancing** — setting or adapting coefficients on multiple PINN constraints so PDE, boundary, initial, and data terms contribute usefully to optimization. (Ch 6)

**MDP** — Markov Decision Process, specified by states, actions, transitions, rewards, and discount factor; the mathematical scaffold for sequential RL. (Ch 2)

**MCTS** — Monte Carlo Tree Search; guided search that balances exploration and exploitation using policy priors/value estimates, adapted in theorem and tensor search. (Ch 3, Ch 4)

**PatternBoost** — hybrid construction method alternating local improvement/repair with a Transformer trained on strong constructions to propose globally structured candidates. (Ch 5)

**PCA** — Principal Component Analysis; linear dimensionality reduction maximizing retained variance, equivalently minimizing linear reconstruction error. (Ch 2)

**PINN** — Physics-Informed Neural Network; neural function approximation trained against PDE residuals and boundary/initial/data constraints. (Ch 6)

**Policy network** — model mapping a state to a distribution over actions/tactics; used to guide RL construction or proof search. (Ch 2, Ch 4, Ch 5)

**Proof kernel** — small trusted component of an interactive theorem prover that checks whether formal proof steps obey the logic. (Ch 4)

**Residual-based adaptive sampling** — concentrates PINN collocation points where current PDE residual is large. (Ch 6)

**RLHF** — Reinforcement Learning from Human Feedback; fits preference/reward information and updates a policy while controlling deviation from a reference model. (Ch 2)

**Saliency** — sensitivity/gradient-based feature importance used in the knot example to identify which invariants drive prediction. (Ch 3)

**Soft margin SVM** — support-vector formulation using slack variables and penalty parameter C to trade wider margin against classification violations. (Ch 2)

**Spectral bias** — tendency of ordinary neural networks to learn low-frequency components more readily than high-frequency structure, relevant to PINNs. (Ch 6)

**Spectral method** — global-basis numerical method (e.g. Fourier/Chebyshev) that can converge extremely rapidly for smooth solutions but struggles with discontinuities/complex geometry. (Ch 6)

**Tensor rank decomposition** — expression of a tensor as a sum of rank-one factors; for matrix-multiplication tensors, the rank count corresponds to scalar multiplication count. (Ch 3)

**Transformer** — attention-based sequence architecture with token/position representations, multi-head self-attention, residual paths, normalization, and feed-forward blocks. (Ch 2)

**Universal Approximation Theorem** — existence result showing sufficiently wide neural networks can approximate continuous functions under specified assumptions; it does not guarantee trainability or data efficiency. (Ch 2, Ch 6)

**Value network** — estimator of expected future success/return from a state; used to prioritize promising search branches. (Ch 2, Ch 4)
