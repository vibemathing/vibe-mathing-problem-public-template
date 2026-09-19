---
name: xena-formalization-method
description: "Operational methods distilled from the Xena Project blog by Kevin Buzzard and contributors for formalizing mathematics in Lean: statement design, proof-state work, equality and rewriting, definition/API engineering, representation choices, research-scale project planning, trusted automation, teaching, AI autoformalization, and counterexample verification."
when_to_use: "formalize this theorem in Lean; help me state this mathematics precisely; why does rw/refl/exact/change fail; design a mathlib-style definition or API; choose a representation for a formalization; debug coercions or typeclasses; plan a large Lean research project; build a formalization blueprint; teach or learn formal mathematics; verify an AI-generated proof; audit an AI-generated Lean statement or definition; find and certify a counterexample; decide whether autoformalization is suitable; review a formal proof for trust or semantic correctness; 用 Lean 形式化/设计定义/检查 AI 数学证明"
allowed-tools: Read Grep
argument-hint: "[topic, theorem, Lean error, project, framework, or chapter]"
---

# Xena Formalization Method

Knowledge base compiled from the complete supplied Xena Project blog mirror (133 canonical units, 2017–2026). It captures operational methods and failure modes, not historical prose. Concrete Lean syntax and mathlib APIs in the source span Lean 3 and Lean 4; verify current names in the user's environment.

## What this skill does

Use this skill to turn informal mathematics or formalization problems into a controlled workflow: classify the task, make the statement precise, select a representation and API, construct or diagnose a proof, recover from failure, and validate meaning as well as compilation. It also covers research-scale dependency planning, teaching, AI-generated formal mathematics, and verified counterexample workflows.

## Do not use it when

- The user only wants an ordinary mathematical answer and has no formalization, proof-engineering, verification, or theorem-prover goal.
- The task is pure Lean software engineering unrelated to mathematical meaning (build systems, editor configuration, general metaprogramming). Use a programming/Lean reference instead.
- The request asks for the *current* name/signature of a mathlib theorem and you have not checked the live library. This skill gives conceptual routing; historical API names can drift.
- A formal statement itself is unavailable and the user asks you to certify a proof. First obtain or construct the exact statement.

## Inputs

At minimum identify the user's mathematical goal. When available also collect: intended theorem statement; Lean version/imports; current goal state/error; existing definitions; required level of generality; whether computation matters; whether classical choice is acceptable; and whether the artifact is human-written or AI-generated.


## How to Use This Skill

- **No topic supplied:** use the routing table and core operating method to classify the task.
- **Topic/framework supplied:** load the matching chapter from the Topic/Chapter Index before answering.
- **Chapter supplied:** read that chapter plus any linked supporting file needed for the task.
- **Concrete Lean code requested:** apply the conceptual method, then verify current Lean/mathlib names and compile in the user's toolchain; historical source syntax is version-sensitive.

## Routing policy

Classify the request before proving anything.

| Task | Route | Load |
|---|---|---|
| Translate prose into Lean / audit a theorem statement | Statement semantics | [01](chapters/ch01-orientation-and-statement-routing.md), [12](chapters/ch12-ai-autoformalization-and-semantic-audit.md) |
| Small/medium proof construction | Proof-state loop | [02](chapters/ch02-types-proof-terms-and-proof-state.md), [03](chapters/ch03-proof-construction-and-tactic-selection.md) |
| `rw`/`rfl`/`exact`/`change`/casts fail | Equality diagnosis | [04](chapters/ch04-equality-rewriting-and-normalization.md) |
| Inductive data or quotient | Eliminator/universal-property route | [05](chapters/ch05-induction-recursors-and-quotients.md) |
| New definition or reusable library object | API engineering | [06](chapters/ch06-definition-api-and-library-engineering.md) |
| Representation, classical choice, computability | Representation route | [07](chapters/ch07-representation-specification-and-computation.md) |
| Heavy automation / trust / proof certificates | Trusted automation | [08](chapters/ch08-automation-reflection-and-trust.md) |
| Limits, continuity, filter abstractions | Analysis abstraction | [09](chapters/ch09-filters-topology-and-useful-abstraction.md) |
| Large modern theorem / many prerequisites | Research blueprint | [10](chapters/ch10-research-blueprints-and-library-growth.md) |
| Teaching/learning/collaboration | Pedagogy route | [11](chapters/ch11-teaching-learning-and-collaboration.md) |
| AI-generated statement/definition/proof | AI verification route | [12](chapters/ch12-ai-autoformalization-and-semantic-audit.md) |
| Universal conjecture / machine-generated witness | Counterexample route | [13](chapters/ch13-counterexamples-benchmarks-and-proof-digestion.md) |
| Repeated failure, old syntax, unclear trust | Recovery audit | [14](chapters/ch14-failure-recovery-version-drift-and-self-check.md) |

## Core operating method

### 1. Freeze the mathematical claim

Write the intended claim before proof search. Make types, structures, quantifier order, domains, and edge conditions explicit. Ask what “same” means here: literal/definitional equality, proved equality, extensional equality, isomorphism, or a weaker equivalence. For AI-generated formalizations, compare the formal claim to the human claim line by line. A compiled proof of a mistranslated statement has no value for the intended theorem.

### 2. Choose the interface that matches downstream work

Prefer a specification, universal property, or typeclass interface when client theorems should survive implementation changes. Keep concrete constructions when they expose facts the abstract interface does not, or when efficient computation needs them. If two representations are useful, prove a bridge and operation-compatibility lemmas rather than forcing one representation to serve every purpose.

A definition is incomplete as library infrastructure until its basic API exists: constructors/eliminators, extensionality, coercions or instances, simplification/canonicalization lemmas, and characteristic theorems. Test the API immediately on representative downstream proofs.

### 3. Run the proof-state loop

Work one or two justified transformations ahead:

1. Read the exact goal and hypotheses.
2. Use a structural move (`intro`, `apply`/`refine`, `exact`, `cases`, `split`, `induction`, local `have`) that mirrors the mathematics.
3. Re-read the new state.
4. Normalize only enough to expose a known theorem or solver domain.
5. Use automation after the goal has the right shape.

Build an explicit proof first when the route is unclear. Compress later. Goal-state feedback is part of the reasoning process, especially on research proofs where humans cannot keep every object in working memory.

### 4. Normalize before automation

For structural equalities, try extensionality. For algebraic expressions, orient rewrites toward a stable normal form, then use the solver appropriate to the domain (`ring`, linear/nonlinear arithmetic, numeral normalization, library search, etc.). Do not ask a tactic to cross a representation boundary or invent a missing hypothesis. Powerful tactics are acceptable because the kernel rechecks their output; their heuristics themselves are not the trust anchor.

### 5. Diagnose failure in a fixed order

When a proof stalls, inspect:

1. parse/precedence/scope;
2. missing or wrongly ordered hypotheses/quantifiers;
3. syntactic vs definitional vs propositional equality;
4. wrong representation or abstraction level;
5. missing extensionality/simp/coercion/typeclass API;
6. theorem proved at the wrong generality;
7. missing library infrastructure;
8. false, vacuous, or mistranslated statement.

Changing tactics repeatedly without identifying the layer is low-value search.

### 6. Scale research targets by dependencies

For a large theorem, formalizing the exact statement is a milestone of its own. Build a dependency graph: definitions → reusable infrastructure → reductions → delicate core lemmas → target. Mark nodes done, ready, blocked, or temporarily assumed. Parallelize independent branches. Temporary axioms/sorries can unblock architecture during development only when they are explicit, minimal, tracked, and discharged before a finished artifact.

Let important targets drive library growth. General infrastructure becomes valuable when a real client proof demonstrates that the API works. Move reusable components upstream or into a maintained shared layer; otherwise version drift makes large projects expensive.

### 7. Treat AI output according to artifact type

- **AI proof of an already-audited formal statement:** compile/type-check it; for high stakes inspect axioms/dependencies and consider an independent checker. The proof may still be ugly, but logical gaps should be rejected by the checker.
- **AI theorem statement or definition:** perform human semantic review. Compilation cannot detect a missing axiom, flipped quantifier, wrong generality, or a definition that captures the wrong concept. Test standard examples, nonexamples, and characterization theorems.
- **AI informal proof:** treat as untrusted mathematical prose. One unjustified assumption is enough to invalidate a long argument. Request or construct a formal certificate when feasible.
- **AI counterexample:** re-audit the conjecture statement, then verify the witness formally. After correctness is secured, digest the example into a human explanation.

## Failure recovery

If the preferred route fails, change the *representation or interface* before escalating automation. A quotient problem may need its lift/eliminator; an equality problem may need extensionality or `convert`; a computation may need a binary/efficient representation with a proof bridge; a universal-property proof may need an explicit model for element-level facts; a stalled research target may need a missing definition or a different reference proof.

Return “insufficient to determine” when the formal claim, dependencies, or semantic correspondence cannot be established. Never infer truth from a famous source, a plausible LLM answer, or a successful numerical guess.

## SELF_CHECK

Before returning a result, verify all of the following:

- Did I identify the user's actual formalization goal and choose the right route?
- Are all types, structures, quantifiers, and domain hypotheses present?
- Am I relying on the correct notion of equality/equivalence?
- Did I choose a representation/API compatible with the required operations?
- Did I use automation only after satisfying its preconditions?
- Did I miss an edge case, hidden choice, nonempty/nonzero assumption, or version-sensitive API?
- If I used temporary axioms/sorries, are they explicitly tracked and absent from the final artifact?
- If AI generated the statement/definition, did a human-style semantic audit occur?
- If AI generated the proof, did a proof checker validate the exact intended statement?
- For a large result, can a fresh reader find the dependency path and the human explanation?


## Chapter Index

| # | Chapter | Core capability |
|---|---|---|
| 01 | [Orientation and statement routing](chapters/ch01-orientation-and-statement-routing.md) | task classification, type-first disambiguation |
| 02 | [Types, proof terms, and proof state](chapters/ch02-types-proof-terms-and-proof-state.md) | Curry–Howard, local proof-state loop |
| 03 | [Proof construction and tactic selection](chapters/ch03-proof-construction-and-tactic-selection.md) | structural tactics, explicit-first proofs |
| 04 | [Equality, rewriting, and normalization](chapters/ch04-equality-rewriting-and-normalization.md) | equality layers, extensionality, normalization |
| 05 | [Induction, recursors, and quotients](chapters/ch05-induction-recursors-and-quotients.md) | eliminators, quotient universal properties |
| 06 | [Definition, API, and library engineering](chapters/ch06-definition-api-and-library-engineering.md) | interface design, simp/coercion/typeclass APIs |
| 07 | [Representation, specification, and computation](chapters/ch07-representation-specification-and-computation.md) | dual representations, choice/computability |
| 08 | [Automation, reflection, and trust](chapters/ch08-automation-reflection-and-trust.md) | proof certificates, kernel trust |
| 09 | [Filters, topology, and useful abstraction](chapters/ch09-filters-topology-and-useful-abstraction.md) | `map`/`comap`/`Tendsto`, abstraction tests |
| 10 | [Research blueprints and library growth](chapters/ch10-research-blueprints-and-library-growth.md) | dependency graphs, staged assumptions |
| 11 | [Teaching, learning, and collaboration](chapters/ch11-teaching-learning-and-collaboration.md) | familiar-math onboarding, collaborative debugging |
| 12 | [AI autoformalization and semantic audit](chapters/ch12-ai-autoformalization-and-semantic-audit.md) | statement/definition audit, proof verification |
| 13 | [Counterexamples, benchmarks, and proof digestion](chapters/ch13-counterexamples-benchmarks-and-proof-digestion.md) | witness verification, benchmark integrity |
| 14 | [Failure recovery, version drift, and self-check](chapters/ch14-failure-recovery-version-drift-and-self-check.md) | recovery ladder, release audit |

## Topic index

- equality / `rw` / `rfl` / `change` / `exact` / `convert` → [04](chapters/ch04-equality-rewriting-and-normalization.md)
- induction / recursive definitions / equality induction / quotients → [05](chapters/ch05-induction-recursors-and-quotients.md)
- definitions / APIs / simp lemmas / coercions / typeclasses / generality → [06](chapters/ch06-definition-api-and-library-engineering.md)
- specification vs implementation / choice / computability / total functions → [07](chapters/ch07-representation-specification-and-computation.md)
- reflection / kernel / proof certificates / trust → [08](chapters/ch08-automation-reflection-and-trust.md)
- filters / `map` / `comap` / `Tendsto` / abstraction → [09](chapters/ch09-filters-topology-and-useful-abstraction.md)
- blueprint / research formalization / library gaps / parallel work → [10](chapters/ch10-research-blueprints-and-library-growth.md)
- beginner learning / course design / collaboration → [11](chapters/ch11-teaching-learning-and-collaboration.md)
- LLM / autoformalization / statement audit / misformalization → [12](chapters/ch12-ai-autoformalization-and-semantic-audit.md)
- counterexamples / benchmark integrity / machine-proof explanation → [13](chapters/ch13-counterexamples-benchmarks-and-proof-digestion.md)
- old Lean versions / recovery / release audit / security → [14](chapters/ch14-failure-recovery-version-drift-and-self-check.md)

## Supporting files

- [glossary.md](glossary.md) — key terms and operational meanings.
- [patterns.md](patterns.md) — reusable procedures with triggers and trade-offs.
- [cheatsheet.md](cheatsheet.md) — decision tables and quick rules.
- [references/source-map.md](references/source-map.md) — all 133 canonical source units.
- [references/provenance.md](references/provenance.md) — capability-to-source traceability.
- [references/capability-library.md](references/capability-library.md) — atomic capability catalog.
- [references/historical-lean-notes.md](references/historical-lean-notes.md) — how to handle Lean 3/4 drift.

## Scope and limits

This skill encodes the Xena Project's methods and engineering lessons. It does not ship the original blog, does not guarantee current mathlib theorem names, and does not replace domain mathematics needed for a specific research theorem. It can route such gaps precisely: missing mathematics, missing formal definitions, missing library API, proof search, or semantic uncertainty.
