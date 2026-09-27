# Patterns

## 1. Produce → Share → Verify → Trust
**When:** any new mathematical claim emerges.  
**How:** private scratch → typed global finding with evidence → worker submission → verifier acceptance → fact graph.  
**Trade-off:** slower than social consensus, much stronger provenance and error containment.

## 2. Truth/awareness split
**When:** coordinating many agents.  
**How:** use global memory to know what others tried; use only fact ids as established premises.  
**Failure avoided:** attractive unverified claims silently becoming proof dependencies.

## 3. Counterexample-before-grind
**When:** a subgoal resists direct proof.  
**How:** actively try to preserve assumptions and break the conclusion before spending more proof effort.  
**Trade-off:** may add early work; often exposes false or over-strong lemmas quickly.

## 4. Two-attempt escalation
**When:** no counterexample found and the same subgoal remains blocked.  
**How:** after at least two genuine direct attempts, record obstacle/dead end and replan.  
**Failure avoided:** indefinite local grinding.

## 5. Portfolio control beat
**When:** active unsolved project.  
**How:** about every 30 minutes, inspect goal, facts, findings, workers, all live/parked routes; make explicit continue/redirect decisions.  
**Trade-off:** coordination overhead in exchange for less tunnel vision.

## 6. Macro route audit
**When:** long-running project.  
**How:** about every four hours compare routes, frontiers, obstacles, evidence, allocation, and revisit conditions.  
**Failure avoided:** recent-context bias erasing older credible strategies.

## 7. Interface contract diagnosis
**When:** a multi-step proof architecture feels “almost closed.”  
**How:** state exact input required by next step, exact output guaranteed by current theorem, matched facts, missing hypotheses, and concrete downstream breakage.  
**Failure avoided:** calling a conditional package closed before hypotheses are matched.

## 8. Proof-migration analysis
**When:** literature theorem is close but has extra assumptions.  
**How:** identify where each extra assumption is used, then adapt mechanism or isolate the missing bridge.  
**Trade-off:** deeper reading; avoids black-box theorem chasing.

## 9. Verify-before-depend
**When:** an intermediate result will support later subgoals.  
**How:** package it self-contained and verify before composing downstream proof.  
**Failure avoided:** large proof tree collapsing around a false intermediate lemma.

## 10. Cascade-aware revocation
**When:** a stored fact is discovered wrong.  
**How:** revoke it and descendants; rebuild from surviving facts or new proof.  
**Failure avoided:** stale dependent conclusions surviving a broken premise.

## 11. Explicit paper target
**When:** moving from research to publication.  
**How:** operator selects/finalizes headline fact(s); unset target blocks writer.  
**Failure avoided:** manuscript centered on a heuristic terminal node.

## 12. Curate before render
**When:** target closure is nontrivial, especially ≥10 facts.  
**How:** inspect statements-only subgraph, choose support layer, pass only selected full proofs to writer. Recurse for deep sub-results.  
**Trade-off:** main agent must understand the proof shape; output is shorter and more coherent.

## 13. Offline audit → online verify
**When:** bibliography contains uncertain entries.  
**How:** offline auditor creates worklist without promoting from memory; networked verifier checks authoritative sources and records exact source.  
**Failure avoided:** plausible bibliographic hallucination.

## 14. Quarantine on unsafe authoring failure
**When:** generated report/paper leaks identifiers, collapses, or fails compile.  
**How:** keep the last good artifact, write suspect output to quarantine path, return non-ok status.  
**Trade-off:** fewer “successful” artifacts, stronger delivery integrity.

## 15. Whole-document re-verification
**When:** fact-graph mathematics has been rewritten into prose.  
**How:** verify the paper as written; precise confirmed citations are givens; classify omissions as ignorable or must-fix.  
**Failure avoided:** correct source facts becoming an invalid manuscript through editorial seams.

## Anti-patterns

- **Fact spam:** splitting routine calculations into many verified nodes to simulate progress.
- **Shared-memory theorem:** treating a global-memory entry as proof because several agents agree.
- **Closed-too-early:** marking an interface closed with unmatched hypotheses.
- **Terminal-fact guessing:** letting the writer infer paper target from graph shape.
- **Full-closure dump:** passing dozens/hundreds of fact bodies to one writer call.
- **Citation-by-memory:** filling author/title/year because they sound familiar.
- **Status theater:** storing new guidance that changes no strategic decision.
- **Silent partial artifact:** overwriting the clean deliverable with a leaky, broken, truncated, or uncompilable generation.
