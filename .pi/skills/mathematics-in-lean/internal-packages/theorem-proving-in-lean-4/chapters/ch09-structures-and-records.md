# Chapter 9: Structures and Records

## Core Idea
Structures package named fields into a one-constructor inductive type and generate projections, constructor support, and convenient object/update syntax. Use them when the important interface is a stable collection of named components rather than positional constructor arguments.

## Frameworks Introduced
- **Named-field data modeling**
  - When to use: a value has several semantically distinct components.
  - How: declare a `structure`, construct values with named fields, and access fields through projections or dot notation.
- **Persistent record update**
  - When to use: create a value differing from an existing record in a few fields.
  - How: use `{ old with field := newValue }` rather than rebuilding every unchanged field.
- **Structural reuse with inheritance**
  - When to use: several record types share a common field set or a richer record should extend a smaller interface.
  - How: use `extends`, supplying parent objects/fields as appropriate.

## Key Concepts
- **Structure**: specialized one-constructor inductive declaration with named fields.
- **Field**: named constructor component.
- **Projection**: generated function retrieving a field.
- **Record/object syntax**: `{ field := value, ... }` construction syntax.
- **Record update**: `{ x with field := value }` syntax copying unspecified fields.
- **Dot notation**: syntax that inserts a structure value into a suitable explicit parameter position.
- **Inheritance / `extends`**: composition of structure fields through parent structures.

## Mental Models
- Treat a structure declaration as **constructor + projections + naming discipline**. The logical foundation remains inductive types.
- Prefer named-field construction as an **API-stability tool**: readers see what each value means and field order is less significant.
- Think of record update as **immutable copying with selected replacement**.
- Use `extends` for **interface composition** when the inherited fields represent a genuine reusable abstraction.

## Anti-patterns
- **Using positional constructor arguments for a wide record** when named fields communicate intent better.
- **Expecting Lean to infer a record type without enough expected-type information**: several structures can share field names.
- **Creating deep inheritance only to save typing**: field reuse should correspond to a meaningful parent interface.
- **Assuming dot notation is object-oriented dispatch**: it is elaboration syntax based on argument positions/types, not runtime method lookup.

## Code Examples
```lean
structure Point where
  x : Float
  y : Float

#check Point.x
#check Point.y
```
- **What it demonstrates**: a structure generates named projections.

```lean
def origin : Point := { x := 0.0, y := 0.0 }

def moveX (p : Point) (dx : Float) : Point :=
  { p with x := p.x + dx }
```
- **What it demonstrates**: object syntax, projections, dot notation, and record update.

```lean
structure Named where
  name : String

structure Employee extends Named where
  id : Nat
```
- **What it demonstrates**: a richer record reuses a parent structure's fields.

## Reference Tables
| Need | Mechanism | Check |
|---|---|---|
| construct full record | `{ field := value, ... }` | expected structure type is known |
| read field | `p.field` / projection | projection type matches desired receiver |
| modify one/few fields | `{ p with field := new }` | unchanged fields should be copied |
| share common fields | `extends Parent` | parent is a meaningful abstraction |
| disambiguate object literal | type ascription | field names alone may underconstrain type |

## Worked Example
Suppose a configuration has `host`, `port`, and `secure` fields. A function should switch only the port.
1. Model the configuration as a structure so each component is named.
2. Give the original value type `Config` explicitly where needed; this helps object syntax resolve field names.
3. Implement the transformation as `{ cfg with port := newPort }`.
4. Use `cfg.host` and related projections rather than destructuring/reconstructing all fields.
5. If multiple configuration structures later share connection identity fields, factor those into a parent only if code genuinely consumes the common interface.

## Failure Recovery
- record literal has ambiguous/missing type → add a type ascription or expected type.
- dot notation selects no declaration → inspect the projection/function's explicit parameter order with `#check`.
- inherited field initialization is unclear → inspect generated parent projection/constructor and use explicit parent object syntax if clearer.

## Key Takeaways
1. Structures are record-oriented inductive types with generated field projections.
2. Named construction and update syntax improve maintainability and elaboration clarity.
3. Dot notation is typed syntactic convenience, not dynamic dispatch.
4. `extends` expresses reusable record interfaces and supports multiple-parent composition.
5. Expected type information remains important when record field names are insufficient to determine the structure.

## Connects To
- **Ch 7**: structures are grounded in one-constructor inductive types.
- **Ch 10**: type classes use structure-like declarations to represent inferred capabilities.
- **Ch 6**: expected types and dot-notation elaboration are part of the broader interaction model.
