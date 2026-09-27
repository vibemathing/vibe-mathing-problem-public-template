---
name: lean4-metaprogramming
description: Knowledge base from "Metaprogramming in Lean 4" by Arthur Paulino, Damiano Testa, Edward Ayers, Evgenia Karunus, Henrik Böving, Jannis Limperg, Siddhartha Gadgil, and Siddharth Bhat. Use for Lean 4 metaprogramming involving Expr, MetaM, syntax, macros, elaborators, tactics, DSLs, options, delaboration, or pretty printing.
when_to_use: Lean 4 metaprogramming, write a Lean macro, custom syntax in Lean, write a Lean elaborator, manipulate Expr, MetaM metavariables, definitional equality Lean, build a custom tactic, TacticM goals, embed a DSL in Lean, syntax quotations and hygiene, command elaboration, term elaboration postponement, Lean delaborator or unexpander, Lean pretty printer
allowed-tools: Read Grep
argument-hint: "[topic, API, problem, or chapter number]"
---

# Metaprogramming in Lean 4
**Authors**: Arthur Paulino, Damiano Testa, Edward Ayers, Evgenia Karunus, Henrik Böving, Jannis Limperg, Siddhartha Gadgil, Siddharth Bhat | **Pages**: n/a (site mirror) | **Source units**: 17 | **Topic files**: 12 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when a task changes how Lean parses, elaborates, constructs, transforms, proves, or prints code. Start here to choose the abstraction layer, then load only the relevant chapter file.

- `/lean4-metaprogramming` — load the routing rules and core mental models.
- `/lean4-metaprogramming MetaM backtracking` — read the relevant topic file before proposing code.
- `/lean4-metaprogramming ch09` — load the tactics file.
- Ask for the chapter list to browse the topic map.

For API-sensitive implementation, inspect the user's installed Lean/library version before claiming an exact signature. The book teaches durable architecture plus concrete APIs from its snapshot; Lean metaprogramming APIs can evolve.

## Operational Router

Classify the task before writing code:

| Need | Primary route | Load |
|---|---|---|
| Understand/build kernel terms | `Expr`, binders, universes | ch03 |
| Inspect/unify/reduce terms or manage holes | `MetaM` | ch04 |
| Define parsers/precedence/categories | syntax layer | ch05 |
| Pure syntax-to-syntax sugar | macro layer | ch06 |
| Meaning depends on types/context/expected type | elaboration layer | ch07 |
| Build a typed embedded language | syntax + elaboration | ch08 |
| Manipulate proof goals | tactic layer | ch09 |
| Find an API quickly | cheat sheet | ch10 |
| Add configurable behavior | options | ch11 |
| Control output syntax/printing | delaboration/unexpansion | ch12 |

When two routes seem plausible, choose the lowest layer that has enough semantic information. A macro is suitable for transparent syntax rewriting. Type-directed behavior belongs in elaboration. Proof-state behavior belongs in tactics, usually backed by `MetaM`.

## Core Frameworks & Mental Models

### 1. Treat Lean metaprogramming as a staged compiler pipeline
Think in transformations: source text is parsed into `Syntax`; macros repeatedly rewrite `Syntax → Syntax`; elaboration interprets syntax in context and produces `Expr`; the kernel checks the resulting terms. Printing travels in the opposite direction through delaboration, parenthesization, and formatting. Locate a bug at the stage where its information first exists.

**Decision rule:** if the problem is lexical/grammatical, change syntax. If the transformation is context-free sugar, use a macro. If it needs expected types, local declarations, coercions, type-class search, or unification, use an elaborator. If it changes proof goals, use a tactic.

### 2. Regard `Expr` as kernel-facing structure with invariants
`Expr` contains bound variables, free variables, metavariables, sorts, constants, applications, lambdas, foralls, lets, literals, metadata, and projections. Raw constructors are powerful and assume you maintain binding, universe, and typing invariants. Prefer higher-level `MetaM` builders when context or inference matters.

For binders, use the locally nameless discipline: temporary free variables while constructing bodies, then close them with `mkLambdaFVars` or `mkForallFVars`. Avoid loose de Bruijn indices in ordinary metaprogramming.

### 3. Treat metavariables as mutable proof obligations
A metavariable has a local context and target type; assignment fills the corresponding hole. Existing expressions containing a metavariable do not mutate structurally when it is assigned. Call `instantiateMVars` before structural inspection when assignments may matter.

Run metavariable operations under the correct local context, commonly with `mvarId.withContext`. Be cautious with delayed assignments and metavariable depth; a simple `isAssigned` test does not capture every delayed state.

### 4. Normalize only as far as the decision requires
Use weak-head normalization when you need the outer constructor after unfolding enough computation. Use full reduction only when a fully normalized term is genuinely required. Select transparency intentionally: more transparency can make equality succeed but increases unfolding and can change behavior.

`isDefEq` is a unification operation as well as a predicate: it may assign metavariables. Do not treat it as pure. If probing must leave state unchanged, wrap it in a state-preserving or rollback pattern.

### 5. Make state mutation and rollback explicit
A caught exception does not automatically restore `MetaM` state. For speculative operations, save/restore state or use helpers such as `withoutModifyingState` or `observing?` according to the intended commit semantics. Remember that restoring meta state does not necessarily undo caches, traces, or global name generation.

### 6. Use quotations to preserve syntax structure and hygiene
Construct and match syntax with syntax quotations and antiquotations when possible. Typed syntax (`TSyntax`) carries category information and improves matching. Macro hygiene uses scopes to prevent accidental capture. Generated internal names should remain hygienic; intentionally user-visible identifiers may need explicit construction such as `mkIdent`.

### 7. Let elaborators own semantic ambiguity
A term elaborator receives syntax plus an optional expected type. If correct meaning depends on an expected type that is still unknown, postpone instead of guessing. Reject unsuitable expected types clearly, then recursively delegate ordinary subterms to Lean's elaborator.

Command elaborators may update the environment, log, perform IO, or report errors. Multiple handlers can coexist; unsupported syntax should yield to other handlers when overloading is intended.

### 8. Tactics are goal-list programs over `MetaM`
`TacticM` adds a list of current goals on top of elaboration/meta capabilities. Inspect the main goal under its context, perform a `MetaM` transformation, then replace or close goals coherently. Use `liftMetaTactic` when a low-level function naturally maps one metavariable goal to zero or more new goals.

Closing a goal means assigning its metavariable to a proof term. Merely editing the goal list can hide an unsolved metavariable and create inconsistent tactic behavior.

### 9. Validate printer extensions by round-trip meaning
Delaborators turn `Expr` into `Syntax`; unexpanders reverse selected application shapes into surface notation. A successful pretty-printer rule must yield syntax that elaborates back to an equivalent expression. Unexpanders run before parenthesization, so avoid patterns that assume parentheses are already present.

## Failure Recovery

When metaprogramming code fails, route by symptom:

1. **Parser rejects input or precedence is wrong** → inspect syntax category, precedence, associativity, repetition/separator parser, and longest-match interactions; load ch05.
2. **Macro expansion captures names or expands incorrectly** → inspect quotations, antiquotations, macro scopes, handler order, and `throwUnsupported`; load ch06.
3. **Elaborator lacks enough type information** → inspect expected type and metavariables; postpone if meaning is underdetermined; load ch07.
4. **Expression match sees an unexpected metavariable/application head** → run in the correct context, `instantiateMVars`, then `whnf` only as needed; load ch04.
5. **A probe changes later behavior** → assume unification/state mutation; isolate or restore state; load ch04.
6. **`mkAppM` cannot infer arguments** → supply more explicit arguments or use `mkAppOptM`; ensure types and context constrain implicits; load ch04.
7. **Tactic reports success but proof state is broken** → verify every removed goal was assigned or deliberately replaced; load ch09.
8. **Pretty output cannot be re-elaborated** → reject the custom delaboration/unexpansion and fall back to a safer rendering; load ch12.
9. **Exact API name/signature differs** → search the installed Lean source/docs and adapt the book's method to that version; keep semantic invariants unchanged.

## SELF_CHECK

Before finalizing a Lean metaprogramming answer or implementation:

- What stage owns the user's problem: syntax, macro, elaboration, meta, tactic, or printer?
- Does the chosen method have enough information at that stage?
- Are all inspected metavariables instantiated enough for the operation?
- Is the correct local context active for free variables and goals?
- Could `isDefEq`, elaboration, or tactic code mutate state during a “check”?
- Are binder and universe invariants preserved?
- Is normalization/transparency stronger than necessary?
- If expected type is unknown, should elaboration postpone?
- If goals are removed, were their metavariables actually assigned?
- Does generated/printed syntax preserve hygiene and re-elaborate to the intended meaning?
- If an API detail is version-sensitive, was it verified in the target Lean environment?

## Chapter Index

| # | Topic | Key capability |
|---|---|---|
| [ch01](chapters/ch01-introduction.md) | Introduction | choose the metaprogramming layer |
| [ch02](chapters/ch02-overview.md) | Overview | reason through the full pipeline |
| [ch03](chapters/ch03-expressions.md) | Expressions | construct and inspect `Expr` safely |
| [ch04](chapters/ch04-metam.md) | MetaM | metavariables, reduction, unification, backtracking |
| [ch05](chapters/ch05-syntax.md) | Syntax | grammars, categories, precedence, typed syntax |
| [ch06](chapters/ch06-macros.md) | Macros | hygienic syntax rewriting |
| [ch07](chapters/ch07-elaboration.md) | Elaboration | command/term elaborators and postponement |
| [ch08](chapters/ch08-dsls.md) | DSLs | elaborate embedded languages into typed terms |
| [ch09](chapters/ch09-tactics.md) | Tactics | proof-goal inspection and transformation |
| [ch10](chapters/ch10-cheat-sheet.md) | Lean 4 Cheat-sheet | rapid API routing |
| [ch11](chapters/ch11-options.md) | Options | configurable metaprograms |
| [ch12](chapters/ch12-pretty-printing.md) | Pretty Printing | delaboration and unexpansion |

## Topic Index

- **Backtracking / saveState** → ch04
- **Bound variables / de Bruijn** → ch03, ch04
- **CommandElab** → ch07
- **Definitional equality / isDefEq** → ch04
- **Delab / delaborator** → ch12
- **DSL** → ch08
- **Expr constructors** → ch03
- **Expected type / postponement** → ch07
- **Free variables / local context** → ch04
- **Hygiene / macro scopes** → ch06
- **Metavariables / MVarId** → ch04, ch09
- **mkAppM / mkAppOptM** → ch04
- **Options / register_option** → ch11
- **Precedence / associativity** → ch05
- **Quotations / antiquotations** → ch05, ch06
- **Reduction / whnf / transparency** → ch04
- **Syntax categories / TSyntax** → ch05
- **TacticM / goals** → ch09
- **Unexpander** → ch12
- **Universes / Level** → ch03

## Supporting Files

- [glossary.md](glossary.md) — important terms and APIs.
- [patterns.md](patterns.md) — reusable procedures and decision patterns.
- [cheatsheet.md](cheatsheet.md) — one-page routing and API reference.
- [provenance.md](provenance.md) — source-unit coverage and derivation labels.
- [evals.md](evals.md) — trigger, routing, recovery, and fresh-agent tests.

## Scope & Limits

This skill captures the uploaded 2026-09-12 mirror of the book and its readable source units. It is optimized for applying the book's methods, not reproducing its prose. Four diagrams in the Overview page were external image references rather than bundled image files; their surrounding explanatory text is covered. Exact Lean API signatures may differ across releases, so version-specific implementation should be checked against the target Lean installation.
