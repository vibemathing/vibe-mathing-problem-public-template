# Source Map

## 1. VibeMath 原始定义（规范性来源）

以下 internal 文件定义本项目中 OSPS 的含义，优先级高于外部类比：

- `governance/strategy/VIBEMATH_POINT_LINE_FACE_BODY_METAMODEL_v0.1.md`：PLFB 是唯一概念根；OSPS 是 F04，PWTSJ 是 F05。
- `governance/strategy/OSPS_DYNAMIC_OUTCOME_GRAPH_MODEL_v0.1.md`：OutcomeNode 字段、七类结果、状态、typed relations、动态更新、frontier、并行、根传播和 PWTSJ 接口。
- `governance/strategy/PLFB_FACE_CONTRACTS_v0.1.md`：F04 owner/input/output/gate/跨面边界。
- `governance/strategy/PLFB_LINE_TYPE_CATALOG_v0.1.md`：逻辑线、搜索线、证据线及 candidate/admitted 状态分离。
- `governance/strategy/PLFB_CROSS_FACE_BINDING_AND_BODY_CONTRACT_v0.1.md`：Outcome↔Task↔Obligation↔Evidence 的 reference-only binding 和禁止状态传播。

本 Skill 是上述定义的候选规划适配，不是另一个元模型根，也不把 v0.1 概念文档冒充 runtime。

## 2. 外部一手文献：相邻机制

### 2.1 AND/OR 图与启发式搜索

- C. L. Chang and J. R. Slagle, “An admissible and optimal algorithm for searching AND/OR graphs,” *Artificial Intelligence* 2(2), 117–128 (1971), DOI [10.1016/0004-3702(71)90006-3](https://doi.org/10.1016/0004-3702(71)90006-3).
- 采用的相邻认识：解目标可由“任选一个分支”的 OR 结构与“必须共同满足”的 AND 结构组成；frontier expansion 与启发式选择需要显式语义。
- 未采用：不声称 OSPS 使用 AO*、满足 admissible cost heuristic 或具有最优/完备保证。Outcome Graph 允许逻辑关系、版本和失效，不能压成单一最小成本 solution graph。

### 2.2 Blackboard 与机会式控制

- Lee D. Erman, Frederick Hayes-Roth, Victor R. Lesser and D. Raj Reddy, “The Hearsay-II Speech-Understanding System: Integrating Knowledge to Resolve Uncertainty,” *ACM Computing Surveys* 12(2), 213–253 (1980), DOI [10.1145/356810.356816](https://doi.org/10.1145/356810.356816).
- Barbara Hayes-Roth, “A blackboard architecture for control,” *Artificial Intelligence* 26(3), 251–321 (1985), DOI [10.1016/0004-3702(85)90063-3](https://doi.org/10.1016/0004-3702(85)90063-3).
- 采用的相邻认识：多个专门知识源可围绕共享、可观察的候选状态工作；问题求解与“下一步选什么”的控制知识应分开；机会式更新优于强制单一自顶向下顺序。
- 未采用：不建立一个可被任意 agent 写入的万能 blackboard；OSPS plan 不复制 Problem/Evidence/Result owner truth，也不授予执行权限。

### 2.3 Proof hypergraph search

- Guillaume Lample, Timothée Lacroix, Marie-Anne Lachaux, Aurélien Rodriguez, Amaury Hayat, Thibaut Lavril, Gabriel Ebner and Xavier Martinet, “HyperTree Proof Search for Neural Theorem Proving,” *NeurIPS 35*, 26337–26349 (2022), DOI [10.52202/068431-1910](https://doi.org/10.52202/068431-1910); [official abstract](https://papers.neurips.cc/paper_files/paper/2022/hash/a8901c5e85fb8e1823bbf0f755053672-Abstract-Conference.html).
- 采用的相邻认识：证明动作可能生成多个必须共同解决的子目标，因此树之外的超图/共享子目标结构对 proof search 有价值；在线反馈可改变后续 search priority。
- 未采用：论文报告的 Metamath/Lean benchmark 是特定系统实证，不推出 OSPS 对开放数学问题有效、完备或可终止；本 Skill 不训练模型或运行 proof search。

### 2.4 Generator–evaluator 与多样性池

- Bernardino Romera-Paredes et al., “Mathematical discoveries from program search with large language models,” *Nature* 625, 468–475, DOI [10.1038/s41586-023-06924-6](https://doi.org/10.1038/s41586-023-06924-6).
- 采用的相邻认识：当候选具有高质量、可执行 evaluator 时，生成器和 evaluator 分离、候选池、多样性 islands、best-shot feedback 与异步扩展可以有效组织搜索。
- 未采用：OSPS 面向的不只是不难评价的程序搜索问题；没有明确 closure/evaluator 的开放命题不能套用 FunSearch 结论；evaluator score 不等于数学 Evidence 或 Result。

## 3. 固定上游源码：实现邻居（非 active runtime）

- `bfs-prover-v2`：固定 commit `ada0f976e95b09e0b9efa8f171fdf4b09e161ba0`，Apache-2.0，reference-only。其 README 描述 planner 分解子目标、共享 subgoal cache、多 prover 并行 best-first search 和失败后动态重规划。只吸收“共享子目标 + 多样化搜索 + 重规划”的相邻形状，不复制模型、安装器或 benchmark 能力声明。
- `proofflow`：固定 commit `97f1b7be82380733fb0380973c164e40645ae9da`，MIT。其 README/源码把自然语言证明分解为 dependency graph，再做 lemma formalization/tactic completion。只吸收“显式依赖图与局部义务”的结构；已有审计发现未知依赖与 cycle 处理边界，因此不执行其调度器。
- `formal-conjectures`：固定 commit `858d0e73105101fbc9f86c6d6dd86bbc6d4d789e`，Apache-2.0，reference-only。只说明候选命题语料需要身份、来源和准入隔离，不把 dataset 条目当 active ProblemContract。
- `local-auto-research-archive`：隔离、非 active 的方法库存。只用于供应链对照，不把其中自动循环、并行控制或模型自评搬入本 Skill。

以上 ID 均由 `vendor/sources.lock.json` 固定。下载或 source-lock 不等于安装、激活、evidence capability 或 verifier admission。

## 4. 综合关系与原创性边界

OSPS 的具体组合——PLFB F04 定位、七类 Outcome、scope-aware identity、candidate/admitted typed lines、九维显式 priority、Pareto+diversity frontier、PWTSJ/F05 授权分离、F09/F10 根传播门——来自 VibeMath internal 设计。

外部来源分别提供 AND/OR、共享 blackboard、机会式控制、proof hypergraph、generator–evaluator、多样性池与并行 proof search 的相邻先例。它们证明这些部件有研究谱系，但不证明该组合新颖、正确、有效或已实现。本文档不作专利、新颖性或优先权声明。

未保存论文全文、模型权重、运行日志或上游工作树；这里只保存书目信息、固定 source identity、有限方法映射和边界判断。
