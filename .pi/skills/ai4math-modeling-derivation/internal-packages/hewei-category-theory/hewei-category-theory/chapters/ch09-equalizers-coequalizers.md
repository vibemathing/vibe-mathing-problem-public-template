# 2.2 等值子与余等值子

**Source**: 《范畴论》贺伟，PDF pp. 36–38

## Core Idea
等值子抽取两条平行态射“相等的最大部分”，余等值子把它们强制识别。它们还定义正则 mono/epi。

## Frameworks Introduced
- **Equalizer construction**
  - When to use: 处理 f,g:A→B 的一致部分时
  - How: 找 e:E→A 满足 fe=ge，并让所有 h:X→A 且 fh=gh 唯一经 e 分解。
- **Regularity test**
  - When to use: 需要比 mono/epi 更强的结构信息时
  - How: 问该态射能否表示为某对态射的 equalizer/coequalizer。
- **Degeneracy check**
  - When to use: 要判断 f=g 时
  - How: 若 f,g 的 equalizer 是 epi/iso，或 1_A 本身为 equalizer，可推出 f=g；对偶类推。

## Key Concepts
- equalizer 等值子。
- coequalizer 余等值子。
- regular mono：某个等值子。
- regular epi：某个余等值子。
- Top 中 regular epi 对应商映射。

## Mental Models
- equalizer 是“约束满足对象”；coequalizer 是“施加等价关系”。
- regular 性质记录态射由万有构造产生，而非只有消去律。

## Anti-patterns
- **Avoid**: 把所有 mono 都视为 regular mono。
- **Avoid**: 把 Top 中所有 epi 都视为商映射。

## Worked Example
在 Set 中，f,g:A→B 的等值子可以取 E={a∈A|f(a)=g(a)} 的包含 e:E↪A。任意 h:X→A 若 fh=gh，其像自动落在 E，从而唯一经 e 分解。

## Key Takeaways
1. 平行态射的“相等部分”用 equalizer。
2. 强制两态射相同用 coequalizer。
3. 需要结构稳定性时区分 ordinary 与 regular mono/epi。

## Connects To
- 2.5 完备性可归约到积+等值子。
- 4.1 核是加法环境下 f 与 0 的等值子。
