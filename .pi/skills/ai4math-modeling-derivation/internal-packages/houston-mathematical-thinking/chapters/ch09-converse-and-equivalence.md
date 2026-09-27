# 第9章：逆命题与等价

## Core Idea
看到任何蕴含都追问逆命题是否成立；若两个方向都成立，才获得“当且仅当”的等价。

## Frameworks Introduced
- **逆命题检查**：从 $A\Rightarrow B$ 单独考察 $B\Rightarrow A$，不可自动继承真值。
- **双条件**：$A\Leftrightarrow B$ 等价于同时证明 $A\Rightarrow B$ 和 $B\Rightarrow A$。
- **双向证明**：写作时明确分成两个方向，避免一串可逆性不明的变形。

## Procedure
1. 从 A⇒B 明确写出 converse B⇒A。
2. 用简单/极端例子先测试 converse 是否可能为真。
3. 若目标是 iff，固定成两个独立子任务。
4. 两个方向完成后再合并为等价结论。

## Key Concepts
- **逆命题**：A⇒B 的 converse：B⇒A，需独立判断。
- **双条件**：A⇔B，同时包含 A⇒B 与 B⇒A。
- **当且仅当**：iff；两个方向的蕴含都成立。
- **等价**：在指定关系或逻辑意义下满足双向一致性。

## Mental Models
- “iff”默认拆两件事做。
- 一串代数变形只有每一步可逆时才足以证明等价。

## Anti-patterns
- 只证明一个方向就写“iff”。
- 把一个成功例子当作逆命题证明。

## Worked Example (reconstructed)
若要证明“整数 $n$ 为偶数 iff $n^2$ 为偶数”，先证偶 $n$ 推出偶平方；反向可用逆否：若 $n$ 为奇数，则 $n^2$ 为奇数。两个方向合并后才可写 iff。

## Decision Notes
若 converse 被反例推翻，就保留原单向定理，不能强行升级为 iff。若 converse 可信，两个方向可采用完全不同的证明技术；验收标准只看每个方向是否各自闭合。

## Key Takeaways
1. 逆命题独立检查。
2. iff 必须覆盖两个方向。
3. 每个方向可使用不同证明技巧。

## Connects To
第13章汇总逻辑；第20章提供双向证明模板。

