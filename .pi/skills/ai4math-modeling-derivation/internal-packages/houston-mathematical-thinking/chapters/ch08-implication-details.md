# 第8章：蕴含的细节

## Core Idea
必要条件、充分条件、逆命题与逆否命题经常被混淆。把所有自然语言先还原成箭头方向。

## Frameworks Introduced
- **充分条件**：A 对 B 充分意味着 $A\Rightarrow B$。
- **必要条件**：A 对 B 必要意味着 $B\Rightarrow A$。
- **逆命题/逆形式区分**：$A\Rightarrow B$ 的逆命题为 $B\Rightarrow A$；“非A⇒非B”一般也不等价。
- **逆否等价**：$A\Rightarrow B$ 与 $\neg B\Rightarrow\neg A$ 逻辑等价。

## Procedure
1. 把“必要/充分/only if”全部画成箭头。
2. 分别写出原命题、converse、inverse、contrapositive，避免名称混淆。
3. 若直接路线困难，检查 ¬B 是否提供更可操作起点。
4. 只把逆否当作与原命题等价的替代；其余方向独立判断。

## Key Concepts
- **必要**：A 是 B 的必要条件表示 B⇒A。
- **充分**：A 是 B 的充分条件表示 A⇒B。
- **逆命题**：A⇒B 的 converse：B⇒A，需独立判断。
- **逆否命题**：A⇒B 的等价形式 ¬B⇒¬A。
- **逻辑等价**：两个陈述在所有真值情形下具有相同真值。

## Mental Models
- 所有“necessary/sufficient/only if”都先画箭头。
- 直接证明难时查看逆否的起点是否更具体。

## Anti-patterns
- 把必要条件当充分条件。
- 把逆命题当原命题的自动推论。

## Worked Example (reconstructed)
“能被4整除”是“偶数”的充分条件；“偶数”是“能被4整除”的必要条件。反方向“偶数⇒被4整除”失败，因为 $2$ 是反例。

## Key Takeaways
1. 必要条件箭头指向必要条件。
2. 逆否与原命题等价。
3. 逆命题需独立判断。

## Connects To
直接连接第9章和第26章的逆否证明法。

