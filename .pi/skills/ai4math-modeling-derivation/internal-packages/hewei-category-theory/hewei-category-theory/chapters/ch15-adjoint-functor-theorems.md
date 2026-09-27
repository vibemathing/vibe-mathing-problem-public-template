# 3.2 伴随函子定理

**Source**: 《范畴论》贺伟，PDF pp. 59–61

## Core Idea
伴随存在性可通过“保持极限 + 解答集”之类结构条件保证。核心中介是逗号范畴 (A↓G) 的初始对象。

## Frameworks Introduced
- **Comma initial-object criterion**
  - When to use: 判断 G:B→A 是否有左伴随时
  - How: 对每个 A∈A 构造 (A↓G) 的初始对象；其箭头 A→G(B) 就是通用箭头。
- **General adjoint theorem**
  - When to use: 直接构造通用对象困难时
  - How: 核对 B 完备、G 保持极限、solution set condition；条件齐全再调用广义伴随函子定理。
- **Special adjoint theorem**
  - When to use: 有更强的范畴结构时
  - How: 核对 B 完备且 well-powered，并有余分离集；此时保持极限足以推出左伴随存在。

## Key Concepts
- comma category (A↓G)。
- solution set condition 解答集条件。
- general adjoint functor theorem。
- special adjoint functor theorem。
- 右伴随保持极限；左伴随保持余极限。

## Mental Models
- 伴随存在问题可重写成“某逗号范畴是否有初始对象”。
- 定理使用前先做假设清单，避免只凭“保持极限”下结论。

## Anti-patterns
- **Avoid**: 遗漏完备性或解答集条件就调用广义定理。
- **Avoid**: 把“右伴随保持极限”的必要条件误当成无条件充分条件。

## Worked Example
若要证明 G 有左伴随，可固定 A，观察所有 A→G(B) 组成的 (A↓G)。若找到一个初始对象 η_A:A→G(F(A))，任何 A→G(B) 都唯一经 G(f)∘η_A 分解，这正给出 F(A) 的通用性。

## Key Takeaways
1. 显式通用对象最直接。
2. 失败时升级到逗号范畴与伴随函子定理。
3. 每次调用存在定理都列出完整前提。

## Connects To
- 2.6 保持极限提供关键必要条件。
- 3.3 反射子范畴由包含函子的伴随刻画。
