# Patterns

## Three-Capability Triage
**When to use**: At the start of an AI4M request or project.

**How**:
1. State the mathematical objective.
2. Mark the dominant bottleneck: knowledge navigation, proof/verification, insight/connection.
3. Mark secondary bottlenecks.
4. Choose the smallest method that addresses the dominant one.

**Trade-offs**: One project may span all three; forcing a single category can hide dependencies.

**Failure / fallback**: If the category remains unclear, ask what activity consumes the most research time and what output would count as progress.

**Validation**: The chosen method must map directly to a bottleneck and a measurable or inspectable output.

## Special-Purpose Discovery Loop
**When to use**: A narrow mathematical subproblem has computable/curatable data and requires pattern discovery.

**How**: bottleneck → data representation → data generation → model choice → train/evaluate → mathematical interpretation → conjecture/structure → mathematical tests.

**Trade-offs**: High potential for surprising structure; sensitive to data artifacts and feature choices.

**Failure / fallback**: If the signal has no mathematical reading, inspect confounders or redesign the representation before forming a conjecture.

**Validation**: A useful output survives mathematical interpretation and independent tests; predictive performance alone is insufficient.

## Formalization Stack
**When to use**: Correctness guarantees, formal benchmarks, reusable formal reasoning, or verifier feedback are important.

**How**: informal math → Lean definitions/statement → mathlib search → assisted formalization → proof search/completion → checker.

**Trade-offs**: Strong rigor and feedback; initial formalization and library navigation cost can be high.

**Failure / fallback**: Search the library semantically; reuse existing abstractions; split the theorem; repair definitions and assumptions manually.

**Validation**: Check both semantic fidelity of the formal statement and checker acceptance of the proof.

## Library-First Lean Workflow
**When to use**: Lean progress stalls because a needed lemma, definition, or API cannot be found.

**How**: describe mathematical intent → semantic search → inspect candidate types/assumptions → adapt the goal to library abstractions → only then generate a new proof.

**Trade-offs**: Reduces duplicate proof work; search can return superficially related facts.

**Failure / fallback**: Search by related concepts or definitions, inspect neighboring files, then prove a minimal bridge lemma.

**Validation**: The selected lemma type-checks in the target context and matches the intended mathematics.

## Autoformalization with Semantic Audit
**When to use**: Translating informal statements/proofs into Lean is the bottleneck.

**How**: generate candidate formalization → type-check → compare assumptions/conclusion with source → repair → prove/check.

**Trade-offs**: Speeds translation; can silently formalize a weaker, stronger, or different theorem.

**Failure / fallback**: Formalize definitions and statement manually, then use AI only for local proof fragments.

**Validation**: A mathematician can map each informal assumption and conclusion to the formal artifact.

## Verifier Feedback Loop
**When to use**: Candidate outputs are cheaply machine-checkable.

**How**: candidate → verifier → structured error/success → revision/search → verifier, with bounded retries and explicit stop criteria.

**Trade-offs**: Precise feedback enables reliable iteration; only properties represented by the verifier are guaranteed.

**Failure / fallback**: If errors are too opaque, reduce to smaller lemmas or add intermediate checks.

**Validation**: Final correctness claims correspond exactly to properties the checker verified.

## Agent-First Prototype
**When to use**: A strong base model can solve local steps and the overall task requires multi-step orchestration.

**How**: decompose → assign tools/retrieval → expose intermediate artifacts → attach evaluators/verifiers → iterate → stop on success/limit.

**Trade-offs**: Fast to prototype and flexible; can loop or compound small errors.

**Failure / fallback**: Reduce task scope, strengthen evaluators, formalize critical steps, or replace a weak agent stage with a specialized tool.

**Validation**: Every critical transition has an observable intermediate result and a check.

## Evolve-Style Improvement
**When to use**: The goal is quantitatively evaluable and a viable initial candidate exists.

**How**: seed → mutate/generate alternatives → score under constraints → select → iterate → periodically audit the evaluator.

**Trade-offs**: Can discover unexpected improvements; can aggressively exploit scoring defects.

**Failure / fallback**: Redesign the score/constraints or create a stronger seed before further search.

**Validation**: Evaluate top candidates with an independent mathematical check or secondary metric.

## Understanding Extraction
**When to use**: A proof has been generated/verified or automation has solved the mechanical layer.

**How**: identify decisive lemmas/invariants → explain mechanism → test weakened assumptions → connect to related results → propose generalizations/questions.

**Trade-offs**: Adds interpretive work after success; converts one-off proof artifacts into reusable knowledge.

**Failure / fallback**: If no explanation emerges, simplify the proof, compare alternate proofs, or inspect dependency structure.

**Validation**: The explanation predicts what changes when assumptions or constructions change and stays anchored to the checked proof.
