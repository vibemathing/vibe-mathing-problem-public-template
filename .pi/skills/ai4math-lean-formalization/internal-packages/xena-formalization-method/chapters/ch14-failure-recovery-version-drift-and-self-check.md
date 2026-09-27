# Chapter 14: Failure Recovery, Version Drift, and Self-Check

## Core Idea

A robust formalization method must know when its preferred route is wrong. Diagnose failures by layer, switch representations or interfaces deliberately, and run a semantic/trust audit before release. The Xena corpus spans major Lean/mathlib changes, so conceptual methods must be separated from historical API details.

## Recovery Ladder

When progress stops, climb this ladder in order:

### 1. Syntax and elaboration

Check precedence, parentheses, binder scope, function application, implicit arguments, notation namespace, and the actual inferred type. Many “mathematical” problems vanish here.

### 2. Preconditions and statement shape

Check missing nonzero/nonempty/positivity/finite assumptions, quantifier order, and edge cases. Try tiny examples. If the theorem is false as stated, stop proof search and repair it.

### 3. Equality layer

Determine whether the mismatch is syntactic, definitional, propositional, extensional, or only an isomorphism. Use the matching bridge rather than stronger automation.

### 4. Representation

Ask whether the current model exposes the needed fact. Switch locally to another representation or prove a conversion theorem. Universal properties can fail to expose element-level information; computation-oriented representations can be poor proof interfaces.

### 5. API/library gap

Look for missing extensionality, simp lemmas, coercions, instances, or characterization theorems. If many proofs suffer, fix the library layer.

### 6. Generality mismatch

A theorem may be stated with assumptions too strong, too weak, or in a hierarchy that does not line up with available instances. Refactor the core theorem and add ergonomic wrappers.

### 7. External dependency gap

For research mathematics, the required definition/theorem may simply not exist formally. Add it to the dependency graph; temporarily assume it only when that helps architecture and the gap remains explicit.

## Historical Version Drift

The source contains Lean 3 installation commands, APIs, tactic names, and 2017–2026 library states. Treat these as evidence for *concepts*, not current instructions.

For any concrete code answer:
1. identify the user's Lean version/toolchain;
2. search/check the current declaration name and signature;
3. inspect current imports and namespaces;
4. translate historical patterns into the contemporary API;
5. compile the minimal example.

Do not preserve an old syntax merely because it appears in the source.

## Release Self-Check

Before presenting a nontrivial result:

**Goal:** Did we solve the actual user goal or a nearby theorem?

**Statement:** Are types, binders, domains, and equality notions correct?

**Method:** Were all method preconditions satisfied? Did a solver operate in its intended domain?

**Exceptions:** Did we handle zero/empty/small/degenerate inputs and choice/computability boundaries?

**Dependencies:** Are all imported assumptions, axioms, and placeholders known? Is the library/API current?

**AI semantics:** If generated, were statements/definitions independently checked for meaning?

**Trust:** Does the exact proof compile under the intended toolchain? For high assurance, is an independent check warranted? Is generated code safe to execute?

**Explanation:** Can a fresh mathematician locate the proof spine or conceptual mechanism without reading all generated code?

## Stop Conditions

Return an explicit uncertainty rather than fake success when:

- the informal theorem is ambiguous in a way that changes truth;
- required source mathematics is missing or disputed;
- a generated definition cannot be matched to a trusted concept;
- the proof only works by an unverified axiom/placeholder;
- the environment/version needed to confirm concrete code is unavailable;
- a claimed counterexample has not survived formal verification.


## Anti-patterns

- Switching tactics repeatedly without first identifying the failing layer.
- Copying historical Lean syntax into a current project without checking declarations/imports.
- Treating a successful compile as evidence that an AI-generated statement has the intended meaning.
- Hiding unresolved assumptions behind automation or packaging.
- Releasing a proof that cannot be reproduced in the stated toolchain.

## Validation Checkpoint

When changing routes, record the diagnosed layer and the evidence for the switch. This prevents cycling through tactics without learning from failure. For historical examples, distinguish conceptual advice from exact syntax and verify any concrete declaration against the user's toolchain. Before final delivery, rerun the smallest representative examples after API or representation changes, inspect remaining axioms/sorries, and confirm that the theorem proved is the theorem intended. If any of statement meaning, dependency validity, environment reproducibility, or proof checking remains unresolved, report that uncertainty explicitly rather than upgrading it to a successful result.

## Key Takeaways

Recovery is structural: syntax → statement → equality → representation → API → generality → missing mathematics. Version-check concrete code, audit meaning separately from proof checking, and make uncertainty an acceptable output state.

## Connects To

All chapters; for quick routing use [../cheatsheet.md](../cheatsheet.md).
