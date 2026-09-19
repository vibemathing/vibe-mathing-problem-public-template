# 2.3 积与余积

**Source**: 《范畴论》贺伟，PDF pp. 39–41

## Core Idea
积/余积是离散图的极限/余极限。积的态射由各分量唯一确定，余积对偶；有限积可由终对象和二元积生成。

## Frameworks Introduced
- **Componentwise map**
  - When to use: 要构造 X→∏A_i 时
  - How: 分别给出 f_i:X→A_i，再由积的万有性质得到唯一 ⟨f_i⟩。
- **Product existence reduction**
  - When to use: 证明有限积存在时
  - How: 只需终对象与二元积；任意积问题可迭代。
- **Category-specific coproduct check**
  - When to use: 在具体范畴构造余积时
  - How: 不要沿用集合并集直觉；根据该范畴的万有性质选择不交并、自由积等。

## Key Concepts
- product ∏A_i 与投影 p_i。
- coproduct ∐A_i 与余投影 q_i。
- 有限积/有限余积。
- 二元积与终对象。
- 积中态射按分量唯一。

## Mental Models
- 积收集“同时指向各分量”的数据。
- 余积收集“从各分量出发”的数据。

## Anti-patterns
- **Avoid**: 只给候选底层集合而不验证范畴结构和万有性质。
- **Avoid**: 假设所有具体范畴中的余积等于集合的不交并。

## Worked Example
给定 f_j:A_j→B_j，可用积的万有性质定义 ∏f_j:∏A_j→∏B_j，使第 j 个投影满足 q_j(∏f_i)=f_jp_j。这个分量方程同时给存在与唯一性。

## Key Takeaways
1. 构造到积的箭头时按分量做。
2. 有限积存在性归约到终对象+二元积。
3. 余积始终按其万有性质辨认。

## Connects To
- 2.4 拉回可由积+等值子构造。
- 4.1 在加法范畴中积与余积合并为双积。
