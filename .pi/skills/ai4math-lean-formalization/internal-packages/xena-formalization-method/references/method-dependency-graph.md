# METHOD_DEPENDENCY_GRAPH

1. **Intent classification**
   - depends on: user goal, desired artifact, current Lean/mathlib context.
   - routes to: proof, statement, API, research blueprint, teaching, AI verification.

2. **Statement precision**
   - depends on: types, structures, quantifier order, domain conditions.
   - gates every downstream method. If the statement is wrong, a correct proof is still the wrong result.

3. **Representation and API selection**
   - depends on: downstream operations and theorem shape.
   - enables: reusable lemmas, automation, implementation independence.

4. **Explicit proof construction**
   - depends on: valid statement + usable API.
   - starts with goal-state tactics and local lemmas.

5. **Equality/normalization route**
   - depends on: explicit proof state.
   - chooses among definitional equality, rewriting, extensionality, canonicalization, conversion, isomorphism/transport.

6. **Induction/elimination route**
   - depends on: inductive data or quotient/universal-property structure.
   - uses recursors, cases, induction, quotient lifts, well-definedness proofs.

7. **Automation route**
   - depends on: goal normalized into the solver's domain.
   - produces: proof certificate/term rechecked by kernel.

8. **Failure recovery**
   - if proof search stalls, inspect in order: parse/scope -> missing hypotheses -> equality layer -> wrong representation -> missing API -> wrong generality -> library gap -> false/underspecified statement.

9. **Research project scaling**
   - depends on: statement feasibility + library inventory.
   - builds dependency graph, parallel workstreams, tracked assumptions, and documentation.

10. **AI/formal route**
    - depends on: formal statements and library definitions.
    - generated proof -> compile/check -> security audit if executable code exists.
    - generated definition/statement -> human semantic audit -> characterization tests -> downstream proofs.
    - universal conjecture -> counterexample search -> formal verification -> human digestion.
