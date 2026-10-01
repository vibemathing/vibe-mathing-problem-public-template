---
name: pi-goal-operator
description: "Use when explicitly asked to configure, inspect, migrate, or recover pi-goal-x for one concrete canonical mathematical actor; never as a mathematical research Skill."
disable-model-invocation: true
---

# Pi Goal 维护者操作

本 Skill 只供**独立的维护者进程**显式加载；Pi Goal 是扩展，不是本 Skill。先读仓库根的 `TEMPLATE_REPOSITORY.md` 中 **Local actor continuation** 一节，再读本目录 `references/pressure-tests.md` 中与当前操作相符的场景。只读检查无需进入 actor 会话；本 Skill 不授权创建 actor、选择数学路线或提升 Result。

## When to Use This Skill

- 维护者显式要求排查 Goal 是否加载、观察同一 canonical actor 的状态、审计单调度迁移或恢复中断。
- 无需数学推导；已有十个数学 Skills 的能力路由不经本 Skill。

## Not For / Boundaries

- 不在运行中的数学 actor 自动加载，不发数学路线提示，不代替独立证据准入。
- 不自行创建第二个 actor，不自动接受恢复弹窗，不拆旧 Hook 在线写保护。

## Quick Reference

1. 冻结目标：只处理已准入的单题仓库，回读 ProblemContract 身份/摘要、仓库 cwd、唯一 canonical actor、精确 session/lease 和当前数学 `OPEN`/独立准入状态。仅有窗口标题、Goal 文本或模型自评不够。
2. 核对插件与运行边界：`pi list` 只能证明声明；在**隔离进程**核对 `/goal-status` 是否实际注册及 `pi-goal-x@0.31.9` 是否安装。安装后先执行 `python3 scripts/install_goal_patch.py --project-root . --apply` 及 `--check`（裸上游不包含默认隐藏面板或 `/goal-snapshot`），再运行 `make check-full` 和 `make check-release`；`.pi/npm/` 是 Git 忽略且未跟踪的项目缓存，若内容摘要不符先停放，不把缓存加入快照或用 `git add -f` 发布。检查 `/goal-status verbose` 的有效设置来源：`disableTasks=true`、`autoSelectSingleGoal=false`、`strictExecutionContract=false`、网络重试上限、`maxAutonomousRuns` 未被全局设为 `0`/正数上限。`maxAutonomousRuns` 未设置才是无限自动轮次；不得编造“永不中断”保证。`PI_GOAL_ROOT` 必须绑定仓库外、该问题专用、操作者所有且 `0700` 的绝对真实目录，并在目标会话中固定；拒绝符号链接别名，不得公开此目录或用另一个 root 的空状态冒充原 Goal 不存在。
3. 核对所有续行来源：一个 canonical actor 最多一个续行调度器。迁移旧 HookLoop 时先持久暂停**续行**，再清点它承担的写入保护、历史上下文过滤、恢复与 checkpoint 职责。替代保护须独立验证；`paused` 不等于可卸载。普通词法 Shell 判定不能代替文件系统隔离。
4. 只读观察优先：使用 `/goal-list`、`/goal-status verbose`、`/goal-status health`、`/goal-recovery`；面板默认隐藏不表示 Goal 暂停；`/goal-snapshot` 只在额外配置 sealed-pair owner 时使用，不能代替 `/goal-recovery`。不要用 `/goal-focus` 当作只读检查，因为它会武装续行。Goal 与候选状态永远不能签发 Evidence/Result/Solution。
5. 首次激活仅在**原 actor**且无已有 Goal、身份和保护全过后，执行一次抽象根使命 `/goal-direct`（参照 `TEMPLATE_REPOSITORY.md`）。不得使用 `/sisyphus`、路线分解、lemma、强制 phase、固定 run/token/墙钟配额作为数学闭合代理。旧 Goal 已存在就不要用 `/goal-direct` 覆盖焦点或制造并行 Goal。
6. 中断/复原：重新核对相同 session、Goal ID、lease、cwd、根题及实际保护。启动时若弹出恢复暂停 Goal 的确认，**先拒绝**，完成核查后再用 `/goal-resume`；`claimed/running/interrupted` 旧 dispatch 不会重放。先读取 `/goal-recovery`，`repair` 会改文件，不用于常规观察。Goal 网络重试达到上限只是运行态停放，数学根仍 `OPEN`，恢复前确认提供方健康。
7. 如果 Goal 完成或被归档而独立根闭合仍无新鲜准入回执，记录控制面不一致；不得宣布解题、盲目新建 Goal 或第二 actor。先做独立数学核验和同 actor 的恢复评估。发布前只允许有限来源/候选进入验证侧，Goal auditor 也不是数学 verifier。

本 Skill 只定义操作判断，不执行维护命令或替维护者输入目标 pane。报出观察到的身份、设置来源、Goal 状态、缺失保护、下一安全动作和未完成项；不输出会话正文、私密路径、凭据或历史 Hook 控制消息。

## Examples

### Example 1: 离线声明但命令缺失

`pi list` 已有包而 `/goal-status` 未注册：报告项目缓存缺失，安装固定版本后再复核，不把旧调度卸载。

### Example 2: 旧 Hook 已暂停

Hook `paused` 但仍保护写入：Goal 可独占续行，旧 Hook 在等价护栏通过之前继续加载，不贸然卸载。

### Example 3: 中断后 Goal 请求恢复

先拒绝启动弹窗；对账原 session/lease/Goal/私密根及写边界，再对同一 Goal 显式 `/goal-resume`，不重放 dispatch。

## References

- `references/index.md` — 压力场景索引，细节按需读。
- 根 `TEMPLATE_REPOSITORY.md` — 操作契约和数学边界。
- 固定依赖 `pi-goal-x@0.31.9` 的 README/扩展源码 — 命令及恢复语义的外部真相。

## Maintenance

版本、来源与回滚见本目录 `VERSION` / `CHANGELOG.md`。更新插件固定版本前须重新核对命令、恢复行为、设置解析及原生 Pi 加载，并完成生成仓库的 snapshot/validator 回归；不以本 Skill 升级为由切换在线 actor。
