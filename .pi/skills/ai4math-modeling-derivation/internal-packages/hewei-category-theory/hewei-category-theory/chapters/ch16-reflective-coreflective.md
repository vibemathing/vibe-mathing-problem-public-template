# 3.3 反射子范畴与余反射子范畴

**Source**: 《范畴论》贺伟，PDF pp. 62–65

## Core Idea
满子范畴的包含函子若有左伴随，就给出每个对象到子范畴的最佳近似（反射）；若有右伴随则给出余反射。

## Frameworks Introduced
- **Reflection construction**
  - When to use: 要证明 D⊂C reflective 时
  - How: 为每个 C 构造 η_C:C→D_C，要求对任意 D∈D 的 C→D 唯一经 η_C 分解。
- **Coreflection dual**
  - When to use: 最佳近似方向从 D_C→C 时
  - How: 转为包含函子的右伴随，全部论证对偶化。
- **Closure consequence**
  - When to use: D 是同构闭满反射子范畴时
  - How: 利用包含右伴随保持极限，推导 D 对 C 中相应极限封闭。

## Key Concepts
- reflective subcategory 反射子范畴。
- reflector 反射函子。
- coreflective subcategory 余反射子范畴。
- D-reflection。
- mono/epi/bireflective 等加强型。

## Mental Models
- 反射 = “从 C 到 D 的最佳逼近”；余反射 = 方向相反的最佳逼近。
- 反射与闭包性质常由伴随的极限保持性解释。

## Anti-patterns
- **Avoid**: 仅给每个对象一个 D 中对象，却不证明万有分解。
- **Avoid**: 反射与余反射的箭头方向混淆。

## Worked Example
Abel 群作为群的满子范畴具有反射：群 G 映到其 Abel 化 G/[G,G]，任何从 G 到 Abel 群的同态唯一经过这个商。这个万有性质直接给出包含 AbGp→Gp 的左伴随。

## Key Takeaways
1. 最佳近似问题优先识别反射/余反射。
2. 验证反射要写清通用分解。
3. 闭包性可从伴随保持极限/余极限得到。

## Connects To
- 3.4 反射/余反射可继承 Cartesian 闭性（带额外条件）。
- 5.2 层范畴是准层范畴的反射子范畴。
