# Appendix B: Provenance Map

## Purpose

This appendix records where the skill's important capabilities come from and separates source-derived knowledge from engineering added for reliable agent use.

### Provenance labels

- **SOURCE_DERIVED** — directly based on a rule, explanation, exception, or method in the 1918 book.
- **STRUCTURAL_SYNTHESIS** — combines several source rules into an operational workflow without claiming Strunk named that workflow.
- **IMPLEMENTATION_DECISION** — added to make the skill safe, routable, testable, or useful in a contemporary agent environment.

## Source Map

| Capability | Source location | Type | Derived interpretation |
|---|---|---|---|
| Use a compact set of high-frequency essentials | Ch I, pp. 5–6 | SOURCE_DERIVED | Start review with recurring structural problems before narrow preferences |
| Allow a rule departure when it earns compensating merit | Ch I, p. 6 | SOURCE_DERIVED | Preserve deliberate marked constructions when rhetorical benefit is clear |
| Singular possessive with `'s` and listed exceptions | Ch II, Rule 1, p. 7 | SOURCE_DERIVED | Possessive diagnostic |
| Serial comma | Ch II, Rule 2, pp. 7–8 | SOURCE_DERIVED | Series-punctuation diagnostic; house-style routing added separately |
| Parenthetic vs. restrictive material | Ch II, Rule 3, pp. 8–10 | SOURCE_DERIVED | Meaning-sensitive comma diagnostic |
| Coordinate-clause comma | Ch II, Rule 4, pp. 10–11 | SOURCE_DERIVED | Clause-boundary repair |
| Avoid comma splices; use semicolon/period/conjunction | Ch II, Rule 5, pp. 11–12 | SOURCE_DERIVED | Independent-clause repair with source exceptions |
| Repair accidental sentence fragments | Ch II, Rule 6, pp. 12–13 | SOURCE_DERIVED | Fragment diagnostic with emphatic-fragment exception |
| Introductory participial phrase must match subject | Ch II, Rule 7, pp. 13–14 | SOURCE_DERIVED | Dangling-modifier repair |
| One topic per paragraph | Ch III, Rule 8, pp. 15–17 | SOURCE_DERIVED | Paragraph-unity pass |
| Topic sentence and conforming ending | Ch III, Rule 9, pp. 17–19 | SOURCE_DERIVED | Expository paragraph frame with narrative exceptions |
| Active voice preference plus passive exceptions | Ch III, Rule 10, pp. 19–21 | SOURCE_DERIVED | Active-recast test, not a blanket ban |
| Positive form | Ch III, Rule 11, pp. 21–22 | SOURCE_DERIVED | Replace evasive negatives with direct assertions |
| Definite, specific, concrete language | Ch III, Rule 12, pp. 22–24 | SOURCE_DERIVED | Concrete-specificity pass |
| Omit needless words | Ch III, Rule 13, pp. 24–25 | SOURCE_DERIVED | Functional concision pass |
| Avoid succession of loose sentences | Ch III, Rule 14, pp. 25–26 | SOURCE_DERIVED | Sentence-variety recovery based on logical relation |
| Coordinate ideas in similar form | Ch III, Rule 15, pp. 26–28 | SOURCE_DERIVED | Parallelism normalization |
| Keep related words together | Ch III, Rule 16, pp. 28–29 | SOURCE_DERIVED | Modifier-proximity repair |
| Keep one tense in summaries | Ch III, Rule 17, pp. 29–31 | SOURCE_DERIVED | Summary-tense lock |
| Put emphatic material at the end | Ch III, Rule 18, pp. 31–32 | SOURCE_DERIVED | End-weight emphasis test |
| Form conventions | Ch IV, pp. 33–35 | SOURCE_DERIVED | Function-first reference for headings, numerals, parentheses, quotations, references, syllabication, titles |
| Diagnose misused/hackneyed expressions; recast whole sentence when needed | Ch V, pp. 36–47, especially opening | SOURCE_DERIVED | Formulaic-diction recast |
| Spelling follows general agreement; unfamiliar simplification costs reader attention | Ch VI, p. 48 | SOURCE_DERIVED | Reader-expectation spelling principle |
| Practice via punctuation, meaning comparison, and error correction | Ch VII, pp. 50–51 | SOURCE_DERIVED | Exercise/evaluation protocol |
| Diagnose in ordered passes before rewriting | Cross-chapter | STRUCTURAL_SYNTHESIS | Sequence sentence integrity → relation → paragraph logic → directness → economy → rhythm → form |
| Minimal / structural / full-rewrite intervention levels | Cross-chapter | STRUCTURAL_SYNTHESIS | Choose the smallest edit that reliably fixes the diagnosed problem |
| Failure-recovery routing | Cross-chapter source exceptions | STRUCTURAL_SYNTHESIS | Preserve intentional fragments/passives, expose ambiguity, recast when patching fails |
| Modern applicability gate | Source date + period-sensitive Ch IV–VI content | IMPLEMENTATION_DECISION | Prevent 1918 prescriptions from being silently enforced as current universal rules |
| House-style precedence for style-dependent conventions | Ch IV notes editorial variation + agent design | IMPLEMENTATION_DECISION | Defer publication-specific mechanics to the target guide |
| Trigger and negative-trigger boundaries | Skill architecture | IMPLEMENTATION_DECISION | Invoke for English prose/Strunk tasks; avoid unrelated tasks |
| SELF_CHECK | Cross-chapter operationalization | STRUCTURAL_SYNTHESIS | Validate prerequisites, exceptions, meaning preservation, and modern applicability before output |

## Coverage Ledger

| Unit | Status | Main extracted capability |
|---|---|---|
| I. Introductory | processed | scope, essentials, deliberate exceptions |
| II. Elementary Rules of Usage | processed | Rules 1–7 |
| III. Elementary Principles of Composition | processed | Rules 8–18 |
| IV. A Few Matters of Form | processed | manuscript/form conventions |
| V. Words and Expressions Commonly Misused | processed | diction diagnostics + full-sentence recast method |
| VI. Spelling | processed | reader-oriented convention + historical spellings |
| VII. Exercises on Chapters II and III | processed | applied diagnostic evaluation |

## Source Freeze

- **Title**: *The Elements of Style*
- **Author**: William Strunk Jr.
- **Edition represented**: original 1918 text, public-domain HTML transcription
- **Source structure**: 7 major units; 18 numbered rules across Chapters II–III; form, usage, spelling, and exercises in Chapters IV–VII
- **Source pagination represented**: pp. 3–51 in the transcription
- **Non-text dependencies**: no substantive image content required for the operational rules extracted here
- **Known limitation**: the source predates modern usage changes; Appendix A is an implementation layer, not an authorial claim
