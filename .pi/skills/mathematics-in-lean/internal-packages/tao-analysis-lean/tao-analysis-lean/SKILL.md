---
name: tao-analysis-lean
description: Operational knowledge base from the uploaded teorth/analysis Lean companion to Terence Tao's Analysis I. Use for formalizing or debugging Analysis I exercises in Lean 4, navigating the companion's chapter APIs, choosing textbook-defined versus Mathlib objects, translating epsilon proofs to filters, handling custom naturals/reals/sets, sequences, series, continuity, derivatives, Riemann integration, and the included measure-theory or units supplements.
when_to_use: Tao Analysis Lean, Analysis I Lean, teorth analysis, fill this Analysis I Lean sorry, prove this Tao Analysis exercise in Lean, which teorth/analysis theorem should I use, custom Chapter2 Nat, Chapter5 Real in teorth analysis, Cauchy sequence in Analysis companion, limsup EReal in Tao Analysis Lean, series Summable tsum in companion, continuity Tendsto in Analysis Lean, derivWithin in Tao Analysis, Riemann integral in Tao Analysis Lean, Riemann-Stieltjes in teorth analysis, Analysis MeasureTheory companion, teorth UnitsSystem Scalar
allowed-tools: Read Grep
argument-hint: "[goal, theorem/exercise name, concept, source module, or chapter]"
---

# Tao Analysis Lean Companion

**Source**: uploaded snapshot of `teorth/analysis`, a Lean companion to Terence Tao's *Analysis I*  
**Coverage**: 74 literate Analysis I modules (Ch. 2–11, App. A–B), plus uploaded MeasureTheory, Misc, and Tools modules  
**Generated**: 2026-09-12  
**Pinned environment**: Lean `v4.29.0-rc8`, Mathlib `v4.29.0-rc8`; Verso documentation enabled; command-line `sorry` warnings suppressed by project configuration.

## How to Use This Skill

- **No argument** — use the core frameworks below to orient an Analysis I Lean task.
- **Topic or theorem** — route through the Task Router, then read the matching chapter file.
- **Module/chapter** — load that chapter directly and follow its operational procedure.
- **Proof hole / `sorry`** — reconstruct the textbook-style dependency chain, then run the failure-recovery and SELF_CHECK gates.

Treat this skill as a proof-routing and API-selection guide. The uploaded source is an annotated formal companion; the original *Analysis I* PDF/EPUB was not included. Use the companion's mathematical structure and Lean conventions, and do not invent claims about unseen book text.

Before writing a proof, identify all four coordinates:

1. **Mathematical layer** — naturals/sets/reals/limits/series/cardinality/continuity/derivatives/integration/measure theory.
2. **Project phase** — custom textbook construction, bridge/epilogue, or native Mathlib phase.
3. **Representation** — `ℕ` vs `Chapter2.Nat`, `ℝ` vs `Chapter5.Real`, `Real` vs `EReal`, set vs subtype, epsilon predicate vs filter, finite sum vs `tsum`.
4. **Semantic preconditions** — validity assumptions that prevent a totalized definition from returning a default or “junk” value.

Then load the relevant chapter file below. Prefer local declarations and helper lemmas from that source section before reaching for a much stronger unrelated Mathlib theorem. The project deliberately favors proofs that track the textbook argument over proof golfing.

## Core Frameworks & Mental Models

### 1. Phase-aware API selection

Use the definition family active in the source section. Chapter 2 builds a custom natural-number theory and only later proves an equivalence with `ℕ`. Chapter 3 builds a custom set theory and then retires it. Chapters 4–5 construct integers, rationals, and reals by quotient-style models before bridging to Mathlib. Chapters 6 onward increasingly use Mathlib directly. Section 8.2 explicitly transitions infinite sums to `Summable`/`tsum`; Chapter 10 is built around Mathlib differentiation APIs.

**Decision**: if a goal is inside an early section, prove with that section's local API. If the section is an epilogue or later phase, use the bridge theorem and continue with Mathlib. Avoid silently coercing across phases; make the conversion explicit when Lean's elaborator cannot infer it.

### 2. Faithful proof reconstruction

When filling a `sorry`, reconstruct the mathematical dependency chain first: definitions → local lemmas → target theorem. Keep intermediate facts visible with `have`, `obtain`, `calc`, and named helper lemmas. Use automation (`simp`, `linarith`, `omega`, `ring`, `norm_num`, `aesop`) to discharge local algebra/order/logical obligations after the conceptual steps are explicit.

A short proof is useful only when it preserves the intended concept. If a one-line Mathlib result bypasses the section's construction, use it only when the user explicitly wants an idiomatic Mathlib proof or the source has already transitioned to Mathlib.

### 3. Totalization guard

Several mathematical operations that are partial in prose are total in Lean. Examples include formal limits of unsuitable sequences, generalized sums of non-absolutely-convergent functions, one-sided limits when no limit exists, derivatives selected by `derivWithin`, roots outside intended domains, and some Riemann–Stieltjes constructions.

**Rule**: before rewriting with the semantic meaning of such an operation, prove its validity hypothesis. A theorem about a default value says little about the intended mathematical object. When a proof unexpectedly collapses to `0`, inspect the definition's invalid branch before continuing.

### 4. Index translation

The companion systematically prefers 0-based `ℕ`/`Fin` indexing. When importing a textbook statement that starts at 1, write the index map first (`n ↦ n+1`, shifted `Fin`, or a sequence `from` operation), prove its bounds, then transform the algebra. Off-by-one errors often masquerade as theorem-search failures.

### 5. Epsilon ↔ filter bridge

Early limits expose epsilon/Cauchy predicates for pedagogy. Later files provide or use `Filter.Tendsto`, `nhds`, `atTop`, and related Mathlib APIs. Use epsilon form to unfold the textbook definition; use filter form to compose limits, invoke library theorems, or handle limits at infinity. Convert at a named bridge theorem, then stay in one representation until the local argument is complete.

### 6. Real ↔ extended-real discipline

Use `EReal` when `⊤`/`⊥` are legitimate values: sequence suprema/infima, limsup/liminf, unbounded sets, root/ratio tests, and measure-theoretic quantities. Establish finiteness before coercing back to `ℝ`. If a theorem needs a real-valued bound, check that the extended-real expression is neither infinity.

### 7. Finite → series → arbitrary sums → integrals

The aggregation stack progresses through `Finset` sums, partial sums and series convergence, nonnegative/absolute convergence, general `Summable`/`tsum`, Riemann sums/integrals, and the supplemental Lebesgue integral. Route at the highest layer justified by the current section; use bridge lemmas rather than re-proving lower-level convergence facts.

### 8. Type-mismatch diagnosis

When the mathematics is clear but Lean rejects a term, classify the mismatch before changing the proof:

- custom type vs Mathlib type → use an epilogue equivalence;
- set vs subtype → insert/substitute `Subtype.val` or restate membership;
- `ℝ` vs `EReal`/`ENNReal` → use an explicit coercion and prove finiteness/nonnegativity;
- quotient representative vs quotient value → use the quotient API, not representative equality;
- dimension-indexed `Scalar d` vs propositionally equal dimension → cast or embed into `Formal`;
- 1-based vs 0-based index → shift explicitly.

`change`, `simpa`, `convert`, `norm_cast`, extensionality, and bridge lemmas are repair tools after the mismatch class is known.

## Task Router

| Task signal | Load | Primary route |
|---|---|---|
| Peano axioms, custom natural arithmetic | [ch02](chapters/ch02-natural-numbers.md) | custom `Chapter2.Nat` → epilogue equivalence |
| custom sets, functions, images, cardinality | [ch03](chapters/ch03-set-theory.md) | `Chapter3.SetTheory` → ZFSet/Mathlib bridge |
| quotient integers/rationals, rational gaps | [ch04](chapters/ch04-integers-rationals.md) | representative → quotient → arithmetic |
| Cauchy construction of reals, LUB, rational powers | [ch05](chapters/ch05-real-construction.md) | sequence equivalence → `Chapter5.Real` → ℝ bridge |
| sequences, limits, EReal, subsequences | [ch06](chapters/ch06-sequences-limits.md) | epsilon/Cauchy ↔ filters; Real/EReal guard |
| finite/infinite series, tests, rearrangement | [ch07](chapters/ch07-series.md) | partial sums → convergence → absolute/nonnegative criteria |
| countability, `tsum`, choice, order/Zorn | [ch08](chapters/ch08-countability-choice-order.md) | cardinal API; custom sums → `Summable`/`tsum` |
| subsets of ℝ, function limits, continuity | [ch09](chapters/ch09-continuity.md) | topology/filters; domain and adherent-point checks |
| derivatives, MVT, inverse, L'Hôpital | [ch10](chapters/ch10-differentiation.md) | `HasDerivWithinAt`/`derivWithin` + domain conventions |
| Riemann/Riemann–Stieltjes, FTC | [ch11](chapters/ch11-riemann-integration.md) | partitions → integrability → FTC/transform rules |
| basic Lean logic/proof syntax | [ch12](chapters/ch12-appendix-proof-language.md) | implication/quantifiers/equality tactics |
| decimal representations | [ch13](chapters/ch13-decimal-representations.md) | digit/expansion representation and non-uniqueness |
| uploaded measure-theory modules | [ch14](chapters/ch14-measure-theory-supplement.md) | elementary/Jordan → Lebesgue → Mathlib Measure |
| units, SI, finite choice, probability, Erdos utilities | [ch15](chapters/ch15-misc-lean-utilities.md) | specialized supplemental APIs |

## Failure Recovery

1. **Theorem seems unavailable** → verify the current phase and imports; search the local section and its immediate predecessors before global Mathlib.
2. **Types almost match** → stop theorem search and repair representation/coercion/indexing first.
3. **Limit/sum/derivative gives an implausible default** → inspect validity assumptions and totalized branches.
4. **Real proof stalls around infinity** → move to `EReal`; recover `ℝ` only after finiteness.
5. **Epsilon manipulation explodes** → cross a documented bridge to `Filter.Tendsto` and use compositional APIs.
6. **Automation fails** → expose the conceptual intermediate statement; then use `simp`/`linarith`/`omega`/`ring` locally.
7. **A proof compiles but bypasses the chapter** → rewrite with the source section's definitions if the user's goal is companion-style study.
8. **The source contains `sorry`** → treat the statement as an exercise/specification. Do not cite its missing proof as evidence for another step unless the theorem is accepted in the current environment and the user permits using it.

## SELF_CHECK

Before finalizing a proof or explanation, verify:

- The user's target theorem/exercise and intended proof style are identified.
- The selected chapter/API matches the source phase.
- Index origin, domains, nonzero/positivity/boundedness/convergence hypotheses are explicit.
- No semantic claim relies on a junk/default branch.
- Real/extended-real and set/subtype coercions are justified.
- Any use of classical choice is acceptable for this project context.
- The proof follows the local mathematical dependency chain and does not accidentally assume a later theorem.
- If compilation was unavailable, label code as uncompiled and give the exact point most likely to need API adjustment.

## Chapter Index

| File | Coverage |
|---|---|
| [ch02](chapters/ch02-natural-numbers.md) | §2.1–2.3 + natural-number epilogue |
| [ch03](chapters/ch03-set-theory.md) | §3.1–3.6 + ZFSet epilogue |
| [ch04](chapters/ch04-integers-rationals.md) | §4.1–4.4 |
| [ch05](chapters/ch05-real-construction.md) | §5.1–5.6 + real-number epilogue |
| [ch06](chapters/ch06-sequences-limits.md) | §6.1–6.7 + Mathlib-limit epilogue |
| [ch07](chapters/ch07-series.md) | §7.1–7.5 |
| [ch08](chapters/ch08-countability-choice-order.md) | §8.1–8.5 |
| [ch09](chapters/ch09-continuity.md) | §9.1–9.10 |
| [ch10](chapters/ch10-differentiation.md) | §10.1–10.5 |
| [ch11](chapters/ch11-riemann-integration.md) | §11.1–11.10 |
| [ch12](chapters/ch12-appendix-proof-language.md) | Appendix A.1–A.7 |
| [ch13](chapters/ch13-decimal-representations.md) | Appendix B.1–B.2 |
| [ch14](chapters/ch14-measure-theory-supplement.md) | uploaded `Analysis/MeasureTheory/*` |
| [ch15](chapters/ch15-misc-lean-utilities.md) | uploaded `Analysis/Misc/*`, `Analysis/Tools/*` |

## Topic Index

- **absolute convergence, rearrangement, root/ratio tests** → ch07, ch08
- **adherent/limit/isolated points, Heine–Borel** → ch09
- **axiom of choice, Zorn, well-ordering** → ch08
- **Cauchy sequences, constructed real numbers** → ch05
- **continuity, uniform continuity, limits at infinity** → ch09
- **custom naturals / Peano** → ch02
- **custom set theory / Russell / Cartesian products** → ch03
- **derivatives, Rolle, MVT, inverse, L'Hôpital** → ch10
- **EReal, sup/inf, limsup/liminf** → ch06
- **finite sums / infinite series** → ch07
- **integers, rationals, quotient constructions** → ch04
- **Lebesgue/Jordan/measure spaces** → ch14
- **logic, quantifiers, equality tactics** → ch12
- **Riemann / Riemann–Stieltjes / FTC** → ch11
- **Summable / tsum, countability** → ch08
- **units and dimensioned scalars** → ch15

## Supporting Files

- [glossary.md](glossary.md) — project-specific terms and representation bridges
- [patterns.md](patterns.md) — reusable proof and diagnostic procedures
- [cheatsheet.md](cheatsheet.md) — compact routing and failure table

## Scope & Limits

This skill is grounded in the uploaded Lean companion snapshot. It can guide proofs, navigation, and API choice without the original book file. It does not supply hidden solutions for every exercise, and many source theorems intentionally contain `sorry`. For exact textbook prose or claims outside the formal companion, consult a licensed copy of *Analysis I*. For compilation, use the project-pinned Lean/Mathlib environment when available.
