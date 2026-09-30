#!/usr/bin/env python3
"""Validate fail-closed mathematical knowledge source and operator registries."""
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


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def validate(source_registry: dict[str, Any], operator_registry: dict[str, Any], source_schema: dict[str, Any], operator_schema: dict[str, Any], skills_root: Path) -> list[str]:
    errors = [f"source schema: {message}" for message in schema_errors(source_registry, source_schema)]
    errors.extend(f"operator schema: {message}" for message in schema_errors(operator_registry, operator_schema))

    sources = source_registry.get("sources", [])
    source_ids = [item.get("source_id") for item in sources if isinstance(item, dict)]
    if len(source_ids) != len(set(source_ids)):
        errors.append("duplicate mathematical knowledge source_id")
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id")
        maturity = source.get("maturity")
        status = source.get("operational_status")
        ceiling = source.get("evidence_ceiling")
        license_data = source.get("license", {})
        controls = set(source.get("required_controls", []))
        if status == "design_only" and maturity not in {"surveyed", "source_locked"}:
            errors.append(f"design-only source overstates maturity: {source_id}")
        if status in {"quarantined", "suspended"} and "fresh_replay" not in controls and ceiling == "verifier_input":
            errors.append(f"quarantined verifier input lacks fresh_replay control: {source_id}")
        if license_data.get("status") != "reviewed" and "redistribution" in license_data.get("allowed_uses", []):
            errors.append(f"unreviewed license permits redistribution: {source_id}")
        if not license_data.get("bulk_cache", False) and "bulk_snapshot" in source.get("access_modes", []):
            errors.append(f"source offers bulk_snapshot while bulk_cache is false: {source_id}")
        if ceiling in {"computation_evidence", "verifier_input"} and status == "design_only" and "consumer_required" not in controls:
            errors.append(f"design-only high-ceiling source lacks consumer_required: {source_id}")

    operators = operator_registry.get("operators", [])
    operator_ids = [item.get("operator_id") for item in operators if isinstance(item, dict)]
    if len(operator_ids) != len(set(operator_ids)):
        errors.append("duplicate mathematical knowledge operator_id")
    for operator in operators:
        if not isinstance(operator, dict):
            continue
        operator_id = operator.get("operator_id")
        owner = operator.get("owner_skill")
        if not (skills_root / str(owner) / "SKILL.md").is_file():
            errors.append(f"operator owner Skill does not exist: {operator_id} -> {owner}")
        effect = operator.get("external_effect")
        ceiling = operator.get("evidence_ceiling")
        controls = set(operator.get("requires", [])) | set(operator.get("fail_closed_on", []))
        if effect == "read_network" and ceiling not in {"discovery_only", "candidate_only"}:
            errors.append(f"network search operator exceeds candidate ceiling: {operator_id}")
        if effect in {"bounded_candidate_build", "bounded_candidate_compute"} and "timeout" not in set(operator.get("fail_closed_on", [])):
            errors.append(f"bounded execution operator lacks timeout failure: {operator_id}")
        if ceiling == "verifier_receipt" and "verifier_registry" not in controls and "review_policy" not in controls:
            errors.append(f"verifier-receipt operator lacks verifier/review policy: {operator_id}")
    return errors


def preflight_source_use(
    registry_bytes: bytes, source_id: str, intended_use: str, *, expected_registry_sha256: str
) -> dict[str, Any]:
    """只检查冻结目录项资格，不访问上游、不验证定理、不签发执行权限。"""
    digest = hashlib.sha256(registry_bytes).hexdigest()
    report: dict[str, Any] = {
        "decision": "BLOCK", "source_id": source_id, "intended_use": intended_use,
        "registry_sha256": digest, "authorization_scope": "catalog_metadata_only",
        "claims_ceiling": "candidate_only", "errors": [],
    }
    errors: list[str] = report["errors"]
    if re.fullmatch(r"[a-f0-9]{64}", expected_registry_sha256) is None or expected_registry_sha256 != digest:
        errors.append("来源登记摘要缺失、格式无效或与冻结输入不同")
        return report
    if len(registry_bytes) > 2 * 1024 * 1024:
        errors.append("来源登记超出 2 MiB 上限")
        return report
    try:
        registry = json.loads(registry_bytes)
    except (UnicodeDecodeError, ValueError):
        errors.append("来源登记不是有效 JSON")
        return report
    sources = registry.get("sources") if isinstance(registry, dict) else None
    if not isinstance(sources, list):
        errors.append("来源登记缺少 sources 列表")
        return report
    matches = [item for item in sources if isinstance(item, dict) and item.get("source_id") == source_id]
    if len(matches) != 1:
        errors.append("source_id 不存在或不唯一")
        return report
    source = matches[0]
    license_info = source.get("license")
    if not isinstance(license_info, dict) or not isinstance(license_info.get("allowed_uses"), list):
        errors.append("来源许可记录不完整")
        return report
    report.update({
        "maturity": source.get("maturity"),
        "operational_status": source.get("operational_status"),
        "catalog_evidence_ceiling": source.get("evidence_ceiling"),
    })
    if intended_use not in {"discovery", "local_reference", "query", "build", "redistribution"}:
        errors.append("未知的来源用途")
    elif intended_use not in license_info["allowed_uses"]:
        errors.append("许可未包含所请求的用途")
    if intended_use != "discovery":
        if source.get("operational_status") != "available":
            errors.append("来源尚未可用或已隔离")
        if license_info.get("status") != "reviewed":
            errors.append("来源许可尚未审查通过")
        maturity_order = ("surveyed", "source_locked", "installed", "smoke_checked", "evidence_capable", "verifier_admitted")
        maturity = source.get("maturity")
        required = "installed" if intended_use == "build" else "source_locked"
        if maturity not in maturity_order or maturity_order.index(maturity) < maturity_order.index(required):
            errors.append(f"来源成熟度未达到 {required}")
        modes = source.get("access_modes", [])
        needed = {
            "query": {"http_query"}, "local_reference": {"human_reference", "local_exact"},
            "build": {"git", "local_exact"}, "redistribution": {"git", "bulk_snapshot", "local_exact"},
        }.get(intended_use, set())
        if not isinstance(modes, list) or not needed.intersection(modes):
            errors.append("来源未声明对应的访问方式")
    if not errors:
        report["decision"] = "PASS"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate mathematical knowledge source/operator registries.")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--source-id", help="对已有来源进行只读资格预检")
    parser.add_argument("--use", choices=("discovery", "local_reference", "query", "build", "redistribution"))
    parser.add_argument("--expected-registry-sha256", help="调用方冻结的来源登记原始字节摘要")
    args = parser.parse_args()
    preflight_requested = any((args.source_id, args.use, args.expected_registry_sha256))
    if preflight_requested and not all((args.source_id, args.use, args.expected_registry_sha256)):
        parser.error("--source-id、--use 与 --expected-registry-sha256 必须同时提供")
    root = args.project_root.resolve()
    control = root / "governance/control-plane"
    raw_source = b""
    try:
        raw_source = (control / "math-knowledge-source.v1.json").read_bytes()
        source = json.loads(raw_source)
        operators = json.loads((control / "math-knowledge-operators.v1.json").read_text(encoding="utf-8"))
        source_schema = json.loads((control / "math-knowledge-source.schema.json").read_text(encoding="utf-8"))
        operator_schema = json.loads((control / "math-knowledge-operators.schema.json").read_text(encoding="utf-8"))
        errors = validate(source, operators, source_schema, operator_schema, root / ".pi/skills")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        source = {"sources": []}
        operators = {"operators": []}
    report: dict[str, Any] = {
        "decision": "PASS" if not errors else "BLOCK",
        "sources": len(source.get("sources", [])),
        "operators": len(operators.get("operators", [])),
        "errors": errors,
    }
    if preflight_requested:
        preflight = preflight_source_use(
            raw_source, args.source_id, args.use, expected_registry_sha256=args.expected_registry_sha256
        ) if not errors else {
            "decision": "BLOCK", "source_id": args.source_id, "intended_use": args.use,
            "authorization_scope": "catalog_metadata_only", "claims_ceiling": "candidate_only",
            "registry_sha256": hashlib.sha256(raw_source).hexdigest(), "errors": errors,
        }
        report = {**report, **preflight}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"math knowledge registry: {report['decision']} sources={report['sources']} operators={report['operators']}")
        for error in report["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
