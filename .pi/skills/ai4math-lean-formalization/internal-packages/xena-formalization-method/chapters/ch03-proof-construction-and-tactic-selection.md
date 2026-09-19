# Chapter 3: Proof Construction and Tactic Selection

## Core Idea

Choose tactics by the logical or algebraic shape of the current goal. Build a transparent proof route first; introduce automation after the route and solver preconditions are clear.

## Frameworks Introduced

### Structural tactic table

- `intro`: expose a universally quantified variable or implication premise.
- `exact`: close the goal with a term of the required type, allowing definitional equality.
- `apply`: use a theorem backwards; replace the conclusion by its premises.
- `refine`: like a controlled `apply`, useful when some arguments are supplied and others become goals.
- `have`: create a named intermediate fact when a proof needs a local bridge.
- `cases`: eliminate a sum/disjunction/inductive alternative or unpack data.
- `split`: build a conjunction/structure with multiple fields.
- `left` / `right`: select a disjunct.
- `induction`: use the recursor specialized to a proposition about an inductive object.
- `exfalso`: change the target to false when contradiction is the clean route.

Names are historically stable ideas, but concrete Lean syntax should be checked against the current environment.

### Explicit-to-automated progression

1. Express the mathematical spine with structural tactics and local lemmas.
2. Normalize definitions and expressions only as much as necessary.
3. Hand the residual domain problem to a specialized solver.
4. If the solver fails, inspect its input shape instead of trying unrelated automation.
5. Once the proof is stable, compress repetitive local work if readability improves.

For polynomial identities, a typical route is rewrite hypotheses → normalize → `ring`. For linear inequalities, rewrite into linear form → `linarith`; for nonlinear polynomial inequalities, `nlinarith` may apply. Numeral computations often belong to `norm_num`. Library search can discover an existing theorem when the proof should be reuse rather than reconstruction.

### Local lemma extraction

When a tactic sequence recurs, ask whether it reflects a mathematical interface lemma. Repeated proof friction is often a library design signal. Extracting a theorem can be better than building a more elaborate tactic.

## Failure Modes

**Automation ignores a useful hypothesis.** Some solvers normalize the target but do not automatically use a hypothesis in the needed direction. Rewrite or derive the relevant equality first.

**The goal is nearly right.** If a theorem/hypothesis has the intended mathematical content but a definitional/subsingleton/detail mismatch remains, `convert` or an explicit equality bridge may create a small solvable subgoal.

**A theorem requires a side condition.** Split cases (`by_cases`) when division, inverses, or cancellation require nonzero hypotheses. Do not smuggle the condition through a totalized operation.

**Parser or elaborator errors appear before mathematics.** Check precedence, associativity, quantifier scope, function application, and implicit arguments. A surprising parse tree can make a correct tactic plan irrelevant.

## Practitioner Heuristic

Keep the file as close to “zero active errors” as practical. Temporary `sorry`/assumptions can be useful scaffolding in a large project, but each must have an explicit dependency role and removal plan. A finished deliverable has no untracked gaps.

## Anti-patterns

- Tactic roulette: trying commands with no model of the goal transition.
- Reproving a standard library theorem because search was skipped.
- Asking `ring` or arithmetic tactics to solve representation/type mismatches.
- Making the proof shorter at the cost of obscuring the mathematical decomposition.

## Validation Checkpoint

Prefer a proof spine that mirrors the theorem's logical constructors. For each subgoal, name the rule that creates it: implication introduction, constructor selection, case split, induction hypothesis, or a previously proved lemma. If a large tactic closes several unrelated obligations at once, temporarily replace it with explicit steps until the route is understood. Then reintroduce automation and compile again. The final proof may be compact, but you should still be able to reconstruct why each major subgoal follows and identify which assumptions it consumes.

## Key Takeaways

Let logic choose the first tactic and normalized mathematics choose the solver. Repeated difficulty often indicates a missing lemma or API, not a need for stronger automation.

## Connects To

Equality normalization: [04](ch04-equality-rewriting-and-normalization.md). Trusted automation: [08](ch08-automation-reflection-and-trust.md). Recovery order: [14](ch14-failure-recovery-version-drift-and-self-check.md).
