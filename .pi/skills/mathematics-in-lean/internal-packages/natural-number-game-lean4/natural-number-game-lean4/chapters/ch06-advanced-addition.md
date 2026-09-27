# Chapter 6: Advanced Addition — Cancellation and Zero Decomposition

## Core Idea

Advanced Addition turns the commutative-monoid laws into implications that remove structure: cancel a common addend, infer that a term added without changing a value must be zero, and decompose a sum equal to zero. These lemmas become the algebraic engine for the later definition of `≤`.

## Frameworks Introduced

- **Right cancellation**
  - `a + n = b + n → a = b`.
  - Typical derivation: induction on the common right addend. The successor step reduces equality of successors via `succ_inj` and invokes the IH.

- **Left cancellation by transport**
  - Commute both sums so the shared left addend moves to the right, then reuse right cancellation. This is the preferred mirror-lemma strategy once `add_comm` exists.

- **Self-equality to zero**
  - Equations such as `x + y = y` or `x + y = x` are routed through cancellation after expressing the unchanged side with `+ 0`.

- **Zero-sum constructor split**
  - To prove a summand is zero from `a + b = 0`, split the relevant natural into `0` or `succ`. The successor branch rewrites the sum to a successor and contradicts zero/successor separation.

## Key Concepts

- `add_right_cancel`: remove a shared right addend.
- `add_left_cancel`: mirrored cancellation using commutativity.
- `add_left_eq_self`: from `x + y = y`, infer `x = 0`.
- `add_right_eq_self`: from `x + y = x`, infer `y = 0`.
- `add_right_eq_zero`: from `a + b = 0`, infer `a = 0`.
- `add_left_eq_zero`: from `a + b = 0`, infer `b = 0`.
- `cases`: decompose a natural into zero and successor when no induction hypothesis is needed.

## Procedure: cancellation

1. Identify the common addend and whether it is on the left or right.
2. If the theorem for that side exists, `apply` it to the equality.
3. If only the opposite-side theorem exists, commute both sums into the supported orientation.
4. When proving cancellation itself, induct on the common recursive addend; normalize the step to equality of successors and use `succ_inj`.
5. Check that the post-cancellation goal contains exactly the unmatched terms.

## Procedure: derive zero from “adding changes nothing”

For a pattern like `x + y = y`:

1. rewrite the right side as `0 + y` (using `zero_add` backward if useful);
2. apply right cancellation to remove `y`;
3. conclude `x = 0`.

For `x + y = x`, either use the mirrored theorem or commute first.

## Procedure: sum equals zero

1. Decide which summand you need to prove zero.
2. `cases` that summand.
3. Zero case closes by `rfl`.
4. Successor case rewrites the sum into a successor-shaped expression.
5. Turn the supplied equality into a forbidden `succ ... = 0` or `0 = succ ...` and close through the Peano contradiction.

No IH is required: the constructor shape alone is decisive, so `cases` is more precise than `induction`.

## Failure modes

- **Cancellation theorem does not match**: association or commutativity hides the common addend. Normalize the sum before applying the theorem.
- **Using induction where cases suffices**: extra IH noise obscures a pure constructor contradiction.
- **Assuming `a+b=0` permits arbitrary subtraction**: subtraction is not part of the foundational API; reason with constructors/cancellation.
- **Skipping orientation checks**: `add_left_eq_zero` and `add_right_eq_zero` name which summand they conclude, so select intentionally.

## Key Takeaways

1. Cancellation converts an equality about compounds into an equality about components.
2. Commutativity lets one cancellation theorem supply its mirror.
3. Equations of the form “adding something changes nothing” encode zero facts.
4. A sum equal to zero is best analyzed by constructor cases plus zero/successor separation.
5. These results are prerequisite infrastructure for order as an additive-gap relation.

## Connects To

- **Ch 7**: antisymmetry and small-bound order facts depend on additive cancellation/zero lemmas.
- **Ch 8**: multiplication develops analogous-looking results, with the crucial extra complication of zero factors.
- **Ch 5** supplies the implication and contradiction tactics used here.

## Source anchors

`Game/Levels/AdvAddition/L01add_right_cancel.lean` through `L06add_left_eq_zero.lean`; Addition World; Peano axioms; custom `cases` implementation in `Game/Tactic/Cases.lean`.
