# Chapter 13: Counterexamples, Benchmarks, and Proof Digestion

## Core Idea

Machine systems can be unusually effective at witness search. For universal conjectures, a counterexample-first route can be cheaper than a direct proof attempt. Correctness must be certified, and the resulting witness should then be converted from a machine artifact into human mathematical understanding. Evaluation systems should measure this reasoning rather than reward lucky answers.

## Counterexample-First Workflow

WHEN the claim is universal or asserts necessity:
1. formalize the exact conjecture and its negation;
2. audit the statement for intended scope—especially degenerate cases;
3. express a candidate witness contract that is cheap to check;
4. use AI, symbolic computation, search, databases, or bespoke code to generate candidates;
5. verify the candidate independently in Lean or another rigorous checker;
6. confirm the witness does not exploit a mistranslation or omitted hypothesis;
7. simplify the witness and identify the conceptual obstruction;
8. publish/cross-link both the certificate and a human explanation.

This route is especially attractive when refutation reduces a large universal search to finding one structured example. It does not imply that every universal theorem is easy; it is a search heuristic whose value depends on the domain.

## From Witness to Insight

A verified 1000-line counterexample may still teach little. Digest it:

- identify which defining property fails;
- locate the smallest subcalculation responsible;
- replace accidental constants with parameters/invariants when possible;
- trace the example to known constructions or literature;
- ask whether the mechanism generates a family of counterexamples;
- restate the mechanism as a short lemma or conceptual obstruction.

Formal correctness and mathematical understanding are separate deliverables. The second can often be built *after* the first has removed doubt about whether the phenomenon is real.

## Benchmark Integrity

Many AI math benchmarks prefer numerical answers because automated grading is cheap. This creates failure modes:

- a system guesses the answer but cannot justify it;
- best-of-many sampling gets one correct answer with no reliable selector;
- training-data leakage rewards memorization;
- problem format selects a narrow type of mathematics;
- company-defined rules and self-grading undermine comparability.

Better evaluation procedure:
1. fix rules and target set before runs;
2. preserve contamination controls;
3. separate answer discovery from proof/certificate verification;
4. for theorem tasks, use formal proof when possible;
5. audit formal translations independently;
6. require reproducibility and disclose compute/human intervention;
7. report failure categories, not only aggregate scores.

If only a numerical answer is practical, include adversarial checks that make heuristic guessing insufficient and inspect reasoning on a sample.

## Formalization Communities as Data Infrastructure

The Erdős-problem experience shows that AI success can depend on social and formal infrastructure: curated problem statements, active discussion, existing formal conjectures, and a library able to express the objects. To make a field more machine-actionable, formalize definitions and statements even before every proof is available, and link them to human references/examples/counterexamples.

## Anti-patterns

- Declaring a famous conjecture resolved from an informal machine transcript alone.
- Rejecting a counterexample because it is “too simple”; hindsight can hide how long the search space resisted humans.
- Treating a formal witness as self-explanatory.
- Comparing AI systems using privately chosen or mutable scoring rules.

## Validation Checkpoint

For a purported counterexample, write the negation of the exact formal conjecture and make the witness satisfy it in the proof assistant. Recheck that no translation error made the target weaker. Then minimize or perturb the witness to identify which features are essential. For benchmarks, freeze the target and evaluation rules before looking at system behavior, require reproducible certificates where possible, and score reasoning separately from a guessed final answer. A huge verified witness is a correctness result; the next task is to extract a stable human mechanism explaining why the conjecture fails.

## Key Takeaways

For universal claims, verified witness search is a first-class route. After verification, invest in digestion. For AI evaluation, a correct answer without a trustworthy selection/derivation mechanism is weak evidence of mathematical reasoning.

## Connects To

AI semantic audits: [12](ch12-ai-autoformalization-and-semantic-audit.md). Trusted checking: [08](ch08-automation-reflection-and-trust.md). Research project structure: [10](ch10-research-blueprints-and-library-growth.md).
