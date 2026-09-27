# Consolidated core: independent assurance and admission

## Purpose

Decide what a frozen candidate and its evidence actually justify. Assurance reviews evidence capabilities and statement correspondence; admission is a separate authority action. This Skill prepares a recommendation and cannot admit its own candidate.

## Review inputs

Require:

- ProblemContract identity and digest;
- exact target obligation;
- candidate bytes and digest;
- claimed outcome;
- dependency graph;
- generator identity;
- all evidence receipts and invalidations;
- allowed axioms/trust policy;
- known conflicts and failed routes.

Missing identity is a hard stop, not a paperwork defect.

## Capability matrix

Assess capabilities independently:

| Capability | Question |
|---|---|
| source identity | Is this the canonical statement/version? |
| statement faithfulness | Does the checked artifact encode the frozen claim? |
| numeric check | What bounded instances/precision were tested? |
| symbolic check | What exact transformation or solver theory was checked? |
| counterexample check | Is the witness legal and does it negate the exact conclusion? |
| Lean elaboration/kernel | Did the exact term check under the recorded environment/axioms? |
| independent replay | Was evidence reproduced by a sufficiently separate path? |
| human/adversarial review | Were hidden assumptions, vacuity and boundary cases attacked? |
| dependency closure | Are all decisive imported obligations established? |

Do not compress these into one “verified” flag.

## Receipt validation

For each receipt check schema, producer, freshness, input/output digests, command, environment, trust domain, limits, exit status, checker capability and invalidation status. A receipt is evidence about an event only if it binds the exact candidate under review.

## Independence test

Independence is graded by shared failure modes:

- same code path, parser, model or prompt is not independent merely because rerun;
- a clean process improves reproducibility but may share implementation defects;
- a separate checker with independent encoding is stronger;
- adversarial statement translation review covers a different risk from kernel replay;
- human review is useful but does not substitute for executable proof checking where required.

State residual correlated risks.

## Statement-faithfulness audit

Compare source and artifact across:

- domains and type inhabitants;
- quantifier order and implicit binders;
- definitions and equality notions;
- assumptions and regularity conditions;
- conclusion direction and strength;
- finite/infinite and boundary cases;
- totalization and vacuity;
- classical axioms and excluded cases.

Kernel checking cannot detect a faithful-looking but wrong translation.

## Proof review

Check dependency closure, case coverage, witness construction, induction form, termination, imported theorem applicability, forbidden escapes and axiom footprint. Require high-assurance replay according to the project gate for terminal proof results.

## Counterexample review

Independently decode and validate the witness. Check every premise, exact negation, arithmetic/precision, minimization claims and source-domain legality. A counterexample to a lemma is not automatically a counterexample to the root theorem.

## Computational review

Confirm domain bounds, generator completeness, filters, seeds, precision, certificate replay and claims. Finite/numeric evidence must not be promoted beyond its coverage unless a proved reduction transfers it.

## Conflict handling

If proof and counterexample evidence both appear valid, fail closed and open a conflict investigation. Common causes include statement drift, mismatched versions, illegal witnesses, vacuous assumptions, unsound encodings or stale receipts. Never choose the preferred conclusion by confidence score.

## Admission recommendation

Return one of:

- `reject`: identity mismatch, invalid evidence, false candidate or policy violation;
- `revise`: potentially useful candidate with explicit repairable obligations;
- `eligible_for_independent_admission_review`: all required capabilities appear present, but admission authority must still decide.

List the strongest justified outcome and every residual obligation. `eligible` is not `admitted`.

## Adversarial probes

- Can assumptions be inconsistent or impossible?
- Does the proof use the target as a hidden dependency?
- Does a definition bake in the conclusion?
- Are cases missing at zero, empty, disconnected, singular or infinite boundaries?
- Does an equivalence only have one proved direction?
- Is a tool version or theorem type different from the frozen record?
- Does a randomized/numeric result masquerade as universal proof?
- Is “independent” evidence produced by the same implementation?

## Output record

Include candidate identity, reviewed claim, capability matrix, receipt findings, independence assessment, statement-faithfulness matrix, conflicts, residual obligations, recommendation and reviewer boundary. Never write Evidence/Result/Solution truth records from this Skill.
