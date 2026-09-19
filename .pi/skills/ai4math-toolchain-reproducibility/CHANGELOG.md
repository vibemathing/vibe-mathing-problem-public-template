# Changelog

## 1.0.0

- Rename and adapt the existing public capability as the Pi-native `ai4math-toolchain-reproducibility` owner Skill.
- Preserve candidate-only evidence ceilings and repository-local references.

## 0.2.0-web-adaptation - 2026-09-05

- 以计算容器观察到的 `ai4math-toolchain-reproducibility` 0.2.0 薄入口为来源。
- 删除对节点命令、全局 `auto-governance` 和 `auto-tasks` 的运行时依赖。
- Web 状态固定为 constrained：只生成版本锁定、有界、candidate-only 的 ToolPlan，不执行工具或签发证据。
- 路由改为仓库固有的六个数学 Skills、`solve` 与数学知识 registry。
