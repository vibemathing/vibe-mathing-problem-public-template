# CAPABILITY_LIBRARY

Each capability is operational. Provenance IDs point to the canonical source map. Engineering combinations across posts are **STRUCTURAL_SYNTHESIS**; source facts/methods remain **SOURCE_DERIVED**.

## task-router
- **Purpose:** Classify a formal-mathematics request before acting
- **Trigger:** formalization request is ambiguous or multi-stage
- **Required context / inputs:** goal, artifact, environment
- **Procedure:**
  1. Classify: statement/proof/API/project/teaching/AI-verification.
  2. Select the narrowest route that can succeed.
  3. Load the matching chapter/reference.
- **Failure condition:** A wrong route causes wasted proof search
- **Fallback:** Return the missing prerequisite or alternate route
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u013,u019,u050,u051,u093,u099,u117,u127

## type-first-disambiguation
- **Purpose:** Use types and structures to expose hidden assumptions
- **Trigger:** notation or informal prose is ambiguous
- **Required context / inputs:** objects, operations, expected types
- **Procedure:**
  1. State types for every object.
  2. Resolve overloaded notation and coercions.
  3. Check hypotheses implied by the chosen structures.
- **Failure condition:** Type mismatch or accidental stronger assumptions
- **Fallback:** Restate the theorem at a cleaner interface
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u024,u037,u089,u090,u094

## statement-semantics-audit
- **Purpose:** Verify that the formal theorem says what the human intends
- **Trigger:** before trusting any formal proof or AI translation
- **Required context / inputs:** informal statement, formal statement
- **Procedure:**
  1. Compare quantifiers in order.
  2. Check domains, nonempty/nonzero/positivity conditions.
  3. Check equality/equivalence notion.
  4. Test edge cases and trivializations.
- **Failure condition:** A compiling theorem is vacuous, stronger/weaker, or mistranslated
- **Fallback:** Reject or repair statement before proof
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u096,u111,u116,u121,u125,u126,u128,u132,u133

## proof-state-loop
- **Purpose:** Advance by one or two justified local steps while reading the goal state
- **Trigger:** proof is nontrivial but local progress is possible
- **Required context / inputs:** current goal/hypotheses
- **Procedure:**
  1. Inspect goal.
  2. Choose one structural step.
  3. Re-read transformed goal.
  4. Repeat; factor recurring steps into lemmas.
- **Failure condition:** Goal state drifts from intended mathematics
- **Fallback:** Backtrack to last meaningful state and simplify representation
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u017,u020,u023,u034,u054,u099,u111

## core-tactic-selection
- **Purpose:** Choose minimal proof constructors before automation
- **Trigger:** basic logical/algebraic proof
- **Required context / inputs:** goal shape
- **Procedure:**
  1. Use intro for implications/forall.
  2. Use exact/apply/refine for known implications.
  3. Use cases/split/left/right for logical constructors.
  4. Use induction on inductive structure.
  5. Use have for local intermediate facts.
- **Failure condition:** Tactic changes goal without conceptual progress
- **Fallback:** Return to goal shape and use explicit term/tactic
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u017,u020,u023,u039,u054,u100,u101,u108

## equality-layer-diagnosis
- **Purpose:** Identify which notion of sameness is blocking progress
- **Trigger:** rw/exact/change/refl or transport unexpectedly fails
- **Required context / inputs:** two expressions/objects
- **Procedure:**
  1. Check literal syntax.
  2. Check definitional equality.
  3. If theorem equality is needed, find/prove rewrite lemma.
  4. If object identity is too strong, use extensionality/isomorphism/transport with compatibility proofs.
- **Failure condition:** Treating canonical isomorphism as unrestricted equality
- **Fallback:** Use explicit bridge/naturality/commuting theorem
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u062,u063,u064,u091,u095,u109

## normalize-then-solve
- **Purpose:** Normalize a goal into a solver-friendly form
- **Trigger:** algebra/arithmetic tactic fails on a messy goal
- **Required context / inputs:** goal + hypotheses
- **Procedure:**
  1. Apply extensionality if structural equality.
  2. Rewrite/simp to canonical form.
  3. Then use ring/linarith/nlinarith/norm_num/search as appropriate.
  4. Inspect generated subgoals.
- **Failure condition:** Automation is asked to solve outside its domain
- **Fallback:** Manually bridge to the solver domain
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u043,u055,u056,u068,u091,u102

## simp-system-engineering
- **Purpose:** Build terminating canonical rewrite APIs
- **Trigger:** developing a reusable algebraic structure/library
- **Required context / inputs:** equations and target normal form
- **Procedure:**
  1. Choose an intended normal form.
  2. Orient simp lemmas toward it.
  3. Avoid mutually expanding rules.
  4. Test representative expressions and associativity/unit cases.
- **Failure condition:** simp loops, blows up, or normalizes unpredictably
- **Fallback:** Remove/reorient lemmas; keep some rewrites explicit
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u007,u040,u101

## inductive-eliminator-route
- **Purpose:** Use constructors and generated recursors systematically
- **Trigger:** data or proposition is inductively defined
- **Required context / inputs:** inductive definition
- **Procedure:**
  1. List constructors.
  2. For construction into the type, use constructors.
  3. For elimination out, use recursor/cases/induction.
  4. Use computational discriminators only when proposition proof needs data.
- **Failure condition:** Trying to prove constructor facts with unrelated automation
- **Fallback:** Expose recursor or define auxiliary data function
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u009,u027,u039,u108,u109,u110

## quotient-universal-property
- **Purpose:** Define maps out of quotients by invariance, not representative-picking
- **Trigger:** quotient/coset/well-definedness task
- **Required context / inputs:** X, equivalence r, candidate f:X→Y
- **Procedure:**
  1. Prove f is constant on r-classes.
  2. Use Quot.lift or domain-specific lift/map.
  3. Use quotient induction for properties of quotient elements.
  4. Avoid unfolding to sets of classes unless the theorem needs that model.
- **Failure condition:** Representative-dependent definition
- **Fallback:** Prove invariance or redesign target function
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u005,u106,u124

## definition-api-design
- **Purpose:** Treat each definition as the start of an interface
- **Trigger:** introducing new mathematical object in a library
- **Required context / inputs:** definition + intended use cases
- **Procedure:**
  1. Define at useful generality.
  2. Add constructors/destructors/extensionality.
  3. Add coercions and instances.
  4. Add simp/interface theorems.
  5. Test downstream examples immediately.
- **Failure condition:** Every proof unfolds implementation details
- **Fallback:** Add missing API or revise representation
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u030,u048,u078,u080,u085,u091,u098,u132

## specification-implementation-separation
- **Purpose:** Keep the mathematical interface stable across concrete models
- **Trigger:** multiple representations or future refactoring likely
- **Required context / inputs:** specification + implementations
- **Procedure:**
  1. State the abstract properties/typeclass/universal property.
  2. Prove each implementation satisfies them.
  3. Prove conversion/equivalence and operation compatibility.
  4. Prove client theorems against the interface where practical.
- **Failure condition:** Client proof depends on constructor/layout details
- **Fallback:** Move dependency behind an interface lemma
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u062,u064,u090,u091,u095,u124

## proof-vs-compute-representation
- **Purpose:** Separate proof-friendly and computation-friendly representations
- **Trigger:** same object needs induction/proofs and large computation
- **Required context / inputs:** representations + conversion
- **Procedure:**
  1. Use the representation natural for each task.
  2. Prove round-trip/equivalence.
  3. Prove operations commute with conversion.
  4. Transfer theorems/results across bridge.
- **Failure condition:** Forcing huge computation through unary/proof-oriented data
- **Fallback:** Compute externally/efficiently and certify result
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u009,u058,u066,u068,u090

## prop-to-data-boundary
- **Purpose:** Recognize when existence in Prop cannot supply data computationally
- **Trigger:** need an explicit witness/dimension/inverse from an existence proof
- **Required context / inputs:** existence theorem + desired data
- **Procedure:**
  1. Decide whether noncomputable choice is acceptable.
  2. If yes, isolate the choice and prove independence.
  3. If computation matters, require constructive data/interface.
  4. Track subsingleton/propositional equality issues.
- **Failure condition:** Assuming uniqueness/existence makes a canonical executable object
- **Fallback:** Use choice explicitly or strengthen input to data
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u065,u066,u110

## domain-contract-totalization
- **Purpose:** Keep mathematical domain conditions in theorem contracts
- **Trigger:** operation is totalized outside its natural domain
- **Required context / inputs:** operation + theorem
- **Procedure:**
  1. Identify junk/edge inputs.
  2. State nonzero/nonnegative/nonempty hypotheses where theorem needs them.
  3. Do not infer semantics from the chosen junk value.
- **Failure condition:** A theorem appears false only at out-of-domain inputs
- **Fallback:** Add/derive the intended precondition
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u090,u092

## library-search-and-version-drift
- **Purpose:** Find current library API and separate conceptual guidance from historical syntax
- **Trigger:** using old blog code or unknown theorem names
- **Required context / inputs:** concept + current environment
- **Procedure:**
  1. Search/check names before coding.
  2. Inspect current type signature/source.
  3. Prefer current mathlib interfaces.
  4. Label old Lean 3 syntax as historical.
- **Failure condition:** Copying dated install commands/API verbatim
- **Fallback:** Translate concept to current API and recompile
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u011,u012,u014,u016,u031,u033,u054,u118,u119,u120

## coercion-typeclass-debug
- **Purpose:** Diagnose invisible maps and inferred structures
- **Trigger:** Lean chooses/wants unexpected type or instance
- **Required context / inputs:** expression + inferred types
- **Procedure:**
  1. Print/check inferred types and instances.
  2. Make one coercion/instance explicit.
  3. Find canonical map already provided by API.
  4. If repeated friction occurs, improve local library interface.
- **Failure condition:** Patch proofs with many ad hoc casts
- **Fallback:** Create/reuse a systematic coercion/instance/transport lemma
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u024,u085,u098,u100,u101

## reflection-trust-chain
- **Purpose:** Use powerful automation while preserving a small trust base
- **Trigger:** domain solver or external automation is appropriate
- **Required context / inputs:** formal goal
- **Procedure:**
  1. Let tactic compute/search.
  2. Require it to emit/check a proof term or certificate.
  3. Trust the kernel, not the tactic implementation.
  4. For external code, isolate parsing/translation boundary.
- **Failure condition:** Confusing successful heuristic output with verified theorem
- **Fallback:** Recheck proof/certificate in independent kernel/type checker when valuable
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u043,u058,u068,u077,u111,u119

## filter-abstraction
- **Purpose:** Route limit/continuity problems through filters when compositionality matters
- **Trigger:** many variants of convergence/continuity or map/preimage reasoning
- **Required context / inputs:** sets/functions/topology
- **Procedure:**
  1. Model sets as principal filters for intuition.
  2. Use map/comap and their Galois connection.
  3. Express convergence as Tendsto.
  4. Unfold to sets only for local semantic checks.
- **Failure condition:** Abstract proof becomes opaque or API unavailable
- **Fallback:** Prove a concrete lemma then lift back to filter API
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u047,u048,u102,u103,u104,u105

## generality-linter
- **Purpose:** Prove at the broadest useful assumptions while keeping ergonomic wrappers
- **Trigger:** theorem uses stronger structure than proof needs
- **Required context / inputs:** proof + typeclass assumptions
- **Procedure:**
  1. Inspect which assumptions are actually used.
  2. Generalize where it increases reuse.
  3. Keep user-facing specializations if inference/readability improves.
- **Failure condition:** Generalization creates unreadable interfaces or fragile inference
- **Fallback:** Retain a specialized theorem delegating to general core
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u030,u078,u098,u101

## research-blueprint
- **Purpose:** Build and maintain a dependency graph for large formalizations
- **Trigger:** target spans many theories/people
- **Required context / inputs:** target theorem + library inventory
- **Procedure:**
  1. State target first.
  2. List definitions and lemmas needed.
  3. Mark nodes done/ready/blocked.
  4. Assign parallel workstreams.
  5. Keep human blueprint cross-linked to code.
- **Failure condition:** Blueprint diverges from code or becomes gatekeeping overhead
- **Fallback:** Update blueprint from completed Lean work; allow code-first local digestion
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u061,u071,u079,u096,u099,u111,u117,u120,u121

## target-driven-library-growth
- **Purpose:** Use a real target to decide which infrastructure deserves investment
- **Trigger:** library can grow in many directions
- **Required context / inputs:** research target + missing prereqs
- **Procedure:**
  1. Choose target.
  2. Trace missing definitions/theorems.
  3. Promote generally useful pieces into shared library.
  4. Test them immediately in target proof.
- **Failure condition:** Building broad theory with no demonstrated usability
- **Fallback:** Return to a concrete target or representative client theorem
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u069,u078,u096,u111,u117,u120,u129,u132

## statement-first-milestone
- **Purpose:** Treat formal statement as an independent research milestone
- **Trigger:** full proof too distant
- **Required context / inputs:** informal theorem + definitions
- **Procedure:**
  1. Check all objects can be defined.
  2. Formalize statement idiomatically.
  3. Validate semantics with experts/examples.
  4. Only then estimate proof project.
- **Failure condition:** Proof planning before theorem can even be stated
- **Fallback:** Prioritize missing definitions and statement API
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u071,u079,u098,u119,u127,u132

## staged-assumptions
- **Purpose:** Use temporary assumptions only as tracked scaffolding
- **Trigger:** large project blocked by unavailable theorem
- **Required context / inputs:** blocked node
- **Procedure:**
  1. Introduce the weakest explicit assumption/sorry.
  2. Record provenance and dependency.
  3. Continue downstream work.
  4. Schedule discharge/replacement.
  5. Audit no placeholders before release.
- **Failure condition:** False/too-strong axiom silently trivializes work
- **Fallback:** Test whether downstream proof needs weaker true statement; repair and discharge
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u044,u061,u096,u115,u120

## mathematical-typo-repair
- **Purpose:** Distinguish repairable presentation errors from structural proof failures
- **Trigger:** formalization conflicts with literature
- **Required context / inputs:** paper statement/proof + failing formal goal
- **Procedure:**
  1. Localize exact failed step.
  2. Check omitted hypotheses, quotient minima, inequalities, quantifier order.
  3. Ask author/domain expert when intent is unclear.
  4. Repair with minimal change preserving argument.
- **Failure condition:** Assuming famous literature must be literally correct
- **Fallback:** Search alternate references/proofs; record correction
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u096,u111,u119,u121,u128,u132

## teaching-by-familiar-math
- **Purpose:** Teach formalization using mathematics the learner already knows
- **Trigger:** onboarding mathematicians
- **Required context / inputs:** learner level + familiar topic
- **Procedure:**
  1. Start with logic/easy familiar examples.
  2. Expose goal state live.
  3. Add tactics gradually.
  4. Move to open projects after basic fluency.
  5. Encourage help-seeking and reflection on failed plans.
- **Failure condition:** Teaching new advanced math and proof assistant simultaneously
- **Fallback:** Reduce mathematical novelty or formal complexity
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u015,u021,u034,u051,u054,u060,u093,u097,u100-u107,u112-u115

## community-debugging
- **Purpose:** Turn a stuck proof into a useful collaborative question
- **Trigger:** local attempts stall
- **Required context / inputs:** minimal example, imports, exact error
- **Procedure:**
  1. Minimize reproducer.
  2. Share exact goal/error and imports.
  3. State intended mathematics.
  4. Integrate answer into reusable API if broadly useful.
- **Failure condition:** Vague screenshots or missing environment make help nonreproducible
- **Fallback:** Produce a fresh minimal file and retry
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u034,u086,u093,u097,u111,u112,u115

## ai-statement-definition-audit
- **Purpose:** Treat AI-generated formal statements and definitions as untrusted semantics
- **Trigger:** AI autoformalizes prose or library definitions
- **Required context / inputs:** human source + generated Lean
- **Procedure:**
  1. Check quantifier order and hypotheses.
  2. Check standard examples/nonexamples.
  3. Compare with trusted reference definition or characterization theorems.
  4. Review generality/API quality before upstreaming.
- **Failure condition:** Code compiles but formalizes the wrong concept
- **Fallback:** Reject, repair, and add semantic tests
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u116,u121,u125,u127,u128,u129,u130,u131,u132,u133

## ai-proof-verification
- **Purpose:** Use proof assistants as a verifier for untrusted AI proof generation
- **Trigger:** AI proposes a proof
- **Required context / inputs:** formal statement + proof code
- **Procedure:**
  1. Ensure statement already passed semantic audit.
  2. Compile proof in controlled environment.
  3. Inspect axioms/dependencies if trust matters.
  4. Independently type-check/certificate-check for high stakes.
- **Failure condition:** Human-readable prose looks plausible but has one fatal hallucination
- **Fallback:** Request formal proof or return insufficiently verified
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u122,u125,u126,u127,u128,u131,u133

## counterexample-first
- **Purpose:** Search for witnesses against universal conjectures when exploration favors construction
- **Trigger:** goal is forall/necessity claim or old conjecture with computable structure
- **Required context / inputs:** formalized conjecture + search tools
- **Procedure:**
  1. Formalize negation/witness contract.
  2. Search computationally/with AI.
  3. Verify candidate independently in Lean.
  4. Then simplify and explain why it works.
- **Failure condition:** Candidate exploits mistranslated conjecture or degenerate case
- **Fallback:** Re-audit statement and intended scope; retain only genuine counterexample
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u128,u131

## machine-proof-digestion
- **Purpose:** Convert a verified machine artifact into human mathematical insight
- **Trigger:** proof/counterexample is correct but opaque/huge
- **Required context / inputs:** verified Lean + domain expertise
- **Procedure:**
  1. Identify theorem spine and small set of nontrivial lemmas.
  2. Replace accidental constants/representations with conceptual invariants.
  3. Find shortest mechanism behind witness.
  4. Write human exposition cross-linked to formal code.
- **Failure condition:** Equating formal correctness with understanding
- **Fallback:** Maintain certificate and exposition as separate linked deliverables
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u111,u132,u133

## benchmark-integrity
- **Purpose:** Design AI math evaluations that measure reasoning, not answer guessing
- **Trigger:** creating/evaluating AI benchmark
- **Required context / inputs:** tasks + verifier
- **Procedure:**
  1. Separate discovery from verification.
  2. Prefer formal proof when possible.
  3. If answers are numbers, test reasoning and leakage resistance.
  4. Use fixed rules, reproducibility, and official grading.
  5. Avoid best-of-many cherry-picking without selection mechanism.
- **Failure condition:** Correct final number hides invalid reasoning
- **Fallback:** Require certificate/proof or robust adjudication
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u122,u123,u125,u126,u127

## gold-standard-library-definition
- **Purpose:** Elevate definitions from merely correct to maintainable shared infrastructure
- **Trigger:** definition intended for mathlib/core library
- **Required context / inputs:** concept + many downstream uses
- **Procedure:**
  1. Choose right generality.
  2. Align with hierarchy/coercions.
  3. Supply API and characteristic theorems.
  4. Review by domain + Lean experts.
  5. Benchmark downstream ergonomics.
- **Failure condition:** AI generates isolated technically-correct definition with technical debt
- **Fallback:** Keep in project-local layer until refactored/reviewed
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u127,u129,u130,u132,u133

## autoformalization-suitability
- **Purpose:** Decide which project parts are ready for autoformalization
- **Trigger:** large mixed formalization project
- **Required context / inputs:** dependency graph + library state
- **Procedure:**
  1. Partition tasks: definitions missing; statements; proofs with mature APIs; exploration.
  2. Use AI aggressively where interfaces already exist and literature is explicit.
  3. Keep experts on new definitions/ambiguous statements.
  4. Measure failure modes and feed them back into tooling.
- **Failure condition:** Generalizing from cherry-picked easy targets
- **Fallback:** Test on fixed target-first workload
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u130,u131,u132,u133

## formal-code-security-audit
- **Purpose:** Treat proof-assistant files as executable code when verifying external output
- **Trigger:** large third-party/generated Lean repository
- **Required context / inputs:** repo + build environment
- **Procedure:**
  1. Inspect non-theorem/definition commands and custom tactics.
  2. Build in sandbox/controlled environment.
  3. Check Lean version/trust base.
  4. Inspect axioms and suspicious escape hatches.
  5. Optionally verify with independent checker.
- **Failure condition:** Assuming “Lean file” cannot execute side effects or exploit soundness bugs
- **Fallback:** Isolate build; audit custom code; use known-good toolchain
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** u119,u131,u133

## release-self-check
- **Purpose:** Audit route, prerequisites, exceptions, meaning, and completeness before returning
- **Trigger:** any nontrivial formalization output
- **Required context / inputs:** result + method trace
- **Procedure:**
  1. Reconfirm user goal and theorem statement.
  2. Check method preconditions.
  3. Check missing inputs/hypotheses.
  4. Check equality/generalization/edge cases.
  5. Check no sorries/false axioms.
  6. Check semantic statement match and version-sensitive claims.
- **Failure condition:** Passing compilation used as sole quality criterion
- **Fallback:** Run semantic + structural + trust audits
- **Validation:** confirm the transformed goal/output matches the intended mathematics and the method prerequisites.
- **Provenance:** cross-cutting: u062-u068,u091-u099,u111,u121-u133
