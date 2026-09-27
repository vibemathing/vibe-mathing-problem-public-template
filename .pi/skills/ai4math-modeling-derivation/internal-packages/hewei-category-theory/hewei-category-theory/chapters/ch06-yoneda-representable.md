# 1.6 Yoneda 引理与可表达函子

**Source**: 《范畴论》贺伟，PDF pp. 27–28

## Core Idea
Yoneda 把“从表示函子出发的自然变换”完全还原为一个对象中的元素；表示性把万有性质转成可计算的自然同构。

## Frameworks Introduced
- **Yoneda reduction**
  - When to use: 出现 Nat(C(A,-),F) 时
  - How: 用 α↦α_A(1_A) 转成 F(A)；反向由 x∈F(A) 定义 α_B(f)=F(f)(x)。
- **Representability search**
  - When to use: 一个构造对每个 B 给出集合 F(B)，且看似由某个“通用对象”控制时
  - How: 寻找 (A,x)，使 B 中元素与 A→B 唯一对应，并检验自然性。
- **Universal-element method**
  - When to use: 要证明表示对象唯一时
  - How: 把表示对组织成范畴；通用表示是初始对象，因此唯一到同构。

## Key Concepts
- hom 函子 C(A,-)、C(-,A)。
- Yoneda 引理：Nat(C(A,-),F)≅F(A)。
- 可表达函子：自然同构于 hom 函子。
- 表示 representation：对象与自然同构的配对。
- 通用元素：控制整个函子的元素。

## Mental Models
- 对象可由它与所有对象之间的态射行为识别。
- 复杂自然变换问题可降维成单位态射处的一个元素。

## Anti-patterns
- **Avoid**: 只给集合双射却不检查其对对象/态射的自然性。
- **Avoid**: 猜出表示对象后忽略通用元素或表示同构。

## Worked Example
群范畴到 Set 的遗忘函子由整数群 Z 表示：群 G 的元素 g 对应唯一群同态 Z→G，1↦g。于是“选择 G 的一个元素”与“给出 Z→G 的态射”自然等价。

## Key Takeaways
1. 看到 hom 函子和自然变换立即尝试 Yoneda。
2. 万有性质常能重写为表示问题。
3. 表示对象的唯一性来自初始性/Yoneda。

## Connects To
- 2.6 可表达函子保持极限。
- 3.1 伴随可视为一族自然的 hom 集表示。
