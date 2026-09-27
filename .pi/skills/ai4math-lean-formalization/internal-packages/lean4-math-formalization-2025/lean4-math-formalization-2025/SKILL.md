---
name: lean4-math-formalization-2025
description: "Operational Lean 4 mathematics formalization guide distilled from the 2025 SJTU–PKU AI4Math summer-school notes. Use for translating mathematical statements into Lean, reading proof states, choosing term/tactic constructions, finding Mathlib lemmas, debugging proofs, planning formalization projects, or working with sets, filters, limits, metric/normed spaces, continuity, continuous linear maps, and derivatives."
---

# Lean 4 Mathematical Formalization

**Source**: 2025 SJTU–PKU AI4Math Lean 4 summer-school archive | **Substantive lectures**: 7 | **Lecture pages**: 95 | **Generated**: 2026-09-12

## How to Use This Skill

- **No topic supplied** — use the core workflow and shape router below.
- **Topic supplied** — use the Topic Index, then load only the relevant chapter file before answering.
- **Chapter requested** — load that chapter directly.
- **Lean code, error, or tactic state supplied** — start from its exact types/state, then load a chapter only when the route needs deeper detail.

Keep chapter loading progressive: start with the smallest relevant file; add a connected chapter only when a dependency crosses topics.

Use this skill to turn a mathematical goal into a tractable Lean construction. Work **type-first**: understand the target and context, expose the right logical/structural layer, then apply a constructor, eliminator, reusable theorem, or focused automation.

## When to use

Use for Lean theorem statements/proofs, tactic-state debugging, Mathlib theorem/API search, natural-language-to-Lean translation, formalization project planning, and the set/analysis topics indexed below.

Do not use this as a substitute for checking the current Lean/Mathlib environment. API names in the source course reflect its Mathlib version; verify uncertain names with `#check`, source navigation, or search.

## Inputs to collect

Prefer the smallest useful set:

- mathematical statement or intended definition;
- current Lean code and tactic state, if any;
- error message and highlighted expression;
- imported modules / Mathlib version when an API or instance issue is suspected;
- constraints such as constructive proof, required abstraction, or allowed automation.

If crucial context is missing, first infer only what the types force. Ask for the tactic state or imports when multiple interpretations remain.

## Operational workflow

1. **Classify the task.** Is it statement formalization, proof construction, theorem search, debugging, project design, or an analysis-domain task?
2. **Read types before syntax.** Identify each context term and the target. For overloaded notation or mysterious operators, inspect with `#check`/source navigation; for instance issues, trace typeclasses.
3. **Recover the outer shape.** For natural language, recursively split into variables, assumptions and conclusion; identify the main logical operator of each block. For Lean, inspect the outer constructor of the goal/hypothesis.
4. **Route by shape.** Use the table below. Prefer explicit constructors/eliminators when they reveal intent.
5. **Search before expanding mature abstractions.** For Mathlib concepts, try source/Ctrl-click, naming/autocomplete, `apply?`, then semantic search. Verify a candidate with `#check`.
6. **Descend definitions only when useful.** `unfold` custom/new definitions when theorem support is sparse. If expansion makes the state harder, return to the higher-level API.
7. **Expose structure before automation.** After quantifiers, cases, witnesses and definitions are in the right form, use `simp`, `ring`, `linarith`, `norm_num`, `aesop`, `continuity`, etc. only where their domain fits.
8. **Blueprint long proofs.** Write the mathematical proof, list intermediate lemmas/state transitions, scaffold independent pieces, and shrink the target if representation complexity dominates.
9. **Validate.** Re-read the final theorem type, remaining goals, assumptions, instances, exceptional cases, and any current-version theorem names.

## Shape router

| Situation | First route | Typical follow-up |
|---|---|---|
| target `A → B` or `∀ x, P x` | `intro` | prove body with new context |
| hypothesis `A → B` / `∀ x, P x` | apply or function-apply it | solve generated premises / instantiate `x` |
| target conjunction / one-constructor structure | explicit constructor, `constructor`, or `refine` | solve fields separately |
| conjunction / structure hypothesis | projection, `rcases`, `obtain` | keep original package if useful |
| target disjunction | apply the intended constructor explicitly | prove chosen branch |
| disjunction hypothesis | `cases`/`rcases` | solve every constructor case |
| target existential | provide witness (`exists`/`refine`) | prove witness property |
| existential hypothesis | `rcases`/`obtain` | use witness and its proof |
| equality / substitution | `rfl` if definitional; else `rw`/`calc` | control direction and location |
| inductive data/proof | `cases` or `match` | use `induction` when recursive hypothesis is needed |
| negation / contradiction | `intro` for `¬P`; explicit contradiction | use classical `by_contra`/`by_cases` only when appropriate |
| algebraic normalization | structural preprocessing first | `ring` / `linarith` / `norm_num` / controlled `simp` |

For rationale and variants, load `chapters/ch03-first-order-logic-formalization.md`, `chapters/ch05-dependent-types-term-construction.md`, and `chapters/ch06-tactic-construction.md`.

## Global decision rules

### Term/tactic duality

A proof is a term whose type is the proposition. Tactics construct that term by transforming goals. If a tactic sequence becomes opaque, restate the step as the constructor/function application it is implementing; if a term becomes deeply nested, switch locally to tactic mode.

### Mathlib abstraction ladder

Stay at the highest layer that has usable theorems. Move downward to definitions when a custom concept lacks API support. Move upward again when raw definitions produce low-level obligations unrelated to the mathematics.

Search ladder: **nearby source and Ctrl-click → naming/autocomplete → `apply?` → semantic search (`#leansearch` or equivalent) → focused helper lemma/definition**.

### Formalization complexity control

Before committing to a large project, test representation and library support on a small core theorem. Prefer a special case, reduced generality, or a nearby existing abstraction over building a large missing framework under time pressure. Split the proof into lemmas and make dependencies explicit.

## Failure recovery

- **`apply` fails:** compare the theorem's result with the exact target; inspect implicit arguments and missing typeclass assumptions.
- **`rw` finds no match:** check direction, occurrence, definitional expansion, and whether rewriting belongs in a hypothesis via `at`.
- **`calc` rejects a step:** verify relation direction and an available transitivity instance; insert an explicit equality/ordering bridge.
- **`simp` behaves poorly:** reduce to `simp only [...]`, add local lemmas deliberately, or perform the structural step yourself.
- **a definition introduced with `have` no longer unfolds:** use `let` when definitional identity must be retained.
- **constructor subgoals appear in an awkward order:** name the constructor with `apply`; use `fconstructor` when preserving field order matters.
- **induction hypothesis is too weak:** `revert` dependent data or `generalize` the obstructing expression before induction.
- **theorem search stalls:** identify the mathematical structure required by the target, then search one abstraction layer above/below.
- **extended-real arithmetic stalls:** split infinite cases, reduce finite cases to real arithmetic, then automate.
- **proof/project keeps expanding:** return to the blueprint and cut scope to a completable core.

If source-version API names no longer resolve, preserve the mathematical method and re-search the current Mathlib API rather than forcing stale names.

## Analysis router

Load details only when needed:

- filters, `Tendsto`, sequences, metric convergence, Cauchy/completeness → `chapters/ch07-filters-limits-metric.md`;
- normed/inner-product spaces, open/closed sets, continuity → `chapters/ch08-normed-topology-continuity.md`;
- continuous linear maps, boundedness, operator norm, Fréchet/ordinary derivatives and gradients → `chapters/ch09-continuous-linear-derivatives.md`.

Prefer filter-level lemmas for compositional limit/continuity proofs and metric epsilon forms for concrete estimates.

## SELF_CHECK

Before returning a proof, plan, or diagnosis, confirm:

- the user's actual mathematical target matches the Lean target;
- the selected method's preconditions and instances are present;
- quantifiers, implicit parameters and dependency order are correct;
- every constructor/case/witness obligation is covered;
- automation is being used inside a domain it understands;
- no definition was unfolded farther than necessary;
- special cases (classical assumptions, empty types, infinities, domain restrictions) were handled;
- theorem/API names that may vary by Mathlib version were verified or clearly marked for verification;
- the final result leaves no unexplained goals and does not rely on `sorry` unless the user explicitly requested scaffolding.

## Chapter Index

| File | Use it for |
|---|---|
| [ch01-orientation-project-strategy](chapters/ch01-orientation-project-strategy.md) | course/project scoping, proof blueprints, representation risk |
| [ch02-lean-types-proof-states](chapters/ch02-lean-types-proof-states.md) | VS Code/InfoView, types, functions, propositions, proof states, basic calculation tactics |
| [ch03-first-order-logic-formalization](chapters/ch03-first-order-logic-formalization.md) | operator trees, logical rules, quantifiers, classical proof-state transforms |
| [ch04-mathlib-search-sets-blueprints](chapters/ch04-mathlib-search-sets-blueprints.md) | theorem search, unfold policy, sets/functions, limit-uniqueness blueprint |
| [ch05-dependent-types-term-construction](chapters/ch05-dependent-types-term-construction.md) | dependent functions, universes, inductives, structures, logic/equality/quantifiers, typeclasses |
| [ch06-tactic-construction](chapters/ch06-tactic-construction.md) | tactic toolbox, subgoals, induction/generalization, tactic anti-patterns |
| [ch07-filters-limits-metric](chapters/ch07-filters-limits-metric.md) | EReal, Euclidean spaces, filters, Tendsto, metric/Cauchy/completeness |
| [ch08-normed-topology-continuity](chapters/ch08-normed-topology-continuity.md) | normed/inner-product spaces, open/closed, continuity |
| [ch09-continuous-linear-derivatives](chapters/ch09-continuous-linear-derivatives.md) | continuous linear maps, operator norms, Fréchet derivatives, deriv/gradient |

## Topic Index

- **abstraction level / unfold** → ch04, ch07–ch09
- **apply / exact / intro / rfl** → ch02, ch03, ch06
- **automation** → ch02, ch04, ch06, ch08
- **blueprint / project planning** → ch01, ch04
- **cases / rcases / match / induction** → ch03, ch05, ch06
- **continuity / `continuity`** → ch08
- **dependent types / currying / universes** → ch02, ch05
- **derivative / gradient / Fréchet** → ch09
- **EReal / ENNReal / infinity cases** → ch07
- **exists / forall / logic** → ch03, ch05, ch06
- **filters / `Tendsto` / eventually** → ch07
- **Mathlib search / theorem names** → ch04
- **metric / Cauchy / CompleteSpace** → ch07
- **normed / Banach / inner product / Hilbert** → ch08
- **proof state / InfoView** → ch02, ch06
- **sets / image / preimage / injective / surjective** → ch04
- **simp / rw / calc** → ch02, ch06
- **typeclass / instance inference** → ch05, ch08

## Supporting files

- [cheatsheet.md](cheatsheet.md) — fast routing and recovery tables.
- [patterns.md](patterns.md) — reusable proof/formalization patterns and anti-patterns.
- [glossary.md](glossary.md) — key Lean/Mathlib terms with chapter references.

## Scope & limits

This skill covers every substantive lecture present in the uploaded 2025 course archive: 1A, 1B, 1C, 2B, 3A, 3B, and the mathematical-analysis lecture stored under `4B-analysis` (identified as 4C in the course schedule). The advertised 4A number-theory and 4B abstract-algebra lecture notes were absent from the archive, so this skill does not claim source-derived coverage of those courses.
