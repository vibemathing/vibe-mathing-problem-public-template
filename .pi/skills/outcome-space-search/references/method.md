# OSPS Candidate Planning Method

## 1. 方法身份

OSPS（Outcome-Space Parallel Search）在 VibeMath 中是 F04 结果空间执行面。它把单一“求解问题”请求展开为一组语义可区分、局部闭合谓词可检查的 OutcomeNode 候选，再在固定边界内选择少量 frontier lanes。

本方法不等于：

- AND/OR、MCTS、HTPS 或任一外部搜索算法的重命名；
- PWTSJ/F05 的 Job scheduler；
- proof-obligation DAG；
- Candidate/Evidence/Result ledger；
- 自动关闭数学根命题的规则引擎。

## 2. 输入冻结

在任何展开前，必须读取 owner truth source 并冻结：

```text
problem_id
contract_version
statement_digest
statement/domain/quantifiers/definitions
assumptions/allowed_axioms
acceptance predicate
current failed-route refs + route-signature digests
current obligation/evidence/result refs
frontier and budget-request bounds
```

缺 active lifecycle、精确 digest 或 acceptance predicate 时返回 `blocked_missing_problem_contract`，不生成 plan。

## 3. 根节点归一化

根 resolution node 必须忠实表达 ProblemContract 的解决目标。根 statement digest 绑定陈述规范化表示；scope digest 绑定定义域、量词、假设与允许公理。二者作用不同，不能只用一个自然语言标题代替。0.2.0 固定 `sha256-canonical-json-nfc-v1`：字符串先统一换行并做 Unicode NFC，映射键排序、紧凑 UTF-8 JSON 后取 SHA-256；validator 对每个 Outcome 重算，不接受任意 digest 占位值。

根节点 closure predicate 说明“什么证据在什么语义范围内足以关闭本节点”，但 Skill 本身不判断它已满足。

## 4. 候选结果展开

按七个 family 生成候选，但只保留具有独立 statement 和 closure predicate 的项：

1. `resolution`：完整证明、完整反例、忠实 resolving equivalence/reduction；
2. `structural`：刻画、分类、不变量、障碍、正规形、必要/充分条件；
3. `scope`：特殊、加强、弱化、有界、条件命题；
4. `quantitative`：界、阈值、渐近、锐性；
5. `constructive`：witness、构造族、算法、归约、certificate；
6. `negative_knowledge`：失败路线、方法障碍、不相容假设、中间反例；
7. `meta`：陈述修订、来源/定义缺口、新义务、图修订。

“尝试方法 X”“跑更多样例”“让模型再想想”都不是 OutcomeNode。

## 5. 语义身份与去重

候选身份键为：

```text
(statement_digest, scope_digest)
```

处理顺序：

1. 相同键：拒绝重复节点；
2. statement 相同但 scope 不同：保留两个节点并审查 specializes/generalizes/strengthens/weakens；
3. 一个节点含多个不能共享 closure predicate 的目标：split；
4. 只有经独立语义审查证明完全重复时才提出 merge；
5. 相似标题、embedding 或仓库邻近只能触发 review，不能建立等价。

## 6. 关系层

Skill 只允许提出 candidate relation：

```text
line.branches_to
line.depends_on
line.implies
line.equivalent_to
line.refutes
line.strengthens
line.weakens
line.specializes
line.generalizes
line.subsumes
line.blocked_by
line.merges_with
line.invalidates
line.supersedes
```

每条线都要有端点、scope basis 和 basis refs。`relation_status=candidate`、`propagation=none` 是本 Skill 的硬限制。逻辑线是否 admitted 由语义/证据 owner 在别处裁决。validator 拒绝重复 typed edge，并要求所有非根 Outcome 至少在忽略方向的候选关系投影中与 root 连通；这只证明没有孤立规划节点，不证明逻辑方向或蕴含成立。

Outcome Graph 可以含逻辑环；若后续要派生执行依赖投影，必须另行证明 DAG 或声明固定点语义。

## 7. Frontier 选择

### 7.1 硬门

候选 lane 必须同时满足：

- Outcome statement/scope/closure predicate 明确；
- 未精确重复已登记 failed route；
- owner skill 与目标类型匹配；
- stop condition 可观察；
- requested budget 有界且明确标记尚未授权；
- route signature 未与任一输入 FailedRoute signature 重复。

### 7.2 九维向量

每维取 `0..4`，每个值都必须有文字 basis 与引用：

| 维度 | 方向 | 含义 |
| --- | --- | --- |
| root_relevance | 高优 | 对根命题的逻辑/信息关联 |
| mathematical_value | 高优 | 独立数学价值和复用价值 |
| semantic_clarity | 高优 | statement/scope/closure 可审查程度 |
| verification_feasibility | 高优 | 有无现实且适用的检查路径 |
| information_gain | 高优 | 成败能否显著更新路线判断 |
| route_novelty | 高优 | 是否避开已登记死路或同质上下文 |
| reuse_value | 高优 | 是否可服务多个 Outcome/Obligation |
| estimated_cost | 低优 | 请求资源的相对成本 |
| epistemic_risk | 低优 | 语义漂移、自验证、近似外推等风险 |

这些是选择特征，不是命题真值或置信度。

### 7.3 Pareto + 多样性

1. 移除被另一 lane 在全部收益维度不差、成本/风险不高且至少一维更优的候选；
2. 在非支配集合内优先覆盖不同 Outcome family、route、representation 与 owner skill；
3. 限制 frontier 数量；默认不超过 3，schema 上限为 9；超过默认值必须给出带已绑定引用的 `limit_exception`；
4. validator 机械拒绝 frontier 内被另一选中 lane 严格 Pareto 支配的项；
5. 保存 deferred/rejected 的显式原因；
6. 不用未披露权重的 scalar score 打破平局。

## 8. Handoff 与 F05 边界

每条 lane 必须绑定恰好一个 owner：

```text
math-discovery | math-derivation | math-computation
math-proof | math-formalization | solve | math-toolchain
```

OSPS 只提出 `requested_budget` 和 `stop_condition`。每条 lane 还必须保存 structural `route_signature`：method family、representation、关键假设 digest、工具能力引用及其重算 digest；`route_id` 改名不能创造新路线。Harness/F05/F12 另行决定是否授权并实例化 Task/Step/Job。`outcome-space-search` 不能成为自己的执行 owner。

## 9. 更新规则

只根据外部可观察输入更新：

- 新 source/semantic review → add/split/merge candidate；
- FailedRoute/Obstruction → block/reprioritize/new negative node；
- CandidateArtifact → candidate_found observation，但不关闭节点；
- valid applicable EvidenceLink/Result → 提议状态重算，由 owner runtime 执行；
- contract digest 改变 → 旧 plan 失去当前适用性，必须重建。

历史 plan 和失败路线不删除。Skill plan 可 supersede 旧 plan，但不是 append-only owner ledger。

## 10. 根传播安全表

| 已观察事项 | 允许的候选更新 | 禁止推断 |
| --- | --- | --- |
| special case closed | 标记该 scope 节点待 owner 重算 | general root closed |
| necessary condition established | 更新 structural node | root proved |
| strengthening 被反例推翻 | block strengthening route | weaker root refuted |
| faithful root counterexample admitted | 提议 root refutation 重算 | Skill 自行签发 Result |
| equivalent statement proof | 等待两方向等价与 faithfulness | 单向关系关闭 root |
| proof/counterexample conflict | 进入 F09 conflict audit | 选择模型偏好的结论 |

## 11. 停止条件

完成一次 Skill 调用需要：

- plan 通过 schema 与语义 validator；
- Outcome/Scope/Route digests 可重算且引用闭合；
- 所有 Outcome 与 root 连通，frontier 内不存在被选中 lane 支配的 lane；
- frontier 在上限内，超过默认 3 时存在可审查 exception；
- 每条 lane 有一个 owner、请求预算和停止条件；
- rejected/deferred 项有范围化理由；
- non-claims 全部为 false；
- 没有执行任何 lane。

若无法做到，输出 blocker 和唯一下一步，不伪造完整 plan。
