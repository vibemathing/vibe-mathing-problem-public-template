# Chapter 1: Introduction

## Core Idea
Lean supports formal reasoning by turning mathematical claims into precise types and proofs into checkable terms. The practical trust model is: use rich automation to construct a proof, then rely on a small kernel to check the resulting object.

## Frameworks Introduced
- **Formal verification loop**
  - When to use: whenever an informal claim must become a mechanically checked theorem.
  - How: state the claim precisely → construct a proof term, directly or through tactics → let Lean's kernel type-check it.
- **Programming + proving + metaprogramming**
  - When to use: when a task mixes executable definitions, theorem statements, and automation.
  - How: treat the same dependent type theory as the substrate for data, programs, propositions, and proofs.
- **Small trusted core with untrusted automation**
  - When to use: when assessing what must be trusted for a theorem.
  - How: distinguish proof-producing elaborators/tactics from the kernel that verifies their output.

## Key Concepts
- **Theorem prover**: software that represents claims and checks formal proofs.
- **Proof assistant**: interactive environment where users guide proof construction while automation fills routine details.
- **Kernel**: small checker responsible for validating fully elaborated terms.
- **Dependent type theory**: foundation in which types can depend on values and propositions can be represented as types.
- **Elaboration**: process that fills omitted information and turns convenient syntax into a fully typed term.
- **Automation**: procedures that search for or synthesize proof terms while preserving kernel checkability.

## Mental Models
- Use **proof object + checker** when deciding whether an automation feature enlarges the trusted base: automation may be complex while the final proof remains independently checkable.
- Think of Lean as a **single typed language** in which computation and proof live together. This makes definitions reusable in both programs and theorems.
- Use **precision before proof**: a proof problem begins by deciding exactly what the claim and its assumptions mean.

## Anti-patterns
- **Treating successful automation as the trust argument**: success matters only because the generated proof is checked.
- **Formalizing before clarifying the statement**: a perfect proof of the wrong formal statement gives the wrong guarantee.
- **Assuming every mathematical step should be written manually**: Lean is designed to combine explicit reasoning with automation.

## Code Examples
```lean
example (p : Prop) (hp : p) : p := by
  exact hp
```
- **What it demonstrates**: a theorem goal is a type and `hp` is already a term inhabiting that type.

```lean
def twice (f : α → α) (x : α) : α := f (f x)

#check twice
```
- **What it demonstrates**: ordinary functional programming and theorem proving share the same typed term language.

## Reference Tables
| Question | Practical interpretation |
|---|---|
| What must be trusted? | Kernel plus the implementation/runtime needed to execute the checker correctly. |
| What may be automated? | Elaboration, simplification, tactic search, and proof construction, provided their outputs are checked. |
| What is the book's progression? | Type theory → propositions/equality → tactics/interaction → inductives/recursion → structures/classes → conversion → axioms/computation. |

## Worked Example
Suppose a user says, “prove that applying the identity function changes nothing.” The operational sequence is:
1. Make the claim precise: for a type `α` and value `x : α`, `(fun y : α => y) x = x`.
2. Observe that reducing the function application gives exactly `x`.
3. Use definitional equality, so the proof can be `rfl`.
4. Let the kernel confirm that the term has the stated equality type.

The example matters because it separates mathematical intent, elaborated expression, computational reduction, and kernel checking.

## Key Takeaways
1. Formal reasoning starts with a precise type-level statement.
2. Proofs are objects that Lean checks, even when tactics construct them.
3. Automation can be aggressive without replacing the kernel as the final checker.
4. Lean deliberately unifies programs, specifications, and proofs.
5. Later method choices should preserve this trust model: inspect the actual goal and produce a term Lean can verify.

## Connects To
- **Ch 2**: supplies the dependent type theory underlying programs and proofs.
- **Ch 3**: identifies propositions with types and proofs with terms.
- **Ch 5**: explains tactics as proof-term construction.
- **Ch 12**: revisits the trusted logical primitives and their computational effects.
