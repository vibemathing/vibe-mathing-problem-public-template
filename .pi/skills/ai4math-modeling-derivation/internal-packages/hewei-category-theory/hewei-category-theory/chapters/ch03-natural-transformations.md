# 1.3 自然变换与范畴等价

**Source**: 《范畴论》贺伟，PDF pp. 17–21

## Core Idea
自然变换要求各对象上的分量与所有态射兼容。范畴等价允许对象只在同构意义下对应，判定时优先使用“full + faithful + essentially surjective”。

## Frameworks Introduced
- **Naturality-square proof**
  - When to use: 要证明一族 α_A:F(A)→G(A) 构成自然变换时
  - How: 对任意 f:A→B 写出 G(f)α_A=α_BF(f)，逐类态射验证。
- **Equivalence criterion**
  - When to use: 要证明 C 与 D 等价时
  - How: 证明 F full、faithful，并证明 D 中每个对象都同构于某个 F(A)。
- **Skeleton reduction**
  - When to use: 等价问题被大量同构对象干扰时
  - How: 取骨架，每个同构类留一个代表；等价范畴的骨架同构。

## Key Concepts
- 自然变换：函子间与所有态射兼容的分量族。
- 自然同构：每个分量均为同构。
- 函子范畴 [C,D]：对象为函子，态射为自然变换。
- 范畴等价：存在拟逆及两个自然同构。
- 本质满射：目标对象均同构于像中的对象。
- 骨架：每个对象同构类只取一个代表。

## Mental Models
- 严格相等太强时，把目标降到自然同构或范畴等价。
- 自然性是“换路径结果一致”，优先画交换方形。

## Anti-patterns
- **Avoid**: 逐对象给出同构，却不检查自然性。
- **Avoid**: 把等价误写成严格同构，导致不必要的对象级一一对应要求。

## Worked Example
若 F:C→D full、faithful 且本质满射，可为 D 中每个对象选一个来自 F 的同构代表，由 full/faithful 唯一地提升态射，构造拟逆 G，并得到 GF≅1_C、FG≅1_D。这个判据通常比直接猜 G 更省力。

## Key Takeaways
1. 自然变换证明的核心是自然性方形。
2. 范畴等价优先走 full+faithful+本质满射判据。
3. 遇到“相同结构”问题，先判断需要同构还是等价。

## Connects To
- 1.6 Yoneda：自然变换被对象元素完全控制。
- 5.2 层与局部同胚：给出重要的范畴等价实例。
