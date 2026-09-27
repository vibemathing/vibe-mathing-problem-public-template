# Chapter 2: Church Type Theory with Lambda Notation

**Source coverage**: §1.2, printed pp. 969-973.

## Core Idea
Church's formulation makes functions first-class typed objects and uses lambda abstraction to name functions, sets, relations, and definitions directly. Proof search therefore operates on typed lambda terms and must normalize after substitution.

## Frameworks Introduced
- **Function type `(alpha beta)`**
  - When to use: whenever an expression maps inputs of type `beta` to outputs of type `alpha`.
  - How: application associates to the left, so multi-argument functions can be represented by functions returning functions.
- **Lambda abstraction**
  - When to use: to construct a function, predicate, set, or relation from an expression with a free variable.
  - How: `lambda x. A` denotes the function sending `x` to `A`; sets are predicates returning truth values.
- **Lambda conversion / beta normalization**
  - When to use: after applying a lambda abstraction or after a substitution changes a term's reducible structure.
  - How: replace `(lambda x. A) B` by the capture-avoiding substitution of `B` for free occurrences of `x` in `A`, then normalize.
- **Elementary type theory J**
  - When to use: when studying proof search for propositional connectives, quantifiers, and lambda conversion without extensionality and description axioms.
  - How: distinguish this core from the fuller system C; many automated-search results in the chapter target J.

## Key Concepts
- **function type**: a type whose elements map one typed domain to another.
- **application**: applying a function-valued wff to an argument.
- **abstraction**: binding a variable to form a function.
- **bound/free occurrence**: whether a variable occurrence is controlled by an abstraction.
- **closed wff / sentence**: an expression with no free variables; a sentence is a closed truth-valued wff.
- **free for**: a capture-avoidance condition on substitution.
- **alpha-conversion**: renaming a bound variable safely.
- **beta-contraction**: reducing an applied lambda abstraction.
- **beta-normal form**: a canonical representative with no beta redexes after allowed alpha changes.
- **description operator**: an operator selecting the unique object satisfying a predicate when one exists.

## Mental Models
- Think of **sets as characteristic functions**: a set of `alpha`-objects is a function `alpha -> truth`.
- Think of **relations as curried functions**: a binary relation needs no special primitive if functions may return predicates.
- Use **normalization as semantic bookkeeping**: compare and unify terms after their obvious lambda computations are performed.

## Anti-patterns
- **Comparing lambda terms syntactically before normalization**: beta-equivalent terms can look different.
- **Substituting without capture checks**: a free variable can become accidentally bound and change meaning.
- **Assuming extensionality/descriptions are present when using a J-oriented method**: those principles belong to the stronger system C.

## Reference Tables

| Construct | Operational reading |
|---|---|
| `o` | type of truth values |
| `iota` (often written `ι`) | type of individuals |
| `(alpha beta)` | functions from `beta` to `alpha` |
| `lambda x_beta. A_alpha` | a function of type `(alpha beta)` |
| predicate/set on `alpha` | a function of type `(o alpha)` |
| beta-normalization | reduce lambda applications after substitution |

## Worked Example
The source uses the function `lambda n. n^2 + 3`. Applying it to `5` reduces by beta-contraction to `5^2 + 3`, hence `28`. The small example carries the full operational lesson for proof search: application creates a reducible term; normalization should occur before deciding whether two terms match, unify, or simplify.

The chapter also illustrates definitional abstraction with transitive closure and natural numbers. A prover can treat a named relation such as `TRANSITIVE-CLOSURE` as an abbreviation backed by a rewrite rule, instantiate the abbreviation when useful, and beta-normalize the result. Selective unfolding matters because eager expansion can enlarge the search space dramatically.

## Key Takeaways
1. Model functions, sets, and relations uniformly as typed functions.
2. Normalize after substitution and definition unfolding.
3. Preserve capture-avoidance conditions during every substitution.
4. Keep track of whether the current target logic is J or the fuller system C.
5. Use abbreviations as controlled search interfaces; unfold them selectively.

## Connects To
- **Ch 4**: abbreviations and recursive definitions exploit this function language.
- **Ch 8**: higher-order unification is defined modulo lambda normalization.
- **Ch 12**: extensional resolution adds the principles omitted from J.
