---
name: houston-mathematical-thinking
description: "Math proofs, logic, problem solving, and rigorous reasoning."
---

<!-- argument-hint: [problem, proof, concept, or chapter number] -->

# Houston Mathematical Thinking
**Source**: *How to Think Like a Mathematician* / 《如何像数学家一样思考》, Kevin Houston  
**Coverage**: 35 chapters + 3 appendices | **Generated**: 2026-09-12

## When to Use
Use this skill when a task requires mathematical reasoning habits: understand a definition/theorem/proof, solve or debug a proof, choose a proof technique, reason about implication/quantifiers, search for counterexamples, write rigorous mathematics, or reflect/generalize after solving.

Skip it for a bare calculator query, translation, historical/biographical lookup, or requests whose answer does not benefit from mathematical reasoning structure.

## Inputs to Recover
Before working, identify: **goal**, **givens/hypotheses**, **object types/domains**, **definitions in force**, **quantifiers**, **user's current attempt**, and any allowed/forbidden methods. If a missing item affects validity, ask for it or state the assumption.

## Core Operational Loop
1. **Type the task** — classify objects, domains, hypotheses, conclusion, quantifiers.
2. **Unpack definitions** — turn named properties into explicit conditions.
3. **Translate representations** — words ↔ symbols; add a diagram/example when useful.
4. **Probe** — test simple, trivial, extreme and nonexamples; for universal claims, actively seek a counterexample.
5. **Route** — choose the smallest proof/problem-solving method that matches the logical shape.
6. **Execute** — use small justified steps. Backward reasoning may guide discovery; present the final proof in a valid dependency order.
7. **Validate** — re-check theorem preconditions, edge cases, reversibility, domain restrictions, and try an independent example or route.
8. **Write for a reader** — complete sentences, precise symbols, explicit reasons, no decorative equality/implication signs.

## Method Router
| Shape / signal | Route |
|---|---|
| Need to start / generally stuck | Ch5 + Ch32: examples → split into bites → change/specialize problem |
| Universal claim may be false | Ch12: write negation shape and hunt a valid counterexample |
| $A\Rightarrow B$, definitions open a path | Ch20 direct proof |
| $A\Rightarrow B$, $\neg B$ is more concrete | Ch26 contrapositive |
| Nonexistence, irrationality, impossibility | Ch23 contradiction |
| Piecewise/sign/parity/residue alternatives | Ch22 exhaustive cases |
| Natural-number indexed family | Ch24 induction; Ch25 for stronger/multi-step dependence |
| $A\Leftrightarrow B$ | Ch9/20: prove both directions separately |
| Equality | Ch20: simplify, difference 0, two inequalities, or common object |
| Set equality | Ch20: two inclusions |
| Exists + unique | Separate existence and uniqueness; see Ch28/App C |
| Injection / surjection | Ch30: equal outputs→inputs / arbitrary target→construct preimage |
| Equivalence relation | Ch31: reflexive + symmetric + transitive; then check well-definedness |
| Need to expand/learn from result | Ch33: generalize/specialize; Ch34 understanding audit |

## Failure Recovery
If the first route stalls, do not repeat it unchanged. In order: re-open definitions; generate a concrete/extreme example; try to falsify; split the goal; switch words/symbols/picture; work backward from the conclusion and forward from givens; solve a special case; compare direct/contrapositive/contradiction/cases/induction. If a needed hypothesis is absent, stop the method and report the gap.

## SELF_CHECK
Before finalizing: Is the real goal clear? Is the chosen method licensed by the hypotheses? Were all quantifiers and domains respected? Did every cited theorem meet its preconditions? Did any square/divide/cancel/sign step lose reversibility? Are zero/boundary/degenerate cases covered? Is a converse being smuggled in? Can an example or alternate route cross-check the result? Is the written answer rigorous enough for a reader to audit?

## Chapter Index
| # | Chapter | Main use |
|---|---|---|
| [ch01](chapters/ch01-sets-and-functions.md) | 集合和函数 | 集合/函数类型 |
| [ch02](chapters/ch02-reading-mathematics.md) | 阅读数学 | 主动阅读 |
| [ch03](chapters/ch03-writing-mathematics-i.md) | 数学写作 I | 严谨写作 |
| [ch04](chapters/ch04-writing-mathematics-ii.md) | 数学写作 II | 符号/措辞 |
| [ch05](chapters/ch05-problem-solving.md) | 如何解决问题 | Polya/卡住恢复 |
| [ch06](chapters/ch06-statements.md) | 数学陈述 | 陈述/否定 |
| [ch07](chapters/ch07-implication.md) | 蕴含 | 蕴含 |
| [ch08](chapters/ch08-implication-details.md) | 蕴含的细节 | 必要/充分/逆否 |
| [ch09](chapters/ch09-converse-and-equivalence.md) | 逆命题与等价 | converse/iff |
| [ch10](chapters/ch10-quantifiers.md) | 量词：对所有与存在 | 量词顺序 |
| [ch11](chapters/ch11-quantifier-negation.md) | 复杂量词与否定 | 量词否定 |
| [ch12](chapters/ch12-examples-and-counterexamples.md) | 例子与反例 | 例子/反例 |
| [ch13](chapters/ch13-logic-summary.md) | 逻辑总结 | 逻辑路由 |
| [ch14](chapters/ch14-definitions-theorems-proofs.md) | 定义、定理与证明 | 定义/定理/证明角色 |
| [ch15](chapters/ch15-reading-definitions.md) | 如何阅读定义 | 读定义 |
| [ch16](chapters/ch16-reading-theorems.md) | 如何阅读定理 | 读定理 |
| [ch17](chapters/ch17-proofs.md) | 证明 | 证明观 |
| [ch18](chapters/ch18-reading-proofs.md) | 如何阅读证明 | 读/审计证明 |
| [ch19](chapters/ch19-pythagoras-case-study.md) | 毕达哥拉斯定理案例研究 | 定理案例审计 |
| [ch20](chapters/ch20-direct-proof.md) | 证明技术 I：直接方法 | 直接法/等式/集合 |
| [ch21](chapters/ch21-common-errors.md) | 常见错误 | 不可逆操作/常见错 |
| [ch22](chapters/ch22-proof-by-cases.md) | 证明技术 II：分情况 | 分情况/WLOG |
| [ch23](chapters/ch23-contradiction.md) | 证明技术 III：反证法 | 反证 |
| [ch24](chapters/ch24-induction.md) | 证明技术 IV：数学归纳法 | 归纳 |
| [ch25](chapters/ch25-advanced-induction.md) | 更复杂的归纳 | 强归纳 |
| [ch26](chapters/ch26-contrapositive.md) | 证明技术 V：逆否法 | 逆否法 |
| [ch27](chapters/ch27-divisibility.md) | 除数与整除 | 整除 |
| [ch28](chapters/ch28-euclidean-algorithm.md) | 欧几里得算法 | gcd/Euclid/Bézout |
| [ch29](chapters/ch29-modular-arithmetic.md) | 模算术 | 模算术 |
| [ch30](chapters/ch30-functions-and-infinity.md) | 注入、满射、双射与无穷 | 注入/满射/双射/无穷 |
| [ch31](chapters/ch31-equivalence-relations.md) | 等价关系 | 等价关系/良定义 |
| [ch32](chapters/ch32-putting-it-together.md) | 把方法放在一起 | 整合/启动 |
| [ch33](chapters/ch33-generalization-specialization.md) | 泛化与特殊化 | 泛化/特殊化 |
| [ch34](chapters/ch34-true-understanding.md) | 真正的理解 | 理解验收 |
| [ch35](chapters/ch35-biggest-secret.md) | 最大的秘密 | 写作+自造例子 |
| [App A](chapters/app-a-greek-alphabet.md) | 希腊字母 | 符号识别 |
| [App B](chapters/app-b-symbols.md) | 常用符号 | 符号语义 |
| [App C](chapters/app-c-how-to-prove.md) | 如何证明 | 证明目标快速配方 |

## Topic Index
- **定义/读定义** → ch14–15, ch34
- **定理/读定理** → ch16, ch19, ch34
- **证明审计** → ch17–18, ch21, ch34
- **写作** → ch03–04, ch35
- **Polya / 卡住恢复** → ch05, ch32
- **逻辑/蕴含/iff** → ch06–13
- **量词/否定** → ch10–11
- **例子/反例** → ch12, ch32, ch35
- **直接/分情况/反证/归纳/逆否** → ch20–26
- **整除/gcd/Diophantine** → ch27–28
- **模算术** → ch29
- **注入/满射/双射/无穷** → ch30
- **等价关系/商/良定义** → ch31
- **泛化/特殊化/WLOG** → ch22, ch33
- **理解验收** → ch34

## Supporting Files
- [glossary.md](glossary.md) — key terms
- [patterns.md](patterns.md) — operational procedures and failure signals
- [cheatsheet.md](cheatsheet.md) — compact decision aid and self-check

## Scope & Limits
This skill operationalizes the source book's mathematical-learning and proof habits. It does not replace course-specific definitions or theorem statements: when the user's problem supplies a different convention, use the problem's convention and apply this skill as the reasoning process.
