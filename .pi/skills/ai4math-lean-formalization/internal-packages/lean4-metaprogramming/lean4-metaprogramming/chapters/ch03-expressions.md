# Chapter 3: Expressions

## Core Idea
`Expr` is Lean's elaborated term representation. Raw construction is useful for understanding and low-level work, but it requires you to preserve binding, universe, and typing invariants yourself.

## Frameworks Introduced
- **Locally nameless representation**: bound variables use de Bruijn indices; local free variables use unique free-variable identifiers.
  - When to use: understanding raw lambdas/foralls and why context-aware builders are safer.
  - How: a bound variable index counts binders outward from its occurrence; avoid leaving loose indices outside a matching binder.
- **Universe-explicit constants**: polymorphic constants carry universe level arguments at the `Expr` level.
  - When to use: constructing constants/applications manually.
  - How: supply the constant's universe levels consistently with its declaration.

## Key Concepts
- **`Expr.bvar`**: bound variable represented by de Bruijn index.
- **`Expr.fvar`**: local free variable tied to a local declaration.
- **`Expr.mvar`**: metavariable/hole with context and target type.
- **`Expr.sort`**: universe sort expression.
- **`Expr.const`**: named declaration, possibly with universe instantiations.
- **`Expr.app`**: function application node.
- **`Expr.lam` / `Expr.forallE`**: binder nodes.
- **Closed expression**: contains no loose bound variables.
- **`Level`**: representation of universe levels.

## Mental Models
Think of de Bruijn indices as relative coordinates. In a body under one binder, index `0` points at that binder; entering another binder shifts which declaration each number denotes. This makes alpha-equivalent terms structurally uniform but makes manual construction error-prone.

Think of raw `Expr` APIs as an unsafe low-level interface: they let you build structure quickly and do not automatically prove that the result is well typed. Move to `MetaM` builders when argument inference, local contexts, or binder closure are involved.

## Anti-patterns
- **Loose `bvar`s**: constructing a body containing a bound-variable index that no enclosing binder captures.
- **Ignoring universe parameters**: a polymorphic constant can be structurally named correctly yet instantiated at the wrong universe level.
- **Assuming raw constructors type-check**: construction and kernel/meta type checking are separate responsibilities.
- **Deeply nesting `.app` by hand** when `mkAppN` or meta-level application builders express intent better.

## Code Examples
```lean
-- Structural application with explicit children.
def rawApp (f x : Expr) : Expr := Expr.app f x

-- Prefer the high-level binder pattern in MetaM code:
-- withLocalDecl ... fun x =>
--   let body := ... x ...
--   mkLambdaFVars #[x] body
```
- **What it demonstrates**: low-level nodes are simple data constructors; correct binding is a separate invariant.

## Reference Tables
| Constructor | Represents | Main invariant |
|---|---|---|
| `bvar` | bound variable | index must be captured |
| `fvar` | local declaration | must be meaningful in local context |
| `mvar` | hole/goal | assignment must fit target/context |
| `const` | global declaration | name + universe levels valid |
| `app` | application | function/argument types compatible |
| `lam` | lambda | body binder indices correct |
| `forallE` | dependent function type | binder/body well scoped |

## Exercise-backed Validation
The expression solutions reinforce that de Bruijn indices and universe levels are mechanical invariants: similar-looking raw trees can represent different binders, and polymorphic constants require explicit level instantiation. Use the solutions as evidence for preferring context-aware builders in production metaprograms.

## Key Takeaways
1. Learn all major `Expr` constructors so structural patterns are readable.
2. Keep bound-variable scope and universe levels explicit when using raw constructors.
3. Prefer higher-level `MetaM` builders for ordinary applications and binders.
4. Do not infer type correctness from the fact that an `Expr` value was successfully constructed.

## Connects To
- **Ch 4**: provides safe/contextual construction, normalization, unification, and metavariables.
- **Ch 9**: proof goals are metavariables whose solutions are `Expr` proof terms.

## Operational Procedure
Before manipulating a raw expression, state the invariant you need to preserve. For a constant, confirm its declaration and universe instantiation. For an application, confirm the function and argument are intended to compose. For a binder, count which occurrences should refer to the new binder and ensure the final expression is closed where required. For transformations under nested binders, prefer opening the binder into a fresh local free variable, transforming the body in that context, and closing it again rather than manually shifting indices.

When debugging an expression tree, inspect it structurally first, then ask the meta layer for its type. A tree that prints plausibly can still be malformed or ill typed; raw syntax-like appearance is weak evidence. Use kernel/meta checks as the correctness boundary.
