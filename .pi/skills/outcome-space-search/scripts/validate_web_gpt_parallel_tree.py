#!/usr/bin/env python3
"""Validate the candidate-only nine-lane Web GPT outcome classification tree."""
from __future__ import annotations

import argparse
import json
import sys
from itertools import product
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TREE = SKILL_ROOT / "references" / "web-gpt-parallel-tree.v1.json"
DEFAULT_SCHEMA = SKILL_ROOT / "references" / "web-gpt-parallel-tree.schema.json"
EXPECTED_LANES = tuple(f"T{index}" for index in range(1, 10))
EXPECTED_SCOPE = {
    "exact",
    "special",
    "conditional",
    "generalized",
    "strengthened",
    "weakened",
    "incomparable",
}
EXPECTED_HIT_GROUPS = {
    "root_closure_candidate": {"T1", "T2"},
    "local_progress": {"T3", "T4", "T5", "T6", "T7"},
    "search_reduction": {"T8"},
    "replan_trigger": {"T9"},
}
EXPECTED_DIMENSIONS = {
    "target": {"root_problem", "intermediate_mathematics", "route", "semantic_contract", "unclassified"},
    "effect": {"establish", "refute", "advance", "block", "revise", "independence", "unknown"},
    "output": {"proof", "refutation", "relation", "local-assertion", "structure", "quantity", "construction-or-procedure", "negative-route-knowledge", "meta-semantic-or-new-type"},
}
EXPECTED_SEARCH_FIELDS = {
    "lane_id", "outcome_id", "statement", "scope", "closure_predicate",
    "priority_vector", "owner", "requested_budget", "stop_condition",
    "input_refs", "expected_artifact",
}
EXPECTED_PRECEDENCE = ("T1", "T2", "T8", "T3", "T5", "T6", "T7", "T4", "T9")
ANCHORS = (
    ({"target": "root_problem", "effect": "establish", "output": "proof"}, "T1"),
    ({"target": "root_problem", "effect": "refute", "output": "refutation"}, "T2"),
    ({"target": "route", "effect": "block", "output": "relation"}, "T8"),
    ({"target": "intermediate_mathematics", "effect": "advance", "output": "relation"}, "T3"),
    ({"target": "intermediate_mathematics", "effect": "advance", "output": "structure"}, "T5"),
    ({"target": "intermediate_mathematics", "effect": "advance", "output": "quantity"}, "T6"),
    ({"target": "intermediate_mathematics", "effect": "advance", "output": "construction-or-procedure"}, "T7"),
    ({"target": "intermediate_mathematics", "effect": "advance", "output": "local-assertion"}, "T4"),
    ({"target": "root_problem", "effect": "independence", "output": "meta-semantic-or-new-type"}, "T9"),
    ({"target": "semantic_contract", "effect": "revise", "output": "meta-semantic-or-new-type"}, "T9"),
    ({"target": "semantic_contract", "effect": "revise", "output": "relation"}, "T9"),
    ({"target": "root_problem", "effect": "advance", "output": "relation"}, "T9"),
)


class TreeError(RuntimeError):
    pass


def load_json(path: Path, label: str) -> Any:
    if path.is_symlink() or not path.is_file():
        raise TreeError(f"{label} must be a regular file")
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise TreeError(f"{label} is not valid finite JSON: {exc}") from exc


def rule_matches(rule: dict[str, Any], candidate: dict[str, str]) -> bool:
    if rule["mode"] == "fallback":
        return True
    matches = [candidate[key] in values for key, values in rule["conditions"].items()]
    return all(matches) if rule["mode"] == "all" else any(matches)


def classify(tree: dict[str, Any], candidate: dict[str, str]) -> str:
    for rule in tree["assignment_rules"]:
        if rule_matches(rule, candidate):
            return rule["lane_id"]
    raise TreeError("classifier has no fallback for candidate")


def validate(tree_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> dict[str, int]:
    tree = load_json(tree_path, "tree")
    schema = load_json(schema_path, "schema")
    Draft202012Validator.check_schema(schema)
    schema_errors = sorted(
        Draft202012Validator(schema).iter_errors(tree),
        key=lambda error: [str(item) for item in error.absolute_path],
    )
    errors = [
        f"schema at {'/'.join(str(item) for item in error.absolute_path) or '<root>'}: {error.message}"
        for error in schema_errors
    ]
    if schema_errors:
        raise TreeError("\n".join(errors))

    lanes = tree["lanes"]
    lane_ids = [lane["lane_id"] for lane in lanes]
    if tuple(lane_ids) != EXPECTED_LANES:
        errors.append(f"lanes must be ordered exactly as {EXPECTED_LANES}")
    if tree["lane_count"] != len(lanes):
        errors.append("lane_count does not match lanes length")
    if tuple(tree["assignment_precedence"]) != EXPECTED_PRECEDENCE:
        errors.append(f"assignment_precedence must be exactly {EXPECTED_PRECEDENCE}")

    actual_dimensions = {key: set(values) for key, values in tree["classifier_dimensions"].items()}
    if actual_dimensions != EXPECTED_DIMENSIONS:
        errors.append("classifier_dimensions must equal the closed v1 target/effect/output universe")

    rules = tree["assignment_rules"]
    rule_ids = [rule["lane_id"] for rule in rules]
    if rule_ids != tree["assignment_precedence"]:
        errors.append("assignment_rules must follow assignment_precedence exactly")
    fallback_rules = [rule["lane_id"] for rule in rules if rule["mode"] == "fallback"]
    if fallback_rules != ["T9"] or rules[-1]["conditions"]:
        errors.append("T9 must be the only final rule with empty fallback conditions")
    for rule in rules:
        if rule["mode"] != "fallback" and not rule["conditions"]:
            errors.append(f"non-fallback assignment rule has no conditions: {rule['lane_id']}")
        for dimension, values in rule["conditions"].items():
            if dimension not in EXPECTED_DIMENSIONS or not set(values) <= EXPECTED_DIMENSIONS[dimension]:
                errors.append(f"assignment rule uses unknown {dimension} value: {rule['lane_id']}")

    fallback_ids = [lane["lane_id"] for lane in lanes if lane["fallback"]]
    if fallback_ids != ["T9"]:
        errors.append("T9 must be the only fallback lane")

    slugs = [lane["slug"] for lane in lanes]
    if len(slugs) != len(set(slugs)):
        errors.append("lane slugs must be unique")
    for lane in lanes:
        if len(lane["children"]) != len(set(lane["children"])):
            errors.append(f"duplicate child in lane {lane['lane_id']}")

    if set(tree["scope_overlay"]) != EXPECTED_SCOPE:
        errors.append("scope_overlay must cover the seven exact v1 scope values")

    classified: dict[str, int] = {lane_id: 0 for lane_id in EXPECTED_LANES}
    dimension_order = ("target", "effect", "output")
    combinations = list(product(*(sorted(EXPECTED_DIMENSIONS[key]) for key in dimension_order)))
    for values in combinations:
        candidate = dict(zip(dimension_order, values))
        try:
            classified[classify(tree, candidate)] += 1
        except (KeyError, TreeError) as exc:
            errors.append(f"classifier failed to cover {candidate}: {exc}")
    unreachable = [lane_id for lane_id, count in classified.items() if count == 0]
    if unreachable:
        errors.append(f"assignment rules contain unreachable lanes: {unreachable}")
    for candidate, expected_lane in ANCHORS:
        try:
            actual_lane = classify(tree, candidate)
        except (KeyError, TreeError) as exc:
            errors.append(f"anchor classification failed for {candidate}: {exc}")
            continue
        if actual_lane != expected_lane:
            errors.append(f"anchor {candidate} classified as {actual_lane}, expected {expected_lane}")

    unit_contract = tree["search_unit_contract"]
    if set(unit_contract["required_fields"]) != EXPECTED_SEARCH_FIELDS:
        errors.append("search_unit_contract must bind all eleven required task-candidate fields")
    projection = tree["concurrency_projection"]
    if projection["classification_slots"] != len(lanes):
        errors.append("concurrency projection must expose one classification slot per lane")
    if projection["maximum_task_candidates"] != len(lanes) * projection["task_candidates_per_slot"]:
        errors.append("maximum_task_candidates must derive from slots times candidates per slot")

    actual_hit_groups = {key: set(value) for key, value in tree["hit_semantics"].items()}
    if actual_hit_groups != EXPECTED_HIT_GROUPS:
        errors.append("hit_semantics must partition T1-T9 into the four fixed hit groups")
    hit_ids = [lane_id for values in tree["hit_semantics"].values() for lane_id in values]
    if len(hit_ids) != len(set(hit_ids)) or set(hit_ids) != set(EXPECTED_LANES):
        errors.append("hit_semantics must cover every lane exactly once")

    if len(tree["atomicity_rules"]) < 4:
        errors.append("atomicity_rules must include split, single-lane and fallback rules")
    if any(tree["non_claims"].values()):
        errors.append("all non_claims flags must remain false")

    if errors:
        raise TreeError("\n".join(errors))
    return {
        "lanes": len(lanes),
        "children": sum(len(lane["children"]) for lane in lanes),
        "scope_values": len(tree["scope_overlay"]),
        "classified_combinations": len(combinations),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=DEFAULT_TREE)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()
    try:
        counts = validate(args.file, args.schema)
    except TreeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        "Web GPT parallel outcome tree: PASS "
        f"lanes={counts['lanes']} children={counts['children']} "
        f"scope_values={counts['scope_values']} "
        f"classified_combinations={counts['classified_combinations']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
