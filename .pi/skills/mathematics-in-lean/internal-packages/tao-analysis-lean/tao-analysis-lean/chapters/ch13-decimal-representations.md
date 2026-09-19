# Appendix B: Decimal Representations

## Core Idea

Appendix B formalizes decimal representations for Mathlib naturals and reals as explicit mathematical data, separate from Lean's built-in numeral syntax. It is useful for reasoning about digit expansions, conversion, surjectivity, terminating versus nonterminating representations, and the familiar non-uniqueness created by trailing 9s.

## Frameworks Introduced

- **Representation type separate from value type**: `Digit` and decimal structures encode syntax/data; conversion functions map them into `ℕ`, nonnegative reals, or reals. Keep representation equality distinct from equality of represented values.
- **Evaluation map analysis**: prove basic evaluation formulas, then establish surjectivity (every target value has a representation) and characterize failures of injectivity.
- **Terminating/nonterminating split**: uniqueness often requires excluding the degenerate dual expansions associated with terminating decimals and repeating 9s. State that condition before attempting injectivity.
- **Independent from `OfNat`**: these objects model decimal mathematics, while Lean's literal notation already uses `OfNat`. Do not expect parser numerals to elaborate to the appendix structures automatically.
- **Reuse of standard naturals**: Appendix B works with Mathlib `ℕ`; Chapter 2's custom naturals have already been retired.

## Key Concepts

- `Digit` with values 0–9;
- decimal expansion data and evaluation;
- place value and powers of ten;
- natural-number representation;
- nonnegative-real and signed-real decimal representations;
- surjectivity of evaluation;
- noninjectivity and terminating decimals;
- uniqueness for appropriately normalized/nonterminating forms.

## Operational Procedure

1. Identify whether a goal concerns the **representation** or the **evaluated numeric value**.
2. If it concerns value, rewrite through the appendix's `toNat`/`toNNReal`/real-evaluation function before using arithmetic.
3. For existence, construct digits/expansion data and then prove the evaluator returns the target; or invoke the provided surjectivity theorem when the task is downstream of representation construction.
4. For equality of representations, first ask whether injectivity is actually true. If trailing-zero/repeating-nine ambiguity applies, add the relevant normalization/nonterminating condition.
5. For arithmetic on evaluated decimals, move to ordinary `ℕ`/`ℝ`, prove the numerical identity, then transport back only if a representation theorem is required.
6. When digit indexing appears, check the direction and base-10 exponent convention explicitly; avoid assuming the prose's visual left-to-right position equals the Lean index.

## Decision Table

| Target | Route |
|---|---|
| show decimal denotes a number | unfold/evaluate representation |
| produce a decimal for a number | use construction/surjectivity |
| prove two decimals equal from equal values | first establish injectivity conditions |
| show two different decimals have same value | use terminating/repeating-nine phenomenon |
| use arithmetic theorem | evaluate to `ℕ`/`ℝ`, reason there |

## Failure Modes

- **Lean numeral notation has wrong type** → distinguish a built-in numeral from the custom `Digit`/decimal structure and annotate the type.
- **evaluation is not injective** → expected behavior; inspect terminating/nonterminating assumptions.
- **proof mixes Appendix B with Chapter 2 naturals** → use Mathlib `ℕ` here; the custom Chapter 2 model is not the active representation.
- **digit sequence equality is hard** → prove pointwise digit equality after extracting uniqueness conditions, rather than comparing the evaluated sums alone.

## Anti-patterns

- Treating decimal syntax as definitional equality with the represented real number.
- Assuming every real has a unique raw decimal representation.
- Reconstructing numerical arithmetic at the digit level when the theorem only concerns evaluated values.
- Conflating this appendix with Lean's internal `OfNat` elaboration.

## Source Map

- `Analysis/Appendix_B_1.lean` — `Digit`, natural-number decimal representation, evaluator and supporting lemmas.
- `Analysis/Appendix_B_2.lean` — nonnegative-real/real decimal representations, surjectivity, explicit noninjectivity, terminating-decimal and uniqueness results.

## Key Takeaways

1. Representation identity and numeric equality are separate proof domains.
2. Push arithmetic through the evaluation map unless the representation itself is the subject.
3. Decimal non-uniqueness is a theorem feature, not a Lean artifact.
4. State normalization/nontermination conditions before claiming injectivity.
5. Use Mathlib `ℕ`/`ℝ` as the semantic codomain for Appendix B calculations.

## Connects To

- **Chapter 5–6**: real-number properties used to reason about evaluated real decimals.
- **Appendix A**: equality/extensionality tools for representation uniqueness proofs.
