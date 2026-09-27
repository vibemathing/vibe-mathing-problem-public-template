# Chapter 2: Types, Proof Terms, and the Proof-State Loop

## Core Idea

Dependent type theory turns many informal ambiguities into explicit typing obligations. Propositions behave as types and proofs as terms. This viewpoint is useful operationally: a theorem declaration states a type, and the proof task is to construct a term of that type while Lean continuously shows the remaining obligations.

## Frameworks Introduced

### Type-first disambiguation

When notation or prose is unclear, ask “what is the type of every object here?” before asking which theorem to apply. The same symbol may denote operations in naturals, integers, reals, groups, modules, functions, or sets. Hidden coercions can make a line look mathematically obvious while Lean sees a different term.

Practical sequence:
1. identify the type of each variable;
2. identify the structure supplying each operation;
3. inspect inferred coercions and instances;
4. restate the goal with one ambiguous component made explicit;
5. only then search the library.

### Proposition-as-type

Use the Curry–Howard correspondence as a tactic guide:

- a proof of `P → Q` is a function taking a proof of `P` to a proof of `Q`;
- a proof of `∀ x, P x` accepts an arbitrary `x` and returns a proof of `P x`;
- conjunction has constructor data for both sides;
- disjunction is built by choosing a side;
- false has no constructors, so from false any proposition follows through its eliminator.

This explains the behavior of `intro`, `apply`, `exact`, `split`, `left`, `right`, `cases`, and `exfalso` without memorizing them as unrelated commands.

### Proof-state loop

Treat the interactive state as working memory supplied by the prover:

1. Read the exact target and local context.
2. Predict one structural transformation.
3. Apply it.
4. Confirm the new state matches the prediction.
5. Repeat until the remaining goal belongs to a known API or decision procedure.

On difficult research proofs, seeing only one or two steps ahead is acceptable. The source's Liquid Tensor reports show that the assistant can help humans navigate proofs whose global object graph exceeds working memory.

## Mental Models

**A hypothesis is a term.** If `h : P → Q` and `hp : P`, then applying `h` to `hp` creates a proof of `Q`. `apply h` works backwards from a desired conclusion; `exact h hp` works forwards with a completed term.

**The goal state is executable documentation.** Tactic scripts alone can be hard to read because they omit intermediate states. For explanation or debugging, reconstruct the state transitions. Human-readable proof documents should cross-link statements, local goals, and code.

**Types are diagnostic instruments.** Formalization does not merely encode a finished paper argument; it can reveal that two things casually identified on paper live in different structures or depend on different hypotheses.

## Anti-patterns

- Memorizing a long tactic list without understanding goal shape.
- Copying a proof term whose variable types are only “morally” the same.
- Taking a type mismatch as evidence that the mathematics is deep before checking coercions and scopes.
- Hiding every intermediate step behind automation while the route is still unknown.

## Validation Checkpoint

After each structural step, read the elaborated goal literally. Confirm that introduced variables have the types you expected and that implicit structure has not changed the problem. When a term almost fits, compare its full type with the goal before adding casts or automation. A useful local invariant is: every tactic should have a mathematical reason you can state in ordinary language. If the next proof-state transformation cannot be predicted, make the step smaller or expose an intermediate `have`; this keeps elaboration feedback diagnostic rather than mysterious.

## Key Takeaways

Use types to expose assumptions, proof terms to understand logic, and the proof state as a disciplined feedback loop. Explicit local progress should precede aggressive automation when the proof architecture is uncertain.

## Connects To

Tactic selection: [03](ch03-proof-construction-and-tactic-selection.md). Equality failures: [04](ch04-equality-rewriting-and-normalization.md). Inductive eliminators: [05](ch05-induction-recursors-and-quotients.md).
