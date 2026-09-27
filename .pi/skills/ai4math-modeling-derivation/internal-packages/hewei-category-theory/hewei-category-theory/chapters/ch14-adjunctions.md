# 3.1 伴随函子的定义

**Source**: 《范畴论》贺伟，PDF pp. 53–58

## Core Idea
伴随用自然的 hom 集双射表达两个方向的“最佳近似”。可在 hom 双射、单位/余单位、通用箭头三种等价表述间切换。

## Frameworks Introduced
- **Adjoint search via hom**
  - When to use: 要找 F 的右伴随 G 时
  - How: 把 B(F(A),B) 重写成 A(A,G(B))，确保双射对 A、B 都自然。
- **Unit/counit verification**
  - When to use: 已有候选 η:1→GF 与 ε:FG→1 时
  - How: 检查两个三角恒等式；成立即得到伴随。
- **Universal-arrow route**
  - When to use: 难以直接写 hom 双射时
  - How: 对每个 A 构造 η_A:A→GF(A) 的通用性，或对每个 B 构造 ε_B:FG(B)→B 的对偶通用性。

## Key Concepts
- F⊣G：F 左伴随、G 右伴随。
- unit η:1_A→GF。
- counit ε:FG→1_B。
- 三角恒等式。
- 通用箭头。
- 伴随在自然同构意义下唯一。

## Mental Models
- 左伴随“自由地产生”，右伴随“忘却/限制”是常见图景。
- 同一伴随可选最省力的表示来证明。

## Anti-patterns
- **Avoid**: 只给逐对象 hom 集等势，不检查自然性。
- **Avoid**: 只写 unit/counit 却不验证三角恒等式。

## Worked Example
离散拓扑函子 D:Set→Top 与底层集合函子 U:Top→Set 满足 D⊣U；同时 U 还有右伴随“赋予平庸拓扑”。这展示同一函子可以既是左伴随又是右伴随。

## Key Takeaways
1. 找伴随优先尝试 hom 集变形。
2. unit/counit 与通用箭头是实用替代路线。
3. 伴随的唯一性以自然同构为准。

## Connects To
- 3.2 伴随存在定理。
- 3.5 伴随自然诱导 monad。
