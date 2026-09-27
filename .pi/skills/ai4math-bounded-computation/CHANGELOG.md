# Changelog

## 1.6.0 - 2026-09-21

### Added
- Extend the experiment-integrity reference with oracle provenance, model-output-as-ground-truth rejection, minimal sanity runs, and an explicit scale-up gate.

### Reason
- Preserve the useful integrity checks from an experiment bridge without importing deployment, GPU queues, cloud lifecycle, automatic debugging, or paper workflow automation.

### Affected
- `VERSION` and `references/experiment-integrity-audit.md`; the top-level entry contract and digest are unchanged.

### Validation
- Strict Skill validation and targeted version/reference checks are required; full Harness remains subject to the existing stale snapshot reconciliation.

### Risk
- The reviewed candidate is ML-runtime-oriented and has unresolved exact upstream rights; only independently rewritten domain-neutral checks were retained.

### Rollback
- Restore version 1.5.0 and remove the oracle/sanity/scale-up additions and source binding.

### Source
- Pattern-only review of the `experiment-bridge` snapshot bound by SHA-256 in the reference.

## 1.5.0 - 2026-09-21

### Added
- Extend the subordinate experiment-integrity reference with claim-driven experiment design, discriminating evidence, single-factor ablation, sensitivity analysis, aggregation, and negative-result handling.

### Reason
- Absorb reusable experiment-planning and result-analysis methods without importing ML paper workflows, automatic run queues, or a new top-level Skill.

### Affected
- `VERSION` and `references/experiment-integrity-audit.md`; the top-level entry contract and digest are unchanged.

### Validation
- Strict Skill validation and targeted version/reference checks pass; full Harness remains blocked by the known stale snapshot/manifest baseline.

### Risk
- The reviewed candidates are ML/paper-oriented and have unresolved exact upstream rights, so only domain-neutral bounded methods were rewritten.

### Rollback
- Restore version 1.4.0 and remove the second-batch sections and source bindings from the subordinate reference.

### Source
- Pattern-only review of `experiment-plan`, `ablation-planner`, and `analyze-results` snapshots bound by SHA-256 in the reference.

## 1.4.0 - 2026-09-21

### Added
- Add the subordinate `experiment-integrity-audit.md` reference for experiment identity, coverage, failure semantics, bounded resources, and independent replay.

### Reason
- Absorb reusable experiment-audit behavior without importing automated research loops, cloud execution, or another top-level Skill.

### Affected
- `SKILL.md`, `VERSION`, `references/index.md`, and the new subordinate reference.

### Validation
- Targeted entry/version/reference and WEB_ACTIVE_SKILLS digest checks pass; full Harness remains blocked by the known stale snapshot/manifest baseline.

### Risk
- The reviewed candidate's exact upstream identity and redistribution rights remain unresolved; no source body was imported.

### Rollback
- Restore version 1.3.0 and remove the new reference and navigation entries.

### Source
- Pattern-only review of the `experiment-audit` candidate snapshot bound by SHA-256 in the reference.

## 1.3.0

- Bundle every owned original Skill package completely under `internal-packages/` with byte-level manifests.
- Replace private-vault routing with repository-relative, self-contained package paths and preserve HOLD publication status.

## 1.2.0

- Add the top-level internal-package registry and progressive routing guide.
- Bind complete private-local source packages to one primary owner while keeping HOLD bodies out of public output.

## 1.1.0

- Add an independently written consolidated operational core derived from the audited 31-package / 29-source-family review set.
- Bind the entry Skill to the consolidation map, evidence boundaries, failure recovery, and anti-loop discipline without redistributing held source text.

## 1.0.0

- Rename and adapt the existing public capability as the Pi-native `ai4math-bounded-computation` owner Skill.
- Preserve candidate-only evidence ceilings and repository-local references.

## 0.6.0

- 接入数学知识 registry；OEIS/LMFDB/DLMF/SageMath 查询与执行受许可、预算、digest 和 candidate-only evidence ceiling 约束。

## 0.5.0

- 持久研究统一为有界 step；计算必须绑定 timeout、内存/CPU、输出和 producer artifact 配额，high-watermark 只暂停当前 producer。

## 0.4.0

- CandidateObservation 未形成 active ProblemContract 时禁止启动研究计算。
- 工具能力按 surveyed/source_locked/installed/smoke_checked/evidence_capable/verifier_admitted 分层。
- solver、CAS、枚举和外部命令强制 wall-time、线程/内存预算与终止回执。

## 0.3.1 - 2026-08-29

- 支持为 Sage、FEniCSx、Lean/Lake 显式绑定独立运行时，非交互执行不再依赖登录 shell 的 PATH。
- FEniCSx 探针适配 DOLFINx 0.11 `create_unit_square` API，并增加 conda-forge 环境幂等部署脚本。

## 0.3.0 - 2026-08-16

- 新增按领域划分的数学工具目录、独立运行时边界和 evidence 上限。
- 要求任务启动前使用 `check_math_tools.py` 对实际行为做 fail-closed 探测。

## 0.2.0 - 2026-08-15

- 强制 GPU 可行性预检：新增计算类型路由决策表与 `scripts/compute_plan.py` 入口；GPU 只做粗筛，精确裁决回 CPU。

## 0.1.0 - 2026-08-13

- 建立 SymPy/NumPy/SciPy/mpmath/OEIS 计算证据契约和复杂度边界。
