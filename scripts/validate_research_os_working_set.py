#!/usr/bin/env python3
"""Validate a candidate-only Mathematical Research OS working-set projection.

The working set records research cognition across seven functions, but it is
not a Problem, Evidence, Result, Solution, or execution ledger.  Validation is
structural and reference-oriented; it never starts research or mutates a
truth-plane ledger.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "research" / "schema" / "research-os-working-set.v1.schema.json"
DEFAULT_FIXTURE = ROOT / "fixtures" / "research-os" / "valid-working-set.json"

LOCAL_PREFIXES = {
    "example",
    "conjecture",
    "refutation",
    "connection",
    "verification",
}
FORBIDDEN_STATUS_VALUES = {"admitted", "closed", "result", "solution"}


class WorkingSetError(RuntimeError):
    """Raised when the working-set input cannot be inspected safely."""


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def load_json(path: Path, label: str = "JSON") -> Any:
    """Load one regular UTF-8 finite JSON file without following symlinks."""
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise WorkingSetError(f"{label} must be a regular file: {path}")
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), parse_constant=_reject_constant
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise WorkingSetError(f"{label} is not valid finite JSON: {exc}") from exc


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    return [
        f"schema at {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def _prefix(value: str) -> str:
    return value.split(":", 1)[0] if ":" in value else ""


def _duplicate_ids(items: list[dict[str, Any]], field: str, label: str) -> list[str]:
    counts = Counter(item.get(field) for item in items if isinstance(item, dict))
    return [f"duplicate {label}: {item_id}" for item_id, count in sorted(counts.items()) if count > 1]


def _local_ids(graph: dict[str, Any]) -> dict[str, set[str]]:
    return {
        "example": {item["example_id"] for item in graph.get("examples", [])},
        "conjecture": {item["conjecture_id"] for item in graph.get("conjectures", [])},
        "refutation": {item["refutation_id"] for item in graph.get("refutations", [])},
        "connection": {item["connection_id"] for item in graph.get("connections", [])},
        "verification": {item["verification_id"] for item in graph.get("verification", [])},
        "obligation": {item["obligation_ref"] for item in graph.get("proof_dependencies", [])},
    }


def _check_local_ref(
    value: str,
    local: dict[str, set[str]],
    owner: str,
    errors: list[str],
) -> None:
    prefix = _prefix(value)
    if prefix in local and value not in local[prefix]:
        errors.append(f"{owner} references unknown local ID: {value}")


def _semantic_errors(working_set: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if working_set.get("claims_ceiling") != "candidate_only":
        errors.append("working set claims ceiling must remain candidate_only")

    all_items: list[tuple[str, str]] = []
    sections = (
        ("examples", "example_id"),
        ("conjectures", "conjecture_id"),
        ("refutations", "refutation_id"),
        ("connections", "connection_id"),
        ("verification", "verification_id"),
        ("proof_dependencies", "obligation_ref"),
    )
    for section, field in sections:
        items = working_set.get(section, [])
        errors.extend(_duplicate_ids(items, field, field))
        for item in items:
            value = item.get(field)
            if isinstance(value, str):
                all_items.append((value, section))

    counts = Counter(item_id for item_id, _ in all_items)
    for item_id, count in sorted(counts.items()):
        if count > 1:
            sections_for_id = sorted(section for value, section in all_items if value == item_id)
            errors.append(f"duplicate working-set identity across sections: {item_id} ({','.join(sections_for_id)})")

    local = _local_ids(working_set)
    frame = working_set.get("frame", {})
    for ref in frame.get("obligation_refs", []):
        if _prefix(ref) != "obligation":
            errors.append(f"frame obligation_refs must use obligation IDs: {ref}")
        _check_local_ref(ref, local, "frame", errors)
    for ref in frame.get("definition_refs", []):
        _check_local_ref(ref, local, "frame definition_refs", errors)

    for example in working_set.get("examples", []):
        for ref in example.get("source_refs", []):
            _check_local_ref(ref, local, f"example {example.get('example_id')} source_refs", errors)

    for conjecture in working_set.get("conjectures", []):
        for ref in conjecture.get("origin_refs", []):
            _check_local_ref(ref, local, f"conjecture {conjecture.get('conjecture_id')} origin_refs", errors)
        if conjecture.get("status") in FORBIDDEN_STATUS_VALUES:
            errors.append(f"conjecture cannot claim terminal/admitted status: {conjecture.get('conjecture_id')}")

    for dependency in working_set.get("proof_dependencies", []):
        for ref in dependency.get("dependency_refs", []):
            if _prefix(ref) != "obligation":
                errors.append(
                    f"proof dependency references a non-obligation dependency: {dependency.get('obligation_ref')}/{ref}"
                )
            _check_local_ref(ref, local, f"proof dependency {dependency.get('obligation_ref')}", errors)

    for refutation in working_set.get("refutations", []):
        target_ref = refutation.get("target_ref")
        if _prefix(target_ref) == "conjecture":
            _check_local_ref(target_ref, local, f"refutation {refutation.get('refutation_id')} target_ref", errors)
        if refutation.get("status") in FORBIDDEN_STATUS_VALUES:
            errors.append(f"refutation cannot claim terminal/admitted status: {refutation.get('refutation_id')}")

    for connection in working_set.get("connections", []):
        source_ref = connection.get("source_ref")
        target_ref = connection.get("target_ref")
        if source_ref == target_ref:
            errors.append(f"connection cannot connect an object to itself: {connection.get('connection_id')}")
        _check_local_ref(source_ref, local, f"connection {connection.get('connection_id')} source_ref", errors)
        _check_local_ref(target_ref, local, f"connection {connection.get('connection_id')} target_ref", errors)
        if connection.get("basis_ref") is not None:
            _check_local_ref(connection["basis_ref"], local, f"connection {connection.get('connection_id')} basis_ref", errors)

    for verification in working_set.get("verification", []):
        status = verification.get("status")
        evidence_refs = verification.get("evidence_refs", [])
        admission_refs = verification.get("admission_refs", [])
        if status == "linked" and not evidence_refs:
            errors.append(
                f"linked verification requires at least one evidence reference: {verification.get('verification_id')}"
            )
        if status == "conflict" and not (evidence_refs or admission_refs):
            errors.append(
                f"conflict verification requires an evidence or admission reference: {verification.get('verification_id')}"
            )
        if status in FORBIDDEN_STATUS_VALUES:
            errors.append(f"verification cannot claim terminal/admitted status: {verification.get('verification_id')}")

    supersedes = working_set.get("supersedes")
    version = working_set.get("record_version")
    reason = working_set.get("supersession_reason")
    if supersedes is None:
        if version != 1:
            errors.append("a working-set version after v1 must supersede an earlier record")
        if reason is not None:
            errors.append("supersession_reason is forbidden when supersedes is null")
    else:
        if version <= 1:
            errors.append("a superseding working-set record must have record_version > 1")
        if supersedes == working_set.get("record_id"):
            errors.append("a working-set record cannot supersede itself")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("supersession_reason is required for a superseding record")

    # Only inspect machine status/ceiling fields.  Human notes may mention
    # Result/Evidence terminology as part of the non-authority explanation.
    def scan_status_fields(value: Any, path: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                if key in {"status", "claims_ceiling"} and child in FORBIDDEN_STATUS_VALUES:
                    errors.append(f"forbidden truth-plane status at {child_path}: {child}")
                scan_status_fields(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                scan_status_fields(child, f"{path}[{index}]")

    scan_status_fields(working_set)
    return errors


def semantic_errors(working_set: dict[str, Any]) -> list[str]:
    """Return semantic errors for a schema-shaped working set."""
    if not isinstance(working_set, dict):
        return ["working set must be a JSON object"]
    return _semantic_errors(working_set)


def validate(
    working_set: dict[str, Any] | Path,
    schema: dict[str, Any] | None = None,
) -> list[str]:
    """Validate schema and fail-closed working-set semantics."""
    if isinstance(working_set, (str, Path)):
        working_set = load_json(Path(working_set), "working set")
    if schema is None:
        schema = load_json(DEFAULT_SCHEMA, "schema")
    if not isinstance(schema, dict):
        raise WorkingSetError("schema must be a JSON object")
    errors = schema_errors(working_set, schema)
    if not errors and isinstance(working_set, dict):
        errors.extend(_semantic_errors(working_set))
    return errors


def validate_file(path: Path, schema_path: Path = DEFAULT_SCHEMA) -> tuple[list[str], dict[str, Any]]:
    working_set = load_json(path, "working set")
    schema = load_json(schema_path, "schema")
    if not isinstance(working_set, dict):
        return ["working set must be a JSON object"], {}
    return validate(working_set, schema), working_set


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a candidate-only Mathematical Research OS working set."
    )
    parser.add_argument("file", nargs="?", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        errors, working_set = validate_file(args.file.resolve(), args.schema.resolve())
    except (OSError, ValueError, WorkingSetError) as exc:
        errors, working_set = [str(exc)], {}
    report = {
        "decision": "PASS" if not errors else "BLOCK",
        "record_id": working_set.get("record_id"),
        "record_version": working_set.get("record_version"),
        "claims_ceiling": working_set.get("claims_ceiling"),
        "examples": len(working_set.get("examples", [])),
        "conjectures": len(working_set.get("conjectures", [])),
        "proof_dependencies": len(working_set.get("proof_dependencies", [])),
        "refutations": len(working_set.get("refutations", [])),
        "connections": len(working_set.get("connections", [])),
        "verification": len(working_set.get("verification", [])),
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(
            "Research OS working set: "
            f"{report['decision']} record={report['record_id']} "
            f"ceiling={report['claims_ceiling']} examples={report['examples']} "
            f"conjectures={report['conjectures']} dependencies={report['proof_dependencies']} "
            f"refutations={report['refutations']} connections={report['connections']} "
            f"verification={report['verification']}"
        )
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
