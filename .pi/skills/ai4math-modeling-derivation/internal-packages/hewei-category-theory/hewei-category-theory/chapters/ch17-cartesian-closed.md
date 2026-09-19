# 3.4 Cartesian 闭范畴

**Source**: 《范畴论》贺伟，PDF pp. 66–68

## Core Idea
具有有限积的范畴 C 若每个 A×- 都有右伴随 (-)^A，就能把“二元输入的态射”柯里化为“到幂对象的态射”。

## Frameworks Introduced
- **CCC test**
  - When to use: 判断 C 是否 Cartesian closed 时
  - How: 先确认有限积；再对每个 A 寻找 B^A 与 evaluation e:A×B^A→B，使任意 f:A×C→B 唯一对应 ar f:C→B^A。
- **Right-adjoint obstruction**
  - When to use: 怀疑 A×- 没有右伴随时
  - How: 检查 A×- 是否保持余极限；若不保持，则不能有右伴随。
- **Reflective inheritance**
  - When to use: D 是 C 的反射/余反射满子范畴时
  - How: 按书中命题检查反射函子保持有限积，或余反射子范畴对有限积封闭，再传递 CCC 性质。

## Key Concepts
- Cartesian closed category。
- power object B^A。
- evaluation morphism e:A×B^A→B。
- currying：Hom(A×C,B)≅Hom(C,B^A)。
- Heyting algebra/frame 与偏序型 CCC。

## Mental Models
- 幂对象代表“从 A 到 B 的内部映射空间”。
- CCC 的核心就是乘积函子具有右伴随。

## Anti-patterns
- **Avoid**: 看到普通函数集合就默认它在目标范畴中具有正确结构。
- **Avoid**: 忽略 evaluation 的万有性，只构造 B^A 的候选对象。

## Worked Example
在 Set 中，B^A 取所有函数 A→B 的集合，evaluation 为 e(a,φ)=φ(a)。给定 f:A×C→B，唯一的 ar f:C→B^A 由 ar f(c)(a)=f(a,c) 定义。

## Key Takeaways
1. CCC 验证 = 有限积 + 幂对象万有性质。
2. 右伴随不存在可用余极限不保持来否证。
3. 幂对象让外部 hom 集关系内部化。

## Connects To
- 3.1 幂对象是 A×- 的右伴随。
- 5.3 Sh(X) 是 Cartesian 闭范畴。
