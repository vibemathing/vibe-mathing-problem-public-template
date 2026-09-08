---
id: GOV-AGENT-ENTRY
type: process
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Agent Entry

## 项目工作协议

1. 不要在没有验证证据的情况下声明“已完成”或“已测试”。
2. 开始任务前先读取 `governance/INDEX.md`。
3. 根据 `governance/context/CONTEXT-ROUTER.md` 选择最小上下文。
4. 涉及架构边界时必须读取相关 ADR。
5. 涉及用户功能时必须产出 QA 计划或验证证据。
6. 高风险变更必须说明回滚路径。
7. 如果发现重复错误或标准缺失，记录到 `agent-governance/agent-feedback/`。
8. 涉及跨模块研究结构时，先按点—线—面—体唯一元模型根定位对象、关系、知识面和知识体作用域；不得另立并列顶层。
9. 涉及研究目标或执行编排时，在 F05 PWTSJ 过程编排面按 `Project → Workflow → Task → Step → Job` 建模，并分别绑定 ProblemContract、OutcomeNode、Attempt/Route、Obligation、CandidateArtifact、Evidence 与 Result；不得把 Job 成功当作数学闭合。
