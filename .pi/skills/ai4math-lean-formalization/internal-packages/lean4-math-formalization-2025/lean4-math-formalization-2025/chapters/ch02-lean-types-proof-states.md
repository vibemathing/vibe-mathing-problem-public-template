# 02 — Lean Types and Proof States

## Core Idea

Lean interaction is easiest when every question is translated into: **what term is available, what type does it have, and what type must be constructed next?** InfoView makes this loop visible.

## Working interface

In the usual VS Code setup:

- File Explorer locates project files;
- Code Editor contains Lean source;
- Lean InfoView shows context-sensitive information;
- tactic state shows hypotheses/variables and goals;
- Messages shows errors, warnings, completed goals, `#check` output, and search suggestions.

When debugging, put the cursor at the exact proof step that first creates the surprising state. Later errors often cascade from that point.

## Terms and types

A judgment has the form `a : A`: term `a` has type `A`.

Use:

```lean
#check expr
#eval computableExpr
```

Do not assume every visible piece of Lean syntax is itself a term. Commands, declaration punctuation, and overloaded notation live partly at the language/meta level. When `#check +` or similar surface notation is unhelpful, inspect the underlying declaration or class instead.

### Definitions

```lean
def n : Nat := 1

def succ' (n : Nat) : Nat := n + 1

def succ'' : Nat → Nat := fun n => n + 1
```

Function application uses whitespace: `f a`. Function arrows associate to the right, so `A → B → C` means `A → (B → C)`.

### Dependent and implicit parameters

Later types may depend on earlier terms. Keep parameters in dependency order.

Lean can infer parameters declared with braces. When inference chooses poorly or cannot determine one, supply a named argument such as `(a := value)`.

## Propositions as types

`Prop` is the universe of propositions. A proof of proposition `P` is a term whose type is `P`.

Consequences:

- a theorem declaration is a typed term declaration specialized to `Prop`;
- implication and universal quantification behave like function types;
- proving a theorem means constructing a term of the target proposition;
- existing theorems can be applied like functions.

`theorem` and `lemma` create named reusable declarations. `example` is anonymous/temporary. `axiom` introduces a proposition without a construction and should represent an intended assumption, not a proof shortcut.

## Term proof vs tactic proof

Term style constructs the proof directly. Tactic style starts with `by` and incrementally transforms goals until all are solved.

A proof state can be read schematically as:

```text
x₁ : T₁
...
h₁ : P₁
...
⊢ Goal
```

Conceptually, it is the type of a function from the available parameters/hypotheses to the target. A tactic step that replaces one goal by several new goals is promising: “give me proofs of these subgoals and I can synthesize the original proof.”

This viewpoint is the bridge to [ch03](ch03-first-order-logic-formalization.md) and [ch06](ch06-tactic-construction.md).

## First calculation tools

### `rw`

Use an equality/equivalence to replace a matching expression. Control direction and location:

```lean
rw [h]
rw [← h]
rw [h] at hx
rw [h] at *
```

If rewriting fails, check the exact occurrence and whether a definition needs exposure first.

### `calc`

Use for a readable transitive chain of equalities/inequalities:

```lean
calc
  a = b := step1
  _ = c := step2
```

Every link needs a relation whose transitivity is known. A failed `calc` step can therefore indicate a relation/direction problem rather than a missing mathematical fact.

### Focused automation

- `ring`: normalize polynomial identities in suitable commutative-ring structures;
- `linarith`: linear arithmetic from hypotheses;
- `simp`: rewriting using simplification lemmas plus supplied facts;
- `norm_num`: normalize concrete numeric expressions;
- `aesop`: proof search for many structural goals.

Use automation after the logical/structural shape is correct. If it fails, expose the missing structure manually rather than stacking more automation.

## Worked Example — read the goal as a function type

If InfoView shows `h : P` and goal `Q → P`, read the goal as a function waiting for evidence of `Q`. Introduce that argument, then return the already available proof `h`. In tactic form the state change is `intro hq` followed by `exact h`; at term level it is a lambda that ignores `hq`. Use this translation whenever a tactic step feels opaque.

## Diagnostic loop

1. Put cursor before the failing step.
2. Read the exact context and goal.
3. `#check` the theorem/function you intend to use.
4. Compare its result type to the target.
5. If overloaded notation is involved, inspect the underlying class/declaration.
6. Make one state-changing step.
7. Re-read InfoView.

## Failure modes

- **Treating notation as a primitive operation:** inspect its class/instance route.
- **Forgetting right-associative arrows:** parenthesize the Curry chain mentally.
- **Implicit argument confusion:** make the relevant argument explicit by name.
- **Automation on the wrong shape:** introduce quantifiers/destructure data/unfold the local definition first.
- **Reading only the error text:** the tactic state often tells you which premise or instance is actually missing.

## Key Takeaways

Lean proof development is a feedback loop around types. Read the state, perform a type-justified construction, then read the new state.

## Connects To

- Logic-shaped routing → [ch03](ch03-first-order-logic-formalization.md)
- Term semantics → [ch05](ch05-dependent-types-term-construction.md)
- Full tactic toolbox → [ch06](ch06-tactic-construction.md)
