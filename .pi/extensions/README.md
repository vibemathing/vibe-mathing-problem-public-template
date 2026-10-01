# 受信项目的 Pi 上下文扩展

`goal-context.ts` 是唯一自动发现入口；`goal-context-core.mjs` 仅作历史尾部文件清单投影。默认 `VIBE_GOAL_CONTEXT_CONFIG` 不存在时入口直接返回，不注册额外事件或调用模型。显式配置必须绑定受信 Pi 项目、当前 session 和实际仓库 cwd；复用 Pi 原生 `compact` 和 retry、signal、stream、token 计算，绝不裁剪数学正文。项目范围只包含这两个通用文件，不包含 R03 的配置或历史会话。命令和出错边界见根 `TEMPLATE_REPOSITORY.md`。
