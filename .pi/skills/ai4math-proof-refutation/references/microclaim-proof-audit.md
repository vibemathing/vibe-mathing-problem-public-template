# 微命题与证明审计

## 定位

这是 `ai4math-proof-refutation` 的从属 reference，用于把证明草稿压缩为可逐项攻击、可回溯的微命题视图。它不创建平行数学真相源；微命题视图必须引用 canonical Claim/Obligation/Candidate，状态始终为 `candidate_only`。

## 输入契约

- 精确 Claim、定义域、量词、假设和结论；
- ProblemContract、Attempt/Route、ObligationGraph 和 Candidate 引用；
- 当前证明草稿、外部定理引用和已有反例/失败路线；
- 本轮只审查的有界范围。

## 微命题记录

每个非平凡推理步形成一个有界记录：

```text
microclaim_id
canonical_obligation_ref
statement
quantifiers
assumptions_used
depends_on
justification_ref
attack_cases
status: open | supported | refuted | blocked
residual_gap
```

`microclaim_id` 只用于候选审计视图；它不能替代 canonical obligation ID。

## 审计流程

1. 冻结原 Claim，禁止在审查中静默改量词、定义域或假设。
2. 将每个“显然、类似、标准”步骤拆成最小可检查蕴含。
3. 检查依赖 ID 唯一、依赖存在、无环，并能回溯到 Claim。
4. 对每个微命题执行适用的边界、退化、极端尺度、等号、量词交换、构造 witness 和最小反例攻击。
5. 区分“证明文本存在”“该步被支持”“支持覆盖该步全部范围”。
6. 子引理失败只关闭当前路线；只有反例直接满足原 Claim 的否定时，才可提出 `refuted` 候选判断。
7. 输出开放缺口和最小可复验反例；不得用风格审查替代数学检查。

## 独立性与状态

- 生成者自检可以发现缺口，但不能自称独立验证。
- 形式化 elaboration、自动求解器输出和有限枚举只覆盖冻结输入；statement faithfulness 与适用范围另审。
- 审计完成只能产出候选 proof-audit artifact；EvidenceLink、Result 和 Solution 仍由独立 verifier 与 admission owner 处理。

## Fail-closed 规则

- 未绑定 canonical obligation、依赖不闭合或状态混用时，审计结果为 `blocked`。
- 不把“没有发现错误”写成“证明正确”。
- 不把路线失败写成原命题失败。
- 不由 `/loop`、schedule 或重复同一模型自审生成新的 verdict。

## 压力场景

- 场景：长证明草稿只有一个量词交换步骤没有依据，其余步骤看似完整。
- 诱惑性错误：因整体连贯而给出“证明通过”。
- 正确行为：把该步拆成开放微命题，保留原 Claim 和路线状态，执行反例攻击。
- 通过条件：未闭合微命题阻止完成声明，且不会把路线失败误写成原 Claim 被反驳。

## 方法来源边界

本 reference 是项目原创重写，只吸收已审 `proof-checker` 候选中的微命题拆分、依赖核对和反例压力测试方法；评估输入 SHA-256 为 `49a2ddedb11747f88c416c19abde151f7591530032d976d4f8ba7d40d3083205`。

候选的精确上游身份和再分发权仍未完成独立确认；没有复制其原文、脚本或依赖。`proof-writer` 与 `formula-derivation` 的职责已被现有证明和建模 owner 覆盖，因此不再导入平行实现。
