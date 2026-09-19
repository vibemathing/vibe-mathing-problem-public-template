# Chapter 7: Finite Sums, Infinite Series, Rearrangement, and Tests

## Core Idea

Chapter 7 moves from finite indexed sums to convergence of partial sums, develops absolute and nonnegative convergence, proves rearrangement results, and formalizes root/ratio tests. Its proof discipline is to make the partial-sum representation explicit, isolate tail estimates, and recognize when the correct limit object is extended-real rather than real-valued.

## Frameworks Introduced

- **Finite-sum algebra first**: finite rearrangement and double-sum manipulations are `Finset`/`Fin` problems. Normalize index ranges and 0-based shifts before invoking ring or combinatorial identities.
- **Series = limit of partial sums**: convergence statements reduce to convergence of a sequence of finite sums. To prove a law for series, first prove the corresponding partial-sum identity, then pass to the limit.
- **Cauchy tail criterion**: a series converges exactly when sufficiently late finite tails are small. For estimates, this is often easier than identifying the final sum.
- **Absolute/nonnegative domination**: absolute convergence controls arbitrary rearrangements and allows comparison; nonnegative series admit monotonic partial sums and order-based tests.
- **Rearrangement safety boundary**: nonnegative or absolutely convergent series are stable under permissible reindexings; conditionally convergent series require care and lead into the later Riemann rearrangement material.
- **Root/ratio tests in extended reals**: limsup/liminf of roots or ratios can be infinite. The source explicitly makes an extended-real subtlety that prose may leave implicit, and some conclusions need finiteness conditions.

## Key Concepts

- finite sums and index shifts;
- formal series and partial sums;
- convergence/divergence and series value;
- absolute vs conditional convergence;
- tails, shifts, telescoping;
- nonnegative comparison and condensation;
- rearrangement via injective/bijective index maps;
- `EReal` limsup/liminf for root/ratio tests.

## Operational Procedure

1. Convert a prose sum into an exact 0-based `Finset.range`/`Fin` expression; write the index translation before proving identities.
2. For a series theorem, define or expose its partial sums and prove the finite algebraic identity there.
3. For convergence, choose between direct known-limit transfer, the Cauchy tail criterion, comparison, monotone boundedness, absolute convergence, or a specialized test.
4. When combining series, prove the relevant absolute convergence or denominator/nonzero hypotheses before rewriting sums.
5. For nonnegative terms, exploit monotonicity of partial sums and order completeness rather than epsilon estimates term-by-term.
6. For rearrangement, prove the index map is injective/bijective and track how finite approximants/tails transform.
7. For root/ratio tests, calculate the `EReal` limsup/liminf first. Prove it lies on the needed side of `1`, and discharge any “finite limsup” technical hypothesis required by the formal statement.
8. Treat equality cases (`= 1`) as inconclusive unless another argument applies.

## Failure Recovery

- **finite sum differs by one endpoint** → resolve `Fin n` versus book `≤ n` convention and rewrite the shifted range.
- **series algebra theorem will not apply** → check absolute convergence or summability prerequisites.
- **comparison proof needs positivity** → isolate eventual/nonnegative hypotheses and work on a tail if necessary.
- **root/ratio test type mismatch** → the limiting ratio/root likely lives in `EReal`; coerce terms deliberately.
- **rearranged series goal is too strong** → determine whether convergence is conditional; absolute/nonnegative assumptions are the stable regime.

## Reference Table

| Series shape | First method |
|---|---|
| telescoping | finite partial-sum identity |
| geometric | standard geometric partial sum/limit |
| nonnegative dominated | comparison / monotone partial sums |
| decreasing nonnegative with powers of 2 | condensation |
| absolute | comparison + rearrangement safety |
| exponential-growth terms | root or ratio test |
| limit test gives exactly 1 | choose another method |

## Anti-patterns

- Manipulating an infinite sum symbol as though it were a finite ring expression before proving convergence.
- Reindexing a conditionally convergent series under an arbitrary permutation.
- Using real limsup for a sequence whose ratios/roots can diverge to infinity.
- Ignoring the source's 0-based indexing when translating a finite combinatorial identity.

## Source Map

`Section_7_1` Finite series; `7_2` Infinite series and absolute convergence; `7_3` Sums of non-negative numbers and condensation; `7_4` Rearrangement of series; `7_5` The root and ratio tests with explicit extended-real semantics.

## Key Takeaways

1. Infinite-series proofs are finite partial-sum proofs plus a convergence passage.
2. Tail estimates are the reusable currency of convergence.
3. Absolute convergence is the main permission slip for algebra and rearrangement.
4. Nonnegative series should be attacked with order/monotonicity whenever possible.
5. Root/ratio tests require careful `EReal` handling and are intentionally inconclusive at the boundary.

## Connects To

- **Chapter 6** supplies sequence convergence, limsup/liminf, and standard limits.
- **Chapter 8** generalizes series to sums over arbitrary/countable sets and then adopts `Summable`/`tsum`.
