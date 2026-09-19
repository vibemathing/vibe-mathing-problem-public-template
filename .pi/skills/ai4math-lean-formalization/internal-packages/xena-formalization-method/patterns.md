# Operational Patterns

## Pattern: Statement Before Search
**When to use:** Any nontrivial formalization, especially AI-translated mathematics.  
**How:** Freeze types, binders, hypotheses, equality notion, and edge conditions; test examples; then search/prove.  
**Trade-offs:** Slower first five minutes, dramatically lower risk of proving the wrong theorem.

## Pattern: Goal-State Microsteps
**When to use:** The proof route is not globally obvious.  
**How:** Read goal → make one structural move → inspect new goal → repeat; factor recurring local moves into lemmas.  
**Trade-offs:** Verbose early proof, better diagnostics and later compression.

## Pattern: Normalize Then Solve
**When to use:** Algebraic/arithmetic automation fails on a mathematically routine goal.  
**How:** extensionality if needed → rewrite/simp toward canonical form → expose hypotheses → call the domain solver.  
**Trade-offs:** Requires choosing/maintaining a good normal form.

## Pattern: Equality Layer Probe
**When to use:** `rw`, `rfl`, `exact`, casts, or transports behave unexpectedly.  
**How:** test syntax → definitional equality → propositional equality → extensionality → isomorphism/compatibility.  
**Trade-offs:** More explicit bridges, less dependence on fragile implementation reduction.

## Pattern: Universal-Property First
**When to use:** Quotients, tensors, localizations, completions, free/generated objects.  
**How:** identify the map/characterization promised by the universal property; prove invariance/compatibility; use the library lift/map.  
**Trade-offs:** Abstract API may not expose element-level facts; keep an explicit model available when needed.

## Pattern: Dual Representation
**When to use:** One model proves well but computes poorly, or a universal model hides a special property.  
**How:** maintain two representations; prove conversions/equivalence and operation compatibility; transfer results.  
**Trade-offs:** More bridge theorems, much cleaner downstream tasks.

## Pattern: Definition + API as One Unit
**When to use:** Adding reusable mathematical infrastructure.  
**How:** definition → constructors/eliminators → extensionality → coercions/instances → simp/interface theorems → representative client proofs.  
**Trade-offs:** More work before “feature complete,” lower long-term proof friction.

## Pattern: Target-Driven Library Growth
**When to use:** Large research project needs substantial missing theory.  
**How:** choose target → trace blockers → build the reusable minimum → test in target → upstream/maintain.  
**Trade-offs:** Architecture is influenced by one target; review generality before upstreaming.

## Pattern: Tracked Temporary Assumption
**When to use:** Architecture can proceed while one hard theorem is unavailable.  
**How:** state the weakest explicit assumption; record dependents and provenance; continue; later replace and retest everything downstream.  
**Trade-offs:** Enables parallelism; dangerous if placeholders are forgotten or false.

## Pattern: Literature Failure Triage
**When to use:** Lean rejects a published argument.  
**How:** localize exact step → check missing hypotheses/quantifiers/minimum-vs-infimum/edge cases → consult alternate reference/expert → minimally repair.  
**Trade-offs:** Some “obvious” steps expand substantially; the repair becomes valuable documentation.

## Pattern: AI Artifact Routing
**When to use:** LLM/agent output participates in mathematics.  
**How:** prose = untrusted; statement/definition = semantic audit; proof = compile after statement audit; generated repo = security + trust audit.  
**Trade-offs:** Human effort concentrates on semantics and architecture rather than line-by-line proof checking.

## Pattern: Counterexample First
**When to use:** A universal conjecture has computable/constructive structure and witness search is plausible.  
**How:** formalize negation → search candidates → formally verify → rule out mistranslation/degenerate loopholes → digest mechanism.  
**Trade-offs:** Excellent for refutation; provides little evidence toward proving a true universal statement.

## Pattern: Certificate + Exposition
**When to use:** A machine-generated proof/counterexample is correct but unreadable.  
**How:** retain the formal certificate; separately identify theorem spine, key lemmas, conceptual mechanism, and human narrative; cross-link them.  
**Trade-offs:** Duplicates presentation work, preserves both assurance and understanding.

## Pattern: Familiar-Math Onboarding
**When to use:** Teaching mathematicians Lean/formal proof.  
**How:** familiar logic/arithmetic → small tactics → known undergraduate theorems → library search → open project; encourage collaboration and visible debugging.  
**Trade-offs:** Delays exposure to glamorous advanced formalizations; improves actual fluency.

## Pattern: Version-Drift Translation
**When to use:** Source/example was written in Lean 3 or old mathlib.  
**How:** preserve mathematical intent → identify current toolchain → search current API → rewrite minimal example → compile.  
**Trade-offs:** Exact historical code may be lost; contemporary correctness improves.

## Pattern: Semantic Stop
**When to use:** Required meaning cannot be verified.  
**How:** return “insufficient to determine,” identify the unresolved statement/definition/dependency, and specify what evidence would unblock the task.  
**Trade-offs:** Produces no fake success; may require domain-expert input.
