# Decision Cheatsheet

## Goal/Hypothesis Router

| You see | Do first | If it fails |
|---|---|---|
| goal `A → B` / `∀ x, P x` | `intro` | inspect dependent order / implicit binders |
| `h : A → B` | apply `h` to evidence of `A` | prove/search the missing premise |
| goal `A ∧ B` / record | constructor/refine | name the constructor if field order is unclear |
| `h : A ∧ B` / record | projection or `rcases` | keep `h` if later API expects the package |
| goal `A ∨ B` | choose constructor explicitly | reconsider which branch is provable |
| `h : A ∨ B` | `cases`/`rcases` | ensure every branch closes |
| goal `∃ x, P x` | give a witness | search/derive the witness property |
| `h : ∃ x, P x` | `rcases h with ⟨x, hx⟩` | preserve dependent evidence together |
| equality | `rfl` if definitional, else `rw`/`calc` | check direction, location, reduction |
| recursive inductive property | `induction` | `revert`/`generalize` first if IH is weak |

## Search vs. Unfold

`Known Mathlib concept` → nearby source/Ctrl-click → names/autocomplete → `apply?` → semantic search → verify with `#check`.

`Fresh custom definition` → unfold one layer → expose logical/data shape → prove helper lemma → return to the abstraction.

Smell: repeated low-level field/function reduction on a mature concept usually means you descended too far.

## Automation Gate

| Residual goal | Tool family |
|---|---|
| ring-polynomial identity | `ring` |
| linear arithmetic | `linarith` |
| concrete numerals | `norm_num` |
| routine rewrites | narrow `simp` / `simp only` |
| generic small search | `aesop` after structure is exposed |
| standard continuity composition | `continuity` / library continuity lemmas |

Rule: expose quantifiers, cases, witnesses and definitions before broad automation.

## Failure Recovery

- `apply` mismatch → compare theorem conclusion with exact target; inspect implicit args/instances.
- `rw` no match → reverse direction, choose `at`, or expose the matching definition.
- `calc` transition fails → inspect relation direction/transitivity; insert a bridge step.
- `simp` surprises → `simp only [...]` and add lemmas deliberately.
- need a retained local definition → use `let`; use `have` for a proved proposition/fact.
- constructor goals arrive awkwardly → apply the constructor by name or use `fconstructor`.
- induction hypothesis too weak → generalize/revert before induction.
- theorem search empty → search neighboring abstraction levels and reshape the goal.

## Analysis Router

`limit/sequence/subsequence` → `Tendsto` + filters first; metric epsilon form for explicit estimates.

`Cauchy/convergence from completeness` → identify `MetricSpace`/`CompleteSpace` instances before proving estimates.

`normed/Banach/Hilbert` → inspect inherited metric/topological/typeclass structure; reuse instances.

`continuity` → try compositional continuity lemmas/automation; descend to metric/filter definitions only for custom estimates.

`EReal/ENNReal` → split infinity cases → prove finite branch → convert/lift to reals → return result.

`derivative` → prove `HasFDeriv*` → derive differentiability → use `fderiv`/ordinary derivative/gradient values.

## Project Stop Rules

Cut scope when representation work outweighs the theorem, key concepts have no usable library support, or every lemma opens a larger missing framework. Ship a compiling core, then expand.

## Final Check

Target matches mathematics; all binders/instances present; every case/witness covered; no unnecessary unfolding; automation is in-domain; exceptional cases handled; API names verified for the current Mathlib; no unexplained goals remain.
