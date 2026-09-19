# Chapter 7: Limits of Formal Reasoning

**Source coverage**: Harrison Ch. 7, §§7.1–7.8, book pp. 526–592.

## Core Idea
Mechanized deduction has precise limits. Tarski, Gödel, Church, and related results constrain definability, axiomatization, and decision procedures, while still leaving proof checking and many specialized decision methods fully mechanical.

## Frameworks Introduced
### Hilbert's programme and the proof/object distinction
Hilbert sought to justify strong “ideal” mathematical reasoning by finitistic metamathematical analysis of formal proofs. The programme sharpened the distinction between:
- mathematical objects/statements inside a formal system;
- finite syntactic proof objects examined from outside.

Constructive concerns motivate asking whether an existence proof yields an explicit witness. Classical principles such as excluded middle can establish existence without providing a construction.

### Arithmetization and definability
To reason about syntax inside arithmetic:
1. Assign numbers to symbols/strings/formulas/proofs (Gödel coding).
2. Show syntactic relations such as “is a term,” “is a formula,” substitution, and “is a proof” are arithmetically definable.
3. Represent computable/primitive-recursive operations arithmetically.
4. Use diagonal/fixed-point machinery to build sentences referring to their own codes indirectly.

The chapter makes these constructions explicit enough to see them as algorithms/definitions rather than mystical self-reference.

### Tarski's undefinability of truth
For a sufficiently expressive fixed arithmetic language interpreted in the natural numbers, there is no arithmetically definable predicate that correctly picks out exactly the Gödel numbers of all true sentences of that same language.

**Operational use**: Reject designs that assume a fully correct internal truth predicate for their own sufficiently expressive arithmetic language without changing levels/languages or weakening the claim.

**Do not overextend**: The theorem has precise assumptions. It does not say that no particular truth predicate can exist in a stronger metalanguage or for a weaker object language.

### Incompleteness of definable axiom systems
If an axiom set is definable and sound enough, the set of its theorems is also definable/semidecidable in the relevant sense. Tarski-style reasoning then shows that no such effective sound system captures every arithmetic truth.

**Diagnostic rule**: A fixed mechanical axiomatization of sufficiently rich arithmetic must sacrifice completeness, soundness, or effective character under the theorem's hypotheses.

### Gödel's first incompleteness theorem
Construct a sentence `G` satisfying, in effect, `G ↔ ¬Pr_A(⌜G⌝)` where `Pr_A` expresses provability in axiom system `A`.

The chapter refines the needed assumptions using the arithmetic hierarchy:
- **Δ0**: bounded-quantifier formulas; effectively decidable in the standard model.
- **Σ1**: existentially quantified decidable relation; true Σ1 facts are semidecidable and, for suitable weak arithmetic such as Robinson `Q`, provable when true.
- **Π1**: negations/universal counterparts of Σ1.

Under appropriate consistency/soundness hypotheses, `G` is unprovable, and stronger hypotheses also block proof of `¬G`.

**Operational discipline**: State exactly which consistency or soundness assumption a claimed incompleteness consequence uses.

### Computability and recursively enumerable sets
A Turing machine gives a precise operational model of computation.
- **Computable/recursive function**: machine halts with the correct output on every input in its domain (total when it halts on all inputs).
- **r.e./semicomputable set**: membership can be recognized by a machine that halts on members, with no termination guarantee on nonmembers.
- A set is decidable when both it and its complement are r.e.

Central bridge in the chapter: r.e. relations correspond to Σ1-definability over arithmetic. Computation histories can be encoded arithmetically.

### Robinson arithmetic and Σ1 completeness
Robinson arithmetic `Q` is finitely axiomatized and much weaker than Peano arithmetic, yet strong enough to verify concrete arithmetic computations and prove every true Σ1 sentence.

Harrison's `sigma_prove` development is constructive: ground arithmetic and bounded quantifiers are mechanically reduced until a proof can be built.

**Consequence**: This very weak arithmetic suffices for undecidability reductions.

### Church's theorem
First-order logical validity is undecidable.

Operational reading:
- A complete semidecision procedure can enumerate proofs of valid formulas and halt when one is found.
- There can be no algorithm that always halts and correctly answers validity for every first-order formula.
- Therefore nontermination on nonvalid inputs is not merely a defect of a naive prover; it is unavoidable for any complete general procedure.

### Further limitative results
The chapter surveys stronger boundaries:
- **Gödel's second theorem**: sufficiently strong consistent theories satisfying derivability conditions cannot prove their own standard consistency statement.
- **Löb's theorem** and reflection principles refine relationships between internal provability and truth claims.
- **Hilbert's tenth problem**: no general algorithm decides whether an integer polynomial equation has a solution; r.e. sets can be represented Diophantinely.
- Sharper first-order undecidability persists under severe syntactic restrictions (e.g. restricted prefixes/signatures).
- **Rosser's refinement** weakens some soundness assumptions to consistency for a suitable incompleteness construction.
- Robinson arithmetic is essentially/strongly undecidable in senses discussed in the text.

### Retrospective: what remains mechanical
Even though theoremhood can be undecidable, a detailed proof in a fixed effective first-order proof system is mechanically checkable.

This supports the practical architecture of Ch. 6:
- theorem search may be incomplete in time/resource behavior;
- proof checking can still be small, deterministic, and decidable;
- specialized theories can have terminating decision procedures even though full first-order logic does not.

## Key Concepts
- **Definable relation**: Relation characterized by a first-order arithmetic formula in the intended model.
- **Gödel numbering**: Effective injection of syntax/proofs into natural numbers.
- **Diagonal/fixed-point lemma**: Constructs a sentence equivalent to applying a property to its own code.
- **Sound axiom system**: Proves only truths in the intended interpretation.
- **Complete theory/system**: Decides/proves every sentence or its negation according to the specified notion.
- **Σ1 / Π1 / Δ0**: Low levels of the arithmetical hierarchy central to provability/computability arguments.
- **r.e. / semidecidable**: Positive instances can be recognized by a halting computation.
- **Church–Turing thesis**: Informal identification of effectively computable procedures with standard equivalent formal computation models.
- **Essential undecidability**: Roughly, every consistent effective extension in a given class remains undecidable.

## Mental Models
- **Code syntax into data**: Metamathematics works by turning formulas/proofs into natural-number objects that arithmetic can discuss.
- **Semidecision is a real algorithmic target**: For general theorem proving, termination on the positive side can be the strongest possible guarantee.
- **Proof checker survives undecidability**: Checking a finite purported derivation is different from finding one or deciding whether one exists.
- **Limit theorem = quantified engineering constraint**: Always unpack the language, theory strength, effectiveness, and soundness assumptions before applying the slogan.

## Anti-patterns
- **“Gödel means mathematics cannot be automated.”** Too broad; many fragments are decidable and formal proof checking is mechanical.
- **“Undecidable means no useful prover exists.”** Semidecision, heuristics, interactive proof, and domain decision procedures remain powerful.
- **Using Tarski to ban all truth predicates**: The result concerns internal definability for a sufficiently expressive fixed language/model setup.
- **Claiming consistency alone always yields both sides of Gödel independence**: The exact theorem variant and soundness/consistency hypothesis matters.
- **Treating nontermination as evidence of falsehood**: In a semidecision procedure, nontermination carries no such conclusion.
- **Asserting a current open/closed status from the 2009 text without checking freshness**: Historical status belongs to the source date.

## Code Examples
Semidecision versus decision:

```text
prove_valid(phi):
    enumerate proof-search states fairly
    if a formal proof of phi is found: return VALID
    # may run forever when phi is not valid
```

Proof checking:

```text
check(proof):
    for each finite inference step:
        verify rule and side conditions
    return ACCEPT or REJECT
```

Diagonal pattern:

```text
Given a definable one-place property P(n),
construct a sentence G whose arithmetic meaning satisfies
G <-> P(code(G)).
Choose P to express a negated provability/truth condition.
```

## Reference Tables
### What the limit results constrain
| Result | Blocks | Leaves available |
|---|---|---|
| Tarski undefinability | internal definition of full arithmetic truth in same adequate language | external/metalinguistic truth, weaker fragments |
| Gödel I | complete effective sound-enough axiomatization of sufficiently strong arithmetic | incomplete sound theories, stronger extensions, individual proofs |
| Church | total decision algorithm for general first-order validity | complete semidecision/proof enumeration, decidable fragments |
| Gödel II | suitable theory proving its own standard consistency under hypotheses | relative consistency, stronger metatheory, restricted reflection |
| Hilbert 10 | total algorithm for integer Diophantine solvability | special polynomial classes, semidecision by witness search |

### Result interpretation checklist
| Ask | Reason |
|---|---|
| Which formal language/theory? | Expressive strength matters. |
| What is effective/definable/r.e.? | Theorems target mechanical or definable systems. |
| Which model supplies “truth”? | Standard-model soundness may be assumed. |
| Which consistency/soundness level? | Gödel/Rosser variants differ. |
| Is the task search, decision, or checking? | Their computability status can differ. |

## Worked Example
Suppose a user asks: “Build a theorem prover for arbitrary first-order formulas that always returns VALID or INVALID.”

1. Clarify that the target is semantic validity over all first-order interpretations.
2. A sound and complete proof calculus can support a procedure that searches fairly for a proof of a valid formula.
3. On a valid input, completeness guarantees some finite proof exists, so fair enumeration eventually finds one.
4. If the formula is invalid, no proof exists. A general finite countermodel search is insufficient because some satisfiable first-order formulas need infinite models.
5. Church's theorem rules out a total algorithm that always terminates with the correct yes/no answer for all first-order formulas.
6. Offer valid alternatives: semidecision, a bounded prover returning `unknown`, interactive proof, or a total decision procedure after restricting the input to a decidable fragment such as those in Ch. 5.

This is the correct engineering use of an undecidability theorem: it changes the API contract.

## Failure Recovery
- User requests “always terminate” for full FOL → negotiate a decidable fragment or allow `unknown`/semidecision.
- Incompleteness claim seems paradoxical → identify the object theory, provability predicate, and metalanguage level.
- A result cites “consistency” vaguely → determine whether consistency, 1-consistency, Σ1-soundness, or Π1-soundness is actually needed.
- A 2009 open-problem claim matters operationally → verify current status externally before relying on it.

## Key Takeaways
1. Formal syntax can encode its own proof theory arithmetically.
2. Tarski blocks an internal full truth definition for sufficiently expressive arithmetic.
3. Gödel blocks complete effective sound-enough axiomatizations of sufficiently strong arithmetic.
4. r.e. and Σ1-definability connect computation with arithmetic syntax.
5. Church blocks total decision of general first-order validity, making semidecision a principled target.
6. Proof checking remains mechanical even where proof existence is undecidable.
7. Limitative theorems must be applied with their exact assumptions, not as slogans.

## Connects To
- **Ch. 3**: Explains why general first-order proof search may diverge.
- **Ch. 5**: Motivates careful identification of decidable fragments.
- **Ch. 6**: Supports small proof checkers and interactive proof despite undecidable theorem search.
