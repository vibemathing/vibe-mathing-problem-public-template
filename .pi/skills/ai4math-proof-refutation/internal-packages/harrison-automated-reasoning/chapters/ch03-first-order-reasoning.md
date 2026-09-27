# Chapter 3: First-Order Reasoning

**Source coverage**: Harrison Ch. 3, §§3.1–3.16, book pp. 118–234.

## Core Idea
First-order logic adds object-denoting terms, predicates, and quantifiers. Automation therefore needs binding-safe syntax operations, semantic-preserving quantifier transformations, term unification, and a search calculus that is complete enough to find finite refutations when they exist.

## Frameworks Introduced
### Terms, predicates, quantifiers, and models
- **Terms** denote domain objects and are built from variables and function symbols.
- **Atomic formulas** apply predicates to terms.
- **Interpretation** supplies a nonempty domain plus meanings for function/predicate symbols.
- **Valuation** assigns domain elements to variables.
- **Free-variable rule**: A formula's truth under a fixed interpretation depends only on valuations of its free variables.
- **Sentence**: Formula with no free variables.

Quantifier order matters. `∀x ∃y R(x,y)` allows the witness to depend on `x`; `∃y ∀x R(x,y)` demands one common witness.

### Capture-avoiding substitution
**When to use**: Instantiating terms into formulas under quantifiers.

**Procedure**:
1. Do not replace occurrences bound by the current quantifier.
2. Inspect free variables of replacement terms.
3. If a replacement variable would become captured, alpha-rename the binder to a fresh variant.
4. Continue substitution under the renamed binder.

**Validation**: The free variables and semantic interpretation of the substituted formula should match the substitution lemmas, not merely its surface text.

### Prenex conversion
Move quantifiers to a prefix after simplifying and pushing negations inward.
- Rename bound variables apart before moving quantifiers across binary connectives.
- Use equivalences such as moving a quantifier past a connective only when the moved variable is not free in the other operand.
- Prenex form is a staging representation for Skolemization and metatheory, not always the best human-readable form.

### Skolemization
**Goal**: Remove existential quantifiers while preserving satisfiability behavior needed for refutation.

**Procedure**:
1. Work from an appropriately normalized formula.
2. For an existential variable under universal variables `u1...uk`, replace it by a fresh Skolem function `f(u1,...,uk)`.
3. If it depends on no universal variable, use a fresh Skolem constant.
4. Remove the existential quantifier; continue recursively.
5. Never reuse a symbol already present in the relevant language.

Direct Skolemization can sometimes exploit only the actually relevant free variables, reducing function arity relative to a naive prenex scheme.

### Herbrand search
After Skolemization and universal closure, ground terms from the Herbrand universe provide candidate instantiations. Herbrand's theorem supports a semidecision strategy:
1. Enumerate ground tuples by increasing term complexity.
2. Generate substitution instances of the quantifier-free matrix.
3. Test growing finite propositional combinations for unsatisfiability.
4. Stop when a finite unsatisfiable set is found.

This is a completeness foundation, yet naive enumeration repeats enormous search.

### Unification
Unification postpones choosing concrete ground terms.

**MGU procedure**:
1. Maintain equations between terms.
2. Delete identical equations.
3. Decompose `f(s1,...,sn)=f(t1,...,tn)` into pairwise equations; fail on different heads/arities.
4. Orient equations to place a variable on the left where possible.
5. For `x=t`, fail if `x` occurs properly in `t`.
6. Substitute `t` for `x` throughout the remaining problem and accumulated substitution.
7. The resulting substitution is most general when successful.

### Tableaux
Analytic tableau refutation recursively decomposes logical structure, closing branches when complementary literals unify.
- Conjunctive information stays on a branch.
- Disjunction creates branches.
- Quantifier instances are generated as needed.
- Iterative deepening can restore completeness to a depth-bounded implementation.

### Resolution and lifting
First transform a negated target to clauses.
- Propositional resolution is lifted to first-order clauses by unifying complementary literals.
- **Factoring** unifies same-polarity literals within a clause to recover completeness lost by treating clauses as sets of non-ground literals.
- The **lifting lemma** relates ground propositional resolvents to lifted first-order inference.

Operational saturation uses:
- renaming variables apart between clauses;
- subsumption and tautology deletion;
- replacement/demodulation for simplification;
- a **given-clause** loop with processed/unprocessed sets.

### Resolution refinements
The chapter surveys restrictions that reduce branching while retaining completeness under stated conditions:
- linear/input-style restrictions;
- positive/negative resolution;
- semantic resolution;
- set-of-support;
- hyperresolution.

Treat each as a search policy with a completeness theorem and preconditions, not as a free optimization.

### Horn clauses and Prolog
A definite Horn clause `A1 ∧ ... ∧ An ⇒ B` supports goal-directed backward chaining.
- Least Herbrand model gives a clean semantic interpretation.
- Prolog's left-to-right depth-first rule selection is operationally convenient but can loop or miss answers because search is unfair.
- Rule order and goal order therefore affect termination although declarative meaning is unchanged.

### Model elimination / MESON
Model elimination turns clauses into contrapositives and performs goal-directed chaining with ancestor closure.
- Ancestor literals allow reduction/closure against earlier goals.
- Unification carries substitutions through the whole branch.
- Harrison's MESON implementation uses iterative deepening and compact control to avoid Prolog's raw depth-first incompleteness.

## Key Concepts
- **Signature**: Function/predicate names with arities defining a first-order language.
- **Ground term/formula**: Contains no variables.
- **Free/bound variable**: Variable occurrence outside/inside the scope of its binder.
- **Universal closure**: Universally quantify all free variables.
- **Canonical/Herbrand model**: Domain of syntactic ground terms under their natural function interpretation.
- **Unifier / MGU**: Substitution making expressions identical / most general such substitution.
- **Factoring**: Clause inference merging unifiable literals.
- **Subsumption**: Clause redundancy check by substitution inclusion.
- **Horn clause**: Clause with at most one positive literal; definite Horn clauses have exactly one positive head.
- **Compactness / Löwenheim–Skolem**: Model-theoretic results derived constructively from first-order proof machinery.

## Mental Models
- **Quantifiers encode dependencies**: Skolem function arguments are a concrete record of which universal choices an existential witness may depend on.
- **Unification is delayed enumeration**: Instead of guessing a ground term, retain the most general symbolic condition that would make the inference work.
- **Refutation as the common interface**: Validity proof becomes unsatisfiability of the negation, allowing tableau, resolution, and model-elimination families to share preprocessing.
- **Calculus versus search strategy**: A complete inference system can still fail operationally under an unfair search order.

## Anti-patterns
- **Naive textual substitution**: Captures variables and changes meaning.
- **Reusing Skolem symbols**: Can impose accidental equalities/dependencies and destroy satisfiability preservation.
- **Dropping the occurs-check**: Accepts cyclic finite-term equations such as `x=f(x)`.
- **Treating Prolog's DFS as logically complete search**: Declarative Horn completeness does not guarantee a particular operational ordering terminates.
- **Resolving clauses without variable renaming apart**: Accidental name collisions create false constraints.
- **Assuming search failure is falsity**: General first-order validity is only semidecidable.

## Code Examples
Capture-safe binder step:

```text
subst(∀x. p, σ):
    if x occurs free in any σ(y) for relevant free y:
        choose fresh x'
        rename bound x to x' in p
    remove x from σ beneath the binder
    return ∀x'. subst(p, σ)
```

Unification skeleton:

```text
unify(equations):
    while equations remain:
        choose s = t
        if s == t: continue
        if both have same function head: enqueue argument pairs
        elif s is variable and s not in FV(t): substitute s := t everywhere
        elif t is variable: swap and continue
        else: fail
    return accumulated substitution
```

Given-clause saturation:

```text
processed := {}
unprocessed := initial_clauses
while unprocessed not empty:
    g := fair_select(unprocessed)
    g := simplify(g, processed)
    if g is empty_clause: return UNSAT
    infer resolvents/factors with processed
    delete tautologies and subsumed clauses
    processed.add(g); unprocessed.add(new_clauses)
```

## Reference Tables
### Method selection
| Method | Search character | Strength | Typical failure |
|---|---|---|---|
| Herbrand enumeration | ground-instance growth | simple completeness basis | combinatorial explosion |
| Tableau | branch decomposition | direct logical structure | repeated instances / branch blowup |
| Resolution | saturation of clauses | flexible refinements/redundancy | clause explosion |
| Horn/Prolog | goal-directed DFS | efficient on well-behaved programs | loops/order sensitivity |
| Model elimination/MESON | goal-directed + ancestor closure | compact general prover | depth bound/search explosion |

### Transformation invariant
| Step | Preserves |
|---|---|
| capture-safe substitution with semantic interpretation | intended substitution semantics |
| prenex equivalence rules with side conditions | logical equivalence |
| Skolemization | satisfiability relationship/equisatisfiable form under freshness conditions |
| clausal conversion after Skolemization | refutation target |
| unification | most-general syntactic compatibility |

## Worked Example
Goal: prove `∀x. P(x) ⇒ ∃y. P(y)` over nonempty domains.

1. Negate the sentence: `∀x.P(x) ∧ ¬∃y.P(y)`.
2. Push negation through the existential: `∀x.P(x) ∧ ∀y.¬P(y)`.
3. Standardize variables apart and treat universals as available for instantiation.
4. Clausify to `P(x)` and `¬P(y)`.
5. Unify `x` and `y` with the MGU `{x ↦ y}` (or a fresh common variable representation).
6. Resolve to the empty clause.

A tableau closes for the same reason: one branch eventually contains `P(t)` and `¬P(t)` under a unifying substitution. The proof search is finite here; on arbitrary nonvalid FOL formulas, the search may continue forever.

## Failure Recovery
- Preprocessing creates giant prenex/NNF forms → preserve sharing and avoid transformations the chosen prover does not require.
- Herbrand enumeration repeats equivalent work → switch to unification-driven inference.
- Resolution saturates too broadly → add sound redundancy deletion and a completeness-preserving refinement/set-of-support policy.
- Goal-directed search loops → iterative deepening/fair scheduling, or switch to saturation.
- A formula belongs to a decidable fragment → stop general proof search and route to Ch. 5.

## Key Takeaways
1. Binding correctness is a prerequisite for every later first-order algorithm.
2. Skolemization records existential dependencies with fresh function symbols.
3. Herbrand's theorem explains why finite refutations can witness first-order validity.
4. Unification compresses many ground choices into one most-general symbolic step.
5. Tableau, resolution, Horn search, and model elimination differ heavily in search organization despite sharing semantic foundations.
6. Search strategy, redundancy control, and fairness determine practical success.
7. General first-order failure under finite resources must remain `unknown`.

## Connects To
- **Ch. 4**: Equality requires congruence, rewriting, or paramodulation beyond plain syntactic unification.
- **Ch. 5**: Some first-order fragments become decidable through finite models or quantifier elimination.
- **Ch. 6**: The same calculi can be reconstructed as trusted inference objects.
