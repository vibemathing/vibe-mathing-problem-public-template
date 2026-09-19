# Chapter 6: Lean Execution Discipline

## Core Idea
Proof work is compiler-guided. Search the local/project context before inventing infrastructure, use Lean LSP to inspect goals and diagnostics, and verify with the project build rather than trusting prose or empty-looking diagnostics.

## Search Ladder
1. local/project search;
2. semantic Lean search for mathematical content;
3. type-pattern search for simple shapes;
4. direct source/API inspection when needed.

Do not use generic filesystem grep as a theorem-discovery substitute when the Lean search tools are available.

## Tactic Escalation
For small goals, try cheap deterministic tactics first (`rfl`, simplification, arithmetic/ring/omega-family automation, exact/apply suggestions), then stronger automation/search. After each meaningful edit, inspect the goal state and compile diagnostics.

## Verification Ladder
- LSP diagnostics/goal after local edits;
- file/module check when useful;
- project `lake build` as the integration gate;
- axiom inspection when declarations may hide non-standard assumptions.

Empty diagnostics do not alone prove a tactic attempt solved the goal; inspect the resulting goal state. Likewise, a helper that compiles against `sorry` dependencies can still be useful progress, but it does not mean the dependency cone is complete.

## Sorry and Axiom Discipline
A `sorry` with the intended type is an explicit unresolved obligation. A proof that transitively depends on `sorryAx` can launder that gap behind a declaration that looks closed; the axiom sweep exists to catch this. Do not introduce new axioms to manufacture completion.

## Compiler-Guided Repair
Classify failures: missing name/import, type mismatch, instance synthesis, simplifier mismatch, elaboration ambiguity, termination/performance, or genuine mathematical gap. Change one cause at a time, re-check, and preserve a small reproducible failing goal when escalation is needed.

## Source Provenance
Primary: bundled `lean4` skill and references, prover prompts, axiom/sorry scripts and tests.

## Frameworks Introduced
- **Search-before-invent**: inspect local APIs and semantic theorem search before building parallel infrastructure.
- **Compiler-guided repair loop**: edit → inspect diagnostics/goals → classify failure → make one targeted change → re-check.
- **Verification ladder**: local LSP feedback is fast; project build and axiom inspection are stronger evidence.

## Key Concepts
- **Goal state**: authoritative outstanding obligations after a tactic attempt.
- **Semantic search**: theorem lookup by mathematical content rather than filename text.
- **Instance synthesis failure**: typeclass search cannot construct required structure; often a modeling/import issue.
- **Axiom footprint**: non-standard axioms a declaration depends on.
- **Scoped sorry**: explicit unresolved proof at the intended type, preferable to a fake proof or weakened statement.

## Mental Models
- Treat Lean as an **interactive typechecker**, not a text generator target. Every proposed proof step should reduce or clarify a goal.
- Treat `lake build` as **integration truth** and LSP as **fast local feedback**.

## Anti-patterns
- **Empty diagnostics = solved**: some tooling paths can be misleading; inspect goals and build.
- **Filesystem grep for theorem search**: loses semantic/type information available through Lean tooling.
- **New axiom for convenience**: hides rather than solves the formalization obligation.
- **Rewrite working proofs during unrelated work**: increases regression surface.

## Worked Example
A prover expects `SomeNamespace.foo` but local search finds no such lemma. Semantic search reveals an equivalent theorem under a different namespace requiring an instance not currently in scope. Hover/goal inspection shows the missing typeclass. Add or derive the correct instance/import, apply the real theorem, re-run diagnostics, then `lake build`. If no theorem exists after verified search, state the exact missing helper and follow the infrastructure gradient instead of guessing more names.

## Key Takeaways
1. Goal state and compiler output outrank natural-language confidence.
2. Search semantically before creating new APIs.
3. Preserve honest unresolved obligations.
4. Validate at the project level before claiming success.

## Connects To
- **Ch 05**: prover mode sets the shape of Lean work.
- **Ch 11**: external mathematical sources complement library search.
- **Ch 14**: axiom/sorry gates at completion.
