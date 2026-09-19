# Chapter 12: Axioms and Computation

## Core Idea
Lean combines a constructive computational core with extensional and classical principles: propositional extensionality, quotients (supporting function extensionality), and choice. These principles are consistent with the intended logic, but they affect how terms compute: proof erasure helps compiled execution, while casts and choice can block kernel normalization or require `noncomputable` definitions.

## Frameworks Introduced
- **Proof vs computation audit**
  - When to use: a theorem/definition depends on extensionality, quotient reasoning, choice, or classical decidability.
  - How: separate logical validity, kernel reduction, and executable evaluation; identify whether axioms occur only in proofs or are used to manufacture data.
- **Extensional equality**
  - When to use: functions/predicates behave identically at every input but are not definitionally equal.
  - How: use `funext` for functions, `propext` for propositions, and compose them for sets/predicates.
- **Quotient lifting**
  - When to use: define operations on equivalence classes.
  - How: define the operation on representatives → prove it respects the relation → lift it to the quotient; use quotient induction to prove quotient-wide properties.
- **Choice boundary**
  - When to use: only `Nonempty α` or an existential proposition is available but a data-level witness is demanded.
  - How: `Classical.choice`/`choose` can select an element; mark data definitions depending on that selection `noncomputable` and do not claim a general extraction algorithm.
- **Classical consequence chain**
  - When to use: understand why excluded middle/decidability are available in `Classical`.
  - How: recognize that choice together with extensional principles yields excluded middle; proposition-level excluded middle can then supply classical decidability.

## Key Concepts
- **Propositional extensionality (`propext`)**: `p ↔ q` implies `p = q`.
- **Function extensionality (`funext`)**: pointwise equality implies equality of functions.
- **Quotient `Quot r`**: identifies representatives according to a relation generated into quotient equality.
- **`Quot.mk`**: inject a representative into a quotient.
- **`Quot.sound`**: related representatives become equal in the quotient.
- **`Quot.lift`**: define a function out of a quotient after proving representative independence.
- **`Quot.ind`**: prove a proposition for all quotient values from representatives.
- **`Setoid` / `Quotient`**: equivalence relation packaged with a type and the corresponding quotient interface.
- **`Nonempty α`**: proposition asserting existence of an inhabitant while erasing which inhabitant.
- **`Classical.choice`**: obtains an `α` from `Nonempty α` nonconstructively.
- **`choose` / `choose_spec`**: select a witness from an existential and recover its specification.
- **`noncomputable`**: declaration marker acknowledging Lean cannot generate general executable code from the definition.
- **Excluded middle**: `p ∨ ¬p` for every proposition.
- **Classical proposition decidability**: nonconstructive `Decidable p`, sufficient for branching but not an algorithm extracted from `p` itself.

## Mental Models
- Separate three questions: **Is the declaration logically accepted? Does the kernel reduce it to a canonical form? Can compiled evaluation run it?** Their answers can differ.
- Quotients require **representative independence**. A candidate function on quotient values is well-defined only if equivalent representatives map to equal outputs.
- `Nonempty α` lives in `Prop`, so it communicates existence while intentionally hiding computational witness information. Choice crosses that boundary nonconstructively.
- The historical constructive/classical distinction is operational here: constructive proofs can carry algorithms/witnesses, while classical existence reasoning may certify a fact without providing executable data.
- Proof irrelevance/erasure means many classical proofs can disappear from compiled code, but a choice used to build actual data cannot become an algorithm merely through erasure.

## Anti-patterns
- **Assuming pointwise-equal functions should close by `rfl`**: extensional equality is stronger than definitional equality.
- **Lifting a quotient function without proving respectfulness**: the result could depend on the chosen representative.
- **Treating `Classical.choice` as witness extraction algorithm**: `Nonempty` contains no data-level witness available to computation.
- **Expecting `#reduce` and `#eval` to agree operationally** after extensionality-related casts or proof erasure.
- **Marking a definition `noncomputable` without explaining why** when executability is part of the user's requirement.

## Code Examples
```lean
example (f g : α → β) (h : ∀ x, f x = g x) : f = g := by
  exact funext h
```
- **What it demonstrates**: equality of functions from pointwise equality.

```lean
example (p q : Prop) (h : p ↔ q) : p = q := by
  exact propext h
```
- **What it demonstrates**: proposition equality from logical equivalence.

```lean
open Classical

noncomputable def pick [Nonempty α] : α :=
  Classical.choice inferInstance
```
- **What it demonstrates**: data selection by classical choice must be treated as noncomputable.

```lean
def QuotMap {α β : Sort _} (r : α → α → Prop)
    (f : α → β)
    (h : ∀ a b, r a b → f a = f b) : Quot r → β :=
  Quot.lift f h
```
- **What it demonstrates**: quotient lifting requires a proof that the representative function respects the relation.

## Reference Tables
### Extensionality selection
| Equality target | Evidence | Principle |
|---|---|---|
| functions `f = g` | `∀ x, f x = g x` | `funext` |
| propositions `p = q` | `p ↔ q` | `propext` |
| predicates/sets | pointwise iff | `funext` outside + `propext` inside |
| quotient representatives | relation proof | `Quot.sound` |

### Quotient workflow
1. Choose representative type `α` and relation `r` (or a `Setoid`).
2. Prove equivalence when using `Quotient`/setoid semantics.
3. Build quotient values with `Quot.mk`/`Quotient.mk`.
4. To define `f̄`, first define representative `f`.
5. Prove `r a b → f a = f b`.
6. Lift with `Quot.lift`/`Quotient.lift`.
7. Use quotient induction to prove statements about arbitrary quotient values.

### Computation audit
| Dependency | Proof validity | Kernel reduction | Executable data impact |
|---|---|---|---|
| constructive recursive definition | checked | usually computational | executable if supported |
| `propext` / extensional casts | checked | casts may block normalization | proof content often erased |
| quotient extensional reasoning | checked | may introduce casts/axiom steps | lifted executable functions depend on erased proof obligations where valid |
| `Classical.choice` used only in proof | checked | may not normalize | often erased in compiled proof context |
| `Classical.choice` used to produce data | checked | no constructive reduction rule | definition requires `noncomputable` |

## Worked Example: unordered pairs by quotient
Goal: represent `(a, b)` and `(b, a)` as the same unordered pair.
1. Start with representatives `α × α`.
2. Define a relation saying two pairs are equal either componentwise or after swapping.
3. Prove reflexivity, symmetry, and transitivity; package it as a `Setoid`.
4. Define unordered pairs as the quotient of product representatives.
5. `Quotient.sound` proves the pair equals its swap because the representatives are related.
6. To define membership, first define `mem_fn a (x, y) := a = x ∨ a = y`.
7. Prove `mem_fn` is unchanged by the equivalence relation; the swap case is the key respectfulness argument.
8. Lift `mem_fn` to the quotient. Membership now depends only on the equivalence class, not on representative order.

This is the general quotient pattern: quotient equality is easy to obtain from the relation, while functions out of the quotient must prove representative independence.

## Worked Example: choice and a left inverse
For an injective `f : α → β` with inhabited `α`, classical choice can define a left inverse by selecting a preimage when one exists and using a default otherwise.

The proof that `linv f (f a) = a` can use injectivity and the specification of the chosen witness. Yet the definition of `linv` is `noncomputable`: deciding arbitrary existence and selecting a preimage came from classical principles, not an executable search procedure. If the application requires an actual algorithm, replace the classical existence premise with constructive search/decidability data.

## Failure Recovery
- `rfl` fails for extensionally equal functions → prove pointwise equality and use `funext`.
- quotient lift rejected → the respectfulness theorem is missing/wrong; find two related reps and verify outputs are equal.
- definition using `choose` rejected as computable → mark it `noncomputable` only if execution is not required; otherwise redesign with constructive witness data.
- `#reduce` sticks on a cast → inspect extensional axioms/quotients in the term; use theorem reasoning or compiled evaluation for the appropriate question.
- classical `Decidable p` is mistaken for algorithm → require a constructive `[Decidable p]` instance when computational evidence matters.

## Key Takeaways
1. Extensional principles prove equalities that computation alone does not establish.
2. Quotient operations are valid only when representative independence is proved.
3. Choice can turn pure existence into data logically, while losing general computability.
4. `Nonempty` and `Inhabited` differ constructively; choice can bridge them only noncomputably.
5. Choice plus extensional principles supports excluded middle and classical decidability.
6. Kernel normalization and compiled evaluation have different operational behavior in the presence of axioms/proof erasure.
7. Final answers should state when a construction is logically valid yet not an executable algorithm.

## Connects To
- **Ch 3**: classical reasoning, `Prop`, proof irrelevance, and contradiction.
- **Ch 4**: equality and substitution are the base language for extensional equality.
- **Ch 7**: quotients and equality interact with inductive elimination restrictions.
- **Ch 10**: `Decidable`, `Nonempty`, `Inhabited`, and classical proposition decidability interact with type-class inference.
