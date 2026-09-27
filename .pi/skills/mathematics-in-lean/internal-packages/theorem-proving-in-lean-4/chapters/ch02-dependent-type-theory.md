# Chapter 2: Dependent Type Theory

## Core Idea
Lean's elaborator and kernel work over a typed term language whose expressive power comes from functions, universes, and dependency. Effective Lean work depends on understanding where type information comes from and how much the elaborator can infer.

## Frameworks Introduced
- **Types first**
  - When to use: before proving or debugging any Lean expression.
  - How: determine the expression's type with `#check`; use expected types and local annotations to constrain elaboration.
- **Function-space construction**
  - When to use: represent computations, implications, parameterized definitions, and quantification.
  - How: build function types with `→` or dependent arrows, then inhabit them with lambdas or named definitions.
- **Universe-polymorphic abstraction**
  - When to use: definitions should work uniformly across types living at different universe levels.
  - How: use universe variables and let Lean compute the resulting universe constraints.
- **Elaboration through omitted arguments**
  - When to use: declarations have predictable type parameters or evidence that can be inferred.
  - How: mark arguments implicit; provide explicit values, expected types, or `@`-expanded calls when inference stalls.

## Key Concepts
- **Simple function type** `α → β`: output type does not depend on the input value.
- **Dependent function type** `(x : α) → β x`: result type can mention the input.
- **Lambda abstraction** `fun x => t`: creates a function term.
- **Application** `f a`: consumes a function term.
- **Definitional equality**: equality recognized by reduction/unfolding rather than a separate theorem.
- **Universe** `Type u`: level in Lean's hierarchy of types.
- **`Prop`**: proposition universe, later connected to proof irrelevance and impredicativity.
- **Section variable**: parameter that Lean automatically includes in declarations when the declaration actually depends on it.
- **Namespace**: hierarchical naming mechanism for avoiding collisions and grouping declarations.
- **Implicit argument** `{x : α}`: parameter Lean tries to infer.
- **Metavariable**: inference placeholder that must be solved from typing constraints.
- **Sigma type** `Σ x : α, β x`: dependent pair whose second component's type depends on the first.

## Mental Models
- Use **bidirectional information flow**: explicit arguments constrain implicit ones, while the expected result type can constrain earlier missing information.
- Think of `def` as giving a **named typed term** whose body may unfold during elaboration/reduction according to reducibility rules.
- Treat universe levels as **consistency and polymorphism infrastructure**, not decorative annotations.
- Use dependent types when the output type itself should encode a relationship to the input; use ordinary products/functions when no such dependency is needed.

## Anti-patterns
- **Guessing an implicit parameter** when Lean reports a stuck metavariable: first inspect the full declaration and add a minimal annotation.
- **Making every argument explicit permanently**: this can obscure the intended API and fight useful elaboration.
- **Assuming `Type : Type`**: Lean uses a universe hierarchy; definitions may have nontrivial level constraints.
- **Confusing propositional equality with definitional equality**: a term may need an equality proof even when two expressions look mathematically equivalent.

## Code Examples
```lean
#check Nat
#check Nat → Nat
#check fun x : Nat => x + 1
#eval (fun x : Nat => x + 1) 4
```
- **What it demonstrates**: types classify terms; lambda terms can be checked and evaluated.

```lean
universe u v

def compose {α : Type u} {β : Type v} {γ : Type _}
    (g : β → γ) (f : α → β) : α → γ :=
  fun x => g (f x)

#check compose
#check @compose
```
- **What it demonstrates**: universe polymorphism, implicit type parameters, and using `@` to expose them.

```lean
def depPair : Sigma (fun n : Nat => Fin (n + 1)) :=
  ⟨2, ⟨1, by decide⟩⟩
```
- **What it demonstrates**: the type of the second component depends on the first component.

## Reference Tables
| Need | Preferred mechanism | Failure signal | Repair |
|---|---|---|---|
| inspect inferred type | `#check term` | output surprises you | add type ascription / inspect declaration |
| inspect implicit parameters | `#check @name` | metavariable stuck | pass selected implicit/named args |
| local reusable expression | `let x := ...` | repeated term noise | name it locally |
| reusable global definition | `def` | repeated logic across contexts | abstract parameters explicitly |
| dependent result type | `(x : α) → β x` | ordinary arrow loses relation | introduce dependency |
| polymorphic type level | universe variables | level mismatch | inspect universe constraints rather than fixing arbitrary levels |

## Worked Example
A common elaboration failure occurs when a polymorphic operation has too little context. Suppose Lean sees a function with implicit type argument `{α}` and a term whose type does not constrain `α` enough. Instead of immediately rewriting the whole expression:
1. Run `#check @theFunction` to see all hidden parameters.
2. Find which metavariable is underconstrained.
3. Add an expected type around the result or annotate one explicit input.
4. If needed, pass the implicit with `(α := Nat)` or another named argument.
5. Re-check the term; remove unnecessary explicit arguments after the minimal constraint is clear.

This pattern scales to overloaded numerals, polymorphic constructors, and type-class calls in later chapters.

## Key Takeaways
1. Every proof/debugging task is constrained by the types Lean actually elaborates.
2. Expected types are active inputs to elaboration; use them strategically.
3. Dependency lets types express relationships that ordinary function/product types cannot.
4. Universe polymorphism is part of Lean's sound type architecture.
5. Implicit arguments improve APIs only when enough information exists to infer them.
6. `#check` and `@` form a fast diagnostic pair for elaboration problems.

## Connects To
- **Ch 3**: `Prop` turns this typed term language into a proof language.
- **Ch 4**: universal quantification is dependent function space, and equality is an inductive type.
- **Ch 6**: expands the inspection and elaboration diagnostics.
- **Ch 7–8**: dependent types support indexed inductive families and dependent pattern matching.
- **Ch 10**: instance implicits extend elaboration with type-class search.
