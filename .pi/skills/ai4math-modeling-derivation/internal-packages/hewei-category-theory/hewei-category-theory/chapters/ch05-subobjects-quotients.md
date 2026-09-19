# 1.5 子对象与商对象

**Source**: 《范畴论》贺伟，PDF pp. 24–26

## Core Idea
子对象与商对象以 mono/epi 的同构类来编码“包含/商”的范畴化版本，并形成偏序结构；初始、终对象和分离子提供极端与探针。

## Frameworks Introduced
- **Subobject ordering**
  - When to use: 比较 A 的两个子对象时
  - How: 用是否存在使三角形交换的态射定义 ≤；随后按同构类理解反对称性。
- **Universal-object uniqueness**
  - When to use: 证明初始/终对象唯一时
  - How: 利用唯一态射双向构造，复合必须等于单位，得到唯一同构。
- **Separator test**
  - When to use: 需要区分两个态射 f,g:A→B 时
  - How: 从分离集中的对象 S 找 h:S→A，使 fh≠gh；对偶使用余分离集。

## Key Concepts
- M-子对象：由指定 mono 类定义的子对象。
- Sub(A)：A 的子对象偏序。
- 良幂范畴 well-powered：每对象的子对象类为集合。
- 终对象/初始对象：唯一入箭头/出箭头。
- 商对象：epi 的同构类。
- 余良幂范畴：商对象形成集合。
- 分离子/余分离子：检测态射相等的探针。

## Mental Models
- “子集”在抽象环境中换成 mono 的等价类；“商集”换成 epi 的等价类。
- 唯一性结论常为“唯一到同构”。

## Anti-patterns
- **Avoid**: 把 Top 的任意子对象等同于固定的子空间拓扑。
- **Avoid**: 把 epi 商对象自动当成具体商拓扑或普通商结构。

## Worked Example
若 T 与 P 都是终对象，则有唯一 f:T→P 与 g:P→T。由于 T→T、P→P 各只有一个态射，gf=1_T、fg=1_P，于是 f 是同构。这一套路贯穿极限、表示对象等大量“唯一到唯一同构”证明。

## Key Takeaways
1. 子对象/商对象应在同构类上比较。
2. 初始/终对象的唯一性是通用证明模板。
3. 遇到态射相等问题，可尝试 separator。

## Connects To
- 2.1 极限：终对象成为空图极限。
- 5.3 子对象分类子：把子对象编码为特征态射。
