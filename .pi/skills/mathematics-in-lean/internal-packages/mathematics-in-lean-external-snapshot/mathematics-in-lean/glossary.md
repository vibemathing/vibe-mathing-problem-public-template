# Glossary

**`ae μ`** — filter of facts holding almost everywhere with respect to measure `μ` (Ch 11, 13).

**`aeval`** — algebraic evaluation homomorphism used to evaluate polynomials in algebra elements or endomorphisms (Ch 9, 10).

**`atTop`** — filter describing sufficiently large values in an ordered type (Ch 11).

**Basis** — `Basis ι K V`, a linear equivalence from `V` to finitely supported coordinate functions `ι →₀ K` (Ch 10).

**Bundled morphism** — a structure carrying a function together with laws, such as `MonoidHom`, `RingHom`, `LinearMap`, or `ContinuousLinearMap` (Ch 8–12).

**`Classical.choose`** — extracts a witness from an existence proof under classical logic; useful when defining noncomputable inverses or selections (Ch 4).

**`comap`** — pullback of filters, subobjects, or related structures along a map; often paired with `map` in a Galois connection (Ch 4, 9–11).

**Continuous linear map** — `E →L[𝕜] F`, a bundled linear map with continuity and operator norm (Ch 12).

**`deriv` / `fderiv`** — totalized derivative functions; return default zero where differentiability fails, so evidence-bearing predicates should guard substantive use (Ch 12).

**`Eventually`** — `∀ᶠ x in F, P x`, meaning `P` holds on a set belonging to filter `F` (Ch 11).

**Filter** — upward-closed, finite-intersection-closed collection of sets, used as a generalized set and the common language for limits (Ch 11).

**`Finset`** — computational finite set requiring decidable membership/equality for many operations (Ch 6).

**`Fintype`** — typeclass saying a type has finitely many inhabitants, exposed through `univ` (Ch 6).

**Galois connection** — adjunction such as image/preimage, map/comap, or topology induced/coinduced that converts inequalities across two maps (Ch 4, 9–11).

**`HasBasis`** — description of a filter through a family of basic sets, allowing abstract filter statements to reduce to concrete epsilon/ball criteria (Ch 11).

**`HasFDerivAt`** — proposition asserting a specific continuous linear map is the Fréchet derivative at a point (Ch 12).

**Ideal** — additive subobject of a commutative ring closed under multiplication by arbitrary ring elements; basis for ring quotients (Ch 9).

**Image / preimage** — direct and inverse set transport; image introduces an existential witness, preimage reduces by evaluation (Ch 4).

**`Integrable`** — side-condition predicate controlling most theorems about Bochner integrals (Ch 13).

**`LinearMap`** — `V →ₗ[K] W`, bundled linear map with additive and scalar compatibility (Ch 10).

**`Module.finrank`** — natural-number dimension; returns zero for infinite-dimensional spaces, so substantive finite-dimensional results require assumptions (Ch 10).

**`Module.rank`** — cardinal-valued general dimension, with universe-lift issues made explicit (Ch 10).

**`NeBot`** — typeclass/proposition asserting a filter is nontrivial, needed when existence/cluster arguments would fail for the bottom filter (Ch 11).

**Neighborhood `𝓝 x`** — filter of sets containing a neighborhood of `x`; central representation of local topology (Ch 11).

**Normal subgroup** — subgroup satisfying the condition needed to form a group quotient (Ch 9).

**`outParam`** — typeclass parameter annotation used to steer instance synthesis when some types should be determined by other inputs (Ch 8).

**Quotient lift** — construction defining a function/map from a quotient by proving it respects the equivalence relation or kernel condition (Ch 8–10).

**`SetLike`** — abstraction for bundled subobjects that coerce to sets while retaining structure and extensionality (Ch 8).

**Span** — smallest submodule containing a set; use its universal property (`span_le`) rather than unfolding linear combinations (Ch 10).

**Strong induction** — natural-number induction where the induction hypothesis is available for every smaller value (Ch 5).

**`Tendsto`** — convergence relation `map f F ≤ G` between source and target filters (Ch 11).

**Typeclass diamond** — two inheritance paths producing instances of the same data-bearing parent; harmful when the results are not definitionally equal (Ch 8).

**Universal property** — constructor/lift/uniqueness interface characterizing objects such as quotients, spans, free objects, bases, and induced structures (Ch 8–11).
