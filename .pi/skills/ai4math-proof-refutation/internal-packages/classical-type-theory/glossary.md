# Glossary

**Abstract consistency property** — A closure property on finite formula sets used by the Unifying Principle to establish consistency/completeness (Ch 5).

**Abstraction / lambda abstraction** — A typed term former `lambda x. A` denoting the function mapping `x` to `A` (Ch 2).

**Alpha-conversion** — Capture-safe renaming of bound variables (Ch 2).

**Axiom of Choice** — A typed schema asserting suitable choice functions; treated as an extra logical principle in the chapter (Ch 3).

**Beta-contraction / beta-normal form** — Reduction of an applied lambda abstraction by substitution; a term is beta-normal when no such redex remains after allowed renaming (Ch 2).

**Choice function** — A function selecting an element from each nonempty predicate/set of a given type (Ch 3).

**Comprehension** — The principle that a formula of the right type can determine a function/set/relation object (Ch 1-2).

**Constrained clause** — A clause paired with pending higher-order unification constraints (Ch 11).

**Constraint** — A set of same-typed formulas required to become identical under a substitution (Ch 11-12).

**Deep formula** — The propositional formula obtained from an expansion tree after its quantifier instantiations are represented by branch combinations (Ch 6).

**Dependency condition** — The acyclicity requirement on dependencies among expansion terms/selected parameters (Ch 6).

**Elementary type theory (J)** — The chapter's subsystem containing propositional/quantifier logic and lambda conversion, omitting extensionality and descriptions (Ch 2).

**Expansion node** — An essentially existential quantifier occurrence with one or more expansion terms (Ch 6).

**Expansion option** — A pairing of an expansion node with a candidate instantiation term (Ch 10).

**Expansion proof** — An expansion tree whose deep formula is tautological and whose dependency relation is acyclic (Ch 6).

**Expansion term** — A typed term used to instantiate an expansion variable (Ch 6, 10).

**Extensionality** — Principles identifying propositions/functions by equivalent truth behavior or agreement on all arguments (Ch 1, 12).

**Flex-rigid unification** — A higher-order unification problem with a variable-headed term on one side and a constant-headed term on the other (Ch 12).

**Gensub** — A general substitution template richer than a primitive substitution, often normalized to control equivalent variants (Ch 10).

**Higher-order logic** — Classical type theory viewed as an extension of first-order logic with variables/quantification at higher types (Ch 1).

**Higher-order unifier** — A substitution making terms have the same lambda-normal form (Ch 8).

**Imitation** — A flex-rigid substitution candidate that copies the rigid head and delegates arguments to fresh helper variables (Ch 12).

**Leibniz equality** — Equality defined by indistinguishability with respect to all properties (Ch 1).

**Mating / connection** — A pairing of complementary literals used to span paths through a deep formula (Ch 10).

**Necessary argument** — An argument that a Skolem symbol must carry to preserve the dependency under which the witness was introduced (Ch 3).

**Projection** — A substitution candidate that returns one of a function's arguments, possibly through helper structure (Ch 10, 12).

**Selected parameter** — A suitably fresh parameter introduced at a selection node in an expansion tree (Ch 6).

**Selection node** — An essentially universal quantifier occurrence in an expansion tree, with one selected parameter branch (Ch 6).

**Shallow formula** — The formula directly represented by an expansion tree or node before deep instantiation structure is collapsed (Ch 6).

**Skolem term** — A witness term whose arguments encode the variables/terms on which the witness depends (Ch 3, 12).

**Splitting rule** — A higher-order resolution rule that introduces logical structure for a variable-headed atom (Ch 11).

**Type order** — The hierarchy level induced by nested relation/function types; proof-internal orders are not bounded by theorem syntax in general (Ch 1, 9).

**Unifying Principle** — Smullyan/Andrews metatheorem turning an abstract consistency property into an actual consistency result, used for completeness proofs (Ch 5).

**Z-match** — A context-driven rule that incrementally elaborates set/predicate instantiations during backward proof search (Ch 13).
