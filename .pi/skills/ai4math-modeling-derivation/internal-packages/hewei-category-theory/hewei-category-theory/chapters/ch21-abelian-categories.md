# 4.2 Abel 范畴

**Source**: 《范畴论》贺伟，PDF pp. 82–84

## Core Idea
Abel 范畴把加法、有限极限/余极限、kernel/cokernel 紧密结合，使每个态射都有规范的 epi–mono 分解，并定义像与余像。

## Frameworks Introduced
- **Abelian checklist**
  - When to use: 判断 C 是否 Abel 时
  - How: 核对：加法；有限完备与有限余完备；每个 mono 是某态射的 kernel；每个 epi 是某态射的 cokernel。
- **Mono/epi by kernel**
  - When to use: Abel 范畴中判定 f 的 mono/epi
  - How: mono ⇔ ker(f)=0；epi ⇔ coker(f)=0。
- **Canonical factorization**
  - When to use: 分析任意 f:A→B 时
  - How: 构造 m=ker(coker f)=im(f)，e=coker(ker f)=coim(f)，得到唯一 f=me，e epi、m mono。
- **Square via biproduct**
  - When to use: 判断交换方形是否 pullback/pushout 时
  - How: 把方形编码成 A→B⊕C 与 B⊕C→D；kernel/cokernel 条件给出判据。

## Key Concepts
- Abelian category。
- im(f)=ker(coker f)。
- coim(f)=coker(ker f)。
- epi–mono factorization。
- AbGp、Mod_R 为基本例子。

## Mental Models
- 在 Abel 范畴中，“像=核的核外部分”有完全范畴化表达。
- kernel/cokernel 是大量证明的统一接口。

## Anti-patterns
- **Avoid**: 在一般加法范畴中使用 Abel 范畴特有的 mono⇔ker=0。
- **Avoid**: 略过“所有 mono/epi 都正规”的条件。

## Worked Example
给 f:A→B，先取 coker(f):B→C，再取其 kernel m:I→B；因为 coker(f)f=0，f 唯一分解为 A→I→B。书中进一步证明前一箭头为 epi，并等于 coker(ker f)，从而得到规范的 coim→im 分解。

## Key Takeaways
1. Abel 范畴优先使用 kernel/cokernel 语言。
2. 任意态射有规范 epi–mono 分解。
3. mono/epi 可用零 kernel/cokernel 快速判断。

## Connects To
- 4.3 exactness 由 im=ker 定义。
- 2.4 pullback 在 Abel 范畴中与正合性强烈互动。
