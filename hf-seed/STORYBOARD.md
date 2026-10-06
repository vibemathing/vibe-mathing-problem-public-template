---
format: 1080x1920
duration: 40s
message: "一个 LM head 每步给整个词表打分；时间展开后得到输出空间中的生成轨迹。"
arc: 定义 → 单步快照 → 时间展开 → 采样与准确命名
audience: 想直观理解 LLM 逐 token 解码机制的学习者
mode: autonomous
music: none
---

## Video direction

科研极简竖屏。纸白底，蓝色概率热度，青绿色只表示最终采样。主矩阵占据画面主体；信息按时间逐层出现，避免前 25% 一次性铺满。所有内容保持在上方约 83% 安全区，底部留作序列轨迹区域。无人物、无照片、无装饰性说明框。

## Frame 1 — 一个输出头

- status: animated
- src: compositions/frames/01-lm-head.html
- duration: 8s
- poster: 4s
- transition_in: cut
- scene: 一个 LM head 把隐藏状态映射成整张词表的 logits
- voiceover: ""
- blueprint: compose
- focal: LM HEAD 与 8192 → 128K 映射
- roles: LM HEAD = foreground subject; 8192/128K = supporting; grid = background

Scene 1 (0.0–2.0s): 标题“前沿 LLM 的输出层有几个？”进入；画面只保留问题与一条细网格。
Scene 2 (2.0–4.5s): 中央出现“1 个 LM HEAD”，建立唯一输出投影层概念。
Scene 3 (4.5–6.5s): 左侧隐藏维度 8192、右侧词表维度 ≈128K 由线连接，形成 8192 → 128K。
Scene 4 (6.5–8.0s): 底部结论“每一步：给整个词表打分”出现并保持。

## Frame 2 — 单步输出快照

- status: animated
- src: compositions/frames/02-output-snapshot.html
- duration: 9s
- poster: 4.5s
- transition_in: cut
- scene: 一列固定 token 候选按概率深浅着色，最终选择单独高亮
- voiceover: ""
- blueprint: compose
- focal: 单列 token 概率热度
- roles: token column = foreground subject; probability gradient = supporting; selected cell = foreground subject

Scene 1 (0.0–2.0s): 左侧 token 名单与右侧单列空白概率格进入。
Scene 2 (2.0–5.5s): 概率格由浅到深逐行点亮，不显示具体数值。
Scene 3 (5.5–7.5s): “好”对应格被青绿色描边并高亮，强调“最终采样”。
Scene 4 (7.5–9.0s): 顶部出现“1 个生成步 = 1 张全词表打分表”。

## Frame 3 — 时间展开

- status: animated
- src: compositions/frames/03-time-matrix.html
- duration: 13s
- poster: 7s
- transition_in: cut
- scene: 14 个生成步横向展开成 token × 时间概率矩阵，并形成青绿色采样轨迹
- voiceover: ""
- blueprint: compose
- focal: token × 时间概率矩阵
- roles: heatmap = foreground subject; selected trajectory = foreground subject; vocabulary ellipsis = supporting; coherent sequence = supporting

Scene 1 (0.0–2.5s): 纵向随机 token 与时间轴 t1…t14 建立坐标。
Scene 2 (2.5–7.5s): 概率矩阵按列从左向右逐步出现；每列数值不同，颜色代表当前步完整输出分布。
Scene 3 (7.5–10.0s): 中间“…”省略带出现，旁标“词表总量 ≈128K”，说明只展示少量 token。
Scene 4 (10.0–13.0s): 每列最终采样格被青绿色依次点亮并连成轨迹；底部同步出现连贯 token 序列。

## Frame 4 — 最高概率不等于最终采样

- status: animated
- src: compositions/frames/04-sampling-and-name.html
- duration: 10s
- poster: 5s
- transition_in: cut
- scene: 对比最高概率 token 与实际采样 token，最后给出准确名称
- voiceover: ""
- blueprint: compose
- focal: MAX PROB 与 SAMPLED 的分离
- roles: probability comparison = foreground subject; output-space naming = foreground subject; trajectory = supporting

Scene 1 (0.0–3.0s): 两个候选格出现：深蓝“概率最高”和青绿“最终采样”，位置明确分离。
Scene 2 (3.0–5.5s): 中央出现“sampling ≠ argmax”，说明 temperature/top-p/top-k 下可能选到非最高概率 token。
Scene 3 (5.5–8.0s): 矩阵缩略图与轨迹出现，标题切换为“LLM 输出空间与生成轨迹”。
Scene 4 (8.0–10.0s): 最终定义收束：“每一列 = 一次全词表输出分布；从左到右 = 生成过程。”
