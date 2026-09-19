# Chapter 6: Discrete Mathematics

## Core Idea
Finite mathematics in Lean has two complementary interfaces: `Finset α` for explicit finite collections and `Fintype α` for finite types. Counting proofs reduce to cardinality-preserving constructions, finite sums/products, and induction; inductively defined data types provide the same recursion/induction architecture beyond natural numbers.

## Frameworks Introduced
- **Finset vs Fintype selection**
  - When to use: deciding how to represent a finite problem.
  - How: use `Finset` when a particular finite subset matters; use `Fintype` when the entire type is finite. Coerce a finset to a subtype when type-level cardinality/equivalence is more convenient.
- **Finite-set extensionality and simplification**
  - When to use: equality/inclusion of finsets.
  - How: `ext x`; reduce membership with `simp`; use `tauto` for the resulting propositional identity. Remember many finset membership laws are theorem-driven rather than definitional.
- **Finset induction**
  - When to use: prove a property of arbitrary finite sets or products/sums defined over them.
  - How: prove the empty case; in the insert step assume the new element is absent, rewrite the operation with `*_insert`, and apply the induction hypothesis.
- **Counting by decomposition / equivalence**
  - When to use: cardinality of a structured finite collection.
  - How: decompose into disjoint unions/fibers and sum cardinalities, or build an explicit equivalence between a subtype and a sigma/product type, then use `Fintype.card_congr`.
- **Double counting**
  - When to use: bipartite incidence/edge-count problems.
  - How: express the same finite sum in two orders (`sum_comm`); bound rows and columns separately; chain inequalities in `calc`.
- **Structural recursion and induction**
  - When to use: lists, trees, formulas, or custom inductive types.
  - How: define functions by constructor cases; prove equations recursively using the same cases. Use the generated induction principle or equation-style theorem definition.

## Key Concepts
- **`DecidableEq α`**: computational ability to test equality, required by many `Finset` operations.
- **Classical fallback**: reasoning can use classical decidable equality when computation is irrelevant.
- **`Finset.filter` / `image` / `product` / `powerset` / `fold`**: central finite constructions.
- **`card`**: number of elements of a finset/fintype.
- **Disjointness**: allows cardinality of union to become addition.
- **Equivalence (`≃`)**: often the cleanest proof that two finite types have the same cardinality.
- **Inductive datatype**: every value is built from declared constructors.
- **Structural induction**: one proof case per constructor, with hypotheses for recursive fields.

## Mental Models
- Treat cardinality arguments as **construction problems**: find a disjoint decomposition, fiber map, injection, surjection, or equivalence.
- Think of a finset fold/sum/product as **order-independent recursion** enabled by commutativity/associativity.
- A subtype of a finset is a bridge from **set-style membership** to **type-style equivalence/cardinality**.
- For inductive objects, use **constructor shape as the control flow** for both computation and proof.

## Anti-patterns
- **Using `Finset` without decidable equality** while expecting computation: add the instance or enter a classical/noncomputable section when only reasoning is needed.
- **Expanding cardinalities element-by-element** when an equivalence or standard `card_*` lemma exists.
- **Ignoring disjointness side conditions** in union/biUnion counts.
- **Defining a fold with a noncommutative/nonassociative operation**: the result would depend on element order.
- **Writing recursive proofs unrelated to constructors**: follow the datatype's induction principle.

## Code Examples
```lean
open Finset

example (s : Finset Nat) : s.card = ∑ _x ∈ s, 1 := by
  simp
```
```lean
inductive BinTree where
  | empty : BinTree
  | node : BinTree → BinTree → BinTree
```
- **What they demonstrate**: cardinality as a finite sum and an inductive datatype whose recursion/induction is structural.

## Reference Tables
| Need | Preferred representation |
|---|---|
| explicit finite subset | `Finset α` |
| all elements of finite type | `[Fintype α]` / `Finset.univ` |
| filtered finite subset | `s.filter P` |
| finite image | `s.image f` |
| counting pairs | `s ×ˢ t`, product cardinality |
| finite partition/fibers | `biUnion` / sums of cards |
| prove all finsets satisfy `P` | `Finset.induction_on` |
| convert finset to finite type | subtype `↥s` |

## Section-by-Section Operational Map

**6.1 Finsets and Fintypes.** Finsets are computational and often require `[DecidableEq α]`; classical reasoning can synthesize it when computation is irrelevant. Finset literal notation is repeated `insert`; `filter`, `image`, cartesian product, powerset, fold, sums/products, and bounded unions cover most constructions. `Finset.Nonempty` plus choice gives an element; min/max APIs distinguish empty-safe and nonempty versions. Coercing `s : Finset α` to a type produces the subtype of elements of `s`, whose `Fintype.card` is `s.card`.

**6.2 Counting Arguments.** Standard card lemmas cover products, unions, and injective images. More complex counts often decompose into disjoint fibers/rows and use sums of cards. An alternate route is to build a type equivalence and apply `Fintype.card_congr`; this is often cleaner when the combinatorial bijection is conceptually central. `omega` is effective at the arithmetic boundary once the finite combinatorics is represented correctly. Double counting is naturally a chain of finite-sum equalities/inequalities, and the pigeonhole principle appears as a library theorem about fibers.

**6.3 Inductively defined types.** Lists, binary trees, and propositional formulas demonstrate recursion beyond naturals. Define recursive functions by constructor equations; theorem proofs can use matching equation syntax or induction tactics. The substitution/evaluation examples on formulas show that structural induction scales to semantically interesting transformations. Efficiency matters for executable definitions: a mathematically straightforward recursive function may be quadratic/exponential, while an accumulator/tail-recursive implementation can be proved extensionally equal to it.

## Failure Recovery Notes

- If Finset equality produces messy element-order issues, switch to `ext x; simp` rather than reasoning about underlying lists.
- If `card_union` leaves an unwanted subtraction, seek the disjoint-union lemma and prove disjointness directly.
- If a `biUnion` cardinality theorem requests pairwise disjointness, isolate that obligation before the main arithmetic chain.
- If structural induction explodes, define helper lemmas that match the recursive auxiliary function rather than trying to prove the final theorem in one induction.

## Worked Example
A triangle of lattice points can be counted by rows. Define a finset of pairs `(i,j)` in a square range with `i < j`. Prove by extensionality that it equals a disjoint union indexed by `j`, where row `j` is the image of `range j` under `i ↦ (i,j)`. Use `card_biUnion`, discharge disjointness, show each row image has cardinality `j` by injectivity, then reduce the result to the familiar sum `0 + ... + n`. This separates geometric insight (row decomposition) from library mechanics (image/card/disjoint union/sum).

## Key Takeaways
1. Choose Finset for a finite subset and Fintype for a finite universe.
2. Convert counting to standard cardinality identities or equivalences.
3. Use `omega` aggressively for routine finite index arithmetic after the combinatorial structure is correct.
4. Finset induction is the default for proofs about arbitrary finite collections.
5. Structural recursion and structural induction are the same design pattern applied to new datatypes.
6. Keep computational concerns (`DecidableEq`, efficient recursion) separate from purely logical proofs when possible.

## Connects To
- **Ch 5**: finite products, prime arguments, and induction on naturals.
- **Ch 7**: structures package data/proofs; inductive types package constructors/recursors.
- **Ch 10**: finite index types power matrices, bases, and dimension calculations.
