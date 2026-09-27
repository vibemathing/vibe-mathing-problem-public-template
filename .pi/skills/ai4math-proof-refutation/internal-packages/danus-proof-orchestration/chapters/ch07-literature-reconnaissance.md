# 07 — Literature Reconnaissance and Proof Transfer

## Why literature search is strategic

Danus treats literature as a mechanism source and a hypothesis map. Search is most useful when it can change a proof route, resolve a theorem-level blocker, or reveal a known obstruction. Search results remain unverified awareness until their mathematical use is checked.

## When to search

Search aggressively when:

- entering a new mature area with known technique families;
- a central obstruction appears;
- a current theorem resembles a known result whose proof may transfer;
- a route needs a specific bridge theorem;
- repeated proof attempts suggest a missing established tool;
- a counterexample family or negative result may kill the route early.

Delay broad search when a problem is fresh and immediate structural consequences have not yet been extracted. Otherwise search can anchor the program prematurely on a nearby theorem.

## Search modes

Useful modes include:

- **repair:** find machinery that addresses a concrete failed step;
- **mutation:** find variants that alter one hypothesis or construction;
- **analogy:** look for the same mechanism in a neighboring setting;
- **program shift:** search for a different architecture after route failure;
- **theorem-level blocker:** locate a precise known result needed at an interface.

## Procedure

1. Phrase the mathematical need as a complete statement where possible.
2. Search multiple formulations, synonyms, and technique names.
3. Capture title, source identifier, exact theorem/definition, and cited purpose.
4. Read the actual paper/source before relying on a result.
5. Expand the paper's definitions and ambient assumptions.
6. Compare those definitions with the current project.
7. Study how the proof uses each extra hypothesis.
8. Classify the relationship:
   - direct applicable theorem;
   - adaptable proof mechanism;
   - partial result with missing interface;
   - near-miss with incompatible definitions;
   - negative/obstruction evidence.
9. Store a concise, source-identified global-memory note.
10. If the result will support a proof, cite it precisely in the candidate and let verification check applicability.

## Proof migration over black-box citation

A partial external theorem can still be valuable when its assumptions fail. Ask:

- Which proof step uses the extra assumption?
- Does our object have a weaker substitute?
- Can that step be replaced by a project-specific argument?
- Does the failure expose the true bridge lemma?
- Is the theorem's construction itself reusable?

This often yields a better plan than trying only to prove that the current object fits the published theorem unchanged.

## Failure modes

- search before understanding the local statement;
- keep only titles/abstracts and forget exact theorem hypotheses;
- equate shared terminology across papers without checking definitions;
- treat a semantically similar theorem as a verified citation;
- store search output as if it were a fact;
- keep searching after the relevant literature space is mature and no new interface is emerging;
- cite a paper from model memory without source verification.

## Verification handoff

The candidate verifier checks external theorem statements and contextual applicability. The paper pipeline separately verifies bibliography metadata. Keep these jobs distinct: theorem correctness/application and bibliographic identity are related, yet each has its own failure mode.

## Output standard for a literature note

A useful note says: exact result, source, definitions that matter, proof mechanism, assumptions, fit to current project, limitation, and what next experiment/lemma would discriminate whether transfer works.
