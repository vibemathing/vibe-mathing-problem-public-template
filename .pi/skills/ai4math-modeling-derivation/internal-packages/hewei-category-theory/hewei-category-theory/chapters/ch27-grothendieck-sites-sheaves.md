# 5.5 Grothendieck 拓扑与 Grothendieck 层

**Source**: 《范畴论》贺伟，PDF pp. 108–113

## Core Idea
Grothendieck 拓扑把“开覆盖”推广为小范畴上的覆盖筛；层条件继续要求相容局部数据唯一粘合。拓扑基版本用覆盖族和 pullback 表述，更接近实际计算。

## Frameworks Introduced
- **Sieve check**
  - When to use: 判断 S 是否为 C 上的筛时
  - How: 确认所有箭头值域为 C，且若 f∈S、g 可与 f 复合，则 fg 仍在 S；等价地 S⊂C(-,C) 为子函子。
- **Grothendieck topology axioms**
  - When to use: 验证 J 时
  - How: 逐对象检查最大筛覆盖；覆盖筛沿任意箭头拉回仍覆盖；局部传递条件成立。
- **Basis route**
  - When to use: 给覆盖族而非筛时
  - How: 在有 pullback 的小范畴上检查同构覆盖、基变换稳定、复合覆盖；由此生成 Grothendieck topology。
- **Site sheaf test**
  - When to use: 判断 P:C^op→Set 是否为 sheaf 时
  - How: 对每个 covering sieve 的 matching family 要求唯一 amalgamation；若有 Grothendieck basis，只需对基中的覆盖族检查。

## Key Concepts
- sieve 筛。
- covering sieve 覆盖筛。
- Grothendieck topology J。
- site (C,J)。
- Grothendieck topology basis。
- matching family 相容族。
- Grothendieck sheaf。

## Mental Models
- 普通开覆盖只依赖“覆盖如何拉回、如何复合”；Grothendieck topology 抽取的正是这些范畴性质。
- 层条件的核心保持不变：相容局部数据具有唯一全局粘合。

## Anti-patterns
- **Avoid**: 把任意箭头族叫覆盖而不检查基变换与传递。
- **Avoid**: 有拓扑基时仍遍历所有 covering sieves，造成不必要复杂度。

## Worked Example
普通拓扑空间 X 的开集偏序 T(X) 可赋 Grothendieck topology：U 上的 covering sieve S 要覆盖 U，并向下闭合。任意普通开覆盖生成这样的筛；于是定义 5.5.3 的 site-sheaf 条件还原到熟悉的开覆盖粘合条件。

## Key Takeaways
1. 筛就是 representable hom 函子的子对象。
2. Grothendieck topology 用最大性、拉回稳定、局部传递编码覆盖。
3. 有 basis 时用 matching family 检查 sheaf 条件最实用。

## Connects To
- 1.6 sieve 定义依赖 representable functor。
- 5.1 普通 sheaf 条件是 site sheaf 的原型。
