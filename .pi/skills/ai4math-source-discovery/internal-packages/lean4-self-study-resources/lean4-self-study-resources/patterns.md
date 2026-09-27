# Patterns

## Goal-to-Resource Routing
**Origin**: STRUCTURAL_SYNTHESIS

**When to use**: A learner asks which Lean4 resource fits a concrete learning goal.

**How**:
1. Classify the goal: setup, functional programming, theorem proving, formal mathematics, metaprogramming, practice, lectures, or quick reference.
2. Select a resource whose archived label directly matches that category.
3. Give one next action rather than the whole resource list.
4. If the archive does not describe the needed capability, state the gap.

**Trade-offs**: Fast and source-faithful, but intentionally limited to what the archive recorded.

## Beginner Learning Ladder
**Origin**: STRUCTURAL_SYNTHESIS

**When to use**: A user asks for an end-to-end starting path.

**How**: installation if needed → functional programming/theorem proving foundations → optional Natural Number Game practice → *Mathematics in Lean* → specialized material/reference.

**Trade-offs**: Gives structure to a flat list. Skip stages the learner already knows; the sequence is synthesized, not author-prescribed.

## Search Escalation
**Origin**: STRUCTURAL_SYNTHESIS

**When to use**: The proof idea is known but the Mathlib theorem/declaration is not.

**How**:
1. Use Mathlib docs when the library area is known.
2. Try LeanSearch or Moogle when the name is unknown.
3. Validate the candidate in Lean.
4. Ask Zulip when still blocked.

**Trade-offs**: Reduces random browsing; search quality and external service availability can vary.

## Automation With Validation
**Origin**: IMPLEMENTATION_DECISION

**When to use**: The user chooses Quokka for automated formalization.

**How**: obtain a candidate formalization → run/check it in Lean → diagnose failures with docs/search → escalate to community support if needed.

**Trade-offs**: Automation can accelerate exploration, but correctness comes from successful Lean checking.

## Resource-Mismatch Recovery
**Origin**: STRUCTURAL_SYNTHESIS

**When to use**: A recommended resource is unavailable, too broad, too advanced, or fails to answer the actual need.

**How**:
1. Reclassify the user's goal.
2. For learning, move to an adjacent stage in the learning ladder.
3. For lookup, move between docs/search/community layers.
4. For unavailable theorem search, try the alternate search engine.
5. If no archived alternative exists, state the coverage gap.

**Trade-offs**: Keeps recovery grounded in the source instead of inventing a new curriculum.


## Suspected Platform-Bug Recovery
**Origin**: SOURCE_DERIVED + IMPLEMENTATION_DECISION

**When to use**: ReasLab or Quokka appears broken in a way that may be a service defect.

**How**:
1. Reproduce the issue and separate Lean/code errors from service behavior when possible.
2. If it still looks like a service bug, the archive explicitly says feedback is welcome.
3. Use only a feedback path exposed by the current service; the archive does not specify one.

**Trade-offs**: Preserves the source's invitation to report bugs while avoiding an invented support channel.
