# Historical Lean / mathlib Notes

The source archive spans 2017–2026 and therefore multiple Lean/mathlib eras. Many early posts use Lean 3 syntax, package-install instructions, theorem names, and library states that should not be copied as current instructions.

## Stable conceptual guidance

These ideas survive version changes and are safe to use as routing principles:

- propositions as types / proofs as terms;
- constructors and recursors for inductive types;
- definitional versus propositional equality;
- quotient lifts and universal properties;
- extensionality and canonicalization APIs;
- reflection plus kernel verification;
- representation/specification separation;
- filter `map`/`comap`/`Tendsto` architecture;
- target-driven library engineering;
- statement-semantic auditing for autoformalization.

## Version-sensitive material

Always verify before giving executable code:

- imports and namespaces;
- tactic names and tactic syntax;
- declaration names/signatures;
- typeclass hierarchy and coercions;
- package/tool installation commands;
- Lean 3 → Lean 4 port status;
- deprecated predicates/structures.

## Translation procedure

1. Extract the mathematical purpose of the historical snippet.
2. Ask/check the user's actual Lean toolchain.
3. Search the current library for the concept, not only the old identifier.
4. Inspect the current declaration type and source/API documentation.
5. Rebuild the smallest example and compile it.
6. Only then scale to the user's file.

Do not treat source posts named “what Lean already knows” or installation pages as current catalogues. They are historical evidence about the project's development.
