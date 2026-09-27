# Xena Formalization Cheatsheet

## Route by symptom

| Symptom | First move | Then |
|---|---|---|
| Informal theorem | Freeze types, binders, hypotheses | Audit examples; only then prove |
| `rw` cannot find occurrence | Inspect exact syntax | `change`/normalize; reverse equality; extensionality |
| `exact` “almost fits” | Check definitional vs propositional equality | `convert` or explicit bridge |
| `rfl` fails on “obvious” equality | Check recursion/definition direction | use theorem/induction/rewrite |
| `simp` grows/loops | Decide normal form | remove/reorient simp lemmas |
| `ring`/arithmetic tactic fails | Normalize and expose hypotheses | choose solver matching domain |
| Quotient “well-definedness” | Prove representative invariance | use `lift`/quotient induction |
| Repeated casts/typeclass pain | Inspect inferred types/instances | improve coercion/API layer |
| Need explicit witness from `∃` | Decide if classical choice is acceptable | choice + independence proof, or require data |
| Operation has weird edge value | Check theorem's domain contract | add/derive intended precondition |
| Large theorem blocked | Formalize statement + dependency graph | build missing reusable infrastructure |
| Published proof fails | Localize exact step | missing assumption / typo / alternate proof |
| AI proof looks convincing | Audit statement first | compile/type-check proof |
| AI definition compiles | Do not trust semantics yet | examples + characterization + expert review |
| Universal conjecture | Consider witness search | formal verification + digestion |
| Old blog/API example | Identify current Lean/mathlib | search current declaration and compile |

## Proof-state primitives

`intro` → assume binder/premise.  
`apply` / `refine` → use theorem backwards.  
`exact` → supply completed term.  
`have` → local bridge.  
`cases` / `split` / `left` / `right` → follow inductive/logical constructors.  
`induction` → use inductive recursor.  
`change` → replace target by definitionally equal target.  
`rw` → theorem equality substitution with syntactic matching.  
`convert` → align near-matching statements and generate equality side-goals.

## Equality ladder

`same syntax` → `definitionally equal` → `proved equal` → `extensionally equal` → `isomorphic/equivalent`.

Never jump down the ladder without a bridge.

## AI trust ladder

1. Human intent.
2. Formal statement/definitions semantically checked.
3. Generated proof code.
4. Kernel/type checker accepts exact declaration.
5. Optional independent checker / axiom audit.
6. Human explanation for understanding.

## SELF_CHECK

Goal correct? Preconditions present? Equality notion right? Representation suitable? Solver preconditions met? Edge cases handled? No hidden placeholders? Current API checked? AI semantics audited? Exact proof compiled? Human can find the conceptual spine?
