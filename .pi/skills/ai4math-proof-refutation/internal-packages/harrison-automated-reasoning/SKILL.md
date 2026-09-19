---
name: harrison-automated-reasoning
description: "Logic automation: SAT, FOL, rewriting, QE/SMT, LCF, limits."
---

<!-- argument-hint: [formula, reasoning task, theory, method, or chapter] -->

# Harrison Automated Reasoning
**Source**: John Harrison, *Handbook of Practical Logic and Automated Reasoning* (Cambridge University Press, 2009) | **PDF**: 703 pages | **Main chapters**: 7 + 3 appendices | **Generated**: 2026-09-11

## Use this skill when
Use it for formal deductive reasoning where an agent must choose or explain an executable method: propositional satisfiability/validity, first-order proof search, unification, equality reasoning, rewriting/completion, specialized decision procedures, SMT-style combination, proof-producing automation, interactive proof architecture, or limits from undecidability/incompleteness.

Do not route ordinary probabilistic diagnosis, informal persuasion, modal/intuitionistic/higher-order/type-theoretic reasoning, inductive theorem proving, or model checking here unless the task is specifically to contrast them with the book's classical one-sorted first-order setting.

## Operating contract
1. **Fix the formal meaning first.** Identify the object language, signature, free/bound variables, quantifier scope, assumptions, and requested evidence: theorem, satisfying assignment, countermodel, normal form, proof certificate, or impossibility result.
2. **Classify before searching.** Prefer a complete decision procedure for a recognized fragment over unrestricted first-order search.
3. **Track the invariant of every transformation.** Distinguish logical equivalence, equisatisfiability, and one-way consequence. Definitional CNF and Skolemization usually preserve satisfiability properties, not literal equivalence.
4. **Preserve binding hygiene.** Apply capture-avoiding substitution, alpha-rename bound variables when needed, and keep Skolem symbols fresh with the correct dependency arguments.
5. **Use representations that fit the job.** ASTs for syntax, clauses for SAT/resolution, union-find/congruence classes for ground equality, rewrite normal forms for equations, BDDs when canonical Boolean sharing is advantageous.
6. **Treat search control as part of the method.** Completeness of an inference rule set does not make an arbitrary search strategy effective or fair.
7. **Return principled uncertainty.** A timeout, bounded saturation failure, nontermination, or unmet theory precondition is `unknown` unless it logically establishes a result.

## Router
| Situation | Primary route | Load |
|---|---|---|
| Propositional validity/SAT, Boolean circuit equivalence | Simplify → NNF as useful → definitional CNF → DPLL; use BDD for canonical/repeated Boolean manipulation | [ch02](chapters/ch02-propositional-reasoning.md) |
| First-order validity, contradiction, quantifier reasoning | Close/negate as appropriate → capture-safe normalization → Skolemize → tableau, resolution, or model elimination/MESON | [ch03](chapters/ch03-first-order-reasoning.md) |
| Ground equalities / uninterpreted functions | Congruence closure; Ackermann-style reduction if useful | [ch04](chapters/ch04-equality-rewriting.md) |
| Equational theory / simplifier / canonical forms | Orient equations with a well-founded ordering → rewrite; use completion for unresolved critical pairs | [ch04](chapters/ch04-equality-rewriting.md) |
| General first-order equality | Paramodulation/superposition-style equality inference, with resolution support | [ch04](chapters/ch04-equality-rewriting.md) |
| Presburger, dense orders, real/complex polynomial theories, ideal membership, geometry | Verify fragment → specialized quantifier-elimination/algebraic method | [ch05](chapters/ch05-decision-procedures-smt.md) |
| Mixed decidable theories | Purify → share equalities/arrangements → Nelson–Oppen/Shostak or SAT+theory organization; verify combination hypotheses | [ch05](chapters/ch05-decision-procedures-smt.md) |
| Result must be kernel-checked | Small trusted LCF-style kernel + derived rules + proof reconstruction/certificate replay | [ch06](chapters/ch06-interactive-theorem-proving.md) |
| User asks for a general complete algorithm/axiomatization | Check Church/Tarski/Gödel/Hilbert-tenth boundaries before promising decidability or completeness | [ch07](chapters/ch07-limitations-decidability.md) |
| Implementing the engine | Use structural recursion, immutable symbolic data, finite maps/sets/union-find, parser/prettyprinter round trips | [ch08](chapters/ch08-mathematical-background.md), [ch09](chapters/ch09-ocaml-symbolic-programming.md), [ch10](chapters/ch10-parsing-printing-formulas.md) |

## Core method selection
### Propositional
- Small atom count and explanation needed: truth-table enumeration can be acceptable.
- SAT-scale formula: avoid equivalent CNF expansion; introduce fresh definitions and solve the resulting clauses with DPLL-style search.
- Repeated equivalence/manipulation of related Boolean functions: consider a reduced ordered BDD. Variable ordering is a first-class choice; exponential BDD growth is a switch signal.
- Bounded Stålmarck saturation can prove many formulas efficiently. Exhausting only a fixed saturation depth without contradiction gives no refutation of validity.

### First-order
- If a recognized decidable fragment applies, use it.
- For general validity, refute the negation. Normalize bindings, Skolemize, then choose:
  - **Tableau/model elimination** for goal-directed proof search and compact proof reconstruction.
  - **Resolution** for clause-oriented saturation and mature redundancy controls.
  - **Herbrand expansion** mainly as a completeness foundation or tiny baseline; blind enumeration scales poorly.
- Unification must enforce the occurs-check for first-order terms. Propagate substitutions consistently.

### Equality
- **Ground EUF** → congruence closure.
- **Oriented equational simplification** → rewriting; establish termination, then check confluence/critical pairs if unique normal forms matter.
- **Completion** may fail because equations cannot be oriented or because generation diverges; then retain equations and change method.
- **Mixed FOL + equality** → paramodulation/superposition-style reasoning rather than expanding equality axioms indiscriminately.

### Decision procedures and SMT
- Quantifier elimination is a reusable architecture: normalize a target quantifier, eliminate it in the base fragment, then lift recursively.
- Exploit theory structure: linear integer arithmetic differs from real closed fields; polynomial ideal membership differs from general field reasoning.
- In theory combination, purification and shared-variable equalities are essential. Stable infiniteness, disjoint signatures, and convexity affect which combination protocol is sound/complete and how many arrangements must be explored.

## Failure recovery
| Failure signal | Recovery |
|---|---|
| Truth table / equivalent DNF-CNF explodes | Use definitional CNF and DPLL; avoid materializing all valuations. |
| Recursive DPLL exhausts memory or repeats conflicts | Use an explicit trail, unit propagation, non-chronological backtracking, learned clauses, and better branching heuristics. |
| BDD grows rapidly | Reconsider variable order, exploit definitions, or switch to SAT. |
| First-order search diverges | Check for a decidable fragment; impose fair/iterative-deepening control; change between tableau/MESON and resolution strategies; report unknown on resource cutoff. |
| Unification creates cyclic substitution | Reject it through the occurs-check. |
| Rewrite system loops | Reorient with a well-founded reduction ordering or stop using the rules as an unconditional simplifier. |
| Completion cannot orient a critical equation / keeps growing | Switch to a method that tolerates unoriented equalities, such as paramodulation/superposition. |
| Quantifier elimination blows up | Detect a smaller fragment (linear, monadic, finite-model, ideal-membership, etc.), simplify aggressively, or use theory-specific SAT/SMT cooperation. |
| Theory combination precondition fails | Use a dedicated combined procedure or an arrangement/SAT-level combination that explicitly handles the missing property. |
| Proof search found a result but trust is required | Reconstruct through a small kernel or replay a proof/certificate; do not treat a raw search trace as trusted. |

## SELF_CHECK
Before finalizing a reasoning result, verify:
- Did I formalize the user's actual goal and assumptions with the intended quantifier scope?
- Did I choose a method complete for this fragment, or clearly label a heuristic/bounded search?
- Did every transformation preserve the property I later rely on: equivalence, satisfiability, or consequence?
- Did I avoid variable capture, stale Skolem names, and missing unification occurs-checks?
- Did I satisfy termination/confluence or combination hypotheses before claiming their consequences?
- If the result is SAT, do I have a witness/model assignment? If UNSAT/valid, can I give a proof trace, kernel theorem, or independently checkable argument when requested?
- If the computation stopped early, did I return `unknown` with the limiting condition and next route?

## Chapter index
| File | Source coverage | Operational focus |
|---|---|---|
| [ch01](chapters/ch01-introduction-symbolic-foundations.md) | Ch. 1 | Formalization, syntax/semantics, symbolic representation |
| [ch02](chapters/ch02-propositional-reasoning.md) | Ch. 2 | SAT, DPLL, Stålmarck, BDD, Boolean encodings |
| [ch03](chapters/ch03-first-order-reasoning.md) | Ch. 3 | Substitution, Skolemization, Herbrand, unification, tableau/resolution/MESON |
| [ch04](chapters/ch04-equality-rewriting.md) | Ch. 4 | Congruence closure, rewriting, completion, paramodulation |
| [ch05](chapters/ch05-decision-procedures-smt.md) | Ch. 5 | Decidable fragments, QE, arithmetic/algebra/geometry, theory combination |
| [ch06](chapters/ch06-interactive-theorem-proving.md) | Ch. 6 | LCF kernel, derived rules, tactics, declarative proof, replay |
| [ch07](chapters/ch07-limitations-decidability.md) | Ch. 7 | Tarski, Gödel, computability, Church, limitative results |
| [ch08](chapters/ch08-mathematical-background.md) | Appendix 1 | Sets, relations, inductive definitions, well-foundedness |
| [ch09](chapters/ch09-ocaml-symbolic-programming.md) | Appendix 2 | Functional implementation patterns and data structures |
| [ch10](chapters/ch10-parsing-printing-formulas.md) | Appendix 3 | Parser combinators, precedence, formula/term printing |

## Topic index
- **BDD, Boolean circuits, CNF, DPLL, SAT, Stålmarck** → ch02
- **Herbrand, model elimination, Prolog, resolution, Skolemization, tableau, unification** → ch03
- **completion, congruence closure, equality, LPO, paramodulation, rewriting** → ch04
- **Gröbner, Nelson–Oppen, Presburger, quantifier elimination, real/complex fields, SMT, Wu** → ch05
- **LCF, natural deduction, proof certificates, sequent calculus, tactics** → ch06
- **Church, computability, Gödel, Hilbert's programme, Tarski, undecidability** → ch07
- **induction, relations, well-founded orders** → ch08
- **OCaml, finite maps, sets, union-find** → ch09
- **parsing, precedence, prettyprinting** → ch10

## Supporting files
- [glossary.md](glossary.md) — compact definitions and chapter pointers
- [patterns.md](patterns.md) — reusable operational procedures and trade-offs
- [cheatsheet.md](cheatsheet.md) — one-page-style method selection and warning signs

## Scope and source discipline
This skill is a method-level reconstruction of the uploaded 2009 book. It keeps the author's classical first-order, model-theoretic, constructive/algorithmic orientation and uses later terminology only when it is already reflected in the source (for example SAT modulo theories). It does not silently update 2009 historical status claims. For current software, patents, or open-problem status, verify separately.
