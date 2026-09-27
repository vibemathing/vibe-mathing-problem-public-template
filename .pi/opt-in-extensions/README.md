# 本地 Pi 扩展（可选）

`local-write-guard.ts` 是通用单问题仓库的**文件工具护栏**，不负责 Goal/Hook 续行、数学策略或 Evidence/Result 准入。它保存在自动发现目录 `.pi/extensions/` **之外**；模板不自动加载它，也不包含任何具体问题、会话、租约或本机路径。运行器只能在审查后的具体 ProblemContract、私密 `0600` 策略文件、准确 session/lease/profile 和固定工具清单均具备时，显式以 `--no-extensions --extension <本文件>` 加载；`VIBEMATH_LOCAL_WRITE_GUARD_POLICY` 指向运行时私密策略，绝不可提交。

策略包含 `schema_version=vibemathing.local-write-guard.v1`、绝对 `repository_root`/`profile_file`、`scope.session_id/lease_epoch/problem_id/problem_contract_sha256/statement_sha256` 和非空的仓库内 `protected_relative_paths`。被保护的目录必须已经存在且可解析；不存在、策略无效、身份漂移时，写工具拒绝。`write/edit` 同时检查词法路径和符号链接落点。

**重要限制**：没有独立的文件系统隔离时，Shell 程序可绕过任何词法路径扫描，所以此扩展对 `bash/powershell` 一律拒绝（包括只读 Shell 命令）。它仅覆盖 Pi 内置 `write/edit/bash/powershell`；未声明的第三方写工具和扩展不在保证范围内。需要 Shell 的本地研究不能靠关闭此拒绝来冒充安全，应先在启动器验证操作系统级只读保护、工具 allowlist 和进程身份，再设计独立升级。`.pi/settings.json` 固定的 `pi-goal-x@0.31.9` 是唯一可选续行调度器，不是 Skill，也不由本护栏启动；实际 `/goal-direct` 与恢复流程见 `TEMPLATE_REPOSITORY.md`。严禁同时启用 HookLoop 续行。旧会话的 Hook 控制消息过滤属于**问题/会话专有迁移**，不写入通用模板。

验证：在母版根执行 `node --experimental-transform-types --test scripts/test_local_write_guard.mjs`；该测试仅作预执行判定，不运行测试字符串里的命令。未通过真实 Pi loader、隔离和恢复演练前，不声明其可替代现役 Hook。
