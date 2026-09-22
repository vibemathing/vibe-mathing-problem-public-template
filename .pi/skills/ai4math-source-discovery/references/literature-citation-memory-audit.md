# 文献、引用与研究记忆审计

## 定位

这是 `ai4math-source-discovery` 的从属 reference，只在需要核对文献身份、引用语境、查新范围或压缩研究记忆时按需加载。它不新增顶层 Skill，不建立第二套 Claim/Result ledger，输出上限为 `candidate_only`。

## 输入契约

- 精确问题、候选主张或 ProblemContract 引用；
- 检索范围、来源类型、截止日期、语言和停止条件；
- 已知来源 ID、版本、DOI/arXiv ID/稳定 URL，以及允许访问的正文位置；
- 需要核对的引用句、定理、定义、实验结论或“未发现先例”主张。

缺少主张、版本或可定位正文时，结论必须标为 `unresolved`，不得从摘要或搜索片段补造语境。

## 审计流程

1. **身份**：核对标题、作者、版本、发布日期、稳定标识符和撤回/修订状态；预印本与正式版分别记录。
2. **语境**：保存支持当前判断的最小精确段落、定理编号、页码或章节；区分正文、摘要、引用转述和模型总结。
3. **关系**：把来源与主张的关系标为 `supports | contradicts | limits | extends | mentions | unknown`。
4. **支持范围**：分别记录适用定义域、量词、假设、尺度、误差、数据集和版本；局部支持不得升级为完整覆盖。
5. **查新**：记录查询式、数据库、日期、命中与未覆盖区域；“未找到”只能形成有界检索事实，不能形成“从未存在”的结论。
6. **冲突**：来源冲突时保留双方身份和精确差异，不用引用数量投票；优先检查版本、定义和前提不一致。
7. **研究记忆投影**：只压缩已存在的 Source、Attempt、Obligation、Candidate、Evidence 和 failed-route 引用；摘要必须保留原始 ID 和状态，不复制为新真相。

## 最小输出

每个来源—主张关系至少包含：

```text
source_identity
source_version
claim_or_obligation_ref
exact_locator
relation
support_scope
uncovered_scope
verification_state
conflict_or_uncertainty
```

研究记忆摘要还必须包含 `source_refs`、`failed_route_refs`、`open_obligation_refs` 和 `candidate_only=true`。

## Fail-closed 规则

- URL 可访问不等于身份已核验；摘要匹配不等于正文支持。
- 引用存在、引用支持主张、引用覆盖完整结论是三件事。
- 知识页、wiki、检索摘要和上下文包只能是可重建投影，不能签发 Evidence、Result、Solution 或 admission。
- 不把 citation count、搜索排序或多个重复版本当作独立证据。
- 来源身份、许可、正文定位或关系判断无法核实时，保留 `unknown/unresolved`。

## 压力场景

- 场景：搜索摘要看似支持全称主张，但正文定理只覆盖更强假设下的有限情形。
- 诱惑性错误：只记录 URL 并标记 `supports`。
- 正确行为：绑定正文位置，标记局部支持与未覆盖范围；查新和研究记忆仍保持 candidate-only。
- 通过条件：输出能指出假设差异，且不出现“已证明/无先例”的无界结论。

## 方法来源边界

本 reference 是项目原创重写，只吸收了已审候选中“文献身份核对、引用语境核对、有界查新和可回溯研究记忆”的通用方法。评估输入绑定到以下内容摘要：

- `research-lit`：`0a263919812b1135b26e5901af3076395baf03833d0f73c57fe4f11528161453`
- `citation-audit`：`72714bbb165803f918281123a8b50eb15cd28db526e053dfb8f0d9835d28e246`
- `research-wiki`：`93d66229579cb6180c06b661eac022e3784ea770e6793eb3661ba6dc0158f308`
- `novelty-check`：`e1dc8d5e068ffec8ab1fda4fd379394e0f0798ab0f18d0fda3135449f1799a10`

这些候选的精确上游身份和再分发权仍未完成独立确认；因此没有复制其原文、脚本、安装器或依赖，也不把它们加入 internal package registry。
