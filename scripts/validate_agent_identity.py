#!/usr/bin/env python3
"""Fail-closed validation of the required repository identity block."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

IDENTITY_BEGIN = b"<!-- REQUIRED-IDENTITY-BLOCK-BEGIN -->\n"
IDENTITY_END = b"<!-- REQUIRED-IDENTITY-BLOCK-END -->\n"
IDENTITY_HEADER = "# 你的身份（不得执行任何改动）\n".encode("utf-8")
EXPECTED_IDENTITY_SHA256 = "79fbb8baa1d24b4609800a3b5b82cf28bbd87a73c82e5726ba1df6170fc91db4"


def validate(project_root: Path) -> list[str]:
    root = project_root.resolve()
    path = root / "AGENTS.md"
    errors: list[str] = []
    if path.is_symlink() or not path.is_file():
        return ["required regular file missing: AGENTS.md"]
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"cannot read AGENTS.md: {exc}"]

    begin_count = data.count(IDENTITY_BEGIN)
    end_count = data.count(IDENTITY_END)
    if begin_count != 1:
        errors.append(f"required identity begin marker count is {begin_count}, expected 1")
    if end_count != 1:
        errors.append(f"required identity end marker count is {end_count}, expected 1")
    if errors:
        return errors

    payload_start = data.index(IDENTITY_BEGIN) + len(IDENTITY_BEGIN)
    payload_end = data.index(IDENTITY_END)
    if payload_end < payload_start:
        return ["required identity markers are out of order"]
    payload = data[payload_start:payload_end]
    if not payload.startswith(IDENTITY_HEADER):
        errors.append("required identity block header is missing")
    actual = hashlib.sha256(payload).hexdigest()
    if actual != EXPECTED_IDENTITY_SHA256:
        errors.append(
            "required identity block SHA-256 mismatch: "
            f"expected {EXPECTED_IDENTITY_SHA256}, got {actual}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the required AGENTS.md identity block.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(args.project_root)
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "expected_identity_sha256": EXPECTED_IDENTITY_SHA256,
        "errors": errors,
        "file": "AGENTS.md",
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"agent identity gate: {report['decision']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
