# Operational Patterns

## Inspect Before Proving
**When to use**: Any elaboration, unknown identifier, coercion, instance, or surprising goal-shape failure.

**How**:
1. Read the exact error and current goal.
2. `#check` important expressions and `#print` declarations whose parameters/definitions matter.
3. Expose hidden arguments with `@` or pretty-printer options.
4. Check imports, namespace/scope state, attributes, and options.
5. Add the smallest type annotation or explicit argument that resolves the missing constraint.

**Trade-offs**: Slightly slower than guessing; avoids long chains of proof edits aimed at the wrong elaborated term.

## Shape-Directed Logical Proof
**When to use**: Goal is built from `→`, `∀`, `∧`, `∨`, `¬`, `↔`, or `∃`.

**How**: Follow the connective's constructor/eliminator. Introduce `→`/`∀`; construct both sides of `∧`/`↔`; choose a provable `∨` branch; derive `False` for negation; give a witness for `∃`; use `cases` to consume disjunctions/existentials.

**Trade-offs**: Deterministic and readable; may need domain lemmas after the logical shell is removed.

## Equality Escalation
**When to use**: Goal differs by definitions or known equalities.

**How**: `rfl` → targeted `rw` → controlled `simp`/`simp only` → `calc` or congruence → `conv` for exact occurrence/binder selection.

**Trade-offs**: Later steps add control and verbosity. Avoid reaching for broad simplification when one rewrite communicates intent better.

## Induction Alignment
**When to use**: Property of recursive data or a recursive computation.

**How**:
1. Inspect the recursive definition and constructors.
2. Induct on the argument that actually decreases.
3. If the IH is over-specialized, `revert` or `generalize` dependent values before induction.
4. If the proof follows the recursive function's branches, use `fun_induction`.

**Trade-offs**: Generalization yields stronger, more useful IHs but increases quantified context.

## Indexed Family Preservation
**When to use**: Constructors constrain indices, or ordinary `cases` causes dependent hypotheses to disappear/mis-type.

**How**: Preserve indices in the motive; use dependent pattern matching or the generated recursor; use inaccessible patterns for terms forced by indices; revert dependent hypotheses before case splitting if required.

**Trade-offs**: More explicit motives/patterns; prevents impossible branches and lost equalities.

## Structural → Well-Founded Recursion
**When to use**: Termination checker rejects a mathematically terminating definition.

**How**:
1. Try to expose structural recursion by refactoring.
2. Choose a measure or well-founded relation with `termination_by`.
3. Prove each recursive call decreases with `decreasing_by`.
4. Strengthen the measure if one branch cannot be proved decreasing.

**Trade-offs**: Well-founded recursion adds proof obligations and may make definitional reduction less direct.

## Type-Class Debug Pipeline
**When to use**: `failed to synthesize` or unexpected instance/coercion.

**How**:
1. Make class input types concrete.
2. Confirm local/scoped instances are active.
3. Try `inferInstance` or `inferInstanceAs` for the exact class.
4. Trace `Meta.synthInstance` to see search branches.
5. Inspect priorities and instance chains only after inputs are known.

**Trade-offs**: Explicit local instances can stabilize a call site but can hide a poor global class design if overused.

## Quotient Lift
**When to use**: Define a function/property on equivalence classes.

**How**: define the representative function → prove it respects the relation → lift with `Quot.lift`/`Quotient.lift` → use quotient induction for proofs.

**Trade-offs**: Respectfulness is mandatory; a convenient representative computation is unusable if equivalent representatives can yield unequal outputs.

## Constructive → Classical Boundary
**When to use**: A proof requires excluded middle, contradiction, or selecting data from pure existence.

**How**: keep constructive evidence when available; use `Classical.em`/`byCases`/`byContradiction` for proposition-level branching; use choice only when data selection is logically required; mark choice-dependent data definitions `noncomputable`.

**Trade-offs**: Classical proof reasoning is convenient; choice-based data loses general executable content.

## Soundness and Computation Audit
**When to use**: Before declaring a proof/definition finished.

**How**: remove unfinished placeholders → inspect axiomatic dependencies when relevant → distinguish kernel reduction from compiled evaluation → check whether choice/extensional casts affect computation → state limits explicitly.

**Trade-offs**: Adds a validation pass; catches false claims about constructivity, normalization, or executable behavior.
