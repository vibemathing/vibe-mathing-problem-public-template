---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "前沿 LLM 通常通过一个 LM head 在每个生成步为整个词表产生 logits/概率；跨时间步展开后，可以观察输出空间中的 token 选择轨迹。"
destination: shorts
aspect: 1080x1920
language: zh-CN
audience: 想直观理解 LLM 逐 token 解码机制的学习者
length: 40s
angle: concept
narration: no
style_preset: cobalt-grid
---

## Intent

把上传的 ChatGPT 对话整理成一个约 40 秒的 9:16 科普解释视频。核心不是泛讲 Transformer，而是把“LM head → 全词表打分 → 每步选择一个 token → 多时间步展开成生成轨迹”讲清楚，并明确区分输出空间与内部状态空间。

## Customizations

- 画面采用科研信息图风格，主视觉是 token × 时间步概率矩阵。
- 单元格不显示具体概率数字，只用由浅到深的填色表示概率大小。
- 最终被采样的 token 用青绿色单独高亮；它可以不是概率最高项。
- 纵向 token 示例要随机、分散，不组成刻意的自然语言序列。
- 中部保留“…”省略带，并标明词表总量约 128K。
- 增加足够多的时间步列，压缩无效空白。
- 矩阵下方显示按生成顺序排列的连贯 token 序列。
- 只保留必要标题、轴标签与关键结论，不添加说明框、脚注式备注或装饰性废话。

## Notes

- 竖屏 1080×1920。
- 蓝色负责概率强度；青绿色负责最终采样轨迹。
- 不使用人物、网站截图或生成式图片；全部视觉由 HTML/CSS/SVG/数据可视化构成。
- 静音成片；不生成旁白、BGM 或字幕轨。
