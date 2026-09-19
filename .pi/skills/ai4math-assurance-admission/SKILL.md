---
name: ai4math-assurance-admission
description: Reviews a frozen mathematical candidate and its receipts for provenance, independence, statement faithfulness, verifier scope, and unresolved obligations. Use to produce a candidate-only admission recommendation; never use it to self-admit Evidence, Results, or Solutions.
---

# AI4Math Assurance and Admission Review

Use this Skill only after a candidate statement and digest are frozen.

## Review contract

1. Bind the exact ProblemContract, obligation, candidate digest, claimed outcome, assumptions, and quantifiers.
2. Separate generator assertions from independently produced receipts.
3. Check receipt identity, freshness, input digest, verifier capability, trust domain, limits, and exit status.
4. Audit statement identity and statement faithfulness separately from formal elaboration or kernel success.
5. Check axiom/escape use, counterexample validity, dependency closure, and proof/counterexample conflicts.
6. List every residual obligation and the strongest conclusion justified by the weakest missing gate.

## Output

Return a bounded review with:

- `candidate_identity`;
- `verified_capabilities`;
- `missing_or_invalid_capabilities`;
- `independence_assessment`;
- `statement_faithfulness_assessment`;
- `residual_obligations`;
- `recommendation`: `reject | revise | eligible_for_independent_admission_review`.

The output is a Candidate review only. This Skill cannot write truth ledgers, sign verifier receipts, or admit a Result or Solution.

## Internal package routing

Read `INTERNAL-PACKAGES.json` and `references/internal-package-routing.md` before choosing source material. Load only the smallest applicable internal package. Complete package bodies are bundled under this top-level Skill. Use only repository-relative registry paths; rights remain HOLD and bundling does not grant publication or execution authority.

## Progressive disclosure

Read `references/consolidated-core.md` for the capability matrix, receipt validation, independence analysis, statement-faithfulness audit, proof/counterexample/computation review, conflict handling, adversarial probes and admission recommendation semantics consolidated from the reviewed assurance sources.
