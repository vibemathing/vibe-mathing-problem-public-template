# Reusable Patterns

## Outer-Shape Routing
**When to use**: Any new proof state.

**How**:
1. Read the target and local context as types.
2. Identify the target's outer constructor/operator.
3. Choose the corresponding constructor or eliminator: introduce functions/foralls, construct products/existentials, split cases for sums/inductives, rewrite equalities.
4. Re-read the smaller goals before automating.

**Trade-offs**: Explicit routing is verbose for trivial goals, but it exposes dependencies and gives reliable failure diagnostics.

## Natural Proof → Lean Blueprint
**When to use**: A theorem is mathematically clear but Lean implementation is long.

**How**:
1. Write the ordinary proof in short mathematical steps.
2. Mark each introduced object, assumption, case split, witness, and intermediate claim.
3. Translate those into `intro`, `have`, constructors, `rcases`, case splits, or theorem applications.
4. Search Mathlib for each nontrivial bridge.
5. Isolate missing bridges as helper lemmas; scaffold independent pieces if collaborating.
6. Close local arithmetic only after the structure is exposed.

**Trade-offs**: Costs planning time up front; pays off by preventing tactic thrashing.

## Mathlib Search Ladder
**When to use**: You know the mathematical fact but not its declaration name.

**How**:
1. Inspect nearby source or Ctrl-click related definitions/theorems.
2. Try predictable names/autocomplete.
3. Use `apply?` on the live goal.
4. Use semantic search such as LeanSearch/`#leansearch` or equivalent tools.
5. Verify the candidate with `#check` and inspect required instances/arguments.
6. If no theorem fits, search one abstraction layer above/below before proving from scratch.

**Trade-offs**: Search is fast when the target is well shaped; a poorly normalized target can hide the right theorem.

## Controlled Unfolding
**When to use**: A custom/new definition blocks progress.

**How**:
1. Prefer API theorems for mature Mathlib concepts.
2. `unfold` a custom definition when its body directly reveals the needed logical structure.
3. Stop when expansion introduces implementation detail unrelated to the mathematics.
4. Repackage useful low-level facts into a helper lemma and return to the higher abstraction.

**Trade-offs**: Unfolding increases transparency and brittleness simultaneously.

## Constructor/Eliminator Pairing
**When to use**: Propositions or data are represented by structures/inductives.

**How**:
- To prove a one-constructor object, supply its fields.
- To use one, project or destructure fields.
- To prove a multi-constructor target, choose a constructor explicitly.
- To use a multi-constructor hypothesis, cover every constructor case.

**Trade-offs**: Explicit constructors make intent stable; generic tactics can be shorter but hide which branch was selected.

## Rewrite → Calculation Chain
**When to use**: Equality or ordered calculations involve several controlled transformations.

**How**:
1. Use `rw` for a local substitution with a clear match.
2. Use `calc` when intermediate expressions or relation changes carry mathematical meaning.
3. Normalize only the residual algebra with `ring`, `linarith`, `norm_num`, or narrow `simp` as appropriate.

**Trade-offs**: `calc` is longer, but localizes failures to a single transition.

## Strengthen Induction Setup
**When to use**: An induction hypothesis is unusably specialized.

**How**:
1. Identify variables/relations that became fixed too early.
2. `revert` dependent data, or `generalize` a complex expression into a fresh variable/equality.
3. Perform induction on the structural object.
4. Reintroduce generalized data in each case.

**Trade-offs**: More general statements produce stronger hypotheses but larger contexts.

## Extended-Real Finite Reduction
**When to use**: EReal/ENNReal arithmetic stalls because infinities are possible.

**How**:
1. Identify which operands may be infinite.
2. Split exceptional infinite cases explicitly.
3. In the finite branch, establish finiteness hypotheses.
4. Convert/lift to real-valued arithmetic where the desired inequality is easier.
5. Transfer the result back.

**Trade-offs**: Extra case work buys access to familiar real arithmetic and automation.

## Filter First, Metric Second
**When to use**: Limits, continuity, or subsequences in analysis.

**How**:
1. Keep compositional reasoning at `Tendsto`/filter level.
2. Use map/preimage/eventual lemmas to compose transformations.
3. Switch to metric epsilon statements only when a concrete bound or witness is required.
4. Return to abstract continuity/limit lemmas after the estimate.

**Trade-offs**: Filters compose cleanly; metric forms are easier for explicit estimates.

## Derivative API Ladder
**When to use**: Proving differentiability or extracting a derivative value.

**How**:
1. Prefer a `HasFDeriv*` statement when constructing or composing a derivative proof.
2. Derive `Differentiable*` when only existence matters.
3. Use computed `fderiv*`/ordinary derivative functions after differentiability is established.
4. Treat fallback values of derivative functions as semantically uninformative when differentiability is absent.

**Trade-offs**: Stronger derivative predicates need more proof data but support robust composition.

## Small-Core Project Strategy
**When to use**: Competition or research formalization under limited time.

**How**:
1. Test representation and library support on a small theorem.
2. Prefer domains with direct existing infrastructure.
3. Build definitions and key lemmas before broad generalization.
4. Reduce scope when a missing framework dominates the mathematical task.
5. Expand only after the core compiles end to end.

**Trade-offs**: Less initial generality; much lower risk of an unfinished formalization.
