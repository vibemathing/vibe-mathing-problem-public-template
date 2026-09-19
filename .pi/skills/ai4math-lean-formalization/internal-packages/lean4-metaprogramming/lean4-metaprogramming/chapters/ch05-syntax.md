# Chapter 5: Syntax

## Core Idea
Lean's syntax system is an extensible parser with named categories, precedence, repetition combinators, and typed syntax trees. Design grammar and tree shape intentionally before attaching semantics.

## Frameworks Introduced
- **Syntax category design**: create a custom category when a DSL or notation needs its own grammar, then embed that category into an existing one when needed.
- **Precedence as parse control**: use precedence and associativity to encode grouping directly in the grammar.
- **Typed syntax (`TSyntax`)**: attach a category marker to syntax so matching and helper APIs know what kind of syntax is expected.

## Key Concepts
- **`syntax`**: declares a parser rule and syntax kind.
- **`declare_syntax_cat`**: creates a new syntax category.
- **Precedence**: determines which nested forms may consume which subexpressions.
- **Longest parse**: overlapping rules often resolve by consuming the longest valid parse.
- **Parser alternatives**: combine parsers when several forms are accepted.
- **Repetition**: one-or-more/zero-or-more, optionally with separators.
- **Optional parser**: syntax element may be absent.
- **`Syntax.node` / `atom` / `ident` / `missing`**: primary syntax-tree shapes.
- **Syntax quotation**: category-aware template/pattern for constructing or matching syntax.
- **Antiquotation**: embeds/captures syntax within a quotation.

## Mental Models
Think of precedence as a contract between a parser and its subparsers: each child position announces the maximum/minimum binding power it accepts. Associativity follows from how recursive positions are assigned precedence, not from a separate evaluator rule.

Think of a custom syntax category as a typed AST front-end. It narrows the shapes an elaborator or macro must handle and makes embedded DSLs easier to reason about.

Use quotations as the normal representation-level interface. They preserve exact syntax kinds and make patterns readable; manual `Syntax.mk*` construction is valuable when a dynamic shape cannot be expressed cleanly by a quotation.

## Anti-patterns
- **Treating whitespace as irrelevant to all tooling**: parser and pretty-printer conventions can depend on syntax declaration details.
- **Ignoring overlapping rules**: longest-match behavior can make an apparently obvious grammar parse differently than intended.
- **Manually indexing child arrays everywhere**: quotation patterns are usually more robust and maintainable.
- **Using untyped `Syntax` when category-specific helpers would prevent mistakes**.

## Code Examples
```lean
-- Distilled custom category pattern.
declare_syntax_cat arith
syntax num : arith
syntax:60 arith:60 " + " arith:61 : arith
syntax "⟪" arith "⟫" : term
```
```lean
-- Category-aware quotation matching shape.
match stx with
| `(arith| $n:num) => ...
| `(arith| $a + $b) => ...
| _ => ...
```
- **What it demonstrates**: grammar shape and quotation patterns form a stable interface between parsing and later processing.

## Reference Tables
| Need | Syntax tool |
|---|---|
| New grammar namespace | `declare_syntax_cat` |
| New parser rule | `syntax` |
| One-or-more / zero-or-more | repetition combinators |
| Delimited lists | repetition with separators |
| Maybe-present fragment | optional parser |
| Construct/match known syntax | quotations/antiquotations |
| Category-aware syntax value | `TSyntax` |

## Exercise-backed Validation
The syntax solutions show that associativity can be encoded by asymmetric precedence on recursive operands and that equivalent user-facing forms can be accepted through parser alternatives. Use tests with chained operators to confirm the parse tree, rather than trusting visual spacing.

## Key Takeaways
1. Design syntax categories around semantic sublanguages, not around chapter-sized features.
2. Test precedence with chained examples and overlapping forms.
3. Prefer quotations for matching and construction; reach for raw `Syntax` constructors only when dynamic structure requires them.
4. Carry category information with typed syntax when it improves safety and API access.

## Connects To
- **Ch 6**: transforms parsed syntax hygienically.
- **Ch 7–8**: assigns context-sensitive meaning to syntax and DSLs.

## Operational Procedure
Test a grammar with a small parse matrix before attaching semantics: the shortest valid form, a chained form, a nested parenthesized form, an overlapping alternative, and an invalid near miss. For operators, include three operands so associativity becomes observable. For repetition, test zero/one/many cases according to the declared combinator. For optional pieces, test both presence and absence. Inspect the quotation pattern you expect later and make sure the parser's actual node shape matches it.

If downstream macro/elaboration code needs many manual child indexes, revisit the grammar or typed-syntax boundary. A better category split often produces a syntax tree that can be matched directly with quotations and named captures.
