# Pi Goal 维护者 Skill（显式加载）

`pi-goal-operator/` 只教维护者配置、观察和恢复已有数学 actor 的 Goal；它不是数学研究能力、续行调度器或准入 verifier。默认的十个数学 Skills 与 `.pi/settings.json` 不加载它，普通 actor 不应接收这份维护者上下文。

在独立的维护者 Pi 进程中，受信后可显式运行 `pi --no-session --no-skills --skill .pi/opt-in-skills/pi-goal-operator/SKILL.md`，然后输入 `/skill:pi-goal-operator` 阅读方法；这个命令**不**打开已有 canonical session，不创建或恢复 Goal；若未由受信启动环境绑定与目标 actor 相同的 `PI_GOAL_ROOT`，它读到的 `/goal-status` **不能**用于判断原 actor 是否已有 Goal。实际操作者如要进入目标会话，仍须先依据 `TEMPLATE_REPOSITORY.md` 校验身份、lease、调度器、仓库外的私密 Goal 根和原有写保护。不能把维护者 Skill 复制进运行中 actor 的十项数学 Skill allowlist。
