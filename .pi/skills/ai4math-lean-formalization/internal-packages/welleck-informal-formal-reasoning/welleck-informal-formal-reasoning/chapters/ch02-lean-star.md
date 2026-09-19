# Chapter 2: Lean-STaR — Learning to Interleave Thinking and Proving

## Core Idea
Lean-STaR augments formal proof generation with informal thoughts before each tactic. The thought supplies strategic information missing from proof code; Lean supplies hard feedback on the tactic. Training is bootstrapped from retrospectively generated thoughts and improved by expert iteration on verified successful proofs.

## Frameworks Introduced
- **Lean-STaR**: generate an informal thought, then a formal tactic, then verify; repeat until the proof closes or the search budget ends.
  - When to use: the next tactic is difficult to choose from the proof state alone and intermediate strategic reasoning could help.
  - How: (1) summarize the state and intended mathematical move; (2) generate a tactic conditioned on both state and thought; (3) run Lean; (4) keep successful transitions; (5) branch/backtrack on failure.
  - Why it works: formal proofs omit much of the reasoning humans use to choose the next step; synthetic thoughts can expose that latent information to the model.
  - Failure mode: verbose thoughts can become decoration if they do not change action selection or track the actual proof state.
- **Retrospective thought initialization**: use known correct tactics to synthesize plausible preceding thoughts, then fine-tune a model on thought+tactic sequences.
  - When to use: building a training set where formal traces exist but informal reasoning traces do not.
  - How: condition on the state and ground-truth next action, generate the thought that could motivate it, then train the model to produce thought before action at inference.
- **Expert iteration / online self-improvement**: sample candidate proofs, verify them, add successful trajectories to training data, and retrain.
  - When to use: a verifier can label complete trajectories cheaply relative to human annotation.
  - How: sample → verify → filter successes → update dataset/model → repeat until stopping criterion.

## Key Concepts
- **Chain-of-thought augmentation**: adding informal intermediate reasoning before formal actions.
- **Pass@k**: success when at least one of k sampled attempts verifies; Lean-STaR's paper reports improvement on miniF2F under sampling.
- **Parallel proof sampling**: explore multiple complete/partial proof trajectories instead of relying solely on one globally scored frontier.
- **Backtracking**: return to an earlier accepted proof state after a later tactic fails.
- **Search budget**: number of sampled trajectories, steps, or verifier interactions allocated to the theorem.
- **miniF2F**: a standard formal mathematics benchmark used in the Lean-STaR evaluation.

## Mental Models
- **Think, act, check**: the informal thought is a proposal for why an action should work; Lean immediately tests the formal action.
- **Verifier-grounded self-training**: only trajectories that actually verify deserve promotion into expert data.
- **Prefer branchable search when scores are unreliable**: the lecture notes report difficulty scoring thought/action pairs with best-first search, motivating parallel generation plus backtracking/retry.

## Anti-patterns
- **Scoring fiction**: assigning precise global scores to thought/action pairs when the score is not calibrated to proof completion.
- **Thought-state drift**: continuing an informal plan after Lean has changed the formal obligations in a way that invalidates the plan.
- **Failure repetition**: sampling near-identical tactics from the same state without changing thought, branch, premises, or context.
- **Training on unverified self-output**: expert iteration depends on verifier-filtered successes; accepting unverified trajectories destroys the signal.

## Reference Table
| Stage | Input | Output | Gate |
|---|---|---|---|
| Retrospective initialization | proof state + known tactic | synthetic preceding thought | consistency with known tactic/state |
| Inference step | current state | thought + tactic | Lean accepts tactic |
| Search | accepted states + remaining budget | alternate trajectories | proof closes or branch pruned |
| Expert iteration | sampled trajectories | new training examples | only verified proofs retained |

## Worked Example
A theorem stalls after several accepted steps. The current state contains a nonlinear equality and a positivity hypothesis. A Lean-STaR-style agent first records a compact thought such as “normalize the equality; positivity should discharge the sign case,” then proposes the corresponding tactic. If Lean rejects it because normalization exposes an unmet side condition, the agent records that exact state, backs up, and tries a branch that proves the side condition first. The new branch is judged by Lean, not by whether the prose sounded convincing.

## Failure Recovery
1. **Tactic rejected immediately** → regenerate from the same state with a changed mathematical move, not just paraphrased syntax.
2. **Many branches die late** → add earlier state checks or split the proof into higher-level subgoals; consider DSP.
3. **All branches need an unknown lemma** → switch to premise retrieval/LeanHammer.
4. **The state lacks project definitions needed to reason** → load repository context; switch to miniCTX-style workflow.
5. **A proof verifies but is unreadable or bloated** → stop generation search and route to proof optimization.

## Key Takeaways
1. Insert informal reasoning exactly where it can influence a formal action.
2. Let formal verification filter both search and self-training data.
3. Increase search budget only when the sampling process explores meaningful diversity.
4. Backtracking is valuable because tactic failure is local; it need not invalidate earlier verified states.
5. If the bottleneck is missing premises or long context, more tactic sampling attacks the wrong problem.

## Connects To
- **Ch 1**: instantiates the proof-state/tactic verifier loop.
- **Ch 3**: DSP raises reasoning from per-tactic thoughts to whole-proof sketches.
- **Ch 4**: premise retrieval supplies facts that thought+tactic generation may lack.
