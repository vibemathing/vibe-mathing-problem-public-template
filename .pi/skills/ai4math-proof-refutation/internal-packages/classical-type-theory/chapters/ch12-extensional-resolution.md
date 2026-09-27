# Chapter 12: Extensional Resolution

**Source coverage**: §3.3, printed pp. 994-996.

## Core Idea
Elementary higher-order calculi omit extensionality and descriptions. Extensional resolution integrates equality constraints, higher-order unification steps, and extensionality rules directly into a clause calculus so the prover does not have to encode all extensional reasoning as bulky background axioms.

## Frameworks Introduced
- **Constraint-as-negative-equality encoding**
  - When to use: to unify clause reasoning and unification reasoning in one calculus.
  - How: represent positive/negative literals explicitly and encode pending unification constraints as negative equality literals in the clause.
- **Unification inference rules**
  - When to use: to simplify equality constraints inside clauses.
  - How: lambda-reduce both sides, decompose rigid heads, remove trivial equalities, apply safe substitutions, and handle flex-rigid cases by projection or imitation.
- **Projection / imitation in flex-rigid problems**
  - When to use: when a variable-headed term must equal a rigid constant-headed term.
  - How: instantiate the flexible variable with a lambda term whose head either projects one input or imitates the rigid head, introducing fresh helper variables for substructure.
- **Extensionality rules**
  - When to use: when equality of propositions/functions is central.
  - How: add rules corresponding to propositional equivalence, Leibniz-style equality, and functional extensionality, with clause-specific Skolem terms where needed.

## Key Concepts
- **extensional resolution**: a resolution calculus augmented for higher-order unification and extensionality.
- **rigid term**: a term with a fixed constant head.
- **flexible term**: a term with a variable head.
- **flex-rigid pair**: a unification equation between flexible and rigid heads.
- **projection**: instantiate a flexible function by returning one of its arguments (possibly transformed).
- **imitation**: instantiate it by copying the rigid head and introducing fresh variables for arguments.
- **functional extensionality**: functions equal when their outputs agree on arguments.

## Mental Models
- Use one **clause-level worklist** for logic, equality, and unification rather than treating unification as an opaque subroutine.
- See projection/imitation as a **typed grammar of plausible function shapes**.
- Switch to extensional reasoning only when the proof requires observational/function equality; keep elementary search simpler when possible.

## Anti-patterns
- **Adding a giant conjunction of extensionality axioms to every goal**: logically possible, often operationally poor.
- **Treating equality constraints as separate from resolution forever**: the extensional calculus gains leverage by letting inference rules act on them.
- **Applying flex-rigid substitutions without occurs/dependency checks**: helper terms must remain well-typed and non-circular.

## Reference Tables

| Constraint shape | Typical action |
|---|---|
| two normalized lambda abstractions | compare instantiated bodies using a fresh/Skolem argument |
| same rigid constant head | decompose into argument equalities |
| `A = A` | delete as trivial |
| variable equals term | apply safe substitution if non-circular |
| flexible head vs rigid head | branch on projection / imitation candidates |
| function equality | reduce via functional extensionality to equality on an argument |

## Worked Example
For a flex-rigid constraint `F(U1,...,Un) = c(V1,...,Vm)`, direct first-order decomposition is impossible because `F` has no fixed head. Extensional higher-order unification instead gives `F` candidate lambda definitions. A projection candidate returns one of the inputs; an imitation candidate builds a result headed by `c` and delegates each rigid argument to fresh helper functions. The remaining equality constraints then determine whether the candidate can succeed.

## Key Takeaways
1. Recognize when extensionality is the missing proof principle.
2. Encode pending unification obligations so clause rules can process them.
3. Normalize and decompose rigid equalities aggressively.
4. Use projection/imitation for flex-rigid higher-order constraints.
5. Keep equality handling integrated with the proof calculus when equality dominates search.

## Connects To
- **Ch 1**: extensionality is one of the defining higher-order principles.
- **Ch 8**: projection/imitation are higher-order unification techniques.
- **Ch 11**: extensional resolution evolves the constrained-resolution idea.
