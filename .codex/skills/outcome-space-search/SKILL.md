---
name: outcome-space-search
description: "结果空间并行搜索（OSPS）规划。用于把一个已准入 ProblemContract 展开为版本化候选 Outcome Graph，区分 resolution/structural/scope/quantitative/constructive/negative/meta 结果族，做语义去重、关系审计、可解释 frontier 选择，并把每条 lane 交给恰好一个数学 owner skill；不调度 Job、不签发 Evidence 或 Result。"
---

# Outcome-Space Parallel Search

OSPS 是 PLFB 的 F04 结果空间执行面：维护“值得得到哪些可验证数学结果”的候选图，而不是直接执行“怎样做”的过程图。本 Skill 是项目级全局、问题实例内使用的**候选规划 owner**；它不属于用户级全局配置，也不是 OSPS runtime/orchestrator。

## When to Use This Skill

- 已有精确、`lifecycle=active` 且 digest 已冻结的 ProblemContract，但还不知道应优先攻击完整证明、反例、结构引理、特殊情形、界、构造还是障碍。
- 当前路线卡住，需要从已登记 FailedRoute、Observation 或新文献中生成不同的 OutcomeNode，而不是重复同一路线。
- 多个候选目标看似相近，需要按 statement、scope、量词、假设和 closure predicate 去重或建立候选关系。
- 需要在固定总预算内选择少量、方法多样、可独立验证的 frontier lanes，并分别交给 discovery、derivation、computation、proof、formalization、solve 或 math-toolchain。
- 新 Candidate/Result/Obstruction 到来后，需要重算候选 frontier，但尚未建立正式 Outcome Graph owner/runtime。

## Not For / Boundaries

- 没有 active ProblemContract、statement digest 或明确 acceptance predicate 时，停止并路由到 `math-discovery`；不从题目标题、仓库名或聊天猜测根命题。
- 本 Skill 只产出 `candidate-planning-only` 的 OSPS plan，不创建正式 OutcomeGraph、Task、Job、Attempt、EvidenceLink、Result 或 Solution。
- OSPS 选择“攻击什么”；PWTSJ/F05 与 Harness 决定“是否获授权、何时、由哪个有界 Job 执行”。本 Skill 不能启动 worker、并行进程、网络请求、solver、GPU 或 proof assistant。
- `branches_to` 可以由规划决定提出；`implies`、`equivalent_to`、`refutes`、`strengthens` 等逻辑关系在本 Skill 中只能是 candidate relation，不能冒充 admitted Line。
- 不把相同标题、相同仓库、文本相似度、共同样例或模型高分当作语义等价。
- 不把 Job/CI/PR/checkpoint 成功、有限枚举、自然语言证明草稿或模型自评传播为 Outcome closed 或根问题 solved。
- 不保存或要求隐藏思维链。只记录输入引用、候选 statement/scope、可观察依据、优先级维度、选择决定、停止条件和开放缺口。
- “并行”表示 frontier 中可独立攻击的 `OutcomeNode × Route × Method` lanes；不等于自动获得并发、预算或执行授权。

## Quick Reference

```text
Preflight
  active ProblemContract + exact digest + acceptance predicate
  + current failed routes / obligations / evidence state

Normalize root
  exact statement + domain + quantifiers + assumptions + allowed axioms
  + local closure predicate

Expand candidate outcomes
  resolution | structural | scope | quantitative
  | constructive | negative_knowledge | meta

Audit graph
  exact identity -> scope-aware dedup -> typed candidate relations
  -> dangling/self-edge rejection -> no automatic root propagation

Select frontier
  hard gates: semantic clarity + feasible closure predicate
  -> Pareto comparison of explicit dimensions
  -> diversity across outcome/route/method
  -> bounded lanes with stop conditions and requested budgets

Handoff
  each lane -> exactly one execution owner skill
  requested budget != authorization
  candidate plan != Outcome runtime / Evidence / Result
```

### Required inputs

1. Problem ID, contract version and canonical statement digest.
2. Exact root statement, scope and acceptance predicate.
3. Current obligation/failed-route references and every FailedRoute 的结构化 route signature，或显式确认集合为空。
4. Existing candidate/evidence/result references relevant to reprioritization, with current validity status.
5. Frontier-size and resource request bounds; if absent, default to at most three lanes and request no execution.

### Outcome construction rules

Every proposed node must have a distinct, reviewable `statement`, `scope`, `statement_digest`, `scope_digest`, `closure_predicate`, `value_if_closed` and family. Digests must use `sha256-canonical-json-nfc-v1`; validator 会重算 statement/scope digest，不能填任意 64 位占位值。A direction note such as “try spectral methods” is a Route/Method proposal, not an OutcomeNode.

For Web GPT candidate classification, use the separately validated nine-slot projection in `references/web-gpt-parallel-tree.md`: `T1` direct proof, `T2` root refutation, `T3` relation/reduction, `T4` local theorem/scope, `T5` structure, `T6` quantity, `T7` construction/algorithm, `T8` obstruction/FailedRoute, and `T9` meta/semantic/new-type fallback. Apply its ordered first-match rule so one atomic Outcome enters exactly one slot; split compound findings before classification. The nine slots are a coverage projection only and do not authorize nine concurrent sessions.

Use the seven legacy families as derived routing aids, not as mathematical semantics:

- `resolution`: faithful complete proof, complete counterexample, or fully checked resolving equivalence/reduction;
- `structural`: characterization, classification, invariant, necessary/sufficient condition, obstruction, normal form;
- `scope`: special, strengthened, weakened, bounded or conditional statement;
- `quantitative`: upper/lower bound, threshold, asymptotic or sharpness statement;
- `constructive`: witness, family, algorithm, reduction or checkable certificate;
- `negative_knowledge`: failed route, method barrier, incompatible assumptions or intermediate refutation;
- `meta`: corrected statement, missing source/definition, new obligation or graph revision.

### Frontier policy

Use `pareto-then-diversity`; do not compute one opaque “confidence” or “truth probability”. For every lane record integer values `0..4` and a matching basis entry for:

```text
root_relevance
mathematical_value
semantic_clarity
verification_feasibility
information_gain
route_novelty
reuse_value
estimated_cost        # 0 low, 4 high
epistemic_risk        # 0 low, 4 high
```

Reject a lane if its statement or closure predicate is not independently reviewable. 每条 lane 必须提供由 Outcome semantic digests、owner、artifact type、method family、representation、关键假设和工具能力指针计算的 `route_signature`；改 route 名称不能绕过 FailedRoute 去重。Among remaining lanes, retain non-dominated choices, then prefer diversity of outcome family, route and owner method. Validator 会拒绝 frontier 内被另一 lane Pareto 支配的选择。High cost/risk cannot be hidden by a scalar total. A frontier may contain one lane when no second lane is genuinely distinct；`frontier_limit > 3` 必须提供带引用的 exception，且始终不得超过 9。九槽 Web 分类投影可以保留九个候选，但这仍不授权创建任务、会话或并发执行。

### Output contract

Write a candidate plan conforming to `references/osps-plan.schema.json`, then run when command execution is permitted:

```bash
python3 .codex/skills/outcome-space-search/scripts/validate_osps_plan.py \
  --file research/artifacts/candidates/<candidate-id>/osps-plan.json
```

In a Web problem repository, the plan may only be written under an already allowed candidate/source-note path. The Skill directory, governance, schemas, workflows, ledgers and default branch remain read-only to the research principal.

The final response must summarize:

```text
Problem binding
Outcome inventory by family
Candidate relation audit
Dedup/split/merge decisions
Selected frontier lanes and explicit basis
Rejected/deferred lanes and blockers
Exactly one owner skill per lane
Requested budget + stop condition (not authorization)
Non-claims: no runtime, Evidence, Result, root closure or hidden reasoning
```

## Examples

### Example 1：全称猜想的有限计算路线

- 输入：active 全称 ProblemContract；已有小规模枚举支持；尚无一般证明。
- 动作：建立 root resolution node、有限范围 scope node、结构性 obstruction node；有限范围节点用 `specializes` 候选线指向根，禁止向根自动传播。
- 验收：计算 lane 可交给 `math-computation`，但 root 保持未闭合；plan 的全部 non-claim 标志为 false。

### Example 2：证明路线中的辅助引理被反驳

- 输入：一个中间引理反例和对应 FailedRoute。
- 动作：新增 negative-knowledge node，将当前 route 标为 blocked；检查反例是否直接满足根命题否定。若不满足，提出新的 structural/scope outcomes 并降低重复路线优先级。
- 验收：只反驳中间路线，不把根命题标记 refuted；FailedRoute 历史被引用而非删除。

### Example 3：两个“等价”表述只有文本相似

- 输入：两个名称相似但量词或假设不同的候选 OutcomeNode。
- 动作：分别冻结 scope digest；若双向蕴含没有已准入依据，只保留两个节点和 `candidate` 关系或不建线。
- 验收：没有 `admitted equivalent_to`，也不因同仓库或相似标题 merge。

### Example 4：三条方法路线竞争固定预算

- 输入：同一 structural outcome 可由组合、SAT 搜索和 Lean 形式化攻击，总预算只允许两个小步。
- 动作：按九维 basis 做 Pareto 比较，再按方法多样性选两条 lane；每条 lane 绑定一个 owner、requested budget 和 stop condition。
- 验收：未选 lane 记录 deferred basis；OSPS 不创建 Job，也不把预算请求当授权。

### Example 5：缺少 active ProblemContract

- 输入：一个公开仓库标题和未审来源摘要。
- 动作：停止 OSPS，路由到 `math-discovery` 完成来源、陈述和 ProblemContract 准入。
- 验收：不生成 osps-plan，不创建 Attempt，不开始并行搜索。

## References

- `references/index.md`：Skill 阅读顺序和本地文件入口。
- `references/method.md`：完整 OSPS 候选规划算法、状态和跨面接口。
- `references/output-contract.md`：候选 plan 字段、消费者和非真相边界。
- `references/osps-plan.schema.json`：仅限候选规划的 JSON Schema，不是正式 Outcome Graph schema。
- `references/source-map.md`：internal 原始定义与外部相邻方法的一手来源映射。
- `references/pressure-tests.md`：错误传播、伪等价、重复路线、隐藏打分和越权执行攻击场景。
- `references/web-gpt-parallel-tree.md`：Web GPT 九路分类完整树和唯一归类顺序。
- `references/web-gpt-parallel-tree.v1.json`：九路分类机器真相源；对应 schema 和 validator 位于同一 Skill 内。
- `references/web-gpt-task-set.schema.json` 与 `references/web-gpt-synthetic-response-set.schema.json`：九槽任务候选和 shape-only 合成返回合同。
- `references/optimization-notes.md`：0.2.0 加固基线、仍未机械解决的局限与下一轮优化入口。

## Maintenance

- Owner：F04 / `outcome-space-search` candidate-planning owner。
- Sources：internal PLFB/OSPS 原始定义；`proofflow`、`bfs-prover-v2` 等固定来源只作相邻实现证据；AND/OR search、blackboard control、HTPS 与 FunSearch 一手文献只作方法参照。
- Version：`0.3.0`。
- Last updated：2026-09-08。
- Verification：`python3 scripts/validate_project.py`、`python3 scripts/test_outcome_space_search_skill.py`、`python3 scripts/test_web_gpt_task_set.py`；当前含 2 个 OSPS 正例、39 个 OSPS 攻击及九槽合成演练攻击；数学关系和 Result 仍需各自 owner gate。
- Distribution status：private central Skill 0.3.0 complete；internal Web builder/Harness 1.4.0 将它标为 `constrained` candidate-planning-only，但尚未向既有问题仓 fleet rollout，也未声明正式 OSPS schema/runtime/orchestrator 已实现。
