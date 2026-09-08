# Web GPT 并发结果空间完整树

本文件只定义 Web GPT 候选研究的九路分类投影。它不创建会话、Task、Job、Evidence 或 Result，也不授权并发。机器真相源是 `web-gpt-parallel-tree.v1.json`。

## 数量

- 每个 ProblemContract：固定九个分类槽 `T1..T9`。
- 每个原子 Outcome：按 `assignment_precedence` 恰好进入一个槽。
- 每槽：一个 Web GPT 研究会话/任务候选；是否实际启用由外部授权决定。
- 每槽内部子方向：在同一会话中展开，不继续自动派生并发会话。

## 完整树

```text
WebGPT-Problem
├─ T1 直接证明
│  ├─ 完整证明
│  ├─ 关键证明链
│  ├─ 等价转移证明
│  └─ 归约转移证明
├─ T2 反例与反驳
│  ├─ 最小反例
│  ├─ 有限反例
│  ├─ 参数化反例族
│  └─ 边界反例
├─ T3 等价、归约与分解
│  ├─ 等价表述
│  ├─ 单向归约
│  ├─ 已知结果转移
│  ├─ AND 子问题分解
│  └─ OR 子问题分解
├─ T4 局部定理与适用范围
│  ├─ 特殊情形定理
│  ├─ 必要条件
│  ├─ 充分条件
│  ├─ 条件性结果
│  └─ 中间命题反驳
├─ T5 结构刻画
│  ├─ 刻画
│  ├─ 分类
│  ├─ 不变量或单调量
│  ├─ 正规形
│  └─ 极小反例结构
├─ T6 定量与界
│  ├─ 上界
│  ├─ 下界
│  ├─ 精确值
│  ├─ 锐性
│  └─ 渐近或阈值
├─ T7 构造与算法
│  ├─ 显式构造
│  ├─ witness 或对象族
│  ├─ 可检查 certificate
│  ├─ 判定算法
│  └─ 生成或搜索算法
├─ T8 障碍与失败路线
│  ├─ 辅助引理失败
│  ├─ 假设不相容
│  ├─ 结构性障碍
│  ├─ 方法或工具障碍
│  └─ FailedRoute 与换路建议
└─ T9 元数学、语义修订与新类型 [最终 fallback]
   ├─ 独立性或不可判定性
   ├─ 相对一致性
   ├─ 来源或题目修正
   ├─ 定义、量词或 Scope 修正
   └─ 新 Outcome 类型审查
```

## 唯一归类顺序

每个候选先规范化为三个机器分类维度：

```text
target = root_problem | intermediate_mathematics | route
       | semantic_contract | unclassified
effect = establish | refute | advance | block
       | revise | independence | unknown
output = proof | refutation | relation | local-assertion
       | structure | quantity | construction-or-procedure
       | negative-route-knowledge | meta-semantic-or-new-type
```

按以下顺序取第一个匹配槽：

```text
T1 → T2 → T8 → T3 → T5 → T6 → T7 → T4 → T9
```

1. 能建立精确根命题：`T1`。
2. 能反驳精确根命题：`T2`。
3. 主要结果是阻断、淘汰或替换路线：`T8`。
4. 主要闭合谓词验证等价、归约、蕴含或分解：`T3`。
5. 主要闭合谓词验证刻画、分类、不变量或正规形：`T5`。
6. 主要闭合谓词验证界、精确值、锐性、渐近或阈值：`T6`。
7. 主要闭合谓词验证对象、witness、certificate 或算法：`T7`。
8. 其余可独立验证的局部命题：`T4`。
9. 独立性、一致性、语义修订或尚未分类的新结果：`T9`。

复合发现必须先拆分。例如“构造达到锐下界”拆为 `T7` 构造 Outcome 与 `T6` 锐下界 Outcome，再建立 candidate typed relation；不能同时把一个 Outcome 放入两个槽。

## Scope 覆盖

每个 `T1..T9` Outcome 另外绑定一个 Scope 值：

```text
exact | special | conditional | generalized
| strengthened | weakened | incomparable
```

Scope 是覆盖维度，不增加第十个并发槽。

## 单个 Web 搜索单元

每个槽最多形成一个任务候选，并必须绑定：

```text
lane_id + outcome_id + statement + scope + closure_predicate
+ priority_vector + exactly-one owner + requested_budget
+ stop_condition + input_refs + expected_artifact
```

九槽最多形成九个任务候选；子方向保留在对应槽内，不自动生成更多任务。分类树不授权执行。

## 命中语义

| 槽 | 命中后的候选增量 |
|---|---|
| T1–T2 | 根闭合候选 |
| T3–T7 | 可独立验证的局部数学推进 |
| T8 | 搜索空间缩减、路线阻断或换路依据 |
| T9 | 元数学候选、语义修复或重新分类触发器 |

任何命中都只形成候选增量；只有后续 owner gate 可以建立 Evidence 或 Result。
