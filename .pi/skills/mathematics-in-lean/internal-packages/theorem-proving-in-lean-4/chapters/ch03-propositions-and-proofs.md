# Chapter 3: Propositions and Proofs

## Core Idea
Under Curry–Howard, propositions are types and proofs are terms. Logical reasoning becomes construction and elimination of typed objects, while `Prop` supplies proof irrelevance and a disciplined boundary between logical evidence and computational data.

## Frameworks Introduced
- **Curry–Howard proof construction**
  - When to use: every propositional theorem.
  - How: read the goal's outer connective as a type constructor, then build the corresponding term.
- **Introduction/elimination pairing**
  - When to use: choosing the next proof step.
  - How: use constructors/introduction rules to build a proposition; use projection, application, cases, or eliminators to consume a proof.
- **Auxiliary subgoal factoring**
  - When to use: a long proof has a reusable intermediate fact.
  - How: use `have` to prove and name it; use `suffices` when it is clearer to state the remaining sufficient condition first.
- **Constructive-to-classical escalation**
  - When to use: a goal requires excluded middle, double-negation elimination, or proof by contradiction.
  - How: keep the proof constructive if possible; otherwise open/use `Classical` locally and make the logical dependency visible.

## Key Concepts
- **`Prop`**: universe of propositions.
- **Proof irrelevance**: proofs of the same proposition carry no computational distinction.
- **Implication** `p → q`: function from a proof of `p` to a proof of `q`.
- **Conjunction** `p ∧ q`: proposition with constructor carrying proofs of both sides.
- **Disjunction** `p ∨ q`: proposition with two constructors identifying which side is proved.
- **Negation** `¬p`: abbreviation for `p → False`.
- **`False`**: proposition with no constructors; from a proof of `False`, any proposition follows via elimination.
- **`True`**: trivially inhabited proposition.
- **`Iff`** `p ↔ q`: pair of implications.
- **Classical excluded middle**: `p ∨ ¬p` for every proposition.

## Mental Models
- Read `p → q` as **a program converting evidence** for `p` into evidence for `q`.
- Read `p ∧ q` as **both pieces are available**, `p ∨ q` as **one tagged alternative is available**, and `∃` later as **a witness plus evidence**.
- Use `False` as an **impossible-state eliminator**: once contradiction is derived, the branch can close at any proposition.
- Treat classical reasoning as a **local logical dependency**, especially when the theorem may later interact with computation.

## Anti-patterns
- **Declaring an `axiom` for a hard lemma**: this bypasses proof construction and changes the theorem's trusted assumptions.
- **Leaving `sorry` in final code**: it creates an unsound placeholder (`sorryAx`).
- **Applying classical logic reflexively**: it can hide where constructive information is available and matters.
- **Proving a large implication monolithically** when intermediate `have` facts would expose the logical structure.

## Code Examples
```lean
example (p q : Prop) : p → q → p ∧ q := by
  intro hp hq
  exact ⟨hp, hq⟩
```
- **What it demonstrates**: function introduction for implications and constructor introduction for conjunction.

```lean
example (p q : Prop) : p ∧ q → q ∧ p := by
  intro h
  exact ⟨h.right, h.left⟩
```
- **What it demonstrates**: consume conjunction evidence through projections and build a new proof.

```lean
example (p : Prop) : ¬¬p → p := by
  classical
  intro hnnp
  by_cases hp : p
  · exact hp
  · exact False.elim (hnnp hp)
```
- **What it demonstrates**: explicit classical escalation and contradiction.

## Reference Tables
| Goal shape | Construct it | Consume matching hypothesis |
|---|---|---|
| `p → q` | lambda / `intro hp` | apply it to proof of `p` |
| `p ∧ q` | `⟨hp, hq⟩` / `constructor` | `.left`, `.right`, or `cases` |
| `p ∨ q` | `Or.inl hp` / `Or.inr hq` | `cases` into two branches |
| `¬p` | assume `p`, derive `False` | apply it to proof of `p` |
| `p ↔ q` | two implications | use `.mp`/`.mpr` or projections |
| `False` | no constructor | `False.elim` closes any proposition |

## Worked Example
To prove `(p ∧ (p → q)) → q`:
1. The outer goal is an implication, so introduce `h : p ∧ (p → q)`.
2. The conjunction gives `h.left : p` and `h.right : p → q`.
3. Apply the implication proof to the proof of `p`: `h.right h.left`.
4. `exact` that term, because it has type `q`.

The same proof can be expressed as a one-line term, but the staged version demonstrates a reusable diagnostic rule: peel the outer connective, inspect what evidence each hypothesis contains, then compose proof terms.

## Key Takeaways
1. Logical connectives define concrete proof-construction interfaces.
2. Introduction builds evidence; elimination consumes it.
3. `have` and `suffices` make intermediate logical dependencies explicit.
4. Negation is a function into `False`, so contradiction is ordinary function application plus elimination.
5. Classical reasoning should be introduced intentionally and locally.
6. Final soundness depends on eliminating unsound placeholders and unnecessary axioms.

## Connects To
- **Ch 2**: supplies function types and `Prop`'s place in the universe hierarchy.
- **Ch 4**: extends the proof-as-term view to quantifiers and equality.
- **Ch 5**: tactics automate the same constructor/eliminator steps.
- **Ch 12**: explains where classical principles and extensional axioms come from and what they mean computationally.
