# Operational Section 10: Multi-hole Problems and Specification Quality

## Core Idea
Multi-hole problems can contain theorems, definitions, and named instances. Comparator semantics differ by hole kind, so authoring quality depends on both correct generator configuration and sufficiently strong trusted specifications.

## Frameworks Introduced

- **Hole-kind routing**
  - **When to use**: manifest has multiple holes or generated config includes `definition_names`.
  - **How**:
    1. Classify each owned declaration by kind.
    2. Put theorem targets in `theorem_names`.
    3. Put definition/instance targets requiring body variation in `definition_names`.
    4. Ensure Submission exposes every named target under `namespace Submission`.
    5. Ensure Solution builds the correct bridge for each kind.

- **Named-instance stability rule**
  - **When to use**: an `instance` is a solver hole.
  - **How**: give the instance an explicit stable name. Do not rely on Lean's auto-generated instance name because the generator/comparator addresses holes by declaration name.

- **Specification-strength review**
  - **When to use**: any `def`/`instance` body may vary.
  - **How**: ask what trusted theorem(s) constrain the semantic value/behavior. Type equality alone may accept a trivial or unintended implementation.

## Why `definition_names` Need Extra Review

For normal theorem targets, comparator's reachable constant comparison ties the proof to the Challenge statement/body graph plus the axiom allowlist. For `definition_names`, the intended flexibility allows a participant to provide a different body with the same required type. That flexibility can become a benchmark weakness when no theorem statement forces the intended behavior.

Use this review question:

> If a solver chooses the easiest inhabitant of this type, do the trusted theorem holes force it to satisfy the intended semantics?

If the answer is unclear, the problem needs stronger specification or explicit human review before it should be treated as a meaningful benchmark.

## Worked Example: `def_hole_example`

The example owns two holes:

- `foo : Nat` — definition hole.
- `foo_def : foo = 37` — theorem hole.

Generated config routes `foo` to `definition_names` and `foo_def` to `theorem_names`. Submission may choose a body for `foo`, but the theorem requires the chosen value to equal 37. The theorem therefore supplies a semantic constraint that prevents an arbitrary unrelated `Nat` from satisfying the whole problem.

The generated Solution exposes a reducible definition backed by `Submission.foo` and proves the theorem via `Submission.foo_def`.

## Instance-hole Example

An instance-hole problem can have a type/instance pair such as a carrier type plus `Inhabited` instance. Both may be routed as definitions. This is useful for testing the pipeline, but a production benchmark must review whether any trusted theorem pins down meaningful behavior. Merely producing an inhabitant of the right type may be too weak for the author's intent.

## Author Checklist

- Every hole appears in exactly one problem manifest.
- Every instance hole has an explicit name.
- Generated `config.json` classifies theorem vs definition targets correctly.
- Submission starter contains all required declarations.
- Solution bridge references corresponding `Submission` declarations.
- Every flexible def/instance has enough trusted theorem constraints.
- Permitted axioms remain unchanged unless deliberately reviewed.
- `generate --problem <id>` and `check-generated-builds --problem <id>` pass.
- A known-good submission passes comparator/nanoda.
- A plausible trivial/unintended submission is tested when spec strength is in doubt.

## Anti-patterns

- **One theorem in `holes` plus hidden unlisted solver obligations**: generator/comparator cannot enforce what the manifest does not own.
- **Anonymous instance holes**: unstable names break addressing.
- **Equating type correctness with semantic correctness**: especially dangerous for flexible definitions.
- **Adding heuristic automated guards and treating them as proof of spec quality**: the source explicitly treats this as a review problem because comparator cannot infer author intent.

## Key Takeaways

1. Multi-hole manifests describe every solver-owned target explicitly.
2. Hole kind changes comparator behavior.
3. Named instances are required for stable generation.
4. Definition/instance holes transfer part of correctness to trusted spec theorems.
5. Human semantic review remains necessary for flexible definitions.

## Connects To

- **ch01**: graph-comparison model.
- **ch05**: manifest/generation workflow.
- **ch07**: proof-integrity consequences of relaxed definition comparison.
