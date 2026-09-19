# Patterns

## Choose the Lowest Semantic Layer
**When to use**: every new syntax/metaprogram feature.

**How**: classify required information. Grammar only → syntax. Pure context-free rewrite → macro. Expected type/name resolution/local context/type classes → elaborator. Proof goals → tactic. Expression normalization/unification/construction → `MetaM`. Output rendering → delaborator/unexpander.

**Trade-offs**: lower layers are simpler and more transparent; higher layers provide more semantic information and state, increasing complexity and failure modes.

## Context-Safe Goal Inspection
**When to use**: reading or solving a metavariable/tactic goal.

**How**: obtain the `MVarId`; execute with `mvarId.withContext` or `withMainContext`; read target/local context; instantiate metavariables; normalize only as needed; construct/validate a solution; assign it; update tactic goals coherently.

**Trade-offs**: context switching is essential correctness plumbing. Skipping it may appear to work in simple cases while failing with local variables or dependent types.

## Instantiate → Normalize → Match
**When to use**: structural analysis of expressions whose shape may be hidden by solved holes or reducible definitions.

**How**: `instantiateMVars`; if the outer constructor is still unavailable, run `whnf` under an appropriate transparency; pattern-match; recurse only where the decision requires deeper normalization.

**Trade-offs**: stronger normalization increases cost and unfolding sensitivity. Avoid full `reduce` as a default.

## Transactional Unification Probe
**When to use**: testing definitional equality or speculative elaboration without committing assignments.

**How**: execute `isDefEq`/the speculative operation in `withoutModifyingState` or save state before the attempt and restore it on rejection/failure. Commit only if the caller intentionally wants inferred metavariable assignments.

**Trade-offs**: rollback concerns the relevant meta state; caches, traces, and global fresh-name generation may not be reverted.

## Locally-Nameless Binder Construction
**When to use**: building lambdas, foralls, or dependent bodies.

**How**: create temporary local free variables with `withLocalDecl`/telescope helpers; build the body using those `fvar`s; close the body with `mkLambdaFVars` or `mkForallFVars`.

**Trade-offs**: slightly higher-level API, far fewer de Bruijn mistakes. Raw `bvar` construction remains useful for specialized low-level transformations.

## Controlled Application Inference
**When to use**: applying a declaration while Lean should infer universes/implicit arguments.

**How**: start with `mkAppM` when explicit arguments constrain everything. If inference is ambiguous or some arguments must be fixed, use `mkAppOptM`/a more explicit builder. Validate that the target declaration and argument types provide sufficient constraints.

**Trade-offs**: inference reduces boilerplate but can fail under weak constraints. More explicit construction is verbose and predictable.

## Hygienic Macro Rewrite
**When to use**: context-free syntax sugar.

**How**: declare syntax; match with a quotation; capture components via antiquotation; construct replacement syntax with a quotation; preserve generated macro scopes; use explicit identifiers only for names intentionally exposed to user lookup; `throwUnsupported` for shapes another handler may own.

**Trade-offs**: excellent for transparent sugar; poor fit for type-directed semantics.

## Expected-Type-Directed Elaboration
**When to use**: custom term syntax whose interpretation depends on the expected type.

**How**: obtain expected type; if absent/metavariable and semantics need it, postpone; instantiate/normalize enough to validate; emit a focused incompatibility error when known; elaborate ordinary children with `elabTerm`; construct result with meta APIs.

**Trade-offs**: postponement composes with Lean's constraint solver but requires careful termination/diagnostics. Guessing early is simpler and fragile.

## Embedded DSL Compiler
**When to use**: a specialized mini-language should produce ordinary typed Lean values.

**How**: define semantic datatypes/functions; create a dedicated syntax category; recursively translate each syntax constructor to a semantic constructor/application; embed through a term elaborator; decide which invalid forms grammar, elaboration, or the type system rejects.

**Trade-offs**: clean separation of surface language and semantics; requires explicit policy for semantic validation and good errors.

## Meta Tactic Lift
**When to use**: one proof goal naturally transforms into zero or more metavariable goals.

**How**: implement `MVarId → MetaM (List MVarId)`-style logic; ensure solved goals are assigned; expose through `liftMetaTactic`; use tactic state helpers for integration.

**Trade-offs**: less manual goal plumbing and fewer invariant bugs; direct `setGoals` remains useful for unusual scheduling transformations.

## Assumption-by-DefEq
**When to use**: find a local hypothesis whose type solves the current target up to definitional equality.

**How**: enter goal context; read target; iterate usable local declarations; compare declaration type with target using mutation-aware `isDefEq`; assign the goal to the matching free variable; close/remove it from tactic state.

**Trade-offs**: definitional equality may mutate metavariables. Probe transactionally if a failed candidate must leave no changes.

## Round-Trip Pretty Printer
**When to use**: adding a delaborator or unexpander.

**How**: recognize a precise expression/application shape; return the intended surface syntax; allow fallback on unsupported cases; test that output reparses/re-elaborates to a definitionally equivalent expression. For unexpanders, do not assume parentheses that are inserted only by the later parenthesizer.

**Trade-offs**: readable output and notation recovery; overbroad rules can print misleading syntax.
