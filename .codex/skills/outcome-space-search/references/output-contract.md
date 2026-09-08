# OSPS Candidate Plan Output Contract

## 1. 角色

`osps-plan.v0.2` 是一个可审查的候选规划包，用于在正式 Outcome Graph schema/runtime 出现之前表达一次有界 OSPS 分析。它不是 owner ledger，也不能被 Result 或 Solution 直接消费为数学证据。

```text
artifact_role = candidate-planning-only
digest_policy = sha256-canonical-json-nfc-v1
relation_status = candidate
propagation = none
requested_budget.authorized = false
non_claims.* = false
```

## 2. 核心字段

| 字段 | 含义 |
| --- | --- |
| `analysis_id/plan_version/generated_at` | 本次分析身份、版本和时间；version > 1 必须绑定 superseded plan |
| `problem_contract_ref` | Problem ID、contract version、statement/scope/acceptance digests、acceptance policy pointer 和 owner locator |
| `root_outcome_id` | 忠实根 resolution node |
| `outcomes[]` | 精确 statement/scope/digest/closure/value/status 的候选节点 |
| `relations[]` | 仅 candidate、无自动传播的 typed Lines |
| `frontier_policy` | 固定 `pareto-then-diversity`、默认 3/硬上限 9、exception 和维度语义 |
| `frontier[]` | Outcome × Route × owner Skill lane；含可重算 route signature |
| `deferred[]` | 未选目标及范围化原因 |
| `input_refs` | failed route、obligation、source、candidate/evidence/result 指针；FailedRoute 必须附 structural route signature |
| `observations[]` | 外部可观察事实及 locator；不含隐藏思维链 |
| `non_claims` | 明确未执行、未授权、未签证据、未准入 Result、未闭合根 |

## 3. 消费边界

允许消费者：

- 人工/Agent 审查候选 Outcome taxonomy；
- router 为某一 lane 选择一个 owner Skill；
- 未来 adapter 把经过重验的 plan 转成正式 owner schema 输入；
- 测试器执行错绑、重复、传播和能力声明攻击。

禁止消费者行为：

- 把 plan 当正式 Outcome Graph current version；
- 因 plan 中存在 root node 或高优先 lane 创建 Result；
- 从 priority 值推断数学真值；
- 绕过 F05/F12 授权启动并发任务；
- 把 candidate relation 直接升级为 admitted logical Line；
- 将 plan 复制进 Body manifest 代替 reference-only owner pointer。

## 4. 文件位置

private central research 可把实例保存在 task/candidate 作用域；Web 问题仓只能放在 profile 已允许的候选路径，例如：

```text
research/artifacts/candidates/<candidate-id>/osps-plan.json
research/artifacts/source-notes/<note-id>-osps-analysis.json
```

不得写入：

```text
.codex/skills/**
governance/**
problem-library/records/**
research/schema/**
research/records/**
result-library/**
.github/workflows/**
```

Skill 包自带的 `valid-minimal-plan.json` 是合成 fixture，无数学业务含义。validator 只证明 v0.2 结构、digest、引用、连通和 frontier 内部不变量成立；它不证明候选关系、priority basis 或数学陈述为真。
