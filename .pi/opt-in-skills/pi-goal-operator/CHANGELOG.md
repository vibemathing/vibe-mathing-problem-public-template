# pi-goal-operator Changelog

## 0.1.1 - 2026-09-27

- 增加 Pi 本地安装缓存及维护进程误读存储根的场景：区分固定包安装、Git 忽略的可执行缓存与公开 Harness 源码；安装后仍要运行 `make check-full`，包摘要漂移或被强制跟踪必须停放。不能用另一存储根的空列表推断原 Goal 不存在。
- 回滚：撤销本版文档增量，不改变原有数学 actor、包版本或在线 Hook 防护。

## 0.1.0 - 2026-09-27

### Added
- 单问题 canonical actor 的 Pi Goal 身份核验、唯一调度、恢复和独立数学准入边界。
- 离线压力场景：包声明不等于加载、旧 Hook 护栏未替换、旧 dispatch 不重放、Goal 完成不等于数学闭合。

### Reason
- `pi-goal-x` 是扩展，不属于十个数学 Skills；维护者仍需要可显式加载、可审查的操作说明，不应污染数学 actor 的能力 allowlist。

### Affected
- `SKILL.md`、`references/pressure-tests.md`，及母版 `TEMPLATE_REPOSITORY.md` 中的维护者入口。

### Validation
- 用固定版本插件源码核对命令、调度和设置语义；母版生成与 validator 回归测试及显式 Pi Skill 加载测试在本轮执行。

### Rollback
- 恢复到原先只读 `TEMPLATE_REPOSITORY.md` 的维护方式，移除这个尚未激活的可选 Skill 与源清单中的整树条目；不要改变运行中的 Goal 或 Hook。
