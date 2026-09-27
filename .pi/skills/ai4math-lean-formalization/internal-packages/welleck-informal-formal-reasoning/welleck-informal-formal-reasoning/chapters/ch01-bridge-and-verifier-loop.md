# Chapter 1: Bridging Informal and Formal Reasoning

## Core Idea
The lecture frames AI-for-mathematics as a bridge between two complementary representations: informal reasoning is expressive and useful for planning, while formal reasoning is granular and mechanically verifiable. Effective systems move between them instead of forcing one representation to do every job.

## Frameworks Introduced
- **Proof-state → tactic loop**: treat interactive theorem proving as repeated state transition.
  - When to use: whenever an agent works inside Lean or a similar proof assistant.
  - How: read the current goal and local context, propose one tactic, run the verifier, then continue from the returned proof state.
- **Informal/formal bridge**: use natural-language mathematical reasoning to provide information absent from proof code, but keep the formal system as the validity gate.
  - When to use: when a model has strategic insight that is difficult to express directly as low-level tactics.
  - How: express the intended logical move informally, map it to a formal action or subgoal, verify, and retain only verifier-consistent progress.

## Key Concepts
- **Informal reasoning**: human-style mathematical explanation, intuition, decomposition, and planning that may omit mechanically required details.
- **Formal reasoning**: theorem statements and proof terms/tactics accepted by a proof assistant under explicit definitions and dependencies.
- **Proof state**: the current formal obligations plus local hypotheses/context.
- **Tactic**: an action that transforms a proof state, ideally reducing or closing obligations.
- **Verifier feedback**: the proof assistant's acceptance, rejection, error, or next state; the most reliable local signal in the workflow.
- **Neural theorem proving**: using a learned model to propose proof actions, often searched over with verifier feedback.

## Mental Models
- **Use two representations for two jobs**: let informal language carry strategy; let formal language carry correctness.
- **Think of a verifier as a transition oracle**: it tells you which formal moves are legal, not which strategy is globally best.
- **Treat an error as state information**: a failed tactic narrows the branch; it does not justify repeating the same action indefinitely.

## Anti-patterns
- **Fluent-proof fallacy**: accepting a polished informal proof as formally correct. Formal correctness requires a checker result.
- **State-only tunnel vision**: generating low-level tactics without capturing the strategic mathematical move can create brittle search.
- **One-shot formalization**: translating an entire proof directly and treating failure as all-or-nothing; the later lecture methods deliberately introduce intermediate layers.
- **Verifier bypass**: reporting completion from model confidence when a proof assistant is available.

## Reference Table
| Representation | Strength | Weakness | Best use |
|---|---|---|---|
| Informal proof/thought | strategy, abstraction, communication | can omit details or contain errors | planning, decomposition, search guidance |
| Formal proof/tactic | precise, checkable | verbose, brittle, context-sensitive | correctness, local state transitions |
| Formal sketch | preserves high-level structure with holes | holes may still be difficult | divide a hard proof into prover-sized obligations |
| Retrieved premises | narrows library search | depends on retrieval quality | routine subgoals in large libraries |

## Worked Example
Suppose Lean reports a goal that is mathematically obvious after rewriting a definition. Do not immediately sample many unrelated tactics. First state the intended move informally: “unfold the definition, then use the local equality.” Translate that into one candidate tactic sequence and run Lean. If the tactic changes the goal but does not close it, carry the new state forward. If it fails because a lemma is missing, route the problem toward premise selection instead of insisting that the initial strategy was wrong.

## Key Takeaways
1. Preserve the separation between strategic plausibility and formal validity.
2. Treat proof assistants as interactive environments with state, actions, and feedback.
3. Introduce intermediate representations when a direct informal→formal jump is too brittle.
4. Diagnose whether failure comes from strategy, action selection, missing context, or automation before allocating more search.

## Connects To
- **Ch 2**: Lean-STaR operationalizes the thought-before-tactic bridge.
- **Ch 3**: Draft-Sketch-Prove moves the bridge to a higher abstraction level.
- **Ch 5**: miniCTX shows that real proof states may be insufficient without repository context.
