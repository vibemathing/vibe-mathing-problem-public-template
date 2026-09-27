---
name: welleck-informal-formal-reasoning
description: "Lean proving: Lean-STaR, DSP, LeanHammer, miniCTX, ImProver."
---

<!-- argument-hint: [goal, proof state, method name, failure mode, or chapter] -->

# Bridging Informal and Formal Mathematical Reasoning with AI
**Author/Speaker**: Sean Welleck | **Course**: Berkeley Advanced LLM Agents, 2025-04-14 | **Chapters**: 6 | **Generated**: 2026-09-12

## Use This Skill When
Use this skill when the task involves machine-checked mathematical reasoning and the main difficulty is choosing how to connect informal reasoning, formal proof search, library context, automation, or proof optimization.

Do not invoke it for ordinary informal math explanations, generic coding help, or claims of formal correctness when no proof assistant/verifier result is available. If the user wants a certified proof and verification cannot be run, produce a candidate/plan and label the verification gap explicitly.

## First Route the Task
1. **Local proof-step search with verifier feedback** → use **Lean-STaR** (`ch02`).
2. **An informal proof/strategy exists, but direct formalization is hard** → use **Draft-Sketch-Prove** (`ch03`).
3. **A formal subgoal is plausible but the library search space is large** → use **LeanHammer / premise selection** (`ch04`).
4. **The theorem depends on project-local definitions, lemmas, comments, or long files** → use **miniCTX-style context-first proving** (`ch05`).
5. **A correct formal proof already exists and must become shorter, clearer, or more modular** → use **ImProver-style optimization** (`ch06`).
6. **Mixed case** → compose methods: context package → high-level draft/sketch → hammer easy gaps → interleaved thought+tactic search for stubborn gaps → verifier gate → optional optimization.

## Core Operating Principles

### Treat the verifier as the hard boundary
Informal reasoning proposes; the formal system decides validity. Never convert a plausible natural-language derivation into a correctness claim without a successful formal check. Preserve the current proof state and verifier feedback after each attempted tactic or completed gap.

### Search at the right abstraction level
When low-level tactic branching explodes, move upward: generate an informal route or a formal sketch that decomposes the theorem into easier obligations. When the strategy is already right but one obligation is routine, move downward and hand the gap to automation.

### Interleave reasoning and proving when the next formal action is unclear
Lean-STaR's key move is to generate an informal thought before a formal tactic, then let Lean accept or reject the tactic. Use the rejected state as a branch signal, not as evidence that the high-level theorem is false.

### Retrieve context before increasing brute-force search
On real projects, failures often come from missing definitions or premises rather than weak tactic generation. Gather in-file and cross-file context, then rank likely premises. miniCTX makes this distinction explicit: state-only benchmarks can hide the context problem.

### Keep proof generation and proof optimization separate
A proof can be valid yet poor for downstream use. Once correctness is stable, optimize a verified proof against a declared metric such as length, declarativity, readability, or modular structure; re-verify every rewrite.

## Default Workflow
1. **Define the target**: formal theorem/goal, proof assistant, desired deliverable, and success criterion.
2. **Capture context**: current proof state; local hypotheses; imports; relevant definitions/lemmas; preceding file/project context.
3. **Classify the bottleneck** using the route above.
4. **Execute the selected method** from its chapter file.
5. **Verify every formal candidate**. Store the exact error/state on failure.
6. **Diagnose failure before retrying**:
   - repeated invalid tactics → revise reasoning or branch, not the same tactic wording;
   - sketch gaps remain too hard → refine/redraft the sketch into smaller obligations;
   - hammer misses → inspect/rerank premises or include local project context;
   - long-context proof fails → check whether needed dependencies were omitted or buried;
   - optimized proof breaks → revert to the last verified proof and change one transformation at a time.
7. **Escalate method** only when the failure signature justifies it.
8. **Return evidence**: verified proof or verified steps; otherwise the best candidate plus unresolved obligations and the exact verification blocker.

## Failure-Recovery Ladder
| Symptom | Likely bottleneck | Next move |
|---|---|---|
| Plausible reasoning, invalid next tactic | step selection | Lean-STaR branch/backtrack with verifier feedback |
| Direct proof search branches wildly | abstraction | Draft-Sketch-Prove; create easier subgoals |
| Routine-looking gap times out | premise access/search | LeanHammer; improve premise selection |
| Works on isolated benchmarks, fails in repository | missing/new context | miniCTX-style context packaging |
| Proof is correct but unsuitable for humans/training | objective mismatch | ImProver-style metric-driven rewrite |
| Several methods fail | statement/context/interface issue | validate theorem statement, imports, definitions, toolchain, and verifier before more search |

## SELF_CHECK
Before finalizing:
- Did I identify whether the user's goal is discovery, formalization, completion, debugging, or optimization?
- Did I choose a method whose prerequisites are actually present?
- Did I include the necessary local and cross-file context?
- Did I distinguish informal plausibility from formal verification?
- Did I react to verifier errors by changing the search state or method?
- Did I avoid claiming the lecture says something sourced only from a supplemental paper?
- If I optimized a proof, is the rewritten proof still verified?
- If certainty is unavailable, did I return an explicit unresolved status instead of inventing success?

## Chapter Index
| # | Title | Key Frameworks |
|---|---|---|
| [ch01](chapters/ch01-bridge-and-verifier-loop.md) | Bridge & verifier loop | informal/formal trade-off, proof state, tactic loop |
| [ch02](chapters/ch02-lean-star.md) | Lean-STaR | thought→tactic interleaving, expert iteration, backtracking |
| [ch03](chapters/ch03-draft-sketch-prove.md) | Draft-Sketch-Prove | draft, formal sketch, gap proving, abstraction-level search |
| [ch04](chapters/ch04-leanhammer.md) | LeanHammer | premise selection, retrieval, ATP, reconstruction, Aesop |
| [ch05](chapters/ch05-minictx-research-context.md) | Research-level context | miniCTX, LLMLean, in-file/cross-file dependencies |
| [ch06](chapters/ch06-improver-proof-optimization.md) | Proof optimization | ImProver, metric-driven rewriting, Chain-of-States |

## Topic Index
- **Aesop / tree search** → ch04
- **backtracking / retry** → ch02
- **context selection** → ch04, ch05
- **Draft-Sketch-Prove (DSP)** → ch03
- **expert iteration** → ch02
- **formal sketch / proof gaps** → ch03
- **ImProver** → ch06
- **informal thoughts** → ch01, ch02
- **LeanHammer** → ch04
- **Lean-STaR** → ch02
- **LLMLean** → ch05
- **miniCTX** → ch05
- **premise selection** → ch04, ch05
- **proof optimization** → ch06
- **proof state / tactic** → ch01, ch02
- **verifier feedback** → ch01, ch02, ch06

## Supporting Files
- [glossary.md](glossary.md) — compact definitions and chapter locations
- [patterns.md](patterns.md) — executable methods and fallback logic
- [cheatsheet.md](cheatsheet.md) — routing, decisions, smells, and verification gates

## Scope & Limits
This skill is built from the user-provided Berkeley lecture pack plus the lecture's course-linked materials and corroborating official/project sources. The uploaded `slides.pdf` is a truncated 2,354,768-byte copy with no PDF catalog/page tree/xref/EOF; the same-named official slide deck is 18,176,794 bytes. Therefore slide-by-slide completeness cannot be claimed. Source-derived claims are restricted to content recovered from readable files, detailed lecture notes, the speaker's official page, and the course-linked primary papers. See `provenance/source_map.json` for the audit trail.
