# Consolidated core: Lean formalization and proof engineering

## Purpose

Translate frozen mathematical obligations into Lean 4, construct proof terms under a pinned environment, diagnose failures and return auditable candidates. Elaboration and kernel acceptance establish the Lean proposition only; correspondence to the source statement is reviewed separately.

## Statement translation record

Before coding, record:

- source statement and identity;
- domains, binders and quantifier order;
- definitions and intended equality/equivalence;
- explicit and implicit assumptions;
- existence versus construction intent;
- classical/choice/propext/quotient expectations;
- boundary and degenerate cases;
- proposed Lean theorem type;
- forward/back translation notes.

Review the theorem type before proving it. A proof of a mistranslated theorem is a valid proof of the wrong claim.

## Environment preflight

Capture repository revision, `lean-toolchain`, Lake/Mathlib revision, imports, namespace, options and build command. Check existing declarations before adding dependencies. Live search results and remote backends are hints; locally elaborated declarations are authoritative for the pinned project.

## Proof-state loop

1. inspect target outer constructor and local context;
2. introduce or construct according to the target shape;
3. normalize only enough to expose a known interface;
4. search by theorem type and available hypotheses;
5. apply the weakest sufficient lemma;
6. discharge side conditions explicitly;
7. compile immediately after a coherent increment;
8. inspect generated axioms and dependencies.

Read goals as typed APIs. Do not let a long tactic script obscure the mathematical dependency graph.

## Shape router

- `∀` / implication: introduce arbitrary variables/hypotheses;
- `∃`: provide a witness and proof;
- conjunction/structures: construct fields;
- disjunction: choose a branch with justification;
- equality: rewrite, extensionality, congruence or calculation chains;
- equivalence/iff: prove both directions;
- inductive object: use constructor or recursor aligned with definition;
- recursive function/property: induct where recursion unfolds;
- subtype/set membership: separate carrier data from property proofs;
- quotient: use the public quotient API and prove representative independence;
- typeclass goal: expose missing instance dependencies rather than brute-force search.

## Abstraction and API selection

Prefer stable interfaces over implementation fields. Search in this order:

1. exact theorem already available;
2. general theorem at the weakest adequate abstraction;
3. structural interface or universal property;
4. small local bridging lemma;
5. new definition only when existing semantics do not fit.

For algebra, topology and analysis, separate structural transformations from routine normalization (`simp`, ring/linear arithmetic, norm bounds). In filter-based reasoning, identify the filter and convergence predicate before unfolding epsilon definitions.

## Search discipline

Select search mode by information:

- declaration-name grep for known vocabulary;
- type-pattern search for known shape;
- semantic search for an informal description;
- state search for the current goal and context;
- source inspection for namespace, arguments and attributes.

Validate every suggestion locally. Cache/backend success does not imply compatibility with the pinned revision.

## Failure diagnosis order

1. parser/syntax and missing import;
2. name resolution/namespace;
3. elaboration and expected type;
4. coercion or universe mismatch;
5. missing instance;
6. definitional equality versus propositional equality;
7. rewrite orientation or syntactic mismatch;
8. theorem precondition;
9. termination/structural recursion;
10. genuine mathematical gap.

Do not add broad automation before identifying the layer.

## Metaprogramming boundary

Treat syntax, elaboration, `Expr`, metavariables, tactics and kernel checking as distinct stages. Metaprograms may mutate proof state and require rollback discipline. Pretty-printing is not expression identity. Any generated term must still elaborate and kernel-check in the target environment.

## Static analysis and dependency inspection

When using analyzers, preserve distinctions among declarations, tactics, lines, InfoTrees and dependencies. Match the analyzer's Lean revision. Analyzer output is diagnostic data, not a proof receipt unless the relevant checker actually replayed the term.

## Project-scale formalization

Build a theorem dependency graph from stable definitions upward. Protect admitted declarations from accidental weakening. Separate planning, candidate proving and independent review. Parallel work may proceed only on non-overlapping declarations or explicit interfaces; merge success is not theorem admission.

## Trust and escape audit

Reject candidates containing forbidden placeholders or unsafe escapes. Inspect `#print axioms` or equivalent dependency evidence for critical theorems. Distinguish accepted classical axioms from unexpected project axioms. `native_decide` or external computation must satisfy the project's trust policy; compilation alone does not expand the evidence ceiling.

## Replay receipt

A replay records theorem identity/type, source digest, imports, Lean/Lake/Mathlib revisions, exact command, timeout, diagnostics, exit code, axiom report and artifact digest. A separate reviewer checks statement faithfulness and whether the replay environment is independent enough for the claimed gate.

## Failure recovery

- minimize to the smallest failing theorem;
- inspect inferred types with explicit annotations;
- replace brittle automation with a typed intermediate lemma;
- align induction with recursive structure;
- expose a missing mathematical obligation rather than fabricating an instance;
- if environment is unavailable, return a bounded candidate and exact obstruction;
- if formal statement drift is found, freeze a corrected candidate under a new digest.

## Completion boundary

Lean success is `lean-kernel` evidence for the encoded type under recorded axioms. It is not source truth, novelty, root closure or admission. Preserve that separation in every report.
