# Appendix Skill Layer 1: Mathematical Background

**Source coverage**: Harrison Appendix 1, book pp. 593–602.

## Core Idea
The book's algorithms repeatedly rely on a small mathematical toolkit: sets/functions/relations, inductive definitions, closures, well-founded induction, and order constructions. These concepts are operational proof obligations for termination and correctness, not decorative background.

## Frameworks Introduced
### Sets, functions, and finite combinatorics
Use set language deliberately:
- membership, subset, union/intersection/difference;
- Cartesian products and power sets;
- functions with explicit domain/codomain/range;
- injections, surjections, bijections;
- finite and countable cardinality.

In implementations, mathematical sets may be represented as sorted duplicate-free lists. Verify that list equality/order behavior does not accidentally replace extensional set equality.

### Relations and closures
For a binary relation `R` distinguish:
- reflexive/symmetric/transitive properties;
- equivalence relations and equivalence classes;
- partial/total orders;
- reflexive transitive closure `R*` and transitive closure `R+`.

This vocabulary underlies rewrite reachability, congruence, proof search, and graph encodings.

### Inductive definitions as least fixed points
A set defined by closure rules can be seen as the least set closed under those rules.

Operational proof principles:
1. **Rule induction**: To show every generated object has property `P`, prove `P` is preserved by each generating rule.
2. **Cases/inversion**: To reason about an element of the least fixed point, analyze the rules that could have generated it.
3. **Monotone fixed point**: If an operator on sets is monotone, its least fixed point captures repeated closure from below.

Use this model for reachable states, syntax trees, derivations, and semantic closure operations.

### Well-foundedness and induction
Equivalent working views:
- every nonempty subset has a minimal element;
- there is no infinite descending chain;
- well-founded induction is valid.

**Termination pattern**:
1. Choose a measure/order on states.
2. Prove every recursive/rewrite step strictly decreases it.
3. Invoke well-foundedness to exclude infinite execution.

### Building well-founded orders
The appendix highlights reusable constructions:
- natural-number measures;
- lexicographic product orders;
- multiset extensions;
- subrelations and related closure facts.

These feed directly into termination orderings for rewriting and recursive algorithms.

## Key Concepts
- **Relation**: Set/predicate on pairs.
- **Equivalence relation**: Reflexive, symmetric, transitive relation.
- **Partial order**: Reflexive, antisymmetric, transitive relation.
- **Well-order**: Total well-founded order.
- **Monotone operator**: Preserves set inclusion.
- **Least fixed point**: Smallest `X` satisfying `F(X)=X` or closure condition.
- **Structural induction**: Induction following constructors of a recursively defined datatype.
- **Complete induction**: Prove a natural-number case assuming all smaller cases.

## Mental Models
- **Termination = descent in hidden mathematics**: A recursive function terminates because some well-founded measure decreases, even if code does not display that measure explicitly.
- **Induction mirrors construction**: Prove facts in the same shape objects are generated.
- **Closure is repeated inference**: Reachability, congruence closure, and deductive closure are all least-fixed-point computations.

## Anti-patterns
- **“It gets smaller” without defining an order**: Informal size intuition is insufficient for a termination proof.
- **Using a non-well-founded ordering as a rewrite orientation**: Local decreases can still permit infinite chains.
- **Confusing element order with multiset/lexicographic order**: Each lifting has its own proof obligations.
- **Treating implementation lists as mathematical sets without duplicate/order discipline**: Breaks extensional reasoning.

## Code Examples
Termination proof pattern:

```text
measure : State -> Nat
for every transition s -> s':
    prove measure(s') < measure(s)
therefore no infinite transition chain exists
```

Least fixed-point closure:

```text
X := initial
repeat:
    X' := X union consequences(X)
until X' == X
return X
```

## Reference Tables
| Mathematical tool | Used later for |
|---|---|
| equivalence relation | congruence classes, union-find, Stålmarck equivalences |
| reflexive-transitive closure | rewriting/search reachability |
| least fixed point | inductive syntax, least Herbrand model, closure computations |
| well-founded induction | termination of recursion and rewriting |
| lexicographic/multiset orders | term/rewrite order construction |
| finite/cardinality reasoning | finite model search, truth valuations, combinatorial encodings |

## Worked Example
To prove a recursive parser terminates, define the measure as the number of unconsumed tokens plus a structural submeasure for the active grammar level. Each successful consuming call strictly decreases token count; calls that only switch grammar levels descend through a finite grammar hierarchy before consumption. This turns “the parser obviously progresses” into a checkable well-founded argument.

## Key Takeaways
1. State the mathematical structure your algorithm relies on.
2. Use least-fixed-point reasoning for inductive closures.
3. Use well-founded descent for termination.
4. Match the induction principle to the way objects or computations are generated.
5. Preserve mathematical set semantics when choosing concrete data structures.

## Connects To
- **Ch. 4**: Rewrite termination and LPO are applications of well-founded order theory.
- **Ch. 3**: Least Herbrand models and proof-search closures use inductive/fixed-point ideas.
- **App. 2**: Structural recursion and algebraic datatypes implement these mathematical patterns directly.
