# Provenance Map

Labels: **SOURCE_DERIVED** = directly grounded in source behavior; **STRUCTURAL_SYNTHESIS** = operational rule synthesized across multiple source examples; **IMPLEMENTATION_DECISION** = packaging/agent design choice.

| Capability | Class | Source anchor | Interpretation |
|---|---|---|---|
| route_goal_shape | STRUCTURAL_SYNTHESIS | all nine active worlds | Cross-world routing over recurring goal forms. |
| close_exact_goal | SOURCE_DERIVED | Implication L01-L02 | Exact match and normalize-before-exact. |
| rewrite_precisely | SOURCE_DERIVED | Tutorial L02,L04,L06,L08; Power L07; AdvMul L10 | Direction, argument precision, occurrence control. |
| normalize_numerals | SOURCE_DERIVED | Tutorial L03,L07,L08; TutorialLemmas | Bridge numerals to succ form. |
| induct_on_recursive_argument | STRUCTURAL_SYNTHESIS | Addition; Multiplication; Power | Repeated alignment of induction with second-argument/exponent recursion. |
| generalize_for_induction | SOURCE_DERIVED | AdvMultiplication L09; Tactic/Induction | Use generalized IH when another variable changes. |
| derive_mirror_by_commutativity | SOURCE_DERIVED | Multiplication L05,L08; AdvAddition mirror lemmas | Reuse one-sided laws after commutativity. |
| ac_rearrange | SOURCE_DERIVED | Addition L04-L05; Algorithm L01-L04; Tactic/SimpAdd | Manual then controlled automated AC normalization. |
| route_implication | SOURCE_DERIVED | Implication L03-L07 | Forward evidence and backward goal modes. |
| prove_negation_by_false | SOURCE_DERIVED | Implication L08-L11; PeanoAxioms | ≠ as implication to False plus constructor separation. |
| case_split_natural | SOURCE_DERIVED | AdvAddition L05; AdvMultiplication; LessOrEqual | Use cases when constructor shape alone decides. |
| construct_order_witness | SOURCE_DERIVED | LessOrEqual L01-L04,L08-L11; MyNat/LE | ≤ as existential additive gap. |
| unpack_order_witness | SOURCE_DERIVED | LessOrEqual L04-L11 | Extract witness/equality with cases. |
| construct_or_split_disjunction | SOURCE_DERIVED | LessOrEqual L07-L11 | left/right/cases routing. |
| cancel_addition | SOURCE_DERIVED | AdvAddition L01-L04 | Additive cancellation and self-equality. |
| decompose_zero_sum | SOURCE_DERIVED | AdvAddition L05-L06 | Constructor proof that zero sum has zero summands. |
| order_reasoning | STRUCTURAL_SYNTHESIS | LessOrEqual World | Unifies witness-based reflexivity/transitivity/antisymmetry/totality. |
| classify_bounded_natural | SOURCE_DERIVED | LessOrEqual L10-L11 | Small upper bound to finite disjunction. |
| nonzero_to_successor | SOURCE_DERIVED | AdvMultiplication L03-L04 | Nonzero constructor bridge. |
| multiplication_nonzero_route | SOURCE_DERIVED | AdvMultiplication L02,L07,L08 | Product zero/nonzero case structure. |
| cancel_multiplication | SOURCE_DERIVED | AdvMultiplication L09-L10 | Cancellation with nonzero side condition. |
| decide_closed_mynat | SOURCE_DERIVED | Algorithm L07-L09; MyNat/DecidableEq; Tactic/Decide | Recursive decision and closed computation. |
| respect_game_tactic_semantics | STRUCTURAL_SYNTHESIS | Game/Tactic/*.lean | Cross-cutting compatibility guard. |
| handle_flt_boundary | SOURCE_DERIVED | Power L10; Tactic/Xyzzy | Axiom-backed game escape hatch must be disclosed. |
| skill packaging / routing files | IMPLEMENTATION_DECISION | book-to-skill-master spec | Progressive loading, references, diagnostics, evals. |
