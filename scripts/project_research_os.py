#!/usr/bin/env python3
# 做什么：只读生成或验证 Research OS candidate-only metadata projection。
# 怎么运行：python3 scripts/project_research_os.py --project-root . [--ledger PATH] [--stored PATH]
# 需要什么：项目 owner ledger、Research OS event/projection schema，以及 jsonschema 依赖。

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from vibe_mathing.research_os import ResearchOsError, ResearchOsProjector, validate_projection  # noqa: E402


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _project_path(root: Path, requested: str) -> Path:
    path = Path(requested)
    if path.is_absolute():
        resolved = path.absolute()
    else:
        if ".." in path.parts:
            raise ResearchOsError(f"path cannot contain '..': {requested}")
        resolved = (root / path).absolute()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ResearchOsError(f"path escapes project root: {requested}") from exc
    return resolved


def _read_stored_projection(root: Path, requested: str) -> dict[str, Any]:
    path = _project_path(root, requested)
    if path.is_symlink() or not path.is_file():
        raise ResearchOsError(f"stored projection must be a regular file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ResearchOsError(f"stored projection is not finite JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ResearchOsError("stored projection must be a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="只读 Research OS projection 生成/验证器")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--ledger", default="research/records/research-os-events.jsonl")
    parser.add_argument("--stored", help="验证一个已保存 projection；不提供时输出新 projection")
    parser.add_argument("--pretty", action="store_true", help="以缩进 JSON 输出生成的 projection")
    args = parser.parse_args(argv)

    try:
        root = args.project_root.expanduser().resolve()
        projector = ResearchOsProjector(root)
        expected = projector.project_file(_project_path(root, args.ledger))
        if args.stored:
            stored = _read_stored_projection(root, args.stored)
            errors = validate_projection(stored, expected, projector.schema)
            if errors:
                for error in errors:
                    print(f"BLOCK: {error}", file=sys.stderr)
                return 2
            print(json.dumps({"status": "PASS", "projection_sha256": expected["projection_sha256"]}, sort_keys=True))
            return 0
        print(json.dumps(expected, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
        return 0
    except (OSError, ResearchOsError, ValueError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
