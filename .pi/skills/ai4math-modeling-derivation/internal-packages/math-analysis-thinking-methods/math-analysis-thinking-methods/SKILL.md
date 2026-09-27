---
name: math-analysis-thinking-methods
description: "Knowledge base and problem-solving router from《数学分析中的思想方法》by 崔国忠、郭从洲、王耀革. Use for mathematical-analysis proofs and calculations: choose the right theorem by structure, standardize expressions, handle limits, continuity, mean-value theorems, inequalities, integration, improper integrals, series, uniform convergence, and Fourier series, with failure recovery and self-checks."
---

# 数学分析中的思想方法
**来源**：崔国忠、郭从洲、王耀革 | **页数**：313 PDF 页 | **内容**：60 讲 | **生成**：2026-09-12

## How to Use This Skill
- 无参数：按下列总控流程解决数学分析题。
- 给题目/主题：先用“任务路由”定位章节，再读取对应 `chapters/chNN-*.md`。
- 给 `chNN`：直接加载该讲。
- 需要快速选法：读取 `cheatsheet.md`；需要跨章方法：读取 `patterns.md`。

## Core Frameworks & Mental Models
1. **结构分析 → 形式统一**：先判断题型、挖掘结构特征、类比已知，解决“用什么”；再把题目标准化为所选定理的结构，解决“怎么用”。
2. **近似 → 极限 → 抽象**：无直接公式时先构造可计算近似，分析误差，再用极限达到精确并抽象为一般理论。
3. **定量化**：把“充分小/大/接近”转为 ε、N、δ、G 等量词关系；严守依赖顺序。
4. **化繁为简**：夹逼、Stolz、Taylor、对数法、换元、分部、连续化都服务于结构降复杂度。
5. **主次分析**：保留决定量级/难度的主因子，用主项控制、预控制、分段把次要因素甩掉。
6. **局部 ↔ 整体**：闭区间套处理整体→局部；有限开覆盖处理局部→整体；开区间局部性质用内闭子区间。
7. **特殊 → 一般**：能归一化就直接转化；不能就化用简单情形的核心机制。
8. **全体 ↔ 部分**：一个坏部分可否定整体；从所有局部得到整体通常还需一致性/紧性。

## Task Router
- **极限定义/ε语言** → Ch03–07, Ch14–16；幂指/重要极限/Taylor → Ch17–20, Ch26。
- **数列极限存在/迭代/不定和** → Ch08–14。
- **连续、零点、中值、导数存在** → Ch21–26。
- **不等式/研究逻辑** → Ch27–30。
- **不定积分** → Ch31–36。
- **定积分、Riemann 和、可积性、积分不等式** → Ch37–44。
- **广义积分** → Ch45–48。
- **数项级数** → Ch49–52, Ch55。
- **一致收敛/函数项级数** → Ch53–58。
- **幂级数/Fourier** → Ch59–60。

## Failure Recovery
- 首选定理条件不满足：回到结构分析，换“同一目标的另一层工具”（定义 ↔ 性质 ↔ 特殊定理）。
- 放缩得不到同一量级：恢复被丢掉的主阶信息，改精细放缩、分段或换比较标准。
- 形式统一更复杂：撤销变换，改向已知/低阶/单变量/标准形统一。
- 临界值判别无结论：视为正常失败信号，改定义、积分判别、Raabe、Cauchy 或构造反例。
- 一致性问题卡住：先找坏点；判“非”优先必要条件/端点，再上 Cauchy。

## SELF_CHECK
- [ ] 真正目标是计算、存在、估计、敛散、还是一致性？
- [ ] 所选定理的作用对象和题目结构匹配吗？
- [ ] 连续/可导/单调/正性/闭区间/非零等前提都验证了吗？
- [ ] N、δ 等控制量只依赖允许依赖的先行参数吗？
- [ ] 放缩保留了正确主阶，局部与整体概念没有混淆吗？
- [ ] 临界/边界/分段点是否单独检查？

## Chapter Index
- 01 [微分学和积分学中的思想方法](chapters/ch01-calculus-approximation-limit.md)
- 02 [结构分析和形式统一的思想方法](chapters/ch02-structural-analysis-form-unification.md)
- 03 [数学概念的定量化思想](chapters/ch03-quantification.md)
- 04 [数列极限定义中的思想方法](chapters/ch04-sequence-limit-definition.md)
- 05 [从数列极限的性质谈起](chapters/ch05-sequence-limit-properties.md)
- 06 [量ε中的数学思想](chapters/ch06-epsilon-thinking.md)
- 07 [无穷大量中的数学思想](chapters/ch07-infinite-quantities.md)
- 08 [夹逼定理的应用思想](chapters/ch08-squeeze-theorem.md)
- 09 [Stolz定理及其应用](chapters/ch09-stolz.md)
- 10 [确界与极限的关系及应用方法](chapters/ch10-supremum-limit.md)
- 11 [单调有界收敛定理的应用方法](chapters/ch11-monotone-bounded.md)
- 12 [闭区间套定理的应用方法](chapters/ch12-nested-intervals.md)
- 13 [有限开覆盖定理及其应用方法](chapters/ch13-finite-open-cover.md)
- 14 [Cauchy收敛准则及其应用方法](chapters/ch14-cauchy-sequences.md)
- 15 [函数极限定义及其应用方法](chapters/ch15-function-limit-definition.md)
- 16 [基本初等函数极限的建立方法](chapters/ch16-elementary-function-limits.md)
- 17 [对数法求极限的思想方法](chapters/ch17-logarithmic-method.md)
- 18 [Heine归结定理中的数学思想](chapters/ch18-heine.md)
- 19 [两个重要极限的思想方法](chapters/ch19-two-important-limits.md)
- 20 [函数极限的结构表示定理及其应用方法](chapters/ch20-limit-representation.md)
- 21 [函数连续性的局部性的应用方法](chapters/ch21-local-continuity.md)
- 22 [闭区间上连续函数的性质应用方法](chapters/ch22-continuous-closed-interval.md)
- 23 [零点存在定理的结构分析与应用方法](chapters/ch23-zero-existence.md)
- 24 [Rolle定理的结构分析与应用方法](chapters/ch24-rolle.md)
- 25 [微分中值定理的结构分析及应用方法](chapters/ch25-mean-value-theorems.md)
- 26 [Taylor展开定理结构分析与应用方法](chapters/ch26-taylor.md)
- 27 [不等式中的数学思想方法](chapters/ch27-inequalities.md)
- 28 [再论Cauchy收敛准则及其应用](chapters/ch28-cauchy-advanced.md)
- 29 [从特殊到一般的应用方法](chapters/ch29-special-to-general.md)
- 30 [部分和整体逻辑关系的应用方法](chapters/ch30-part-whole-logic.md)
- 31 [不定积分计算的基本思想](chapters/ch31-antiderivative-basics.md)
- 32 [不定积分计算的换元法](chapters/ch32-substitution.md)
- 33 [不定积分计算的分部积分法](chapters/ch33-integration-by-parts.md)
- 34 [含n结构的不定积分的计算方法](chapters/ch34-parameterized-indefinite-integrals.md)
- 35 [不定积分计算的主次分析法](chapters/ch35-primary-secondary-integration.md)
- 36 [三角函数的不定积分的计算方法](chapters/ch36-trig-antiderivatives.md)
- 37 [定积分定义中的数学思想方法](chapters/ch37-riemann-integral-definition.md)
- 38 [定积分定义的结构分析方法](chapters/ch38-riemann-integral-structure.md)
- 39 [可积的充要条件的应用方法](chapters/ch39-integrability-criteria.md)
- 40 [特殊结构的定积分的计算方法](chapters/ch40-special-definite-integrals.md)
- 41 [由定积分定义的数列极限的计算方法](chapters/ch41-riemann-sum-sequence-limits.md)
- 42 [定积分不等式](chapters/ch42-integral-inequalities.md)
- 43 [定积分的中值问题](chapters/ch43-integral-mean-value.md)
- 44 [积分学中的形式统一方法](chapters/ch44-integral-form-unification.md)
- 45 [无穷限广义积分的Cauchy收敛准则及应用方法](chapters/ch45-improper-cauchy.md)
- 46 [含三角函数的广义积分方法](chapters/ch46-trig-improper-integrals.md)
- 47 [广义积分敛散性判别的试验性方法](chapters/ch47-improper-test-method.md)
- 48 [广义积分的计算方法](chapters/ch48-improper-integration.md)
- 49 [正项级数敛散性判别法则的逻辑关系及其应用思想方法](chapters/ch49-positive-series-tests.md)
- 50 [再谈试验性判别方法](chapters/ch50-series-test-trial-method.md)
- 51 [级数敛散性判别中的主次分析法和形式统一法](chapters/ch51-series-primary-secondary.md)
- 52 [绝对收敛概念引入的数学思想方法](chapters/ch52-absolute-convergence.md)
- 53 [函数项级数一致收敛性的最值判别法](chapters/ch53-uniform-max-test.md)
- 54 [Dini定理中的判别思想方法](chapters/ch54-dini.md)
- 55 [具交错结构的级数敛散性判别方法](chapters/ch55-alternating-series.md)
- 56 [内闭一致收敛性引入的数学思想方法](chapters/ch56-local-uniform.md)
- 57 [含三角函数因子的函数项级数的一致收敛性](chapters/ch57-trig-function-series.md)
- 58 [函数项级数的非一致收敛性的研究方法](chapters/ch58-nonuniform-convergence.md)
- 59 [幂级数的和函数的计算方法](chapters/ch59-power-series-sums.md)
- 60 [Fourier级数理论中数学思想方法](chapters/ch60-fourier-series.md)

## Topic Index
- **结构分析 / 形式统一** → Ch02, Ch44, Ch51
- **ε、放缩、Cauchy** → Ch03–07, Ch14–16, Ch28, Ch45
- **夹逼 / Stolz / 单调有界** → Ch08–11
- **紧性、局部整体** → Ch12–13, Ch21–22, Ch56
- **零点 / Rolle / 中值 / Taylor** → Ch23–26
- **不定积分** → Ch31–36；**定积分** → Ch37–44；**广义积分** → Ch45–48
- **正项/交错/绝对收敛** → Ch49–52, Ch55
- **一致/非一致收敛** → Ch53–58
- **幂级数 / Fourier** → Ch59–60

## Supporting Files
- [glossary.md](glossary.md) — 关键术语与章节定位
- [patterns.md](patterns.md) — 跨章节操作方法库
- [cheatsheet.md](cheatsheet.md) — 结构→方法决策表

## Scope & Limits
覆盖本书的数学分析思想方法与典型应用。面对测度论、复分析、泛函分析等超出本书范围的核心理论时，应明确说明超出来源范围；可以借用本 Skill 的结构分析方法，但不得冒充书中结论。
