# Glossary

**`Acc`** — accessibility predicate used to justify well-founded recursion. (Ch 8)

**Attribute** — metadata attached to declarations, often controlling mechanisms such as simplification or instance search; can be scoped locally. (Ch 6)

**Classical choice** — principle `Classical.choice : Nonempty α → α`; useful for selecting data from mere nonemptiness, with computational consequences. (Ch 12)

**Coercion** — automatic conversion inserted by elaboration; type-class forms include `Coe`, `CoeDep`, `CoeSort`, and `CoeFun`. (Ch 6, 10)

**Constructor** — primitive way to build a value of an inductive type; constructor shape determines case and induction branches. (Ch 7)

**`conv`** — tactic mode for navigating to a selected subexpression and rewriting it precisely, including under binders. (Ch 11)

**Curry–Howard correspondence** — interpretation of propositions as types and proofs as terms. (Ch 3)

**Definitional equality** — equality recognized by computation/reduction, often closed by `rfl` without a separate equality theorem. (Ch 2, 4)

**Dependent function type** — function type `(x : α) → β x` whose result type can depend on the input. (Ch 2)

**`Decidable p`** — data describing whether proposition `p` is true or false; supports computation such as `if` over propositions. (Ch 10, 12)

**Elaboration** — process that resolves syntax, implicit parameters, overloads, coercions, expected types, and metavariables into a fully typed term. (Ch 2, 6, 10)

**Equation compiler** — mechanism compiling pattern-matching and recursive equations to primitive eliminators plus generated equation theorems. (Ch 8)

**Existential proof** — proof of `∃ x, p x` containing a witness and proof that the witness satisfies the predicate. (Ch 4)

**Function extensionality** — principle deriving `f = g` from pointwise equality `∀ x, f x = g x`; supported by Lean's quotient construction. (Ch 12)

**Functional induction** — induction principle aligned with a recursive function's equations and recursive calls, exposed through `fun_induction`. (Ch 8)

**Implicit argument** — parameter omitted from surface syntax and inferred by elaboration; written with braces in declarations. (Ch 2, 6)

**Inaccessible pattern** — dependent pattern marker for an index-forced term that should not be matched freely. (Ch 8)

**Inductive family** — inductive type indexed by values, so constructors constrain result indices. (Ch 7, 8)

**Instance** — declaration used by type-class inference to synthesize a class goal. (Ch 10)

**Metavariable** — placeholder introduced during elaboration whose value must be inferred from constraints. (Ch 2, 10)

**Motive** — type family describing what an eliminator/recursor produces for each scrutinee; especially important for dependent elimination. (Ch 7, 8)

**`Nonempty α`** — proposition asserting that type `α` has an inhabitant while hiding the inhabitant from data-level elimination. (Ch 12)

**`outParam`** — class parameter annotation allowing instance selection to proceed while treating that parameter as an output. (Ch 10)

**Proof irrelevance** — all proofs of the same proposition are treated as equal, supporting erasure of proof content. (Ch 3, 12)

**Propositional extensionality (`propext`)** — principle converting `p ↔ q` into equality `p = q`. (Ch 12)

**Quotient** — type whose elements represent equivalence classes; functions out of it require proof that the representative-level function respects the relation. (Ch 12)

**Recursor** — generated elimination principle for an inductive type, underlying recursion, cases, and induction. (Ch 7)

**`Setoid`** — a type equipped with an equivalence relation, used by `Quotient`. (Ch 12)

**Simplifier (`simp`)** — tactic repeatedly applying simplification lemmas and reductions toward canonical forms. (Ch 5)

**Structural recursion** — recursion accepted because recursive calls are made on structurally smaller constructor subterms. (Ch 8)

**Subtype** — data `{x : α // p x}` containing a value and a proof of its property. (Ch 7)

**Universe** — level in Lean's hierarchy of types (`Type u`) used to avoid type-in-type inconsistency while supporting polymorphism. (Ch 2)

**Well-founded recursion** — recursion justified by a relation with no infinite descending chain rather than direct structural subterms. (Ch 8)
