---
name: mathematics-in-lean
description: "Operational guide from Mathematics in Lean by Jeremy Avigad and Patrick Massot. Use for Lean 4/Mathlib proof design, tactic choice, theorem search, algebra, logic, sets, induction, structures, hierarchies, linear algebra, topology, calculus, measure, and integration."
---

<!-- argument-hint: [Lean goal, topic, tactic, error, or chapter number] -->

# Mathematics in Lean
**Authors**: Jeremy Avigad, Patrick Massot | **Source release**: v4.19.0 | **PDF pages**: 212 | **Chapters**: 14 | **Generated**: 2026-09-11

Use this skill as a proof-engineering router for Lean 4 with Mathlib. The source teaches a style of formalization: read the goal and context, expose the right mathematical structure, reuse library abstractions, and let specialized automation handle routine residue.

## How to Use This Skill

- Give a **Lean goal/context or failing proof**: classify it, choose a method, and propose a proof path.
- Give a **mathematical theorem**: translate it to Lean-friendly objects and identify the likely Mathlib layer.
- Give a **topic** such as `filters`, `submodule`, `Finset`, `typeclass`, `fderiv`, or `integral`: load the relevant chapter.
- Give a **tactic problem** such as “rw does not match” or “typeclass instance problem is stuck”: use the recovery rules below.
- Give `chNN` to load that chapter directly. Use [glossary.md](glossary.md), [patterns.md](patterns.md), and [cheatsheet.md](cheatsheet.md) for quick lookup.

The book targets Mathlib around Lean release v4.19.0. Treat names and signatures as source-version guidance when working in newer Mathlib; verify changed APIs in the active environment.

## Core Frameworks & Mental Models

### 1. Read the proof state as an API
A Lean proof state has a **context** and a **target**. Before writing tactics, identify:
1. the target's outer shape (`=`, `≤`, `∀`, `→`, `∃`, `∧`, `∨`, `↔`, membership, function equality, etc.);
2. which hypotheses can be applied, rewritten, destructured, or specialized;
3. the algebraic/topological structures available through typeclasses;
4. whether a library theorem already expresses the intended step.

This classification determines the first tactic more reliably than guessing theorem names.

### 2. Use the weakest sufficient abstraction
Mathlib theorems are often stated for structures weaker than the concrete object in the goal. A fact about reals may only need a `CommRing`, `LinearOrder`, `Monoid`, `Module`, or `TopologicalSpace`. Prefer a theorem at the weakest useful level: it is more reusable and usually matches library organization better. When a theorem seems missing, search the parent structure before specializing further.

### 3. Separate structural work from routine algebra
Use structural tactics to expose the real subgoals, then automation on the residue.

- **Logic/data structure**: `intro`, `rintro`, `rcases`, `constructor`, `left`, `right`, `by_cases`, `induction`, `ext`.
- **Rewriting/normalization**: `rw`, `nth_rw`, `simp`, `simp only`, `dsimp`, `change`, `calc`, `convert`.
- **Routine domains**: `ring`, `noncomm_ring`, `abel`, `group`, `linarith`, `norm_num`, `omega`, `field_simp`.

Do not ask an arithmetic tactic to discover the mathematical decomposition. First provide the missing witness, case split, intermediate inequality, or helper lemma.

### 4. Prefer library interfaces over representations
Sets are predicates, subgroups/submodules/ideals are bundled subobjects, morphisms are bundled maps, quotients have lift principles, bases are linear equivalences, and filters are generalized sets. Use their public interfaces—`ext`, `map`, `comap`, `ker`, `range`, `span`, `mkQ`, `lift`, `repr`, `Tendsto`, `Eventually`—before unfolding definitions. Unfold only enough to make a stubborn goal legible.

### 5. Use universal properties as construction tools
When constructing a map out of a free or quotient-like object, look for the corresponding universal property:
- basis → `Basis.constr`;
- quotient → `lift`/`liftQ`;
- subgroup/submodule/ideal transport → `map`/`comap`;
- polynomial evaluation → `eval`, `eval₂`, `aeval`;
- free/presented algebraic objects → their lift/equivalence APIs.

These routes avoid coordinate-level or representative-level proofs.

### 6. Treat typeclass inference as part of proof design
Square-bracket arguments are synthesized. If inference is stuck:
1. make the carrier/base type explicit;
2. check the expected class with `#check`/type annotations;
3. verify the instance actually exists;
4. inspect whether two inheritance paths produce definitionally different data;
5. avoid redefining operations already supplied by a richer structure.

When designing hierarchies, prefer **forgetful inheritance**: extending a richer class should reuse existing data rather than invent another copy. This prevents bad diamonds.

### 7. Use filters to factor limit reasoning
For limits, continuity, “eventually,” and almost-everywhere reasoning, prefer filters over hand-expanded ε–N arguments. Translate concrete statements with a filter basis only when the concrete form helps. Compose limits algebraically with `Tendsto`; combine eventual facts with `Eventually.and`, `.mono`, or `filter_upwards`.

### 8. Let recursion determine induction
For recursive definitions, induct on the argument used by recursion. If another parameter must change in the inductive step, generalize it before induction. Use strong or well-founded induction when recursive calls go to arbitrary smaller inputs, and structural induction for lists, trees, formulas, finsets, and other inductive types.

## Routing Policy

| Goal / situation | First route | Load |
|---|---|---|
| Equality from identities | `rw` / `calc`; then domain automation | ch02 |
| Polynomial/ring identity | `ring` (commutative) or `noncomm_ring` | ch02 |
| Linear inequalities | expose needed inequalities, then `linarith` | ch02 |
| Concrete numerals | `norm_num` | ch02 |
| Natural/integer Presburger arithmetic | `omega`; case split if structural | ch05–06 |
| `∀` / `→` | `intro` / `rintro` | ch03 |
| `∃` | `use` to construct, `rcases` to consume | ch03 |
| `∧` / `↔` | `constructor` or destruct/projections | ch03 |
| `∨` / decidable case | `left`/`right`, `rcases`, `by_cases` | ch03 |
| Function/set/structure equality | `ext` then pointwise/component proof | ch03–04, ch07 |
| Set image/preimage | prefer preimage form when equivalent | ch04 |
| Recursive/finite object | induction aligned with constructors/recursion | ch05–06 |
| Typeclass/notation/hierarchy | inspect class path and instance synthesis | ch07–08 |
| Group/ring/subobject/quotient | bundled homs, map/comap, universal property | ch09 |
| Linear algebra | `LinearMap`/`Submodule`/`Basis` APIs before coordinates | ch10 |
| Limit/continuity/closure | `Tendsto`, `Eventually`, filter bases | ch11 |
| Derivative | `HasDerivAt`/`HasFDerivAt` first; `deriv`/`fderiv` second | ch12 |
| Integral/measure | establish measurability + integrability, then theorem | ch13 |

## Failure Recovery

- **`rw` cannot find the pattern**: inspect definitional wrappers. Try `dsimp`, `change`, a targeted `simp only`, or sparingly `erw`; check rewrite direction and occurrence (`nth_rw`).
- **`apply` creates a mysterious metavariable**: supply the intermediate object explicitly, use `trans`/`calc`, or pass more theorem arguments.
- **A theorem almost matches**: use `convert`; solve the resulting equality side-goals separately.
- **Automation stalls**: expose the hidden logical or algebraic structure first. A local `have` often turns a nonlinear-looking goal into a routine linear one.
- **Typeclass synthesis is stuck**: add type ascriptions or named arguments, check parent instances, and look for duplicated structure paths.
- **Coercions obscure the goal**: use `show`, `change`, or an explicit type ascription before rewriting.
- **A quotient/subobject proof becomes representative-heavy**: switch to `lift`, `map`, `comap`, `ker`, `range`, lattice operations, or an extensionality theorem.
- **A topological proof explodes into ε bookkeeping**: move back to filters; use a basis only at the boundary.
- **A derivative or integral theorem seems to require no hypothesis**: remember `deriv`, `fderiv`, and the integral are totalized with default values outside their intended domain. Check whether the theorem relies on that convention.
- **A library theorem name is unknown**: infer prefixes from the operation/conclusion, try editor completion or `apply?`, and search around a known neighboring theorem.

## SELF_CHECK

Before finalizing a proof or recommendation, verify:
- the user's mathematical goal and Lean target are aligned;
- the chosen theorem lives at an appropriate abstraction level;
- required typeclasses and side conditions are present;
- hidden quantifiers/connectives have been introduced or destructured correctly;
- automation is being used only after the goal has the right shape;
- no exception case from totalized definitions, empty finsets/types, quotients, or nontrivial filters was missed;
- the proof has no `sorry`/placeholder and all generated goals are closed;
- the script is readable enough to survive minor library changes;
- a second route (`simp` vs explicit lemmas, filter vs metric form, abstract vs coordinates) would reveal a mismatch if confidence is low.

## Chapter Index

| # | Title | Operational focus |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction | proof terms, tactics, interactive workflow |
| [ch02](chapters/ch02-basics.md) | Basics | rewriting, theorem application, algebraic automation |
| [ch03](chapters/ch03-logic.md) | Logic | quantifiers, connectives, cases, convergence proof structure |
| [ch04](chapters/ch04-sets-and-functions.md) | Sets and Functions | extensionality, image/preimage, inverses, Schröder–Bernstein |
| [ch05](chapters/ch05-elementary-number-theory.md) | Elementary Number Theory | divisibility, induction, recursion, prime arguments |
| [ch06](chapters/ch06-discrete-mathematics.md) | Discrete Mathematics | Finset/Fintype, counting, inductive types |
| [ch07](chapters/ch07-structures.md) | Structures | structures, instances, Gaussian integers |
| [ch08](chapters/ch08-hierarchies.md) | Hierarchies | class inheritance, morphisms, subobjects, quotients |
| [ch09](chapters/ch09-groups-and-rings.md) | Groups and Rings | bundled morphisms, subgroups, ideals, polynomials |
| [ch10](chapters/ch10-linear-algebra.md) | Linear Algebra | linear maps, submodules, bases, matrices, dimension |
| [ch11](chapters/ch11-topology.md) | Topology | filters, metric/topological spaces, compactness |
| [ch12](chapters/ch12-differential-calculus.md) | Differential Calculus | normed spaces, Fréchet derivatives, local inverse |
| [ch13](chapters/ch13-integration-and-measure-theory.md) | Integration and Measure Theory | measurability, AE, Bochner integrals |
| [ch14](chapters/ch14-index-and-navigation.md) | Index | source index mapped to skill navigation |

## Topic Index

- **algebraic automation** → ch02, ch05
- **bases / matrices / dimension** → ch10
- **classes / instances / typeclass inference** → ch07, ch08
- **compactness / continuity / filters** → ch11
- **derivatives / Fréchet derivatives** → ch12
- **existentials / conjunction / disjunction / negation** → ch03
- **Finset / Fintype / counting** → ch05, ch06
- **groups / subgroups / actions / quotients** → ch09
- **images / preimages / injective / surjective** → ch04
- **induction / recursion** → ch05, ch06
- **integration / measure / almost everywhere** → ch13
- **linear maps / submodules / quotients** → ch10
- **morphisms / `DFunLike` / `SetLike`** → ch08
- **polynomials / ideals / algebras** → ch09
- **rewriting / `simp` / `calc` / theorem search** → ch02
- **sets / extensionality** → ch04
- **structures / Gaussian integers** → ch07

## Supporting Files

- [glossary.md](glossary.md) — high-value Lean/Mathlib terms from the book
- [patterns.md](patterns.md) — reusable proof and design procedures
- [cheatsheet.md](cheatsheet.md) — compact routing and recovery rules

## Scope & Limits

This skill captures the book's operational methods and source-version Mathlib vocabulary. It does not replace the active project's compiler, imports, or current Mathlib documentation. For API-sensitive work, use the installed Lean environment as the final authority.
