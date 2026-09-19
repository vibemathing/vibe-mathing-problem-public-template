# Appendix Skill Layer 2: Functional Symbolic Programming

**Source coverage**: Harrison Appendix 2, book pp. 603–622.

## Core Idea
Functional programming fits symbolic reasoning because formulas are recursive immutable trees and most algorithms are naturally recursive transformations over them. Keep theorem-proving state explicit, favor pure functions, and use small generic data-structure combinators.

## Frameworks Introduced
### Expression-oriented functional style
Core habits:
- definitions bind names to values/functions;
- functions are first-class values;
- application and local `let` bindings replace command sequences;
- recursion replaces loops;
- currying lets multi-argument functions be partially applied;
- higher-order functions factor traversal/control patterns.

### Algebraic datatypes + pattern matching
Represent syntax by constructors such as `Var`, `Fn`, `Atom`, `Not`, `And`, etc.

**Operational pattern**:
1. Define the recursive datatype so invalid structural cases are hard to express.
2. Define transformations by pattern matching on constructors.
3. Recurse only on immediate substructures.
4. Prove properties by structural induction matching the code.

This alignment between datatype, recursion, and induction is a major reason the book uses ML-family languages.

### Type inference and parametric polymorphism
Generic list/set/formula traversals can remain independent of the exact atom type. Let the type system catch structural mistakes while avoiding boilerplate type annotations.

**Boundary**: Overloading/ad-hoc polymorphism is different from parametric polymorphism; do not assume one operator has the same algebraic meaning at every type merely because syntax is shared.

### Tail recursion and accumulators
For long linear traversals, reformulate recursive calls in tail position with an accumulator when stack growth matters.

Tree algorithms often remain naturally non-tail-recursive; optimize only where actual depth/scale justifies it.

### Exceptions as controlled failure
Operations such as destructors, parser alternatives, or partial map lookup may fail legitimately.
- Raise an exception/failure marker at the local impossible/missing case.
- Catch it only at a layer that knows an alternate path.
- Do not use exception swallowing to hide semantic errors.

### Lists as the default symbolic container
The supporting library uses lists for:
- stacks/trails;
- sequences of clauses/literals;
- function arguments;
- finite sets when normalized for duplicate/order behavior.

Common reusable operations include map, filter, fold/iteration, pairwise mapping, Cartesian pair generation, insertion, sorting, union/intersection, and subset tests.

### Finite partial functions
Represent maps used for:
- substitutions;
- valuations;
- BDD unique/computed tables;
- parser contexts;
- solver metadata.

Design lookup with explicit “undefined” behavior and separate update/removal operations. Persistent functional maps make branching search easier to reason about because previous states remain available.

### Union-find / partition structures
Equivalence-class maintenance supports:
- congruence closure;
- Stålmarck equivalences;
- theory arrangements.

Even when a simple functional implementation is slower than an imperative one, the abstraction clarifies which operations the reasoning method requires: find canonical representative, merge classes, enumerate known equalities.

## Key Concepts
- **Recursive datatype**: Type defined in terms of itself through constructors.
- **Pattern matching**: Case analysis that simultaneously tests and destructures a constructor.
- **Currying**: Treat multi-argument functions as chains of single-argument functions.
- **Higher-order function**: Function accepting/returning functions.
- **Polymorphism**: Reusing one function uniformly over multiple types.
- **Finite partial function**: Mapping defined only on a finite subset of keys.
- **Persistent state**: Updating by creating a new value rather than mutating the old one.
- **Tail recursion**: Recursive call is the final operation, enabling constant-stack execution in suitable runtimes.

## Mental Models
- **Program structure as proof skeleton**: Recursive clauses mirror the inductive proof cases used to establish correctness.
- **State threading instead of hidden mutation**: Pass updated tables/contexts explicitly so dependencies are visible.
- **Pure core, effectful shell**: Keep logical transformations pure; confine printing/diagnostics/I/O to boundaries.

## Anti-patterns
- **Embedding concrete syntax strings throughout the prover**: Parse once into typed ASTs.
- **Mutable global solver tables without a clear invariant**: Harder to backtrack and reason about.
- **Using list-as-set while tolerating duplicates**: Changes complexity and may break equality/subsumption assumptions.
- **Catching every exception at the top**: Erases the distinction between expected branch failure and implementation bugs.
- **Premature low-level optimization**: The book prioritizes executable clarity; optimize hot paths after preserving semantics.

## Code Examples
Structural recursion pattern:

```text
map_formula(f, fm):
    Atom(a)       -> f(a)
    Not(p)        -> Not(map_formula(f,p))
    And(p,q)      -> And(map_formula(f,p), map_formula(f,q))
    Forall(x,p)   -> Forall(x, map_formula(f,p))
    ...
```

Persistent map branch:

```text
state1 := update(state, key, valueA)
solve(branchA, state1)
state2 := update(state, key, valueB)   # original state still available
solve(branchB, state2)
```

## Reference Tables
| Programming device | Reasoning use |
|---|---|
| recursive datatype | terms, formulas, proof objects, Turing-machine states |
| structural recursion | evaluation, substitution, normalization, printing |
| higher-order iterator | atom collection, generalized traversals |
| finite partial map | substitutions, valuations, memo tables |
| normalized list-set | clauses, literals, finite domains |
| partition/union-find | congruence/equivalence classes |
| continuations | search/control without rebuilding global state |
| exceptions | parser/destructor branch failure |

## Worked Example
A substitution engine stores `σ` as a finite map from variable names to terms. Applying it to a term is a structural recursion: variables look up in `σ`, while function applications map substitution over their argument list. Formula substitution reuses the term function but adds binder logic that updates/renames the map. The persistent map representation makes recursive descent through quantifiers and proof branches local and reversible.

## Key Takeaways
1. Recursive symbolic datatypes should drive both program structure and correctness proofs.
2. Pure functional state makes branching proof search easier to reason about.
3. Generic map/fold/set/map abstractions remove repeated low-level code.
4. Treat partiality and expected failure explicitly.
5. Optimize data structures only after the logical invariants are clear.

## Connects To
- **Ch. 1**: AST and recursive simplification are the introductory instance.
- **Ch. 2–5**: Every solver reuses finite sets/maps, structural recursion, and explicit state.
- **App. 3**: Parser combinators and printers are built from the same functional composition style.
