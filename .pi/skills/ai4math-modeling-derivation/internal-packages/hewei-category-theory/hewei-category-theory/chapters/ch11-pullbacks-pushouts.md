# 2.4 拉回与推出

**Source**: 《范畴论》贺伟，PDF pp. 42–46

## Core Idea
拉回把两条指向同一对象的态射同步化，是范畴化的纤维积与逆像；推出是完全对偶的“粘合”。

## Frameworks Introduced
- **Pullback test**
  - When to use: 给定 A→C←B 并有候选 P 时
  - How: 检查方形交换；对任何 X→A、X→B 且两复合相等，构造唯一 X→P。
- **Inverse-image route**
  - When to use: 要把 B 的子对象沿 f:A→B 拉回时
  - How: 形成 pullback；得到 A 中的逆像子对象。
- **Stability transfer**
  - When to use: 要证明 mono/regular mono 在基变换下保持时
  - How: 使用其 pullback 稳定性；对偶地 epi/regular epi 在 pushout 下稳定。

## Key Concepts
- pullback 拉回/纤维积。
- pushout 推出。
- pullback-stable 类。
- 子对象的逆像。
- 拉回可由积+等值子构造。
- 推出可由余积+余等值子构造。

## Mental Models
- 拉回表达“两个数据具有同一像”的最通用解。
- pushout 表达“沿共同部分粘合”的最通用解。

## Anti-patterns
- **Avoid**: 只画交换方形就称为 pullback。
- **Avoid**: 从底层集合纤维积直接推出任意具体范畴中的拉回而不检查附加结构。

## Worked Example
在 Set 中，f:A→C、g:B→C 的拉回可取 P={(a,b)|f(a)=g(b)}，投影到 A、B。给定 x↦a(x)、x↦b(x) 且 f(a(x))=g(b(x))，唯一中介映射是 x↦(a(x),b(x))。

## Key Takeaways
1. 拉回证明必须包含唯一中介态射。
2. 子对象逆像优先画 pullback。
3. 基变换稳定性常替代繁琐元素计算。

## Connects To
- 2.5 有限完备性可由终对象+拉回刻画。
- 5.4 逆向层函子用局部同胚的拉回来构造。
