# Proof Routing Workflow

Use this when the goal is unfamiliar or several tactics seem plausible.

## 1. Freeze the proof contract

Record:
- exact theorem/goal;
- hypotheses;
- game world/level or imports;
- whether later theorems/automation are allowed;
- whether output must run in NNG4 or ordinary Lean.

Do not propose a tactic until these constraints are known or inferable.

## 2. Classify the outer connective

- Equality → Section 3.
- Implication → `intro` if proving it; otherwise use/apply an implication.
- Negation → introduce equality and aim for `False`.
- Existential / `≤` → witness construction or elimination.
- Disjunction → branch construction or case elimination.

## 3. Equality routing

A. **Reflexive now?** → `rfl`.

B. **One equality rewrite away?** → `rw`, choosing direction and occurrence deliberately.

C. **Recursive universal law?** → find the primitive recursion equation and induct on its argument.

D. **Mirror of known theorem?** → commute, reuse, commute back.

E. **Only association/order differs?** → AC rewrites; `simp_add` only when unlocked.

F. **Closed concrete proposition?** → custom `decide` only after DecidableEq is available.

## 4. Recursion diagnostic

For `a+b`: recursion argument = `b`.
For `a*b`: recursion argument = `b`.
For `a^n`: recursion argument = `n`.

If induction on another variable is chosen, state why: e.g. proving a mirror lemma whose left position must be exposed, or because a stronger theorem makes that induction convenient.

## 5. Side-condition gate

Before multiplication cancellation, product-self conclusions, or positivity-like claims, check zero explicitly.

- Have `a ≠ 0` → proceed.
- Can derive it from `a*b ≠ 0` → derive first.
- Cannot exclude `a=0` → do not cancel; split cases or report insufficient assumptions.

## 6. Choose proof granularity

- Level-valid solution: use only unlocked tools, show the intended conceptual step.
- Explanation: name the method and failure condition before giving code.
- Unrestricted Lean translation: map the NNG method to standard `Nat`/Mathlib, warning about renamed/custom tactics.

## 7. Validate before returning

Check every rewrite theorem direction, every induction dependency, every existential witness, every zero case, and the current theorem inventory. For FLT, disclose `xyzzy` if it is relevant.
