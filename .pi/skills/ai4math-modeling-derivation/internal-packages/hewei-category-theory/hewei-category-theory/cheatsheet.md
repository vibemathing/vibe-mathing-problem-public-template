# Decision Cheatsheet

| 信号 | 路线 | 关键检查 | 章 |
|---|---|---|---|
| 范畴/函子？ | 公理清单 | 单位、复合 | 01–02 |
| 自然同构/等价？ | 自然性；full+faithful+本质满射 | 每个方形 | 03 |
| mono/epi？ | 消去律 | concrete 直觉另证 | 04 |
| 子对象/商/唯一对象 | mono/epi 同构类+万有性 | 唯一到同构 | 05 |
| hom 函子/自然变换 | Yoneda | `α_A(1_A)` | 06 |
| lift/extend | projective/injective | epi/mono 量词 | 07 |
| 极限 | 锥→中介→唯一 | 竞争锥 | 08 |
| 平行态射一致 | equalizer/coequalizer | regularity | 09 |
| 多分量 | product/coproduct | 分量万有性 | 10 |
| 纤维积/逆像 | pullback | 交换+唯一分解 | 11 |
| 完备性 | products+equalizers | 有限/任意 | 12 |
| 函子与极限 | preserve/reflect/create | 强度分级 | 13 |
| 找伴随 | hom→unit/counit→comma | 前提 | 14–15 |
| 最佳子范畴逼近 | reflection/coreflection | 包含函子伴随 | 16 |
| 函数对象 | Cartesian closed | `A×-` 右伴随 | 17 |
| 自由-遗忘 | monad/EM | `η,μ,T`-algebra | 18 |
| monadic? | Beck | split coequalizers | 19 |
| 态射可加 | biproduct | 双线性、零对象 | 20 |
| Abel 中的 f | ker/coker→coim/im | 规范分解 | 21 |
| 正合性 | `im=ker` | `gf=0` 仍不够 | 22 |
| 局部拼接 | sheaf | 存在+唯一 | 23 |
| 层几何/层化 | étalé space | local homeomorphism | 24 |
| Sh(X) 结构 | pointwise/Ω/internal hom | sheaf 条件 | 25 |
| 连续映射与层 | `f^*⊣f_*` | pullback 模型 | 26 |
| 广义覆盖 | site+sieve+matching | 三条拓扑公理 | 27 |

## Recovery
元素追踪卡住→万有性质；严格目标过强→自然同构/等价；极限太大→生成定理；伴随猜不到→comma category；mono/epi 异常→消去律/regular；覆盖太多→basis；monadicity→Beck。
