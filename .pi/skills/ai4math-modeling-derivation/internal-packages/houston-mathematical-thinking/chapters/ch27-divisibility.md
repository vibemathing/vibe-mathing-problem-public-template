# 第27章：除数与整除

## Core Idea
整除问题的首要动作是展开定义：$a\mid b$ 意味着存在整数 k 使 $b=ka$。这把抽象关系转成可代数操作的等式。

## Frameworks Introduced
- **整除展开**：每遇到 $a\mid b$ 就考虑写成 $b=ka$。
- **线性组合闭包**：若 a 同时整除 b,c，则 a 整除任意整数线性组合 $mb+nc$。
- **传递性**：$a\mid b$ 且 $b\mid c$ 可通过两次定义展开得 $a\mid c$。
- **互整除**：$a\mid b$ 且 $b\mid a$ 时得到 $a=\pm b$。
- **最大公因数视角**：gcd 是共同除数中的最大正数；可用保持共同除数集合的变换处理。

## Procedure
1. 把每个 a|b 展开成 b=ka（k 为整数）。
2. 把多个整除事实代入同一代数表达。
3. 要证新的整除，整理出“整数系数×除数”的形式。
4. 对“整除乘积→整除因子”类结论主动检查是否缺素数/互素条件。

## Key Concepts
- **整除**：a|b 表示存在整数 k 使 b=ka。
- **除数**：若 a|b，则 a 是 b 的一个除数。
- **素数**：大于1且正因子只有1和自身的自然数。
- **最大公因数**：同时整除两个整数的最大正整数。
- **线性组合**：形如 ma+nb（m,n 为整数）的组合。
- **互素**：两个整数的 gcd 为1。

## Mental Models
- 数论证明优先“展开定义”，其次才找高级定理。
- 遇到“积被整除”不要随意把整除分配到因子。

## Anti-patterns
- 相信 $n\mid ab$ 必推出 $n\mid a$ 或 $n\mid b$。
- 忘记整数系数条件。

## Worked Example (reconstructed)
从 $a\mid b$、$a\mid c$，写 $b=ra,c=sa$。则 $mb+nc=(mr+ns)a$，且 $mr+ns$ 为整数，所以 a 整除该线性组合。

## Key Takeaways
1. 整除定义是首选接口。
2. 线性组合是核心封闭性。
3. 积的整除需要额外条件。

## Connects To
第28章将这些规则组织成 Euclidean algorithm 与 Bézout；第29章转成同余。

