# Chapter 2: AI4M 具体学习科研指南——专用工具、形式化、Agent 与 Evolve

## Core Idea
作者把 AI4M 研究分成两种主模式：专用工具从数据中提取数学特征并启发猜想；通用模型系统解决一类数学任务，并借助形式化数学获得严格反馈。强基座模型推动 Agent 路线；目标可量化且有初始化时，可用 Evolve 类系统持续改进方案。

## Frameworks Introduced
- **专用工具闭环**
  - When：数学问题存在可数据化环节，目标是找结构/猜想。
  - How：识别环节 → 生成数据 → 选模型/训练 → 找稳定特征 → 数学解释 → 猜想/验证。
  - Failure：只有预测效果，无法给出数学意义；应重做表征、缩题或加强领域解释。
- **数学数字化与形式反馈**
  - When：需要严格验证、系统化推理训练或自动证明。
  - How：自然语言数学 → 形式表达 → Lean/mathlib → 检索/自动形式化 → 形式验证 → 把反馈用于训练、搜索、推理。
- **形式化瓶颈路由**
  - 库里找不到引理 → 语义检索；自然语言难转 Lean → 自动形式化；证明搜索失败 → prover；局部证明缺口 → tactic。
- **Agent-first**
  - When：基座模型强、任务多步、存在工具与可检查反馈。
  - Failure：没有可靠反馈时，多步循环会放大错误。
- **Evolve**
  - When：目标明确、可量化、评价函数可信、已有可用初始化。
  - Failure：评价指标与真正数学价值错位时，先修目标函数。

## Key Concepts
- **专用工具**：针对具体数学问题构建的数据驱动工具；作者以 Williamson/DeepMind 及受其启发的 ADLV 研究作代表。
- **通用模型**：系统化解决一类数学问题/任务的模型或系统。
- **数学数字化**：把自然语言数学转成形式化表达。
- **Lean / mathlib**：本书重点推荐的形式化生态；Lean 可严格验证证明、构建高难评测。作者称基于 mathlib 形式化时，频繁检索可占近一半时间，因此检索本身应作为独立瓶颈治理。
- **LeanSearch / LeanExplorer**：语义检索工具例子。
- **autoformalization**：自然语言数学到形式语言的自动转换；书中列举 Isabelle/HOL 工作、ProofNet、多语言自动形式化、TheoremLlama、Herald、GAUSS。
- **形式验证驱动推理**：GPT-f、HyperTree Proof Search、AlphaProof/AlphaGeometry 等代表“验证器提供反馈”的路线；AlphaGeometry 使用独立形式系统，且只覆盖一部分平面几何问题。
- **Lean 推理模型/系统**：Goedel-Prover、Kimina Prover、REAL-Prover、DeepSeek-Prover、Qwen2.5-math；`reap` 是 REAL-Prover 的 Lean tactic 形态。
- **Agent**：书中以 DeepMind-DeepThink、Harmonic-Aristotle、ByteDance-Seed Prover 及基于 Gemini 2.5 Pro 的 Agent 等 2025 IMO 相关例子，说明“强基座 + Agent”值得优先评估。
- **AI Scientist / Evolve**：AlphaEvolve、OpenEvolve、ShinkaEvolve 代表可量化目标的迭代改进路线。

## Mental Models
- **数据发现，数学解释升格**：模型输出先是线索，经过解释和验证后才成为数学成果候选。
- **验证器是推理杠杆**：形式系统的价值包含训练/搜索中的高质量反馈。
- **先疏通瓶颈，再追求全自动**：检索与自动形式化常是高收益入口。
- **Evolve 忠实优化指标**：评价函数定义错误时，自动搜索会稳定优化到错误方向。

## Anti-patterns
- 没找可推动环节就直接训练模型。
- 把准确率当数学发现。
- 低估 mathlib 检索与自然语言转形式语言的成本。
- 把 Lean 只当最终验算工具，忽略评测与反馈用途。
- 无工具/验证器时强行 Agent 化。
- 无量化目标或无可靠初始化时使用 Evolve。

## Worked Example — Structural Synthesis
以下执行示意由书中方法工程化重构，用于调用演练，并非原文案例复述。
**专用工具**：先为数学对象生成数据，让模型暴露规律，再由数学家把规律写成结构性猜想并验证。  
**形式化**：自然语言定理 → 检索相关定义/引理 → 自动形式化 → prover/tactic 补全 → Lean 验证；失败时先定位表示、检索、搜索或补全层。  
**Evolve**：已有可运行方案且候选可自动评分时进入“变体—评价—选择—迭代”；只能主观判断优劣时先暂停。

## Reference Table
| 目标 | 路线 | 关键前提 | 失败信号 |
|---|---|---|---|
| 找结构/猜想 | 专用工具 | 可生成数据、数学解释 | 只有准确率 |
| 严格验证 | Lean | 可形式化目标 | 表示/检索卡死 |
| 训练系统推理 | 形式化 + 通用模型 | 形式数据、验证器 | 反馈不足 |
| 多步求解 | Agent | 强基座、工具、反馈 | 循环不收敛 |
| 改进方案 | Evolve | 量化目标、初始化 | 指标失真 |

## Key Takeaways
1. 专用工具与通用模型对应不同研究重心。
2. 专用工具的关键是数据环节选择与数学解释。
3. 形式化把数学变成机器可检查对象，并提供高质量反馈。
4. 先定位检索、自动形式化、证明搜索或局部补全瓶颈，再选工具。
5. 强基座时代值得优先评估 Agent；Evolve 只适合可量化且有初始化的目标。

## Connects To
- Ch 1：任务能力与兴趣决定路线入口。
- Ch 3：所有自动化最终接受“是否提升数学理解”的评价。

## Source Scope
来源第（二）节，PDF 第 1–3 页。
