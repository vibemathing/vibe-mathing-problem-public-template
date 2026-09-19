# Chapter 6: Interactive Theorem Proving and Trusted Proof Production

**Source coverage**: Harrison Ch. 6, §§6.1–6.9, book pp. 464–525.

## Core Idea
Interactive theorem proving separates proof discovery from proof trust. A small sound kernel can certify results from derived rules, tactics, automation, or declarative proof scripts, allowing aggressive search code to remain outside the trusted core.

## Frameworks Introduced
### Human-oriented proof methods
Humans excel at abstraction, choosing lemmas, restructuring goals, and exploiting mathematical meaning; machines excel at exhaustive symbolic bookkeeping and checking. An interactive prover should let humans steer high-level decomposition while automating routine logical detail.

### Prover versus proof checker
- **Prover**: Searches for proofs.
- **Proof checker**: Verifies a presented proof object or a sequence of kernel inferences.

A system can safely combine untrusted automation with a trusted checker if every final theorem is reconstructed through the checker.

### Proof systems: Hilbert, natural deduction, sequent calculus
The chapter compares proof-system styles:
- Hilbert systems use few inference rules plus many axioms and are compact metatheoretically, awkward interactively.
- Natural deduction mirrors introduction/elimination reasoning around connectives and quantifiers.
- Sequent calculus makes contexts explicit and supports structural analysis such as cut elimination.

**Operational lesson**: Proof-system choice and proof-search strategy are distinct. Automated search often uses specialized refutation calculi even when the trusted interface is natural-deduction-like.

### LCF architecture
Core pattern:
1. Define an abstract theorem type `thm` that user code cannot construct directly.
2. Provide only a small set of primitive functions representing sound inference rules/axioms.
3. Build every convenience rule as a program composing primitive inferences.
4. Let tactics and automated provers return theorem values only through those rules.

**Security/trust invariant**: A bug in an untrusted tactic may fail, loop, or find the wrong search route; it cannot manufacture a theorem if the abstract type and kernel boundary are intact.

### Derived propositional rules
From a tiny kernel, derive useful rules for:
- implication reflexivity/transitivity;
- conjunction/disjunction introduction/elimination;
- contraposition and contradiction handling;
- equivalence decomposition/reconstruction;
- assumption management.

**Pattern**: Prove a reusable propositional tautology once, instantiate it, and combine it with existing theorems rather than expanding low-level primitive steps each time.

### Proof-producing tautology search
The book modifies tableau-style propositional search so that each recursive branch returns a theorem, not merely a Boolean.
- Search logic stays close to a fast refutation procedure.
- Closing a branch constructs an explicit contradiction theorem.
- Decomposition combines child theorems using derived inference rules.
- The final result is accepted because kernel constructors mediate every step.

### First-order derived rules
Binding-sensitive rules need extra side conditions:
- generalization requires freshness/non-freeness constraints on assumptions;
- specialization must be capture-safe;
- alpha-conversion changes only bound names;
- existential introduction/elimination must preserve witness-variable discipline;
- equality rules maintain reflexivity/congruence/substitutivity.

A useful `ispec`-style rule performs specialization while alpha-renaming as necessary to avoid capture.

### First-order proof by inference
The completeness development reconstructs first-order tableau/refutation search through LCF inference.

Operational pipeline:
1. Search with normalized/Skolemized forms.
2. Record enough information to recover original theorem structure.
3. Introduce temporary hypotheses for Skolemized formulas when convenient.
4. Construct theorem steps for each tableau expansion/closure.
5. Eliminate Skolem dependencies and discharge hypotheses with freshness conditions.
6. Produce a theorem in the original language.

**Lesson**: Search transformations such as Skolemization cannot be treated as trusted theorem equivalences casually; proof-producing code must justify how the transformed search result is transported back.

### Tactics and goals
A **goal** contains assumptions plus a desired conclusion. A **tactic** transforms one goal into subgoals and returns a justification function that combines theorem solutions of the subgoals into a theorem of the original goal.

Conceptual type:

```text
tactic : goal -> (subgoals, justification)
justification : theorem list -> theorem
```

Typical tactics:
- implication/conjunction introduction;
- universal introduction with fresh variable;
- existential witness provision;
- assumption/exact theorem;
- case split;
- lemma/subproof insertion;
- call automated first-order reasoning for a local subgoal.

### Procedural and declarative proof styles
- **Procedural**: Script tactic applications and goal transformations.
- **Declarative**: Present readable statements such as assume/fix/consider/take/have/conclude/qed, with automation filling local inference gaps.

The two styles can coexist: declarative structure captures the mathematical narrative while tactics handle routine subgoals.

### Proof finding versus proof checking
For performance, automation may:
- run a fast theorem-finding algorithm that does not build kernel terms at every inner step;
- emit a search trace/certificate;
- replay that trace through the trusted kernel.

This reduces trusted code while preserving speed. Reflection can move computation into the logic after formally proving the correctness of the reflected algorithm, but proving such correctness is itself substantial work.

## Key Concepts
- **Trusted kernel**: Small code base implementing primitive inference and theorem representation.
- **Derived rule**: Sound rule implemented by composing primitive kernel rules.
- **Tactic**: Backward goal transformer paired with a forward justification function.
- **Goal state**: Outstanding subgoals plus their relation to the original theorem.
- **Proof certificate**: Compact evidence replayable by a checker.
- **Cut**: Inference introducing an intermediate formula; cut elimination motivates analytic proof structure.
- **Reflection**: Prove an algorithm correct inside the logic, then use evaluated computations as certified reasoning steps.

## Mental Models
- **Tiny trusted core, large untrusted shell**: Minimize what must be correct for soundness.
- **Backward planning, forward checking**: Tactics choose subgoals backward; justification reconstructs a forward theorem.
- **Search trace as compression**: The expensive component finds a path; the trusted component only verifies the path.
- **Freshness is part of the theorem**: Quantifier side conditions are logical obligations, not implementation trivia.

## Anti-patterns
- **Letting automation construct theorem objects directly**: Enlarges the trusted base to all search code.
- **Equating successful search with certified proof**: A Boolean `true` from a prover is weaker evidence than a checked theorem when assurance matters.
- **Ignoring binder side conditions in tactics**: Generalization/existential rules become unsound.
- **Reconstructing from too little trace information**: The checker cannot justify search transformations after the fact.
- **Building every search step through the kernel when performance dominates**: Correct but potentially expensive; certificate replay is often better.
- **Using procedural tactics for the entire mathematical narrative**: Can make proofs brittle and unreadable; preserve meaningful intermediate propositions declaratively.

## Code Examples
LCF kernel boundary:

```text
abstract type Theorem
primitive assume(p)       -> Theorem(p |- p)
primitive modus_ponens(t1, t2) -> checked theorem
primitive generalize(x,t) -> checked theorem if freshness holds
# no public constructor for arbitrary Theorem values
```

Tactic interface:

```text
imp_intro(goal A |- p => q):
    subgoal := A union {p} |- q
    justify([th_q]) := discharge p from th_q
    return [subgoal], justify
```

Certificate architecture:

```text
trace := fast_untrusted_search(problem)
if trace absent: return UNKNOWN/FAILURE
result := replay_through_kernel(problem, trace)
return result
```

## Reference Tables
### Trust placement
| Component | May be complex/heuristic? | Must be trusted for soundness? |
|---|---:|---:|
| Search heuristic | yes | no, if result is replayed |
| Tactic strategy | yes | no, if it only composes kernel rules |
| Parser/printer | can be complex | input/output correctness matters, but theorem construction still kernel-gated |
| Primitive inference kernel | keep tiny | yes |
| Proof/certificate checker | preferably small | yes if it directly authorizes theorem acceptance |
| Reflection theorem | can support large computation | its proof and evaluator assumptions enter trust analysis |

### Proof style selection
| Need | Prefer |
|---|---|
| Fine control/debugging of search | procedural tactics |
| Readable mathematical artifact | declarative proof structure |
| Routine local closure | automation tactic |
| High assurance from fast external search | certificate replay through kernel |

## Worked Example
Goal: prove `A ∧ B ⇒ B ∧ A` in an LCF-style environment.

1. A backward implication-introduction tactic changes the goal to proving `B ∧ A` under assumption `A ∧ B`.
2. Conjunction introduction creates two subgoals: prove `B`, prove `A`.
3. Conjunction-elimination derived rules obtain both components from the assumption theorem for `A ∧ B`.
4. The justification functions combine the two component theorems into `B ∧ A`, then discharge the assumption to get the implication.
5. Every theorem object is produced through primitive/derived functions ultimately grounded in the kernel.

A search tactic could automate all five steps, while the kernel still sees only sound inference applications.

## Failure Recovery
- Search engine is fast but untrusted → emit a certificate or trace and replay it.
- Proof reconstruction is slow → store higher-level reusable lemmas, improve certificate granularity, or formally reflect a stable algorithm.
- Quantifier reconstruction fails → inspect freshness, alpha-renaming, and Skolem-witness discharge conditions.
- Tactic creates too many brittle subgoals → introduce meaningful lemmas or use a declarative block around the stable proof structure.
- Kernel becomes large → move conveniences back into derived rules outside the primitive theorem constructors.

## Key Takeaways
1. Proof discovery and proof checking should be architecturally separable.
2. LCF obtains strong soundness assurance by making theorem construction an abstract-kernel privilege.
3. Derived rules and tactics can be arbitrarily convenient without enlarging the trusted kernel if they cannot forge theorem values.
4. Binding/freshness conditions remain critical during proof reconstruction.
5. Backward tactics need forward justification functions.
6. Declarative proofs improve readability while retaining automated local reasoning.
7. Certificate replay is the standard bridge between fast search and small trusted checking.

## Connects To
- **Ch. 3**: Tableaux/model-elimination search can be reconstructed as kernel theorems.
- **Ch. 2**: SAT/tautology engines can return assignments or proof traces rather than booleans only.
- **Ch. 7**: Mechanical proof checking can remain decidable even when theoremhood in the represented theory is undecidable.
