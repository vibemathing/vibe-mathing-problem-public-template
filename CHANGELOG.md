# 母版变更记录

## 2.3.5 - 候选（2026-10-01）

- `pi-goal-x@0.31.9` MIT 原版与 MIT 项目补丁分别固定摘要；`scripts/install_goal_patch.py` 在官方 Pi 项目安装后仅接受受审前镜像或目标镜像。默认隐藏 Goal 面板但不改变原生续行、Esc/暂停/恢复；`/goal-snapshot` 仅有明确配置时桥接 `sealed-pair-shadow.v1`，母版现存 checkpoint reporter **不**提供兼容 owner。
- `.pi/extensions/goal-context.ts` 默认惰性，显式绑定受信 session/cwd 时保留 Pi 原生 compaction 语义并仅压缩历史文件清单的重复呈现；`scripts/goal_shadow_bridge.py`/`goal_snapshot_store.py` 保存经 owner checksum 与附件字节校验的候选双文档，恢复到新目录，不产生 Evidence/Result。
- `VERSION`、source manifest、snapshot 与同仓历史同步升级；安装/代码、进程已加载及数学准入分别验收。本模板不启动任何研究 actor。
- 候选复核修正：安装器接受文档中的 `--project-root .`，但仍拒绝符号链接/词法越界；协作安装由 advisory lock 协调，源树在 promotion 前再次核对字节及 inode/时间，后半程读回失败会隔离当前镜像并尽力恢复原件。断电双 rename 窗口与非协作 writer 最终窗口有明确人工恢复边界，不宣称事务原子性。

回滚：使用正常 revert PR 回到 2.3.4 快照和补丁前版本；不要删除历史条目或修改运行中的 Goal/会话/研究目录。
