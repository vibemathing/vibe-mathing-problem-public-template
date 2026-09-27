# Consolidated core: Mathematics in Lean

## Operating principle

A Lean proof is a typed program checked by the kernel. Effective mathematical formalization comes from aligning the mathematical structure, the library abstraction and the goal's syntactic shape.

## Read the state as an interface

For every goal identify:

- outer logical constructor;
- carrier types and their instances;
- local hypotheses and whether they are data or properties;
- coercions and overloaded notation;
- definitional forms hidden by notation;
- likely library abstraction.

Choose the first proof move from that shape rather than from superficial vocabulary.

## Core proof patterns

### Universal and implication goals

Introduce arbitrary inputs. Keep their generality; do not specialize before needed. For a contrapositive, verify that it is applied to an established implication and preserve the direction.

### Existential goals

Construct the witness explicitly, then prove membership/properties. If a classical existence theorem is used, keep it separate from later executable claims.

### Equality

Try, in order: definitional reduction, targeted simplification, rewriting with known equalities, congruence, extensionality, algebraic normalization, or a structural uniqueness theorem. Do not unfold representations merely because an equality is difficult.

### Sets and subtypes

Use extensionality for set equality and reduce to element membership. Distinguish `x : α` plus `x ∈ s` from `x : s`. Preserve subtype coercions explicitly when elaboration becomes ambiguous.

### Induction and recursion

Induct where the definition recurses. State a sufficiently general motive before induction. A valid induction report includes base case, arbitrary induction hypothesis, step and domain coverage.

### Algebra

Use homomorphism and subobject APIs before elementwise field manipulation. Separate structural lemmas from `ring`, `linarith`, `nlinarith`, `norm_num` or simplification. Verify solver preconditions and domains.

### Order

Choose the order interface matching the theorem: witnesses for constructive `≤`, lattice lemmas for sup/inf, monotonicity for composed functions, or order duality where supported. Do not conflate strict and non-strict variants.

### Topology and analysis

Work through filters and evidence-bearing predicates when the library does. Identify topology, norm, measure and convergence mode. Keep continuity, uniform continuity, differentiability, measurability and integrability distinct. Discharge neighborhood/eventual side conditions rather than unfolding everything.

### Linear algebra

Use linear maps, spans, kernels, ranges, bases and universal properties. Track scalar towers, finite-dimensional assumptions and coercions between bundled maps and functions.

### Quotients

Define on representatives only after proving representative independence. Prefer quotient lift/induction APIs. Equality of representatives is stronger than quotient equality.

### Measure and integration

Track almost-everywhere equality, measurability, integrability, finite measure and extended-real conversions. Do not transfer pointwise statements through an AE API without proof.

## Abstraction ladder

Prefer the weakest sufficient theorem:

1. reusable abstract interface;
2. domain-specific theorem;
3. local bridging lemma;
4. representation unfolding.

Working too concretely causes coercion and rewrite explosions; working too abstractly creates missing-instance obligations. Move one level at a time and record why.

## Theorem search

- Search names when terminology is known.
- Search types when the desired input/output shape is known.
- Inspect source for implicit parameters and namespaces.
- Test a candidate in a small `example` under the pinned imports.
- Prefer local environment truth over online snippets from another revision.

A search suggestion is not evidence until it elaborates locally.

## Tactic selection

- `intro`, `constructor`, `refine`, `use`, `cases`: expose logical/inductive structure.
- `rw`, `simp`, `simpa`, `change`, `convert`: align expressions and interfaces.
- `ext`, `funext`: prove equality through observations.
- arithmetic tactics: close supported arithmetic fragments after structure is exposed.
- `aesop` or broader automation: use as bounded search and review generated dependencies.

Prefer explicit intermediate facts when automation obscures a decisive step.

## Elaboration and typeclass diagnosis

When Lean reports a mismatch:

1. print the full expected and inferred types;
2. expose implicit arguments;
3. inspect coercions;
4. locate the missing instance edge;
5. distinguish definitional equality from a theorem-required conversion;
6. reduce to a minimal example.

Adding arbitrary type annotations or imports without diagnosis often hides the real gap.

## Formalization integrity

- never use placeholders or unsafe escape hatches;
- inspect axioms for important declarations;
- pin Lean and Mathlib revisions;
- keep the source-statement translation beside the theorem;
- avoid accidental vacuity from impossible hypotheses or empty types;
- test degenerate cases;
- request independent statement-faithfulness review.

## Learning and project progression

For unfamiliar domains, proceed from tiny executable examples to the relevant core APIs, then formalize a faithful small lemma before the root theorem. This is capability acquisition, not a controller-mandated mathematical route. Record reusable API knowledge rather than repeating blind tactic attempts.

## Completion boundary

A clean build establishes that Lean accepted the declaration under its environment and axioms. Root mathematical closure additionally needs source identity, faithful translation, dependency closure, independent replay and admission.
