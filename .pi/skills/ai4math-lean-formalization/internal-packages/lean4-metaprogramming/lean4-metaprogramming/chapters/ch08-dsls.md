# Chapter 8: Embedding DSLs by Elaboration

## Core Idea
A Lean-embedded DSL can have its own syntax category and recursively elaborate directly into ordinary typed Lean expressions, keeping custom parsing separate from the semantic representation.

## Frameworks Introduced
- **Syntax-front / typed-back pattern**:
  1. Define ordinary Lean inductive types or functions representing the DSL semantics.
  2. Define one or more custom syntax categories for the surface language.
  3. Write recursive `Syntax → MetaM Expr`/elaboration functions that map each syntax form to the semantic constructors.
  4. Embed the DSL syntax in a Lean term position through a term elaborator.
- **Recursive structural elaboration**: each grammar constructor maps to a semantic constructor, recursively elaborating its children.

## Key Concepts
- **Embedded DSL**: specialized surface language compiled into Lean terms inside Lean source.
- **Semantic AST**: ordinary Lean datatype representing the DSL after elaboration.
- **Recursive elaborator**: syntax-directed function that constructs `Expr` for each DSL form.
- **`mkAppM`**: convenient constructor when semantic nodes are ordinary Lean functions/constructors and implicit arguments can be inferred.
- **Syntactic safety**: invalid grammar shapes cannot parse.
- **Semantic/type safety**: Lean types or elaborator checks reject semantically invalid combinations.

## Mental Models
Treat a DSL as a tiny compiler embedded in the Lean compiler. The custom syntax is the front end; the target Lean datatype/functions are the IR/semantic target; the elaborator is code generation plus semantic checking.

Decide deliberately where validation lives. Some restrictions are best encoded in grammar, some in the semantic datatype's type, and some in elaboration-time checks with tailored diagnostics.

Keep the translation compositional: one syntax constructor should generally map to one semantic constructor/application. This makes new forms easy to add and test.

## Anti-patterns
- **Encoding all validation in syntax**: grammar alone cannot express many type/semantic relationships.
- **Allowing accidental weird combinations without deciding whether they are valid**: a teaching DSL may permit them, but production DSLs should choose a semantic policy.
- **Building every target application manually with raw `Expr.app`** when meta-level application builders can infer routine parameters.
- **Mixing parser design and semantic representation so tightly that either cannot evolve independently**.

## Code Examples
```lean
-- Distilled recursive shape.
partial def elabDsl : Syntax → MetaM Expr
  | stx =>
    match stx with
    | `(mydsl| $n:num) => mkAppM ``MyDsl.lit #[toExpr n.getNat]
    | `(mydsl| $a + $b) =>
        mkAppM ``MyDsl.add #[← elabDsl a, ← elabDsl b]
    | _ => throwUnsupportedSyntax
```
- **What it demonstrates**: syntax-directed recursion targets ordinary Lean constructors while leaving inferred parameters to `MetaM`.

## Reference Tables
| Concern | Good home |
|---|---|
| Token/shape invalidity | Syntax grammar |
| Target data representation | Lean inductive/function definitions |
| Type/context-dependent validity | Elaborator / Lean type checker |
| Surface sugar | Macro before elaboration, if purely syntactic |
| Detailed semantic errors | Elaborator |

## Key Takeaways
1. Separate surface grammar from semantic representation.
2. Make the translation recursively compositional.
3. Use Lean's type system and elaborator context for semantic restrictions that syntax cannot express.
4. Prefer `MetaM` builders for semantic target construction.
5. Test both parse failures and semantic/type failures.

## Connects To
- **Ch 5**: creates the custom syntax category.
- **Ch 7**: embeds the category into terms with contextual elaboration.
- **Ch 4**: constructs target expressions safely.

## Operational Procedure
Design the DSL from the semantic target backward. List the Lean constructors/functions that should exist after elaboration, then create one grammar form for each user-facing operation that deserves dedicated syntax. For every form, decide whether invalidity is syntactic, semantic, or type-level. Build one positive and one negative test per constructor. Finally embed the DSL into `term` only through a narrow boundary so ordinary Lean elaboration resumes outside the DSL.

When the DSL grows, keep the recursive translator partitioned by syntax category rather than one giant match. Shared semantic constructors can remain ordinary Lean APIs, which makes them testable independently from the custom syntax and lets other metaprograms construct the same values without going through parsing.
