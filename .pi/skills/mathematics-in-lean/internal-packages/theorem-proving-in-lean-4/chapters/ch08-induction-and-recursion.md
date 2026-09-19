# Chapter 8: Induction and Recursion

## Core Idea
Lean accepts recursive definitions only with a termination argument and compiles high-level pattern matching to primitive eliminators. Proofs work best when they follow the same recursive control flow: structural induction first, functional induction when function equations are the true shape, and well-founded induction when structural descent is not visible.

## Frameworks Introduced
- **Equation-compiler view**
  - When to use: reading pattern-matching definitions or generated theorem behavior.
  - How: remember that convenient equations compile to recursors and equation lemmas checked by the kernel.
- **Structural recursion first**
  - When to use: recursive calls operate on constructor subterms.
  - How: pattern match on the recursive input and call recursively only on structurally smaller pieces.
- **Well-founded fallback**
  - When to use: recursive calls decrease mathematically but the smaller argument is not syntactically a constructor subterm.
  - How: pick a well-founded relation/measure with `termination_by`; solve each descent obligation with `decreasing_by`.
- **Functional induction**
  - When to use: a theorem tracks the branching and recursive calls of a function more directly than its input datatype.
  - How: use `fun_induction` for recursive proof hypotheses or `fun_cases` for branch-aligned case analysis.
- **Dependent pattern matching**
  - When to use: matching an indexed family where the constructor determines result indices.
  - How: let the pattern match refine indices, eliminate unreachable cases, and use inaccessible patterns for values forced by those indices.

## Key Concepts
- **Pattern matching**: defining/eliminating by constructor patterns.
- **Wildcard** `_`: ignore a field/pattern component.
- **Overlapping patterns**: ordered clauses where earlier matches can take precedence.
- **Exhaustiveness**: every possible constructor/input shape must be covered unless a default/other construction handles it.
- **Structural recursion**: termination from constructor subterms.
- **Course-of-values recursion**: recursion with access to results for structurally smaller values, supported through generated mechanisms such as `below`/`brecOn`.
- **Local recursion**: recursive definitions nested in a larger definition via `let rec` or `where`.
- **`Acc` / `WellFounded`**: logical infrastructure for general terminating recursion.
- **`termination_by`**: declaration of measure/relation used for termination.
- **`decreasing_by`**: proof script for recursive-call descent obligations.
- **`fun_induction` / `fun_cases`**: function-equation-aligned reasoning.
- **Mutual recursion**: several functions defined together with recursive calls across the group; termination must account for the whole recursive dependency.
- **Inaccessible pattern** `.(t)`: expression forced by indices, recorded rather than independently matched.

## Mental Models
- View termination checking as **proof that recursion follows a finite descent**. Structural recursion provides that proof implicitly; well-founded recursion makes it explicit.
- Use function equations as a **control-flow specification**. If the theorem mentions the function, following those equations can yield exactly the branch assumptions and IHs you need.
- Treat dependent pattern matching as **simultaneous data and type refinement**: a constructor match can rewrite indices in the goal.
- Distinguish **definitional equations** from generated propositional equation theorems; simplification can use both even when kernel reduction does not treat them identically.

## Anti-patterns
- **Using `decreasing_by` to fight a false measure**: if a recursive call does not decrease, strengthen/change the measure or redesign the definition.
- **Hiding a termination hole with an unfinished proof**: it compromises the definition's trusted totality argument.
- **Datatype induction on the wrong shape for a function theorem**: can produce irrelevant IHs and lose branch conditions.
- **Matching freely on an index-forced value**: use an inaccessible pattern when the index already determines it.
- **Assuming overlapping pattern order is irrelevant**: ordered equations may encode behavior.

## Code Examples
```lean
def sum : List Nat → Nat
  | [] => 0
  | x :: xs => x + sum xs
```
- **What it demonstrates**: transparent structural recursion on a constructor subterm.

```lean
def countdown : Nat → List Nat
  | 0 => []
  | n + 1 => (n + 1) :: countdown n
```
- **What it demonstrates**: recursive call has a visibly smaller natural argument.

```lean
def ack : Nat → Nat → Nat
  | 0, y => y + 1
  | x + 1, 0 => ack x 1
  | x + 1, y + 1 => ack x (ack (x + 1) y)
termination_by x y => (x, y)
```
- **What it demonstrates**: a lexicographic measure can justify recursion whose nested calls are not simple constructor-subterm recursion.

```lean
theorem ack_pos (n m : Nat) : ack n m > 0 := by
  fun_induction ack <;> simp_all [ack]
```
- **What it demonstrates**: functional induction produces branches and induction hypotheses aligned with the recursive equations.

## Reference Tables
### Recursion decision tree
| Question | Route |
|---|---|
| recursive call consumes direct constructor subterm? | structural recursion |
| can refactoring expose structural descent? | refactor first |
| a natural-number measure decreases? | `termination_by` that measure |
| several dimensions decrease | lexicographic/product well-founded relation |
| theorem follows recursive calls | `fun_induction` |
| functions recurse into each other | mutual recursion; inspect the shared termination argument and generated induction principles |
| theorem only needs branch facts | `fun_cases` |
| indices determine possible constructors | dependent pattern matching |

### Termination diagnosis
1. Identify every recursive call.
2. For each call, write the proposed “smaller than” fact explicitly.
3. If any fact is false, the measure is wrong.
4. If true but Lean cannot prove it, inspect simplification/arithmetic facts needed by `decreasing_by`.
5. If the relation is complicated, search for an existing well-founded instance/relation before building one from scratch.

## Worked Example
Consider Euclidean-style recursion where the next argument is a remainder. The recursive argument may not be a direct constructor subterm, even though mathematics guarantees it is smaller.

Operational workflow:
1. Try the direct definition and read the termination failure.
2. Choose a natural-number measure that tracks the argument known to decrease.
3. State it with `termination_by`.
4. For the recursive branch, prove the remainder is less than the divisor/current measure in `decreasing_by`.
5. If the theorem later proves an invariant about this function, use functional induction so the recursive case includes the same “remainder branch” condition and IH.

This avoids inventing an unrelated datatype induction whose cases do not match the algorithm.

## Failure Recovery
- Structural checker fails → expose a smaller subterm, refactor helper function, then escalate to well-founded recursion.
- `decreasing_by` cannot close a branch → inspect the exact generated inequality; change measure if it is genuinely nondecreasing.
- ordinary induction yields unusable IH → use `fun_induction`, or revert/generalize values before datatype induction.
- dependent match reports motive errors → write a more explicit result type/motive so index refinement is visible.
- equation does not reduce with `rfl` → use generated equation theorem or simplification; not every compiled equation is definitionally transparent in the same way.

## Key Takeaways
1. Total recursive definitions require a structural or well-founded descent argument.
2. `termination_by` selects what decreases; `decreasing_by` proves that recursive calls obey it.
3. Functional induction is often the best theorem method for recursive algorithms.
4. Dependent pattern matching can remove impossible cases by refining indices.
5. Inaccessible patterns mark values determined by type indices rather than freely inspected.
6. High-level equations remain kernel-checked after compilation to primitive recursion machinery.

## Connects To
- **Ch 7**: constructors, recursors, inductive families, and ordinary induction supply the foundation.
- **Ch 5**: `revert`, `generalize`, and simplification repair induction shape and recursive equations.
- **Ch 10**: well-founded relations and other infrastructure may be supplied through instances.
- **Ch 12**: unfinished termination proofs affect soundness; computation behavior depends on how definitions reduce.
