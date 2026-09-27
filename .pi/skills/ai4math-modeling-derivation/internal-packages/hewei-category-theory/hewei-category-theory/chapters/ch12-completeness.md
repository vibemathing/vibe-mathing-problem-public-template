# 2.5 完备范畴与余完备范畴

**Source**: 《范畴论》贺伟，PDF pp. 47–49

## Core Idea
完备性是“所有小图都有极限”的总括性质，可由更小的生成构造验证：积+等值子；有限版本可用终对象+拉回。

## Frameworks Introduced
- **Completeness basis**
  - When to use: 要证明 C 完备时
  - How: 证明所有小积与所有 equalizer 存在；随后任意图的极限可由对象积与态射约束的 equalizer 构造。
- **Finite-completeness basis**
  - When to use: 只需有限极限时
  - How: 证明终对象与 pullback 存在，或有限积与 equalizer 存在。
- **Dual cocompleteness basis**
  - When to use: 余极限问题
  - How: 把上述条件对偶化为 coproduct+coequalizer，有限版本为初始对象+pushout。

## Key Concepts
- complete 完备。
- finitely complete 有限完备。
- cocomplete 余完备。
- finitely cocomplete 有限余完备。
- 极限生成基。

## Mental Models
- “所有图都存在”通常可拆成少数基本形状。
- 存在性证明优先找生成定理，避免逐图构造。

## Anti-patterns
- **Avoid**: 验证若干熟悉极限就宣称完备。
- **Avoid**: 有限完备与完备混用。

## Worked Example
若 C 有任意积和 equalizer，对 D:J→C，可先取 P=∏_{j∈obJ}D(j)，再把每条 α:i→j 的兼容条件编码成两条 P→∏_{α∈MorJ}D(j)；两者的 equalizer 即满足全部兼容条件的极限对象。

## Key Takeaways
1. 完备性首选积+等值子判据。
2. 有限完备性首选终对象+拉回。
3. 余完备性直接对偶。

## Connects To
- 2.6 保持极限可用同样的基本形状测试。
- 3.2 伴随函子定理需要完备性等结构条件。
