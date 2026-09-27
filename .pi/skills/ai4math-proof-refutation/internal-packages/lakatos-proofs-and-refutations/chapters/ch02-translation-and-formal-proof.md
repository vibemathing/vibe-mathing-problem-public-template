# Chapter 2: Translation, Dominant Theories, and Formal Proof

## Core Idea

A deeper proof can arise by translating an informal theory into a more exact mathematical language, but the gain in internal rigor does not automatically guarantee fidelity to the original problem. The translation itself becomes an object of criticism.

## Frameworks Introduced

### Translation procedure (翻译程序)

**When to use:** when an informal object is encoded into algebra, set theory, logic, a computational model, a type system, a simulation, or any theory treated as more secure.

**Procedure:**
1. List the source terms and relations.
2. List the target representations.
3. Record what each mapping preserves.
4. Record what it discards or adds.
5. Identify the target axioms/presuppositions used by the proof.
6. Test whether source counterexamples remain representable after translation.
7. Separate proof validity in the target theory from faithfulness of the translation.

The chapter's central challenge is that a definition can play two different roles. If it claims to preserve the old meaning, it can be wrong or incomplete. If it merely stipulates a new meaning, it can be definitionally safe while silently changing the subject.

### Dominant theory (主导理论)

A **dominant theory** is the accepted theory into which another theory is translated—for example, the chapter treats vector algebra and later logic as candidate secure backgrounds.

**Use:** to localize where certainty is coming from.

Ask:
- Which theory supplies the fixed rules of deduction?
- Which source concepts are represented inside it?
- What would count as evidence that the translation is inadequate?
- What happens if confidence in the dominant theory itself weakens?

Changing the dominant theory can reorganize what counts as proof, primitive concept, or legitimate counterexample.

### Formal proof relative to formative terms

A proof becomes formal to the extent that its correctness no longer depends on the meanings of the specialized descriptive terms. Reinterpret those terms and the conditional remains true, provided the formative/logical structure is fixed.

**Important boundary:** mechanized checking can decide whether a derivation obeys the rules of a fixed formal system. This moves the critical burden toward axioms, formalization choices, semantic interpretation, and translation from the informal problem.

## Technical Model Used in the Chapter

The polyhedron is represented through sets of vertices, edges, and faces together with incidence information. The proof then introduces:

- **k-chains:** mod-2 sums of k-dimensional cells;
- **boundary:** the sum of incident lower-dimensional cells;
- **k-circuits:** chains whose boundary is zero;
- **bounding circuits:** circuits that are boundaries of higher-dimensional chains;
- vector spaces of chains, cycles, and boundaries over mod 2;
- dimension/rank relations that yield the Euler characteristic under suitable homological-style conditions.

The technical point matters methodologically: geometric notions such as connectedness are replaced by algebraic conditions. This can broaden the theorem to cases where older geometric intuition fails, including some star polyhedra. Greater rigor and greater scope can coincide when the translation captures a deeper invariant.

## Translation Audit Matrix

| Translation stance | Strength | Failure mode | Required check |
|---|---|---|---|
| meaning-preserving definition | keeps contact with original problem | mistranslation, lost aspects | counterexamples to semantic fidelity |
| stipulative/nominal definition | internally unambiguous | replaces old problem | compare source goals with target theorem |
| dominant-theory reduction | inherits target rigor | target theory/model assumptions hidden | expose axioms and modeling commitments |
| formal proof | mechanically checkable relative to rules | false confidence in applicability | audit encoding and assumptions |

## Worked Example: From Geometric Polyhedra to Incidence Algebra

Suppose an informal theorem concerns polyhedra with a topological connectedness condition. A translation replaces visual deformation arguments with incidence structures and the algebra of boundaries.

1. Encode cells and incidence.
2. Define boundary using mod-2 addition, so shared internal boundaries cancel.
3. Define a closed chain by `boundary = 0`.
4. Express “bounding” as being the boundary of a higher-dimensional chain.
5. State connectedness-like conditions using equality of cycle and boundary spaces.
6. Derive the Euler relation from dimensions/ranks.

The algebraic derivation can be tight. Yet two independent questions remain:

- Does the encoded structure represent every source object we intended?
- Does every encoded structure still deserve the source name “polyhedron” for this problem?

A failed application after successful formal verification therefore points first to the modeling/translation boundary, not automatically to the deductive core.

## Decision Rules

- If a formal theorem is correct but an intended example violates the informal claim, inspect **translation fidelity**.
- If a definition is defended only because “definitions cannot be false,” determine whether the old problem has been abandoned.
- If the translation yields a wider explanatory theorem, preserve the gain while documenting which source intuitions were replaced.
- If two translations disagree, compare which source distinctions each preserves; do not choose solely by syntactic simplicity.
- If the dominant theory changes, re-audit prior translations rather than treating old reductions as timeless.

## Anti-patterns

- **Semantic laundering:** calling a stipulative redefinition a faithful translation.
- **Formal-certainty leakage:** transferring certainty from a checked derivation to the unverified model mapping.
- **Primitive-term absolutism:** assuming a term is permanently clear because it currently feels intuitive.
- **Model replacement without notice:** solving a cleaner target problem while reporting success on the original problem.

## Key Takeaways

1. Formalization can deepen and broaden a proof.
2. Translation is itself fallible when it claims to preserve meaning.
3. Stipulative definitions avoid falsity by changing meaning; they require a scope audit.
4. Formal proof certainty is relative to fixed rules and formative terms.
5. Application failures often live at the representation boundary.
6. A dominant theory is a methodological choice that can later be revised.

## Connects To

- **Chapter 1:** hidden lemmas in informal proof correspond to hidden assumptions in translation/modeling.
- **Appendix 2:** proof-generated definitions are easiest to understand when their proof-ancestors remain visible.
