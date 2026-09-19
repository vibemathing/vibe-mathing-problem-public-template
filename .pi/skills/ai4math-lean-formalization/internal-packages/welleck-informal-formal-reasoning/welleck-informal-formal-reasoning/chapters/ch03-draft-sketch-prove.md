# Chapter 3: Draft, Sketch, and Prove — Search at a Higher Abstraction

## Core Idea
Draft-Sketch-Prove (DSP) uses an informal proof to guide a formal proof sketch, leaving explicit gaps for an automated prover. The method relocates search from raw low-level tactics to a structured intermediate representation whose subproblems are easier to automate.

## Frameworks Introduced
- **Draft-Sketch-Prove (DSP)**: three-stage formalization pipeline.
  - When to use: an informal proof or plausible high-level argument exists, but directly generating a complete formal proof is brittle or expensive.
  - How:
    1. **Draft**: obtain one or more informal proofs from a human or language model.
    2. **Sketch**: translate a draft into a formal skeleton that mirrors its major reasoning steps while leaving hard local obligations as explicit holes.
    3. **Prove**: invoke an off-the-shelf formal prover/hammer on each hole; accept the result only when the complete formal artifact verifies.
  - Why it works: a good sketch partitions one difficult proof-search problem into smaller obligations and injects human-like high-level structure.
  - Failure mode: a mathematically wrong draft can produce a structurally coherent but unprovable sketch; a sketch can also be too coarse, leaving gaps as hard as the original theorem.
- **Abstraction-level proof search**: sample multiple drafts/sketches rather than only many low-level tactic sequences.
  - When to use: local branching is enormous but there are a few qualitatively distinct proof strategies.
  - How: diversify the informal strategy first, map promising strategies to formal sketches, then spend low-level automation only on their resulting gaps.

## Key Concepts
- **Draft**: an informal mathematical proof candidate.
- **Formal sketch**: a syntactically formal proof skeleton with unproven subgoals/gaps.
- **Gap**: a local conjecture delegated to an automated prover.
- **Hammer**: automation that attempts to solve a local formal goal, often using premise selection and external provers.
- **Decomposition quality**: whether sketch gaps are substantially easier than the original theorem.
- **Inference-time scaling**: allocating more candidate trajectories/sketches; the lecture notes emphasize gains can plateau.

## Mental Models
- **Search over strategies before syntax**: when two proof ideas differ conceptually, represent that difference in the draft/sketch layer instead of hoping tactic sampling discovers it accidentally.
- **A sketch is a contract**: every hole must have a precise formal statement, known local context, and a clear verifier outcome.
- **Spend automation where it is strongest**: let the model choose structure; let symbolic tools discharge routine local obligations.

## Anti-patterns
- **Hole laundering**: replacing a hard theorem with one enormous hole and calling the result a useful sketch.
- **Draft worship**: refusing to revise the informal proof after formal gaps reveal a hidden logical flaw.
- **Blind trajectory scaling**: increasing the number of nearly identical drafts after success has plateaued.
- **Untracked translation drift**: allowing the formal sketch to change theorem meaning or silently drop assumptions from the informal statement.

## Reference Table
| Layer | Primary job | Success signal | Typical failure |
|---|---|---|---|
| Draft | choose mathematical route | coherent derivation under intended assumptions | wrong/incomplete strategy |
| Sketch | encode route into formal subgoals | theorem/assumptions preserved; gaps smaller | translation drift; giant gaps |
| Prove | close each local gap | proof assistant accepts each insertion | missing premise; hard subgoal |
| Final verification | certify composition | whole theorem checks | interface mismatch between pieces |

## Worked Example
The lecture deck uses a small number-theory-style example: an informal argument first derives a compact arithmetic consequence from gcd/lcm relationships, from which the unknown value is determined. DSP would preserve those major steps in the formal sketch, while replacing routine algebraic justifications with local proof holes. A hammer then closes those holes. The important artifact is the decomposition: the automated prover sees small arithmetic obligations instead of having to discover the entire argument and its structure from scratch.

## Procedure
1. Check that informal and formal theorem statements express the same claim and assumptions.
2. Generate 1–N meaningfully different drafts if strategy is uncertain.
3. For each draft, identify indispensable lemmas/intermediate claims.
4. Translate those claims into a formal sketch; use explicit holes only for local obligations.
5. Estimate each hole: routine automation, premise retrieval, or custom reasoning.
6. Run automation on routine holes; route unresolved holes to LeanHammer or Lean-STaR.
7. If several holes fail for the same conceptual reason, revise the sketch rather than retrying each independently.
8. Verify the assembled proof end-to-end.

## Failure Recovery
- **Sketch does not type-check before filling holes** → fix translation/theorem alignment first.
- **Most holes fail** → draft/structure is likely wrong or too ambitious; redraft.
- **One routine hole fails with unknown facts** → premise selection problem; use LeanHammer.
- **One conceptually hard hole fails** → split it further or use interleaved thought+tactic reasoning.
- **Search improvements plateau** → diversify strategy/model/representation instead of only increasing samples.

## Key Takeaways
1. Use formal sketches to turn high-level reasoning into verifier-addressable subproblems.
2. Judge a sketch by how much it simplifies downstream proof search.
3. Preserve statement semantics across informal→formal translation.
4. Search budget is most valuable when it buys strategy diversity.
5. Final correctness still comes only from the completed formal proof.

## Connects To
- **Ch 2**: Lean-STaR can solve difficult local gaps after DSP chooses the global structure.
- **Ch 4**: LeanHammer is a natural gap-closing component when premises can be selected effectively.
