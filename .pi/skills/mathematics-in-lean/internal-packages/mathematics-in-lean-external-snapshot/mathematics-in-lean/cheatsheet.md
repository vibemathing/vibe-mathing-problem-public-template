# Decision Cheatsheet

| If the goal looks like... | First move | Escalate to |
|---|---|---|
| `∀ x, ...` / `A → B` | `intro` / `rintro` | `apply`, theorem search |
| `∃ x, P x` | choose witness with `use`/`refine` | derive witness from hypotheses via `rcases` |
| `A ∧ B` / `A ↔ B` | `constructor` | solve each branch independently |
| `A ∨ B` | `left`/`right` if known; `rcases` if assumed | `by_cases` for classical split |
| set equality | `ext x`; reduce membership | `simp only`, propositional tactics |
| algebraic identity | focused `rw` / `calc` | `ring` or `group`/`abel` |
| linear inequality | isolate monotonicity facts | `linarith` |
| concrete numerals | expose expression | `norm_num` |
| Nat/Int linear arithmetic | simplify constructors/divisibility side facts | `omega` |
| image inclusion | expose witness only if needed | switch to preimage/comap/Galois lemma |
| injectivity/surjectivity of a hom | inspect kernel/range | standard equivalence / first isomorphism |
| quotient map | find `lift`/`map` | prove relation/kernel compatibility |
| span membership/inclusion | `span_le` | `span_induction` |
| map defined by basis | `Basis.constr` | verify on basis vectors, e.g. `B.constr_basis` |
| sequence/point limit | `Tendsto` | filter basis for epsilon form |
| several “eventually” facts | `.and` / `filter_upwards` | `.mono` to strengthen consequence |
| continuity composite | compositional lemmas / `continuity` | pointwise combinator (`.dist`, `.add`, `.prodMk`) |
| derivative value | prove `HasDerivAt`/`HasFDerivAt` | convert to `deriv`/`fderiv` equality |
| integral identity | establish integrability/measurability | FTC / dominated convergence / Fubini theorem |

## Fast Failure Triage

- **Metavariable after `apply`** → name the intermediate object or use `calc`.
- **`rw` misses** → wrong orientation, hidden definition, coercion, or non-definitional match.
- **Instance search stuck** → add missing type/scalar/index information; inspect hierarchy diamond.
- **Induction IH unusable** → generalize changing parameters or strengthen to strong induction.
- **Nat subtraction/division awkward** → prove order/divisibility first or change numeric domain.
- **Quotient representative proof exploding** → back up to the quotient universal property.
- **Topology proof has repetitive epsilons** → move to filters; re-enter a basis only at the boundary.
- **Analytic expression silently defaults to zero** → establish the evidence predicate before using the value.

## Default Preference Order

1. Existing theorem at the right abstraction.
2. Constructor/destructor + small rewrite/calc chain.
3. Domain tactic on a normalized subgoal.
4. Universal property / map-comap reformulation.
5. Unfold definitions only when the public API does not expose the needed fact.
