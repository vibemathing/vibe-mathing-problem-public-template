# Chapter 12: AI Autoformalization and Semantic Audit

## Core Idea

AI changes the cost of producing Lean code, but different artifacts have different verification stories. Proofs of an already trusted formal statement can be mechanically checked. Statements and definitions encode meaning; they can compile while being wrong. Route AI output by artifact type and place human review where the checker has no semantic oracle.

## Four Artifact Classes

### A. Informal mathematical prose

Treat as untrusted. Language models can produce long plausible arguments containing one hidden invalid assumption, change their conclusion to please the user, or reuse a theorem outside its hypotheses. Inspect prerequisites and request formalization when the stakes justify it.

### B. Formal theorem statements

Audit manually:
1. binders and quantifier order;
2. hypotheses, including small/edge cases;
3. intended structures and coercions;
4. conclusion and equality notion;
5. whether the theorem became vacuous/trivial;
6. representative examples/nonexamples.

Translation is not unique. The correct formal statement is a mathematical judgment.

### C. Formal definitions

Use the strongest review. A definition can omit an axiom and still compile. Check it against trusted references and characterization theorems; exercise standard examples and nonexamples; review hierarchy placement, generality, coercions, and downstream API. “Correct enough for one generated proof” may create large technical debt in a shared library.

### D. Formal proofs

Once the statement and definitions are trusted, compile/type-check the proof. For high-stakes work, inspect axioms/dependencies and consider an independent checker. Proof generation can be delegated much more aggressively than definition design because invalid proof terms should be rejected.

## Autoformalization Suitability Matrix

**Strong candidate:** definitions already exist in a mature library; theorem statement is fixed; human literature gives a detailed proof; subgoals use established APIs.

**Medium candidate:** statement is clear but some local API or library lemmas are missing. Let AI propose code, keep expert review on new infrastructure.

**Weak candidate:** project is definition-heavy, the intended generality is unsettled, the theorem statement itself is ambiguous, or the area is absent from the library. Use AI for brainstorming/local code only; humans own semantics and architecture.

Test this on a **target chosen before evaluating the tool**. Choosing only tasks where autoformalization already works gives a distorted capability estimate.

## Misformalization Taxonomy

1. **Low-level:** flipped inequality, wrong constant, zero case, typo, bug.
2. **Missing hypotheses:** statement is false in an omitted edge condition.
3. **Quantifier/scope:** variables depend on the wrong earlier choices.
4. **Definition mismatch:** formal concept differs from the literature.
5. **High-level misunderstanding:** the human source/problem itself was misread.

When AI finds a failure, determine which class occurred. A failed proof attempt can be a valuable theorem-statement debugger.

## Workflow

For AI-assisted formalization:
1. freeze the target statement with a human/domain audit;
2. inventory which definitions are trusted library components;
3. permit AI to generate proof code for mature-interface regions;
4. quarantine new definitions/APIs for expert review;
5. compile continuously;
6. log places where the source needed repair;
7. refactor successful generated infrastructure before upstreaming;
8. produce a human explanation for results of lasting importance.

## Anti-patterns

- “It compiles, therefore the definition is correct.”
- Accepting a correct numerical answer backed by invalid reasoning.
- Best-of-many generation where nobody can identify which output is trustworthy.
- Assuming scale of generated code compensates for missing semantic review.

## Validation Checkpoint

Use three independent gates. First, compare the generated statement or definition with a trusted human specification using examples, nonexamples, quantifier order, and boundary cases. Second, compile the proof in the intended environment and inspect dependencies or axioms appropriate to the assurance level. Third, ask for a short human explanation of the proof spine or generated construction. Passing the second gate cannot repair failure at the first. If the artifact includes executable project code, add a security review before running it; formal correctness of a theorem says nothing about repository safety.

## Key Takeaways

Automate proof search aggressively after meaning is frozen. Treat statements and definitions as specification artifacts requiring expert semantic review. The bottleneck shifts toward formalizing modern concepts idiomatically and maintaining high-quality shared libraries.

## Connects To

Statement routing: [01](ch01-orientation-and-statement-routing.md). Definition quality: [06](ch06-definition-api-and-library-engineering.md). Trust: [08](ch08-automation-reflection-and-trust.md). Counterexamples and benchmarks: [13](ch13-counterexamples-benchmarks-and-proof-digestion.md).
