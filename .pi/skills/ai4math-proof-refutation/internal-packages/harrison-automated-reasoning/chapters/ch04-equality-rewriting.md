# Chapter 4: Equality, Rewriting, and Paramodulation

**Source coverage**: Harrison Ch. 4, §§4.1–4.9, book pp. 235–307.

## Core Idea
Equality is structurally stronger than an ordinary predicate because it must be a congruence respected by every function and predicate. Efficient reasoning therefore uses dedicated closure, rewriting, completion, or equality inference rather than repeatedly expanding generic equality axioms.

## Frameworks Introduced
### Equality axiomatization
The generic first-order route adds:
- reflexivity;
- symmetry/transitivity or equivalent equivalence axioms;
- function congruence;
- predicate congruence.

**When to use**: As a semantic baseline, completeness argument, or fallback.

**Cost**: Axioms create many irrelevant inferences. Dedicated methods generally search less.

### Categoricity and elementary equivalence
- A theory is categorical in a cardinality when all models of that size are isomorphic.
- Isomorphic models satisfy the same first-order sentences.
- Elementary equivalence is weaker: models agree on all sentences of the language without necessarily being isomorphic.

Operational lesson: Do not infer a structure is uniquely determined merely because a set of first-order sentences captures many of its properties. Löwenheim–Skolem/compactness can force non-categoricity in important infinite settings.

### Equational logic
For pure equations, Birkhoff-style equational reasoning uses reflexivity, symmetry, transitivity, congruence, and substitution. This gives a focused complete calculus for universal equational consequence.

### Congruence closure
**When to use**: Ground equalities/disequalities involving uninterpreted functions.

**Procedure**:
1. Create equivalence classes for ground subterms.
2. Merge classes for each asserted equality.
3. Whenever two applications have the same function symbol and pairwise-equivalent arguments, merge their result classes.
4. Repeat to closure.
5. A disequality `s ≠ t` is inconsistent if `s` and `t` end in the same class.

**Implementation model**: union-find for equality classes plus indexing/signatures for congruent function applications.

**Ackermann reduction**: Replace function applications by fresh variables and add pairwise congruence constraints, reducing EUF-style reasoning to equality constraints at the price of potentially many implications.

### Term rewriting
Orient equation `l = r` into rewrite `l → r` and repeatedly replace matching instances of `l` by `r`.

Key properties:
- **termination / strong normalization**: no infinite reduction chain;
- **confluence**: diverging reductions can rejoin;
- **weak confluence**: one-step divergences can rejoin;
- **normal form**: term with no rewrite step available.

If a rewrite system is terminating and confluent, equality in the induced theory can be decided by comparing unique normal forms. Newman's lemma lets termination + weak confluence yield confluence.

### Termination orderings
To guarantee termination, orient every rule so the left side is strictly greater than the right side in a well-founded ordering stable under substitution and contexts.

**Lexicographic path ordering (LPO)** is a key example:
- compare root symbols by a precedence;
- include a subterm property so a term exceeds its proper subterms;
- recurse lexicographically/multiset-like according to the defined path ordering.

Use the order as a proof obligation, not merely a heuristic score.

### Knuth–Bendix completion
**Goal**: Transform equations into a convergent rewrite system where possible.

**Loop**:
1. Normalize both sides of each pending equation under current rules.
2. Delete trivial equations whose sides normalize identically.
3. Orient a nontrivial equation using the reduction ordering; if neither direction is allowed, ordinary completion fails.
4. Add the rule and simplify/interreduce existing rules/equations.
5. Compute critical overlaps involving the new rule.
6. For each nonjoinable critical pair, add the resulting equation to pending work.
7. Continue until no unresolved critical pairs remain.

**Completeness caveat**: The completion procedure itself may fail or run forever even when the equational theory has useful consequences.

### Equality elimination / Brand transformation
Equality can be compiled into predicate-like constraints and additional clauses. This can let a plain resolution prover handle equality with better structure than naive axioms in some settings, but it is still an encoding choice with search costs.

### Paramodulation and superposition idea
Paramodulation performs equality rewriting and unification inside an inference rule.

From an equality `l = r` and a clause containing a subterm unifiable with `l`, infer a clause where that occurrence is replaced by `r` under the unifier. Together with resolution (and suitable reflexivity/equality machinery), this yields a complete first-order equality calculus. Ordering restrictions motivate superposition-style refinements.

## Key Concepts
- **Congruence**: Equivalence relation preserved by function/predicate contexts.
- **Demodulation**: Using oriented equalities as simplification rewrite rules inside theorem proving.
- **Critical pair**: Pair of results obtained from overlapping rewrite rules; its joinability tests local confluence.
- **Reduction ordering**: Well-founded, monotone, substitution-stable term order for orienting equations.
- **Completion**: Procedure that adds consequences to make an oriented rewrite system confluent.
- **Paramodulation**: Equality inference combining rewriting with unification.
- **Superposition**: Ordered/refined form of equality inference built around maximal terms/literals.

## Mental Models
- **Equality as closure, not lookup**: `a=b` implies equality of surrounding function contexts; this is why union-find alone needs congruence propagation.
- **Canonicalization turns proof into comparison**: A convergent rewrite system converts equational reasoning into computing normal forms.
- **Completion is proof search over missing confluence**: Critical pairs identify exactly where two reduction paths disagree.
- **Orientation is a semantic engineering choice**: A rewrite rule is safe as an equation, yet its use as an unconditional reduction also needs termination control.

## Anti-patterns
- **Expanding all equality axioms in every problem**: Search becomes saturated with generic congruence facts.
- **Using union-find without function congruence**: Misses equalities such as `f(a)=f(b)` after learning `a=b`.
- **Assuming local simplification terminates**: Symmetric rules or poorly oriented equations can loop.
- **Claiming unique normal forms from termination alone**: Confluence is also needed.
- **Forcing an unorientable equation into a rewrite direction**: Breaks the termination proof.
- **Treating completion failure as inconsistency**: It is a method failure, not a semantic result.

## Code Examples
Congruence-closure skeleton:

```text
initialize class(term) for every ground subterm
for each asserted s = t: merge(class(s), class(t))
repeat:
    if f(s1,...,sn) and f(t1,...,tn) have equivalent arguments:
        merge their result classes
until no merge occurs
reject if any required s != t has equal classes
```

Completion skeleton:

```text
while pending_equations:
    s=t := normalize_both(pop())
    if s == t: continue
    if s > t: add_rule(s -> t)
    elif t > s: add_rule(t -> s)
    else: return ORIENTATION_FAILURE
    interreduce()
    enqueue(nonjoinable_critical_pairs(new_rule, rules))
return convergent_rules
```

Paramodulation sketch:

```text
choose equality l = r and target occurrence u in another clause
σ := mgu(l, u)
replace u by r, apply σ to the whole inferred clause
simplify / standardize apart / retain according to prover restrictions
```

## Reference Tables
### Equality method routing
| Input shape | Method | Main precondition |
|---|---|---|
| Ground EUF equalities/disequalities | Congruence closure | quantifier-free ground terms |
| Universal equations used for simplification | Rewriting | oriented rules terminate |
| Need canonical equational theory | Knuth–Bendix completion | orientability + completion terminates |
| General clauses with equality | Paramodulation/superposition | fair equality-aware saturation |
| Existing plain resolution infrastructure | Equality axioms / Brand-style transformation | accept larger encoded search |

### Rewrite claims
| Known property | Safe conclusion |
|---|---|
| terminating | every reduction reaches some normal form |
| confluent | any two reductions can be joined |
| terminating + confluent | unique normal form |
| terminating + weakly confluent | confluent (Newman's lemma) |

## Worked Example
Given ground facts `a=b`, `f(a)=c`, and `f(b)≠c`:

1. Initialize classes for `a`, `b`, `f(a)`, `f(b)`, and `c`.
2. Merge `a` with `b`.
3. Congruence forces `f(a)` and `f(b)` into the same class because their function symbols match and arguments are equal.
4. `f(a)=c` merges that shared class with `c`.
5. The asserted disequality `f(b)≠c` now compares two members of the same class, producing a contradiction.

A generic equality-axiom proof exists, but congruence closure exposes the exact computational invariant directly.

## Failure Recovery
- Ground problem starts acquiring quantifiers → move to a first-order equality calculus.
- Rewrite rules normalize slowly → interreduce and orient with a better ordering; index rewrite heads.
- Critical pairs do not join → add their equation if orientable.
- Completion reaches an unorientable equation or grows without bound → stop claiming canonicalization and use paramodulation/superposition for proof search.
- Associative/commutative operators dominate → ordinary syntactic rewriting/completion is a poor fit; use AC-aware matching/unification or a specialized algebraic representation.

## Key Takeaways
1. Equality's congruence property justifies specialized algorithms.
2. Congruence closure is the natural ground-EUF engine.
3. Rewriting is reliable only with an explicit termination argument.
4. Unique normal forms require confluence as well as termination.
5. Knuth–Bendix completion repairs nonconfluence through critical-pair equations when it succeeds.
6. Paramodulation internalizes equality rewriting into first-order inference.
7. Method failure in completion or rewriting carries no semantic verdict by itself.

## Connects To
- **Ch. 3**: Paramodulation inherits unification, clauses, and saturation control from resolution.
- **Ch. 5**: Congruence closure becomes a component decision procedure in theory combination; Gröbner bases give an algebraic analogue of canonical reduction.
- **App. 1**: Well-founded orders justify rewrite termination.
