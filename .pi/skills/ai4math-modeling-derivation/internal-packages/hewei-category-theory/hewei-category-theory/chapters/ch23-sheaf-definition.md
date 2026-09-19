# 5.1 层的定义

**Source**: 《范畴论》贺伟，PDF pp. 91–94

## Core Idea
层是开集上的反变函子，附加“局部相容数据可唯一粘合为全局数据”的条件；该条件可写成一个 equalizer。

## Frameworks Introduced
- **Sheaf two-condition test**
  - When to use: 判断 presheaf F 是否为 sheaf 时
  - How: 对覆盖 U=∪U_i：①局部截面在交叠上一致；②存在唯一 s∈F(U) 限制为各 s_i。
- **Equalizer formulation**
  - When to use: 需要范畴化地处理 sheaf 条件时
  - How: 检查 F(U)→∏F(U_i) 是两条到 ∏F(U_i∩U_j) 映射的 equalizer。
- **Pointwise-limit method**
  - When to use: 在 Sh(X) 中计算极限时
  - How: 按每个开集 U 在 Set 中计算，再验证得到的 presheaf 仍满足 sheaf 条件。

## Key Concepts
- presheaf 准层 F:T(X)^op→Set。
- restriction 限制映射。
- sheaf 层。
- gluing 粘合。
- local compatibility 相容性。
- subsheaf 子层。
- Sh(X) 层范畴。

## Mental Models
- 层把“局部可见且相容”升级为“唯一全局对象”。
- sheaf 条件本质是一个 equalizer 万有性质。

## Anti-patterns
- **Avoid**: 只验证局部唯一性，不验证存在性。
- **Avoid**: 只在一类覆盖上检查，却未说明该类是否形成足够的基。

## Worked Example
连续实值函数形成层：若 U=∪U_i，连续函数 f_i:U_i→R 在 U_i∩U_j 上一致，则可逐点定义 f(x)=f_i(x)，相容性保证良定义，局部连续性保证 f 连续，且限制条件保证唯一。

## Key Takeaways
1. 层题固定检查 restriction、相容、存在、唯一。
2. equalizer 形式便于极限论证。
3. Sh(X) 中极限可逐点计算。

## Connects To
- 5.2 把层转成局部同胚空间。
- 5.5 把覆盖从拓扑空间推广到 Grothendieck site。
