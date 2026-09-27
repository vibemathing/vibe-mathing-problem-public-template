# Patterns and Procedures

## 1. Source-Phase Routing
**When to use**: a goal has a familiar mathematical name but theorem search returns mismatched types.  
**How**:
1. Locate the source section.
2. Identify whether it uses a custom object, a bridge, or native Mathlib.
3. Stay inside that phase for the local proof.
4. Cross an epilogue/bridge only once, then continue on the destination side.  
**Trade-off**: custom proofs are longer but preserve the companion's pedagogy; Mathlib proofs are shorter after the intended migration point.

## 2. Faithful `sorry` Reconstruction
**When to use**: filling an exercise `sorry`.  
**How**:
1. Translate the theorem statement to a paper proof.
2. List only preceding definitions/lemmas needed by that proof.
3. Encode the logical skeleton with `intro`, `obtain`, `have`, `constructor`, `calc`, or induction.
4. Use local automation for arithmetic/rewrite subgoals.
5. Audit for accidental use of a later theorem or a theorem whose source proof is itself the target exercise.  
**Failure signal**: a one-line imported theorem solves the goal but bypasses the section's central construction.

## 3. Totalization Guard
**When to use**: `LIM`, `lim`, generalized sums, roots, one-sided limits, `derivWithin`, Riemann–Stieltjes helpers, or supplemental integrals.  
**How**: prove convergence/measurability/nonzero/sign/domain hypotheses first; only then use evaluation/uniqueness laws.  
**Failure signal**: an unexpected `0` or other default appears without contradiction.

## 4. Index-Shift Normalization
**When to use**: book statement starts at 1 while Lean uses `ℕ`/`Fin` from 0.  
**How**:
1. State the map (`n ↦ n+1`, shifted `Fin`, `Sequence.from`).
2. Prove bound/monotonicity properties.
3. Rewrite the finite sum/sequence term under the map.
4. Perform algebra only after index ranges match.  
**Trade-off**: a small upfront lemma eliminates repeated off-by-one side goals.

## 5. Epsilon-to-Filter Escalation
**When to use**: direct ε proofs become repetitive or need composition.  
**How**: use the section's equivalence with `Filter.Tendsto`; apply native limit/continuity composition; convert back only for a chapter-level target.  
**Failure signal**: repeated manual merging of many δ/N witnesses with no new mathematical content.

## 6. Extended-Real Escalation
**When to use**: sup/inf/limsup/liminf or ratio/root values may be infinite.  
**How**: formulate the order statement in `EReal`; prove inequalities/finiteness there; coerce to `ℝ` only after ruling out `⊤`/`⊥`.  
**Failure signal**: a real supremum theorem demands a bound that is mathematically unavailable.

## 7. Quotient-Lift Workflow
**When to use**: Chapter 4 or 5 constructed numbers.  
**How**: define on representatives → prove compatibility with equivalence → descend to quotient → prove algebraic laws with the quotient API.  
**Failure signal**: trying to show quotient equality from literal representative equality.

## 8. Series via Partial Sums
**When to use**: any infinite-series identity or convergence result.  
**How**: prove finite partial-sum identity → establish convergence/tail bound → pass to limit. For rearrangement, add absolute/nonnegative convergence and index bijection.  
**Failure signal**: manipulating an infinite sum as a ring expression before proving convergence.

## 9. `Summable`/`tsum` Migration
**When to use**: Section 8.2 onward or arbitrary indexed sums.  
**How**: prove `Summable`; use `tsum`, subtype/indicator lemmas, and the source bridge from custom absolute convergence.  
**Failure signal**: custom `Sum'` is used where convergence has not been established.

## 10. Within-Derivative Workflow
**When to use**: Chapter 10 differentiation.  
**How**: target `HasDerivWithinAt` → compose calculus-rule lemmas → use limit-point assumptions for uniqueness → derive `derivWithin` only at the end.  
**Failure signal**: `derivWithin = 0` is being treated as proof that the derivative exists.

## 11. Riemann Integrability Routing
**When to use**: Chapter 11.  
**How**: choose regularity route (uniformly continuous/continuous/monotone/piecewise continuous) or construct upper/lower approximations; after `IntegrableOn`, use closure laws.  
**Failure signal**: repeatedly unfolding upper/lower integrals for simple algebraic combinations.

## 12. Dimensioned Scalar Normalization
**When to use**: `Scalar d` algebra in `UnitsSystem`.  
**How**: resolve dimension equality → `simp [← toFormal_inj]` → `ring`; alternatively `simp [← val_inj]` for coordinate reasoning. Use `Scalar.cast` when propositionally equal dimensions remain different types.  
**Failure signal**: commutativity is mathematically obvious but the result types differ.

## 13. Coercion Diagnostic Ladder
**When to use**: “type mismatch” with an apparently correct theorem.  
**How**: classify: custom/Mathlib, set/subtype, quotient/representative, Real/EReal/ENNReal, dimension index, index origin. Then use the matching bridge. Try `change`, `simpa`, `convert`, `norm_cast`, `ext` only after classification.  
**Trade-off**: diagnosis takes seconds and prevents long blind theorem searches.

## 14. Proof Quality Validation
**When to use**: before returning Lean code.  
**How**: verify all hypotheses, index/domain conventions, totalization guards, source phase, theorem dependency order, and user-requested proof style. If no Lean compiler is available, clearly mark the code uncompiled and identify API-sensitive names.
