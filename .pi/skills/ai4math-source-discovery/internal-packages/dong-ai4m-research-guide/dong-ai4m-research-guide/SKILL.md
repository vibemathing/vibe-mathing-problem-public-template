---
name: dong-ai4m-research-guide
description: "规划 AI4M 学习科研：分诊导航、验证、洞察，选择专用工具、Lean/自动形式化、Agent/Evolve 路线。"
---
<!-- argument-hint: [目标、研究问题、路线选择、工具名或章节号] -->

# AI for Mathematics 从入门到前沿的学习指南
**作者**：董彬（北京大学） | **来源日期**：2025-09-28 | **页数**：3 | **内容单元**：3 | **生成**：2026-09-12

## How to Use This Skill
- 给目标/问题：先定位能力，再选路线。
- 给工具/路线：读取相应章节，返回前提、流程、失败信号、验证。
- `ch01` / `ch02` / `ch03`：读取指定章节。
- 术语、方法、快速决策：读取 `glossary.md`、`patterns.md`、`cheatsheet.md`。
- Core 未覆盖细节时，回答前读取相关章节。

## Core Frameworks & Mental Models

### AI4M 三能力
先标记主能力与辅助能力：
- **知识导航**：找相似结论、学新理论、掌握工具。
- **证明与验证**：构造证明、检验反例、严格验证、获得反馈。
- **洞察与连接**：从理论、证明、数据中找模式、联系与猜想。

### 兴趣—路线匹配
- 数学兴趣更强 → 优先评估**专用工具**；重点是找可数据驱动的数学环节，并做数学解释。
- 算法/编程兴趣更强 → 优先评估**通用模型、形式化推理、Agent**。
- 共同前提 → AI/编程与 ML、DL、RL、LLM 基础；Agent/PE 也重要。

### 三条操作链
- **专用工具**：可推动环节 → 数据 → 模型/训练 → 稳定特征 → 数学解释 → 猜想/验证。只有性能、没有解释时，输出只能作为线索。
- **形式化**：自然语言数学 → 形式表达 → Lean/mathlib → 检索/自动形式化 → 形式验证 → 训练或推理反馈。卡住时区分库检索、自动形式化、证明搜索、局部补全。
- **Agent / Evolve**：强基座、多步任务、工具与反馈齐全时评估 Agent；目标明确可量化、评价可信且已有初始化时评估 Evolve。

### 理解优先
最终评价点是系统是否增加人对数学结构的理解与洞察。机械、可验证的证明工作可更多交给 AI，人类注意力投入概念、联系、猜想与解释；严格验证仍保留。

## Routing Policy
1. 快速学懂/找理论 → ch01；涉及 Lean 检索再读 ch02。
2. 严格验证/形式证明/训练证明模型 → ch02 形式化链。
3. 从数据找猜想/模式 → ch02 专用工具闭环。
4. 多步求解 + 强基座 + 可验证反馈 → ch02 Agent-first。
5. 优化已有方案 + 可量化目标 + 初始化 → ch02 Evolve。
6. 证明指标与数学理解失衡 → ch03。

## Failure Recovery
- 前提不足：重查目标、兴趣、数据、形式化可行性、反馈信号并换路。
- 专用工具无数学解释：降级为线索，重做数据/表征或缩题。
- Lean 过慢：定位检索/形式化/搜索/补全层级再处理。
- Agent 不收敛：检查工具、验证器、反馈、终止条件。
- Evolve 指标失真：先重写评价函数。
- 信息不足：返回“当前不足以判断”，列出缺少条件。

## SELF_CHECK
- 目标属于哪项核心能力？
- 路线与兴趣、能力匹配吗？
- 数据/形式化/工具/验证器前提齐吗？
- 是否把模型线索误当数学结论？
- 是否写明失败与换路条件？
- 结果有数学解释或可验证反馈吗？
- 最终是否增加数学理解？

## Chapter Index
| # | Title | Key Frameworks |
|---|---|---|
| [ch01](chapters/ch01-orientation-and-foundations.md) | 绪论：三能力与基础准备 | 三能力、兴趣定位 |
| [ch02](chapters/ch02-research-routes-and-formalization.md) | AI4M 具体学习科研指南 | 专用工具、Lean、自动形式化、Agent、Evolve |
| [ch03](chapters/ch03-understanding-first-math-research.md) | 写在后面的话 | 理解优先、人机分工 |

## Topic Index
- **Agent / Evolve / AI Scientist** → ch02
- **autoformalization / Lean / mathlib / LeanSearch** → ch02
- **Prompt Engineering** → ch01
- **专用工具 / 通用模型 / 数学数字化** → ch02
- **知识导航 / 证明与验证 / 洞察与连接** → ch01, ch03
- **理解优先** → ch03

## Supporting Files
- [glossary.md](glossary.md) — 术语与系统名
- [patterns.md](patterns.md) — 方法、失败恢复与验证
- [cheatsheet.md](cheatsheet.md) — 决策表与自检

## Scope & Limits
只编码该 3 页指南。适用于 AI4M 学习/科研路线、形式化、数据驱动发现、Agent/Evolve 与 AI4M 评价；不用于普通数学知识讲解、一般编程或与 AI4M 无关的任务。文中“今年/近期”与项目状态以 2025-09-28 为语境；用户要求最新进展时另行检索并区分来源内容与外部更新。
