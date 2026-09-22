# Changelog

## 1.4.0 - 2026-09-21

### Added
- Add the subordinate `microclaim-proof-audit.md` reference for line-by-line proof obligations, dependency closure, attack cases, and route/Claim status separation.

### Reason
- Absorb the useful proof-checking pattern under the existing proof owner instead of adding a parallel Skill or truth ledger.

### Affected
- `SKILL.md`, `VERSION`, `references/index.md`, and the new subordinate reference.

### Validation
- Targeted entry/version/reference and WEB_ACTIVE_SKILLS digest checks pass; full Harness remains blocked by the known stale snapshot/manifest baseline.

### Risk
- The reviewed candidate's exact upstream identity and redistribution rights remain unresolved; no source body was imported.

### Rollback
- Restore version 1.3.0 and remove the new reference and navigation entries.

### Source
- Pattern-only review of the `proof-checker` candidate snapshot; `proof-writer` and `formula-derivation` were rejected as duplicate owner surfaces.

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

- Rename and adapt the existing public capability as the Pi-native `ai4math-proof-refutation` owner Skill.
- Preserve candidate-only evidence ceilings and repository-local references.

## 0.5.0

- 增加 reuse-first 定理门：固定 package/version/commit/declaration/import，并要求陈述比较、前提证明和双审计。

## 0.4.0

- proof obligation 按持久 worker 的有界小步推进；路线 blocker 追加记录后换路，stalled 不等于 Claim 完成。

## 0.3.0

- 候选来源状态和 candidate formal file 不得触发研究证明或 Result 晋升。
- 研究库任务必须先绑定明确请求或 active ProblemContract。

## 0.2.0 - 2026-08-26

- 增加 proof-obligation DAG 的唯一节点、依赖存在、无环和开放义务 fail-closed 契约。
- 分离 route status 与原 Claim status，阻止“辅助引理失败即原命题被反驳”的错误升级。
- 接入固定 commit 的 ProofFlow 与 Lean 官方 Skills 证据谱系，并以源码缺陷生成反例压力测试。

## 0.1.0 - 2026-08-13

- 建立定理陈述、证明义务、依赖图、反例攻击和状态分层契约。
