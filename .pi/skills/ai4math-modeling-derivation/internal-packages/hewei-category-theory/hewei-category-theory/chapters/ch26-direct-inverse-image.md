# 5.4 定向层函子与逆向层函子

**Source**: 《范畴论》贺伟，PDF pp. 104–108

## Core Idea
连续映射 f:X→Y 在层范畴间诱导定向层函子 f_*:Sh(X)→Sh(Y) 与逆向层函子 f^*:Sh(Y)→Sh(X)，且 f^*⊣f_*；逆向层函子保持有限极限。

## Frameworks Introduced
- **Direct image**
  - When to use: 给 F∈Sh(X) 时
  - How: 定义 (f_*F)(V)=F(f^{-1}V)，restriction 由逆像包含诱导；f^{-1} 保持交与并保证仍为层。
- **Inverse image geometrically**
  - When to use: 给 G∈Sh(Y) 时
  - How: 把 G 对应到局部同胚 A_G→Y，沿 f 拉回得到 X 上局部同胚，再转回层，定义 f^*G。
- **Adjunction check**
  - When to use: 需要 f^*⊣f_* 时
  - How: 使用局部同胚/截面模型构造 unit 与 counit，验证三角恒等式。
- **Finite-limit preservation**
  - When to use: 证明 f^* 左正合时
  - How: 在局部同胚切片范畴中把 f^* 视为 pullback functor；它保持终对象与 pullback，因此保持有限极限。

## Key Concepts
- direct image sheaf functor f_*。
- inverse image sheaf functor f^*。
- f^*⊣f_*。
- base change/pullback of local homeomorphisms。
- f^* preserves finite limits。

## Mental Models
- f_* 直接做开集逆像；f^* 用几何 pullback 重建局部数据。
- 逆像函子左伴随同时保持有限极限，是层论的重要组合。

## Anti-patterns
- **Avoid**: 把 f^* 简单写成对开集的复合而忽略层化/几何重建。
- **Avoid**: 只因 f^* 是左伴随就推断保持极限；有限极限保持来自额外 pullback 结构。

## Worked Example
若 p:E→Y 是与层 G 对应的局部同胚，则 f^*G 对应 E×_Y X→X。局部同胚沿任意连续映射拉回仍为局部同胚，因此该构造留在层的几何模型内。

## Key Takeaways
1. f_* 可直接按 f^{-1}(V) 计算。
2. f^* 用 étalé space 的 pullback 最清楚。
3. f^*⊣f_*，且 f^* 保持有限极限。

## Connects To
- 2.4 pullback 是 f^* 几何构造的核心。
- 5.2 Sh(X)≃LH/X 提供翻译桥梁。
