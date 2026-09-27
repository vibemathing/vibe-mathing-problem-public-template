# Operational Patterns

## Mathematical Task Router
**When to use**: At the beginning of an AI-for-math project.

**How**:
1. Classify the goal as discovery, proof, refutation/construction, or numerical/inverse solution.
2. Write an explicit success criterion and verifier.
3. Characterize the search object: vector/features, sequential discrete object, proof state, executable program, or function/PDE field.
4. Choose the method family whose representation and feedback match that object.
5. Define a held-out or independent validation channel before optimization.

**Trade-offs**: Strong routing saves more effort than swapping models late. A poor formalization can make a powerful optimizer systematically solve the wrong problem.

## Prediction → Interpretation → Conjecture → Stress Test
**When to use**: You suspect a relation between mathematical invariants/features and have labeled examples.

**How**:
1. Build multiple datasets with different purposes: systematic/census coverage, broader random/generalization coverage, and deliberately constructed edge cases.
2. Train a supervised predictor on the candidate features.
3. Require strong held-out performance before interpretation.
4. Use saliency/feature ablation to isolate influential variables; retrain on the reduced set.
5. Translate stable features into natural mathematical combinations using domain knowledge.
6. State a precise conjecture.
7. Stress-test on constructed/distribution-shifted examples that were excluded from fitting.
8. Refine when counterexamples expose a missing quantity; escalate survivors to proof.

**Failure recovery**: If explanations vary across seeds/data splits, treat them as unstable clues. If stress tests fail, use the failure to identify the missing geometric/algebraic factor rather than tuning the predictor to hide it.

## TensorGame / Object-Level RL
**When to use**: The mathematical object admits a compact state, discrete action, exact transition, and exact terminal condition.

**How**:
1. Re-express the objective as sequential reduction of a residual object.
2. Make each action a mathematically meaningful elementary component.
3. Define terminal success exactly; reward shorter/cheaper successful trajectories.
4. Train a policy/value model using self-play/search plus synthetic demonstrations when inverse construction is easy.
5. Inject symmetry/basis transformations that preserve the mathematical objective to improve exploration.
6. Verify the final decomposition/construction exactly and translate it back to a human-readable algorithm.

**Trade-offs**: Highly efficient when the game captures the mathematics; expensive to design and narrow in transfer.

## Program Evolution with an Automated Evaluator
**When to use**: A candidate solution can be represented as executable code and scored reliably.

**How**:
1. Provide a seed program with a clearly delimited evolvable region.
2. Define objective tests and correctness guards independently from the mutation model.
3. Maintain an archive of high-scoring *and diverse* programs.
4. Prompt an LLM with selected candidates, evaluation feedback, and task context to propose code changes.
5. Use cascading evaluation: cheap validity/performance filters first, full expensive tests later.
6. Add accepted variants to the archive; iterate until a threshold or budget is reached.
7. Analyze the best program for a mathematical construction/algorithm that can be stated and checked independently.

**Failure recovery**: If programs exploit evaluator holes, expand invariants/tests and replay adversarial cases. If search homogenizes, select for behavioral/structural diversity, not score alone.

## Neuro-Symbolic Formal Proof Search
**When to use**: A theorem can be formalized in a proof assistant and a library contains useful lemmas/tactics.

**How**:
1. Formalize the statement and validate that the formal version matches the intended mathematics.
2. Encode the current proof state for a policy/value model.
3. Use the policy to rank next tactics/steps; execute each candidate inside the proof assistant.
4. Search the proof tree with an exploration/exploitation rule; use value estimates to prioritize states.
5. For AND-style subgoals, focus resources on the lowest-value/hardest remaining subgoal.
6. Feed successful trajectories back into training or retrieval.
7. Accept only a proof that the trusted kernel checks.

**Failure recovery**: Improve formalization and lemma retrieval before scaling search. Curriculum/synthetic formal problems can improve the policy. A correct natural-language sketch remains a hint until formal replay succeeds.

## Deep Cross-Entropy Counterexample Search
**When to use**: A construction can be serialized as T discrete choices and rapidly assigned a scalar violation/quality score.

**How**:
1. Initialize policy π over action sequences.
2. Sample N full candidates and compute exact/robust rewards.
3. Keep the top K = ceil(ρN), typically a small elite fraction.
4. Convert elite trajectories into state-action examples.
5. Minimize cross-entropy on those elite decisions so the policy shifts toward successful motifs.
6. Repeat until an independently verified counterexample is found or the budget ends.
7. Inspect elite structure even on failure; recurring motifs can define a parameterized family for direct analysis.

**Failure recovery**: Collapse indicates insufficient exploration, an overaggressive elite ratio, or a lossy encoding. Add diverse seeds or change representation before merely increasing N.

## PatternBoost: Local Repair + Global Pattern Learning
**When to use**: Good combinatorial constructions have reusable global structure and a competent local improver/constraint repair routine exists.

**How**:
1. Generate or seed feasible candidates.
2. Run local search to repair hard constraints and improve the objective.
3. Serialize strong constructions; train an autoregressive Transformer on the elite dataset.
4. Sample globally structured candidates from the model.
5. Send generated candidates through local repair/improvement and exact scoring.
6. Refresh the elite training set and repeat.
7. Verify any record/counterexample independently.

**Trade-offs**: Local search gives precision; the learned generator jumps between basins. It loses its advantage when high-quality objects have little shared pattern or the local optimizer cannot reliably restore feasibility.

## Generator–Verifier Mathematical Agent
**When to use**: Open-ended candidate generation benefits from LLM reasoning, while correctness can be delegated to a stronger external checker.

**How**:
1. Make the LLM responsible for proposals, decomposition, and repair—not final truth.
2. Use an independent verifier: proof assistant, exact program, CAS, exhaustive checker, or human expert.
3. Return concise, actionable verifier diagnostics to the generator.
4. Preserve failed attempts and their causes to avoid loops.
5. Decompose into subgoals at a level where each can be verified and dependencies remain visible.
6. Synthesize only verified pieces, then run a final whole-object verification.

**Failure recovery**: If the verifier cannot certify the candidate, downgrade the output to a conjectural lead. Repeated identical failures imply the plan or representation should change.

## Classical PDE Method Selector
**When to use**: Before choosing a PINN.

**How**:
- Use **FDM** for regular grids and simple geometry where finite-difference stencils are natural.
- Use **FEM** for complex geometry and variational formulations requiring flexible meshing.
- Use **FVM** for conservation laws, flux balance, shocks, and cases where discrete conservation is central.
- Use **spectral methods** for smooth solutions/simple geometry when high accuracy is needed and dense/global operations are acceptable.
- Consider **PINNs** when high dimensionality, inverse/data-assimilation structure, or meshless geometry makes classical discretization especially awkward.

**Trade-offs**: A neural solver should earn its complexity. Classical methods often provide better accuracy, convergence theory, and baseline verification in their favorable regimes.

## PINN Composite-Loss Workflow
**When to use**: A differential equation and constraints can be differentiated through a neural function approximation.

**How**:
1. Parameterize u(x,t) with a differentiable network.
2. Use AutoDiff to compute the PDE residual.
3. Build `L = λf Lf + λb Lb + λi Li + λd Ld` as applicable.
4. Set initial weights so terms contribute at comparable useful scales; adapt by loss or gradient magnitude if imbalance appears.
5. Sample interior/boundary/initial/data points with independent validation points held out.
6. Optimize with Adam/L-BFGS or staged variants.
7. Increase collocation density and adaptively resample high-residual/rapid-change regions.
8. Check physical invariants and compare with a trusted numerical reference where feasible.

**Failure recovery**: Diagnose approximation, optimization, and generalization/discretization error separately. Use Fourier features, decomposition, hard constraints, regularization/priors, or a hybrid method only when the diagnosed error motivates them.
