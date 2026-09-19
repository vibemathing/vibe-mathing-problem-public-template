# 04 — Worker Proof-Search Loop

## Orientation

Workers turn strategic direction into verified mathematical units. They use local memory for process, global memory for reusable findings, and the fact graph for established premises. Their loop values falsification, explicit failure information, and verification of load-bearing intermediate results.

## Recommended route

### 1. Query memory

Search in this order: worker-local memory → global memory → fact graph. Target queries to the active subgoal. Give special weight to prior counterexamples, dead ends, verifier rejections, and established predecessor facts.

### 2. Obtain immediate conclusions

Normalize notation and equivalent formulations. Derive direct consequences from definitions and basic reasoning. Separate necessary conditions from candidate sufficient conditions. Mark fragile conclusions for counterexample testing. Publish useful formed conclusions with explicit evidence.

### 3. Construct toy examples

Choose simple cases that satisfy the assumptions and conclusion. Identify where each assumption becomes active, what mechanism makes the conclusion work, and which patterns may generalize. Toy examples give intuition; they do not prove the theorem.

### 4. Construct counterexamples

For a fragile claim, keep its assumptions true while forcing the conclusion to fail. Classify the attempt:

- `refuted`: a valid counterexample exists;
- `not_refuted`: none found yet;
- `inconclusive`: search space remains unclear.

A lack of counterexample is evidence only. If a counterexample kills a branch, publish both the concrete counterexample and a shared dead-end record.

### 5. Propose materially different decompositions

Create several plans that attack the theorem through different mechanisms. Each plan should state ordered subgoals, why the decomposition might work, dependencies, and known routes/failures it avoids.

### 6. Screen a plan by direct proving

Try to carry the entire plan through before switching to diagnosis. For each subgoal:

- use relevant facts, examples, counterexamples, and literature;
- adapt proof ideas rather than treating similar theorems as black boxes;
- when an external theorem has extra hypotheses, analyze why its proof needs them and where transfer fails;
- mark status `solved`, `partial`, or `stuck`.

If a subgoal is stuck, run counterexample search first. If no refutation appears after at least two genuine direct attempts, publish a concrete obstacle/dead end instead of grinding indefinitely.

### 7. Verify downstream dependencies

If a partial result will be used by the rest of the plan, make it self-contained and send it through verification before treating it as established. This is the main defense against a proof tree built on one attractive but false intermediate step.

### 8. Identify key failures and replan

When plans fail, synthesize common stuck points, recurring obstructions, missing background, and proof-migration failures. Publish this as shared failure knowledge and return to planning with a new direction.

## Sustained work

When a direction remains viable and supports real progress, spend sustained effort on one deep obstacle rather than producing many shallow facts. A fact should represent a substantive mathematical unit whose verification helps downstream work.

## External theorem transfer

When a similar result exists:

1. recover the exact theorem statement and definitions;
2. understand its proof mechanism;
3. list all extra hypotheses;
4. locate where those hypotheses enter the proof;
5. compare them with the current object;
6. either adapt the mechanism, prove the missing interface, or record the precise migration failure.

Do not reduce transfer to “show our object satisfies the published theorem's assumptions” when the method itself may reveal a better route or a genuine obstruction.

## Failure records are first-class output

A high-quality dead end names:

- the attempted route;
- the exact step that fails;
- evidence for failure;
- whether the claim seems false, too strong, or merely unproved;
- what future evidence would justify revisiting it.

This saves other workers from repeating the same work and gives the main agent signal for the next portfolio decision.

## Self-check

Before claiming progress, ask:

- Did I search for existing facts and failures first?
- Does every used premise exist in the fact graph?
- Did I stress-test fragile subgoals before escalating effort?
- If I adapted a theorem, did I inspect definitions and all hypotheses?
- Is every downstream-used intermediate result verified?
- Am I creating one substantive verified unit, or fragmenting routine steps into fact spam?
