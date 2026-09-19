# 2.6 保持、反射与产生极限

**Source**: 《范畴论》贺伟，PDF pp. 50–52

## Core Idea
函子与极限的关系分为保持、反射、产生三种强度。右伴随和可表达函子常保持极限；产生极限比反射更强。

## Frameworks Introduced
- **Preservation reduction**
  - When to use: 要证明 F 保持有限极限时
  - How: 检查有限积+equalizer，或终对象+pullback；全极限检查积+equalizer。
- **Representable shortcut**
  - When to use: F=C(A,-) 或其他可表达函子时
  - How: 直接调用可表达函子保持极限。
- **Create-vs-reflect check**
  - When to use: 已知像中的极限时
  - How: 若能唯一提升为原范畴极限，称 create；若只从“像是极限”推出“原来是极限”，称 reflect。

## Key Concepts
- preserve limits 保持极限。
- reflect limits 反射极限。
- create limits 产生极限。
- 产生⇒反射。
- 可表达函子保持极限。

## Mental Models
- 保持：已有极限向前不坏；反射：目标极限可倒推；产生：目标构造可唯一提升。
- 用少数基本极限形状测试复杂保持性。

## Anti-patterns
- **Avoid**: 从 reflect 直接推出 create。
- **Avoid**: 忽略有限极限与任意极限的范围差异。

## Worked Example
遗忘函子 Gp→Set 可通过底层集合上的极限构造并唯一赋予逐点群结构，因此书中把它作为“产生极限”的典型；这比单纯保持或反射提供了更多重建信息。

## Key Takeaways
1. 先明确所需强度：preserve、reflect、create。
2. 极限保持性尽量归约到基本形状。
3. hom/representable 情形优先用现成定理。

## Connects To
- 3.2 右伴随保持极限、左伴随保持余极限。
- 5.4 逆向层函子保持有限极限。
