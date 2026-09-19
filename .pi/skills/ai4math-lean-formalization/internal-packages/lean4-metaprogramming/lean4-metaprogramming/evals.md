# Evaluation Cases

These cases are designed for a fresh agent that has only this installed skill. Passing means it routes to the correct file/method and preserves the stated invariants; exact code signatures remain version-sensitive.

## Trigger Tests

### T1 — Macro design
**Prompt**: “I want `twice t` syntax in Lean 4 that expands to a pair. How should I implement it?”

**Expected**: Trigger skill; route to ch05/ch06; recommend syntax + hygienic macro because the transformation is context-free; use quotations.

### T2 — Type-directed literal
**Prompt**: “My custom literal should elaborate differently depending on its expected type.”

**Expected**: Trigger; route to ch07; use a term elaborator; inspect expected type; postpone if absent/unsolved; delegate children to normal elaboration.

### T3 — Metavariable inspection
**Prompt**: “Why does pattern matching on my `Expr` still see an `mvar` after I solved the goal?”

**Expected**: Trigger; route to ch04; explain assignment does not mutate existing expression structure; call `instantiateMVars` before inspection.

### T4 — Tactic implementation
**Prompt**: “Write a custom tactic that finds a local hypothesis definitionally equal to the target.”

**Expected**: Trigger; route to ch09 + ch04; enter main context, scan local declarations, use mutation-aware defeq, assign proof, close goal coherently.

### T5 — Pretty printer
**Prompt**: “I want applications of my constructor to print as custom notation.”

**Expected**: Trigger; route to ch12; choose unexpander for simple inverse syntax or delaborator for semantic/contextual rendering; demand round-trip equivalence.

## Negative Trigger Tests

### N1 — Ordinary theorem proof
**Prompt**: “Prove `Nat.succ n > n` in Lean.”

**Expected**: Do not invoke this skill merely because Lean is mentioned; this is ordinary theorem proving unless the user asks for metaprogramming/tactic implementation.

### N2 — General compiler theory
**Prompt**: “Explain SSA form in compiler design.”

**Expected**: Do not trigger; the pipeline analogy in this skill is specific to Lean metaprogramming.

### N3 — Lean project build error
**Prompt**: “Lake cannot find package X.”

**Expected**: Do not trigger unless the error concerns metaprogramming APIs or generated syntax/elaboration.

## Method Selection Tests

### M1 — Macro vs elaborator
**Case A**: syntax is a transparent alias. **Expected**: macro.

**Case B**: same syntax must inspect expected type. **Expected**: elaborator with possible postponement.

### M2 — `whnf` vs full reduce
**Prompt**: “I only need to know whether the target reduces to a forall.”

**Expected**: instantiate current mvars, use `whnf` under suitable transparency, avoid full normalization unless head form remains insufficient.

### M3 — `mkAppM` failure
**Prompt**: “`mkAppM` cannot infer an implicit parameter because no explicit argument constrains it.”

**Expected**: explain underconstraint; provide more explicit information or use `mkAppOptM`/explicit construction, not repeated blind retries.

## Failure Recovery Tests

### F1 — DefEq probe contaminates state
**Scenario**: candidate 1 fails but partially assigns metavariables; candidate 2 behaves differently afterward.

**Expected**: diagnose stateful `isDefEq`; isolate each candidate with `withoutModifyingState` or explicit save/restore, committing only the chosen candidate.

### F2 — Hidden unsolved tactic goal
**Scenario**: custom tactic calls `setGoals []` and Lean later reports an unsolved metavariable or invalid proof.

**Expected**: diagnose goal-list/proof-state mismatch; assign the main `MVarId` to a valid proof before closure or replace it with real successor goals.

### F3 — Unexpander pattern never fires on parenthesized form
**Expected**: explain unexpanders run before parenthesizer; match nested syntax structurally without relying on inserted parentheses.

## Fresh-Agent Simulation

A fresh agent should be able to answer this compound task with no original book:

> “Design a `by_cases_type t` term extension that can only decide its behavior once Lean knows the expected type; inside its implementation I need to inspect that type's head constructor, and I want a readable printed form later. What layers and safety checks do I need?”

**Expected route and answer skeleton**:
1. ch07: use a term elaborator, not a macro, because semantics depend on expected type; postpone if expected type is absent/metavariable.
2. ch04: after expected type is available, `instantiateMVars`; use `whnf` to expose the head; choose transparency intentionally; remember semantic checks/unification may mutate state.
3. ch04: build the resulting expression with high-level meta constructors; avoid loose bvars and underconstrained inferred applications.
4. ch12: add a delaborator/unexpander only when output can re-elaborate to equivalent meaning; preserve fallback printing.
5. SELF_CHECK: verify local context, state mutation, expected-type readiness, version-specific API names, and round-trip meaning.

## Coverage / Hallucination Audit Questions
- Can every major method in SKILL.md be located in `provenance.md`? Expected: yes.
- Do solution pages contribute edge-case validation rather than duplicated chapter summaries? Expected: yes.
- Are there claims that Lean metaprogramming APIs are version-stable? Expected: no.
- Does any core rule require the original book to be present at runtime? Expected: no.
