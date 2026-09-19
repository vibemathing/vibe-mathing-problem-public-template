# Consolidated core: bounded mathematical computation

## Purpose

Use finite, exact, symbolic, numeric or solver-backed computation to falsify, discover, measure or verify a precisely bounded claim. Computation emits observations and receipts; it does not automatically prove a universal mathematical statement.

## Computation request

Freeze:

- mathematical predicate being tested;
- encoding and decoding maps;
- instance domain and enumeration/sampling rule;
- algorithm and implementation identity;
- exactness model: integers/rationals, algebraic numbers, floating point, interval arithmetic, symbolic rewriting or solver theory;
- resource budget and termination condition;
- expected witness/certificate/output;
- replay command and environment;
- evidence ceiling.

If these cannot be stated, return a computation design rather than running an unscoped experiment.

## Method routing

### Exact enumeration

Use when the domain is finite and generation completeness can be justified. Record canonicalization, isomorphism rejection, counts at every filter and an independent membership check.

### Symbolic computation

Record simplification assumptions, branch conditions, domains, normalization conventions and whether transformations are equivalences. Check results by substitution or a second method where possible.

### SAT/SMT/constraint solving

Provide the mathematical-to-solver encoding, theory assumptions, bounds and model decoding. Preserve proof objects or unsat certificates when supported. `unknown`, timeout and incomplete theory support are not negative results.

### Numeric computation

Use controlled precision, conditioning analysis, error bounds and interval/enclosure methods when sign or inequality matters. Separate empirical stability from proved stability.

### Randomized search

Freeze seeds, distributions, rejection rules and sample counts. A failure to find a witness estimates behavior only under that distribution; it is not exhaustive evidence.

### Optimization/evolutionary search

Record objective, constraints, initialization, mutations, stopping rule and all post-validation. A high score is not a legal mathematical witness until decoded and checked.

## Verification-first experiment design

Prefer outputs that can be cheaply checked:

- explicit counterexample witnesses;
- certificates with independent checkers;
- traces of transformations;
- exact counts with conservation checks;
- hashes of inputs and outputs;
- small minimized examples;
- comparison against a trusted reference implementation.

The generator and checker should be separated whenever feasible. Avoid a single code path defining, generating and validating the same object.

## Completeness claims

To claim exhaustive coverage, establish:

1. finite search domain;
2. complete generator;
3. sound filters;
4. duplicate handling that does not remove distinct legal cases;
5. deterministic termination;
6. coverage counts or a mathematical counting argument;
7. replay under the pinned environment.

Without all seven, use “searched the stated sample/bound,” not “verified all cases.”

## Counterexample handling

For a found witness:

- decode it into source-domain objects;
- independently check every premise and the negated conclusion;
- minimize it without changing validity;
- rule out overflow, precision, parser and symmetry artifacts;
- save a human-readable witness plus machine-checkable form;
- state exactly which claim it refutes.

## Negative search handling

“No witness found” must include bounds, generation method, sample size, seeds, runtime and filters. Its value may be:

- removing a naive family;
- suggesting a stronger invariant;
- calibrating minimal size;
- exposing a performance barrier;
- motivating a proof obligation for completeness.

It is never silently promoted to existence/nonexistence proof.

## Resource and safety contract

Set wall-clock, CPU, memory, process, file-count and output-byte limits. Use safe working paths, deny secrets, and clean descendants on timeout. Preserve a checkpoint before changing algorithms or bounds. High-watermark means stop/rotate/compress the current producer, not erase evidence.

## Reproducibility receipt

Record source digest, command, parameters, tool versions, platform-relevant facts, start/end status, exit code, timeout, seeds, input/output digests, checker result and known nondeterminism. Distinguish executable success from mathematical acceptance.

## Failure recovery

- **Timeout:** reduce scope or improve algorithm with a new checkpoint; do not claim a result.
- **Memory blow-up:** stream, canonicalize, partition or derive a tighter bound.
- **Numeric instability:** increase precision, rescale, use intervals or reformulate.
- **Solver unknown:** change only with a documented theory/encoding reason.
- **Generator/checker disagreement:** quarantine output and debug identity/semantics first.
- **Repeated bound increases:** require a mathematical reason why the new bound is informative.

## Evidence ceiling

Finite exact checks support only the frozen finite domain unless a separate proved reduction transfers them. Numeric and randomized checks are observations. Symbolic/solver outputs cover their exact encoding. None replace statement-faithfulness or independent admission.
