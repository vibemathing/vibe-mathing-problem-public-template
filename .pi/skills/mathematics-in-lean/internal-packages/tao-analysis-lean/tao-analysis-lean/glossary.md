# Glossary

**Absolute convergence** — convergence strong enough to control the series of absolute values; a key condition for safe rearrangement and algebra (Ch. 7–8).

**Adherent point** — a point approached by points of a set; used to state closure and uniqueness conditions for limits (Ch. 9).

**BoundedInterval** — project structure representing bounded real intervals; different constructors may coerce to the same empty set (Ch. 11, Measure Theory).

**Cauchy sequence** — a sequence whose sufficiently late values are mutually close; used to construct reals and characterize convergence (Ch. 5–6).

**Chapter2.Nat** — custom natural-number type used only for the foundational Chapter 2 development; bridged to `ℕ` in the epilogue.

**Chapter5.Real** — real-number type constructed from rational Cauchy sequences; bridged to Mathlib `ℝ` in the Chapter 5 epilogue.

**Convergesto** — chapter-level epsilon definition of function convergence at a point, with a bridge to `Filter.Tendsto` (Ch. 9).

**EReal** — extended real numbers with `⊤` and `⊥`; preferred for unrestricted sup/inf, limsup/liminf, and infinity-sensitive quantities (Ch. 6–7, supplements).

**EventuallySteady** — eventually ε-steady behavior for Chapter 5 rational sequences, used in the Cauchy definition.

**Filter.Tendsto** — Mathlib's compositional convergence relation; preferred after crossing the project's epsilon/filter bridges (Ch. 6, 9–10).

**Formal** — graded commutative ring used by `UnitsSystem` to normalize algebra across dimension-indexed `Scalar` types (Misc supplement).

**HasDerivWithinAt** — relation asserting a specified derivative within a set; preferred proof object for Chapter 10 calculus.

**IntegrableOn** — project predicate for Riemann integrability on a bounded interval/set context (Ch. 11).

**Junk/default value** — implementation value assigned to make an otherwise partial mathematical operation total. Semantic theorems require the operation's intended validity hypotheses.

**LebesgueMeasurable** — custom/supplemental measurable-set notion used before the MeasureTheory transition to native Mathlib infrastructure.

**Limit point** — adherent point of a set with the point itself removed; controls uniqueness/derivative conventions (Ch. 9–10).

**LIM / lim** — totalized formal/numeric limit operators in construction-oriented chapters; use only after proving convergence.

**limsup / liminf** — tail-envelope limit bounds, naturally valued in `EReal` when unbounded behavior is possible (Ch. 6–7).

**Mathlib bridge** — theorem/equivalence connecting a custom textbook construction to the standard Mathlib type/API; often marks the point after which the custom layer is retired.

**Partial sum** — finite sum of an initial segment; the sequence whose limit defines an infinite series (Ch. 7).

**Riemann–Stieltjes integral** — integration with respect to an integrator `α`, built using jumps/`α_length` and regularity assumptions (Ch. 11).

**Scalar d** — unit-aware scalar quantity indexed by a dimension `d`; propositionally equal dimensions can still require casts (Misc supplement).

**Sequence.from** — Chapter 5 operation shifting the start of a sequence; values outside the intended start region inherit totalized behavior.

**SetTheory** — Chapter 3 custom ZF-style set-theory structure with atoms; educational layer later retired in favor of Mathlib sets/ZFSet.

**Summable** — Mathlib predicate for convergence of arbitrary indexed sums; preferred after Section 8.2.

**tsum** — Mathlib infinite-sum operator paired with `Summable`; the long-term summation API after the Chapter 8 bridge.

**Uniform continuity** — a single δ works uniformly over the domain for each ε; obtained from continuity on compact intervals and used in Riemann integrability (Ch. 9, 11).

**Zero-based indexing** — project convention using `ℕ`/`Fin` starting at 0; textbook 1-based sequences/sums must be shifted explicitly.
