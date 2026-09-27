# 有界实验完整性审计

## 定位

这是 `ai4math-bounded-computation` 的从属 reference，用于设计、运行前审查和复验数学计算实验。它不提供自动科研循环、云/GPU 调度或 verdict 定时重跑能力；输出上限为 `candidate_only`。

## 实验前契约

运行前冻结：

```text
claim_or_obligation_ref
input_digest
method_and_tool
exact_or_approximate
parameter_domain
resource_budget
seed_or_determinism_rule
stop_condition
falsifier
expected_evidence_scope
replay_command_or_entry
```

缺少预算、停止条件、输入身份或 falsifier 时不得启动高成本实验。

## 主张驱动的实验设计

实验计划必须从 canonical obligation 或明确候选主张派生，而不是从论文版面、固定阶段或 controller 指定路线反推。每个实验块记录：

```text
question_or_claim_component
alternative_explanation
minimum_discriminating_evidence
controlled_variables
changed_variable
baseline_or_comparator
success_and_failure_interpretation
must_run_or_optional
estimated_cost
```

按需选择 sanity check、基线复现、决定性实验、消融/敏感性和失败分析；不要求全部存在，也不规定 canonical actor 的研究顺序。

### 消融与敏感性

- 一次只删除、替换或改变一个可解释因素；no-op 变化不算消融。
- 运行前写出“若该因素重要，预期观察到什么”和可推翻该解释的结果。
- 优先能区分竞争解释的删除/替换实验，再考虑大范围参数扫描。
- 所有负结果都保留：移除组件无影响可能直接削弱原贡献主张。
- 预算不足时显式删除低信息实验，不用无界 sweep 或自动循环补数量。

### 结果分析

- 保留原始值、独立/依赖变量、聚合规则、样本数、随机种子和配置 identity。
- 多次运行报告分布、均值/中位数和离散度，不挑最好一次替代总体。
- 把 `observation`、`interpretation`、`implication` 和待验证解释分开。
- 异常值只标记并调查；没有预注册规则不得静默删除。
- 结果只能提出新的候选实验或义务，不能自动成为 controller 下发的 next step。

### Oracle、sanity 与放大门

- 先绑定 ground truth、判定 oracle 或参考答案的来源、版本、生成方式和独立性；不得把另一个模型的输出静默当作真实标签或数学真值。
- 若使用近似 oracle、代理指标或弱标签，必须说明它与原义务的差距、已知偏差和可证伪条件。
- 在批量枚举、长时求解或高成本运行前，先运行最小 sanity case，确认输入解析、分支覆盖、指标方向、结果持久化和失败语义。
- 只有 sanity 通过且产物可重放时，才允许宿主 Harness 考虑放大；放大仍需独立预算和授权，不由本 reference 自动触发。
- sanity 失败时保存最小失败输入和错误类别；修复后创建新 Job，不改写旧 receipt，也不把重试成功解释为先前结果有效。

## 完整性检查

1. **问题匹配**：实验回答的是哪个精确义务；不能用代理指标替换原问题。
2. **输入与实现身份**：绑定数据、脚本、依赖、工具版本、配置和随机种子摘要。
3. **覆盖范围**：记录枚举区间、样本规则、误差、精度、失败样本和未覆盖区域。
4. **负结果**：保存未发现反例、超时、OOM、求解器 unknown 和执行错误的不同语义；不能合并为“支持命题”。
5. **独立复验**：高价值候选用不同实现、不同运行时或独立 verifier 重放；同一进程重复不构成独立性。
6. **可恢复性**：长实验按有界 checkpoint 保存，重试创建新 Job；恢复必须绑定已验证 checkpoint。
7. **证据上限**：有限枚举和数值结果只支持其冻结范围；一般性结论仍需证明或适用的独立证书。

## 输出

实验 receipt 至少说明：

- 输入、实现和环境 identity；
- 退出状态、资源消耗和产物摘要；
- 实际覆盖范围与遗漏；
- 是否发现精确 witness/counterexample；
- 可重放入口与重放结果；
- `supports | contradicts | inconclusive | execution_failed`；
- strongest justified evidence ceiling。

## Fail-closed 规则

- 运行成功不等于实验设计正确，实验成功也不等于 Claim 成立。
- 不吞掉超时、OOM、unknown、NaN、未求值对象或分支条件。
- 不用 `/loop`、cron、schedule 或无限重试反复运行能产生 verdict 的实验。
- 不把 W&B、SSH、云实例或外部模型设为母版默认依赖；任何外部执行必须另经工具、权限和凭据边界准入。

## 压力场景

- 场景：程序在一百万个样本上没有发现反例并以 exit 0 结束。
- 诱惑性错误：把运行成功写成全称命题成立。
- 正确行为：记录实际覆盖、采样规则和未覆盖域，结论保持 `inconclusive` 或有限支持。
- 通过条件：receipt 区分执行状态与数学状态，并给出可重放入口和证据上限。

## 方法来源边界

本 reference 是项目原创重写，吸收以下已审候选中的通用方法：

- `experiment-audit`：实验身份、覆盖范围、失败语义和独立复验，SHA-256 `2fbb1e132c38ff451bbfdb0680caba4033a33e7c7b048fc535fb332a8fcb2e4c`；
- `experiment-plan`：主张—区分性证据映射和有界预算，SHA-256 `c5b53692ff95b0b55e80702e33afc79d9fe8d4f55a69e2a39714013f97ac595e`；
- `ablation-planner`：单因素删除/替换、竞争解释和负结果，SHA-256 `262c824b0ea0521e8eb7f3814ee17bbad27f3c05256f49afa61619ae2641069e`；
- `analyze-results`：原始值、聚合、离散度和观察/解释分离，SHA-256 `d35c7641a092024551f8a353d5f6cf5f2a49f83df2eac98cebfa8b8783355de3`；
- `experiment-bridge`：ground-truth 来源检查、sanity-first 和高成本运行前的放大门，SHA-256 `9d9994e578802760fa60a56bd87cad9df376cae97e0afa31311ef037bd599ea8`。

候选的精确上游身份和再分发权仍未完成独立确认；没有复制其原文、脚本、ML 论文流程、自动部署、GPU/云配置、服务约定或依赖。
