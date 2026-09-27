# Web Single-Problem Research Space

This directory stores bounded candidate work, verifier/import receipts, and append-only machine records for exactly one ProblemContract. Read the repository root `AGENTS.md` and `research/AGENTS.md` before use.

The Web GPT channel writes only candidate paths admitted by `WEB_CHANNEL_PROFILE.json`. Trusted importers and independent verifiers own EvidenceLink/receipt transitions. Every verifier receipt binds the current registry digest, policy/version digest, replay command/input identity, and a tamper-evident receipt attestation; this is not a substitute for an independent cryptographic signer or human review. Results are derived only after statement-faithful, non-conflicting Obligation DAG closure.

## Research OS（候选认知投影）

本模板还提供一个可选的 Research OS 薄层，用来记录工作集、例子、候选猜想、反驳线索、连接和验证引用。它只保存 metadata 与 typed references，固定 `candidate_only`，不产生数学 Evidence、Result、Solution 或 closure。

运行 `make check-research-os` 可执行 profile、schema、边界、哈希链、WAL 和只读 projection 回归检查。模板中的 `problem:template-placeholder` 是 synthetic draft fixture；具体问题仓必须先替换为自己的 ProblemContract，再启用真实研究记录。
