# 03 — First-Order Logic and Statement Formalization

## Core Idea

Translate mathematics by recovering its **operator tree**, then prove it by following the introduction/elimination rule of the outermost constructor. Natural-language ambiguity is handled before tactic selection.

## Operator-tree method

Given a statement:

1. identify object variables and their types;
2. identify explicit and implicit hypotheses;
3. identify the conclusion;
4. split each clause into smaller blocks;
5. find the main operator of each block (`→`, `↔`, `∧`, `∨`, `¬`, `∀`, `∃`, `=`...);
6. recurse until leaves are atomic predicates/expressions;
7. rebuild the tree as Lean syntax.

A common source of mistakes is compressed mathematical language. For example, “for every positive ε” means a universal variable plus an implication/ordered hypothesis, and “there exists N with property...” introduces both a witness and its property.

Use a namespace for local pedagogical definitions when their names may collide with Mathlib.

## Logic as constructors and functions

### Implication and universal quantification

Target:

```lean
⊢ P → Q
```

Introduce a proof of `P`, then prove `Q`:

```lean
intro hp
```

Likewise `∀ x, R x` introduces an arbitrary `x`.

Hypothesis:

```lean
h : P → Q
```

can be used as a function. `apply h` turns a goal `Q` into goal `P`; direct term application `h hp` constructs `Q` when `hp : P` is already present.

A universal hypothesis `h : ∀ x, R x` is also a dependent function; instantiate it with `h a`.

### Conjunction

Target `P ∧ Q`: construct both fields.

```lean
constructor
-- goals P and Q
```

or use `refine ⟨?_, ?_⟩` / an explicit `And.intro`.

Hypothesis `h : P ∧ Q`: project `h.1`, `h.2` / `h.left`, `h.right`, or destruct it:

```lean
rcases h with ⟨hp, hq⟩
```

Choose projections/`have` if keeping `h` is useful; `rcases` is cleaner when only the fields matter.

### Disjunction

Target `P ∨ Q`: choose the branch you can prove. Prefer explicit constructors in maintainable proofs:

```lean
apply Or.inl
-- goal P
```

Hypothesis `h : P ∨ Q`: both possibilities must establish the same final goal:

```lean
rcases h with hp | hq
· ...
· ...
```

### Existential quantification

Target `∃ x, R x`: supply a witness and prove its property.

```lean
refine ⟨witness, ?_⟩
```

or `exists witness`.

Hypothesis `h : ∃ x, R x`: extract witness and evidence:

```lean
rcases h with ⟨x, hx⟩
```

For nested existentials/structures, `rcases` patterns can destruct recursively.

### Negation and contradiction

`¬P` is function-like: `P → False`. To prove it, `intro hp` and derive `False`.

If both `P` and `¬P` are present, contradiction closes any proposition. When a direct route is awkward and classical reasoning is intended:

- `by_contra h` changes proof of `P` into deriving contradiction from `¬P`;
- `by_cases h : P` creates `P` and `¬P` branches;
- `contrapose`/`contrapose!` can transform implication-like reasoning.

Record the logical dependency: classical case splits use excluded-middle principles.

## Proof-state direction

A tactic transforms the current goal into obligations sufficient to reconstruct it. This direction runs “backward” from the final theorem toward simpler subgoals, while the eventual proof term is synthesized “forward” from solved leaves.

This explains why `apply theorem` is so useful: it unifies the theorem's conclusion with the current goal and exposes the theorem's unsatisfied premises as subgoals.

## `have` as a cut

When an intermediate proposition will simplify the rest of the proof:

```lean
have hmid : P := by
  ...
-- hmid is now available
```

This is the operational form of introducing a lemma/cut. Use it to keep proof states small and to expose reusable facts to automation.

## Worked Example — formalize a limit-uniqueness statement

For a simple epsilon-style sequence limit definition:

1. represent a sequence as `Nat → Real`;
2. define “has limit a” as a proposition with `∀ ε > 0, ∃ N, ∀ n > N, ...`;
3. state uniqueness with sequence and two candidate limits as parameters, two limit proofs as hypotheses, equality as target;
4. prove by contradiction if using the course blueprint;
5. reduce `a ≠ b` to an ordered case (possibly using symmetry/`wlog`);
6. unfold the local limit definition;
7. choose a positive epsilon from `a-b`;
8. instantiate both universal hypotheses and destruct their existential witnesses;
9. choose an index exceeding both bounds;
10. extract the two inequalities and discharge the contradiction with linear arithmetic.

The reusable lesson is the **shape sequence**: classical reduction → definition exposure → quantified instantiation → witness extraction → common index → arithmetic contradiction.

## Failure modes

- **Statement is hard to prove because it was mistranslated:** rebuild the operator tree before changing tactics.
- **Bound variables have wrong scope:** make quantifier nesting explicit.
- **`apply` creates surprising goals:** inspect the complete theorem type and implicit parameters.
- **Case split duplicates a symmetric proof:** use a valid symmetry reduction (`wlog`) only when you can prove the omitted case reduces to the chosen one.
- **Destructing loses a hypothesis you later need:** use projections/`have` or duplicate the useful information before `rcases`.

## Key Takeaways

Logical syntax is executable proof guidance. The goal's outer form tells you how to introduce it; a hypothesis's outer form tells you how to eliminate/use it.

## Connects To

- Underlying constructor definitions → [ch05](ch05-dependent-types-term-construction.md)
- Tactic variants and caveats → [ch06](ch06-tactic-construction.md)
- Full blueprint/Search example → [ch04](ch04-mathlib-search-sets-blueprints.md)
