# PROVENANCE_MAP

Labels:
- **SOURCE_DERIVED**: operational rule directly reflects one or more source units.
- **STRUCTURAL_SYNTHESIS**: combines compatible rules across source units into a routing/workflow layer.
- **IMPLEMENTATION_DECISION**: packaging or adaptation required by this compilation, not asserted by the blog.

## Capability provenance

- **task-router** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u013,u019,u050,u051,u093,u099,u117,u127
- **type-first-disambiguation** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u024,u037,u089,u090,u094
- **statement-semantics-audit** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u096,u111,u116,u121,u125,u126,u128,u132,u133
- **proof-state-loop** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u017,u020,u023,u034,u054,u099,u111
- **core-tactic-selection** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u017,u020,u023,u039,u054,u100,u101,u108
- **equality-layer-diagnosis** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u062,u063,u064,u091,u095,u109
- **normalize-then-solve** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u043,u055,u056,u068,u091,u102
- **simp-system-engineering** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u007,u040,u101
- **inductive-eliminator-route** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u009,u027,u039,u108,u109,u110
- **quotient-universal-property** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u005,u106,u124
- **definition-api-design** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u030,u048,u078,u080,u085,u091,u098,u132
- **specification-implementation-separation** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u062,u064,u090,u091,u095,u124
- **proof-vs-compute-representation** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u009,u058,u066,u068,u090
- **prop-to-data-boundary** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u065,u066,u110
- **domain-contract-totalization** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u090,u092
- **library-search-and-version-drift** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u011,u012,u014,u016,u031,u033,u054,u118,u119,u120
- **coercion-typeclass-debug** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u024,u085,u098,u100,u101
- **reflection-trust-chain** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u043,u058,u068,u077,u111,u119
- **filter-abstraction** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u047,u048,u102,u103,u104,u105
- **generality-linter** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u030,u078,u098,u101
- **research-blueprint** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u061,u071,u079,u096,u099,u111,u117,u120,u121
- **target-driven-library-growth** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u069,u078,u096,u111,u117,u120,u129,u132
- **statement-first-milestone** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u071,u079,u098,u119,u127,u132
- **staged-assumptions** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u044,u061,u096,u115,u120
- **mathematical-typo-repair** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u096,u111,u119,u121,u128,u132
- **teaching-by-familiar-math** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u015,u021,u034,u051,u054,u060,u093,u097,u100-u107,u112-u115
- **community-debugging** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u034,u086,u093,u097,u111,u112,u115
- **ai-statement-definition-audit** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u116,u121,u125,u127,u128,u129,u130,u131,u132,u133
- **ai-proof-verification** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u122,u125,u126,u127,u128,u131,u133
- **counterexample-first** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u128,u131
- **machine-proof-digestion** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u111,u132,u133
- **benchmark-integrity** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u122,u123,u125,u126,u127
- **gold-standard-library-definition** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u127,u129,u130,u132,u133
- **autoformalization-suitability** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u130,u131,u132,u133
- **formal-code-security-audit** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — u119,u131,u133
- **release-self-check** — SOURCE_DERIVED + STRUCTURAL_SYNTHESIS — cross-cutting: u062-u068,u091-u099,u111,u121-u133

## Implementation decisions

- Treat the website mirror as the source “book” and the 133 canonical entry bodies as content units because the supplied artifact is HTML, while `book-to-skill-master` natively expects PDF/EPUB.
- Group 133 units into thematic on-demand chapters instead of generating 133 chapter files; this preserves the master skill’s progressive-loading goal and follows the user’s capability-first requirement.
- Add `references/`, `evals/`, and a local validator; these are auxiliary files and do not alter the master-required `SKILL.md`, `chapters/`, `glossary.md`, `patterns.md`, `cheatsheet.md` structure.
- Keep historical syntax as conceptual provenance and require live API lookup for current Lean/mathlib details.
