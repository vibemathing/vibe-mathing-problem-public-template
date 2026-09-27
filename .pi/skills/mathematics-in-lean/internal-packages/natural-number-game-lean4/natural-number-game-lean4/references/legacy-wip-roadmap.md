# Legacy, WIP, and Roadmap Material

The uploaded repository contains inactive and work-in-progress material in addition to the nine active worlds. This reference preserves its role without treating unfinished levels as current curriculum guarantees.

## Legacy order/inequality files

`Game/Levels/LessOrEqual/Level_1.lean` through `Level_17.lean` are an older inequality sequence. Parts overlap the active existential-witness approach; several files are placeholders/stubs. Prefer the active `L01...L11` series for operational proofs unless the user explicitly asks about the legacy source.

An accompanying tactic-notes text records earlier design thinking around `use`, `cases`, and inequality presentation.

## Old advanced multiplication

`Game/Levels/OldAdvMultiplication/` contains an earlier four-level sequence plus `mul_left_comm`. It is useful as historical evidence for theorem design, but the active ten-level `AdvMultiplication` world is authoritative for current routing.

## Old logic/function worlds

- `OldFunction/` explores functions-as-implications and tactics such as `exact`, `intro`, `have`, and `apply` through older exercises.
- `OldProposition/` and `OldAdvProposition/` contain propositional-logic exercises: conjunction/disjunction construction and elimination, iff, cases, `by_cases`, `exfalso`, and excluded-middle-style material.

These files show broader pedagogical ambitions but are not imported by the active `Game.lean` curriculum.

## Work in progress

- `WIPAlgorithm/L11ac_rfl.lean` explores an `ac_rfl`-style associative/commutative normalizer.
- `WIPFuncProg/decide_level.lean` experiments further with computation/decision.
- WIP world files exist for hard problems, strict inequality, primes, even/odd, and related future material; several are empty/minimal scaffolds.

## Roadmap (`Game/Levels/Map.txt`)

The roadmap sketches future/earlier sequencing around:

- algorithms and functional programming;
- stronger inequality and `<` lemmas;
- advanced multiplication;
- divisibility and primes;
- harder worlds, parity, and strong induction.

It also sketches ordered-semiring-style goals and strict-order lemmas. Treat these as design intent, not as active theorem inventory.

## Use policy

1. Active worlds + foundational modules determine default skill behavior.
2. Legacy/WIP files can explain historical alternatives, planned tactics, or how the curriculum evolved.
3. Do not promise an inactive theorem/tactic is available in a live level unless its import context confirms it.
4. If the user asks to extend NNG4, this material can seed design ideas, but label those as source-derived roadmap concepts rather than completed features.
