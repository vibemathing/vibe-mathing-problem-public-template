# Chapter 2: Basics

## Core Idea
Most elementary Lean proofs become manageable after separating two tasks: expose the mathematical step with rewriting/theorem application, then use the tactic specialized to the remaining algebraic structure. The proof state, theorem types, and typeclass assumptions tell you which route is valid.

## Frameworks Introduced
- **Controlled rewriting**
  - When to use: a hypothesis or theorem gives an equality/iff whose substitution moves the target toward a known form.
  - How: `rw [h]`; reverse with `rw [← h]`; rewrite a hypothesis with `rw [...] at h`; target a specific occurrence with `nth_rw`.
  - Failure mode: `rw` is syntactic. If the pattern is hidden by a definition/lambda, normalize or `change` the expression first.
- **Structured calculation (`calc`)**
  - When to use: a proof naturally passes through chosen intermediate expressions.
  - How: state each intermediate equality/inequality and justify each step independently. This also avoids `apply le_trans` generating an unknown intermediate metavariable.
- **Apply/exact ladder**
  - When to use: a theorem's conclusion matches the current goal.
  - How: use `exact theorem args` when complete; use `apply theorem` when its premises should become subgoals; use `have` for a reusable local lemma.
- **Domain-specific automation**
  - When to use: the structural/mathematical choices have already been made.
  - How: `ring` for commutative polynomial identities, `noncomm_ring` for noncommutative rings, `group` for group identities, `abel` for additive commutative groups, `linarith` for linear arithmetic, `norm_num` for concrete numerals.
- **Library discovery loop**
  - When to use: the right fact is standard but its name is unknown.
  - How: inspect nearby APIs/documentation, rely on naming conventions, use completion, and try `apply?`. Names often encode result and premises (`A_of_B_of_C`).

## Key Concepts
- **Context / target**: assumptions and objects above the turnstile; proposition below it.
- **Implicit argument**: an argument Lean infers from later terms/context; written with braces in declarations.
- **Definitional equality**: reduction makes two expressions the same; `rfl` can prove it.
- **Namespace**: groups related names and controls ambiguity.
- **Partial order / lattice**: abstract structures whose theorems work for many concrete instances.
- **Typeclass assumption**: square-bracket structure such as `[Ring R]` or `[PartialOrder α]`.
- **Transitivity intermediate**: often must be supplied explicitly with `calc` or `trans`.

## Mental Models
- Use `rw` as **substitution with explicit provenance**.
- Use `apply` as **backward reasoning**: match the desired conclusion and ask Lean to expose sufficient premises.
- Think of automation as a **decision procedure for a restricted theory**, not general proof search.
- Read abstract theorems as **interfaces**: a theorem stated for `Ring R` automatically applies to concrete rings and stronger structures.

## Anti-patterns
- **Using `ring` in a noncommutative setting**: commutativity is an essential precondition; use `noncomm_ring` or explicit axioms.
- **Blind `apply le_trans`**: Lean may create an unconstrained intermediate; use `calc` or `trans y`.
- **Writing every implicit argument**: let hypotheses determine them; force explicit values only when inference is ambiguous.
- **Long rewrite chains with no structure**: convert a human calculation to `calc` once the sequence matters for readability.
- **Searching only concrete APIs**: a real-number goal may be solved by a theorem on ordered rings, lattices, groups, or monoids.

## Code Examples
```lean
example (a b c : R) : (a + b) * c = a * c + b * c := by
  rw [add_mul]
```
```lean
example (x y z : R) (hxy : x ≤ y) (hyz : y < z) : x < z := by
  exact lt_of_le_of_lt hxy hyz
```
```lean
example (a b : R) : (a + b) * (a - b) = a ^ 2 - b ^ 2 := by
  ring
```
- **What they demonstrate**: direct rewriting, theorem reuse, and specialization to a decidable algebraic theory.

## Reference Tables
| Goal residue | Preferred tactic | Precondition/check |
|---|---|---|
| commutative polynomial identity | `ring` | commutative semiring/ring structure |
| noncommutative ring identity | `noncomm_ring` | ring structure |
| group identity | `group` | group operations |
| additive commutative identity | `abel` | additive commutative group |
| linear equalities/inequalities | `linarith` | linear arithmetic facts in context |
| concrete arithmetic | `norm_num` | computable numeric normalization |
| exact theorem conclusion | `exact` | term matches target |
| theorem with missing premises | `apply` | conclusion matches target |

## Section-by-Section Operational Map

**2.1 Calculating.** Start with `rw` to see exactly how a named identity changes the target. Use theorem arguments only when pattern matching is ambiguous; otherwise let Lean infer them. Multiple rewrites can be listed in one command, but keep them separated while debugging. `calc` is the readability upgrade for calculations with meaningful intermediate expressions. Rewriting can happen in local hypotheses, and `exact` closes the goal when a transformed hypothesis matches it.

**2.2 Proving Identities in Algebraic Structures.** Re-run concrete calculations over `[Ring R]`, `[CommRing R]`, groups, and additive groups to learn which axioms were genuinely used. Use namespaces when temporarily reproving library lemmas. Implicit arguments encode information recoverable from later hypotheses. `have` gives modular subproofs. Distinguish propositional identities from definitional equalities: subtraction may reduce definitionally in one concrete type while only being theorem-equivalent in a generic ring.

**2.3 Using Theorems and Lemmas.** Treat theorem types as curried functions from premises to conclusions. Iff lemmas provide `.mp`/`.mpr` directions and also support rewriting. For inequalities, chain order lemmas explicitly until `linarith` can take over. Theorem search is part of proof design; use naming conventions and nearby declarations rather than inventing facts.

**2.4 More examples using apply and rw.** Equality of ordered objects often goes through antisymmetry; repeated symmetric branches can be factored into a local lemma or `repeat`. Divisibility, gcd/lcm, min/max all reward learning characterization lemmas. Prefer explicit intermediate objects when transitivity otherwise leaves metavariables.

**2.5 Proving Facts about Algebraic Structures.** Use the characterizing axioms of partial orders, lattices, distributive lattices, ordered rings, and metric spaces to prove generic facts. This is the chapter's main abstraction lesson: once a proof uses only interface laws, state it at that interface and let concrete instances inherit it.

## Failure Recovery Notes

- If a generic theorem fails on a concrete type, inspect whether the required class is actually available or whether the theorem needs a stronger property such as commutativity or totality.
- If `ring` fails, identify whether a non-ring operation, local nonlinear hypothesis, or noncommutative multiplication remains; rewrite it away or choose a different tactic.
- If `linarith` cannot see a nonlinear fact such as square nonnegativity, prove that fact separately and pass it in.
- If a proof becomes opaque after aggressive rewriting, restore structure with `calc`, `show`, and named `have` statements.

## Worked Example
Suppose the goal is an inequality whose decisive idea is that a square is nonnegative. First prove a helper fact `h : 0 ≤ (a - b)^2` using a library nonnegativity theorem. Rewrite or `ring`-normalize the square if necessary. Once `h` is in the context, the desired inequality can often be solved by `linarith`. This division of labor is characteristic: the user supplies the nonlinear mathematical insight; `linarith` closes the linear consequences.

## Key Takeaways
1. Rewriting and theorem application are the basic moves; automation is the finisher.
2. Inspect theorem types with `#check` before fighting elaboration.
3. Use `calc` when the intermediate expression is mathematical information Lean cannot infer.
4. Prefer the weakest abstraction that supports the argument.
5. If the theorem is standard, invest in finding the library statement before reproving it.
6. Proof style should balance brevity, readability, and stability under library evolution.

## Connects To
- **Ch 3**: gives the logic behind theorem premises and hidden quantifiers.
- **Ch 5–6**: adds induction and arithmetic tactics for natural-number/discrete goals.
- **Ch 7–9**: explains why generic algebraic theorems and notation resolve automatically.
