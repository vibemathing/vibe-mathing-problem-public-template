# Operational Patterns

## 1. Recursive-Argument Induction
**When to use:** Universal identities over `+`, `*`, or `^` where one argument is a MyNat variable.

**How:**
1. Find the primitive successor equation (`add_succ`, `mul_succ`, `pow_succ`).
2. Induct on the argument occupying that recursive position.
3. Base: rewrite the zero equation.
4. Step: rewrite the successor equation on both sides until the IH appears.
5. Apply IH; normalize lower-layer algebra; finish with `rfl`.

**Trade-offs:** Direct and curriculum-aligned. A poor induction variable can make the IH unusable.

## 2. Mirror a Theorem by Commutativity
**When to use:** A left/right analogue is needed and commutativity already exists.

**How:** Commute the target operation, apply the existing one-sided law, commute result components if needed.

**Trade-offs:** Short and dependency-efficient; invalid if commutativity itself depends on the theorem being proved.

## 3. Rewrite → Apply → Exact
**When to use:** A logical theorem almost matches the goal/hypothesis.

**How:** Normalize the relevant proposition with `rw`; `apply` the implication in the useful direction; `exact` the aligned proof.

**Trade-offs:** Makes proof-state movement explicit. Requires careful orientation.

## 4. Prove Negation by Constructor Contradiction
**When to use:** Goal `a ≠ b` where numeral/arithmetic normalization can reveal different Peano constructors.

**How:** `intro h`; normalize; repeatedly use `succ_inj`; reduce to `0 = succ n`; apply `zero_ne_succ` (symmetrize if required).

**Trade-offs:** Very transparent; tedious for large closed numerals, where `decide` later becomes preferable.

## 5. `≤` as Witness Engineering
**When to use:** Any NNG `≤` theorem.

**How:** Goal → choose gap `c` with `use`. Hypothesis → `cases` to obtain gap and endpoint equality. Compose gaps with addition for transitivity; use cancellation for antisymmetry.

**Trade-offs:** Constructive and local. Do not assume subtraction exists to compute the gap.

## 6. Cases Instead of Induction
**When to use:** The result depends on zero vs successor shape and no recursive hypothesis is needed.

**How:** `cases n`; solve zero case; in successor case expose a forbidden constructor equality or direct witness.

**Trade-offs:** Cleaner than induction for structural dichotomies; insufficient for recursive statements.

## 7. Nonzero → Successor → Multiplicative Structure
**When to use:** Multiplication theorem has `a ≠ 0` or needs a positive-like fact.

**How:** Case-split `a`; contradiction in zero branch; return `a = succ n` in successor branch. From this derive `1 ≤ a`, nonzero product behavior, or a cancellable shape.

**Trade-offs:** Avoids subtraction/positivity primitives. Requires carrying explicit nonzero assumptions.

## 8. Safe Multiplication Cancellation
**When to use:** `a*b = a*c` or `a*b = a`.

**How:** prove/locate `ha : a ≠ 0`; orient both products; apply `mul_left_cancel`. For `a*b=a`, rewrite `a` as `a*1` first.

**Trade-offs:** Mathematically correct only with the guard. If the guard cannot be established, report insufficient assumptions.

## 9. Generalize Before Induction
**When to use:** The step changes a variable that the naive IH fixes.

**How:** use `induction b ... generalizing c`; let each branch choose the needed `c`; apply the stronger IH after constructor rewrites.

**Trade-offs:** Stronger and reusable IH; over-generalizing can increase proof-state complexity.

## 10. AC Normalization
**When to use:** Addition expressions differ only by association/permutation.

**How:** Early worlds: explicit `rw` with assoc/comm. Algorithm World: `simp only` on the approved AC lemmas or `simp_add`.

**Trade-offs:** Automation is concise but can hide lesson structure. Keep the lemma set controlled.

## 11. Closed-Proposition Decision
**When to use:** Closed MyNat equality/inequality after `DecidableEq` is available.

**How:** use the game's custom `decide`; it first performs MyNat-specific simplification then runs the decision procedure.

**Trade-offs:** Excellent for concrete facts; does not replace symbolic induction for variables.

## 12. FLT Boundary Handling
**When to use:** Power World final boss / `xyzzy`.

**How:** identify the source's hidden axiom-backed tactic. For game questions, explain its role. For a genuine FLT proof request, route outside this curriculum.

**Trade-offs:** Preserves source fidelity and avoids a false mathematical claim.
