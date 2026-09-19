# Changelog

## 0.3.0 - 2026-09-08

- 将 frontier 机器硬上限从 8 对齐为 9，使九槽 Web 分类投影能在不静默丢槽的前提下保存九个候选；默认上限仍为 3，超过 3 仍要求带引用 exception。
- Web Harness 1.4.0 将本 Skill 由物理 staging 改为 `constrained` candidate-planning-only；不创建 Task/Job/Attempt/Evidence/Result，不授权网页会话或并发，也不向既有 fleet rollout。
- 增加九任务集合和九返回合成演练契约及攻击测试。

## 0.2.0 - 2026-09-07

- 固定 `sha256-canonical-json-nfc-v1`，重算 Outcome statement/scope 与 structural route signature，拒绝任意 digest 占位和 route 改名逃逸。
- 要求 FailedRoute locator/signature 一一覆盖，并拒绝当前 frontier 重复已失败路线。
- 增加 root graph 连通、重复 typed edge、typed observation、basis reference closure 和 plan supersession 门禁。
- 对 frontier 执行内部 Pareto 支配检查；默认 limit 固定为 3，扩大到当时硬上限 8 必须有带引用 exception。
- 测试扩展为 2 个正例和 39 个攻击；没有增加 runtime、授权或数学结论权限。
- 增加 Web GPT 九路候选分类树、机器契约、target/effect/output 有限分类器、唯一归类顺序、T9 fallback 和独立攻击测试；九槽最多形成九个完整字段任务候选，但不创建会话或授权并发。

## 0.1.0 - 2026-09-07

- 建立 PLFB F04 的项目级全局 OSPS 候选规划 Skill。
- 固定七类 Outcome、scope-aware 去重、typed candidate relation、九维可解释 frontier 与多样性选择。
- 增加 candidate-only plan schema、独立校验器、有效 fixture 和越权/错绑攻击测试。
- 明确 OSPS 不调度 Job、不扩大预算、不签发 Evidence/Result、不传播 root closure，也不保存隐藏思维链。
- 记录 internal 原始定义与 AND/OR search、blackboard control、HTPS、FunSearch、BFS-Prover-V2、ProofFlow 的相邻来源；不声称任何来源直接实现或证明 OSPS。
- private central repository 完成；internal Web builder/Harness 1.3.0 仅以 `inactive` staging copy 纳入 synthetic snapshot，既有问题仓 fleet 的激活/rollout 后置。
