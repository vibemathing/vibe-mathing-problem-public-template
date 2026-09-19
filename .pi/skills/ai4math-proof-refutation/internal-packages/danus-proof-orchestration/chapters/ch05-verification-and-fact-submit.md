# 05 — Verification and `fact_submit`

## Verification is the write gate

A worker submits a candidate statement and proof. The gateway performs deterministic prechecks, cold-starts a verifier, and writes the fact only if the verifier returns `correct`. Every verdict is also recorded as a global-memory verification trace so rejection knowledge survives while the verifier itself remains stateless.

## Candidate preparation

Before submission:

1. Make the statement self-contained and precise.
2. Define every non-global symbol or introduce it through the fact glossary.
3. Cite predecessor facts by real fact id when the proof uses established internal results.
4. Include external references with exact statement/application information when needed.
5. Write the proof in ordinary sequential mathematical order.
6. Remove hand-waving, hidden conditional assumptions, and source claims that come only from the problem prompt.

## Deterministic prechecks

The service rejects vacuous statements/proofs and enforces several hard prohibition categories before the LLM verifier runs.

### P1 — problem description used as mathematical source

The problem file describes the target and hypotheses; it does not certify derived premises. Replace substantive “the problem says this reduction holds” reasoning with a verified predecessor fact or a properly checked external result.

### P3 — unproved conditional narrowing

A proof cannot assume that prior reductions have placed the object in a special residual case without citing the signed fact that proves that narrowing in the relevant paragraph.

### P5 — vague classical-result gestures

Phrases such as “by a standard/classical argument” do not establish a load-bearing step. Supply a real predecessor fact, a precise external theorem and hypotheses, or the derivation itself.

## Verifier workflow

The fresh verifier:

1. reads the candidate statement and assumptions;
2. checks proof items sequentially in textual order;
3. records every logical error, theorem misuse, missing assumption, unjustified jump, and gap;
4. inspects referenced fact statements when fact ids are cited;
5. checks external theorem statements through theorem search and, when needed, web retrieval;
6. compares definitions and applicability, not merely theorem titles;
7. returns `correct` iff there are zero critical errors and zero gaps;
8. returns concrete repair hints on rejection.

The final result is persisted to the verifier run's JSON result file; the gateway consumes that verdict.

## Repair loop

When the verdict is `wrong`:

- read every critical error and gap;
- distinguish a false claim from an incomplete proof;
- repair the proof or adjust the statement honestly;
- if a predecessor/application is wrong, replace or re-prove that dependency;
- if an external theorem was misapplied, align definitions/hypotheses or abandon that transfer;
- resubmit only after all major issues are addressed.

Do not repeatedly resubmit cosmetic rewrites against an unchanged mathematical gap.

## Acceptance semantics

On `correct`, the gateway attempts to write the content-addressed fact. If the graph write fails, the verification trace still records the verifier outcome and write error; no fact id means downstream work must not treat the claim as stored truth.

On verifier service failure, submission returns an error and writes no verdict/fact. Restore the service rather than creating an alternate truth path.

## External references

Reference checking has two levels:

- candidate proof verification checks whether the cited external result exists and applies;
- the paper pipeline later audits and verifies bibliographic metadata independently.

External reference metadata is not part of the fact hash, so correcting the bibliography does not invalidate mathematical identity.

## Limits

The verifier is an LLM operating under strict contracts and cold starts. It improves independence from producer agents, yet it is not formal verification. For consequential mathematics, retain human review and, when appropriate, independent formal checking outside the Danus trust claim.

## Submission self-check

- Statement/proof non-vacuous?
- Every symbol defined?
- Every internal dependency a live fact id?
- No global-memory claim masquerading as a fact?
- No hidden “assume reductions already did X” premise?
- External definitions and theorem hypotheses matched?
- Every non-routine load-bearing step derived or cited precisely?
- On rejection, have all verifier findings been addressed?


## Insufficient evidence

If the candidate, predecessor facts, or reference evidence is insufficient to judge the claim, return an insufficient-evidence result with the missing item and next check. Never convert uncertainty into acceptance.
