# Glossary

**Antiquotation** — splice or capture syntax inside a syntax quotation; repeated/optional forms support arrays and optional fragments. (Ch 5–6)

**Bound variable (`bvar`)** — variable represented by a de Bruijn index relative to surrounding binders. (Ch 3)

**Command elaborator** — handler that assigns semantics to command syntax and may inspect/update Lean's environment, log messages, or perform allowed effects. (Ch 7)

**Closed expression** — expression with no loose bound variables. (Ch 3)

**De Bruijn index** — numeric binder reference counting outward from the variable occurrence. (Ch 3)

**Delayed assignment** — metavariable assignment state that may not appear as a simple direct assignment yet. (Ch 4)

**Delaboration** — contextual conversion from `Expr` back to printable `Syntax`. (Ch 12)

**Definitional equality (`isDefEq`)** — unification-aware equality procedure that may assign metavariables while checking whether expressions compute to the same meaning. (Ch 4)

**Elaboration** — context-sensitive translation from syntax to typed expressions, including name resolution, implicit arguments, coercions, unification, and related inference. (Ch 2, 7)

**Expected type** — optional type constraint supplied to a term elaborator; may be absent or contain metavariables. (Ch 7)

**Expression (`Expr`)** — Lean's elaborated term representation: variables, metavariables, sorts, constants, applications, binders, lets, literals, metadata, and projections. (Ch 3)

**Free variable (`fvar`)** — expression referring to a local declaration through a unique identifier. (Ch 3–4)

**Goal** — metavariable used as an outstanding proof obligation; its type is the target and its local context contains available hypotheses/definitions. (Ch 4, 9)

**Hygiene** — macro-scope discipline that prevents accidental capture between user identifiers and generated identifiers. (Ch 6)

**`instantiateMVars`** — replaces currently assigned metavariables in an expression with their values for up-to-date structural inspection. (Ch 4)

**Local context** — ordered collection of local declarations relevant to an expression, metavariable, elaborator, or tactic goal. (Ch 4)

**Locally nameless** — representation combining de Bruijn bound variables with identifier-based local free variables. (Ch 3)

**Macro** — hygienic syntax-to-syntax rewrite in `MacroM`, suitable for context-free desugaring. (Ch 2, 6)

**Macro scope** — freshness marker used by hygienic macro expansion to distinguish generated identifiers. (Ch 6)

**`MetaM`** — monad providing semantic metaprogramming operations such as local contexts, metavariables, reduction, unification, and expression construction. (Ch 4)

**Metavariable (`mvar`)** — assignable expression hole with a local context and target type. (Ch 3–4)

**Metavariable depth** — constraint used to control assignment relationships across nested metavariable contexts. (Ch 4)

**`mkAppM`** — meta-level application builder that infers omitted implicit/universe arguments from available constraints. (Ch 4)

**`mkAppOptM`** — application builder allowing selective control over which arguments are inferred. (Ch 4)

**Parenthesizer** — pretty-printing stage that inserts grouping parentheses after syntax has been chosen. (Ch 12)

**Postponement** — delaying elaboration work until metavariables/expected-type constraints become more informative. (Ch 7)

**Quotation** — syntax template/pattern used for category-aware construction and matching. (Ch 5–6)

**Reduction** — computation/unfolding of expressions; full normalization computes deeply, while `whnf` exposes only the head form needed for many decisions. (Ch 4)

**Syntax** — parsed representation before elaboration; includes nodes, atoms, identifiers, and missing fragments. (Ch 5)

**Syntax category** — named grammar namespace such as `term`, `command`, `tactic`, or a user-declared DSL category. (Ch 5)

**Syntax kind** — identifier attached to parsed syntax nodes and used for extension dispatch. (Ch 2, 5–7)

**`TacticM`** — tactic monad that layers goal-list state over term/meta elaboration capabilities. (Ch 9)

**Telescope** — sequence of dependent binders opened into local free variables for inspection/construction. (Ch 4)

**Term elaborator** — handler mapping term syntax plus optional expected type to an expression in `TermElabM`. (Ch 7)

**Transparency** — policy controlling which definitions may unfold during reduction/definitional equality. (Ch 4)

**`TSyntax`** — syntax value tagged by a syntax category, enabling category-aware matching and helpers. (Ch 5)

**Unexpander** — lightweight pretty-printing hook that turns selected application syntax back into a convenient surface form before parenthesization. (Ch 12)

**Universe `Level`** — representation of universe levels supplied to sorts and polymorphic constants. (Ch 3)

**`whnf`** — weak-head normalization; computes enough to expose an expression's outer constructor. (Ch 4)
