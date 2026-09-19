# CONCEPT_GRAPH

```text
user mathematical intent
  -> precise types / domains / quantifiers
      -> formal statement
          -> statement-semantics audit
          -> proof task
              -> explicit proof state
                  -> equality diagnosis
                  -> induction / cases / apply / exact
                  -> normalization
                      -> simp / rewrite
                      -> domain automation (ring, linarith, nlinarith, norm_num, search)
                          -> kernel-checked proof term

formal statement
  -> definitions
      -> representation choice
          -> specification / universal property
          -> concrete implementation
          -> bridge theorem / equivalence
      -> API layer
          -> constructors / eliminators
          -> extensionality
          -> simp/canonicalization lemmas
          -> coercions / typeclasses
          -> domain preconditions

research target
  -> dependency blueprint
      -> existing mathlib
      -> missing reusable infrastructure
      -> temporary assumptions / sorries (tracked)
      -> core delicate lemma
      -> discharge assumptions
      -> human-readable documentation

AI-generated mathematics
  -> assumptions/quantifiers audit
  -> statement/definition semantic audit
  -> proof checker
      -> accept formal derivation only if compiled
  -> counterexample route for universal claims
  -> human digestion / explanation
```

## High-value concept relationships

- **Types ↔ hidden assumptions**: type checking exposes category mistakes and silently omitted structure.
- **Definitional equality → tactic behavior**: `rfl`, `change`, `exact`, `rw`, and `convert` react differently to syntax versus definitional/propositional equality.
- **Universal properties ↔ API stability**: maps *out of* quotients/tensors/localisations are often best defined by eliminators/lifts; element-level properties can still require explicit models.
- **Representation ↔ proof/computation trade-off**: proof-friendly and compute-friendly forms may differ; bridge them with proved conversions rather than forcing one representation to do both jobs.
- **Prop ↔ data boundary**: existence/uniqueness in `Prop` does not automatically provide executable data; choice can cross the boundary at the cost of computation.
- **Automation ↔ trusted kernel**: tactics may be heuristic or buggy; the trusted result is the proof term rechecked by the small kernel.
- **Library maturity ↔ formalization speed**: the first project builds infrastructure; later projects reuse it and accelerate dramatically.
- **AI ↔ misformalization risk**: formal proofs can be checked automatically; definitions and theorem translations require semantic review because wrong meanings can compile.
- **Universal conjectures ↔ counterexamples**: searching for one witness can be a strong machine route; every claimed witness should be immediately formalized and then conceptually digested.
