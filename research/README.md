# Web Single-Problem Research Space

This directory stores bounded candidate work, verifier/import receipts, and append-only machine records for exactly one ProblemContract. Read the repository root `AGENTS.md` and `research/AGENTS.md` before use.

The Web GPT channel writes only candidate paths admitted by `WEB_CHANNEL_PROFILE.json`. Trusted importers and independent verifiers own EvidenceLink/receipt transitions. Every verifier receipt binds the current registry digest, policy/version digest, replay command/input identity, and a tamper-evident receipt attestation; this is not a substitute for an independent cryptographic signer or human review. Results are derived only after statement-faithful, non-conflicting Obligation DAG closure.

## Research OS（候选认知投影）

本模板还提供一个可选的 Research OS 薄层，用来记录工作集、例子、候选猜想、反驳线索、连接和验证引用。它只保存 metadata 与 typed references，固定 `candidate_only`，不产生数学 Evidence、Result、Solution 或 closure。

运行 `make check-research-os` 可执行 profile、schema、边界、哈希链、WAL 和只读 projection 回归检查。模板中的 `problem:template-placeholder` 是 synthetic draft fixture；具体问题仓必须先替换为自己的 ProblemContract，再启用真实研究记录。

## 来源登记的只读使用预检

已有 `scripts/validate_math_knowledge_registry.py` 除校验目录外，也可对**登记过的来源**执行摘要绑定的只读资格预检。例如：

```sh
registry_sha=$(sha256sum governance/control-plane/math-knowledge-source.v1.json | cut -d' ' -f1)
python3 scripts/validate_math_knowledge_registry.py --project-root . \
  --source-id mathlib-docs-search --use discovery \
  --expected-registry-sha256 "$registry_sha" --json
```

`discovery` 的 PASS 只表示该版本登记项允许**读取目录元数据**；`query`、`build` 等用途还须满足当前登记的许可、成熟度、运行状态和访问模式。不联网、不安装、不运行上游程序；没有新鲜版本/源码/数据快照、重放或独立验证，不能据此证明论文方法可用，更不能把登记中的 `evidence_ceiling` 提升为数学证据。未经登记的论文仍是 opaque 候选，不能以此预检声称已核实。
