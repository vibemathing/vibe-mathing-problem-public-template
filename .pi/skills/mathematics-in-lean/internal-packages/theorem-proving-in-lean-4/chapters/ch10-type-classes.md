# Chapter 10: Type Classes

## Core Idea
Type classes turn structure-like capabilities into implicit parameters resolved by search. Reliable use depends on treating instance synthesis as a constrained search graph: input types must be known, scopes and priorities affect candidates, instances can chain recursively, and coercions/decidability often rely on the same machinery.

## Frameworks Introduced
- **Capability injection through instance implicits**
  - When to use: a polymorphic function requires an operation or law associated with a type.
  - How: declare a class, require it as `[C α]`, and provide instances for concrete/composite types.
- **Recursive instance search**
  - When to use: an instance can be derived from capabilities of component types.
  - How: define an instance with its own instance-implicit prerequisites; let synthesis recursively solve them.
- **Input/output parameter discipline**
  - When to use: a multi-parameter class has parameters determined by others.
  - How: use `outParam` when an output should not block candidate selection; understand semi-output/default behavior before relying on search order.
- **Scoped inference**
  - When to use: an instance should affect only a local region or explicitly opened scope.
  - How: choose local/scoped instances instead of globally registering every candidate.
- **Decidability as computational evidence**
  - When to use: an `if`, `dite`, `decide`, or computation needs a decision procedure for a proposition.
  - How: provide/synthesize `[Decidable p]`; use classical `propDecidable` only when nonconstructive decidability is acceptable.
- **Type-class-backed coercions**
  - When to use: values should behave as another type, sort, or function.
  - How: use the appropriate coercion class and remember target/source constraints participate in instance search.

## Key Concepts
- **Class**: structure whose instances are intended to be synthesized from an instance-implicit goal.
- **Instance implicit** `[C α]`: parameter Lean resolves with type-class search.
- **Instance chaining**: an instance whose prerequisites are themselves class goals.
- **Priority**: ordering influence among instance candidates.
- **`outParam`**: marks a class parameter as an output for synthesis selection.
- **Default instance**: instance that can help commit underconstrained synthesis, used in facilities such as numeral defaults.
- **Local instance**: instance active only in a local lexical context.
- **Scoped instance**: instance activated by opening a scope.
- **`inferInstance`**: ask Lean to synthesize an instance at the expected class type.
- **`inferInstanceAs`**: request a specific class type explicitly, useful when an alias hides it.
- **`Decidable p`**: data distinguishing proof of `p` from proof of `¬p`.
- **`ToString`**: standard example of attaching a rendering operation to many types through instances.
- **`OfNat`**: class underlying overloaded numeral interpretation; default instances help resolve underconstrained numeral types.
- **Semi-output parameter behavior**: some class parameters can influence selection differently from full `outParam`; candidate order can matter, so rely on it only with a controlled instance design.
- **`Coe` / `CoeDep` / `CoeT`**: value coercion mechanisms.
- **`CoeSort`**: lets a value/type-like object be used where a sort is expected.
- **`CoeFun`**: lets an object be applied like a function.

## Mental Models
- Model type-class synthesis as **backtracking search over instance rules**. A candidate instance is a rule whose conclusion matches the goal and whose prerequisites become recursive goals.
- Separate **input inference from output inference**. If input parameters remain metavariables, the search may be stuck before it can meaningfully choose an instance.
- Treat instance priority and order as **search control**, not a substitute for a well-determined goal.
- Treat `Decidable` as **executable evidence**, stronger computationally than the proposition `p ∨ ¬p` living in `Prop`.
- Coercion search is still **typed inference**; an underconstrained target can make a coercion fail even when a conversion exists.

## Anti-patterns
- **Changing priorities before fixing stuck input metavariables**: search cannot choose reliably when the goal is underdetermined.
- **Registering overlapping global instances casually**: behavior can become import/order sensitive.
- **Depending on a scoped instance without activating the scope**.
- **Using a semantically output parameter as ordinary input**, causing search to wait on information it was supposed to infer.
- **Assuming classical proposition decidability is an algorithm**: it provides logical decidability, not constructive computational content.
- **Chaining coercions until elaboration becomes opaque**: make important conversions explicit when clarity wins.

## Code Examples
```lean
class Printable (α : Type) where
  print : α → String

instance : Printable Nat where
  print n := toString n

def render [Printable α] (x : α) : String :=
  Printable.print x

#eval render 12
```
- **What it demonstrates**: capability requirement as an inferred parameter and a concrete instance.

```lean
instance [Printable α] : Printable (Option α) where
  print
    | none => "none"
    | some x => "some " ++ Printable.print x
```
- **What it demonstrates**: instance chaining; synthesizing `Printable (Option α)` creates a prerequisite `Printable α`.

```lean
example : Decidable (2 + 2 = 4) := inferInstance

example : 2 + 2 = 4 := by
  decide
```
- **What it demonstrates**: decidability as synthesizable evidence and the `decide` tactic for a closed decidable proposition.

## Reference Tables
### Type-class failure pipeline
| Step | Question | Action |
|---|---|---|
| 1 | Are class input types concrete? | add type ascription / explicit argument |
| 2 | Is the desired instance in scope? | check imports, local/scoped activation |
| 3 | Is class hidden behind a definition? | try exact class via `inferInstanceAs` |
| 4 | Which candidates are attempted? | enable `trace.Meta.synthInstance true` |
| 5 | Are candidates competing/looping? | inspect priorities and recursive prerequisites |
| 6 | Is global inference the right design? | pass a local explicit instance if appropriate |

### Coercion class choice
| Role | Class family | Use |
|---|---|---|
| value → value type | `Coe` / `CoeT` | ordinary conversion |
| value-dependent conversion | `CoeDep` | target behavior depends on the source value |
| object used as a type/sort | `CoeSort` | container/type-like wrappers |
| object applied as function | `CoeFun` | callable structures/objects |

## Worked Example
Lean reports `failed to synthesize Printable ?m` for `render x`.
1. Do not begin by adding another instance. Inspect `#check x` and the surrounding expected type. The input type itself may still be a metavariable.
2. Add a local annotation such as `(x : Nat)` or constrain the expression's result/context until the type is fixed.
3. Run `inferInstance : Printable Nat` (or `inferInstanceAs`) to isolate synthesis from the rest of the expression.
4. If it fails, confirm the instance's module/scope is active.
5. If several instances compete or recurse, enable instance-synthesis tracing and inspect the candidate tree/priorities.
6. Once synthesis succeeds in isolation, return to the original call.

This pipeline separates elaboration failure from instance-graph failure.

## Failure Recovery
- stuck instance metavariable → fix explicit input types first.
- alias hides class head → `inferInstanceAs`/type ascription.
- scoped instance absent → `open scoped` the relevant scope or add local instance.
- recursive chain hits resource limits → inspect for cycles/overly generic instances; tune design before resource limits.
- numeral picks unexpected type → inspect expected type/default instances; annotate the numeral's type.
- coercion ambiguity → constrain target type or write the conversion explicitly.

## Key Takeaways
1. Type classes encode reusable operations as inferred parameters.
2. Instance search is recursive and backtracking; concrete inputs are its most important constraint.
3. `outParam`, default instances, scopes, and priorities are inference-control tools with distinct roles.
4. `Decidable` carries computation-relevant evidence; classical decidability should be distinguished from an algorithm.
5. Coercions use the same elaboration and instance-search ecosystem.
6. Diagnose the class goal in isolation before making global instance changes.

## Connects To
- **Ch 6**: imports, scopes, attributes, coercions, and inspection commands are essential diagnostics.
- **Ch 9**: classes share the structure/field machinery.
- **Ch 12**: classical choice and excluded middle explain `Classical.propDecidable` and the constructive/computational distinction.
