# 3.5 范畴上的模结构（Monad）

**Source**: 《范畴论》贺伟，PDF pp. 69–73

## Core Idea
伴随 F⊣G 在源范畴上产生 T=GF、单位 η 与乘法 μ=GεF；反过来，任意 monad 通过 Eilenberg–Moore 范畴产生一个标准伴随。

## Frameworks Introduced
- **Adjunction→Monad**
  - When to use: 已有 F⊣G 时
  - How: 设 T=GF、η 为伴随单位、μ=GεF；用三角恒等式验证结合律与单位律。
- **Monad→EM**
  - When to use: 已有 (T,η,μ) 时
  - How: 定义 T-代数 (A,h:T(A)→A)，检查 hη=1 与 hT(h)=hμ；以保持结构的态射组成 C^T。
- **Comparison functor**
  - When to use: 比较原伴随与 EM 标准伴随时
  - How: 构造 K:B→A^T，B↦(G(B),Gε_B)；若 K 为同构，G 可模 monadic。

## Key Concepts
- monad (T,η,μ)。
- T-代数。
- Eilenberg–Moore 范畴 C^T。
- 遗忘函子 G^T 与自由 T-代数函子 F^T。
- comparison functor。
- monadic 可模。

## Mental Models
- monad 是把“自由—遗忘”伴随留在一个范畴内部后的代数化痕迹。
- T-代数是对 T 产生的形式结构进行一致的求值。

## Anti-patterns
- **Avoid**: 只给端函子 T，却遗漏 η、μ 与两条单位律/结合律。
- **Avoid**: 声称 monadic 时只说明存在 comparison functor，未证明其同构。

## Worked Example
自由半群 F:Set→SmGp 与遗忘 G 产生 monad T(X)=所有非空有限字符串；μ 把“字符串的字符串”压平。T-代数结构 h:T(X)→X 正好编码结合的有限乘积，比较函子因此把半群与相应 T-代数对应起来。

## Key Takeaways
1. 伴随自动给 monad。
2. 任意 monad 都有 EM 标准伴随。
3. monadicity 的核心是 comparison functor 是否恢复原范畴。

## Connects To
- 3.6 Beck 定理给 monadicity 判据。
- 3.1 unit/counit 提供 monad 的 η、μ。
