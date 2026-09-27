# 问题锚定与最小路线审计

## 定位

这是 `ai4math-modeling-derivation` 的从属 reference，用于在建模或推导前固定问题身份、比较候选表示，并防止研究过程悄然改成更容易但不同的问题。它只提供 `candidate_only` 的审计框架；canonical research actor 自主决定是否使用、选择哪条路线以及何时换路。

## Problem Anchor

开始非平凡建模前，从已冻结的 ProblemContract 派生最小锚点：

```text
problem_ref
statement_digest
bottom_line_question
must_preserve_domain_and_quantifiers
must_solve_bottleneck
non_goals
hard_constraints
success_condition
```

锚点只能引用 canonical statement 和已确认约束，不能用研究者偏好的方法、预期答案或当前路线替代原问题。若 ProblemContract 信息不足，留下 open obligation，不自行补写业务或数学条件。

## 最小充分机制

提出新对象、假设、模块或中间结构前依次检查：

1. 是否能删除、内联或复用既有定义、定理、表示或工具；
2. 新机制是否直接作用于已识别 bottleneck；
3. 是否存在更弱假设、更少结构或更短 transfer chain 也能回答同一问题；
4. 新增复杂度是否带来可观察的区分能力、证明义务闭合或反例能力；
5. 去掉该机制后，哪条精确主张会失去支持。

无法回答第 2、4、5 项时，把它标为 `unsupported_addition`，不要继续堆叠抽象。

## 候选路线比较

只有 canonical actor 主动需要比较时，才建立小型候选集；这不是 controller 的 route portfolio，也不规定顺序。每个候选只记录：

```text
route_or_representation
problem_anchor_match
new_objects_and_assumptions
preserved_invariants
transfer_obligations
fast_falsifier
required_capabilities
estimated_cost
known_failure_mode
```

比较规则：

- 先排除改变定义域、量词、结论强度或依赖未授权资源的候选；
- 相同目标下，优先 transfer obligations 更少、可证伪性更强、复用更多的候选；
- “新”“现代”“复杂”不是数学优势；只有更清楚的蕴含链或更强的区分能力才算收益；
- 候选的机械去重只按核心假设与变换关系进行，不以同一执行者的主观质量判断提前删除；
- 保留被否定路线的精确 blocker，避免把路线失败误写成根命题被反驳。

## 漂移检查

每次重要改写后对照 Problem Anchor：

- 对象、定义域、量词和假设是否不变；
- 当前 bottleneck 是否仍是原 bottleneck；
- success condition 是否仍能回答原问题；
- 新表示是否有回到原陈述的 transfer map；
- reviewer 或工具建议是否只是让代理任务更容易。

若发生漂移，状态必须为 `drifted_candidate` 或 `reframe_requires_new_statement`。不得用更好的分数、更多实验或更漂亮的模型掩盖目标改变。

## 最小 pilot

当候选路线可通过低成本检查区分时，先设计最小 falsifier 或 sanity check：冻结输入、预期观察、失败解释、预算和证据上限。pilot 只能帮助 actor 判断路线是否值得继续，不能产生 Evidence、Result、admission 或根问题闭合。

## 输出

```text
problem_anchor
candidate_route_records
selected_or_deferred_by_actor
complexity_budget
removed_or_reused_elements
open_transfer_obligations
fast_falsifiers
route_blockers
anchor_status: preserved | drifted_candidate | insufficient_contract
```

## Fail-closed 规则

- 不把固定路线数量、评分表、阶段或模型评语变成强制研究流程。
- 不允许 controller 用本 reference 指定 next lemma、路线优先级或工具顺序。
- 同一模型的生成与自评可以形成候选意见，但不能冒充独立 verdict。
- 计算预算、论文潜力、流行技术或实现便利不能覆盖 statement identity。
- 本 reference 不创建 Attempt、Evidence、Result、Solution 或 admission 记录；写回仍由对应 owner ledger 和独立门禁处理。

## 压力场景

- 场景：一个新表示能快速得到漂亮结论，但只覆盖原问题的有限子类。
- 诱惑性错误：把子类结果写成原问题已解决，或继续叠加模块扩大表面能力。
- 正确行为：保留有限子类候选，标出 transfer gap，并重新比较是否存在直接作用于原 bottleneck 的更小机制。
- 通过条件：Problem Anchor 未改写，候选明确标记覆盖范围，根问题保持 open。

## 方法来源边界

本 reference 是项目原创重写，只吸收以下已审候选中的通用模式：

- `idea-creator`：多视角候选生成、机械去重、便宜 falsifier 和失败记忆，SHA-256 `421777d4ceb35641d0789004fdc9ca61609e21def4417332869b53a4fc8ceee3`；
- `idea-evaluator`：先检查致命约束、能力/资源匹配和可修复风险，SHA-256 `718426dc2d9527e8728b030e667f42379197bcbf693c81c6d38b3a4e8317f385`；
- `research-refine`：Problem Anchor、最小充分机制、复杂度预算和漂移检查，SHA-256 `410bb34a9cd796fa8c9b834627a92cfacc768a31af0152a32f856de87f2879b8`。

候选的精确上游身份和再分发权未完成独立确认；没有复制其原文、评分体系、固定模型、自动复审循环、论文流程、GPU 工作流或目录约定。它们面向 ML 论文选题的价值代理没有进入数学真相或准入流程。
