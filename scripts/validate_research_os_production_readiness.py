#!/usr/bin/env python3
# 做什么：校验公开问题模板的 Research OS 能力 profile、边界和 Makefile 接线。
# 怎么运行：python3 scripts/validate_research_os_production_readiness.py --strict
# 需要什么：项目根、Research OS profile/schema；只读，不写任何研究账本。
"""Validate the public-template Research OS profile without side effects."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "research/research-os-profile.v1.json"
DEFAULT_SCHEMA = ROOT / "research/schema/research-os-profile.v1.schema.json"
PATH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
FORBIDDEN_PATH_PARTS = {".git", ".private", "runtime", "__pycache__"}
FORBIDDEN_COMMAND_MARKERS = (
    "password",
    "secret",
    "access_token",
    "api_key",
    "curl ",
    "wget ",
    "http://",
    "https://",
)
RESEARCH_OS_CHECK_COMMANDS = (
    "python3 scripts/validate_research_os_production_readiness.py --strict",
    "python3 scripts/test_validate_research_os_production_readiness.py",
    "python3 scripts/validate_research_os_metadata.py --strict",
    "python3 scripts/test_validate_research_os_metadata.py",
    "python3 scripts/validate_research_os_working_set.py",
    "python3 scripts/test_validate_research_os_working_set.py",
    "python3 scripts/validate_research_os_events.py",
    "python3 scripts/test_validate_research_os_events.py",
    "python3 scripts/test_research_os_runtime.py",
)


class ProductionReadinessError(RuntimeError):
    """Raised when a Research OS profile cannot be inspected safely."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path, label: str) -> Any:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ProductionReadinessError(f"{label} must be a regular file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ProductionReadinessError(f"{label} is not valid JSON: {exc}") from exc


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_relative(raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        return None
    path = Path(raw)
    if path.is_absolute() or path == Path(".") or raw != path.as_posix() or ".." in path.parts:
        return None
    if not PATH_RE.fullmatch(raw):
        return None
    return path


def _resolve_regular(root: Path, raw: Any) -> tuple[Path | None, str | None]:
    relative = _safe_relative(raw)
    if relative is None:
        return None, "path must be a safe relative POSIX path"
    if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts):
        return None, "path contains a forbidden private/runtime component"
    target = root / relative
    try:
        resolved_root = root.resolve()
        resolved = target.resolve(strict=False)
        if not resolved.is_relative_to(resolved_root):
            return None, "path escapes project root"
        current = resolved_root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                return None, "path component is a symlink"
    except OSError as exc:
        return None, f"path resolution failed: {exc}"
    if not target.is_file() or target.is_symlink():
        return None, "path is missing or not a regular file"
    return target, None


def schema_errors(value: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema:{'/'.join(str(part) for part in issue.absolute_path) or '<root>'}: {issue.message}"
        for issue in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def semantic_errors(value: dict[str, Any], root: Path, strict: bool = False) -> list[str]:
    errors: list[str] = []
    if value.get("claim_boundary") != "candidate_only_no_mathematical_truth":
        errors.append("claim_boundary must remain candidate_only_no_mathematical_truth")
    if value.get("status") not in {"pilot", "blocked", "not_ready"}:
        errors.append("status must describe a pilot or non-ready profile")
    if value.get("problem_scope") != "single_problem_contract":
        errors.append("problem_scope must remain single_problem_contract")

    capabilities = value.get("capabilities", [])
    capability_ids = [item.get("capability_id") for item in capabilities]
    if len(capability_ids) != len(set(capability_ids)):
        errors.append("duplicate capability_id")
    source_paths: set[str] = set()
    for capability in capabilities:
        capability_id = capability.get("capability_id")
        source = capability.get("source")
        if source in source_paths:
            errors.append(f"duplicate capability source: {source}")
        source_paths.add(str(source))
        target, path_error = _resolve_regular(root, source)
        if path_error:
            errors.append(f"{capability_id}: source is not readable: {path_error}: {source}")
        elif target is not None and sha256(target) != capability.get("source_sha256"):
            errors.append(f"{capability_id}: source digest drift: {source}")
        if capability.get("evidence_ceiling") not in {"candidate_only", "control_plane_only"}:
            errors.append(f"{capability_id}: invalid evidence ceiling")
        if capability.get("status") != "implemented_isolated":
            errors.append(f"{capability_id}: only implemented_isolated capabilities may be listed")
        for command in capability.get("validation_commands", []):
            lowered = command.lower()
            if any(marker in lowered for marker in FORBIDDEN_COMMAND_MARKERS):
                errors.append(f"{capability_id}: validation command has network/credential marker")

    deferred = value.get("deferred_capabilities", [])
    deferred_ids = [item.get("capability_id") for item in deferred]
    if len(deferred_ids) != len(set(deferred_ids)):
        errors.append("duplicate deferred capability_id")
    overlap = sorted(set(capability_ids) & set(deferred_ids))
    if overlap:
        errors.append(f"capability cannot be implemented and deferred: {overlap}")

    gates = value.get("gates", [])
    gate_ids = [gate.get("gate_id") for gate in gates]
    if len(gate_ids) != len(set(gate_ids)):
        errors.append("duplicate gate_id")
    for gate in gates:
        if gate.get("status") == "met":
            errors.append(f"{gate.get('gate_id')}: met is not a trusted status")
    boundary = next((gate for gate in gates if gate.get("gate_id") == "gate.math-truth-boundary"), None)
    if boundary is None:
        errors.append("mathematical truth boundary gate is missing")
    elif boundary.get("status") != "enforced":
        errors.append("mathematical truth boundary gate must remain enforced")

    commands = value.get("validation_commands", [])
    if list(commands) != list(RESEARCH_OS_CHECK_COMMANDS):
        errors.append("validation_commands must match the public Research OS check contract")
    makefile = root / "Makefile"
    if not makefile.is_file() or makefile.is_symlink():
        errors.append("Makefile must be a regular file")
    else:
        try:
            text = makefile.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"Makefile cannot be read: {exc}")
        else:
            positions: list[int] = []
            for command in RESEARCH_OS_CHECK_COMMANDS:
                position = text.find(command)
                if position < 0:
                    errors.append(f"Makefile is missing Research OS command: {command}")
                else:
                    positions.append(position)
            if positions != sorted(positions):
                errors.append("Makefile Research OS command order drift")
            if "check-research-os:" not in text:
                errors.append("Makefile is missing check-research-os target")

    for claim in value.get("non_claims", []):
        lowered = claim.lower()
        if not any(token in claim or token in lowered for token in ("candidate_only", "不", "不得", "禁止", "not ", "no ", "cannot")):
            errors.append("non_claims must state an explicit non-claim")
    if strict and value.get("status") == "ready":
        errors.append("Research OS profile cannot self-promote to ready")
    return errors


def validate_document(value: dict[str, Any], schema: dict[str, Any], root: Path, strict: bool = False) -> list[str]:
    errors = schema_errors(value, schema)
    if not errors:
        errors.extend(semantic_errors(value, root, strict=strict))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the public-template Research OS capability profile.")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    root = args.project_root.expanduser().resolve()
    try:
        value = load_json(args.contract, "Research OS profile")
        schema = load_json(args.schema, "Research OS profile schema")
        errors = validate_document(value, schema, root, strict=args.strict)
    except (OSError, ProductionReadinessError, ValueError) as exc:
        value = None
        errors = [str(exc)]
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "profile": str(args.contract),
        "status": value.get("status") if isinstance(value, dict) else None,
        "errors": errors,
        "claim_boundary": "candidate_only_no_mathematical_truth",
    }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"Research OS public profile: {report['decision']} status={report['status']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
