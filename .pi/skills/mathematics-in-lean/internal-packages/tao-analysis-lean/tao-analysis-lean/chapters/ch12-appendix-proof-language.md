# Appendix A: Lean Proof Language for Analysis

## Core Idea

Appendix A teaches the logical mechanics needed to turn mathematical prose into Lean goals: propositions, implication, proof structure, variables, quantifiers, nested quantifiers, examples, and equality. It should be loaded when a mathematical idea is understood but the user is unsure how to express or decompose it in Lean.

## Frameworks Introduced

- **Goal-shape routing**: the outer logical connective determines the first tactic. Implication/universal quantifier → `intro`; conjunction/equivalence → `constructor`; existential → provide a witness; disjunction → choose a side; equality → rewrite/calculation/extensionality depending on structure.
- **Hypothesis-as-function**: a proof of `P → Q` is a function from evidence of `P` to evidence of `Q`. `intro h` and `exact hP h` are concrete manifestations of this view.
- **Contrapositive/contradiction routing**: when the forward implication is awkward, use a logically equivalent contrapositive only if it simplifies the available hypotheses. `by_contra` is useful when the negated target produces exploitable inequalities/equalities.
- **Quantifier order is semantics**: `∀ x, ∃ y, ...` and `∃ y, ∀ x, ...` require different witness strategies. Read nested quantifiers left to right and record which variables each witness may depend on.
- **Equality as rewriting interface**: use equality to transport expressions. Prefer `rw`/`simp` for local substitution, `calc` for readable chains, and `ext`/`funext` when equality is characterized pointwise.

## Key Concepts

- decidable propositions and examples;
- implication and contrapositive;
- proof blocks and intermediate `have` statements;
- explicit/implicit variables;
- universal and existential quantifiers;
- nested quantifier dependencies;
- equality, equivalence relations, quotient motivation.

## Operational Procedure

1. Read the goal's outermost connective before trying automation.
2. Introduce all assumptions/variables whose values are logically available at the current stage.
3. For an existential goal, decide the witness mathematically before entering tactic details; then prove its property.
4. For an existential hypothesis, use `obtain ⟨x, hx⟩ := h` or `rcases` to expose the witness.
5. For a nested quantifier theorem, annotate dependencies: a witness selected after `x` may depend on `x`; one selected before `x` may not.
6. For equality, decide whether the proof is definitional (`rfl`), rewrite-based, algebraic (`ring`/`linarith`), or extensional (`ext`/`funext`).
7. Use `calc` when the proof has a meaningful mathematical chain; it doubles as documentation and localizes failures.
8. Run simplification/automation only after the logical skeleton is correct.

## Decision Table

| Goal shape | First move |
|---|---|
| `P → Q` | `intro hP` |
| `∀ x, P x` | `intro x` |
| `P ∧ Q` | `constructor` |
| `P ↔ Q` | `constructor`; prove each direction |
| `∃ x, P x` | `refine ⟨witness, ?_⟩` |
| `False` from inconsistent hypotheses | `exact` contradiction / `linarith` / `omega` as appropriate |
| `f = g` for functions | `funext x` |
| structured objects equal by fields/membership | `ext` |

## Anti-patterns

- Calling `simp` before understanding a nested quantifier and then losing sight of witness dependencies.
- Using classical contradiction when a direct constructive proof is shorter and clearer.
- Rewriting in every occurrence blindly; target the equality direction that reduces complexity.
- Treating two logically equivalent proposition forms as definitionally equal.
- Hiding the main mathematical step inside large automation when a `have` or `calc` chain would expose it.

## Code Example

```lean
theorem witness_pattern (h : ∀ x, ∃ y, R x y) (x : α) : ∃ y, R x y := by
  obtain ⟨y, hy⟩ := h x
  exact ⟨y, hy⟩
```

This illustrates the dependency order: `y` may depend on the previously introduced `x`.

## Source Map

`Appendix_A_1` propositions; `A_2` implication/contrapositive; `A_3` proof structure; `A_4` variables/quantifiers; `A_5` nested quantifiers; `A_6` worked proof/quantifier examples; `A_7` equality and an equality/quotient-flavored construction.

## Key Takeaways

1. Logical form selects the tactic skeleton.
2. Quantifier order determines legal witness dependencies.
3. Equality proofs should use the abstraction appropriate to the object: rewrite, calculation, or extensionality.
4. Intermediate facts make both mathematical intent and Lean errors easier to diagnose.
5. Automation should discharge local obligations after the proof's logical architecture is explicit.

## Connects To

Every chapter: when a failure is syntactic/logical rather than mathematical, return here before searching for stronger theorems.
