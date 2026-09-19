# 1.2 函子

**Source**: 《范畴论》贺伟，PDF pp. 13–16

## Core Idea
函子在对象和态射两个层面同步映射，并严格保持单位与复合。判断函子的强弱时，区分 faithful、full、对象层面的覆盖程度。

## Frameworks Introduced
- **Functoriality check**
  - When to use: 定义一个候选映射 F:C→D 时
  - How: 验证 F(1_A)=1_{F(A)} 与 F(gf)=F(g)F(f)，同时检查定义域和值域。
- **Full/Faithful diagnosis**
  - When to use: 想知道 F 丢失或制造了多少态射信息时
  - How: 对每对 A,B 检查 C(A,B)→D(F(A),F(B)) 的单射性与满射性。
- **Bifunctor split-check**
  - When to use: 函子同时依赖两个变量时
  - How: 固定一个变量检查另一个变量的函子性，再检查两方向作用彼此相容。

## Key Concepts
- faithful：每个 hom 映射单射。
- full：每个 hom 映射满射。
- 局部单/局部满：书中对 faithful/full 的中文术语。
- 遗忘函子：忘掉部分结构。
- 自由构造：常与遗忘函子配对。
- 双函子：从 C×D 出发的函子。
- 嵌入：书中要求 faithful 且对象映射单射。

## Mental Models
- 把函子视为“结构保持的翻译器”：对象翻译与箭头翻译必须同时成立。
- full/faithful 只控制 hom 集；对象层面的本质满射需另查。

## Anti-patterns
- **Avoid**: 仅检查对象映射就宣称得到函子。
- **Avoid**: 把 full+faithful 直接当成范畴等价：还需对象层面的本质满射。

## Worked Example
幂集可产生协变或反变函子，关键取决于态射如何作用：像映射给出协变方向，逆像映射反转方向。检验复合时使用 (g∘f)^{-1}=f^{-1}∘g^{-1}，方向自然显示为反变。

## Key Takeaways
1. 函数式定义之后立刻做单位与复合两项检查。
2. full、faithful、对象层覆盖分别记录。
3. 双变量构造优先识别为 bifunctor。

## Connects To
- 1.3 自然变换：比较函子。
- 3.1 伴随：用 hom 集自然双射联结两个函子。
