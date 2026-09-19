# 1.7 射影对象与单射对象

**Source**: 《范畴论》贺伟，PDF pp. 29–31

## Core Idea
射影/单射对象由提升与延拓性质定义；它们把 epi/mono 相关的求解问题转为某个 hom 函子的保持性。

## Frameworks Introduced
- **Projective lifting**
  - When to use: 给定 epi e:B→C 与 f:P→C 时
  - How: 寻找 g:P→B 使 eg=f；若对所有 epi 都可做，P 射影。
- **Hom-preservation test**
  - When to use: 判断 P 是否射影时
  - How: 检查 C(P,-) 是否把 epi 送到满射；单射对象使用对偶 hom 函子。
- **Retract inheritance**
  - When to use: 对象已知是射影/单射对象的 retract 时
  - How: 沿 retract 分解转移提升/延拓，快速得到同类性质。

## Key Concepts
- E-射影对象：只针对指定 epi 类 E 的提升。
- 射影对象：针对所有 epi。
- M-单射对象：对指定 mono 类的延拓。
- 单射对象：对所有 mono。
- retract：存在 i,r 且 ri=1。

## Mental Models
- 射影对象让“向下穿过 epi”可解；单射对象让“沿 mono 向外延伸”可解。
- lifting property 与 hom 函子的满射性是同一事实的两种表述。

## Anti-patterns
- **Avoid**: 把相对射影 E-projective 当成绝对射影。
- **Avoid**: 只在一个具体 epi 上能提升就宣称对象射影。

## Worked Example
证明 P 射影时，可把任意 epi e:B→C 作用到 hom 集：C(P,B)→C(P,C)。该映射满射恰好意味着每个 f:P→C 都有 lift g:P→B。

## Key Takeaways
1. 提升图是射影/单射问题的首选表示。
2. 用 hom 函子保持性把对象性质转成映射性质。
3. retract 是常用的性质继承机制。

## Connects To
- 2.2 正则 epi/mono 提供更细的态射类。
- 4.3 正合性中的提升常与射影/单射思想相连。
