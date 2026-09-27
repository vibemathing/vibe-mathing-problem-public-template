---
name: theorem-proving-in-lean-4
description: "Operational knowledge from Theorem Proving in Lean 4 for constructing, debugging, and validating Lean 4 proofs and definitions: dependent types, propositions, equality, tactics, inductive types, recursion, structures, type classes, coercions, conversion mode, quotients, classical logic, and computation. Use for Lean theorem-proving questions, proof repair, elaboration failures, induction/termination choices, or method selection grounded in this book."
---

<!-- argument-hint: [Lean goal, error, topic, tactic, or chapter number] -->

# Theorem Proving in Lean 4
**Authors**: Jeremy Avigad, Leonardo de Moura, Soonho Kong, Sebastian Ullrich | **Lean version assumed by source**: 4.33.0 | **Chapters**: 12 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task is about Lean 4 proof construction, proof debugging, foundational Lean mechanisms, recursive definitions, type-class/coercion behavior, or the logical/computational consequences covered by this book. For APIs or tactics outside the book, inspect the active Lean environment rather than inventing a declaration.

### Route the task first

1. **Elaboration, unknown identifier, type mismatch, failed implicit inference** → inspect the actual declaration and environment before changing the proof. Load [ch02](chapters/ch02-dependent-type-theory.md) and [ch06](chapters/ch06-interacting-with-lean.md); add [ch10](chapters/ch10-type-classes.md) for instance/coercion errors.
2. **Goal shape is logical** → follow introduction/elimination structure. `→`/`∀`: introduce; `∧`/`↔`: build components; `∨`: choose or split cases; `¬`: derive `False`; `∃`: provide or unpack a witness. Load [ch03](chapters/ch03-propositions-and-proofs.md) and [ch04](chapters/ch04-quantifiers-and-equality.md).
3. **Equality/rewrite problem** → try `rfl` for definitional equality, `rw` for a targeted replacement, `simp` for normalization, `calc`/congruence for an explicit chain, then `conv` when an exact occurrence or binder must be targeted. Load [ch04](chapters/ch04-quantifiers-and-equality.md), [ch05](chapters/ch05-tactics.md), and [ch11](chapters/ch11-the-conversion-tactic-mode.md).
4. **Inductive data or proposition** → inspect constructors and the generated recursor; use `cases` for alternatives and `induction` when recursive structure provides the needed hypotheses. Load [ch07](chapters/ch07-inductive-types.md).
5. **Recursive definition or theorem about one** → prefer structural recursion; if termination is not structurally visible, use `termination_by` plus `decreasing_by`. For a proof that follows the function's branches and recursive calls, try `fun_induction`/`fun_cases`. Load [ch08](chapters/ch08-induction-and-recursion.md).
6. **Indexed/dependent family** → preserve index information; use dependent pattern matching, an appropriate recursor, inaccessible patterns, or `revert`/`generalize` before case analysis. Load ch07–ch08.
7. **Structure/API packaging** → use fields, projections, record updates, and `extends`. Load [ch09](chapters/ch09-structures-and-records.md).
8. **Type-class or coercion synthesis** → make input types concrete, check local/scoped instances, inspect priorities/search traces, and distinguish `Coe`, `CoeDep`, `CoeSort`, and `CoeFun`. Load ch10.
9. **Extensionality, quotient, choice, classical logic, or `noncomputable`** → load [ch12](chapters/ch12-axioms-and-computation.md) and audit both logical assumptions and computational consequences.

### Proof-construction defaults

- Prefer a small proof term or `exact` when the intended term is already clear; the expected type gives the elaborator useful information.
- Use tactics when decomposition, branching, controlled rewriting, or automation makes the proof easier to read.
- Mix term and tactic styles freely when that keeps each local step explicit.
- Prefer the weakest adequate mechanism. Escalate only after identifying why the simpler method fails.
- Never repair a final proof with an unsound placeholder. Treat `sorry`/`sorryAx` as an unfinished proof obligation.

### Failure-recovery ladder

1. Read the exact goal/error and inspect types with `#check`; inspect definitions with `#print` when needed.
2. Add the smallest useful type annotation, named argument, or explicit implicit argument.
3. Check imports, namespaces, scopes, local attributes/options, and instance availability.
4. Reshape the goal/context: `show`, `have`, `suffices`, `revert`, or `generalize` while preserving needed equalities.
5. Change proof method: `exact` ↔ `apply`; `rw` ↔ controlled `simp`; datatype induction ↔ functional induction; ordinary cases ↔ dependent matching.
6. Escalate logic/computation deliberately: well-founded recursion, extensionality, or classical choice only when the task requires them.
7. If the assumptions are insufficient or the relevant API is outside this book, report that limitation instead of fabricating a theorem or instance.

## Core Frameworks & Mental Models

### Propositions are types; proofs are terms
A proposition is a type in `Prop`, and proving it means constructing a term of that type. Use this model to read goals structurally: implication is a function type, universal quantification is dependent function space, conjunction and existence are constructor-built data in `Prop`, and elimination corresponds to consuming a proof through its recursor or pattern match.

### Goal-state tactics are proof-term construction
Tactics transform a goal into subgoals while constructing a proof term behind the interface. Judge a tactic by the proof obligation it exposes. `apply` asks for a theorem's premises; `constructor` asks for constructor fields; `cases` supplies one branch per constructor; `induction` also supplies induction hypotheses.

### Elaborator information flows both ways
Lean infers omitted information from explicit arguments and expected types. Before forcing every parameter manually, provide a useful expected type or local annotation. When inference fails, expose the full declaration with `@`, inspect it, and add only the information the elaborator lacks.

### Constructors and recursors determine the proof interface
An inductive declaration generates constructors and an elimination principle. Inspect them before designing a proof. For indexed families, constructor result indices encode constraints; preserve them rather than flattening the problem into an ordinary case split.

### Align induction with recursion
Induct on the argument a definition actually recurses over. If the theorem mirrors a recursive function's control flow, functional induction can produce better hypotheses than datatype induction. If an induction hypothesis is over-specialized, generalize/revert dependent values before induction.

### Rewriting has an escalation path
Use `rfl` for definitional equality; `rw` for one known substitution; `simp` for repeated canonical simplification; `calc` for readable transitive chains; congruence for equality under functions; `conv` for precise occurrence/binder navigation. Keep the simplifier's rule set narrow when predictability matters.

### Total recursion needs a visible descent argument
Start with structural recursion. When recursive calls are mathematically decreasing but not constructor subterms, choose a well-founded relation or measure with `termination_by` and prove every descent with `decreasing_by`. The termination proof is part of the trusted definition.

### Type classes are an inference graph
An instance goal launches search whose success depends on concrete input parameters, active scopes, priorities, and chained instances. Diagnose stuck metavariables before changing global priorities. Type-class-powered coercions share the same inference constraints.

### Logic and computation have a boundary
`propext`, quotient-based function extensionality, and classical choice expand convenient reasoning. Extensionality-related casts can obstruct kernel normalization; choice can turn data definitions into `noncomputable` ones. Distinguish proof validity, kernel reduction, and compiled evaluation when making computational claims.

## Self-Check

Before finalizing an answer or Lean proof, verify:
- Did I identify the user's real goal: proving, defining, debugging elaboration, termination, inference, or computation?
- Does the chosen method match the goal's constructor/recursor/equality/recursive shape?
- Are all required imports, scopes, instances, types, and hypotheses available?
- Did case analysis or generalization discard an equality or dependent relationship that the proof needs?
- Is `simp` using an intentional rule set, and did rewriting change only intended occurrences?
- Does each induction hypothesis correspond to the recursive structure actually used?
- Does every recursive call have a valid structural or well-founded descent argument?
- Are classical axioms or choice necessary, and do they alter executability?
- Are there unresolved placeholders, invented lemmas, or unsupported assumptions?
- When the source's Lean 4.33.0 syntax may differ from the installed version, did I inspect the current environment instead of assuming compatibility?

## Chapter Index

| # | Title | Operational focus |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction | trust model, theorem proving workflow |
| [ch02](chapters/ch02-dependent-type-theory.md) | Dependent Type Theory | types, universes, dependency, elaboration |
| [ch03](chapters/ch03-propositions-and-proofs.md) | Propositions and Proofs | Curry–Howard, connectives, classical logic |
| [ch04](chapters/ch04-quantifiers-and-equality.md) | Quantifiers and Equality | `∀`, `∃`, equality, `calc`, substitution |
| [ch05](chapters/ch05-tactics.md) | Tactics | goal transformation, rewriting, simplification |
| [ch06](chapters/ch06-interacting-with-lean.md) | Interacting with Lean | diagnostics, namespaces, attributes, notation |
| [ch07](chapters/ch07-inductive-types.md) | Inductive Types | constructors, recursors, induction, indexed families |
| [ch08](chapters/ch08-induction-and-recursion.md) | Induction and Recursion | termination, functional/dependent induction |
| [ch09](chapters/ch09-structures-and-records.md) | Structures and Records | fields, objects, updates, inheritance |
| [ch10](chapters/ch10-type-classes.md) | Type Classes | instance search, decidability, coercions |
| [ch11](chapters/ch11-the-conversion-tactic-mode.md) | The Conversion Tactic Mode | precise subterm navigation and rewriting |
| [ch12](chapters/ch12-axioms-and-computation.md) | Axioms and Computation | extensionality, quotients, choice, computation |

## Topic Index

- **axioms / `#print axioms` / soundness** → ch01, ch03, ch08, ch12
- **`calc`, congruence, equality substitution** → ch04
- **case analysis / constructor reasoning** → ch05, ch07
- **choice / `noncomputable` / excluded middle** → ch03, ch12
- **coercions** → ch06, ch10
- **conversion mode / occurrence targeting** → ch11
- **`Decidable` / `decide`** → ch10, ch12
- **dependent functions / implicit arguments / universes** → ch02
- **dependent pattern matching / inaccessible patterns** → ch07, ch08
- **elaboration / metavariables / expected types** → ch02, ch06, ch10
- **existentials / witnesses** → ch04
- **function/propositional extensionality** → ch12
- **functional induction / `fun_cases`** → ch08
- **inductive families / recursors / positivity** → ch07
- **instance search / `outParam` / scoped instances** → ch10
- **messages / imports / namespaces / options / notation** → ch06
- **pattern matching / structural recursion** → ch08
- **propositions as types / logical connectives** → ch03
- **quotients / setoids / representative independence** → ch12
- **`revert` / `generalize` / induction-hypothesis repair** → ch05, ch07, ch08
- **`rw` / `simp` / `simp only`** → ch04, ch05, ch11
- **structures / records / inheritance** → ch09
- **tactic combinators / subgoal management** → ch05
- **termination / `termination_by` / `decreasing_by`** → ch08

## Supporting Files

- [glossary.md](glossary.md) — significant terms with chapter references
- [patterns.md](patterns.md) — reusable proof, recursion, and diagnosis procedures
- [cheatsheet.md](cheatsheet.md) — compact routing and decision rules

## Scope & Limits

This skill operationalizes the uploaded edition of *Theorem Proving in Lean 4*, which states that it assumes Lean 4.33.0. It does not attempt to cover every Mathlib tactic, theorem, or later Lean API. When current declarations differ, inspect the installed environment. When assumptions do not entail the requested theorem, return the gap explicitly. The skill can guide proof construction without the source book, but executable Lean verification still requires a Lean toolchain.
