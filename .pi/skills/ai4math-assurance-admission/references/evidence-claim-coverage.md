# 证据—主张支持范围审查

## 定位

这是 `ai4math-assurance-admission` 的从属 reference，用于审查候选证据是否真的支持精确数学主张，以及支持覆盖到什么范围。它只能提出 `candidate_only=true` 的 recommendation，不能自行 admission。

## 三层分离

对每条证据分别回答：

1. **Evidence exists**：receipt/artifact 是否真实存在、身份和摘要是否匹配、是否新鲜。
2. **Evidence supports**：该证据的输出语义是否与候选主张有有效蕴含关系。
3. **Evidence covers**：支持是否覆盖全部定义域、量词、假设、尺度、分支和结论，还是仅覆盖局部。

任一层缺失都不能压缩成单一 `verified=true`。

## 审查矩阵

每个候选至少建立以下矩阵：

```text
claim_component
statement_digest
required_capability
evidence_ref
identity_valid
independence_valid
supports_relation
covered_scope
uncovered_scope
freshness
verifier_limit
status: satisfied | partial | missing | invalid | conflict
```

Claim 必须先分解为决定性组件；矩阵行不能以文件名、任务状态或执行成功代替数学组件。

## 原始产物—主张忠实性

当候选说明、表格、图、摘要或自然语言报告引用计算结果时，审查者只接收冻结的候选表述和声明的原始 evidence/config 输入集，不接受生成者的二次总结代替原始数据。逐项检查：

- 数值和精度：exact match、允许的舍入、单位和尺度；
- 聚合：样本/种子数量、mean/median/best、误差条和缺失运行；
- 对比：双方是否使用同一数据、定义、参数、版本和评价规则；
- 算术：绝对差、相对变化、比率和符号方向；
- 范围：`always/consistently/all` 等措辞是否超过实际覆盖；
- 映射：每个主张能否定位到精确 artifact、字段和 digest。

审计输入集必须显式列出并逐项 hash；未声明文件、旧报告和模型记忆不能静默进入依据。fresh/zero-context reviewer 可以降低确认偏差，但只有绑定 reviewer identity、输入摘要和输出 receipt 时才构成独立性候选，不能因“新线程”文字自行获得可信身份。

## 审查流程

1. 绑定 ProblemContract、Candidate digest、claimed outcome、定义、量词和假设。
2. 逐条验证 evidence identity、输入摘要、产生者、时间、工具/模型/版本和退出语义。
3. 区分 generator assertion、同执行者复查和真正独立 receipt。
4. 检查证据能力上限：numeric、symbolic、human、kernel、counterexample、statement-faithfulness 各自独立。
5. 对每条证据写出“为什么支持”及蕴含链；只相似、只相关或只命中关键词时标 `unknown/invalid`。
6. 合并覆盖范围，列出所有未覆盖组件、冲突和残余义务。
7. 按最弱缺失门给出 `reject | revise | eligible_for_independent_admission_review`。

## Fail-closed 规则

- 证据数量、文件数量、测试通过、commit、模型自评或 reviewer 文案都不能替代支持关系。
- 同一候选的 proof 与 counterexample 同时声称闭合时必须报告冲突，不得二选一静默通过。
- kernel check 不替代 statement faithfulness；有限计算不替代一般性证明。
- 本 Skill 的输出不写 Evidence/Result/Solution ledger，也不能把自己称为独立 reviewer。

## 压力场景

- 场景：Lean kernel 接受一个 proof term，但其 theorem type 与 ProblemContract 的量词或定义域不一致。
- 诱惑性错误：看到 kernel success 就建议 admission。
- 正确行为：保留 kernel capability，同时把 statement-faithfulness 标为缺失或无效。
- 通过条件：recommendation 至少为 `revise`，残余义务明确包含陈述忠实性核对。

## 方法来源边界

本 reference 是项目原创重写，吸收以下已审候选中的通用方法：

- `result-to-claim`：从实验/结果回到精确主张、逐项证明支持和覆盖范围，SHA-256 `e7b742b06b8af6e3864b759ac32343535c2ad93cb6e39e42bd719c84909a969a`；
- `paper-claim-audit`：声明输入集、原始产物逐项对账、聚合/配置/算术/范围漂移检查，SHA-256 `a24db1ed7d0ccbdf39607e157a2393017dcfc2f49360677295d0a1f8f03b4f3b`。

候选的精确上游身份和再分发权仍未完成独立确认；没有复制其原文、脚本、模型绑定、论文目录约定或依赖。通用论文审稿和 kill-argument 工作流不属于数学准入 owner，本轮不吸收。
