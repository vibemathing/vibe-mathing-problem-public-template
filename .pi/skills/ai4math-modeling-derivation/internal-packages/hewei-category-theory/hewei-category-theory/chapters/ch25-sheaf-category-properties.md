# 5.3 层范畴的性质

**Source**: 《范畴论》贺伟，PDF pp. 100–104

## Core Idea
Sh(X) 具有完备性、子对象分类子和 Cartesian 闭性；这些性质把层范畴推进到与 Topos 思想相关的结构层面。

## Frameworks Introduced
- **Completeness pointwise**
  - When to use: 计算 Sh(X) 的极限时
  - How: 按 U 逐点在 Set 中计算 equalizer、product 等，并用 sheaf 条件证明结果仍是层。
- **Subobject-classifier route**
  - When to use: 要分类 F 的子层 S 时
  - How: 使用 Ω(U)=U 的开子集；对 s∈F(U)，令 χ(s) 为 s 局部落入 S 的最大开部分，得到 χ:F→Ω。
- **Internal-hom construction**
  - When to use: 要证明 Cartesian closed 时
  - How: 定义 G^F(U)=Nat(F|_U,G|_U)，限制由进一步限制自然变换得到；验证其 sheaf 条件及 evaluation 万有性。

## Key Concepts
- subobject classifier Ω。
- truth t:1→Ω。
- characteristic morphism。
- Sh(X) complete。
- Sh(X) Cartesian closed。
- internal hom G^F。

## Mental Models
- Ω 把子层转为“局部真值”。
- 内部 hom 在每个 U 上记录 F|_U→G|_U 的自然变换。

## Anti-patterns
- **Avoid**: 把 Ω(U) 简化成两点真值集，丢失局部开集信息。
- **Avoid**: 证明内部 hom 时只定义对象，未验证 sheaf 条件与 evaluation 的万有性。

## Worked Example
对 X 上的子层 S⊂F，定义 χ_U(s)={V⊂U 开 | s|_V∈S(V)} 的并；它是 U 的开子集。S 恰是 truth t:1→Ω 沿 χ:F→Ω 的拉回，因此 Ω 分类所有子对象。

## Key Takeaways
1. Sh(X) 的极限逐点算。
2. Ω(U)=U 的开集格，承担局部真值。
3. Cartesian 闭性的幂对象用限制层间的自然变换构造。

## Connects To
- 3.4 Cartesian closed 的抽象判据。
- 5.5 Grothendieck 层保留类似的良好性质，书中作简介。
