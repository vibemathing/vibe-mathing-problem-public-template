# 4.3 正合序列

**Source**: 《范畴论》贺伟，PDF pp. 84–90

## Core Idea
序列在某点正合意味着“前一箭头的像 = 后一箭头的核”。加法函子的左/右/双边正合性可归约为 kernel/cokernel 或有限极限/余极限保持性。

## Frameworks Introduced
- **Exactness test**
  - When to use: 检查 A→B→C 在 B 处正合时
  - How: 先确认复合为 0，再比较 im(f) 与 ker(g)；在 Abel 范畴用规范分解构造两者。
- **Short-exact recognition**
  - When to use: 检查 0→A→B→C→0 时
  - How: 左端使 f mono，右端使 g epi，中间要求 f=ker(g)（等价 g=coker(f)）。
- **Functor exactness**
  - When to use: 判断加法函子 T
  - How: 左正合⇔保持 kernels⇔保持有限极限；右正合⇔保持 cokernels⇔保持有限余极限；两者兼有即正合。
- **Pseudoelement route**
  - When to use: 抽象 Abel 范畴想模拟元素追踪时
  - How: 使用伪元素及伪相等；书中给出 mono/epi/正合的伪元素判据。

## Key Concepts
- exact sequence 正合序列。
- connected sequence 连通序列：相邻复合为 0。
- left/right/exact functor。
- pseudoelement 伪元素。
- pseudoequality 伪相等。
- 弱蛇形引理。

## Mental Models
- 正合性 = “所有被下一箭头杀掉的数据恰来自前一箭头”。
- 伪元素让元素追踪在一般 Abel 范畴中保留形式，但必须按书中的等价关系使用。

## Anti-patterns
- **Avoid**: 只检查 gf=0 就称序列正合。
- **Avoid**: 在抽象 Abel 范畴直接使用普通集合元素。

## Worked Example
短列 0→A --f→ B --g→ C→0 正合时，f 是 g 的 kernel，g 是 f 的 cokernel。检查时可分成三件事：ker(f)=0、im(f)=ker(g)、coker(g)=0。

## Key Takeaways
1. 连通只给 gf=0，正合还需 im=ker。
2. 函子正合性可用 kernel/cokernel 保持性判断。
3. 需要 diagram chase 时可转为伪元素。

## Connects To
- 4.2 image/coimage 分解提供 exactness 基础。
- 3.2 伴随的极限保持性可推断某些左/右正合性质。
