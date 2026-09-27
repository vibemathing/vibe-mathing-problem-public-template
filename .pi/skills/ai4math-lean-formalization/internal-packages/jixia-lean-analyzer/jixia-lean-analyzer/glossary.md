# Glossary

**AST** — parsed Lean command syntax; jixia serializes `state.commands` when `-a` is requested. (Ch 3, Ch 7)

**BaseDeclarationInfo** — common source-level declaration record containing kind, syntax ref, name, modifiers, signature, binders, type/value, and scope. (Ch 2, Ch 4)

**BinderView** — Lean representation used by jixia to normalize explicit, implicit, strict implicit, instance, default, and tactic binders. (Ch 4)

**byte range** — source `start`/`stop` coordinates measured in bytes. (Ch 2, Ch 4, Ch 7)

**ContextInfo** — Lean context attached to InfoTree nodes and used to evaluate tactic/term information in the correct environment. (Ch 6)

**DeclarationInfo** — either a base declaration or an inductive record with constructors. (Ch 2, Ch 4)

**Elab.async** — Lean option affecting asynchronous elaboration; jixia defaults it to false when unset to preserve tactic InfoTree nodes. (Ch 1, Ch 3, Ch 6)

**ElaborationTree** — recursive jixia node containing elaboration info, source syntax metadata, and child nodes. (Ch 2, Ch 6)

**FVarId** — identifier for a Lean free variable/local hypothesis. (Ch 6)

**Goal** — rendered metavariable target plus local context, tag, proposition status, and optional dependency metadata. (Ch 2, Ch 6, Ch 7)

**InfoTree** — Lean elaboration information tree used for tactics, terms, macros, and source-position goal queries. (Ch 3, Ch 6, Ch 7)

**initializer** — Lean runtime initialization declaration; jixia can execute initializers with `-i` when analysis requires them. (Ch 1)

**Lake environment** — project package/search-path context supplied by `lake env`. (Ch 1, Ch 5)

**LineInfo** — byte source position plus goal state found there. (Ch 2, Ch 7)

**MVarId** — identifier for a Lean metavariable/goal. (Ch 2, Ch 6)

**ModuleInfo** — imported module names and main-module documentation strings. (Ch 2, Ch 7)

**PPSyntax** — source syntax metadata with originalness, optional range, and optional pretty representation. (Ch 2, Ch 4)

**PluginOption** — `ignore` or a JSON output path, controlling whether a general plugin runs and where it writes. (Ch 3)

**Process.plugins** — registry for normal plugins with `getResult` and optional `onLoad` function names. (Ch 3, Ch 8)

**ScopeInfo** — source declaration context: variables, include/omit sets, universe levels, namespace, open declarations, and active scoped namespaces. (Ch 2, Ch 4)

**SpecialValue** — a term value recognized as a direct constant or free variable. (Ch 2, Ch 6)

**SymbolInfo** — elaborated constant metadata including kind, type renderings, reference sets, and proposition status. (Ch 2, Ch 5)

**typeReferences** — constants referenced by a symbol's type/statement. (Ch 2, Ch 5)

**valueReferences** — optional constants referenced by a symbol's value/proof/definition body. (Ch 2, Ch 5)
