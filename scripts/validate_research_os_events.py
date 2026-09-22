#!/usr/bin/env python3
"""Validate the append-only Mathematical Research OS cognitive event ledger.

This validator proves only event shape, hash-chain integrity, identity binding,
and the non-authoritative candidate-only ceiling.  It never projects or writes
Problem, Candidate, Evidence, Result, or Solution truth.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "research/schema/research-os-event.v1.schema.json"
DEFAULT_LEDGER = ROOT / "fixtures/research-os/valid-events.jsonl"

EVENT_OBJECT_KINDS = {
    "working_set_created": "working_set",
    "example_recorded": "example",
    "conjecture_recorded": "conjecture",
    "proof_dependency_linked": "proof_dependency",
    "refutation_recorded": "refutation",
    "connection_recorded": "connection",
    "verification_linked": "verification",
    "working_set_superseded": "working_set",
}
FORBIDDEN_KEYS = {
    "message",
    "message_text",
    "reasoning",
    "reasoning_text",
    "thinking",
    "tool_arguments",
    "tool_outputs",
    "credential",
    "credentials",
    "access_token",
    "api_key",
    "private_key",
    "cookie",
}


class ResearchOsEventError(RuntimeError):
    """Raised when an event ledger cannot be inspected safely."""


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def load_json(path: Path, label: str = "JSON") -> Any:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ResearchOsEventError(f"{label} must be a regular file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject_constant)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ResearchOsEventError(f"{label} is not valid finite JSON: {exc}") from exc


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def event_digest(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical({key: value for key, value in event.items() if key != "event_sha256"})).hexdigest()


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ResearchOsEventError(f"ledger must be a regular file: {path}")
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line, parse_constant=_reject_constant)
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"line {line_number}: malformed JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {line_number}: event must be an object")
            continue
        rows.append(value)
    return rows, errors


def _walk_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for key, child in value.items():
            result.append(str(key))
            result.extend(_walk_keys(child))
        return result
    if isinstance(value, list):
        result: list[str] = []
        for child in value:
            result.extend(_walk_keys(child))
        return result
    return []


def _timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def validate_events(events: list[dict[str, Any]], schema: dict[str, Any] | None = None) -> list[str]:
    if schema is None:
        schema = load_json(DEFAULT_SCHEMA, "schema")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    previous_digest: str | None = None
    previous_time: datetime | None = None
    event_ids: set[str] = set()
    recorded_objects: set[tuple[str, str]] = set()
    problem_binding: dict[str, Any] | None = None

    for index, event in enumerate(events, 1):
        schema_errors = sorted(validator.iter_errors(event), key=lambda item: list(item.absolute_path))
        for issue in schema_errors:
            path = "/".join(str(part) for part in issue.absolute_path) or "<root>"
            errors.append(f"event {index} schema:{path}: {issue.message}")
        if event.get("sequence") != index:
            errors.append(f"event {index}: sequence must be contiguous")
        event_id = event.get("event_id")
        if isinstance(event_id, str) and event_id in event_ids:
            errors.append(f"event {index}: duplicate event_id: {event_id}")
        if isinstance(event_id, str):
            event_ids.add(event_id)
        if event.get("previous_event_sha256") != previous_digest:
            errors.append(f"event {index}: previous_event_sha256 chain mismatch")
        if event.get("event_sha256") != event_digest(event):
            errors.append(f"event {index}: event_sha256 mismatch")
        previous_digest = event.get("event_sha256") if isinstance(event.get("event_sha256"), str) else None

        try:
            recorded_at = _timestamp(event.get("recorded_at"))
        except (TypeError, ValueError) as exc:
            errors.append(f"event {index}: invalid recorded_at: {exc}")
            recorded_at = None
        if recorded_at is not None and previous_time is not None and recorded_at < previous_time:
            errors.append(f"event {index}: recorded_at regresses")
        if recorded_at is not None:
            previous_time = recorded_at

        if event.get("event_kind") in EVENT_OBJECT_KINDS and event.get("object_kind") != EVENT_OBJECT_KINDS[event["event_kind"]]:
            errors.append(f"event {index}: event/object kind mismatch")
        object_key = (str(event.get("object_kind")), str(event.get("object_id")))
        payload = event.get("payload")
        if isinstance(payload, dict):
            if payload.get("claims_ceiling") != "candidate_only":
                errors.append(f"event {index}: payload claims ceiling is not candidate_only")
            bad_keys = sorted(set(_walk_keys(payload)) & FORBIDDEN_KEYS)
            if bad_keys:
                errors.append(f"event {index}: forbidden content/secret keys: {bad_keys}")
            action = payload.get("action")
            if action == "recorded":
                if object_key in recorded_objects:
                    errors.append(f"event {index}: object recorded more than once without revision: {object_key[1]}")
                recorded_objects.add(object_key)
            if event.get("event_kind") == "working_set_superseded":
                refs = payload.get("refs", [])
                if payload.get("action") != "superseded" or not any(ref.startswith("research-os:") and ref != event.get("object_id") for ref in refs):
                    errors.append(f"event {index}: superseded working set must reference a different research-os record")
            if event.get("event_kind") == "verification_linked" and payload.get("action") == "linked":
                refs = payload.get("refs", [])
                if not any(ref.startswith("evidence-link:") or ref.startswith("admission:") for ref in refs):
                    errors.append(f"event {index}: linked verification must reference evidence-link or admission")

        binding = event.get("problem_contract")
        if isinstance(binding, dict):
            if problem_binding is None:
                problem_binding = binding
            elif binding != problem_binding:
                errors.append(f"event {index}: ProblemContract binding drifts within one ledger")

    return errors


def validate_file(path: Path, schema_path: Path = DEFAULT_SCHEMA) -> tuple[list[str], list[dict[str, Any]]]:
    events, errors = read_jsonl(path)
    schema = load_json(schema_path, "schema")
    errors.extend(validate_events(events, schema))
    return errors, events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a candidate-only Research OS cognitive event ledger.")
    parser.add_argument("file", nargs="?", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        errors, events = validate_file(args.file, args.schema)
    except (OSError, ValueError, ResearchOsEventError) as exc:
        errors, events = [str(exc)], []
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "events": len(events),
        "chain_head_sha256": events[-1].get("event_sha256") if events else None,
        "claims_ceiling": "candidate_only" if events else None,
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"Research OS event ledger: {report['decision']} events={report['events']} chain_head={report['chain_head_sha256']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
