# Appendix A: Modern Applicability Gate

## Purpose

This appendix is an **IMPLEMENTATION_DECISION** added to make a 1918 style handbook safe and useful for contemporary editing. It does not attribute modern usage judgments to Strunk. The source is preserved faithfully in its chapter files; this gate controls when an agent should enforce, contextualize, or merely report those historical prescriptions.

## Classification

### A. Durable structural principles — apply when context fits

These remain broadly useful because they describe reader-facing structure rather than a period-specific lexical fashion:

- distinguish restrictive from parenthetic/nonrestrictive material;
- repair comma splices and accidental fragments;
- attach introductory modifiers to the grammatical subject;
- keep one dominant topic per paragraph;
- make expository paragraph purpose visible and develop it coherently;
- prefer active voice when it improves directness, while preserving useful passives;
- state claims directly and concretely;
- remove wording that performs no function;
- avoid monotonous repetition of one loose-sentence pattern;
- use parallel form for coordinate ideas;
- keep modifiers and antecedents close enough to avoid false attachment;
- keep a controlled tense system in summaries;
- use beginning and ending positions deliberately for emphasis.

These are defaults, not inviolable laws. Genre and rhetorical effect still matter.

### B. Style-dependent conventions — defer to target house style

Use Strunk's choice when the user explicitly wants Strunk style or no competing convention is relevant. If a named publication or organization has a valid house rule, follow it.

Typical examples:

- serial comma policy;
- quotation punctuation and block-quote formatting;
- title styling and capitalization;
- reference/citation formatting;
- date and numeral presentation;
- some choices involving `less/fewer`, `like/as`, or connective placement where modern standards vary by register and region.

### C. Historical or materially dated prescriptions — do not silently enforce in modern prose

Report these as historical guidance unless the user requests a period imitation, a strict Strunk exercise, or a context that still adopts the same rule:

- rejection of singular `they` with indefinite or distributive antecedents;
- blanket avoidance of split infinitives;
- strict person-based `shall/will` and `should/would` future/conditional formulas;
- strict treatment of `data` only as a plural;
- the source's narrow restriction on adverbial `due to`;
- blanket rejection of `different than`;
- source-era restrictions on clause-level `like`;
- source-specific rules for `however` position;
- several lexical preferences such as `dependable`, `viewpoint`, `near by`, and `worth while`;
- hyphenated spellings `to-day`, `to-night`, and `to-morrow`;
- historical spacing/hyphenation of several compounds;
- print-era syllabication as a general writing task.

This list is intentionally conservative: when a Chapter V or VI rule is uncertain, treat it as style-dependent or historical rather than inventing modern authority.

## Decision Procedure

When a proposed edit rests on a potentially dated rule:

1. **Identify the exact source rule or entry.**
2. **Ask what task mode applies**:
   - modern prose editing;
   - named house style;
   - historical Strunk reference;
   - period imitation / classroom exercise.
3. **Classify the rule** as durable, style-dependent, or historical.
4. **Choose action**:
   - durable → apply if it improves the passage and prerequisites fit;
   - style-dependent → follow the target style or present options;
   - historical → explain Strunk's rule, then preserve modern standard usage unless the user explicitly wants the historical constraint.
5. **Label uncertainty** when the book alone cannot settle current usage.

## Conflict Examples

### Singular `they`

Historical source: Chapter V rejects plural pronouns after antecedents such as `everybody` and `somebody` and directs the writer to a gendered singular pronoun.

Modern skill action: do not apply that prescription as a default. If asked what Strunk taught, report it with its date. If asked to edit contemporary inclusive prose, follow the target modern style.

### Split infinitive

Historical source: acknowledges long precedent, yet advises avoidance because the construction was disfavored by careful writers of the period.

Modern skill action: treat placement according to clarity and naturalness unless a house style restricts it.

### `to-day`

Historical source: Chapter VI requires a hyphen.

Modern skill action: retain contemporary `today` in ordinary present-day prose; use the historical form only for quotation, period imitation, or a source-specific exercise.

### Passive voice

Source rule: “Use the active voice,” followed immediately by situations where passive is convenient or necessary.

Modern skill action: this is a durable preference with source-authored exceptions, not a historical ban. Preserve passive when it keeps the correct topic in subject position or omits an irrelevant actor.

## SELF_CHECK for Modern Use

- Am I reporting Strunk's historical view, or editing contemporary prose?
- Is this a structural clarity principle or a lexical convention tied to period and register?
- Did the user name a house style that governs the issue?
- Would applying the historical rule make ordinary contemporary prose less natural or less inclusive?
- Have I labeled the source's date when a modern reader could mistake the prescription for universal current usage?
