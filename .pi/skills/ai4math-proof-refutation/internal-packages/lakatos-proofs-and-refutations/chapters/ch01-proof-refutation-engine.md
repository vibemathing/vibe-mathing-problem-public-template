# Chapter 1: The Proof–Refutation Engine

## Core Idea

Informal mathematical discovery grows through an interaction among conjectures, proofs, counterexamples, and changing concepts. The decisive move is to use a failed proof as information: decompose it into lemmas, locate where falsity enters, revise the theorem or the proof, and then attack the revision again.

## Frameworks Introduced

### Prove and refute the same conjecture

**When to use:** whenever a claim is still research-grade, informal, or supported by an argument whose assumptions may be incomplete.

**How:**
1. State the conjecture in its current language.
2. Build a proof idea even if the conjecture may be false.
3. Extract the non-trivial lemmas used by the proof.
4. Search for counterexamples to the main claim and to each lemma.
5. Feed failures back into the proof analysis.

**Why it works:** proof and refutation reveal different information. Proof exposes dependencies; refutation tells you which dependency, domain, or concept deserves pressure.

### Global/local counterexample matrix

A **global** counterexample falsifies the main conjecture. A **local** counterexample falsifies a proof lemma.

- **Global + local:** the proof has identified a genuine failure channel. Use **lemma incorporation**.
- **Global + not local:** the decomposition missed an assumption. Search for a **hidden lemma**.
- **Local + not global:** the proof failed without the theorem failing. Repair or deepen the proof.
- **Neither:** the case can still be heuristically important by revealing poor explanatory reach.

This classification prevents the common error of treating “the theorem is false,” “this proof fails,” and “this example is awkward” as the same event.

### Falsity-transfer principle (虚假性转送原理)

**Diagnostic rule:** if a global counterexample leaves every explicit lemma untouched, the proof analysis is incomplete. Add a lemma that captures the failure and test it against the counterexample.

Use the principle as a regulator, not as a promise that the current list of lemmas is final. A newly exposed hidden lemma can itself later fail.

### Lemma incorporation (引理并入法)

**When to use:** a counterexample falsifies both the conjecture and an identified proof lemma.

**Procedure:**
1. Identify the lemma actually needed by the proof.
2. Formulate it as a condition on the theorem's domain.
3. Replace the naive conjecture with the conditional, proof-generated theorem.
4. Re-run counterexample search against the new theorem and its proof.

**Quality test:** the new condition should summarize a genuine proof dependency. A restriction such as “convex” may be safe yet methodologically weak if the proof never uses convexity.

### Rule 4: local-only repair

If a local counterexample attacks a lemma but the main conjecture remains true, do not incorporate the false lemma as a domain restriction by default. Replace it with an unfalsified lemma.

Two levels:
- **weak:** a nearby lemma preserves the current proof idea;
- **radical:** a different proof idea handles a larger range and explains why the old proof was narrow.

Use radical mode when repeated repairs produce an increasingly tiny theorem or when distinct proofs expose materially different conditions.

### Rule 5: deductive guessing (演绎的猜测)

A conjecture can be generated from a proof construction or problem structure rather than extrapolated from a table of examples. Given any counterexample, seek a deeper theorem whose proof explains the counterexample's role. This is especially valuable when the initial conjecture has exhausted its usefulness as the research target.

## Major Diagnostic Methods

### Monster-barring (怪物排除法)

A counterexample is rejected by redefining the object so the troublesome case no longer counts. This can stabilize terminology, but it becomes methodologically sterile when the redefinition exists chiefly to protect the theorem and is disconnected from the proof.

**Tell:** “That example was never a real X.”

**Audit:** Ask what proof step motivates the exclusion. If none, keep the exclusion provisional and continue testing the broader concept.

### Exception-barring (例外排除法)

The theorem is narrowed to a safe domain. Its strongest form strategically retreats to a conservative class.

**Risk:** a safe condition can be ad hoc, too narrow, and irrelevant to the proof. It may discard many valid examples along with the counterexamples.

**Upgrade path:** analyze the proof until the restriction can be replaced by proof-generated conditions.

### Monster-adjusting (怪物校正法)

The counterexample is reinterpreted so the theorem appears to hold after all—for example, by changing how its faces, edges, or components are counted.

**Risk:** reinterpretation can mask a genuine conceptual failure.

**Use only when:** the new interpretation has independent structural support and improves later reasoning beyond the single troublesome example.

### Logical vs. heuristic counterexamples (逻辑的反例 VS. 探试的反例)

A **logical counterexample** falsifies the theorem as currently formulated. A **heuristic counterexample** can be logically harmless to a restricted theorem yet still reveal that the theorem is shallow, the proof has little content, or a broader theory is available.

**Operational rule:** after deciding whether an example is logically admissible, ask a second question: *what does this case teach about the proof's explanatory range?* Do not discard an example merely because a defensive restriction makes it cease to be a formal counterexample.

### One-proof/many-refutations → many-proofs/many-refutations

Rules 1–3 produce the **one-proof/many-refutations** cycle. Rule 4's radical form shows why one proof may be insufficient. Distinct proofs of the same naive conjecture expose distinct conditions, scopes, and concepts; the mature method becomes **many-proofs/many-refutations**.

## Content, Depth, and Finality

Each incorporated lemma can increase certainty while shrinking content. Counterbalance this pressure by asking:

- Can a stronger or different lemma preserve more cases?
- Can a deeper proof explain cases that the current proof excludes?
- Does another proof yield a different theorem from the same naive conjecture?
- Is the current target itself too narrow—should a broader invariant or problem replace it?

A “final proof” characterized by necessary and sufficient conditions is an aspiration, not a guaranteed endpoint. The book repeatedly warns that proof analysis can reopen under new counterexamples or concept extensions.

## Concept Formation

### Concept stretching (概念拉伸)

Critical practice can broaden a term so previously excluded “monsters” become legitimate test objects. This changes what counts as a counterexample and can force deeper theory.

Use a **definition genealogy**:
1. record the original intended class;
2. record each extension/restriction;
3. state which new examples become admissible;
4. state which theorem/proof breaks;
5. record the proof-generated replacement concept.

Unrestricted stretching can make criticism arbitrary. Restrict stretching to terms that genuinely carry the disputed mathematical content.

### Moderate concept stretching and relative logical truth

The chapter's closing discussion distinguishes productive, targeted stretching from unlimited semantic deformation. Relative to a chosen subset of terms held fixed, criticism can push a theorem toward a form whose truth no longer depends on the meanings of the remaining descriptive terms. This anticipates the Chapter 2 idea of formal proof.

**Operational rule:** state which terms are allowed to vary and which are treated as formative/fixed. Stop a stretching exercise when it ceases to expose mathematical structure and merely changes logical vocabulary arbitrarily. Treat the resulting “logical truth” as relative to that choice of fixed components.

### Proof-generated concepts (证明引生概念)

A proof can create the right classification. In the Euler case, conditions such as the relevant forms of connectedness emerge from operations the proof needs, yielding a theoretical classification that outperforms naive visual categories.

**Operational rule:** when a definition looks arbitrary, ask which proof step would become valid if that definition held. If there is a clear answer, the definition has a proof-ancestor.

## Worked Example: Euler Characteristic as a Diagnostic Pattern

The naive claim says that polyhedra satisfy `V - E + F = 2`. A flattening/triangulation proof appears to support it. Counterexamples then force progressively finer diagnosis:

1. A polyhedron with a cavity is globally non-Eulerian and undermines the deformation assumption: this motivates a condition tied to the proof's ability to flatten the object.
2. A “topped cube” defeats an early improved theorem while exposing a different proof dependency concerning faces; a hidden assumption must be made explicit.
3. Objects with annular faces reveal that “each face can be divided by a diagonal” is the relevant step, generating a connectedness condition from the proof rather than from visual taste.
4. A cube or dodecahedron can refute the lemma “all faces are triangular” while still satisfying Euler's formula: this is local-only failure and calls for lemma replacement, not theorem rejection.
5. Alternative proofs—projection, cutting, algebraic translation—handle different objects and expose different theoretical scopes. Their value lies partly in what they explain and generate.

The reusable pattern is independent of polyhedra: decompose the argument, classify each failure, and let the proof determine which condition deserves to enter the theorem.

## Anti-patterns

- **Proof worship:** assuming a persuasive proof must establish exactly the claim originally intended.
- **Counterexample dumping:** collecting exceptions without asking which proof dependency they attack.
- **Safety by unrelated restriction:** adding a narrow condition simply because it removes known failures.
- **Retrospective perfection:** rewriting history so a hidden lemma appears to have been known all along.
- **Certainty-only comparison:** preferring proofs solely by apparent rigor while ignoring scope and explanatory depth.
- **Definition amnesia:** changing a term without recording how the change alters admissible counterexamples.

## Key Takeaways

1. A counterexample is also a probe into proof architecture.
2. A theorem failure and a proof failure demand different repairs.
3. Global-without-local failure is evidence for hidden assumptions.
4. Good restrictions are generated by proof dependencies.
5. Local-only failures should stimulate stronger lemmas or deeper proofs.
6. Definitions and classifications can be products of proof development.
7. Mathematical growth can be rational without being monotonic or final.

## Connects To

- **Chapter 2:** translates the same methodological problem into formalization and dominant-theory terms.
- **Appendix 1:** uniform convergence supplies a second historical instance of hidden-lemma discovery.
- **Appendix 2:** shows how deductivist exposition erases the process that generated useful concepts.
