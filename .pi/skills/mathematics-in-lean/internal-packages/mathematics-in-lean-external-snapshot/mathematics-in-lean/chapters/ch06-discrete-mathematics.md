# Chapter 6: Discrete Mathematics

## Core Idea
Choose the finite representation that matches the task: `Finset` for explicit finite collections, `Fintype` for finite carrier types, and inductive types for recursively generated data. Counting proofs then reduce to cardinality-preserving maps, disjoint decompositions, sums, and pigeonhole principles.

## Frameworks Introduced

- **Finset / Fintype router**
  - `Finset α`: use when elements are explicitly selected and operations such as insert, erase, filter, image, powerset, product, sum, or product matter.
  - `Fintype α`: use when the whole type is finite and the relevant set is `univ`.
  - Subtype bridge: a finset/set condition can define a finite subtype; a finite type can be enumerated with `Finset.univ`.
  - Watch `DecidableEq α`: many computational finset operations need it, while abstract membership theorems may avoid it.

- **Cardinality by decomposition**
  - When to use: counting a finite region or combinatorial class.
  - How: partition into disjoint pieces, prove a bijection/image preserves cardinality, combine with `card_union_of_disjoint`, product-cardinality, sum-cardinality, or a sigma-type equivalence.

- **Double counting / fiber counting**
  - When to use: a set of incidences can be counted by either endpoint or a function has more domain elements than codomain capacity.
  - How: express the same finite object as a sum of fiber cardinalities; use the pigeonhole/fiber theorem when average capacity implies a large fiber.

- **Structural recursion / induction**
  - When to use: lists, trees, propositional formulas, syntax, or any custom inductive type.
  - How: define one equation per constructor; prove properties with one case per constructor; invoke induction hypotheses exactly on recursive fields.

## Key Concepts

- **`range n`**: finset `{0, …, n-1}`.
- **`filter`**: retain elements satisfying a decidable predicate.
- **`image`**: finite direct image; cardinality preservation needs injectivity on the source.
- **Cartesian product `×ˢ`**: finset product with multiplicative cardinality.
- **`powerset`**: finset of all subsets of a finite set.
- **`#s` / `s.card`**: finite cardinality.
- **`Fintype.card`**: size of a finite type.
- **Sigma type**: dependent pair useful for “row plus element-in-row” counting.
- **Pigeonhole principle**: finite cardinality imbalance forces collisions or a large fiber.
- **Inductive type**: data generated from constructors; recursion/induction follows the constructor tree.

## Mental Models

- A counting proof is often a proof of equality between two finite representations of the same combinatorial object.
- Turn geometric diagrams into explicit finite predicates, then use symmetry/bijection/decomposition instead of element-by-element enumeration.
- For recursively defined data, the datatype declaration is the proof plan: every recursive field yields an induction hypothesis.
- Lean's finite abstractions separate computation (`Finset`) from global finiteness (`Fintype`); crossing layers intentionally prevents coercion noise.

## Anti-patterns

- **Using a set when cardinality computation is central**: convert to `Finset` or a finite subtype.
- **Assuming an image preserves cardinality without injectivity**: duplicates collapse; establish injectivity before using the corresponding finite-set cardinality theorem.
- **Forgetting decidable equality**: construction operations may fail to synthesize `DecidableEq`; use classical scope when computation is not the goal or provide an instance.
- **Doing combinatorial arithmetic before proving set equality/decomposition**: first identify the counted object, then reduce to numeric cardinalities.
- **Induction on an external natural when the theorem is about recursive syntax**: structural induction usually gives exactly the needed hypotheses.

## Code Examples

```lean
def triangle (n : ℕ) : Finset (ℕ × ℕ) :=
  {p ∈ Finset.range (n + 1) ×ˢ Finset.range (n + 1) | p.1 < p.2}
```

- **What it demonstrates**: encode a finite geometric/combinatorial region as a filtered product.

```lean
inductive BinTree where
  | empty : BinTree
  | node : BinTree → BinTree → BinTree

namespace BinTree

def size : BinTree → ℕ
  | .empty => 0
  | .node l r => size l + size r + 1

def depth : BinTree → ℕ
  | .empty => 0
  | .node l r => max (depth l) (depth r) + 1

end BinTree
```

- **What it demonstrates**: recursive definitions mirror constructor structure.

```lean
example {α β : Type*} [Fintype α] [Fintype β] :
    Fintype.card (α × β) = Fintype.card α * Fintype.card β := by
  simp
```

- **What it demonstrates**: use global finite-type cardinality theorems when the counted object is a whole type.

## Reference Table

| Need | Representation / theorem shape |
|---|---|
| explicit finite subset | `Finset` |
| all elements of finite type | `Fintype`, `univ` |
| choose min/max of finite set | finset + nonempty proof |
| count image | `card_image_of_injOn` / injectivity |
| count disjoint union | `card_union_of_disjoint` |
| count product | product cardinality |
| count dependent choices | sigma type / sum of fiber cards |
| force collision / large fiber | pigeonhole/fiber theorem |
| recursive data property | structural induction |

## Worked Example

For the triangular region `0 ≤ i < j ≤ n`, one route is to pair it with a reflected image and prove the two pieces form a rectangle. Define the reflection map explicitly, prove it is injective on the triangle, prove the two finsets are disjoint, prove their union is the rectangle, and only then compute cards. A second route packages each row as a fiber and uses a sigma-type cardinality. These are distinct method choices: symmetry is good when an involution visibly complements the region; sigma/fiber counting is good when the row structure is canonical.

For pigeonhole-style number theory, define a map such as `u ↦ u / 2` from a finset `A` with `n+1` elements into `n` possible bins. A fiber theorem produces two distinct elements in one fiber; arithmetic (`omega`) then converts “same quotient by 2” plus distinctness into consecutive integers, hence coprime elements.

## Key Takeaways

1. Representation choice (`Finset`, `Fintype`, subtype, inductive type) controls proof complexity.
2. Prove combinatorial bijections/decompositions before doing arithmetic on cardinalities.
3. Pigeonhole arguments are fiber-cardinality statements.
4. Structural induction follows the recursive fields of the datatype.
5. `omega` is especially useful after the combinatorial structure has reduced the problem to linear Nat/Int arithmetic.

## Connects To

- **Ch 5**: bounded predicates and prime enumerations become finsets.
- **Ch 8**: subobjects use a different bundled-set abstraction but share coercion/extensionality concerns.
- **Ch 10**: finite index types control matrices, bases, and finite dimension.
