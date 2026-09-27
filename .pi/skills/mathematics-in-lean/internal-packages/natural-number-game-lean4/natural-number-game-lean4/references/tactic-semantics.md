# NNG4 Custom Tactic Semantics

NNG4 intentionally wraps or weakens several tactics to keep proof steps visible. When producing a script for the game, prefer these semantics over assumptions from ordinary Mathlib usage.

## `rfl`

`Game/Tactic/Rfl.lean` implements a weakened reflexivity using restricted (`withReducible`) transparency. Practical consequence: opaque game operations do not disappear simply because their defining equations are known elsewhere. Use explicit game lemmas such as `add_zero` before expecting reflexivity.

## `rw`

`Game/Tactic/Rw.lean` makes the game's `rw` work like Lean's lower-level `rewrite` tactic: rewriting stays explicit and it omits the usual automatic reflexivity finish. After the intended substitution, a goal that has become `X = X` can remain open; run `rfl` explicitly.

## `induction`

`Game/Tactic/Induction.lean` customizes presentation/syntax for MyNat, including zero display and Lean3-style conveniences, and supports `generalizing`. The important semantic rule is standard structural induction; the important strategy is to align it with the game's recursive equations.

## `cases`

`Game/Tactic/Cases.lean` customizes case presentation and zero handling. Use it for constructor distinctions or eliminating existential/disjunction evidence when no IH is needed.

## `use`

`Game/Tactic/Use.lean` is intentionally weaker than Mathlib's full `use`: it does not run an automatic discharger that could hide the remaining equality. Expect to provide the witness and then prove the residual goal.

## `left` / `right`

`Game/Tactic/LeftRight.lean` supplies branch selection for suitable two-constructor inductive goals, used pedagogically for disjunctions.

## `have`

`Game/Tactic/Have.lean` provides the curriculum's `have`/`let`/`suffices` behavior. Use a local intermediate fact when a long proof needs a named bridge; do not create facts that merely duplicate a hypothesis.

## `simp_add`

Algorithm L04 defines the player-facing `simp_add` as `simp only [add_assoc, add_left_comm, add_comm]`. The globally imported support file `Game/Tactic/SimpAdd.lean` also defines an internal equivalent using separately reproved `_x` AC lemmas. Use `simp_add` only after its Algorithm World introduction when respecting progression.

## custom `decide`

`Game/Tactic/Decide.lean` first simplifies with the `MyNat_decide` simp set and then invokes `decide`. This matters because MyNat numerals/operations do not reduce identically to ordinary natural numbers. `Game/Tactic/LabelAttr.lean` registers the relevant simp attribute.

## `≠` display

`Game/Tactic/Ne.lean` adjusts presentation so negated equality is displayed as `≠`, while the proof meaning remains an implication to `False`.

## Mathlib imports

`Game/Tactic/FromMathlib.lean` deliberately imports only selected tactics (not a broad algebraic arsenal). A comment notes that importing `ring` would introduce root-level multiplication theorems that interfere with the MyNat pedagogy. Do not silently use powerful Mathlib tactics in a level-restricted solution.

## `xyzzy`

`Game/Tactic/Xyzzy.lean` defines an unrestricted axiom and a hidden macro that exacts it. This exists to close the FLT final boss as a game device. It is a trusted assumption added to the environment, not an arithmetic derivation.

## Operational check

Before giving a tactic script, determine whether the user wants:

1. **NNG4 level-valid** proof — use only unlocked game theorems/tactics and the custom semantics above;
2. **NNG4 source-level** explanation — later/imported infrastructure may be discussed explicitly;
3. **ordinary Lean/Mathlib** proof — translate ideas, but warn that names/types/tactic behavior may differ.
