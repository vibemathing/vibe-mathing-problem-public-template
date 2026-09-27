#!/usr/bin/env python3
"""显式、只读地汇报本地 checkpoint 元数据；绝不签发数学准入。

运行：python3 scripts/report_local_checkpoint.py --checkpoints-dir DIR \
  --problem-id ID --problem-contract-sha256 SHA256
依赖：Python 标准库。失败非零；不读取会话、打印候选正文或清理记录。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

MAX_FILES = 4096
MAX_READ_BYTES = 2 * 1024 * 1024


def inventory(directory: Path) -> tuple[list[tuple[Path, os.stat_result]], int, int]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("checkpoint directory must be a real directory")
    files: list[tuple[Path, os.stat_result]] = []
    total = 0
    with os.scandir(directory) as entries:
        for entry in entries:
            if not entry.name.endswith(".json"):
                continue
            info = entry.stat(follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("checkpoint JSON member is not a regular file")
            files.append((directory / entry.name, info))
            total += info.st_size
            if len(files) > MAX_FILES:
                raise ValueError("checkpoint file count exceeds read-only inventory bound")
    if not files:
        raise ValueError("no checkpoint JSON files")
    files.sort(key=lambda row: (row[1].st_mtime_ns, row[0].name))
    return files[-2:], len(files), total


def read_bound(path: Path, expected: os.stat_result) -> dict:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            expected.st_dev, expected.st_ino, expected.st_size, expected.st_mtime_ns
        ) or before.st_size > MAX_READ_BYTES:
            raise ValueError("checkpoint changed or exceeds per-file read bound")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(MAX_READ_BYTES + 1)
        after = os.fstat(fd)
        if len(data) != before.st_size or (after.st_size, after.st_mtime_ns) != (before.st_size, before.st_mtime_ns):
            raise ValueError("checkpoint changed during read")
        value = json.loads(data)
        if not isinstance(value, dict):
            raise ValueError("checkpoint must be a JSON object")
        return value
    finally:
        os.close(fd)


def report(directory: Path, problem_id: str, contract_sha256: str) -> dict:
    if not problem_id or not re.fullmatch(r"[0-9a-f]{64}", contract_sha256):
        raise ValueError("explicit problem ID and lower-case ProblemContract SHA-256 required")
    selected, count, total = inventory(directory)
    snapshots = [read_bound(path, info) for path, info in selected]
    for row in snapshots:
        if row.get("problem_id") != problem_id or row.get("problem_contract_sha256") != contract_sha256:
            raise ValueError("checkpoint identity does not match the expected ProblemContract")
        if type(row.get("sequence")) is not int or row["sequence"] < 0:
            raise ValueError("checkpoint sequence must be a non-negative integer")
    latest = snapshots[-1]
    previous = snapshots[-2] if len(snapshots) == 2 else None
    if previous is not None and previous["sequence"] >= latest["sequence"]:
        raise ValueError("checkpoint sequence and modification order disagree")
    vector = latest.get("state_vector")
    vector = vector if isinstance(vector, dict) else {}
    math = vector.get("mathematical_state")
    math = math if isinstance(math, dict) else None
    evidence = vector.get("evidence_state")
    evidence = evidence if isinstance(evidence, dict) else {}
    admission = vector.get("admission_state")
    admission = admission if isinstance(admission, dict) else {}
    delta: bool | None = None
    if previous is not None and previous["sequence"] + 1 == latest["sequence"] and math is not None:
        prior = previous.get("state_vector")
        prior = prior.get("mathematical_state") if isinstance(prior, dict) else None
        if isinstance(prior, dict):
            delta = prior != math  # 候选状态变动，不表示可信数学进展。
    event = latest.get("infrastructure_update")
    event = event if isinstance(event, dict) else {}
    event_seq = event.get("recorded_at_sequence")
    if type(event_seq) is not int or event_seq < 0:
        event_seq = None
    if event_seq is not None and event_seq > latest["sequence"]:
        raise ValueError("historical event sequence is in the future")
    return {
        "observation_only": True,
        "evidence_ceiling": "checkpoint metadata; not independent Evidence, Result or Solution",
        "problem_id": problem_id,
        "latest_sequence_by_mtime": latest["sequence"],
        "root_status_reported": math.get("root_status") if math is not None and math.get("root_status") in ("open", "closed") else "unknown",
        "claim_boundary_reported": vector.get("claim_boundary") if vector.get("claim_boundary") in ("candidate_only", "admitted") else "unknown",
        "independent_admission_reported_not_verified": evidence.get("independent_admission") if type(evidence.get("independent_admission")) is bool else None,
        "closure_receipt_reported_not_verified": admission.get("closure_receipt") if type(admission.get("closure_receipt")) is bool else None,
        "mathematical_state_differs_from_adjacent_checkpoint": delta,
        "historical_infrastructure_event": {
            "recorded_at_sequence": event_seq,
            "belongs_to_latest_checkpoint": event_seq == latest["sequence"] if event_seq is not None else None,
        },
        "storage": {"json_files": count, "json_bytes": total, "retention_action": "none"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoints-dir", required=True, type=Path)
    parser.add_argument("--problem-id", required=True)
    parser.add_argument("--problem-contract-sha256", required=True)
    args = parser.parse_args()
    try:
        result = report(args.checkpoints_dir, args.problem_id, args.problem_contract_sha256)
    except (OSError, ValueError, RecursionError) as error:
        print(f"checkpoint report: BLOCK ({type(error).__name__})", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
