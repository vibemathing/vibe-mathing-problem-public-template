# Operational Patterns

## 1. Universal-Property Proof
**When to use**: 极限、余极限、表示对象、伴随、初/终对象、层粘合等问题。
**How**:
1. 写清候选对象与结构态射。
2. 验证所需交换关系。
3. 取任意竞争对象/锥/局部数据。
4. 构造中介态射或全局对象。
5. 验证分解。
6. 单独证明唯一性。
**Trade-offs**: 最通用；比元素追踪抽象，但能跨范畴迁移。

## 2. Dualize Once
**When to use**: 已证明关于 mono、limit、product、pullback、initial 等结论，目标是对应的 epi、colimit、coproduct、pushout、terminal 版本。
**How**: 转到 C^op，反转箭头与复合次序，逐项替换成对偶概念；检查命题没有依赖额外非对偶结构。
**Trade-offs**: 极省证明；需要严守箭头方向。

## 3. Yoneda Reduction
**When to use**: 出现 hom 函子、自然变换、表示性、通用元素。
**How**: 把 Nat(C(A,-),F) 化为 F(A)，用 α_A(1_A) 记录全部自然变换；反向用 F(f)(x) 重建。
**Trade-offs**: 把高阶自然性问题降成元素/态射问题；前提是形状确实为 representable。

## 4. Build General Limits from Generators
**When to use**: 证明完备性或某函子保持极限。
**How**: 任意极限用 products + equalizers；有限极限可用 terminal + pullbacks。余极限全部对偶。
**Trade-offs**: 将“所有图”压成少数测试；必须匹配有限/任意范围。

## 5. Adjoint Search Ladder
**When to use**: 需要证明 G 有左伴随或 F 有右伴随。
**How**:
1. 直接变形 hom 集并检查双变量自然性。
2. 构造 unit/counit 并验三角恒等式。
3. 构造通用箭头；等价地找 (A↓G) 初始对象。
4. 若显式构造失败，再核对广义/特殊伴随函子定理的全部假设。
**Trade-offs**: 从具体到抽象逐级升级，避免过早调用重型存在定理。

## 6. Reflection/Coreflection Approximation
**When to use**: “把对象最佳地逼近到某满子范畴”。
**How**: 反射构造 C→D_C 并验证到任意 D∈D 的唯一分解；余反射反向。随后利用伴随推断极限/余极限闭包。
**Trade-offs**: 给出规范近似；必须有真正万有性。

## 7. Monad–Beck Pipeline
**When to use**: 自由/遗忘型伴随，想知道结构能否完全由 monad 恢复。
**How**: F⊣G → T=GF → Eilenberg–Moore C^T → comparison K。要证 K 同构时，优先检查 Beck：G 是否产生指定 split/absolute coequalizers。
**Trade-offs**: 能把“结构范畴”重构为代数；Beck 的 coequalizer 条件需逐项确认。

## 8. Biproduct Matrix Calculus
**When to use**: 加法范畴中的有限对象族与态射计算。
**How**: 用投影 p_j 与余投影 q_i 取矩阵分量 f_{ji}=p_jfq_i；加法和复合按矩阵规则组织。
**Trade-offs**: 计算直接；仅在加法/双积环境使用。

## 9. Abelian Kernel–Cokernel Factorization
**When to use**: Abel 范畴中分析任意 f:A→B。
**How**: im(f)=ker(coker f)，coim(f)=coker(ker f)，得到 f=im-part ∘ coim-part，其中前段 epi、后段 mono。mono/epi 可分别用 ker(f)=0、coker(f)=0 判定。
**Trade-offs**: 是正合性与图追踪的主接口；离开 Abel 假设后需重新验证。

## 10. Exactness Diagnostic
**When to use**: 序列、短正合列、函子正合性。
**How**: 在 B 处检查 im(f)=ker(g)，并先确认 gf=0。函子左正合看 kernels/有限极限；右正合看 cokernels/有限余极限；需要抽象元素追踪时用 pseudoelements。
**Trade-offs**: 比普通元素追踪更普适；pseudoequality 的定义不可省略。

## 11. Sheaf Gluing Test
**When to use**: 判断 presheaf 是否为 sheaf。
**How**: 对覆盖 {U_i} 检查 matching：交叠限制一致；再证明存在唯一 s∈F(U) 限制到 s_i。需要范畴化时写成 equalizer。
**Trade-offs**: 直接；覆盖很多时改用 topology basis。

## 12. Étale-Space Translation
**When to use**: 层的几何解释、sheafification、inverse image。
**How**: sheaf/presheaf → germs 组成 A_F→X；局部同胚 p:Y→X → 局部截面层 Θ_p。对 sheaf 与 local homeomorphism，unit/counit 成同构。
**Trade-offs**: 几何直观强；一般 presheaf 需经 sheafification 才回到层。

## 13. Site Matching-Family Test
**When to use**: Grothendieck topology / site 上的层。
**How**: 若给 covering sieve，按筛定义检查兼容族与唯一粘合；若给 Grothendieck basis，只对基中覆盖族及其 pullback 交叠检查 matching family。
**Trade-offs**: basis 大幅减少检查量；必须先证明 basis 公理。
