# Chapter 8: Automation, Reflection, and Trust

## Core Idea

Use strong automation without enlarging the trusted base unnecessarily. The tactic or external solver may search, normalize, or compute aggressively; the mathematical guarantee comes from a proof term or certificate rechecked by Lean's kernel (and, for high-stakes work, optionally by an independent checker).

## Reflection Pattern

A reflective tactic such as polynomial normalization follows a general architecture:

1. reify a Lean expression into a simpler internal syntax;
2. compute a canonical form with an algorithm;
3. use a proved correctness theorem connecting the reified computation to the original semantics;
4. return a proof term;
5. let the kernel type-check that proof term.

The tactic implementation can contain bugs that make it fail, run slowly, or produce rejected terms. It should not be able to turn a false theorem into a valid kernel proof unless the trusted base itself is compromised.

## Solver Routing

Automation works best after normalization:

- polynomial identities → reflection/ring normalization;
- linear arithmetic → a linear solver after non-linear/structural clutter is removed;
- nonlinear polynomial arithmetic → nonlinear solver with relevant hypotheses exposed;
- concrete numerals → certified numeral normalization;
- theorem reuse → library search after types/coercions are settled.

A solver is not a substitute for a missing representation bridge, quotient well-definedness proof, extensionality lemma, or nonzero hypothesis.

## Trust Layers

For a formal result, distinguish:

1. **Source prose** — may contain omissions or errors.
2. **Formal statement** — must be semantically audited.
3. **Tactic/agent/search code** — untrusted generator of candidate proofs.
4. **Kernel/type checker** — small trusted verifier of proof terms.
5. **Axioms** — inspect when foundational strength matters.
6. **Build/toolchain** — relevant for very high assurance.

A proof certificate also enables independent rechecking. Research formalizations have used external type checkers to increase confidence that one implementation is not the sole verifier.

## Security Boundary

Lean files are programs, not inert mathematical PDFs. Generated repositories can include custom commands, metaprogramming, or ordinary I/O. Before compiling unfamiliar large generated code in a sensitive environment:

1. sandbox the build;
2. inspect files/commands that are not declarations/proofs;
3. inspect custom tactics and unsafe/foreign interfaces;
4. pin a known-good Lean/toolchain version;
5. review suspicious axioms or escape hatches;
6. optionally check the final declarations with an independent verifier.

This security audit is separate from mathematical proof checking.

## Human Understanding

Kernel acceptance gives correctness of the formal derivation, not a human explanation. A giant generated proof may still need a second artifact that reveals the proof spine, conceptual lemmas, and mathematical mechanism. The certificate and the exposition serve different purposes and should be cross-linked rather than conflated.

## Anti-patterns

- Trusting an LLM or tactic because its prose/output “looks formal.”
- Treating successful numerical computation as a theorem without a certificate.
- Treating proof checking as proof that the statement's definitions mean the intended thing.
- Running a huge generated Lean repository with full machine permissions without inspection.

## Validation Checkpoint

Separate tactic success from trust. Confirm the tactic produced a proof term accepted by the kernel, then inspect any axioms, oracles, native-code shortcuts, or imported assumptions that affect the desired assurance level. For reflective procedures, identify the reification step, normalization/decision procedure, correctness theorem, and final kernel check. If external software generates certificates or proof code, treat the generator as untrusted and the checker boundary as critical. A fast tactic that fails is an engineering problem; a checker bypass would be a trust problem.

## Key Takeaways

Untrusted search plus a small trusted checker is a powerful architecture. Keep semantic statement review, proof-term verification, security review, and human explanation as distinct gates.

## Connects To

AI proof route: [12](ch12-ai-autoformalization-and-semantic-audit.md). Machine-proof digestion: [13](ch13-counterexamples-benchmarks-and-proof-digestion.md). Release audit: [14](ch14-failure-recovery-version-drift-and-self-check.md).
