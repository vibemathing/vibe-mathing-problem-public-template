---
name: ai4math-assurance-admission
description: Reviews a frozen mathematical candidate and its receipts for provenance, independence, statement faithfulness, verifier scope, and unresolved obligations. Use to produce a candidate-only admission recommendation; never use it to self-admit Evidence, Results, or Solutions.
---

# AI4Math Assurance and Admission Review

Use this Skill only after a candidate statement and digest are frozen.

## When to Use This Skill

- A frozen proof, counterexample, computation, or formal candidate needs assurance review.
- A claim must be matched to exact receipts, verifier capabilities, independence, and coverage.
- Conflicting proof/counterexample evidence or unresolved statement-faithfulness risk must be surfaced.

## Not For / Boundaries

- Do not generate the candidate being reviewed or call maker self-review independent.
- Do not write Evidence, Result, Solution, or admission ledgers.
- Do not treat execution success, file count, tests, commits, or model confidence as mathematical closure.
- Do not run verdict-bearing review on an automatic schedule or loop.

## Quick Reference

```text
freeze candidate -> verify identity/freshness -> classify capabilities
-> test independence and statement faithfulness -> map support and coverage
-> list residual obligations -> candidate-only recommendation
```

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

## Examples

### Example 1: Kernel-checked term with statement drift

Keep `kernel_check` valid for the compiled type but return `revise` until an independent statement-faithfulness check binds that type to the ProblemContract.

### Example 2: Finite computation supporting a universal claim

Record the tested range as valid numeric/counterexample coverage, leave the unbounded quantifier open, and reject a universal completion claim.

### Example 3: Conflicting proof and counterexample receipts

Bind both receipts, verify identities, report the conflict, and block recommendation until the statement/domain mismatch or invalid receipt is resolved.

## Internal package routing

Read `INTERNAL-PACKAGES.json` and `references/internal-package-routing.md` before choosing source material. Load only the smallest applicable internal package. Complete package bodies are bundled under this top-level Skill. Use only repository-relative registry paths; rights remain HOLD and bundling does not grant publication or execution authority.

## Progressive disclosure

Read `references/consolidated-core.md` for the capability matrix, receipt validation, independence analysis, statement-faithfulness audit, proof/counterexample/computation review, conflict handling, adversarial probes and admission recommendation semantics consolidated from the reviewed assurance sources. Load `references/evidence-claim-coverage.md` when the review must distinguish evidence existence, support relation and full claim coverage.

## References

- `references/consolidated-core.md`：候选证据能力、独立性、陈述忠实性、冲突和准入建议的项目原创综合。
- `references/evidence-claim-coverage.md`：证据存在、支持关系、覆盖范围和残余义务的分层审查。

## Maintenance

- Sources: project assurance contracts and independently rewritten method intake recorded in `CONSOLIDATION-MAP.md`.
- Last updated: 2026-09-21.
- Verification: strict Skill structure check, entry digest reconciliation, and repository Harness validation.
