# Glossary

**Abstract syntax tree (AST)** — Structural tree representation of an expression, separated from its concrete notation (Ch. 1, App. 3).

**Canonical model / Herbrand interpretation** — A model whose domain is built from ground terms and whose function symbols act syntactically; used in Herbrand-style completeness arguments (Ch. 3).

**Clause** — A disjunction of literals, usually represented as a set; a CNF is a set of clauses (Ch. 2–3).

**Compactness** — If every finite subset of a set of formulas is satisfiable, the whole set is satisfiable; used in propositional and first-order metatheory (Ch. 2–3).

**Congruence closure** — Closure of ground equality under reflexivity/symmetry/transitivity and function congruence; a decision method for ground equality with uninterpreted functions (Ch. 4).

**Confluence** — Any two reduction paths from one term can be joined; with termination it gives unique normal forms (Ch. 4).

**Definitional CNF** — Linear-size-style CNF conversion introducing fresh atoms for subformulas; preserves satisfiability rather than full equivalence (Ch. 2).

**DPLL** — SAT procedure combining unit propagation, optional pure-literal simplification, and case splitting; iterative versions support backjumping and learning (Ch. 2).

**Equisatisfiable** — Two formulas are satisfiable under exactly the same existence/nonexistence condition, although they may differ in truth under individual valuations (Ch. 2–3).

**Gröbner basis** — A polynomial basis with reduction properties strong enough to decide ideal membership (Ch. 5).

**Herbrand theorem** — Reduces first-order unsatisfiability/validity search to finite propositional combinations of ground substitution instances (Ch. 3).

**LCF architecture** — Trusted small kernel exposes an abstract theorem type; all accepted theorems must arise from primitive sound inference functions (Ch. 6).

**Literal** — An atom or its negation (Ch. 2).

**Logical validity** — Truth in every valuation/model of the intended semantics (Ch. 2–3).

**LPO (lexicographic path ordering)** — A well-founded term ordering used to orient rewrite rules and prove termination (Ch. 4).

**MGU (most general unifier)** — A unifier through which every other unifier factors by further substitution (Ch. 3).

**Model elimination** — Goal-directed first-order proof method using contrapositives, ancestor closure, and unification; the book's MESON implementation adds iterative-deepening control (Ch. 3).

**Nelson–Oppen combination** — Method for combining suitable decision procedures by purifying formulas and communicating equalities over shared variables (Ch. 5).

**NNF (negation normal form)** — Formula using only conjunction/disjunction over literals, with negation only on atoms (Ch. 2–3).

**Occurs-check** — Unification test forbidding a variable from being equated with a term containing that variable (Ch. 3).

**Paramodulation** — Equality inference that rewrites a matching subterm using an equality while simultaneously unifying; complete with suitable resolution machinery (Ch. 4).

**Prenex normal form** — All quantifiers moved to a prefix in front of a quantifier-free matrix, with variable-renaming side conditions observed (Ch. 3).

**Quantifier elimination** — Transformation eliminating quantified variables while preserving equivalence in a theory, thereby yielding a decision procedure when the quantifier-free case is decidable (Ch. 5).

**Resolution** — Clause inference combining complementary literals; with unification/lifting it becomes a central first-order refutation method (Ch. 2–3).

**Rewrite system** — Directed equations used as reductions; desirable properties include termination and confluence (Ch. 4).

**Satisfiable** — Has a valuation/model satisfying the formula or set of formulas (Ch. 2–3).

**Skolemization** — Elimination of existential quantifiers using fresh constants/functions depending on surrounding universal variables; preserves satisfiability in the required direction/equisatisfiability setting (Ch. 3).

**Stable infiniteness** — Property used in theory combination: every satisfiable quantifier-free formula has an infinite model (Ch. 5).

**Stålmarck saturation** — Propositional procedure deriving equivalences, using bounded-depth dilemmas to intersect consequences from both branches (Ch. 2).

**Subsumption** — Redundancy relation where a stronger/smaller clause or conjunction makes another unnecessary (Ch. 2–3).

**Tautology** — Propositional formula true under every valuation (Ch. 2).

**Unification** — Finding substitutions that make terms/literals syntactically identical (Ch. 3).


**Craig interpolation** — If `p ⇒ q` is valid, an interpolant can be chosen using only vocabulary common to `p` and `q`, with `p ⇒ r` and `r ⇒ q` valid (Ch. 5).

**Factoring** — First-order clause inference that unifies same-polarity literals within a clause; needed with resolution for completeness (Ch. 3).

**Finite model property** — Every satisfiable formula in a class has a finite model, enabling finite-model enumeration to participate in a decision procedure (Ch. 5).

**Horn clause** — Clause with at most one positive literal; definite Horn clauses support rule-like backward chaining and least-Herbrand-model semantics (Ch. 3).

**Hyperresolution** — Resolution refinement combining a nucleus with multiple satellite clauses to derive a consolidated resolvent (Ch. 3).

**Semidecidable / r.e.** — Positive instances can be recognized by a terminating computation, while negative instances may run forever (Ch. 7).

**Wu's method** — Coordinate-algebraic geometry prover based on triangular polynomial sets and pseudo-division, with explicit nondegeneracy conditions (Ch. 5).

**Well-founded relation** — Relation admitting no infinite descending chain; supports induction and termination proofs (App. 1, Ch. 4).
