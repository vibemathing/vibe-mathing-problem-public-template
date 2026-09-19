# Supplement: Miscellaneous Lean Utilities, Units, Probability, and Erdos Files

## Core Idea

The upload contains support modules outside the Analysis I narrative. They should be loaded only when the task names them or their specialized concepts. The most reusable operational component is the dimensioned-units framework: `Scalar d` quantities live in dimension-indexed types, while `Formal` collects all dimensions into a graded commutative ring so ordinary algebra tactics can operate across propositionally equal dimensions.

## Frameworks Introduced

- **UnitsSystem: typed dimensions**: `Scalar d` encodes quantities of dimension `d`. Multiplication changes the dimension index. Two mathematically equal dimension expressions may be propositionally equal without being definitionally equal, so Lean treats the corresponding scalar types as distinct.
- **Formal-ring escape hatch**: embed scalars into `Formal` (an `AddMonoidAlgebra`-style graded ring), normalize coercions, then use `ring`. The source examples recommend `simp [← toFormal_inj]` followed by `ring`; an alternative coordinate route uses `simp [← val_inj]`.
- **Explicit casts across dimensions**: `Scalar.cast` resolves propositionally equal dimension indices when definitional reduction cannot. Do not expect standard `Coe` to solve this dependent-index situation automatically.
- **SI specialization**: `SI.lean` instantiates the dimensions and common units; explicit dimension expressions are often definitionally simple enough to reduce cast burden. `SIExamples.lean` demonstrates derived units/types.
- **Finite-choice helper**: `FiniteChoice.lean` packages finite selection results without requiring callers to rebuild the construction.
- **Finite probability**: `Probability.lean` supplies a small finitely additive probability/order API for bounded lattices.
- **Numeric/order utilities**: `Real-EReal-ENNReal.lean` collects coercion, finite-sum, `tsum`, and inequality lemmas shared by analysis/measure code; `NatBitwise.lean` and `Combinatorics.lean` provide focused combinatorial identities.
- **ExistsUnique helper**: `Tools/ExistsUnique.lean` exposes convenient choice/spec/equality/subsingleton operations for unique-existence statements.
- **Erdos/equational experiments**: the Erdos files are self-contained formalizations/examples and `equational.lean` is a separate algebra experiment; treat them as optional case studies, not prerequisites for Analysis I.

## Key Concepts

- dimension vectors and `Scalar d`;
- graded `Formal` ring;
- dimension casts and injectivity lemmas;
- SI dimensions/units;
- finite choice;
- finitely additive probability;
- Real/EReal/ENNReal bridge utilities;
- finite combinatorial product-of-sums identity;
- natural bit-index lemmas;
- unique-existence extraction;
- standalone Erdos theorem formalizations.

## Operational Procedure: Units

1. Inspect the goal's dimension indices. If the two sides differ only by commutativity/associativity of dimension addition, expect a type-level mismatch before an algebraic mismatch.
2. First try reducing definitional equalities via `simp`.
3. If dimensions remain propositionally equal, either insert `Scalar.cast` with the equality proof or move the whole equality into `Formal` using injectivity.
4. For polynomial scalar identities, use the source's preferred pattern: simplify through `toFormal_inj`, then invoke `ring`.
5. If only numeric coordinates matter, use `val_inj` and normalize the underlying values.
6. Return from `Formal`/coordinates through injectivity, keeping dimension correctness explicit.

## Other Routing Rules

- Need a finite dependent selection → inspect `Misc/FiniteChoice.lean` before using unrestricted choice.
- Need `EReal`/`ENNReal` coercion or `tsum` arithmetic → inspect `Misc/Real-EReal-ENNReal.lean` for project-specific helper lemmas.
- Need product-of-sums expansion over boolean choices → `Misc/Combinatorics.lean`.
- Need bit-index membership/powers-of-two sums → `Misc/NatBitwise.lean`.
- Need a unique witness and proof/equality API → `Tools/ExistsUnique.lean`.
- Need finite probability identities → `Misc/Probability.lean`.
- Erdos/equational modules should be treated as named examples; do not route ordinary Analysis I goals through them.

## Failure Recovery

- **“type mismatch” between `Scalar (d₁+d₂)` and `Scalar (d₂+d₁)`** → normalize dimensions or use `Scalar.cast`/`Formal`.
- **`ring` cannot see through scalar types** → embed into `Formal` first.
- **EReal inequality cannot coerce to real** → prove finiteness/nonnegativity and use the utility lemmas.
- **a helper theorem seems unrelated to book chapters** → check whether it lives under `Misc`; keep it as infrastructure, not a conceptual dependency unless imported by the target module.

## Source Map

`Misc/UnitsSystem.lean`, `UnitsSystemExamples.lean`, `SI.lean`, `SIExamples.lean`; `FiniteChoice.lean`; `Probability.lean`; `Real-EReal-ENNReal.lean`; `NatBitwise.lean`; `Combinatorics.lean`; `equational.lean`; Erdos `379`, `613`, `707`, `987`; plus `Tools/ExistsUnique.lean`. The root `Analysis.lean` imports the main subset intended for project-wide availability.

## Key Takeaways

1. Dimensioned scalar algebra often fails at the type index before it fails algebraically.
2. `Formal` is the intended normalization domain for unit-aware polynomial identities.
3. Use specialized Misc helpers when their exact domain appears; keep them out of unrelated chapter proofs.
4. Real/EReal/ENNReal utility lemmas can remove repetitive coercion and `tsum` boilerplate.
5. Standalone Erdos/equational modules are examples, not part of the Analysis I chapter dependency chain.

## Connects To

- **Chapters 6–8 / Measure Theory**: shared `EReal`/`ENNReal`, countability, and summation utilities.
- **Appendix A**: unique-existence and dependent-choice proof patterns.
