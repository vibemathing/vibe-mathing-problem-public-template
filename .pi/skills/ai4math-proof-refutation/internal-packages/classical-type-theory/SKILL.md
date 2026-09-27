---
name: classical-type-theory
description: "HOL λ-types, Skolemization, expansion proofs, unification."
---

<!-- argument-hint: [topic, method, theorem-proving problem, or chapter number] -->

# Classical Type Theory
**Author**: Peter B. Andrews | **Source**: Chapter 15 of *Handbook of Automated Reasoning* | **Pages**: 43 PDF pages (printed pp. 967-1007 plus contents) | **Major skill units**: 14 | **Generated**: 2026-09-11

## How to Use This Skill

Use this skill when a task involves formalizing or proving in classical simple type theory / higher-order logic, especially when first-order proof-search techniques must be extended to typed lambda terms, higher-order quantifiers, extensionality, or higher-order unification.

Before acting, identify five pieces of context when available: the target formula or specification; its type structure; proof mode (direct proof, refutation, or proof-object translation); the intended logical system (elementary type theory versus a setting with extensionality/descriptions/choice); and the acceptable search limits. If one is missing, state the assumption that affects method selection.

Route by problem shape:
- **Language, typing, lambda notation, equality, definitions** -> read [ch01](chapters/ch01-foundations.md) and [ch02](chapters/ch02-church-lambda.md).
- **Choice or Skolemization** -> read [ch03](chapters/ch03-choice-skolemization.md) before introducing higher-order Skolem symbols.
- **Expressiveness or type-theory-vs-set-theory modeling** -> read [ch04](chapters/ch04-expressiveness-tradeoffs.md).
- **Completeness argument for a proof procedure** -> read [ch05](chapters/ch05-unifying-principle.md).
- **Compact proof certificate / Herbrand-style higher-order reasoning** -> read [ch06](chapters/ch06-expansion-proofs.md).
- **Readable proof reconstruction** -> read [ch07](chapters/ch07-proof-translation.md).
- **Substitution must make lambda terms coincide** -> read [ch08](chapters/ch08-higher-order-unification.md).
- **A search bound on type order is being proposed** -> read [ch09](chapters/ch09-unbounded-types.md).
- **Need to invent higher-order instantiations during connection/mating search** -> read [ch10](chapters/ch10-expansion-search.md).
- **Resolution with non-unitary or delayed higher-order unification** -> read [ch11](chapters/ch11-constrained-resolution.md).
- **Equality/extensionality is central** -> read [ch12](chapters/ch12-extensional-resolution.md).
- **Need another instantiation generator or search-space reducer** -> read [ch13](chapters/ch13-instantiation-techniques.md).
- **Designing a prover or diagnosing systemic search failure** -> read [ch14](chapters/ch14-search-architecture.md) and [cheatsheet.md](cheatsheet.md).

When the question names a topic outside the core material below, read the linked chapter before answering. Preserve the distinction between source-derived claims and engineering choices made for the current system.

## Core Frameworks & Mental Models

### 1. Type information is search information
Treat types as more than correctness annotations. They constrain admissible applications and substitutions, sharply reducing candidate terms. When formalizing a domain, prefer a type assignment that exposes useful distinctions without inventing unsupported subtyping machinery.

### 2. Lambda abstraction is the operational form of comprehension
Represent functions, sets, and relations as typed functions and use lambda abstraction to build them from formulas. Normalize after substitution. This makes higher-order terms directly manipulable by proof search and unification rather than requiring a separate set-construction language.

### 3. Skolemization must preserve dependencies
In higher-order logic a casually introduced Skolem function can act like a choice function. When Choice is not intended, track each Skolem symbol's necessary arguments and prevent free variables inside those arguments from later being captured. Where convenient, enforce the expansion-tree dependency relation instead of materializing long Skolem terms.

### 4. Expansion proofs separate proof ideas from presentation
Use an expansion tree to record quantifier instantiations. Accept it as a proof only when its deep formula is propositionally valid and its dependency relation is acyclic. This compact representation exposes the essential instantiation structure and supports later translation into a readable natural-deduction proof.

### 5. Higher-order unification is search, not a single mgu call
Unification compares terms after lambda normalization. A most-general unifier may not exist, and search can fail to terminate. Bound exploration, preserve alternatives, and avoid treating lack of an early unifier as proof of non-unifiability.

### 6. Generate missing instantiations structurally
Unification of existing subformulas cannot generate every higher-order instantiation. Use typed primitive substitutions, projections, richer general substitutions, theorem-specific abbreviations, Z-match-style incremental elaboration, or related generators. Prefer forms whose equivalence class can be normalized to reduce redundant candidates.

### 7. Defer expensive unification when resolution needs it
For resolution-style search, attach unification requirements as constraints when no single mgu is available. Resolve/factor first, then simplify, merge, solve, or reject constraints as information accumulates. This keeps completeness options open while avoiding premature branching.

### 8. Extensionality changes the proof calculus
Methods complete for elementary type theory do not automatically handle the full extensional system efficiently. When functional or propositional extensionality is essential, route to extensional resolution or an explicit extensionality treatment rather than merely adding large axiom conjunctions to every goal.

### 9. Do not infer a safe type-order ceiling from the theorem
The chapter's metatheoretic warning is strong: low-order statements can require proofs containing variables of arbitrarily high type order. A practical prover may impose bounds, but a bound is a resource heuristic and can destroy completeness.

### 10. Search for the invariant proof core, then reconstruct style
Mating/connection search, expansion proofs, and resolution can produce proof data in forms unsuited to humans. Merge redundancy in the expansion proof and translate to natural deduction for checking, explanation, or mixed interactive/automatic work.

## Failure Recovery

- **Skolemization seems to derive Choice unexpectedly** -> stop using unrestricted higher-order Skolem functions; enforce necessary-argument discipline or dependency-aware instantiation.
- **Higher-order unification branches forever** -> apply resource bounds, preserve unresolved constraints, or change to a search regime that can postpone unification.
- **Search cannot invent a crucial predicate/set/function** -> add typed expansion options: projection, primitive substitution, gensub, theorem abbreviations, or incremental Z-match-style elaboration.
- **Clause count explodes** -> simplify/merge constraints early, prune unsatisfiable constraints, add typing/sort information, use component-style mating search, or tighten bounded search stages.
- **A proof fails only because of equality/extensionality** -> switch to an extensional calculus; do not keep expanding elementary rules indefinitely.
- **A proof is found but unreadable** -> extract/merge its expansion proof and translate the compact proof idea into natural deduction.
- **A finite type-order cap blocks progress** -> raise or remove the cap; classify it as a search heuristic rather than a logical limit.
- **Evidence is insufficient to choose a method** -> report what is missing and avoid claiming completeness or failure.

## SELF_CHECK

Before finalizing a result, verify: the user's real target is identified; the logical system and allowed principles are explicit; types and lambda normalization are handled consistently; higher-order substitutions respect dependencies; the selected search method can generate the required instantiations; extensionality/Choice assumptions have not entered silently; resource bounds are labeled as heuristic; failure alternatives were considered; and any proof artifact can be validated independently of its presentation.

## Chapter Index

| # | Title | Key capabilities |
|---|---|---|
| [ch01](chapters/ch01-foundations.md) | Foundations and early type theory | orders, quantification, comprehension, extensionality |
| [ch02](chapters/ch02-church-lambda.md) | Church type theory with lambda notation | function types, abstraction, normalization, definitions |
| [ch03](chapters/ch03-choice-skolemization.md) | Choice and Skolemization | dependency-safe Skolem terms, choice-risk diagnostics |
| [ch04](chapters/ch04-expressiveness-tradeoffs.md) | Expressiveness and modeling trade-offs | abbreviations, recursion, set theory comparison |
| [ch05](chapters/ch05-unifying-principle.md) | The Unifying Principle | abstract consistency, completeness proof pattern |
| [ch06](chapters/ch06-expansion-proofs.md) | Expansion proofs | deep/shallow formulas, dependency condition, proof certificates |
| [ch07](chapters/ch07-proof-translation.md) | Proof translations | merging, tactics, natural-deduction reconstruction |
| [ch08](chapters/ch08-higher-order-unification.md) | Higher-order unification | lambda-aware unification, Cantor example, failure properties |
| [ch09](chapters/ch09-unbounded-types.md) | Need for arbitrarily high types | completeness limits of type-order bounds |
| [ch10](chapters/ch10-expansion-search.md) | Searching for expansion proofs | primitive substitutions, gensubs, mating/component search |
| [ch11](chapters/ch11-constrained-resolution.md) | Constrained resolution | deferred unification, constraints, splitting rules |
| [ch12](chapters/ch12-extensional-resolution.md) | Extensional resolution | equality constraints, flex-rigid, extensionality rules |
| [ch13](chapters/ch13-instantiation-techniques.md) | Other instantiation methods | Z-match, Bledsoe-style generation, sorts, rippling |
| [ch14](chapters/ch14-search-architecture.md) | Search architecture and research agenda | method selection, search controls, open failure modes |

## Topic Index

- **abstract consistency / completeness** -> ch05
- **abbreviations / definitions** -> ch02, ch04
- **Axiom of Choice** -> ch03
- **comprehension / lambda abstraction** -> ch01, ch02
- **constrained resolution** -> ch11
- **dependency relation** -> ch03, ch06
- **extensionality / equality** -> ch01, ch12
- **expansion proof / expansion tree** -> ch06, ch10
- **gensubs / primitive substitutions / projections** -> ch10
- **higher-order unification** -> ch08, ch10, ch11, ch12
- **lambda conversion / normalization** -> ch02, ch08
- **mating / connections / component search** -> ch10
- **proof translation / natural deduction / tactics** -> ch07
- **Skolemization** -> ch03, ch06, ch11
- **sorts / subtypes / rippling / coloring** -> ch13
- **type-order bounds** -> ch09
- **type theory versus set theory** -> ch04
- **Z-match** -> ch13

## Supporting Files

- [glossary.md](glossary.md) - significant terms and precise meanings
- [patterns.md](patterns.md) - reusable proof-search procedures and recovery patterns
- [cheatsheet.md](cheatsheet.md) - compact routing rules, trade-offs, and failure diagnostics

## Scope & Limits

This skill covers Andrews's 2001 chapter on classical simple type theory and automatic theorem proving. It is strongest on logical representation, metatheoretic foundations, higher-order instantiation, unification, expansion proofs, and resolution-style search. It does not provide a modern implementation manual for any specific prover, and it does not cover constructive/dependent type theory in depth. Bibliography and index were read for terminology, provenance, and cross-reference coverage; detailed bibliographic records are not reproduced. The source PDF uses custom Type-3 fonts, so formulas were cross-checked against rendered pages where native text extraction was unreliable.
