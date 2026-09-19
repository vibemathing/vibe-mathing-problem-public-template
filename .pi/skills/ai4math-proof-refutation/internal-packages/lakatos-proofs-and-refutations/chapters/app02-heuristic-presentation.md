# Appendix 2: Heuristic Presentation and Proof-Generated Concepts

## Core Idea

A finished deductive presentation can conceal the problem situation that generated its definitions and the criticism that made those definitions necessary. To make mathematics intelligible for discovery, teaching, or design review, reconnect concepts to their proof-ancestors.

## Deductivist Presentation: Diagnostic Profile

A polished deductive text typically starts with definitions and axioms, then presents lemmas and theorems in final form. This is efficient for checking consequences, but it can hide:

- the original problem;
- failed conjectures;
- counterexamples;
- earlier proof attempts;
- the inferential step that generated a definition;
- why one condition is important while a nearby condition is irrelevant.

The result can make mature concepts look arbitrary or miraculous.

## Heuristic Reconstruction Workflow

**When to use:** a definition, theorem hypothesis, API invariant, design constraint, or formal specification seems unmotivated.

1. **Recover the problem** the final result solves.
2. **Recover the naive conjecture** that would naturally arise first.
3. **Construct or recover a plausible proof ancestor.**
4. **Locate its failure** through a counterexample or invalid step.
5. **Extract the missing condition** from the failed operation.
6. **Name the proof-generated concept** that packages this condition.
7. **Show the revised theorem/proof.**
8. **Search for the concept in neighboring proofs.**
9. **State the new questions** created by the revision.

For teaching, this sequence usually makes a technical definition easier to remember because the learner knows what failure it prevents.

## Worked Example 1: Uniform Convergence

Instead of beginning with an epsilon-style definition and asking the learner to accept it, begin with the claim that limits of continuous functions should preserve continuity. Exhibit a counterexample, inspect the proof, and identify the need for an index independent of the point. The definition of uniform convergence then arrives as the condition that repairs the proof.

This sequence explains both **what** the definition says and **why that quantifier order matters**.

## Worked Example 2: Bounded Variation

The textbook definition of total variation can look like an arbitrary supremum over partition sums. The appendix connects it to analysis of a proof in Fourier theory: the relevant proof step needs control over accumulated oscillation. Jordan's condition packages that control.

Operational lesson:
- when a supremum/norm/regularity condition looks artificial, trace which estimate in a proof needs exactly that bound;
- then test whether the same condition appears in related problems such as rectifiability or integration.

A concept becomes more than a patch when it coordinates several proof problems.

## Worked Example 3: Carathéodory Measurability

The criterion for a measurable set can seem “magical” if introduced alone. It becomes motivated when attached to the extension problem for an outer measure: the criterion is the splitting condition that makes additive measure behavior possible across a set and its complement.

Operational lesson: present a formal definition together with the theorem construction it enables. If a learner asks “why this exact condition?”, answer by pointing to the proof operation it licenses.

## Pattern: Proof-Ancestor Map

For every important definition `D`, record:

- **Problem:** what was being attempted?
- **Ancestor proof:** which argument failed or became awkward?
- **Failure:** what exact step was invalid?
- **Condition:** what property repairs that step?
- **Definition:** how does `D` package the condition?
- **Reuse:** where else does `D` solve the same structural problem?

This map is useful in mathematics, software specifications, scientific modeling, and policy design whenever final constraints have lost their rationale.

## Anti-patterns

- **Definition-first mystification:** introducing a precise condition without the problem that motivates it.
- **Whig reconstruction:** writing history as though the mature definition was obvious from the start.
- **Proof-ancestor deletion:** retaining a concept after forgetting which inferential failure it repaired.
- **Pedagogical authority:** asking learners to accept a condition because it appears in the final theorem.
- **False chronology:** treating a rational reconstruction as a literal report of historical sequence.

## Validation Criteria for Heuristic Exposition

A reconstruction is useful when a reader can answer:

1. What problem made the concept necessary?
2. Which counterexample/failure changed the proof?
3. Which exact step does the new definition license?
4. What would go wrong without the condition?
5. Where else does the condition recur?
6. Which parts are historical fact and which are rational reconstruction?

## Key Takeaways

1. Finished deductive order can conceal discovery logic.
2. Definitions are often intelligible through the proofs that generated them.
3. A good explanatory reconstruction preserves failures and alternatives, not just the successful endpoint.
4. Reuse across proofs is evidence that a condition captures a genuine structure.
5. Rational reconstruction must be distinguished from literal history.

## Connects To

- **Chapter 1:** proof-generated concepts and theoretical classification.
- **Chapter 2:** translation definitions can similarly hide what is preserved or changed.
- **Appendix 1:** uniform convergence supplies the clearest hidden-lemma-to-definition pipeline.
