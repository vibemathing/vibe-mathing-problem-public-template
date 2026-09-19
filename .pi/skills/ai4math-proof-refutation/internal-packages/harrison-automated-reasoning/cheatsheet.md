# Automated Reasoning Cheatsheet

## Route in one pass
| If the task has... | Prefer | Switch when... |
|---|---|---|
| Only Boolean atoms/connectives | DPLL over definitional CNF | repeated canonical Boolean manipulation favors BDD |
| Boolean equivalence + strong sharing | Reduced ordered BDD | graph size grows sharply or ordering is poor |
| Quantifiers, no special decidable theory | Tableau/MESON or resolution refutation | specialized fragment becomes visible |
| Ground equality + uninterpreted functions | Congruence closure | quantifiers/general equalities appear |
| Equations intended as simplification | Term rewriting | no well-founded orientation / nonjoinable critical pairs |
| Unoriented first-order equality | Paramodulation/superposition family | a dedicated decision procedure applies |
| Linear integer arithmetic | Presburger/Cooper-style QE | nonlinear multiplication appears |
| Polynomial equalities / ideal membership | Gröbner basis | inequalities/order dominate |
| Real polynomial formulas | Real QE/sign methods | linear constraints admit cheaper elimination/LP |
| Several disjoint decidable theories | Purification + Nelson–Oppen-style combination | stable-infiniteness/signature assumptions fail |
| High-assurance theorem output | LCF-style kernel + replay | no proof/certificate can be reconstructed |

## Never lose these invariants
- **Equivalent** transformations preserve truth under each corresponding valuation/model.
- **Equisatisfiable** transformations preserve existence of a model; do not substitute them into arbitrary contexts as if equivalent.
- **Skolem symbols** are fresh; their arguments encode dependencies on surrounding universal variables.
- **Substitution under binders** is capture-avoiding.
- **Unification** uses an occurs-check in ordinary finite first-order terms.
- **Rewrite as simplifier** only after a termination argument; unique normal forms additionally need confluence.
- **Search cutoff** means `unknown` unless the cutoff itself is a complete bound for the fragment.

## Fast warning signs
| Smell | Diagnosis | Move |
|---|---|---|
| Equivalent CNF/DNF doubles repeatedly | normalization blowup | definitional CNF |
| Same SAT conflict reappears below unrelated decisions | chronological backtracking waste | backjump + learn conflict clause |
| BDD node count explodes after a variable | bad ordering / hard function | reorder or SAT |
| Prolog loops although a proof exists | depth-first/rule-order incompleteness | fair or iterative-deepening search |
| `x = f(x)` accepted by unifier | missing occurs-check | reject cyclic binding |
| Rewrite sequence oscillates | orientation not well-founded | change ordering or method |
| Completion emits ever more critical pairs | nontermination of completion | interreduce, use better ordering, or switch equality prover |
| QE input mixes linear and nonlinear structure | overly general eliminator will swell | split/exploit fragment |
| Theory solver communicates only local facts | missed shared-variable coordination | purify and exchange equalities/arrangements |
| Prover says “failed” after bounded Stålmarck/MESON depth | proof not found at bound | raise bound/change method; no semantic conclusion |

## Evidence to return
- SAT → satisfying assignment/model when practical.
- UNSAT/valid → proof, refutation, unsat core, or kernel-checked replay when trust matters.
- Equality simplification → normal form plus termination/confluence assumptions.
- Decision procedure → fragment/preconditions plus decision.
- General FOL timeout → `unknown`, resource bound, and next complete/specialized route.
- Impossibility result → exact metatheoretic assumptions; do not overgeneralize Gödel/Church/Tarski.
