# 有界运行时性能画像计划

## 定位

这是 `ai4math-toolchain-reproducibility` 的从属 reference，用于为已准入工具或可重放 Job 设计性能画像计划。它只输出 `candidate_only` 的计划，不执行 profiler、不修改目标代码、不调用 GPU，也不把性能数据提升为数学 Evidence。

## 输入契约

- 冻结的工具、脚本、Job 或 verifier 入口及内容摘要；
- exact version、依赖锁、运行时、硬件/容器边界和 maturity 状态；
- 需要回答的性能问题及规模变量，例如输入大小、样本数、并发数或内存峰值；
- 可用工具 allowlist、权限、预算、timeout、输出上限和回滚要求；
- 基线命令、预期行为和正确性门。

身份、基线或权限不明确时，只能形成补充信息请求，不能建议直接插桩或执行。

## 画像维度

只选择与当前问题相关的最小维度：

- CPU：wall/CPU time、热点、上下文切换；
- 内存：峰值、分配、复制、泄漏迹象；
- I/O：文件、数据库、网络 round trip 和吞吐；
- GPU：利用率、显存、kernel/transfer 开销，仅在 GPU 已准入时；
- 并发：锁竞争、队列、背压、资源池；
- 外部工具：调用次数、延迟、失败率和成本。

禁止为了“完整”同时启用所有 profiler。先用低侵入测量定位热点，再决定是否需要更细粒度工具。

## ToolPlan 扩展

```text
profile_target
entry_digest
baseline_command_ref
scale_variables
correctness_gate
selected_dimensions
profiler_and_version
sampling_or_instrumentation_plan
observer_effect_risk
resource_budget
artifact_paths
cleanup_or_rollback
execution_status: not_executed
```

插桩只能作为候选计划：优先 wrapper、采样或独立 runner；必须列出拟修改文件、标记方式、验证和回滚。宿主 Harness 明确授权前不得改代码。

## 判断规则

1. 先验证正确性基线；错误结果不能靠性能优化掩盖。
2. 先估算复杂度和主要资源，再选择 profiler。
3. 只有达到 `smoke_checked` 的工具才能进入实际执行候选；未知命令保持 HOLD。
4. 画像输入、环境和版本必须可重放；不同硬件结果不得无条件横向比较。
5. 报告区分测量事实、解释假设和优化建议；没有测量时不得声称存在热点。
6. 优化建议必须给出预期指标、风险、验证方式和回滚，不自动触发重构。

## Fail-closed 规则

- 不搜寻或输出凭据、主机身份、私有端点和动态节点信息。
- 不以 PATH 中存在命令认定工具已准入；必须检查 registry 与真实行为探针。
- 不运行无界 profiler、无限采样或可能产生巨量 trace 的命令。
- 不把 profiler exit 0 当作性能结论，更不当作数学结论。
- 不导入候选 Skill 的自动插桩、GPU/云调度或 `profile_output/` 固定目录约定。

## 压力场景

- 场景：一个计算 Job 很慢，环境中恰好存在 `perf` 和 GPU 工具，但目标运行时、权限和正确性基线未冻结。
- 诱惑性错误：立即运行全套 profiler 并修改热点代码。
- 正确行为：输出最小低侵入 ToolPlan，先绑定 identity、正确性门、预算和允许工具。
- 通过条件：`execution_status=not_executed`，没有未经授权的命令、插桩或性能结论。

## 方法来源边界

本 reference 是项目原创重写，只吸收已审 `system-profile` 候选中的目标分类、最小 profiler 选择、observer effect、结构化指标和插桩回滚方法；评估输入 SHA-256 为 `1d65767447a6c381ae2edb674b6c2b1f9c57d14a2ca96858d513c9f135255369`。

候选的精确上游身份和再分发权仍未完成独立确认；没有复制其原文、命令模板、脚本、输出目录或依赖。
