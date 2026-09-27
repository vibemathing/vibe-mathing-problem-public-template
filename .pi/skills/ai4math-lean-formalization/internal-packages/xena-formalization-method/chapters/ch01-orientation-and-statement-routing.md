# Chapter 1: Orientation and Statement Routing

## Core Idea

Most wasted effort in formalization begins before the first tactic: the task is classified incorrectly or the intended statement has not been frozen. Route first. A proof assistant checks a precise formal proposition; it cannot certify that the proposition is the one the mathematician meant.

## Frameworks Introduced

### Task classifier

Place the request in one primary class:

1. **Statement work** — translate, generalize, or audit a theorem statement.
2. **Proof work** — prove an already trusted statement.
3. **Definition/API work** — introduce reusable mathematical infrastructure.
4. **Project work** — plan a large dependency graph and library growth.
5. **Teaching work** — choose exercises, explanations, and feedback loops.
6. **AI verification work** — review generated statements, definitions, proofs, or witnesses.

Mixed tasks should follow the dependency order: statement → definitions/API → proof → explanation. Do not begin proof search while the semantic layer is unsettled.

### Statement audit

For every formal claim, write a compact contract:

- object types and ambient structures;
- quantifier order;
- hypotheses and their scopes;
- domain restrictions such as nonzero, nonempty, positivity, finiteness;
- conclusion;
- intended meaning of equality/equivalence;
- any classical assumptions that affect computation.

Then test the contract on degenerate examples. Formalization repeatedly exposes omissions that prose treats as implicit: empty sets, zero denominators, small natural numbers, non-attained infima, and reversed dependencies between constants.

## Key Concepts

**Formal correctness has two gates.** Gate A asks whether the formal theorem expresses the intended mathematics. Gate B asks whether a proof term inhabits that formal theorem. Lean is extremely strong at Gate B. Gate A still needs mathematical judgment, especially for AI translations and newly formalized definitions.

**Quantifier order is data.** A statement of the form “for every `ε` choose `C`, then for every `n`…” differs from choosing one `C` that works for all `ε`. Research arguments with hierarchies of constants must encode the dependency order in the proposition itself.

**The statement can be a milestone.** On research-scale mathematics, first getting all objects defined and the main theorem stated idiomatically may take substantial work. Treat this as progress, then estimate the proof phase from the resulting dependency graph.

## Decision Procedure

WHEN the user gives informal prose:
1. Translate each noun phrase to a type/structure.
2. Translate dependencies to explicit binders in order.
3. Add domain hypotheses only when mathematically intended.
4. Check whether the conclusion accidentally becomes trivial or impossible.
5. Compare at least one representative example/nonexample.

WHEN the user gives Lean code that already compiles:
1. Do not infer that the intended theorem is solved.
2. Read the type of the theorem and the definitions it depends on.
3. Check it against the informal claim.
4. Only then discuss proof quality or trust.

## Anti-patterns

- Starting with tactics because the goal “looks familiar”.
- Treating omitted prose assumptions as harmless.
- Letting a generated formal statement define the intended question after the fact.
- Using a convenient equality when the mathematical statement requires isomorphism, extensional equality, or a quotient relation.
- Estimating a research proof before checking whether the main objects can be stated in the library.

## Validation Checkpoint

Before leaving orientation, restate the target in one sentence and list every choice that could change its truth: ambient type or structure, binder order, domain restrictions, equality/equivalence notion, classical assumptions, and intended generality. Test at least one ordinary example and one boundary case. If two plausible formal statements remain, keep both visible and ask which mathematical claim is intended; proof search cannot resolve semantic ambiguity. Route only after the statement is stable enough that a successful proof would answer the user's actual question.

## Key Takeaways

Freeze meaning before proof. Route by artifact type. Compilation is decisive evidence for formal derivation only after semantic alignment has been checked.

## Connects To

Equality details: [04](ch04-equality-rewriting-and-normalization.md). Definition semantics: [06](ch06-definition-api-and-library-engineering.md). AI auditing: [12](ch12-ai-autoformalization-and-semantic-audit.md). Research statements: [10](ch10-research-blueprints-and-library-growth.md).
