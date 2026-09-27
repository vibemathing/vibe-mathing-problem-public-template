# Operational Section 1: Architecture and Trust Boundary

## Core Idea
Model every LeanEval evaluation around a trusted statement, untrusted solver code, and a fixed bridge. Comparator acceptance only has meaning when those roles remain intact.

## Frameworks Introduced

- **Three-artifact proof boundary**
  - **When to use**: any question about what a solver may edit, why comparator accepts/rejects a proof, or where trust lives.
  - **How**:
    1. `Challenge.lean` is trusted and states the target theorem/definitions with holes.
    2. `Submission.lean` and modules under `Submission/` are solver-controlled.
    3. `Solution.lean` is generated/trusted and bridges Challenge-named declarations to `Submission.<name>`.
    4. Comparator checks Challenge and Solution as separate modules; do not compare Submission directly to Challenge.

- **Reachability-based comparison**
  - **When to use**: judging whether extra declarations or dependencies can influence acceptance.
  - **How**: comparator walks constants reachable from configured theorem/definition targets. Reachable theorem dependencies must match between Challenge and Solution unless a target is explicitly treated as a definition hole.

- **Axiom allowlist gate**
  - **When to use**: proof succeeds in Lean but comparator rejects it, or a proof uses nonstandard axioms/tactics.
  - **How**: check all reachable axioms against `{propext, Quot.sound, Classical.choice}`. `sorryAx` and `Lean.ofReduceBool` are outside the allowlist, so `sorry` and `native_decide` do not pass this gate.

## Key Concepts

- **Challenge**: trusted benchmark statement; solver should not edit it.
- **Submission**: solver-owned Lean proof/definitions under `namespace Submission`.
- **Solution**: trusted generated bridge from Challenge names to Submission names.
- **`theorem_names`**: comparator targets whose theorem bodies and reachable graph are compared.
- **`definition_names`**: targets for which type compatibility is central and bodies may differ.
- **`permitted_axioms`**: explicit transitive axiom allowlist.
- **Kernel replay**: final checking of the exported Solution environment in Lean's kernel.
- **Nanoda replay**: additional independent-kernel check forced by the LeanEval harness.

## Mental Models

- **Treat the bridge as a proof adapter**: if Solution typechecks only by referencing `Submission.foo`, then acceptance connects solver code to the exact trusted signature.
- **Think transitively**: the comparison/axiom question is about the reachable dependency graph, not only the top theorem text.
- **Separate syntax from trust**: a file named `Solution.lean` is trusted only when taken from the pristine generated workspace; a solver-modified copy breaks the assumed boundary.

## Anti-patterns

- **Editing Challenge/Solution to make a proof pass**: this changes the trusted benchmark and invalidates the solver path.
- **Assuming a Lean compile proves comparator acceptance**: comparator adds constant-graph, axiom, sandbox, and kernel requirements.
- **Assuming all holes are theorem holes**: `def` and `instance` holes have different comparison semantics; see ch10.

## Reference Table

| Artifact | Controlled by | Normal solver edits? | Comparator role |
|---|---|---:|---|
| `Challenge.lean` | benchmark repository | No | trusted target |
| `Submission.lean` | solver | Yes | untrusted proof/definitions |
| `Submission/*.lean` | solver | Yes | helper code imported by Submission |
| `Solution.lean` | generator/repository | No | trusted bridge to Submission |
| `config.json` | generator/repository | No | names, axiom policy, base settings |
| `WorkspaceTest.lean` | template/repository | No | invokes comparator and forces nanoda |

## Worked Example

The starter problem `two_plus_two` has the same theorem signature in Challenge and Submission. Solution proves the trusted theorem with `exact Submission.two_plus_two_eq_four`. A solver replaces the `sorry` in Submission with a proof such as `norm_num`. Comparator can then verify the bridge while rejecting an unresolved `sorry`, because `sorryAx` is outside the axiom allowlist.

This example is also the installation smoke because it minimizes theorem complexity. If it fails, diagnose environment/integration before debugging a hard benchmark proof.

## Key Takeaways

1. Diagnose trust roles before diagnosing Lean code.
2. Comparator reasons over reachable constants and axioms, not only source text.
3. Solver-owned changes belong in Submission paths.
4. A passing Lean build is necessary but not the full acceptance condition.
5. Definition-hole semantics require extra specification review.

## Connects To

- **ch03**: how the bridge is executed through `WorkspaceTest`.
- **ch07**: where untrusted Submission elaboration occurs and what confines it.
- **ch10**: relaxed body comparison for `def`/`instance` holes.
