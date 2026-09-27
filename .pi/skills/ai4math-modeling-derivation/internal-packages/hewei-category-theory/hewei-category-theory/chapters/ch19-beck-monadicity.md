# 3.6 Beck 定理

**Source**: 《范畴论》贺伟，PDF pp. 74–77

## Core Idea
Beck 定理用某类余等值子的产生性质判定一个右伴随是否 monadic；分裂余等值子提供易验证的充分测试形状。

## Frameworks Introduced
- **Split coequalizer check**
  - When to use: 需要识别稳定于任意函子的余等值子时
  - How: 寻找 s、t 使 cs=1、ft=1、gt=sc；分裂条件只含复合等式，因此被任意函子保持。
- **Beck route**
  - When to use: 已有 F⊣G，需判定 G monadic 时
  - How: 检查 G 是否产生那些经 G 后具有 split coequalizer（等价可用 absolute coequalizer 条件）的平行对的余等值子。
- **Comparison conclusion**
  - When to use: Beck 条件成立时
  - How: 推出比较函子 K:B→A^T 为同构，从而伴随由源范畴上的 monad 完全恢复。

## Key Concepts
- split coequalizer 分裂余等值子。
- absolute coequalizer 绝对余等值子。
- 产生余等值子。
- Beck monadicity theorem。

## Mental Models
- “绝对”表示经所有函子仍保持；“分裂”用显式复合等式保证绝对性。
- Beck 把难检的 comparison-isomorphism 转成余等值子 lifting 条件。

## Anti-patterns
- **Avoid**: 把普通 coequalizer 自动当成 absolute。
- **Avoid**: 调用 Beck 时忘记前提存在伴随 F⊣G。

## Worked Example
若 c:B→C 是 f,g:A⇉B 的 split coequalizer，并有 s:C→B、t:B→A 满足 cs=1_C、ft=1_B、gt=sc，则任何函子都保留这些等式；由此 G(c) 的余等值子性质具有很强的稳定性，正适合 Beck 判据。

## Key Takeaways
1. monadicity 先找伴随，再检查 Beck 的余等值子条件。
2. split coequalizer 是实践中最易验证的版本。
3. comparison functor 是最终对象。

## Connects To
- 3.5 monad 与 comparison functor。
- 2.2 coequalizer 的万有性质。
