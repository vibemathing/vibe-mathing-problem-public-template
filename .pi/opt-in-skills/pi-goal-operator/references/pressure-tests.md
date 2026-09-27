# Goal 操作压力场景（离线判据）

## 1. 包已声明、命令却不存在

- 触发：`pi list` 显示固定 npm 包，但离线仓库尚无项目本地缓存。
- 容易犯错：把包声明当作 Goal 已加载，开始依赖它自动续行。
- 正确：核对真实命令注册；受信后安装固定版本，重新核对，不发送研究消息。
- 判定：Goal 未加载时不把旧续行来源移除。

## 1a. 本地安装后 Harness 校验反而 BLOCK

- 触发：Pi 在 `.pi/npm/` 安装项目包并创建嵌套 `.gitignore`，快照核验报告未列入的包文件。
- 容易犯错：把生成的包和嵌套 `.gitignore` 一起提交，或将整个 `.pi/` 排除校验。
- 正确：项目根 `.gitignore` 只排除 `.pi/npm/` 运行缓存；运行 `make check-full`、`make check-release` 并核对固定版包内容摘要、未跟踪状态和命令注册。包字节漂移/缺失时停放并从受信包管理器重装，不改快照掩盖。
- 判定：未安装时 Harness 通过；受审包本地安装后 Harness 仍通过；任意缓存字节漂移或强制跟踪均 BLOCK。

## 1b. 维护进程读错 Goal 存储根

- 触发：维护者另开 `pi --no-session`，但没有继承目标 actor 的 `PI_GOAL_ROOT`，`/goal-list` 显示为空。
- 容易犯错：把空列表当作原 actor 没有 Goal 并再次 `/goal-direct`。
- 正确：用受信运行态对账同一 ProblemContract、session、Goal ID 和仓库外的用户自有 `0700` 非链接存储根；不能证明一致时只停放，不在原 pane 输入。
- 判定：另一个存储根的只读结果不能证明原会话的 Goal 状态。

## 2. HookLoop 已暂停但仍在护栏链上

- 触发：旧 Hook 不再续行，仍承担写保护/历史过滤；Goal 已持有根使命。
- 容易犯错：同时保留两个调度器，或按 `paused` 卸载旧 Hook。
- 正确：保留唯一续行权；替代写保护及过滤先在受控环境通过，再于同一 actor 维护窗口切换。
- 判定：未验证护栏不能宣称切换完成。

## 3. Goal 中断后弹出恢复提示

- 触发：原 session 的调度记录为 `claimed`、`running` 或 `interrupted`。
- 容易犯错：直接确认弹窗、重发 `/goal-direct` 或重复派发旧命令。
- 正确：先拒绝弹窗，对账 Goal ID/session/lease/存储根/保护，查看只读健康与恢复报告，再明确 `/goal-resume`；旧 dispatch 不重放。
- 判定：任何身份漂移都只停放，不新建 canonical actor。

## 4. Goal/auditor 显示完成但根题仍 OPEN

- 触发：插件记录 `complete`，仅见 Lean 子定理或有限计算。
- 容易犯错：据此晋升数学 Result、归档旧数学记录或另开 actor。
- 正确：以独立验证及陈述忠实性为准；未准入则维持根 OPEN，记录运行/数学状态冲突并设计同 actor 的恢复。
- 判定：Goal 状态不能替代数学闭合回执。

## 5. 网络重试用尽

- 触发：`networkRecovery.maxAttempts=3` 后不再自动重试，Goal 仍可能显示 active。
- 容易犯错：把停放当作根题放弃，或对故障提供方反复盲目 `/goal-resume`。
- 正确：检查提供方/会话与 checkpoint，恢复后同 actor 续行；根保持 OPEN。
- 判定：传输重试上限不是数学停止谓词。
