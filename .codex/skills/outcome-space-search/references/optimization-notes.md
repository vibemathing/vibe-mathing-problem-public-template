# OSPS Skill Optimization Notes

## 0.3.0 infrastructure alignment

九槽 Web 分类投影要求能保存九个候选，因此机器硬上限由 8 对齐为 9；默认仍为 3，超过 3 仍必须有带引用 exception。新增九任务/九返回合成合同和攻击测试，不增加任何执行或数学状态权限。

## 0.2.0 review target

第一轮优化不扩大 OSPS 权限，只减少“形式上通过但无法审计”的候选计划。

## 已加固

| 缺口 | 0.2.0 处理 |
| --- | --- |
| 任意 64 位字符串可冒充 semantic digest | 固定 `sha256-canonical-json-nfc-v1` 并重算 statement/scope |
| 改 route ID 可伪装新路线 | 用 Outcome digests、owner、artifact type、method family、representation、关键假设和工具能力计算 structural route signature |
| FailedRoute 只有 locator、不能机械对照 | `failed_route_refs` 与 `failed_route_signatures` 必须一一覆盖，frontier 不得命中旧 signature |
| Outcome 可孤立于根图 | 所有节点必须在忽略方向的 candidate relation 投影中连接 root |
| 重复 typed relation 可重复计数 | 拒绝相同 `line_type/source/target` |
| 声称 Pareto 但不检查 | 拒绝 frontier 内被另一选中 lane 严格支配的 lane |
| 当时 schema 上限 8 被误当默认 | 固定默认 3；扩大必须给出带已绑定引用的 exception；0.3.0 仅把机器硬上限对齐为 9 |
| basis 可引用不存在对象 | Outcome/relation/priority/exception basis refs 必须在 plan 输入或本地图对象中闭合 |
| Observation 可错挂输入类型 | source/evidence/result/failed-route 等 observation 必须引用对应 typed input set |
| supersession 语义松散 | version 1 禁止 supersedes；version > 1 必须绑定旧 plan |

## 仍未机械解决

1. **候选全集不可见**：当前 plan 只保存 selected frontier 和粗粒度 deferred 项，因此 validator 只能证明 frontier 内无支配项，不能证明所有未选 lane 都被正确比较。
2. **数学关系真实性**：连通性只排除孤立节点；`implies/equivalent_to/refutes` 仍是 candidate relation，validator 不证明其方向或逻辑有效性。
3. **语义改写规避 route signature**：structural fields 提高改名成本，但恶意更改 method family/representation 仍需人工语义审查。
4. **Acceptance 内容不可本地重算**：plan 绑定 acceptance pointer + digest，但 owner policy 内容不复制进 candidate artifact；freshness 由调用方读取 owner truth 后确认。
5. **跨版本 Evidence 适用性**：v0.2 只做 typed reference closure；正式 EvidenceLink 的 statement/scope/assumption/verifier applicability 仍由 F09 owner gate 判断。
6. **Pareto 后 diversity 不是确定性最优器**：本 Skill 要求公开 basis，不声明唯一最优选择、完备性或收敛。

## 下一轮优先候选

按收益/风险排序：

1. 引入 `evaluated_lanes[]` 与派生 `frontier_lane_ids[]`，让 validator 对候选全集计算 Pareto set，并记录每条 deferred lane 的向量和支配 witness；
2. 增加 reference-only input snapshot，绑定 owner locator、object digest、observed validity 和 observed-at，阻断 stale Evidence/Result 复用；
3. 将 route signature 与 append-only FailedRoute ledger 建立只读 adapter，而不是依赖调用者手工抄录；
4. 增加 relation-specific 端点/family 约束和可选 proof obligation pointer，但仍保持 relation candidate-only；
5. 在任何 fleet rollout 前继续扩展 wrong-Problem、old-digest、protected-path、Job creation 和 Evidence reuse 的端到端 fixture；0.3.0 已完成合成九槽绑定与状态升级攻击。

上述候选都不得创建 Outcome runtime、PWTSJ Job、EvidenceLink 或 Result。
