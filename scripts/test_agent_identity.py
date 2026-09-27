#!/usr/bin/env python3
"""Regression tests for the fail-closed AGENTS.md identity gate."""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

from validate_agent_identity import IDENTITY_BEGIN, IDENTITY_END, validate


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    current = (ROOT / "AGENTS.md").read_bytes()
    errors = validate(ROOT)
    if errors:
        raise AssertionError(f"current identity must pass: {errors}")

    with tempfile.TemporaryDirectory() as directory:
        test_root = Path(directory)
        (test_root / "AGENTS.md").write_bytes(current)
        data = current
        start = data.index(IDENTITY_BEGIN) + len(IDENTITY_BEGIN)
        end = data.index(IDENTITY_END)
        stripped = data[:start] + data[end:]
        (test_root / "AGENTS.md").write_bytes(stripped)
        if not validate(test_root):
            raise AssertionError("missing identity block was accepted")

        (test_root / "AGENTS.md").write_bytes(current[:end - 1] + b"X" + current[end:])
        if not validate(test_root):
            raise AssertionError("modified identity block was accepted")

    print("agent identity tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
