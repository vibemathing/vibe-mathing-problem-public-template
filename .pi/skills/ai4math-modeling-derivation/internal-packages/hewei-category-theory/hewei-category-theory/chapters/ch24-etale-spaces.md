# 5.2 局部同胚映射与层空间

**Source**: 《范畴论》贺伟，PDF pp. 95–99

## Core Idea
拓扑空间 X 上的层与 X 上的局部同胚映射等价。准层通过 germs 构造关联层空间，局部同胚通过局部截面构造层。

## Frameworks Introduced
- **Presheaf→étalé space**
  - When to use: 给 F:T(X)^op→Set 时
  - How: 对每个 x 取 stalk/germ 等价类，合并成 A_F→X；用截面像作为拓扑基，得到局部同胚。
- **Map→sheaf**
  - When to use: 给 p:Y→X 时
  - How: 令 Θ_p(U) 为满足 p∘s=包含 U↪X 的连续局部截面；限制由截面限制给出。
- **Equivalence test**
  - When to use: F 已是 sheaf 或 p 已是局部同胚时
  - How: 单位 F→ΘA_F 或余单位 AΘ_p→Y 为同构，得到 Sh(X)≃LH/X。
- **Sheafification route**
  - When to use: 给一般 presheaf 时
  - How: 通过 A 再回到 Θ，得到关联层/层化，体现 Sh(X) 是 presheaf 范畴的反射子范畴。

## Key Concepts
- local homeomorphism 局部同胚映射。
- associated sheaf space A_F。
- germ 芽。
- slice LH/X。
- sheafification 关联层函子。
- Sh(X)≃LH/X。

## Mental Models
- 层的截面语言与局部同胚的几何语言可以互译。
- stalk/germ 把所有局部信息按点聚合成空间。

## Anti-patterns
- **Avoid**: 对任意连续 p:Y→X 都直接宣称 AΘ_p≅Y；需要 p 局部同胚。
- **Avoid**: 准层直接当层使用；单位只有在 sheaf 情形才是同构。

## Worked Example
从层 F 构造 A_F：元素是局部截面的 germ [s]_x，投影 [s]_x↦x。固定 s∈F(U) 时，x↦[s]_x 给出 U→A_F 的局部截面，其像构成拓扑基；投影在这些基本开集上是同胚。

## Key Takeaways
1. 层问题可切换到 étalé space 几何。
2. 一般准层经 sheafification 得最佳层逼近。
3. 等价由伴随的 unit/counit 在对应子范畴上成为同构实现。

## Connects To
- 3.3 sheafification 是反射的实例。
- 5.4 inverse image 可通过局部同胚的 pullback 构造。
