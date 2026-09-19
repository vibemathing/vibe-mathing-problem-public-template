# Chapter 6: Supplemental Reading — ImProver and Verified Proof Optimization

## Core Idea
The course page links ImProver as supplemental reading. Its task begins after a formal proof exists: rewrite the proof so it remains correct while improving a user-defined metric such as length, readability, declarativity, or modularity. Correctness remains a hard constraint; optimization is secondary.

## Frameworks Introduced
- **Automated proof optimization**: search over rewrites of an existing proof under a metric, with formal verification after each candidate.
  - When to use: the theorem already has a checked proof, but that proof is poor for humans, maintenance, or downstream training data.
  - How: define the metric; capture theorem and symbolic context; propose a rewrite; run Lean; score only verified candidates; retain the best; iterate.
  - Why it works: generation and quality objectives are different problems; separating them allows aggressive rewriting without weakening the correctness gate.
  - Failure mode: optimizing a proxy such as character count can damage structure or readability unless the metric reflects the real objective.
- **Chain-of-States**: expose symbolic Lean state/context through the rewriting process rather than asking an LLM to optimize from surface code alone.
  - When to use: rewrites frequently break because the model loses track of intermediate proof obligations or context.
  - How: provide formal state information around candidate transformations; use error correction and retrieval when a rewrite fails.

## Key Concepts
- **Optimization metric**: a function/criterion that scores a verified rewrite, such as length or structural style.
- **Correctness constraint**: the rewritten proof must still be accepted by Lean.
- **Error correction**: use compiler/verifier feedback to repair a candidate rewrite.
- **Retrieval**: supply examples, facts, or documentation that support the requested transformation.
- **Declarativity**: proof structure that states intermediate mathematical facts explicitly instead of relying mainly on opaque tactic sequences.
- **Proof data quality**: optimized proofs can be more suitable as examples for learning systems, depending on the metric.

## Mental Models
- **Verify first, optimize second**: the feasible set contains only checked proofs; the metric ranks within that set.
- **One objective per run**: if “shorter,” “more readable,” and “more modular” conflict, specify priorities or a composite metric before rewriting.
- **Use state feedback as a repair signal**: a failed rewrite should reveal which transformation violated formal constraints.

## Anti-patterns
- **Metric-free optimization**: asking for a “better proof” without defining better.
- **Correctness as a score**: allowing a highly optimized invalid proof to compete with valid candidates. Invalid candidates are rejected, not merely penalized.
- **Whole-proof mutation without checkpoints**: changing many independent parts at once makes error attribution difficult.
- **Proxy gaming**: minimizing raw length so aggressively that the result becomes brittle or unreadable when readability was part of the real goal.

## Reference Table
| Objective | Candidate metric | Guardrail |
|---|---|---|
| Shorter proof | token/AST/tactic count | preserve verification; avoid unreadable compression |
| More declarative | structural measure / explicit fact blocks | preserve theorem semantics and dependency legality |
| More modular | reusable lemma structure | avoid gratuitous fragmentation |
| Training-data cleanup | style/complexity metric | retain proof diversity and correctness |

## Worked Example
Given a verified Lean proof with repeated manual rewrites, define the target as “reduce proof length without decreasing readability.” Preserve the original proof as rollback. Propose one localized rewrite, run Lean, and reject it immediately if verification fails. Score valid alternatives on length plus a readability constraint. Continue from the best verified version. This makes every iteration reversible and keeps optimization errors separate from theorem-proving errors.

## Procedure
1. Save the last known verified proof and environment.
2. Define a measurable optimization objective and any hard style constraints.
3. Extract symbolic context/intermediate states relevant to the proof.
4. Generate a small rewrite candidate rather than mutating unrelated regions simultaneously.
5. Run Lean; reject invalid candidates.
6. Score valid candidates; accept only a strict improvement under the declared objective.
7. On failure, use the error state to repair or revert.
8. Re-run full theorem/project checks after accumulated rewrites.

## Failure Recovery
- **Rewrite fails to compile** → revert, inspect the exact state/error, and make a smaller transformation.
- **Metric improves but humans dislike output** → metric is incomplete; encode readability/structure constraints.
- **Local rewrite verifies but project check fails** → include downstream interface/dependency tests in the correctness gate.
- **No improving rewrite found** → return the verified original; lack of optimization gain is a valid result.

## Key Takeaways
1. Proof correctness is a constraint, not an optimization preference.
2. Define the metric before rewriting.
3. Symbolic state, retrieval, and error correction make rewrites more reliable.
4. Preserve rollback checkpoints and change one region at a time.
5. Optimization belongs after proof discovery/formalization, though its results can improve future training data.

## Connects To
- **Ch 1**: keeps the verifier as the hard validity boundary.
- **Ch 5**: research-level proofs need project context during optimization as well as generation.
