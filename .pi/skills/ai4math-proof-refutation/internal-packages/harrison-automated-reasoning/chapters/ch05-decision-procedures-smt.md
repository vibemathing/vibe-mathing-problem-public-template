# Chapter 5: Decidable Problems and Theory Combination

**Source coverage**: Harrison Ch. 5, §§5.1–5.13, book pp. 308–463.

## Core Idea
General first-order validity is not decidable, yet many useful fragments are. The operational discipline is to recognize the fragment, exploit its structure with a dedicated decision procedure, and combine procedures only under the hypotheses that make their communication sound and complete.

## Frameworks Introduced
### Fragment recognition before general search
The chapter develops several routes to decidability:
- syntactic restrictions on quantifier patterns or signatures;
- a finite model property;
- quantifier elimination;
- algebraic canonicalization/ideal methods;
- cooperation between independent decision procedures.

**Routing rule**: Before launching unrestricted first-order proof search, classify quantifier prefix, function arities, predicate arities, arithmetic operators, and equality structure. A special procedure can change a semidecision problem into a terminating decision.

### AE/EA fragments
For suitable prenex formulas with limited quantifier alternation, Skolemization can produce a language with only finitely many relevant ground terms. Enumerate the finite Herbrand universe, instantiate, and reduce to propositional reasoning.

**Use when**: Prefix and function-symbol restrictions guarantee finiteness after Skolemization.

**Failure signal**: A Skolem function introduces recursively nestable terms; the finite grounding argument disappears.

### Miniscoping and the monadic fragment
**Miniscoping** pushes quantifiers inward when variables are irrelevant to neighboring subformulas. This can expose smaller scopes and eliminate dependencies before Skolemization.

The monadic fragment restricts predicates/functions enough to obtain small/finite model arguments.

**Rule**: Perform semantics-preserving scope reduction before deciding whether a formula qualifies for a fragment; the surface prenex shape may hide a simpler structure.

### Syllogisms as a decidable micro-fragment
Classical categorical syllogisms become simple first-order formulas over unary predicates. The chapter uses them to illustrate how changes in existential assumptions alter validity.

**Operational lesson**: Decide which semantics is intended before automating a historical/informal logic. Modern first-order readings can differ from traditional existential-import conventions.

### Finite model property + dovetailing
If every satisfiable formula in a class has a finite model, satisfiability is semidecidable by enumerating finite interpretations. Unsatisfiability may be semidecidable by a complete prover. Interleave both searches:
1. proof/refutation search;
2. finite-model search of increasing size.

If the class has the finite model property and the proof procedure is complete, one side must eventually terminate.

**Mental model**: Decision by racing a positive certificate against a negative certificate.

### General quantifier-elimination architecture
A theory has quantifier elimination when every formula is equivalent in the theory to a quantifier-free formula.

**Lifting pattern**:
1. Normalize propositional structure.
2. Recursively eliminate inner quantifiers.
3. Reduce the next quantified formula to the base shape expected by the theory-specific eliminator.
4. Eliminate one variable.
5. Simplify and continue outward.

Dense linear orders provide a clean example: eliminate a variable by reducing constraints to relations among its lower/upper bounds, with special handling for equalities.

### Presburger arithmetic / Cooper-style elimination
Theory: integers (or naturals via encoding) with addition, order, constants, and multiplication by constants; variable-variable multiplication is excluded.

**Elimination strategy**:
1. Normalize atomic formulas to linear integer forms.
2. Move the variable to one side and standardize coefficients.
3. Use an LCM to homogenize variable coefficients, adding divisibility information as needed.
4. Separate lower/upper/equality/divisibility constraints.
5. Exploit periodicity modulo a computed modulus.
6. Reduce an infinite existential search to finitely many boundary/residue cases.
7. Simplify resulting quantifier-free arithmetic.

**Special fragments**: Difference logic and UTVPI-like restrictions admit cheaper methods than full Presburger elimination.

### Complex numbers / algebraically closed fields
Polynomial formulas over algebraically closed fields support quantifier elimination.
- Normalize terms to multivariate polynomials.
- Handle equations by polynomial division/pseudo-division and degree reduction.
- Split on leading coefficients when a division step depends on nonzeroness.
- Use algebraic facts such as existence of roots for nonconstant polynomials.

**Engineering point**: “Divide by the leading coefficient” requires a proof that it is nonzero; case splitting preserves correctness without assuming it.

### Real numbers / real closed fields
Real quantifier elimination must track sign and ordering, not just polynomial zeros.

The book develops a sign-determination style procedure using:
- normalized polynomials in the eliminated variable;
- derivatives;
- remainder/pseudo-division sequences;
- sign matrices describing consistent sign patterns over intervals and roots;
- inference of existential conditions from realizable sign rows.

**Cost**: General real QE has severe, often doubly exponential behavior. Specialized linear arithmetic can use Fourier–Motzkin elimination or linear programming instead.

### Rings, ideals, and word problems
For commutative polynomial rings, universal equational consequence can be expressed as ideal membership.
- Put each assumption equation `pi = qi` into zero form `pi - qi = 0`.
- Put the target `p = q` into `p - q = 0`.
- The target follows from assumptions in the universal ring sense exactly when its polynomial lies in the ideal generated by assumption polynomials.

Hilbert's Nullstellensatz links polynomial zeros over algebraically closed fields to ideal/radical membership. The Rabinowitsch trick converts a nonvanishing condition into an auxiliary polynomial equation, allowing ideal methods to handle certain inequational goals.

### Gröbner bases
A Gröbner basis is a generating set whose leading monomials control reduction enough to decide ideal membership.

**Buchberger pattern**:
1. Choose a monomial order.
2. Reduce polynomials by the current basis.
3. For each relevant pair, form an S-polynomial that cancels leading terms.
4. Reduce the S-polynomial.
5. If the remainder is nonzero, add it to the basis and generate new pairs.
6. Stop when all required S-polynomials reduce to zero.
7. Decide ideal membership by reducing the target to normal form.

Dickson's lemma underpins termination for monomial-ideal growth. Pair criteria reduce redundant S-polynomial work.

### Geometric theorem proving
Translate geometry into coordinates and polynomial constraints.

**Workflow**:
1. Select coordinates, exploiting translation/scaling/rotation/affine invariance to normalize easy points when justified.
2. Encode geometric hypotheses as polynomial equations.
3. Encode the conclusion as a polynomial equation.
4. Use Gröbner/ideal reasoning or Wu's triangularization method.
5. Record degeneracy side conditions explicitly, such as denominators/leading terms required to be nonzero.

**Failure mode**: The algebraic implication may rely on a side condition hidden by division or coordinate normalization. A theorem about nondegenerate triangles can silently become false on a degenerate configuration if the side condition is omitted.

### Combining decision procedures
#### Craig interpolation as a bridge
An interpolant uses only vocabulary common to two formulas and sits logically between them. The constructive proof reuses theorem-proving machinery and motivates communication interfaces between theories.

#### Nelson–Oppen-style combination
**When to use**: Quantifier-free formulas whose atoms belong to disjoint component theories sharing only equality, under suitable model-theoretic hypotheses.

**Procedure**:
1. **Purify**: Replace alien subterms with fresh shared variables and defining equalities until each atom belongs to one theory.
2. Partition constraints by theory.
3. Identify variables shared by components.
4. Propagate equalities/disequalities implied over shared variables.
5. For nonconvex cases, explore arrangements (consistent equality partitions) over shared variables.
6. Ask each theory solver whether its local constraints plus shared arrangement are satisfiable.
7. Combine only if all local models can be amalgamated under the hypotheses.

**Key hypotheses**:
- disjoint signatures aside from equality/shared variables;
- stable infiniteness for the classic simple combination theorem;
- convexity determines whether implied equalities can be propagated singly or require disjunction/arrangement splitting.

#### Shostak-style combination
For theories with a solver/canonizer pair, normalize equalities to canonical forms and propagate solved substitutions. This can be efficient but requires stronger interfaces and careful correctness conditions.

#### SAT modulo theories
Two organization styles:
- **eager**: compile theory reasoning into Boolean constraints ahead of time;
- **lazy**: let SAT propose Boolean assignments, ask theory solvers for consistency, and learn a blocking/theory lemma on conflict.

The chapter's SAT/SMT discussion anticipates the modern pattern: Boolean search coordinates specialized theory solvers; theory explanations become learned constraints.

## Key Concepts
- **Decision procedure**: Always terminates with a correct yes/no answer for its target class.
- **Finite model property**: Every satisfiable formula in a class has a finite model.
- **Quantifier elimination**: Effective equivalent removal of quantified variables within a theory.
- **Presburger arithmetic**: First-order additive integer arithmetic, decidable despite quantifiers.
- **Pseudo-division**: Polynomial division variant avoiding division by symbolic leading coefficients.
- **Ideal**: Polynomial set closed under addition and multiplication by arbitrary ring polynomials.
- **S-polynomial**: Combination canceling leading terms of two polynomials.
- **Monomial order**: Well-order compatible with multiplication, used to define polynomial leading terms.
- **Purification**: Replacing cross-theory terms by fresh shared variables and definitions.
- **Convex theory**: Roughly, if a conjunction entails a disjunction of equalities, it entails one equality individually.
- **Stable infiniteness**: Every satisfiable quantifier-free formula has an infinite model.

## Mental Models
- **Recognize structure before proving**: Decidability often comes from syntax/theory restrictions invisible to a generic prover.
- **Eliminate one variable at a time**: Quantifier elimination is controlled projection of a definable set.
- **Canonical algebraic remainder as proof**: Gröbner reduction turns an ideal-membership consequence into a normal-form test.
- **Purify then communicate only the interface**: Combined solvers need not understand each other's internal syntax; they coordinate over shared equalities.
- **Boolean skeleton + theory semantics**: SMT separates combinatorial case choice from domain-specific consistency.

## Anti-patterns
- **Applying a decision procedure without checking its language**: Presburger arithmetic stops applying once unrestricted multiplication of variables appears.
- **Treating a theoretically decidable procedure as practically cheap**: QE can be complete and still computationally prohibitive.
- **Dividing by a symbolic coefficient without case splitting**: Loses solutions when the coefficient is zero.
- **Dropping geometry degeneracy conditions**: Turns a conditional algebraic proof into an overclaimed theorem.
- **Combining theory solvers by mere conjunction**: Shared variables/equalities must be coordinated.
- **Using classic Nelson–Oppen when stable infiniteness or signature assumptions fail**: Completeness may break; use a variant/dedicated combination.
- **Confusing an ideal with its radical**: Nullstellensatz consequences over algebraically closed fields need the right algebraic membership notion.

## Code Examples
Quantifier-elimination driver:

```text
qe(formula):
    recursively normalize Boolean structure
    for Q x. body:
        body' := qe(body)
        return eliminate_one(Q, x, body')
    return simplify_quantifier_free(formula)
```

Buchberger-style core:

```text
G := reduce_initial_generators()
pairs := all_pairs(G)
while pairs:
    f,g := select(pairs)
    h := normal_form(S_polynomial(f,g), G)
    if h != 0:
        add h to G
        add pairs (h, each old basis element)
return interreduce(G)
```

Lazy SAT+theory loop:

```text
while SAT has Boolean assignment A:
    for each theory Ti:
        check Ti-literals selected by A
    if every theory is consistent and shared equalities agree:
        return SAT
    explanation := theory_conflict_clause()
    add explanation to SAT
return UNSAT
```

## Reference Tables
### Fragment routing
| Formula shape | Method | Boundary |
|---|---|---|
| suitable ∀*∃* / ∃*∀* with finite grounding after Skolemization | finite Herbrand decision | recursive function terms can break finiteness |
| monadic restrictions | finite/small-model reasoning | higher-arity/function structure may exit fragment |
| additive integer arithmetic | Presburger/Cooper | no unrestricted variable multiplication |
| dense linear order | order QE | signature must stay in target order theory |
| algebraically closed-field polynomials | complex QE / algebraic methods | order/inequality changes theory |
| real closed-field polynomials | real QE | high complexity |
| universal polynomial equalities | ideal membership / Gröbner | check ring/field semantics and radical issue |
| coordinate geometry | Gröbner/Wu | track degeneracies and chosen coordinate assumptions |
| mixed quantifier-free disjoint theories | Nelson–Oppen/Shostak/SMT | combination hypotheses matter |

### Combination checklist
| Question | Why it matters |
|---|---|
| Are signatures disjoint apart from equality? | Prevents hidden cross-theory semantics. |
| Which variables are shared after purification? | Defines the communication interface. |
| Are component theories stably infinite? | Classic Nelson–Oppen model combination uses this. |
| Are they convex? | Determines equality propagation versus arrangement splitting. |
| Can a solver explain inconsistency? | Lazy SMT needs a useful conflict lemma. |
| Do canonizers/solvers satisfy Shostak interface laws? | Needed for canonical substitution-based cooperation. |

## Worked Example
Mixed constraint:

```text
f(x) = f(y)  ∧  x + 1 = y  ∧  x = y
```

Assume `f` belongs to an uninterpreted-function/equality theory and `+` to linear arithmetic.

1. Purify each theory so arithmetic sees only arithmetic expressions and EUF sees only function applications/equalities.
2. Shared variables include `x` and `y`.
3. Arithmetic has `x+1=y` and `x=y`, which is inconsistent over standard integers/reals.
4. The arithmetic solver can report the conflict without the EUF solver needing to understand `+`.
5. In a lazy SMT setting, the corresponding Boolean combination receives a learned theory-conflict clause blocking that selection.

For a less direct case, if one theory implies `x=y` while the other contains `x≠y`, equality communication exposes the conflict. If a nonconvex theory implies a disjunction such as `x=y ∨ x=z` without choosing either equality alone, arrangement splitting may be necessary.

## Failure Recovery
- Generic prover is wandering → reclassify the fragment using quantifier prefix/signature/theory.
- Finite-model search and proof search both run forever → verify the finite-model property really holds for the class.
- Presburger QE expands sharply → detect difference logic/UTVPI or simplify coefficients/divisibility before full elimination.
- Real QE explodes → isolate a linear subsystem, reduce variables, or use another specialized real-arithmetic method.
- Gröbner basis grows → change monomial ordering, use pair criteria/interreduction, or reconsider whether ideal membership is the right formulation.
- Geometry proof succeeds only after division → surface the required nonzero side condition in the theorem statement.
- Nelson–Oppen assumptions fail → use a non-stably-infinite variant, explicit arrangements, many-sorted method, or a dedicated combined solver.

## Key Takeaways
1. First-order undecidability coexists with rich, practically important decidable fragments.
2. Fragment recognition is itself an operational capability.
3. Quantifier elimination supplies both a decision procedure and a way to expose parameter constraints.
4. Presburger, complex, and real arithmetic need different elimination invariants.
5. Gröbner bases turn polynomial ideal membership into canonical reduction.
6. Algebraic geometry automation must preserve degeneracy assumptions.
7. Theory combination works by purification plus disciplined communication over a shared interface.
8. Decidability guarantees termination in principle; complexity still determines practical routing.

## Connects To
- **Ch. 2**: SAT provides the Boolean search layer for SMT-style cooperation.
- **Ch. 4**: Congruence closure supplies the equality/uninterpreted-function component.
- **Ch. 7**: Church's theorem explains why these fragment boundaries matter.
