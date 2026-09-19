#!/usr/bin/env python3
"""Validate a candidate-only OSPS plan without executing any search lane."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from collections import deque
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_ROOT / "references" / "osps-plan.schema.json"
BENEFIT_DIMENSIONS = (
    "root_relevance",
    "mathematical_value",
    "semantic_clarity",
    "verification_feasibility",
    "information_gain",
    "route_novelty",
    "reuse_value",
)
COST_DIMENSIONS = ("estimated_cost", "epistemic_risk")
DIMENSIONS = BENEFIT_DIMENSIONS + COST_DIMENSIONS
OBSERVATION_INPUT_KIND = {
    "source_record": "source_refs",
    "semantic_review": "source_refs",
    "failed_route": "failed_route_refs",
    "obligation_state": "obligation_refs",
    "candidate_artifact": "candidate_refs",
    "evidence_state": "evidence_refs",
    "result_state": "result_refs",
    "external_event": "source_refs",
}


class PlanError(RuntimeError):
    pass


def load_json(path: Path, label: str) -> Any:
    if path.is_symlink() or not path.is_file():
        raise PlanError(f"{label} must be a regular file")
    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise PlanError(f"{label} is not valid finite JSON: {exc}") from exc


def schema_errors(instance: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: [str(item) for item in error.absolute_path])
    return [f"schema at {'/'.join(str(item) for item in error.absolute_path) or '<root>'}: {error.message}" for error in errors]


def unique_map(items: list[dict[str, Any]], key: str, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item[key]
        if value in values:
            errors.append(f"duplicate {label}: {value}")
        else:
            values[value] = item
    return values


def normalize_json(value: Any) -> Any:
    """Normalize text and JSON shape for the Skill-local digest policy."""
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [normalize_json(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_json(value[key]) for key in sorted(value)}
    return value


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        normalize_json(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def expected_route_signature(lane: dict[str, Any], outcome: dict[str, Any]) -> str:
    signature = lane["route_signature"]
    payload = {
        "outcome_statement_digest": outcome["statement_digest"],
        "outcome_scope_digest": outcome["scope_digest"],
        "owner_skill": lane["owner_skill"],
        "expected_artifact_type": lane["expected_artifact_type"],
        "method_family": signature["method_family"],
        "representation": signature["representation"],
        "key_assumption_digests": sorted(signature["key_assumption_digests"]),
        "tool_capability_refs": sorted(signature["tool_capability_refs"]),
    }
    return canonical_digest(payload)


def dominates(left: dict[str, int], right: dict[str, int]) -> bool:
    no_worse = all(left[key] >= right[key] for key in BENEFIT_DIMENSIONS)
    no_worse = no_worse and all(left[key] <= right[key] for key in COST_DIMENSIONS)
    strict = any(left[key] > right[key] for key in BENEFIT_DIMENSIONS)
    strict = strict or any(left[key] < right[key] for key in COST_DIMENSIONS)
    return no_worse and strict


def semantic_errors(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan["plan_version"] == 1 and plan.get("supersedes_plan_ref") is not None:
        errors.append("plan_version 1 cannot supersede another plan")
    if plan["plan_version"] > 1 and plan.get("supersedes_plan_ref") is None:
        errors.append("plan_version greater than 1 requires supersedes_plan_ref")

    outcomes = unique_map(plan["outcomes"], "outcome_id", "outcome_id", errors)
    root_id = plan["root_outcome_id"]
    root = outcomes.get(root_id)
    if root is None:
        errors.append("root_outcome_id does not identify an outcome")
    else:
        if root["family"] != "resolution":
            errors.append("root outcome must belong to the resolution family")
        if root["statement_digest"] != plan["problem_contract_ref"]["statement_digest"]:
            errors.append("root statement digest does not match the ProblemContract statement digest")
        if root["scope_digest"] != plan["problem_contract_ref"]["scope_digest"]:
            errors.append("root scope digest does not match the ProblemContract scope digest")
        if root["planning_status"] not in {"normalized", "ready"}:
            errors.append("root outcome must be normalized or ready")

    semantic_keys: dict[tuple[str, str], str] = {}
    for outcome in plan["outcomes"]:
        expected_statement = canonical_digest({"statement": outcome["statement"]})
        expected_scope = canonical_digest(outcome["scope"])
        if outcome["statement_digest"] != expected_statement:
            errors.append(f"statement digest mismatch: {outcome['outcome_id']}")
        if outcome["scope_digest"] != expected_scope:
            errors.append(f"scope digest mismatch: {outcome['outcome_id']}")
        key = (outcome["statement_digest"], outcome["scope_digest"])
        prior = semantic_keys.get(key)
        if prior is not None:
            errors.append(f"duplicate statement/scope identity: {prior} and {outcome['outcome_id']}")
        semantic_keys[key] = outcome["outcome_id"]

    relation_ids = unique_map(plan["relations"], "relation_id", "relation_id", errors)
    relation_keys: set[tuple[str, str, str]] = set()
    adjacency = {outcome_id: set() for outcome_id in outcomes}
    for relation in plan["relations"]:
        source = relation["source_outcome_id"]
        target = relation["target_outcome_id"]
        relation_key = (relation["line_type"], source, target)
        if relation_key in relation_keys:
            errors.append(f"duplicate typed relation: {relation['relation_id']}")
        relation_keys.add(relation_key)
        if source not in outcomes:
            errors.append(f"relation source is unknown: {source}")
        if target not in outcomes:
            errors.append(f"relation target is unknown: {target}")
        if source == target:
            errors.append(f"self relation is not allowed in a candidate plan: {relation['relation_id']}")
        if source in outcomes and target in outcomes and source != target:
            adjacency[source].add(target)
            adjacency[target].add(source)

    if root_id in outcomes:
        reached = {root_id}
        queue = deque([root_id])
        while queue:
            current = queue.popleft()
            for target in adjacency[current] - reached:
                reached.add(target)
                queue.append(target)
        disconnected = sorted(set(outcomes) - reached)
        if disconnected:
            errors.append(f"outcomes disconnected from root: {disconnected[0]}")

    policy = plan["frontier_policy"]
    if len(plan["frontier"]) > policy["frontier_limit"]:
        errors.append("frontier exceeds frontier_policy.frontier_limit")
    if policy["frontier_limit"] > policy["default_limit"] and policy["limit_exception"] is None:
        errors.append("frontier limit above the default requires a limit_exception")
    if policy["frontier_limit"] <= policy["default_limit"] and policy["limit_exception"] is not None:
        errors.append("limit_exception is only allowed above the default frontier limit")

    lane_ids = unique_map(plan["frontier"], "lane_id", "lane_id", errors)
    lane_keys: set[tuple[str, str, str]] = set()
    route_signatures: set[str] = set()
    failed_signatures = plan["input_refs"]["failed_route_signatures"]
    unique_map(failed_signatures, "failed_route_ref", "failed_route_ref signature", errors)
    failed_signature_digests: set[str] = set()
    failed_refs = set(plan["input_refs"]["failed_route_refs"])
    signature_refs = {item["failed_route_ref"] for item in failed_signatures}
    if failed_refs != signature_refs:
        errors.append("failed_route_refs and failed_route_signatures must have exact coverage")
    for item in failed_signatures:
        digest = item["route_signature_digest"]
        if digest in failed_signature_digests:
            errors.append(f"duplicate failed route signature: {digest}")
        failed_signature_digests.add(digest)

    required_dimensions = set(DIMENSIONS)
    for lane in plan["frontier"]:
        outcome = outcomes.get(lane["outcome_id"])
        if outcome is None:
            errors.append(f"frontier lane targets unknown outcome: {lane['outcome_id']}")
        elif outcome["planning_status"] not in {"normalized", "ready"}:
            errors.append(f"frontier lane targets non-ready outcome: {lane['outcome_id']}")
        lane_key = (lane["outcome_id"], lane["route_id"], lane["owner_skill"])
        if lane_key in lane_keys:
            errors.append(f"duplicate outcome/route/owner lane: {lane['lane_id']}")
        lane_keys.add(lane_key)
        basis_by_dimension: dict[str, dict[str, Any]] = {}
        for basis in lane["priority_basis"]:
            dimension = basis["dimension"]
            if dimension in basis_by_dimension:
                errors.append(f"duplicate priority basis dimension in {lane['lane_id']}: {dimension}")
            basis_by_dimension[dimension] = basis
        if set(basis_by_dimension) != required_dimensions:
            errors.append(f"priority basis dimensions drifted in {lane['lane_id']}")
        for dimension in required_dimensions & set(basis_by_dimension):
            if basis_by_dimension[dimension]["value"] != lane["priority_vector"][dimension]:
                errors.append(f"priority value/basis mismatch in {lane['lane_id']}: {dimension}")
        if lane["priority_vector"]["semantic_clarity"] == 0:
            errors.append(f"frontier lane failed semantic clarity hard gate: {lane['lane_id']}")
        if lane["priority_vector"]["verification_feasibility"] == 0:
            errors.append(f"frontier lane failed verification feasibility hard gate: {lane['lane_id']}")
        if outcome is not None:
            signature = expected_route_signature(lane, outcome)
            if lane["route_signature"]["digest"] != signature:
                errors.append(f"route signature digest mismatch: {lane['lane_id']}")
            if signature in route_signatures:
                errors.append(f"duplicate semantic route signature: {lane['lane_id']}")
            if signature in failed_signature_digests:
                errors.append(f"frontier repeats a failed route signature: {lane['lane_id']}")
            route_signatures.add(signature)

    lanes = list(lane_ids.values())
    for index, left in enumerate(lanes):
        for right in lanes[index + 1:]:
            if dominates(left["priority_vector"], right["priority_vector"]):
                errors.append(f"frontier contains dominated lane: {right['lane_id']}")
            elif dominates(right["priority_vector"], left["priority_vector"]):
                errors.append(f"frontier contains dominated lane: {left['lane_id']}")

    deferred_keys: set[tuple[str, str | None]] = set()
    selected_keys = {(lane["outcome_id"], lane["route_id"]) for lane in plan["frontier"]}
    for item in plan["deferred"]:
        if item["outcome_id"] not in outcomes:
            errors.append(f"deferred entry targets unknown outcome: {item['outcome_id']}")
        key = (item["outcome_id"], item.get("route_id"))
        if key in deferred_keys:
            errors.append(f"duplicate deferred entry: {item['outcome_id']}")
        if item.get("route_id") is not None and key in selected_keys:
            errors.append(f"lane cannot be selected and deferred: {item['outcome_id']}/{item['route_id']}")
        deferred_keys.add(key)

    observations = unique_map(plan["observations"], "observation_id", "observation_id", errors)
    del observations
    for observation in plan["observations"]:
        expected_refs = set(plan["input_refs"][OBSERVATION_INPUT_KIND[observation["kind"]]])
        if observation["source_ref"] not in expected_refs:
            errors.append(f"observation source_ref is not in its typed input set: {observation['observation_id']}")

    known_refs = {plan["problem_contract_ref"]["problem_id"], plan["problem_contract_ref"]["acceptance_ref"]}
    for key in ("source_refs", "failed_route_refs", "obligation_refs", "candidate_refs", "evidence_refs", "result_refs"):
        known_refs.update(plan["input_refs"][key])
    known_refs.update(outcomes)
    known_refs.update(relation_ids)
    known_refs.update(lane_ids)
    known_refs.update(lane["route_id"] for lane in plan["frontier"])
    for outcome in plan["outcomes"]:
        known_refs.update(outcome["scope"]["definition_refs"])
    for lane in plan["frontier"]:
        known_refs.update(lane["route_signature"]["tool_capability_refs"])

    referenced: list[tuple[str, str]] = []
    for outcome in plan["outcomes"]:
        referenced.extend((f"outcome {outcome['outcome_id']}", ref) for ref in outcome["basis_refs"])
    for relation in plan["relations"]:
        referenced.extend((f"relation {relation['relation_id']}", ref) for ref in relation["basis_refs"])
    for lane in plan["frontier"]:
        for basis in lane["priority_basis"]:
            referenced.extend((f"lane {lane['lane_id']} priority", ref) for ref in basis["basis_refs"])
    exception = policy["limit_exception"]
    if exception is not None:
        referenced.extend(("frontier limit exception", ref) for ref in exception["basis_refs"])
    for owner, ref in referenced:
        if ref not in known_refs:
            errors.append(f"basis reference is not bound by the plan: {owner}: {ref}")
    return errors


def validate(plan_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> dict[str, int]:
    schema = load_json(schema_path, "schema")
    plan = load_json(plan_path, "plan")
    if not isinstance(schema, dict) or not isinstance(plan, dict):
        raise PlanError("schema and plan must be JSON objects")
    errors = schema_errors(plan, schema)
    if not errors:
        errors.extend(semantic_errors(plan))
    if errors:
        raise PlanError(errors[0])
    return {
        "outcomes": len(plan["outcomes"]),
        "relations": len(plan["relations"]),
        "frontier_lanes": len(plan["frontier"]),
        "deferred": len(plan["deferred"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a candidate-only OSPS plan; execute no lanes.")
    parser.add_argument("--file", required=True, type=Path)
    args = parser.parse_args()
    try:
        counts = validate(args.file.resolve())
    except (PlanError, OSError, ValueError) as exc:
        print(f"OSPS plan: BLOCK: {exc}", file=sys.stderr)
        return 1
    print(
        "OSPS plan: PASS "
        f"outcomes={counts['outcomes']} relations={counts['relations']} "
        f"frontier={counts['frontier_lanes']} deferred={counts['deferred']} "
        "role=candidate-planning-only runtime=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
