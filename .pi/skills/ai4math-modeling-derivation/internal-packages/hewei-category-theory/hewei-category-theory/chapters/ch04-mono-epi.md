# 1.4 单态射与满态射

**Source**: 《范畴论》贺伟，PDF pp. 22–23

## Core Idea
单态射与满态射由消去律定义；在一般范畴里，它们与“单射/满射”的集合直觉可能分离。

## Frameworks Introduced
- **Cancellation test**
  - When to use: 判断 f:A→B 是否 mono/epi 时
  - How: mono 检查 fr=fs⇒r=s；epi 检查 rf=sf⇒r=s。不要默认存在元素。
- **Split shortcut**
  - When to use: 已有左逆或右逆时
  - How: 有左逆立即推出 mono；有右逆立即推出 epi；双边逆给同构。
- **Balanced-category check**
  - When to use: 想从 mono+epi 推同构时
  - How: 先确认范畴平稳 balanced；否则寻找反例或额外逆。

## Key Concepts
- 单态射 monomorphism：左消去。
- 满态射 epimorphism：右消去。
- 双态射 bimorphism：同时 mono 和 epi。
- 分裂单态射：存在左逆。
- 分裂满态射：存在右逆。
- 平稳范畴：每个 bimorphism 都是同构。
- 严格单态射：练习中引入的更强概念。

## Mental Models
- mono/epi 是“可区分测试态射的能力”，比底层集合的单/满更范畴化。
- 如果证明只用了消去律，它可迁移到任意范畴。

## Anti-patterns
- **Avoid**: 在 Rng 或 Top 中用集合直觉代替 epi 定义。
- **Avoid**: 从 bimorphism 直接推出 iso 而未检查 balanced 条件。

## Worked Example
书中强调环范畴里的满态射未必在底层集合上满射；因此判定 epi 时应回到“任意两条出箭头在 f 后相等便相等”的定义。这个例子用于提醒：具体范畴中的集合性质需要单独证明。

## Key Takeaways
1. 抽象判定优先使用消去律。
2. 有逆时用 split 条件快速结束。
3. bimorphism→iso 需要 balanced 假设。

## Connects To
- 1.5 子对象/商对象：分别用 mono/epi 表示。
- 2.2 正则单/满态射：用等值子/余等值子加强。
