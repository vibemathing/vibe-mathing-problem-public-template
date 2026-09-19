---
name: hewei-category-theory
description: "Operational knowledge base from 贺伟《范畴论》. Use for category-theory study and proof work involving categories, functors, natural transformations, Yoneda, limits/colimits, adjunctions, monads/Beck, additive or Abelian categories, exact sequences, sheaves, or Grothendieck topology; also use when choosing a proof method or locating the relevant section."
---

<!-- argument-hint: [concept, proof goal, problem, or section] -->

# 《范畴论》— 贺伟
**Source**: 科学出版社，2006 | **PDF**: 118 pages | **Sections**: 27 | **Generated**: 2026-09-12

## Use & Route
Use for definitions, proof planning, hypothesis checks, derivations, and section lookup within this book. Load the matching chapter for non-core detail. Topics absent from the book (enriched, higher/∞-, model, derived categories, etc.) require a labeled extension.

Basics → ch01–03 · mono/epi/subobject/projective → ch04–07 · limits/completeness/preservation → ch08–13 · adjoints/reflection/Cartesian closure → ch14–17 · monads/Beck → ch18–19 · Abel/exactness → ch20–22 · sheaves/sites → ch23–27.

## Core Rules
1. **Universal property**: candidate → arbitrary competitor → mediating map → factorization → uniqueness.
2. **Duality**: test `C^op` for initial/terminal, mono/epi, limit/colimit, product/coproduct, pullback/pushout, kernel/cokernel, projective/injective.
3. **Arrow tests**: mono/epi use cancellation; Abel problems use kernels/cokernels or pseudoelements.
4. **Yoneda**: `Nat(C(A,-),F)≅F(A)` via `α↦α_A(1_A)`; representability = object + universal element.
5. **Limits**: arbitrary = products+equalizers; finite = terminal+pullbacks; dualize for colimits.
6. **Adjoints**: hom-bijection → unit/counit → universal arrow/`(A↓G)` → adjoint-functor theorem after every hypothesis is checked.
7. **Monad**: `F⊣G → T=GF → C^T → K`; monadicity → Beck + required coequalizer creation.
8. **Abelian**: `coim(f)=coker(ker f)`, `im(f)=ker(coker f)`; exact at B ⇔ `im(f)=ker(g)`.
9. **Sheaf**: compatible local sections must admit one unique amalgamation; use covers/equalizers or covering sieves/a verified basis.

## Recovery & SELF_CHECK
If elements fail, use universal properties (or pseudoelements in Abel categories). If the target is too rigid, test natural isomorphism/equivalence. Large limit → ch12 generators. Unknown adjoint → comma category. Mono/epi anomaly → cancellation then regularity. Too many covers → verified basis. Missing hypotheses → state “insufficient to conclude” and name them. Before answering, verify target, prerequisites, arrow directions, existence/factorization/uniqueness, duality, category-specific exceptions, and source scope.

## Chapter Index
01 §1.1 范畴 — [load](chapters/ch01-categories.md)  
02 §1.2 函子 — [load](chapters/ch02-functors.md)  
03 §1.3 自然变换/等价 — [load](chapters/ch03-natural-transformations.md)  
04 §1.4 mono/epi — [load](chapters/ch04-mono-epi.md)  
05 §1.5 子对象/商对象 — [load](chapters/ch05-subobjects-quotients.md)  
06 §1.6 Yoneda/表示 — [load](chapters/ch06-yoneda-representable.md)  
07 §1.7 射影/单射 — [load](chapters/ch07-projective-injective.md)  
08 §2.1 极限 — [load](chapters/ch08-limits.md)  
09 §2.2 等值/余等值 — [load](chapters/ch09-equalizers-coequalizers.md)  
10 §2.3 积/余积 — [load](chapters/ch10-products-coproducts.md)  
11 §2.4 拉回/推出 — [load](chapters/ch11-pullbacks-pushouts.md)  
12 §2.5 完备/余完备 — [load](chapters/ch12-completeness.md)  
13 §2.6 保持/反射/产生极限 — [load](chapters/ch13-preserve-reflect-create-limits.md)  
14 §3.1 伴随 — [load](chapters/ch14-adjunctions.md)  
15 §3.2 伴随函子定理 — [load](chapters/ch15-adjoint-functor-theorems.md)  
16 §3.3 反射/余反射 — [load](chapters/ch16-reflective-coreflective.md)  
17 §3.4 Cartesian 闭 — [load](chapters/ch17-cartesian-closed.md)  
18 §3.5 Monad — [load](chapters/ch18-monads.md)  
19 §3.6 Beck — [load](chapters/ch19-beck-monadicity.md)  
20 §4.1 加法范畴 — [load](chapters/ch20-additive-categories.md)  
21 §4.2 Abel 范畴 — [load](chapters/ch21-abelian-categories.md)  
22 §4.3 正合序列 — [load](chapters/ch22-exact-sequences.md)  
23 §5.1 层 — [load](chapters/ch23-sheaf-definition.md)  
24 §5.2 局部同胚/层空间 — [load](chapters/ch24-etale-spaces.md)  
25 §5.3 `Sh(X)` 性质 — [load](chapters/ch25-sheaf-category-properties.md)  
26 §5.4 `f^*/f_*` — [load](chapters/ch26-direct-inverse-image.md)  
27 §5.5 Grothendieck site/sheaf — [load](chapters/ch27-grothendieck-sites-sheaves.md)

## Topic Index
Yoneda/representable → ch06 · limits/pullback/completeness → ch08–13 · adjunction/reflection/CCC → ch14–17 · monad/Beck → ch18–19 · Abel/exactness → ch20–22 · sheaf/sheafification/`f^*/f_*` → ch23–26 · site/sieve/matching family → ch27.

## Supporting Files
[glossary](glossary.md) · [patterns](patterns.md) · [cheatsheet](cheatsheet.md)

## Scope & Limits
Derived from the uploaded 2006 scan. All 118 PDF pages were processed with OCR. Noisy OCR formulas were not copied; consult the source page when exact formula typography matters.
