# Chapter 3: The Axiom of Choice and Safe Skolemization

**Source coverage**: §1.3, printed pp. 973-975.

## Core Idea
Skolemization in higher-order logic can silently introduce the power of a choice function. If Choice is not part of the intended theory, Skolem symbols need explicit dependency discipline; otherwise a preprocessing step can strengthen the logic.

## Frameworks Introduced
- **Choice schema by type**
  - When to use: when the theory explicitly permits choosing an element from every nonempty predicate/set at a given type.
  - How: treat Choice as an extra logical principle whose use should remain visible.
- **Necessary-argument discipline for Skolem constants**
  - When to use: when refutational proof search introduces Skolem symbols but must avoid accidental Choice.
  - How: assign every Skolem constant an arity; every occurrence must supply those necessary arguments; free variables inside necessary arguments must not later be captured by binders in the containing formula.
- **Dependency-aware alternative**
  - When to use: when explicit Skolem terms become long or logically equivalent argument structures are hard to recognize.
  - How: track the dependency relation directly and permit only substitutions consistent with it.

## Key Concepts
- **Axiom of Choice**: an additional principle asserting the existence of suitable choice functions.
- **choice function**: a function selecting an element from a nonempty set/predicate.
- **Skolem constant/function**: a fresh symbol representing a witness chosen as a function of prior dependencies.
- **necessary argument**: an argument recording a dependency that a Skolem symbol must always carry.
- **capture**: binding a variable occurrence that was intended to remain free.
- **dependency relation**: a relation constraining which instantiation terms may depend on which selected parameters.

## Mental Models
- Treat a Skolem symbol as a **dependency ledger**: its necessary arguments record exactly what the witness was allowed to depend on when introduced.
- Use the **Choice contamination test**: if a Skolem function can be reused as a general selector for arbitrary predicates, preprocessing has likely added strength.
- Prefer dependency relations when explicit witness terms become an implementation burden.

## Anti-patterns
- **First-order-style Skolemization without higher-order restrictions**: a fresh function can serve as a choice operator and derive consequences the target system did not authorize.
- **Dropping necessary arguments because they look redundant**: this can erase semantic dependencies and make later substitutions unsound.
- **Allowing a variable free in a necessary argument to become bound later**: the witness dependency changes under capture.

## Reference Tables

| Situation | Safe action |
|---|---|
| Choice explicitly allowed | a typed choice operator / simple Skolemization may be acceptable |
| Choice should remain external | enforce arity + necessary-argument restrictions |
| Skolem terms become unwieldy | represent dependencies separately and constrain substitutions |
| New quantifiers appear inside expansion terms | expect Skolemization to continue during search, not only preprocessing |

## Worked Example
Consider a refutation step that conceptually has the shape `forall x. exists y. R(x,y)`. A first-order treatment introduces `Y(x)`. In higher-order logic the analogous witness may depend on higher-order instantiation terms, and treating `Y` as an unrestricted function can make it act like a universal chooser. The safe version fixes the arity and insists every occurrence of `Y` carries the dependency arguments that justified the witness. If one of those arguments contains a free variable `z`, subsequent formula construction must not bind that occurrence of `z`.

## Key Takeaways
1. Decide whether Choice is permitted before Skolemizing.
2. Record Skolem dependencies explicitly; never infer them retrospectively.
3. Prevent capture of variables occurring inside necessary arguments.
4. Prefer dependency-aware instantiation when explicit Skolem terms obstruct search.
5. Treat Skolemization as a semantic transformation, not a purely syntactic convenience.

## Connects To
- **Ch 6**: expansion proofs encode dependency conditions directly.
- **Ch 11**: constrained resolution may use a Choice-permitting Skolemization when that assumption is acceptable.
- **Ch 12**: extensional resolution also uses clause-specific Skolem terms.
