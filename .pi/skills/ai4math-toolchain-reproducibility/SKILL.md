---
name: ai4math-toolchain-reproducibility
description: "网页版数学工具链规划入口。用于选择符号、数值、数据库或形式化路线并生成有界执行计划；不执行工具、不签发回执、不接纳数学结果。"
---

# Math Toolchain（Web constrained）

## When to Use This Skill

- 候选研究需要判断使用 SymPy、SageMath、OEIS、LMFDB、Lean/Mathlib 或其他已登记工具；
- 需要在 symbolic、numeric、database、formalization 路线之间选择；
- 需要为后续受信执行器生成带版本、预算、超时和预期证据能力的计划；
- 需要为已准入工具或可重放 Job 生成低侵入、有预算的性能画像计划。

## Not For / Boundaries

- 不执行工具、profiler 或插桩，不生成伪造 stdout/stderr 或性能测量。
- 不安装软件、访问计算节点、调用 GPU、读取凭据或修改受保护运行时。
- 不用性能画像替代正确性、数学验证、Evidence、Result、Solution 或 admission。
- 不为 canonical actor 规定数学路线、工具顺序或下一研究动作。

## Required Inputs

- 冻结的 ProblemContract、当前 Obligation 和已有 EvidenceLink；
- `governance/control-plane/math-tool-maturity.v1.json`；
- `governance/control-plane/math-knowledge-source.v1.json`；
- `governance/control-plane/math-knowledge-operators.v1.json`；
- 当前 Harness snapshot 与 Web output contract。

## Quick Reference

```text
freeze obligation/target -> check registry and maturity -> select smallest capability
-> bind version/input/budget/failure semantics -> emit not_executed candidate ToolPlan
```

需要性能画像时，再按需加载 `references/runtime-profile-plan.md`；先有正确性基线，后有低侵入测量计划。

## Web Channel Contract

本 Skill 状态固定为 `constrained`：

1. 只能选择已登记、许可闭合且 maturity 足够的工具或来源；
2. 只能输出 `ToolPlan`、`ReusePlan` 或 Candidate 中的建议步骤；
3. 必须写明 exact version、输入摘要、预算、timeout、失败语义和 `evidence_ceiling`；
4. 不得声称命令已经执行，不得生成 stdout/stderr、kernel receipt、semantic review receipt 或 EvidenceLink；
5. 不得安装软件、访问计算节点、调用 GPU、修改 workflow 或写入受保护真相路径；
6. 数据库命中、符号化简和有限数值检查都不能自动成为一般性证明。

## Routing

- 来源与既有结果发现：`ai4math-source-discovery`；
- 推导与候选路线：`ai4math-modeling-derivation`；
- 计算设计：`ai4math-bounded-computation`；
- 自然语言证明义务：`ai4math-proof-refutation`；
- Lean 草稿与形式化计划：`ai4math-lean-formalization`；
- 方法选择：`solve`。

## Minimal Output

```json
{
  "tool_or_source_id": "<registered id>",
  "purpose": "<one bounded obligation>",
  "exact_version": "<required version or query profile>",
  "inputs": [],
  "budget": {"timeout_seconds": 0, "max_output_bytes": 0},
  "expected_artifact": "candidate_only",
  "evidence_ceiling": "<registry ceiling>",
  "execution_status": "not_executed"
}
```

`ToolPlan` 不是执行回执；计划可行、CI 通过、PR 合并或模型自评都不是 Evidence、Result 或 Solution。实际执行必须由网页渠道之外的受信、受预算 Harness 完成并独立回读。

## Examples

### Example 1: Symbolic computation plan

为一个冻结恒等式选择已登记 SymPy 版本，绑定输入摘要、timeout、未求值/分支失败语义，输出 `not_executed` ToolPlan。

### Example 2: Formalization reuse plan

为一个 obligation 选择固定 Mathlib declaration，记录 package/version/commit/import 和 statement relation，不声称 Lean 已运行。

### Example 3: Runtime profile plan

为一个已准入、可重放但缓慢的计算 Job 选择最低侵入的 CPU/内存测量，绑定正确性门、预算、observer effect 和回滚，不执行 profiler。

## Internal package routing

Read `INTERNAL-PACKAGES.json` and `references/internal-package-routing.md` before choosing source material. Load only the smallest applicable internal package. Complete package bodies are bundled under this top-level Skill. Use only repository-relative registry paths; rights remain HOLD and bundling does not grant publication or execution authority.

## Progressive disclosure

Read `references/consolidated-core.md` for capability records, maturity levels, reuse-first selection, environment locks, bounded execution plans, archive/dependency security, multi-stage search/analyzer pipelines, comparator semantics, reproducibility tiers, failure taxonomy and recovery. Load `references/runtime-profile-plan.md` only when the current target needs a bounded performance measurement plan.

## References

- `references/consolidated-core.md`：能力成熟度、版本锁、复用、执行计划、可复现性和失败恢复的项目原创综合。
- `references/internal-package-routing.md`：内部 package 的最小加载、相对路径和权利边界。
- `references/runtime-profile-plan.md`：低侵入性能画像、observer effect、资源预算和插桩回滚计划。

## Maintenance

- Sources: project toolchain contracts and independently rewritten method intake recorded in `CONSOLIDATION-MAP.md`.
- Last updated: 2026-09-21.
- Verification: strict Skill structure check, entry digest reconciliation, and repository Harness validation.
