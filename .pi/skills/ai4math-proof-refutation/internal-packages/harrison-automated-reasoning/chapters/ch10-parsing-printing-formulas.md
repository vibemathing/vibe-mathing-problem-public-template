# Appendix Skill Layer 3: Parsing and Printing Formulas

**Source coverage**: Harrison Appendix 3, book pp. 623–630; builds on Ch. 1 parsing/printing.

## Core Idea
A prover's concrete syntax layer should be generic, precedence-aware, and structurally invertible. Parser combinators turn grammar levels into reusable functions; prettyprinters use precedence/associativity to emit the minimum grouping needed to recover the same AST.

## Frameworks Introduced
### Generic infix parsing
Build reusable combinators for:
- right-associative infix operators;
- left-associative infix operators;
- comma/list forms;
- bracketed subexpressions.

**Decision rule**: Association is semantic syntax policy. Use left association for operations such as subtraction; right association for implication/exponentiation where intended; do not inherit recursion direction accidentally.

### Formula parser layers
A formula parser descends through precedence classes:
1. equivalence;
2. implication;
3. disjunction;
4. conjunction;
5. negation/quantifier/atom.

Atomic formula parsing is parameterized so propositional and first-order languages can share the logical-connective parser while differing in their atoms.

### Quantifier parsing with context
When parsing first-order syntax, keep a context of currently bound variable names. An alphanumeric identifier can then be classified as variable or constant according to scope/conventions.

**Invariant**: The parser's variable classification must match the binding semantics later used by free-variable and substitution operations.

### Infix atoms and term parsing
First-order atoms may contain infix predicates such as `x < y` while terms contain infix functions such as `x + y`.
- Parse terms at their own precedence levels.
- Then recognize relational/infix predicate structure around parsed terms.
- Avoid ambiguous fallback that consumes too much input before deciding which grammar applies.

### Prettyprinting by outer precedence
Printer function receives the precedence of the surrounding context.
- Print a subexpression without parentheses when its top-level operator binds at least as tightly as the context permits.
- Add parentheses when omission would alter the parse tree.
- Treat equal-precedence operands asymmetrically according to associativity.

For long formulas, use a formatting engine that supports breakable spaces/boxes so line wrapping follows syntactic structure.

## Key Concepts
- **Parser combinator**: Higher-order function constructing a parser from smaller parsers.
- **Precedence**: Binding strength that determines implicit grouping.
- **Associativity**: Grouping convention for repeated operators at equal precedence.
- **Secondary parser**: Alternate parser passed into a generic layer, for example a specialized atom parser.
- **Bound-variable context**: Parser state recording names currently introduced by quantifiers.
- **Prettyprinter**: Structure-aware renderer, not just string concatenation.

## Mental Models
- **Grammar as executable recursion**: Each nonterminal becomes a function; grammar nesting becomes call structure.
- **Printer as inverse parser modulo presentation**: Preserve AST identity, while spacing/parentheses may normalize.
- **Context is part of syntax**: A token can only be classified correctly when binder context and language conventions are known.

## Anti-patterns
- **Naive left-recursive recursive descent**: Calls itself before consuming input and loops.
- **Ignoring associativity**: Changes the AST for repeated nonassociative operators.
- **Printing without precedence**: Emits ambiguous or semantically different text.
- **Testing `print(parse(s)) == s` as the main invariant**: Redundant whitespace/parentheses make this unrealistic.
- **Failing to check leftover tokens**: A parser may accept a prefix and silently ignore malformed suffix input.

## Code Examples
Generic left-associative parser shape:

```text
parse_left(atom, op, tokens):
    lhs, rest := atom(tokens)
    while rest starts with op:
        rhs, rest := atom(rest after op)
        lhs := Node(op, lhs, rhs)
    return lhs, rest
```

Precedence printer shape:

```text
print(node, outer_prec):
    p := precedence(node.operator)
    body := print children with side-specific precedence
    if p < outer_prec: return "(" + body + ")"
    return body
```

Top-level safety check:

```text
ast, rest := parse(tokens)
if rest != []: fail "unparsed input"
return ast
```

## Reference Tables
| Syntax concern | Required mechanism |
|---|---|
| multiple infix precedences | parser layer per precedence |
| left/right association | dedicated combinator or side-specific recursion |
| quantifier scope | low-precedence quantifier parser + bound-variable context |
| term vs formula atoms | parameterized atom parser |
| readable output | outer-precedence printer |
| long line layout | structured formatting boxes/break hints |

## Worked Example
For `p ==> q /\ r \/ s`, the parser applies the established precedence hierarchy so conjunction binds tighter than disjunction, and both bind tighter than implication. The AST corresponds to `p ⇒ ((q ∧ r) ∨ s)`. The printer can omit most parentheses because the same precedence rules recover that tree. If the AST were `(p ⇒ q) ∧ r`, parentheses around `p ⇒ q` would be mandatory because implication binds more weakly than conjunction.

A round-trip test should generate/obtain ASTs `e`, print them, parse the result, and assert structural equality: `parse(print(e)) = e`.

## Key Takeaways
1. Encode precedence and associativity once in generic parser/printer infrastructure.
2. Reject leftover input at the top level.
3. Keep quantifier/bound-variable context explicit.
4. Test AST round trips, not exact text reproduction.
5. Prettyprinting is a correctness boundary because missing parentheses can change meaning.

## Connects To
- **Ch. 1**: General concrete/abstract syntax architecture.
- **Ch. 3**: Binding-aware parsing must agree with free-variable and substitution semantics.
- **App. 2**: Higher-order functions, recursion, and datatypes implement the parser/printer combinators.
