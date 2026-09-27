# Consolidated core: toolchain and reproducibility

## Purpose

Determine whether a proposed mathematical toolchain can safely and reproducibly transform specified inputs into bounded outputs. Tool selection remains with the canonical research actor; authorization and evidence admission remain independent.

## Capability record

For each tool capture:

- name, source, immutable revision and license;
- accepted input types and limits;
- output types, certificates and diagnostics;
- parameters and defaults;
- prerequisites and dependency closure;
- runtime, network, credential and write requirements;
- failure and timeout semantics;
- deterministic/nondeterministic behavior;
- checkpoint/resume support;
- evidence ceiling and trusted checker;
- maintenance and compatibility status.

A documentation claim is not an installed capability.

## Maturity ladder

Keep distinct:

1. surveyed;
2. source locked;
3. installed;
4. smoke checked;
5. evidence capable;
6. verifier admitted.

Promotion requires a receipt for the exact level. Finding a repository or producing a build plan does not skip levels.

## Reuse-first selection

Compare in order:

1. existing admitted project capability;
2. mature external implementation;
3. thin adapter;
4. composition of existing tools;
5. controlled extension/fork;
6. new implementation only when necessary.

Evaluate semantic fit, license, maintenance, security, version compatibility, resource budget, recoverability and evidence ceiling—not popularity alone.

## Environment lock

A reproducible environment records OS/runtime-relevant facts, language/tool versions, package locks, repository commits, build flags, environment variables that affect semantics, hardware dependence where relevant and container/image digest if used. Never store secrets in the lock.

For Lean, bind `lean-toolchain`, Lake manifest, Mathlib revision, imports and options. For solver/computation stacks, bind solver version, theory/configuration, numeric libraries and precision.

## Execution plan

Specify:

- exact input digests;
- safe working root;
- command and parameters;
- CPU/memory/wall-clock/process/output caps;
- network and credential policy;
- expected outputs and checker;
- timeout cleanup;
- checkpoint and retry semantics;
- reproducibility receipt path.

Retry is a new execution unless resuming the same verified checkpoint.

## Security boundary

Treat source packages, web pages and model output as untrusted data. Audit archive paths, symlinks, executable files, dependency scripts, network calls and environment reads. Use least privilege. Never infer safety from a license or a successful build.

## Search/index/analyzer pipelines

For multi-stage systems record each transformation separately: parse, normalize, index, embed, retrieve, generate, elaborate, check. Schema and revision must agree across stages. Search relevance is not theorem validity; static-analysis output is not kernel evidence.

## Comparator/evaluator systems

Define pristine input, candidate mutation, isolation boundary, checker invocation and scoring semantics. A score is meaningful only under the frozen comparator. Pin changes require security and semantic re-audit. Preserve raw verdicts and avoid converting infrastructure failure into mathematical failure.

## Reproducibility tiers

- **rerunnable:** command and inputs recorded;
- **repeatable:** same environment reproduces result;
- **independently replayable:** separate actor/environment reproduces it;
- **cross-implementation checked:** independent implementation agrees;
- **admitted evidence:** applicable gate accepts the capability and receipt.

Use the exact tier reached.

## Failure taxonomy

Separate:

- unavailable dependency;
- build/configuration error;
- permission/sandbox denial;
- resource exhaustion/timeout;
- parser/schema mismatch;
- tool `unknown` or incomplete algorithm;
- nondeterministic disagreement;
- mathematical counterexample or proof failure.

Only the last category is directly mathematical, and still requires faithful encoding.

## Recovery

- pin drift: restore or explicitly migrate with before/after checks;
- stale cache/index: rebuild from source identity and validate counts;
- backend outage: preserve local candidate and report unavailable capability;
- incompatible toolchain: use a declared adapter or isolated environment, not silent upgrades;
- oversized output: stream, summarize with digest, rotate or checkpoint;
- repeated failure: change a relevant dependency, configuration or method; do not rerun blindly.

## Receipt

Return capability identity, maturity level, environment lock, input/output digests, command, resource limits, exit/timeout state, checker result, nondeterminism, security findings, evidence ceiling and remaining blockers. Tool success never by itself admits a mathematical result.
