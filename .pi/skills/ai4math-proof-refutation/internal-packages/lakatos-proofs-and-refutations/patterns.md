# Patterns

## Counterexample Triage
**When to use**: Any candidate counterexample appears.

**How**:
1. Test the main conjecture → global yes/no.
2. Test each proof lemma → local yes/no.
3. Route by the 2×2 matrix.
4. Record which definition makes the classification possible.

**Trade-offs**: Requires a proof decomposition; without one, local status is provisional.

## Hidden-Lemma Search
**When to use**: Global counterexample; all explicit lemmas survive.

**How**:
1. Expand compressed proof steps.
2. Expose quantifier order, continuity/uniformity, existence, uniqueness, connectedness, finiteness, regularity, and representation assumptions.
3. Turn each tacit dependency into a candidate lemma.
4. Design discriminating examples.
5. Select the candidate that localizes the failure.

**Trade-offs**: Several hidden lemmas may explain one failure; report underdetermination until a discriminating case is found.

## Lemma Incorporation
**When to use**: A global counterexample also falsifies a proof lemma.

**How**:
1. State the falsified lemma precisely.
2. Convert it into a theorem condition.
3. Prefer the weakest proof-generated condition that licenses the step.
4. Re-run global/local counterexample search.

**Trade-offs**: Increases security by shrinking scope; must be balanced with Rule 4/5.

## Rule-4 Proof Deepening
**When to use**: Local counterexample, main conjecture survives.

**How**:
1. Replace the failed lemma within the current proof if a nearby adequate lemma exists.
2. If repairs accumulate, search for a different proof idea.
3. Compare proof ranges and the concepts each generates.

**Trade-offs**: Radical replacement costs more work but can recover content lost by conservative patches.

## Deductive Guessing
**When to use**: A counterexample suggests the current conjecture is the wrong target.

**How**:
1. Identify a constructive proof/problem mechanism.
2. Generalize the mechanism rather than the observed table.
3. Derive a broader candidate theorem.
4. Verify that former counterexamples become explained cases.

**Trade-offs**: Requires a meaningful proof construction; do not label arbitrary generalization “deductive”.

## Definition Genealogy
**When to use**: Terms change during criticism.

**How**:
1. Version each definition.
2. Record included/excluded examples.
3. Record which proof step motivated the change.
4. Label the move: monster-barring, exception-barring, monster-adjusting, concept stretching, or proof-generated concept.
5. Test the new definition on fresh cases.

**Trade-offs**: Adds bookkeeping but prevents semantic drift from masquerading as theorem improvement.

## Translation-Procedure Audit
**When to use**: Informal objects are encoded into algebra, logic, models, or software.

**How**:
1. Build source→target mapping.
2. Mark preserved, lost, and added structure.
3. Separate meaning-preserving claims from stipulative redefinitions.
4. Identify target axioms and formative terms.
5. Test intended counterexamples through the encoding.
6. If formal proof passes but application fails, debug the mapping/model first.

**Trade-offs**: Weakens blanket claims of certainty but sharply localizes where uncertainty remains.

## Proof-Ancestor Reconstruction
**When to use**: A definition or theorem condition seems arbitrary.

**How**:
1. Recover the problem and naive conjecture.
2. Reconstruct a plausible ancestor proof.
3. Find the failing step/counterexample.
4. Derive the condition that repairs it.
5. Show how the final definition packages that condition.
6. Look for reuse in neighboring proofs.

**Trade-offs**: A rational reconstruction may differ from literal chronology; label historical claims separately.
