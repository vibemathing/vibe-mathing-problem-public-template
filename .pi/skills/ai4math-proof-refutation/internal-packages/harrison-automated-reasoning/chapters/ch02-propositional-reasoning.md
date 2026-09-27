# Chapter 2: Propositional Reasoning

**Source coverage**: Harrison Ch. 2, §§2.1–2.12, book pp. 25–117.

## Core Idea
Propositional logic turns finite Boolean reasoning into an executable search problem. The main engineering question is representation and search control: truth tables establish semantics; normal forms, DPLL, Stålmarck saturation, and BDDs offer different ways to avoid blind enumeration.

## Frameworks Introduced
### Valuation-based semantics
A valuation assigns each atom `true` or `false`; formula evaluation follows the connective truth functions recursively. Use this model to define:
- **valid/tautological**: true for every valuation;
- **satisfiable**: true for at least one valuation;
- **unsatisfiable**: true for none.

Operational reductions:
- validity of `p` ↔ unsatisfiability of `¬p`;
- finite entailment `Γ ⊨ q` ↔ validity of `conj(Γ) ⇒ q`.

### Simplification and NNF
- Simplify constants and double negations first.
- Push negations to atoms using De Morgan laws and eliminate implication/equivalence when their removal helps the downstream method.
- **Caution**: expanding nested equivalence can duplicate subformulas exponentially. Use sharing or a weaker normalizing target when full NNF is unnecessary.

### DNF/CNF as set-of-sets
Represent DNF as sets of conjunctions of literals and CNF as sets of clauses. Associativity, commutativity, and idempotence become ordinary set behavior.
- Remove contradictory DNF terms / tautological CNF clauses.
- Apply subsumption to delete redundant supersets.
- Use DNF to read satisfiability and CNF to read validity easily, while remembering conversion itself can be exponential.

### Definitional CNF
**When to use**: General SAT preprocessing where an equivalent CNF may explode.

**How**:
1. Simplify and push negations down.
2. For each nontrivial subformula, introduce a fresh atom.
3. Add a local definition linking the atom to the subformula.
4. Convert each small definition to CNF.
5. Assert the atom for the whole formula.

**Invariant**: Equisatisfiability with the original formula. Freshness of introduced atoms is mandatory.

### Davis–Putnam and DPLL
For a clause set:
1. **Unit propagation**: if `{p}` is a clause, delete clauses containing `p` and delete `¬p` from the rest.
2. **Pure literal rule**: if a literal appears with only one polarity, satisfy it and delete its clauses.
3. Original **DP** eliminates an atom by resolving every positive clause against every negative clause; it can generate many resolvents.
4. **DPLL** replaces elimination with a split on `p` versus `¬p`, then propagates.

Modern control improvements presented in the chapter:
- explicit trail with guessed versus deduced literals;
- non-chronological backjumping;
- conflict-clause learning;
- branching heuristics and possible restarts.

### Stålmarck's method
Convert the formula into small definitional triplets and derive equivalences by saturation.
- `0`-saturation exhausts simple local consequences.
- `n+1`-saturation splits on a literal, performs `n`-saturation in both branches, and keeps consequences common to both.
- **Decision rule**: A bounded implementation that fails to prove the formula only establishes “not solved at this bound.”

### Reduced ordered BDDs
A Boolean function can be represented by a reduced decision DAG under a fixed variable order.
- Eliminate nodes whose true/false children are identical.
- Share identical subgraphs through a unique table.
- Memoize binary operations in a computed table.
- Complement edges make negation constant-time and increase sharing.
- Under a fixed order the reduced representation is canonical, so Boolean equivalence reduces to identity/isomorphism of the canonical nodes.

## Key Concepts
- **Adequate connectives**: A set from which every Boolean truth function can be expressed; NAND or NOR alone suffice.
- **Duality**: Exchange `∧`/`∨` and `true`/`false` to derive dual laws.
- **Literal**: Atom or negated atom.
- **Clause**: Disjunction of literals.
- **Subsumption**: A smaller clause/term makes a larger one redundant in the relevant normal form.
- **Resolution**: From `p ∨ C` and `¬p ∨ D`, infer `C ∨ D`.
- **Unsat core**: Unsatisfiable subset of original clauses explaining inconsistency.
- **BDD variable order**: Global atom order used at every decision node; it controls representation size.
- **Compactness**: If every finite subset of a propositional theory is satisfiable, the whole theory is satisfiable.

## Mental Models
- **SAT as a universal backend**: Encode finite combinatorial constraints or circuits as Boolean variables plus constraints, then delegate search to a SAT method.
- **Propagation before guessing**: Exhaust forced consequences before adding a branch decision.
- **Learn from conflict**: A contradiction often depends on only a subset of decisions; record that dependency so search does not repeat it.
- **Formula versus circuit DAG**: Syntactic formulas duplicate repeated subexpressions; circuits, definitions, and BDDs expose sharing explicitly.
- **Canonical representation versus search**: BDDs spend work building a canonical object; DPLL explores assignments. Choose based on reuse, structure, and expected size.

## Anti-patterns
- **Full truth-table enumeration for large `n`**: Requires up to `2^n` valuations.
- **Equivalent CNF as default preprocessing**: Distribution can blow up exponentially; use definitional CNF when satisfiability is the goal.
- **Confusing equisatisfiability with equivalence**: Fresh-variable transformations cannot be substituted into arbitrary contexts as exact equivalents.
- **Branching without propagation**: Wastes search on consequences already forced by unit clauses.
- **Treating a bounded Stålmarck miss as a counterexample**: The procedure may simply require deeper saturation.
- **Assuming alphabetical BDD order is harmless**: Variable order can change a compact BDD into an exponential one.
- **Ignoring source-era legal constraints**: The 2009 book notes a commercial-use patent on Stålmarck’s method. Treat this as historical source information and verify present legal status before commercial implementation.

## Code Examples
Clause-oriented DPLL skeleton:

```text
solve(clauses, trail):
    clauses, trail := unit_propagate(clauses, trail)
    if empty_clause in clauses: backtrack_or_unsat()
    if all variables assigned: return SAT(trail)
    p := choose_branch_variable(clauses)
    try p; if conflict, try not p
```

Definitional CNF skeleton:

```text
encode(node):
    if literal(node): return node
    a := fresh_atom()
    children := map(encode, node.children)
    emit small CNF enforcing a <-> op(children)
    return a
```

BDD apply rule:

```text
apply(op, u, v):
    use terminal identities and memoized result if present
    branch on the earliest variable occurring at u or v
    recursively combine true and false cofactors
    reduce/hash-cons the resulting node
```

## Reference Tables
### Choosing a propositional method
| Method | Strength | Main cost | Best fit |
|---|---|---|---|
| Truth table | transparent, complete | `2^n` valuations | tiny formulas, teaching, counterexample extraction |
| DNF/CNF expansion | explicit normal form | exponential output | small normalization tasks |
| Definitional CNF + DPLL | scalable search baseline | branch heuristic / conflicts | general SAT and validity-via-refutation |
| DP resolution elimination | logically clean | clause blowup | conceptual baseline / selected formulas |
| Stålmarck | strong bounded saturation | higher saturation levels | structured hardware-like tautologies |
| BDD | canonical under fixed order | ordering-sensitive size | repeated Boolean ops/equivalence, symbolic hardware reasoning |

### Clause terminal states
| Clause-set state | Meaning |
|---|---|
| `[]` (no clauses) | `true`, satisfiable |
| contains `[]` (empty clause) | `false`, unsatisfiable |
| unit clause `{l}` | `l` must hold in every satisfying assignment |

## Worked Example
To verify two Boolean adder designs are equivalent:

1. Introduce atoms for input bits and outputs of each design.
2. Encode each gate relation propositionally; internal wires can be represented by fresh atoms rather than duplicated formulas.
3. Form the formula `designA ∧ designB ⇒ outputs_equal`.
4. For SAT-based checking, negate it and create definitional CNF.
5. Run DPLL. If the negation is unsatisfiable, the designs agree for every input; if satisfiable, the assignment is a concrete counterexample input.
6. For many related equivalence queries, build BDDs for output functions. If BDDs stay compact under a topology-aware order, equality can be checked directly.

The example illustrates a recurring pattern in the book: reduce a domain problem to logic while preserving the exact correctness property, then choose a solver whose representation matches the structure.

## Failure Recovery
- Clause count grows under DP resolution → switch to DPLL splitting.
- Recursive DPLL keeps large intermediate states → use an explicit trail.
- Same conflicts recur → learn conflict clauses and backjump.
- Formula contains abundant subexpression sharing → preserve it through definitions or BDD nodes.
- BDD expansion becomes steep → reorder variables or move back to SAT.
- Need an actual witness/core → modify the solver to retain assignments or resolution provenance rather than returning only a Boolean.

## Key Takeaways
1. Propositional semantics gives a finite, exact baseline for validity and satisfiability.
2. Normal form is useful only when its construction cost is controlled.
3. Definitional CNF is the standard escape from equivalent-CNF explosion when solving SAT.
4. DPLL's practical power comes from propagation, branching control, backtracking discipline, and learned information.
5. BDDs provide canonical Boolean functions only relative to a fixed variable order.
6. Solver failure under an artificial bound must remain `unknown`.
7. SAT encodings are valuable because many finite reasoning problems can reuse one mature Boolean engine.

## Connects To
- **Ch. 3**: Herbrand methods reduce first-order reasoning to propositional instances; resolution is lifted by unification.
- **Ch. 5**: SAT becomes the Boolean control layer for combinations of decision procedures/SMT.
- **Ch. 6**: SAT search can be paired with proof reconstruction for trusted results.
