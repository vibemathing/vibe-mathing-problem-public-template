# Chapter 11: Options

## Core Idea
Lean options are scoped name/value settings that metaprograms can register, read through a `MonadOptions` context, and override locally with `set_option`.

## Frameworks Introduced
- **Scoped configuration pattern**:
  1. Register a named option with metadata/default behavior.
  2. Read it from `getOptions` or the generated option accessor.
  3. Allow users to override it globally or in a local `set_option ... in` scope.
  4. Keep behavioral defaults stable when the option is absent.

## Key Concepts
- **`Options`**: key-value map from `Name` to supported data values.
- **`DataValue`**: option payload kinds such as string, bool, name, nat, int, or syntax-related data.
- **`MonadOptions`**: capability for retrieving active options.
- **`getOptions`**: obtains current option map.
- **`Option.get`**: reads a typed option with its default behavior.
- **`register_option`**: declares an option for users/tooling.
- **`set_option`**: overrides an option, optionally in a scoped command/term region.

## Mental Models
Treat options as dependency-injected configuration for metaprograms. Read them at the layer where behavior changes, rather than threading ad hoc booleans through unrelated APIs.

Keep option names hierarchical and behavior deterministic. An option should tune a method that is already well defined; it should not silently switch unrelated semantics.

## Anti-patterns
- **Relying on a freshly registered option too early in the same initialization context**: registration timing can restrict immediate use.
- **Reading raw option keys everywhere**: centralize typed access so defaults and names remain consistent.
- **Using options for semantic choices that should be explicit syntax or arguments**.

## Code Examples
```lean
register_option myTool.trace : Bool := {
  defValue := false
  descr := "enable diagnostic tracing for myTool"
}

-- Later, in a MonadOptions-capable context:
let enabled := myTool.trace.get (← getOptions)
```
- **What it demonstrates**: registered, typed, scoped configuration.

## Reference Tables
| Need | Mechanism |
|---|---|
| Declare tunable behavior | `register_option` |
| Read active settings | `getOptions` |
| Read one registered option | generated `Option.get` accessor |
| Temporary override | `set_option ... in ...` |

## Key Takeaways
1. Use options for orthogonal configurable behavior.
2. Read them through `MonadOptions` rather than global mutable state.
3. Keep defaults explicit and scoped overrides local.
4. Account for declaration/initialization timing when registering new options.

## Connects To
- **Ch 7**: elaborators commonly read options to tune diagnostics/behavior.
- **Ch 12**: pretty-printing behavior is often option-controlled.

## Operational Procedure
Before adding an option, specify the behavior it controls, its default, its scope, and the layer that reads it. A diagnostic/verbosity option can be read by an elaborator or tactic without changing the meaning of accepted programs. A pretty-printing option can change rendering while preserving the represented expression. If toggling an option would silently change the semantics of a custom term, prefer explicit syntax or an argument unless the surrounding Lean API already treats that choice as configuration.

Register the option once, then expose one typed accessor path. At each read site, obtain the active `Options` from the current monad rather than caching a global copy, because `set_option ... in` establishes a local override. Test the default, an explicit global/local setting, and restoration after the scoped region ends. For nested tools, document whether the inner metaprogram inherits the caller's active options; with `MonadOptions`, inheritance is part of the contextual design.

## Failure Modes
- **Unknown option at use site**: confirm registration/initialization order and that the declaration is available in the imported environment.
- **Scoped override appears ignored**: confirm the implementation reads `getOptions` inside the scope instead of using a previously cached value.
- **Option type mismatch**: use the registered typed accessor rather than decoding the underlying key/value map manually.
- **Configuration leaks into unrelated behavior**: narrow the option's read sites and document its exact effect.

## Design Checklist
1. Name the option in a namespace that identifies the owning tool.
2. Give it a stable default and user-facing description.
3. Read it only where the controlled behavior occurs.
4. Keep semantics independent from diagnostic/printing options when possible.
5. Test scoped `set_option ... in` behavior.
6. Treat initialization restrictions as an environment-ordering issue, not a reason to invent mutable globals.

Options are especially useful in metaprogramming because elaborators, tactics, and pretty printers already execute inside contextual monads. Lean's option mechanism lets those tools share configuration without turning every helper signature into a long chain of explicit flags.
