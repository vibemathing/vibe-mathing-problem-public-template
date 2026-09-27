# Patterns

## Exact Toolchain Alignment
**When to use**: before running jixia on any external project, especially after `invalid header` or internal import failures.

**How**:
1. Read the target `lean-toolchain`.
2. Select/build a jixia source version using that exact Lean version.
3. Rebuild jixia and the target artifacts.
4. Re-run inside the target's Lake environment.

**Trade-offs**: strict alignment adds build work but removes a large class of misleading runtime failures.

## Data-Product Selection
**When to use**: deciding which jixia flags to enable.

**How**: map the question to one view: module (`-m`), declaration (`-d`), symbol (`-s`), elaboration (`-e`), line (`-l`), AST (`-a`). Combine only when the task requires joins across views.

**Trade-offs**: fewer outputs reduce cost and complexity; multi-view analysis gives richer cross-links.

## Registry-Generated Plugin Plumbing
**When to use**: a new plugin fits optional setup plus final result extraction in command elaboration context.

**How**:
1. Implement optional `onLoad` and required `getResult`.
2. Register the pair in `Process.plugins`.
3. Let metaprogrammed `Options`, load, result, and parse plumbing derive from the registry name.
4. Add the matching CLI flag and schema serialization.

**Trade-offs**: low duplication and consistent behavior; unsuitable for features whose lifecycle fundamentally differs.

## Special-Path Escape Hatch
**When to use**: result generation needs post-run file path, imported compiled environment, or raw frontend state.

**How**: keep orchestration in `Main.lean`, as current Symbol and AST outputs do. Reuse general `PluginOption` output handling where practical.

**Trade-offs**: explicit custom code avoids abstraction leakage but adds another path to test.

## Intercept Then Defer
**When to use**: capture source command metadata while retaining Lean's standard elaboration.

**How**: install a higher-priority command elaborator, record the desired source information, then signal unsupported syntax so normal handling continues.

**Trade-offs**: preserves native semantics; depends on Lean elaborator extension behavior and requires version-aware testing.

## InfoTree Accumulation
**When to use**: whole-file tactic/line data across Lean versions where top-level elaboration resets command-local trees/messages.

**How**: save previous state, process one command, append previous trees/messages to the new command state, recurse.

**Trade-offs**: preserves complete analysis at the cost of retaining more frontend state.

## Goal Before/After Diff
**When to use**: explain tactic behavior.

**How**: evaluate goal snapshots in the tactic's pre-context and post-context, then attach dependency metadata for generated goals/hypotheses.

**Trade-offs**: semantically rich; depends on InfoTree/context availability.

## Statement vs Value Dependency Graph
**When to use**: theorem/definition dependency analysis.

**How**: collect constants separately from `ConstantInfo.type` and optional `value?`.

**Trade-offs**: two graphs require more careful downstream modeling but preserve the distinction between what a result states and how it is implemented/proved.

## Rendering Fallback
**When to use**: pretty printing can fail for source syntax or expressions.

**How**: store optional pretty forms and a guaranteed debug fallback where available. Consumers must preserve optionality.

**Trade-offs**: fallback strings may be less readable but prevent data loss.
