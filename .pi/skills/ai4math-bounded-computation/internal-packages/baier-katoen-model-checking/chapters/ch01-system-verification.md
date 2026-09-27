# Chapter 1: System Verification

## Core Idea

Model checking is a disciplined loop over a **formal system model** and a **formal property**. Its result is trustworthy only relative to those two artifacts, so a successful run still depends on model validation, requirement coverage, and reproducible verification organization.

## Frameworks Introduced

### The model-checking process
**When to use**: any model-checking task, before choosing an algorithm.

**How**:
1. **Modeling phase**
   - represent the system in the model checker's language;
   - run simple simulations as a sanity check;
   - formalize each requirement in the property language.
2. **Running phase**
   - configure the checker and verify the property over the model.
3. **Analysis phase**
   - **satisfied**: record the result and move to the next property;
   - **violated**: replay the generated diagnostic/counterexample, then determine whether the defect lies in the model, design, or property;
   - **resource failure**: reduce the model with a property-preserving technique and rerun.
4. **Verification organization**
   - version models, abstractions, properties, checker options, counterexamples, and statistics so a run can be reproduced.

### Verification vs. validation
**Use this distinction whenever a proof result seems stronger than the modeling evidence.**

- **Verification question**: does the formal model satisfy the stated formal property?
- **Validation question**: do the model and property faithfully represent the intended system and requirement?

A checker can establish the first while the second is wrong. Therefore include concrete scenario checks, stakeholder requirements, and model/property review around the formal run.

### Diagnostic classification
When a property is falsified, classify before editing anything:

| Finding | Meaning | Required action |
|---|---|---|
| Model does not reflect design | modeling error | correct model; rerun affected prior properties |
| Model is faithful and trace is undesirable | design error | change design and model; rerun verification |
| Property misstates informal requirement | property error | correct property; recheck that property |
| Checker cannot fit model | capacity problem | apply sound reduction/abstraction and retry |

**Why it works**: changing the wrong artifact can hide a real defect or invalidate earlier evidence.

## Key Concepts

- **Correctness relative to a specification**: a system is called correct only with respect to the properties extracted from a specification; there is no specification-free notion of “all bugs absent.”
- **Model checking**: automated systematic checking of a formal property over a finite-state model (with later chapters extending the setting).
- **Counterexample**: diagnostic execution that demonstrates how a property can fail; it is a debugging artifact, not automatically proof of an implementation defect.
- **Model-based verification**: analysis is performed on a mathematical behavioral model; fidelity of that model bounds the significance of the result.
- **Partial verification**: individual properties can be checked without first producing a complete formal requirements set.
- **State-space explosion**: the reachable state count may grow beyond memory/time even when the component description is compact.
- **Re-verification**: if a model is corrected, previously checked properties may need to be rerun because their earlier result was about a different model.
- **Complementary verification**: testing, peer review, simulation/emulation, and formal checking catch different defect classes and operate at different layers.

## Mental Models

- **Use the checker as an exhaustive debugger over the model** when subtle concurrency/nondeterminism makes scenario testing unreliable.
- **Think of the model as a hypothesis about the product**. Passing properties increases confidence in the hypothesis; it does not test fabrication faults, compiler errors, or omitted requirements.
- **Treat formalization itself as defect discovery**. Ambiguous informal requirements and inconsistent assumptions often surface while choosing states, transitions, and formulas.
- **Front-load defect detection**. Formal modeling and checking have the greatest economic leverage before errors propagate into implementation and deployment.

## Anti-patterns

- **Equating “property holds” with absolute correctness**: only the stated property on the formal model was checked.
- **Editing the property until a counterexample disappears**: a formula change needs an independent requirements justification.
- **Changing a model and keeping all old green checks**: model edits can invalidate earlier verification results.
- **Using model checking as a replacement for testing**: model checking does not directly find implementation/fabrication faults outside the model.
- **Skipping configuration provenance**: different abstractions or checker options can make an old result impossible to reproduce.
- **Assuming a tool cannot contain defects**: the mathematical method may be sound while a checker implementation still has bugs.

## Reference Table: strengths and boundaries

| Model checking is strong when… | Caution when… |
|---|---|
| control behavior and concurrency dominate | data domains are large or infinite |
| exhaustive state exploration is feasible | state space exceeds resources |
| a diagnostic trace accelerates debugging | a counterexample may arise from a bad model/property |
| each requirement can be checked separately | important requirements may be unstated |
| early design models are available | implementation/fabrication differs from the model |
| finite-state abstractions can be justified | arbitrary parameterized systems are expected |

## Worked Example: atomicity exposes a hidden concurrency error

Consider three indefinitely running processes over an integer `x`:

- one increments `x` when `x < 200`;
- one decrements `x` when `x > 0`;
- one resets `x` to `0` when `x == 200`.

A tempting invariant is `0 <= x <= 200`. It fails if each test and subsequent assignment are separate atomic steps:

1. `x = 200`.
2. The decrementing process tests `x > 0` and is preempted before assignment.
3. The reset process tests `x == 200` and sets `x = 0`.
4. The decrementing process resumes its already-enabled assignment and writes `x = -1`.

Operational lesson: before checking any property, specify what is atomic. A model that merges test-and-update into one transition would remove this interleaving and verify a different system.

## Failure Recovery

### Property violation
Replay the diagnostic trace and ask in order:
1. Can the formal model execute this trace?
2. Can the intended design/implementation execute the corresponding behavior?
3. Does the formal property faithfully encode the informal requirement?
4. If all three answers support the trace as a genuine violation, treat it as a design defect.

### Out of memory
Do not reduce blindly. Identify what must be preserved:
- symbolic ROBDDs for regular Boolean structure → Ch 6;
- quotient/abstraction → Ch 7;
- independent interleavings → Ch 8;
- dense time → Ch 9 region abstraction.

### “No bugs found”
Check coverage: which requirements were never formalized? A verified subset cannot support claims about omitted properties.

## Key Takeaways

1. Treat **model + property + checker configuration** as the unit of evidence.
2. Validate models and formulas independently before trusting a green result.
3. Classify counterexamples as model, design, or property problems before repair.
4. Model changes trigger regression verification.
5. State-space reduction is a soundness problem first and a performance problem second.
6. Preserve run provenance so evidence can be reproduced.

## Connects To

- **Ch 2**: how to build operational models whose semantics make the verification result meaningful.
- **Ch 3–6**: how to formalize and check qualitative properties.
- **Ch 7–9**: sound routes when the model is too large or timing matters.
- **Ch 10**: quantitative verification when uncertainty/probability is part of the model.
