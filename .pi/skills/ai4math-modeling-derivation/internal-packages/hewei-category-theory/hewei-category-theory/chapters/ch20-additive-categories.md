# 4.1 加法范畴

**Source**: 《范畴论》贺伟，PDF pp. 78–81

## Core Idea
准加法范畴让每个 hom 集成为 Abel 群并要求复合双线性；加法范畴再加入零对象与有限双积，使态射具备矩阵式运算。

## Frameworks Introduced
- **Preadditive check**
  - When to use: 判断范畴能否进行态射加法时
  - How: 验证每个 C(A,B) 是 Abel 群，且复合对两变量双线性。
- **Kernel as equalizer**
  - When to use: 准加法环境处理 f:A→B 时
  - How: ker(f) 就是 f 与 0 的 equalizer；coker 对偶。
- **Biproduct criterion**
  - When to use: 判断 C 是否同时是 A×B 与 A⊔B 时
  - How: 寻找 p_i、q_i 满足 p_iq_i=1、交叉项为 0、q_1p_1+q_2p_2=1_C。
- **Additive-functor test**
  - When to use: 判断 T 是否加法时
  - How: 若源是加法范畴，检查 T 是否保持双积；等价于保持 hom 上的加法。

## Key Concepts
- preadditive 准加法范畴。
- zero morphism 零态射。
- zero object 零对象。
- kernel/cokernel。
- biproduct 双积。
- additive category。
- additive functor。
- 对角/余对角态射。

## Mental Models
- 双积把积与余积统一，并使态射像矩阵一样组织。
- 加法来自“对角—分量映射—余对角”的复合。

## Anti-patterns
- **Avoid**: 只有零态射就称加法范畴。
- **Avoid**: 把普通积自动视为双积，未验证加法关系。

## Worked Example
对有限双积 ⊕A_i 与 ⊕B_j，态射 f 完全由矩阵分量 f_{ji}=p_j f q_i 决定；态射复合对应通常的矩阵乘法。这给出抽象加法范畴中的可计算表示。

## Key Takeaways
1. 准加法=hom Abel 群+复合双线性。
2. 加法范畴还需零对象与有限双积。
3. 加法函子可通过保持双积测试。

## Connects To
- 4.2 Abel 范畴在加法范畴上增加核/余核条件。
- 2.2 equalizer/coequalizer 在加法环境中化为 kernel/cokernel。
