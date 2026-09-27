# Failure Recovery Matrix

## Rewrite failure

**Signal:** `rw` says it cannot find the pattern, or rewrites the wrong subterm.

**Diagnose in order:**
1. theorem direction;
2. implicit/explicit arguments;
3. parentheses/association;
4. multiple identical occurrences;
5. whether the needed theorem is actually unlocked.

**Recover:** reverse with `←`; instantiate arguments; reassociate; use `nth_rewrite`; switch to a mirror theorem.

## Reflexivity failure

**Signal:** a mathematically trivial arithmetic equality survives `rfl`.

**Cause:** game operations are opaque/custom `rfl` uses restricted reducibility.

**Recover:** apply the explicit primitive/derived equation (`add_zero`, `mul_succ`, etc.), then `rfl`.

## Induction failure

**Signal A:** recursive equation does not fire in the step.

**Recover:** check that induction is on the operation's recursive argument; commute or rewrite the expression to expose it.

**Signal B:** IH is close but fixed at the wrong value of another variable.

**Recover:** restart with `generalizing` on that variable or strengthen the statement.

**Signal C:** both cases are just constructor contradictions.

**Recover:** use `cases` instead of induction.

## Apply/exact failure

**Signal:** theorem is conceptually right but type does not match.

**Recover:** normalize goal/hypothesis first; choose forward `apply ... at h` versus backward `apply theorem`; finish with `exact` only after alignment.

## Existential/order failure

**Signal:** `use c` produces an intractable equality.

**Recover:** derive the witness from an existing `≤` hypothesis, constructor case, or known gap; avoid imaginary subtraction. Unpack `≤` hypotheses before guessing.

## Disjunction failure

**Signal:** choosing `left`/`right` creates an unprovable branch.

**Recover:** delay branch choice; split the natural/order evidence first. If consuming `P∨Q`, use `cases` and solve both branches.

## Multiplication cancellation failure

**Signal:** desired cancellation theorem requires `a ≠ 0`.

**Recover:** derive nonzero from product nonzero if possible; split on zero/nonzero; if zero remains possible, the conclusion may be false and should not be forced.

## Automation failure

**`simp_add`**: if non-additive structure remains, isolate it and prove/normalize that part first.

**`decide`**: if variables remain, use symbolic reasoning. If the goal is closed but still fails, verify the custom DecidableEq/tactic imports.

## FLT boundary

**Signal:** user expects prior worlds to prove the final FLT statement.

**Recover:** inspect the source route. NNG4 uses hidden `xyzzy`, backed by an unrestricted axiom. Explain the game mechanism. Route genuine FLT formalization outside this skill.

## Stop condition

Return “insufficient assumptions / unavailable theorem” when the mathematical precondition truly fails. Do not compensate with stronger unlisted axioms, later-world theorems, or silent Mathlib automation in a level-restricted task.
