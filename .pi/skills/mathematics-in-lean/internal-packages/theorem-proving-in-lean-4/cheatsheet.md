# Lean 4 Decision Cheatsheet

| Situation | First move | Escalate when needed |
|---|---|---|
| Unknown/type/elaboration error | `#check`, inspect goal and expected type | `#print`, `@term`, explicit/named arg, scope/import check |
| `→` or `∀` goal | `intro` / lambda | strengthen context with `have`/`suffices` |
| `∧` / `↔` goal | `constructor` / `⟨…, …⟩` | prove components separately |
| `∨` goal | choose `left`/`right` you can prove | derive branch from hypotheses; classical case split if justified |
| `∃` goal | `refine ⟨witness, ?_⟩` / `exists` | make witness/type explicit |
| Definitional equality | `rfl` | inspect reducibility/definitions |
| One known equality replacement | `rw [h]` or `rw [← h]` | target hypothesis/occurrence explicitly |
| Repetitive normalization | `simp` | `simp only [...]`, disable a rule, use `rw` |
| Equality chain | `calc` | congruence or auxiliary lemma |
| Wrong rewrite occurrence / under binder | `conv` | refine pattern/navigation with `lhs`, `rhs`, `arg`, `intro`, `congr` |
| Inductive alternatives | `cases` | preserve dependent info with `revert` or dependent match |
| Recursive-data theorem | `induction` on recursive argument | generalize context or use `fun_induction` |
| Function-control-flow theorem | `fun_induction` / `fun_cases` | datatype induction + equation lemmas |
| Termination rejected | expose structural descent | `termination_by` + `decreasing_by` |
| Indexed family mismatch | inspect constructor indices | dependent match, inaccessible patterns, custom motive |
| Instance synthesis fails | annotate input types | scope check → `inferInstanceAs` → trace search/priorities |
| Coercion fails | identify source and target types | inspect `Coe`/`CoeDep`/`CoeSort`/`CoeFun`; convert explicitly |
| Equality of functions | `funext` | pointwise proof; audit reduction expectations |
| Equality of propositions | prove `↔`, then `propext` | combine with `funext` for predicate/set equality |
| Function on quotient | representative function + respectfulness proof | `Quot.lift`, quotient induction |
| Need arbitrary witness from `Nonempty`/existence | keep constructive witness if possible | `Classical.choice`/`choose`; data definition becomes `noncomputable` |

## Fast Smells

- **Stuck metavariable** → missing expected/input type before missing theorem.
- **Induction hypothesis is useless** → wrong induction variable or context should have been generalized.
- **`cases` destroys a dependent hypothesis** → indices/equalities need preservation.
- **`simp` changes too much** → narrow to `simp only` or use `rw`.
- **Termination goal looks impossible** → measure does not actually decrease on every recursive call.
- **Instance search explodes** → first freeze input types, then inspect graph/priority.
- **`#reduce` stuck while `#eval` succeeds** → extensionality/quotient casts or other kernel-level reduction limits may be involved.
- **Choice used to construct data** → expect `noncomputable`; do not promise executable extraction.

## Final Gate

No unresolved placeholders; no invented declarations; goal shape matches method; dependencies preserved; recursion decreases; instance inputs concrete; classical/computational assumptions documented.
