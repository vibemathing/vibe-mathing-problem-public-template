# Chapter 1: Foundations and Early Type Theory

**Source coverage**: Preface and §§1-1.1, printed pp. 967-969.

## Core Idea
Classical type theory extends first-order logic by assigning every entity a type and permitting variables and quantification at arbitrarily high orders. The source uses an early Russell-style system to expose the extra proof-theoretic machinery before moving to Church's lambda-based presentation.

## Frameworks Introduced
- **Order hierarchy**
  - When to use: when checking whether a formula stays first-order or requires genuinely higher-order objects.
  - How: individuals are order 0; truth values are order 1; relation types have order one plus the maximum order of their argument types. Quantifying over higher-order variables is one of the defining extensions beyond first-order logic.
- **Leibniz equality**
  - When to use: when equality is represented definitionally rather than by a primitive equality symbol.
  - How: two entities are equal when every property holding of one also holds of the other. This definition itself requires quantification over properties.
- **Comprehension**
  - When to use: when a proof or formalization needs a set/relation whose membership condition is given by a formula.
  - How: assert the existence of an object representing that condition at the appropriate type.
- **Extensionality**
  - When to use: when two truth values, predicates, relations, or functions should be identified by their observable behavior.
  - How: equality at a higher type follows from agreement on arguments; proposition-level extensionality identifies equivalent truth values.

## Key Concepts
- **simple type theory**: the non-ramified typed framework used for the remainder of the chapter.
- **higher-order logic**: type theory viewed as a logic extending first-order logic.
- **type symbol**: a syntactic name for a domain of entities.
- **order**: the level induced by the type structure.
- **wff**: a well-formed formula/expression of the relevant type.
- **propositional variable**: a variable of truth-value type.
- **individual variable**: a variable of the individual type.
- **comprehension axiom**: an existence principle for a property/relation described by a formula.
- **extensionality axiom**: a principle identifying objects that agree extensionally.

## Mental Models
- Use the **type ladder** when deciding what a proof search must quantify over: predicates of individuals already push beyond first-order quantification.
- Think of **Leibniz equality** as a reduction from identity to indistinguishability by all properties.
- Treat **comprehension + extensionality** as a pair: comprehension creates typed predicates/functions; extensionality controls when such objects count as equal.

## Anti-patterns
- **Calling a formula first-order because its surface syntax looks relational**: higher-order quantification or variables in predicate position change the search problem.
- **Ignoring type annotations during search**: this discards information that can rule out many impossible substitutions.
- **Importing ramification constraints into simple type theory without a reason**: the chapter deliberately shifts to simple type theory for practical formalization.

## Reference Tables

| Feature added beyond first-order logic | Operational consequence |
|---|---|
| Variables of arbitrarily high orders | Search may require predicate/function variables, not only individuals |
| Quantification at all types | Instantiation can require structured higher-order terms |
| Comprehension | Predicates/functions described by formulas can be represented internally |
| Extensionality | Equality may require reasoning about behavior on all arguments |

## Worked Example
Suppose equality on individuals is represented through properties. To prove two individual terms `a` and `b` equal under Leibniz equality, the proof obligation becomes: every predicate `P` that holds of `a` also holds of `b`. This reframes equality as a higher-order statement because `P` itself is quantified. The example shows why equality can introduce higher-order search even when `a` and `b` are first-order-looking terms.

## Key Takeaways
1. Identify the highest-order variables before selecting a proof procedure.
2. Use types as hard constraints on legal substitutions and applications.
3. Expect comprehension and extensionality to introduce proof obligations unavailable in pure first-order logic.
4. Treat equality definitions as part of the search architecture, not as cosmetic notation.

## Connects To
- **Ch 2**: Church's lambda notation turns comprehension into an operational term language.
- **Ch 8**: higher-order unification works on typed lambda terms.
- **Ch 12**: extensional resolution handles extensionality directly in proof search.
