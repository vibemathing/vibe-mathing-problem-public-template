# Operational Patterns

## Property-preserving normalization
**When to use**: Before proof search or decision procedures.

**How**: State the target invariant first: logical equivalence, equisatisfiability, or consequence. Apply only transformations justified for that invariant. Keep a short transformation ledger for binding-sensitive steps.

**Trade-offs**: Stronger invariants can cause larger formulas. Definitional abbreviations and Skolemization reduce size/search complexity by preserving the weaker property actually needed.

## SAT by definitional CNF + DPLL
**When to use**: General propositional satisfiability or validity via negation.

**How**: Simplify → push negations → introduce fresh atoms for nontrivial subformulas → emit local CNF definitions → unit-propagate → branch → backtrack/backjump on conflict → retain useful conflict consequences if implementing learning.

**Trade-offs**: Branching heuristic and clause representation dominate practical performance. A satisfying assignment should be reconstructed when the caller needs a witness.

## Canonical Boolean reasoning with BDDs
**When to use**: Repeated equivalence checks or symbolic Boolean manipulation with exploitable structure.

**How**: Fix a variable ordering; construct reduced nodes bottom-up; eliminate nodes with equal children; hash-cons unique nodes; memoize binary operations; use complement edges for cheap negation.

**Trade-offs**: Canonicality is powerful, yet representation size can be exponential and is highly ordering-sensitive.

## Capture-safe substitution
**When to use**: Any substitution beneath quantifiers.

**How**: Compute free variables in replacement terms. Before crossing a binder, alpha-rename the bound variable if it could capture a replacement variable. Do not substitute for occurrences bound by that quantifier.

**Trade-offs**: Fresh-name generation is syntactic overhead that prevents semantic corruption.

## First-order refutation pipeline
**When to use**: General classical first-order validity.

**How**: Universal-close free variables when that matches the validity problem → negate the target → simplify/NNF → standardize variables apart → Skolemize with fresh symbols → remove universal prefix as implicit → choose tableau/model elimination or clausify for resolution.

**Trade-offs**: This is a semidecision pipeline in general. Search may diverge on non-theorems.

## Unify with an occurs-check
**When to use**: Matching complementary literals, tableau branches, resolution, or paramodulation.

**How**: Repeatedly decompose same-headed functions; orient equations toward variables; eliminate a variable only if it does not occur in its replacement; propagate each substitution through remaining equations.

**Trade-offs**: Omitting the occurs-check can be faster in special implementations but changes the term model and can make first-order reasoning unsound.

## Given-clause saturation
**When to use**: Resolution-style theorem proving with many generated clauses.

**How**: Maintain processed and unprocessed sets. Select a given clause, simplify it, generate allowed inferences with processed clauses, delete tautologies/subsumed clauses, and move the clause to processed. Use a fair selection policy.

**Trade-offs**: Aggressive heuristics speed many problems; unfair selection can destroy completeness.

## Rewriting + completion
**When to use**: Equational simplification or canonical representatives.

**How**: Choose a well-founded reduction order → orient equations → normalize both sides of equations → compute critical overlaps → add nonjoinable critical-pair equations → interreduce → repeat.

**Trade-offs**: Completion can fail to orient an equation or diverge. Associative/commutative theories need specialized treatment.

## Ground EUF by congruence closure
**When to use**: Quantifier-free ground equalities/disequalities with uninterpreted functions.

**How**: Merge asserted equalities; propagate congruence whenever function applications have equal arguments; detect conflict when a required disequality lands in one equivalence class.

**Trade-offs**: Excellent for ground equality; quantified equations and richer theories need other methods.

## Quantifier-elimination lifting
**When to use**: A theory has an elimination procedure for one quantified variable over quantifier-free formulas.

**How**: Normalize logical structure; recursively eliminate inner quantifiers; apply the base eliminator to the next quantifier; simplify after each stage.

**Trade-offs**: Correctness may coexist with severe worst-case blowup. Detect more specialized fragments early.

## Algebraic theorem proving via ideal membership
**When to use**: Universal polynomial equations over suitable fields/rings, or coordinate-translated geometry.

**How**: Move equations to polynomial-zero form; generate the ideal of assumptions; compute a Gröbner basis; reduce the target polynomial. For inequational/nonzero conditions, encode them with an auxiliary variable when justified.

**Trade-offs**: Translation can introduce degeneracy side conditions; a formal polynomial consequence may rely on hypotheses absent from the informal diagram.

## Theory combination by purification
**When to use**: Quantifier-free constraints mix otherwise decidable theories.

**How**: Replace alien subterms by shared variables plus defining equalities; partition constraints by signature; communicate equalities/disequalities on shared variables; explore arrangements when convex propagation is insufficient.

**Trade-offs**: Check disjoint-signature and stable-infiniteness assumptions for Nelson–Oppen-style completeness; use a dedicated procedure when they fail.

## Small-kernel proof production
**When to use**: Search results must be trusted independently of the search code.

**How**: Keep theorem construction behind a tiny primitive inference API. Let automation search with efficient mutable or external structures if desired, then replay a proof object/trace through the kernel.

**Trade-offs**: Direct proof-producing search can be slower; certificate replay separates fast discovery from trusted checking.

## Proof/model dovetail for finite-model classes
**When to use**: A fragment has the finite model property and a complete refutation procedure.

**How**: Alternate bounded proof search with enumeration of finite interpretations of increasing size. Stop when the prover refutes the target or a finite model satisfies it.

**Trade-offs**: Decidability depends on the finite-model theorem for the exact fragment. Without it, both searches may run forever.

## Bounded saturation without false negatives
**When to use**: Stålmarck-style or any depth/effort-bounded saturation method.

**How**: Record the saturation depth/limit as part of the result. Contradiction at the bound certifies the proof; exhaustion without contradiction returns `unknown at bound`, then increase the bound or switch methods.

**Trade-offs**: Bounded procedures can be very effective on structured inputs while remaining intentionally incomplete at a fixed bound.
