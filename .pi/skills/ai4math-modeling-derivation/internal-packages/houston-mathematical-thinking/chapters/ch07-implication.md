# 第7章：蕴含

## Core Idea
把 $A\Rightarrow B$ 当作约束：唯一失败情形是 $A$ 真而 $B$ 假。它不自动宣称 $A$ 或 $B$ 实际为真。

## Frameworks Introduced
- **蕴含真值**：$A\Rightarrow B$ 只在“前件真、后件假”时为假。
- **否定蕴含**：$\neg(A\Rightarrow B)\equiv A\land\neg B$。这会直接给出反例的形状。
- **语言翻译**：“若 A 则 B”“B if A”“A only if B”都要按方向精确解析。
- **假设/结论标注**：读定理先把前件标成假设、后件标成结论。

## Procedure
1. 把条件句标准化成 A⇒B，并标出 A、B。
2. 若要判断真假，专找 A 真且 B 假的情形。
3. 若要否定，改写成 A∧¬B。
4. 遇到 if/only if 等自然语言再次核对箭头方向。

## Key Concepts
- **前件**：蕴含 A⇒B 中的 A。
- **后件**：蕴含 A⇒B 中的 B。
- **假设**：证明中可以作为已知使用的前置条件。
- **结论**：需要从假设与已知结果推出的目标陈述。
- **蕴含**：A⇒B；只有 A 真而 B 假时为假。
- **only if**：“A only if B”表达 A⇒B。

## Mental Models
- 想判断一个蕴含是否错，专找“满足 A 但不满足 B”的对象。
- 证明蕴含时从 A 可用信息出发，目标是 B。

## Anti-patterns
- 从 $A\Rightarrow B$ 推断 $B\Rightarrow A$。
- 认为前件为假时整个蕴含也为假。

## Worked Example (reconstructed)
命题“若整数 $n$ 能被4整除，则 $n$ 为偶数”。要推翻它，需要找到“4整除 $n$ 且 $n$ 非偶”的整数；这种对象不存在。寻找“偶但不被4整除”的 $n=2$ 只是在检验逆命题。

## Key Takeaways
1. 先固定蕴含方向。
2. 反例必须满足前件且违反后件。
3. 读“only if”尤其要检查方向。

## Connects To
第8章细化必要/充分与逆否；第9章处理逆命题与等价。

