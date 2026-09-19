---
name: mathematics-in-lean
description: "Operational knowledge from Mathematics in Lean by Jeremy Avigad and Patrick Massot. Use for Lean 4 and Mathlib theorem proving: choosing proof tactics, theorem discovery, logic and sets, induction, finite combinatorics, structures and typeclasses, groups/rings/quotients, linear algebra, filters/topology, derivatives, measure theory, and integration. Also use to diagnose elaboration, typeclass, coercion, quotient, and side-condition failures."
---

<!-- argument-hint: [goal, error, topic, theorem, tactic, or chapter] -->

# Mathematics in Lean
**Authors**: Jeremy Avigad and Patrick Massot | **Book snapshot**: v4.19.0 documentation | **Chapters**: 13 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task is to formalize, repair, explain, or plan a Lean 4 / Mathlib proof in the mathematical domains covered by the book. Given a goal or error, first classify it, then load only the chapter(s) named in the routing table. Keep project-specific APIs, current Mathlib declarations, and compiler feedback authoritative when they differ from this snapshot.

Do not load the whole skill for a narrow problem. Read the relevant chapter file, then consult `patterns.md` or `cheatsheet.md` for cross-cutting proof strategy.

## Operating Loop

1. **Read the goal literally.** Record the target, local hypotheses, inferred types, typeclass assumptions, coercions, and the outer logical constructor.
2. **Normalize only as needed.** Use `dsimp`, `change`, a focused `rw`, or `simp only` when the useful structure is hidden. Avoid broad simplification before understanding the target.
3. **Route by mathematical structure.** Prefer library lemmas and universal properties attached to the weakest sufficient structure. Use automation after the goal has the right shape.
4. **Make witnesses and branches explicit.** For `∃`, images, quotients, finite fibers, cases, and induction, expose the witness/case/induction hypothesis rather than hoping automation invents the mathematical plan.
5. **Check side conditions early.** Positivity, nonzeroness, integrability, measurability, finite-dimensionality, nontrivial filters, normality, and decidable equality often control whether a theorem applies.
6. **Escalate deliberately.** If the first method fails, diagnose the failure category below and switch route instead of repeating a tactic with small syntactic changes.
7. **Validate the proof shape.** Confirm the result uses the intended abstraction and does not depend on an accidental stronger assumption.

## Method Router

| Goal / symptom | Primary route | Load |
|---|---|---|
| Algebraic equality, inequality, theorem application | rewrite/calc + structural lemmas; then `ring`, `linarith`, `norm_num` as appropriate | [ch02](chapters/ch02-basics.md) |
| `∀`, `→`, `∃`, `¬`, `∧`, `↔`, `∨`; logical case split | constructor/destructor matching the outer connective | [ch03](chapters/ch03-logic.md) |
| Set identity, image/preimage, injective/surjective/bijection | extensionality, elementwise logic, image/preimage adjunction | [ch04](chapters/ch04-sets-functions.md) |
| Natural-number recursion, prime/divisibility argument | ordinary/strong/well-founded induction chosen from recursive dependency | [ch05](chapters/ch05-number-theory.md) |
| Finite sets/types, cardinalities, double counting, custom inductive data | Finset/Fintype representation + card lemmas; structural recursion/induction | [ch06](chapters/ch06-discrete-mathematics.md) |
| Define a mathematical object with fields/invariants | structure + projections + extensionality; install instances only when coherent | [ch07](chapters/ch07-structures.md) |
| Instance search, inheritance, morphism abstraction, reusable subobjects | typeclass hierarchy, `outParam`, `DFunLike`, `SetLike`; inspect diamonds | [ch08](chapters/ch08-hierarchies.md) |
| Groups, rings, ideals, quotient objects, actions, polynomial evaluation | bundled morphisms/subobjects + `map`/`comap`/kernel/range + universal properties | [ch09](chapters/ch09-groups-rings.md) |
| Linear maps, submodules, quotient spaces, bases, matrices, dimension | bundled linear maps/submodules; span/map/comap/quotient; basis universal property | [ch10](chapters/ch10-linear-algebra.md) |
| Limits, continuity, eventual statements, compactness/completeness | `Filter`, `Tendsto`, neighborhood bases, `Eventually`, topology assumptions | [ch11](chapters/ch11-topology.md) |
| Derivatives in R or normed spaces | `HasDerivAt` / `HasFDerivAt`, continuous linear maps, little-o | [ch12](chapters/ch12-differential-calculus.md) |
| Interval integrals, measures, a.e. facts, dominated convergence, Fubini | choose interval vs measure-theoretic integral; discharge measurability/integrability | [ch13](chapters/ch13-integration-measure.md) |

## Core Frameworks & Mental Models

### Match the outer constructor
Treat proof goals as data constructors. For `A → B` or `∀ x, P x`, introduce data; for `∃ x, P x`, supply a witness; for conjunctions construct both fields; for disjunctions choose or split cases; for equalities rewrite/calculate; for set equality use extensionality. This gives a deterministic first move for a large fraction of Lean goals.

### Prefer the weakest sufficient abstraction
If a theorem only needs a lattice, monoid, module, topological space, or filter, prove it there. Stronger concrete structures add coercions and instance obligations without improving the argument. Let typeclasses carry reusable laws.

### Convert before automating
Automation is strongest after semantic normalization. Expose hidden definitions with `change`/`dsimp`, orient equalities with `rw`, clear denominator/nonzero obligations before arithmetic solvers, and transform topological epsilon statements into filter statements when the library theorem lives there.

### Use universal properties as routing APIs
For spans, quotients, free groups, ideals, linear quotients, bases, induced/coinduced topologies, and similar objects, look for the constructor/lift/extensionality trio. Define a map by its required generators, prove the compatibility condition, then use the supplied uniqueness/extensionality theorem. This route is usually shorter and more stable than unfolding representations.

### Separate data from properties
Bundle structure when the object carries operations or a canonical map (`MonoidHom`, `LinearMap`, `ContinuousLinearMap`, subgroups, ideals, submodules). Keep predicates as propositions when multiple proof paths should collapse by proof irrelevance. Typeclass diamonds involving data can be harmful; diamonds involving propositions are usually benign.

### Use filters as generalized sets
Interpret a filter as a generalized set of inputs. `map` is a direct image, `comap` a pullback, filter order is generalized inclusion, and `Tendsto f F G` is `map f F ≤ G`. This single algebra covers sequence limits, point limits, infinity, one-sided/restricted behavior, neighborhoods, uniformity, and almost-everywhere statements.

### Prefer evidence-bearing analytic predicates
Use `HasDerivAt`, `HasFDerivAt`, `DifferentiableAt`, `Integrable`, `Measurable`, and their scoped variants when correctness depends on hypotheses. Functions such as `deriv` and integrals are totalized with default values outside their intended domain, so an apparently well-typed expression may hide a missing premise.

## Failure Recovery

- **Rewrite does nothing:** check direction, explicit arguments, definitional equality, coercions, and whether `change`/`dsimp` should expose the target first.
- **`apply` creates a mysterious metavariable:** the chosen lemma may contain an intermediate object Lean cannot infer. Prefer `calc`, name the intermediate with `have`, or provide named arguments.
- **Automation stalls:** isolate a polynomial fragment for `ring`, a linear-arithmetic fragment for `linarith`, concrete numerals for `norm_num`, Presburger arithmetic for `omega`, or finite propositional structure for `tauto`/`simp`.
- **Instance synthesis fails:** identify every type parameter in the desired instance. Add a type annotation or named argument; then inspect whether a parent class leaves a parameter unconstrained or whether two data paths form a bad diamond.
- **Set image proof becomes existentially noisy:** switch to a preimage/comap formulation or use the relevant Galois-connection lemma.
- **Induction hypothesis is too weak:** generalize the variables that change in the recursive call; for dependencies on all smaller naturals switch to strong induction.
- **Natural-number algebra misbehaves:** watch truncated subtraction and integer division. Rearrange before subtracting, prove divisibility/nonzero hypotheses, or move to a more suitable numeric type.
- **Quotient proof fights representatives:** use quotient `lift`, `map`, kernel/range, and provided equivalences. Avoid relying on definitional equality between quotient presentations.
- **Continuity proof fights function composition elaboration:** use source-style continuity combinators such as `hf.comp`, `.prodMk`, `.dist`, or the `continuity` tactic before manually exposing composition.
- **Limit proof repeats epsilon bookkeeping:** move to `Tendsto` plus `Eventually`; combine eventual facts with `.and`, `.mono`, or `filter_upwards`, and return to a basis only when concrete inequalities are needed.
- **Derivative theorem lacks a side condition:** prove an evidence-bearing derivative statement first and derive the `deriv`/`fderiv` equality from it.
- **Integral theorem unexpectedly returns zero or will not apply:** check integrability/measurability, finite measure or sigma-finiteness assumptions, and whether the theorem is for interval, set, or full-space integrals.

## Self-Check

Before finalizing a proof or recommendation, verify:

- the user's actual mathematical claim and intended generality are preserved;
- the selected theorem matches the available typeclass assumptions;
- hidden coercions and default-totalized definitions are understood;
- every existential witness, nonzero/positivity condition, measurability/integrability condition, and quotient compatibility condition is discharged;
- the proof uses a library abstraction that survives representation changes;
- any automation is applied to the fragment it is designed for;
- an alternate route is available if elaboration, instance search, or simplification becomes brittle;
- current compiler feedback takes precedence over names/API details from the v4.19.0 book snapshot.

## Chapter Index

| # | Title | Operational focus |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction | proof-state workflow, source/solution loop |
| [ch02](chapters/ch02-basics.md) | Basics | rewriting, theorem application, algebra/order tactics |
| [ch03](chapters/ch03-logic.md) | Logic | connective-driven proofs, classical reasoning, epsilon convergence |
| [ch04](chapters/ch04-sets-functions.md) | Sets and Functions | extensionality, image/preimage, inverse choices, bijections |
| [ch05](chapters/ch05-number-theory.md) | Elementary Number Theory | divisibility, primes, strong induction, recursion |
| [ch06](chapters/ch06-discrete-mathematics.md) | Discrete Mathematics | Finset/Fintype, counting, inductive types |
| [ch07](chapters/ch07-structures.md) | Structures | structures, instances, Gaussian integers |
| [ch08](chapters/ch08-hierarchies.md) | Hierarchies | inheritance, diamonds, morphism/subobject design |
| [ch09](chapters/ch09-groups-rings.md) | Groups and Rings | homs, subobjects, quotients, ideals, algebras, polynomials |
| [ch10](chapters/ch10-linear-algebra.md) | Linear Algebra | linear maps, subspaces, bases, matrices, dimension |
| [ch11](chapters/ch11-topology.md) | Topology | filters, metric/topological spaces, compactness/completeness |
| [ch12](chapters/ch12-differential-calculus.md) | Differential Calculus | derivatives, continuous linear maps, asymptotics |
| [ch13](chapters/ch13-integration-measure.md) | Integration and Measure Theory | interval integrals, measures, a.e., convergence theorems |

## Topic Index

- **automation / tactics** → ch02, ch03, ch05, ch06
- **bases / matrices / dimension** → ch10
- **classical choice / inverse functions** → ch04
- **compactness / completeness / Baire** → ch11, ch12
- **continuity / limits / filters** → ch03, ch11, ch12, ch13
- **derivatives / Fréchet derivative** → ch12
- **finite counting / pigeonhole** → ch06
- **groups / rings / ideals / quotients** → ch09
- **induction / recursion** → ch05, ch06
- **integration / measure / almost everywhere** → ch13
- **logic / quantifiers / connectives** → ch03
- **morphisms / subobjects / typeclasses** → ch07, ch08, ch09
- **sets / images / preimages / bijections** → ch04
- **span / submodule / linear map / quotient space** → ch10
- **structures / instances / diamonds** → ch07, ch08
- **theorem discovery / rewriting / calc** → ch02

## Supporting Files

- [glossary.md](glossary.md) — compact terminology index
- [patterns.md](patterns.md) — reusable proof and API patterns
- [cheatsheet.md](cheatsheet.md) — decision rules and failure triage

## Scope & Limits

This skill is synthesized from the uploaded *Mathematics in Lean* HTML snapshot and its accompanying Lean source/solution repository. The HTML content in the two uploaded bundles was text-identical. The documentation identifies itself as v4.19.0; the accompanying repository's `lean-toolchain` targets Lean 4.30.0 and Mathlib 4.30.0, so declaration names can drift. Use the current project compiler and Mathlib documentation to resolve API changes. The skill contains operational synthesis and compact examples, not a replacement copy of the book.
