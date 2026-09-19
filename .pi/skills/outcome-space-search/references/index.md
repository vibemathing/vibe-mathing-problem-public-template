# References

建议按以下顺序读取：

1. `../SKILL.md`：触发条件、边界、frontier 规则和输出要求；
2. `method.md`：候选 Outcome Graph 构造与更新算法；
3. `output-contract.md`：plan 字段、消费者与非真相语义；
4. `osps-plan.schema.json`：可机械检查的 candidate-only 输出契约；
5. `valid-minimal-plan.json`：无业务数据的最小正例；
6. `pressure-tests.md`：错 Problem、错 digest、伪等价、错误根传播、重复路线和越权执行攻击；
7. `web-gpt-parallel-tree.md`：Web GPT 九路并发分类完整树、唯一归类顺序和命中语义；
8. `web-gpt-parallel-tree.v1.json` 与 `web-gpt-parallel-tree.schema.json`：九路分类的机器契约；
9. `web-gpt-task-set.schema.json` 与 `web-gpt-synthetic-response-set.schema.json`：九槽候选任务与合成返回合同；
10. `optimization-notes.md`：0.2.0 加固基线、残余局限和下一轮候选；
11. `source-map.md`：internal 原始定义及外部相邻方法来源。

这些文件定义的是规划 Skill，不是正式 Outcome Graph owner、运行时数据库或 orchestrator。
