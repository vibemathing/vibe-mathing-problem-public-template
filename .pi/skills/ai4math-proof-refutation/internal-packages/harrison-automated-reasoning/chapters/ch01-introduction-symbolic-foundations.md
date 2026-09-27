# Chapter 1: Introduction and Symbolic Foundations

**Source coverage**: Harrison Ch. 1, §§1.1–1.8, book pp. 1–24.

## Core Idea
Automated reasoning starts by making logical form explicit. Separate expressions from their meanings, represent syntax structurally, and apply small correctness-preserving transformations mechanically.

## Frameworks Introduced
### Logical form over content
- **When to use**: When deciding whether an inference is logically justified rather than merely plausible or factually true.
- **How**:
  1. Abstract away domain-specific meanings.
  2. Expose the common inferential form.
  3. Make hidden assumptions explicit.
  4. Check whether every substitution/interpretation preserving the form also preserves truth from premises to conclusion.
- **Why it works**: Logical validity is intended to survive changes in subject matter.
- **Failure mode**: A true conclusion can follow through an invalid argument. Truth of the endpoint does not repair a missing premise.

### Leibniz's reasoning-as-calculation architecture
- **Components**: a precise language, a calculus of symbolic manipulation, and mechanization of that calculus.
- **Operational use**: Treat every prover design as three linked engineering problems: representation, inference rules, and execution/search.

### Syntax–semantics separation
- **Syntax**: What expressions are well formed and how they are structurally composed.
- **Semantics**: What those expressions denote or when they are true.
- **Rule**: A syntactic procedure earns logical authority only through a semantic or proof-theoretic justification.
- **Object/meta discipline**: Keep the formula being reasoned about distinct from the metalanguage in which the prover or metatheorem is described.

### Concrete syntax → AST → concrete syntax
- **When to use**: Any symbolic tool that accepts human notation but performs structural transformations.
- **How**: tokenize → parse with precedence/associativity → operate on an AST → prettyprint with enough parentheses to preserve structure.
- **Invariant**: Prefer `parse(print(ast)) = ast`. Exact textual round-tripping is generally impossible because spacing and redundant parentheses are discarded.

## Key Concepts
- **Logical reasoning**: Inference intended to be infallible by virtue of general form rather than subject matter.
- **Proposition**: An assertion assigned a truth value in the chosen logic.
- **Connective**: An operation such as negation, conjunction, or disjunction on propositions.
- **Syntax**: Rules determining well-formed symbolic expressions.
- **Semantics**: A systematic interpretation assigning meanings to well-formed expressions.
- **Object language**: The formal language under study.
- **Metalanguage**: The language used to describe and reason about the object language.
- **Concrete syntax**: Human-facing notation with operators, precedence, and parentheses.
- **Abstract syntax**: Structural representation, usually a tree.
- **Parsing**: Converting concrete syntax to abstract syntax.
- **Prettyprinting**: Converting abstract syntax back to readable concrete syntax.

## Mental Models
- **Reasoning as symbolic calculation**: Once the formal meaning is fixed, routine steps should become mechanically executable.
- **AST as the semantic skeleton**: The linear text is presentation; the tree is where subexpression identity and recursive algorithms become precise.
- **Interpreter sandwich**: `text → syntax tree → transformations/evaluation → text`. Bugs at either boundary can invalidate an otherwise correct core.
- **Small local rewrite, global recursive traversal**: Define trustworthy local simplifications, then compose them through a disciplined traversal strategy.

## Anti-patterns
- **Reasoning from natural-language surface form**: Words such as “is,” “or,” or “if” can hide structural ambiguity.
- **Mixing syntax with denotation**: Rewriting a symbol string and reasoning about its mathematical value are different operations.
- **Applying rewrite rules without a traversal policy**: A local simplifier can miss reducible subterms, redo work, or loop when mixed top-down/bottom-up without a termination argument.
- **Over-parenthesizing as the permanent representation**: It is correct but burdens humans; store structure in the AST and print minimally according to precedence.

## Code Examples
A language-independent expression AST:

```text
Expr := Var(name)
      | Const(integer)
      | Add(Expr, Expr)
      | Mul(Expr, Expr)
```

A safe simplifier pattern:

```text
simplify(node):
    simplify children first
    rebuild node
    apply one local identity/folding rule
    return result
```

A recursive-descent parser follows grammar levels such as:

```text
expression := product ("+" product)*
product    := atom ("*" atom)*
atom       := number | variable | "(" expression ")"
```

- **What it demonstrates**: Data representation and recursive program structure mirror the grammar and expression tree.

## Reference Tables
| Concern | Human-facing form | Internal form | Main risk |
|---|---|---|---|
| Expression | `x + y * z` | tree rooted at `Add` | precedence ambiguity |
| Syntax check | grammar | datatype/constructors | malformed input |
| Meaning | informal/math interpretation | evaluator/semantic function | conflating syntax and value |
| Transformation | algebraic-looking rule | pattern match on AST | unsound rule or looping traversal |
| Output | infix notation | printer with precedence | losing grouping |

## Worked Example
Suppose the input is `(0 * x + 1) * 3 + 12`.

1. The lexer isolates numbers, names, operators, and parentheses.
2. The parser builds a tree in which multiplication binds more tightly than addition.
3. Bottom-up simplification changes `0 * x` to `0`, then `0 + 1` to `1`, then `1 * 3` to `3`, then `3 + 12` to `15`.
4. The final tree is `Const(15)`.
5. The printer emits `15`.

The important lesson is architectural: each local step is simple because structural grouping is already explicit. If a top-down optimization short-circuits `0 * E` without visiting `E`, verify that the traversal still terminates and reaches every simplifiable term that matters.

## Key Takeaways
1. Formal reasoning needs a precise language before it needs a powerful prover.
2. Validity concerns inferential form; factual truth alone is insufficient.
3. Keep syntax, semantics, object language, and metalanguage distinct.
4. Use ASTs as the canonical substrate for manipulation.
5. Parsing and prettyprinting are boundary components whose round-trip property should be tested.
6. Recursive symbolic programs should expose their invariants and termination assumptions.

## Connects To
- **Ch. 2**: Propositional formulas instantiate the syntax/semantics distinction concretely.
- **Ch. 3**: First-order terms, binding, and capture-safe substitution add more demanding syntax operations.
- **App. 2–3**: Functional programming and generic parsing/printing supply the implementation machinery.
