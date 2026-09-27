#!/usr/bin/env python3
# 做什么：校验 Research OS metadata envelope 的内容、引用和 candidate-only 边界。
# 怎么运行：python3 scripts/validate_research_os_metadata.py FILE --strict
# 需要什么：metadata-boundary v1 schema；只读，不写数学或运行账本。
"""Fail-closed validator for bounded Research OS metadata envelopes."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "research/schema/research-os-metadata-boundary.v1.schema.json"
DEFAULT_FIXTURE = ROOT / "fixtures/research-os/metadata-boundary-valid.json"
FORBIDDEN_KEYS = {
    "message", "messagetext", "reasoning", "reasoningtext", "thinking",
    "toolarguments", "tooloutputs", "credential", "credentials", "accesstoken",
    "apikey", "privatekey", "cookie", "password", "secret", "prompt",
    "systemprompt", "route", "routedirective", "nextlemma", "nextstep",
    "toolorder", "priority", "microtask", "sendmessage", "continue", "phase",
}
FORBIDDEN_STATUS = {"admitted", "closed", "result", "solution", "solved"}
SENSITIVE_TEXT = (
    re.compile(r"(?i)\b(?:sk|ghp|xox[baprs])-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|secret)\s*[:=]\s*\S+"),
    re.compile(r"(?i)(?:^|[^A-Za-z0-9])-----BEGIN\s+(?:RSA|OPENSSH|EC|PRIVATE)\s+KEY-----"),
)
PROMPT_INJECTION = (
    re.compile(r"(?i)ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions?"),
    re.compile(r"(?i)\b(?:system\s+message|jailbreak|reveal\s+(?:the\s+)?prompt)\b"),
    re.compile(r"(?i)<\s*(?:tool_call|invoke|parameter)\b"),
)
PATH_TEXT = re.compile(r"(?:^|[^A-Za-z0-9])/(?:home|tmp|srv|mnt|etc|var)/|\b[A-Za-z]:\\\\|\\\\\\\\")
MATH_BODY = (
    re.compile(r"\\begin\s*\{\s*(?:proof|theorem|lemma|equation|align)\s*\}"),
    re.compile(r"(?:\$\$|\\\\\[|\\\\\])"),
    re.compile(r"(?i)\b(?:complete|full|detailed)\s+(?:proof|derivation)\b"),
    re.compile(r"(?i)\bq\.e\.d\.?\b"),
)
MATH_SYMBOLS = set("∀∃∧∨⇒⇔≤≥∑∏∫")


class MetadataBoundaryError(RuntimeError):
    """Raised when metadata cannot be safely inspected."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = child
    return value


def load_json(path: Path, label: str = "JSON") -> Any:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise MetadataBoundaryError(f"{label} must be a regular file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise MetadataBoundaryError(f"{label} is not valid JSON: {exc}") from exc


def _schema_errors(value: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema:{'/'.join(str(part) for part in issue.absolute_path) or '<root>'}: {issue.message}"
        for issue in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def _normalized_key(key: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(key).lower())


def _scan_value(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = _normalized_key(key)
            if normalized in FORBIDDEN_KEYS:
                errors.append(f"forbidden metadata key at {path or '<root>'}: {key}")
            _scan_value(child, f"{path}.{key}" if path else str(key), errors)
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _scan_value(child, f"{path}[{index}]", errors)
        return
    if not isinstance(value, str):
        return
    if _normalized_key(value) in FORBIDDEN_KEYS:
        errors.append(f"forbidden metadata token at {path}")
    for pattern in SENSITIVE_TEXT:
        if pattern.search(value):
            errors.append(f"sensitive content marker at {path}")
            break
    for pattern in PROMPT_INJECTION:
        if pattern.search(value):
            errors.append(f"prompt-injection marker at {path}")
            break
    if PATH_TEXT.search(value):
        errors.append(f"private/path marker at {path}")
    if any(pattern.search(value) for pattern in MATH_BODY):
        errors.append(f"mathematical-body marker at {path}")
    if len(value) > 1200:
        errors.append(f"unbounded metadata string at {path}")
    if sum(value.count(symbol) for symbol in MATH_SYMBOLS) >= 3 and len(value) > 160:
        errors.append(f"formula-density marker at {path}")


def semantic_errors(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["metadata envelope must be an object"]
    errors: list[str] = []
    if value.get("claims_ceiling") != "candidate_only":
        errors.append("claims_ceiling must remain candidate_only")
    if value.get("non_authoritative") is not True:
        errors.append("non_authoritative must be true")
    if value.get("non_mathematical_truth") is not True:
        errors.append("non_mathematical_truth must be true")
    status = value.get("status")
    if status in FORBIDDEN_STATUS:
        errors.append(f"forbidden truth-plane status: {status}")
    refs = value.get("refs", [])
    seen_refs: set[str] = set()
    for index, ref in enumerate(refs):
        identity = ref.get("ref")
        if identity in seen_refs:
            errors.append(f"duplicate ref at refs[{index}]: {identity}")
        seen_refs.add(identity)
        if ref.get("trust") == "unowned" and ref.get("observation") == "observed":
            errors.append(f"unowned ref cannot claim observed: refs[{index}]")
    digests = value.get("digests", [])
    digest_names: set[str] = set()
    for index, digest in enumerate(digests):
        name = digest.get("name")
        if name in digest_names:
            errors.append(f"duplicate digest name at digests[{index}]: {name}")
        digest_names.add(name)
    _scan_value(value, "", errors)
    return errors


def validate(value: Any, schema: dict[str, Any] | None = None) -> list[str]:
    if schema is None:
        schema = load_json(DEFAULT_SCHEMA, "schema")
    errors = _schema_errors(value, schema)
    if not errors:
        errors.extend(semantic_errors(value))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate bounded candidate-only Research OS metadata.")
    parser.add_argument("file", nargs="?", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--strict", action="store_true", help="保留 fail-closed 语义；当前版本与默认模式相同")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        value = load_json(args.file, "metadata")
        schema = load_json(args.schema, "schema")
        errors = validate(value, schema)
    except (OSError, MetadataBoundaryError, ValueError) as exc:
        errors = [str(exc)]
        value = None
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "file": str(args.file),
        "claims_ceiling": value.get("claims_ceiling") if isinstance(value, dict) else None,
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"Research OS metadata boundary: {report['decision']} ceiling={report['claims_ceiling']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
