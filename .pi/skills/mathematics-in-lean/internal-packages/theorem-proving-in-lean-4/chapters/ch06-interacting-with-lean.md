# Chapter 6: Interacting with Lean

## Core Idea
Many apparent proof failures are environment or elaboration failures. Lean provides commands, namespace/scope mechanisms, attributes, options, and pretty-printing controls that let you inspect what the system actually understood before changing the mathematics.

## Frameworks Introduced
- **Inspect before edit**
  - When to use: unknown identifier, unexpected type, implicit argument failure, coercion issue, or confusing notation.
  - How: use `#check`, `#print`, `#eval`, `#reduce`, and pretty-printer options to expose the elaborated object.
- **Environment-state diagnosis**
  - When to use: code behaves differently after imports, namespace openings, scopes, or local attributes.
  - How: identify which imports/namespaces/scopes/attributes/options are active and keep changes local when possible.
- **Parser/elaborator separation**
  - When to use: notation parses but produces an unexpected term, or a token fails before type checking.
  - How: distinguish syntax/fixity/precedence issues from elaboration/type issues.
- **Implicitness spectrum**
  - When to use: API design or inference behaves differently depending on argument visibility.
  - How: understand ordinary explicit arguments, strong implicit `{}`, weak implicit `⦃⦄`/`{{}}`, and instance implicits `[]`.

## Key Concepts
- **Message**: error, warning, or informational diagnostic emitted by Lean.
- **`#guard_msgs`**: command used to assert expected messages, useful in examples/tests.
- **Import**: loads declarations from another module; imports are transitive.
- **Section**: local grouping where variables/options/attributes can influence declarations without creating a name prefix by itself.
- **Namespace**: creates name prefixes and affects name resolution.
- **`open` / `export` / `protected`**: mechanisms controlling accessible names.
- **Attribute**: metadata registering a declaration with an extensible mechanism, e.g. simplification or instances.
- **Notation precedence/fixity**: parser rules controlling grouping and associativity.
- **Coercion**: elaborator-inserted conversion from one expected type role to another.
- **Option**: configurable behavior, commonly scoped to a section/command.
- **Auto-bound implicit**: undeclared identifier that Lean may automatically turn into an implicit parameter when `autoImplicit` is enabled.
- **Implicit lambda / placeholder `·`**: concise syntax for simple anonymous functions when the expected function type supplies missing binders.
- **Named/default argument**: call syntax that avoids brittle positional argument lists; `..` can reuse defaults where supported.

## Mental Models
- Use the Lean environment as a **stateful compiler context**: imports, namespace openings, scopes, local attributes, and options can affect later elaboration.
- Think of pretty printing as a **debugging lens**. The default printer hides details for readability; turn on explicit arguments/universes when those hidden details cause the error.
- Treat notation as **surface syntax with precedence**, then separately reason about the typed term it elaborates to.
- Treat `autoImplicit` as convenience with a **typo risk**; disabling it is useful when a file should require all parameters to be intentional.

## Anti-patterns
- **Editing a proof before reading the exact error and elaborated type**.
- **Assuming `open Namespace` imports a module**: imports and name opening solve different problems.
- **Making a global attribute/option change to fix one proof** when a local change would preserve predictability.
- **Trusting default pretty-print output as the whole declaration** when hidden implicits or universes matter.
- **Allowing accidental auto-bound variables** in definitions meant to have a controlled interface.

## Code Examples
```lean
#check Nat.succ
#print Nat.succ
#eval Nat.succ 4
#reduce Nat.succ 4
```
- **What it demonstrates**: inspect a type/definition and distinguish evaluation-style commands.

```lean
set_option pp.explicit true in
#check List.map
```
- **What it demonstrates**: temporarily expose hidden parameters without globally changing output.

```lean
set_option autoImplicit false

def id' {α : Type} (x : α) : α := x
```
- **What it demonstrates**: require parameters to be explicitly declared.

```lean
#check @List.map
```
- **What it demonstrates**: expose implicit arguments when inference or call syntax is unclear.

## Reference Tables
| Symptom | Inspect | Typical repair |
|---|---|---|
| unknown identifier | imports + qualified name | add correct import or namespace qualification |
| surprising implicit args | `#check @decl` | annotation/named implicit argument |
| universe/type details hidden | `pp.universes`, `pp.explicit`, `pp.all` | understand real declaration before editing |
| notation groups unexpectedly | precedence/fixity declaration | parenthesize or use correct notation |
| coercion inserted/fails | source and expected target type | add type annotation or explicit conversion |
| behavior depends on declaration registration | attributes | localize or inspect `[simp]`, instance, etc. |
| typo silently becomes parameter | `autoImplicit` | `set_option autoImplicit false` |
| call has many optional/default args | declaration type | use named args / `..` syntax where applicable |
| trivial anonymous function is noisy | expected function type | use implicit lambda / `·` only when its inferred binders stay obvious |

## Worked Example
A theorem fails with “failed to synthesize” near a polymorphic expression. A disciplined diagnosis is:
1. `#check` the expression and `#check @declaration` to expose hidden parameters.
2. If the target class/type is hidden behind notation, add parentheses and a local type ascription.
3. Confirm the required module is imported and any scoped instances/notation are open.
4. Turn on `pp.explicit` or `pp.all` if the error still hides a metavariable relationship.
5. Only then change the proof or provide an explicit instance/argument.

This sequence prevents a proof-level workaround from masking an environment problem.

## Key Takeaways
1. Lean exposes enough environment information to diagnose most elaboration problems directly.
2. Imports, namespaces, scopes, attributes, and options are separate axes of environment state.
3. Pretty-printer detail is an active debugging tool.
4. Implicit arguments reduce call-site noise while increasing the importance of expected-type information.
5. Notation/parsing errors and type/elaboration errors should be diagnosed at different layers.
6. `autoImplicit false` is valuable in code where accidental parameters are costly.

## Connects To
- **Ch 2**: elaboration and implicit arguments are grounded in dependent type theory.
- **Ch 5**: tactic failures become easier to understand when the actual types/environment are visible.
- **Ch 10**: type-class inference and coercions add additional elaboration state and tracing tools.
- **Ch 12**: `#reduce`, `#eval`, and declaration inspection matter when axioms affect computation.
