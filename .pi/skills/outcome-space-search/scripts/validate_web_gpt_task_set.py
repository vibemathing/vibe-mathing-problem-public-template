#!/usr/bin/env python3
"""Validate a nine-slot Web GPT task set and optional synthetic response rehearsal."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TREE = SKILL_ROOT / "references/web-gpt-parallel-tree.v1.json"
DEFAULT_TASK_SCHEMA = SKILL_ROOT / "references/web-gpt-task-set.schema.json"
DEFAULT_RESPONSE_SCHEMA = SKILL_ROOT / "references/web-gpt-synthetic-response-set.schema.json"
TREE_VALIDATOR = SKILL_ROOT / "scripts/validate_web_gpt_parallel_tree.py"
EXPECTED_LANES = tuple(f"T{index}" for index in range(1, 10))
REQUIRED_TASK_FIELDS = {
    "lane_id", "outcome_id", "statement", "scope", "closure_predicate",
    "priority_vector", "owner", "requested_budget", "stop_condition",
    "input_refs", "expected_artifact",
}


class TaskSetError(RuntimeError):
    pass


def load_json(path: Path, label: str) -> Any:
    if path.is_symlink() or not path.is_file():
        raise TaskSetError(f"{label} must be a regular file")
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise TaskSetError(f"{label} is not valid finite JSON: {exc}") from exc


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    return value


def canonical_digest(value: Any) -> str:
    payload = json.dumps(normalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without(value: dict[str, Any], key: str) -> dict[str, Any]:
    return {item_key: item_value for item_key, item_value in value.items() if item_key != key}


def load_tree_module():
    spec = importlib.util.spec_from_file_location("validate_web_gpt_parallel_tree", TREE_VALIDATOR)
    if spec is None or spec.loader is None:
        raise TaskSetError("cannot load Web GPT tree validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_schema(instance: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path, f"{label} schema")
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: [str(item) for item in error.absolute_path],
    )
    return [
        f"{label} schema at {'/'.join(str(item) for item in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def route_signature(task: dict[str, Any]) -> str:
    return canonical_digest({
        "classification": task["classification"],
        "expected_artifact": task["expected_artifact"],
        "owner": task["owner"],
        "scope_digest": task["scope_digest"],
        "statement_digest": task["statement_digest"],
        "subdirection": task["subdirection"],
    })


def hit_group_for(tree: dict[str, Any], lane_id: str) -> str:
    groups = [name for name, lanes in tree["hit_semantics"].items() if lane_id in lanes]
    if len(groups) != 1:
        raise TaskSetError(f"lane {lane_id} has {len(groups)} hit groups")
    return groups[0]


def validate(
    tasks_path: Path,
    responses_path: Path | None = None,
    tree_path: Path = DEFAULT_TREE,
    task_schema_path: Path = DEFAULT_TASK_SCHEMA,
    response_schema_path: Path = DEFAULT_RESPONSE_SCHEMA,
) -> dict[str, int]:
    module = load_tree_module()
    module.validate(tree_path)
    tree = load_json(tree_path, "classification tree")
    tasks = load_json(tasks_path, "task set")
    errors = validate_schema(tasks, task_schema_path, "task set")
    if errors:
        raise TaskSetError("\n".join(errors))

    if tasks["classification_tree"]["sha256"] != raw_sha256(tree_path):
        errors.append("classification_tree.sha256 does not bind the tree bytes")
    lanes = tasks["lanes"]
    lane_ids = [task["lane_id"] for task in lanes]
    if tuple(lane_ids) != EXPECTED_LANES:
        errors.append(f"task lanes must be ordered exactly as {EXPECTED_LANES}")
    owners = [task["owner"] for task in lanes]
    if len(owners) != len(set(owners)):
        errors.append("each candidate lane must have one unique owner")
    paths = [task["expected_artifact"]["path"] for task in lanes]
    if len(paths) != len(set(paths)):
        errors.append("expected candidate artifact paths must be unique")

    lane_map = {lane["lane_id"]: lane for lane in tree["lanes"]}
    for task in lanes:
        lane_id = task["lane_id"]
        missing = REQUIRED_TASK_FIELDS - set(task)
        if missing:
            errors.append(f"{lane_id} misses required task fields: {sorted(missing)}")
        if task["owner"] != f"web-gpt-slot-{lane_id}":
            errors.append(f"{lane_id} owner is not bound to its slot")
        if task["outcome_id"] != f"outcome:synthetic-infrastructure:{lane_id}":
            errors.append(f"{lane_id} outcome identity mismatch")
        if task["expected_artifact"]["path"] != f"research/artifacts/candidates/synthetic-infrastructure/{lane_id}.json":
            errors.append(f"{lane_id} candidate artifact path mismatch")
        try:
            classified = module.classify(tree, task["classification"])
        except Exception as exc:  # noqa: BLE001 - convert imported validator failures
            errors.append(f"{lane_id} classification failed: {exc}")
        else:
            if classified != lane_id:
                errors.append(f"{lane_id} classifier result is {classified}")
        if task["subdirection"] not in lane_map[lane_id]["children"]:
            errors.append(f"{lane_id} subdirection is not contained by its lane")
        if task["statement_digest"] != canonical_digest(task["statement"]):
            errors.append(f"{lane_id} statement_digest mismatch")
        if task["scope_digest"] != canonical_digest(task["scope"]):
            errors.append(f"{lane_id} scope_digest mismatch")
        if task["route_signature"] != route_signature(task):
            errors.append(f"{lane_id} route_signature mismatch")
        if task["task_digest"] != canonical_digest(without(task, "task_digest")):
            errors.append(f"{lane_id} task_digest mismatch")
        if tasks["problem_contract"]["ref"] not in task["input_refs"]:
            errors.append(f"{lane_id} input_refs miss synthetic ProblemContract")
        if tasks["classification_tree"]["ref"] not in task["input_refs"]:
            errors.append(f"{lane_id} input_refs miss classification tree")
        if task["requested_budget"]["authorization_status"] != "not_authorized":
            errors.append(f"{lane_id} requested budget was treated as authorization")

    if tasks["task_set_digest"] != canonical_digest(without(tasks, "task_set_digest")):
        errors.append("task_set_digest mismatch")

    response_count = 0
    if responses_path is not None:
        responses = load_json(responses_path, "response set")
        errors.extend(validate_schema(responses, response_schema_path, "response set"))
        if not errors:
            if responses["task_set_digest"] != tasks["task_set_digest"]:
                errors.append("response set is bound to a different task set")
            response_ids = [response["lane_id"] for response in responses["responses"]]
            if tuple(response_ids) != EXPECTED_LANES:
                errors.append(f"responses must be ordered exactly as {EXPECTED_LANES}")
            task_by_lane = {task["lane_id"]: task for task in lanes}
            for response in responses["responses"]:
                lane_id = response["lane_id"]
                task = task_by_lane[lane_id]
                checks = (
                    (response["task_digest"] == task["task_digest"], "task binding"),
                    (response["problem_contract_digest"] == tasks["problem_contract"]["digest"], "ProblemContract binding"),
                    (response["scope"] == task["scope"], "scope binding"),
                    (response["artifact_path"] == task["expected_artifact"]["path"], "artifact path binding"),
                    (response["propagation"]["hit_group"] == hit_group_for(tree, lane_id), "hit propagation group"),
                    (response["payload_digest"] == canonical_digest(response["payload"]), "payload digest"),
                )
                for accepted, label in checks:
                    if not accepted:
                        errors.append(f"{lane_id} response {label} mismatch")
                if any(response[field] for field in ("evidence_created", "result_created", "solution_created", "root_closure_asserted")):
                    errors.append(f"{lane_id} response escalates mathematical state")
                if response["propagation"]["root_closure_allowed"] or response["propagation"]["result_admission_allowed"]:
                    errors.append(f"{lane_id} response enables forbidden propagation")
            if responses["response_set_digest"] != canonical_digest(without(responses, "response_set_digest")):
                errors.append("response_set_digest mismatch")
            response_count = len(responses["responses"])

    if errors:
        raise TaskSetError("\n".join(errors))
    return {"tasks": len(lanes), "responses": response_count}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--tree", type=Path, default=DEFAULT_TREE)
    parser.add_argument("--task-schema", type=Path, default=DEFAULT_TASK_SCHEMA)
    parser.add_argument("--response-schema", type=Path, default=DEFAULT_RESPONSE_SCHEMA)
    args = parser.parse_args()
    try:
        counts = validate(args.tasks, args.responses, args.tree, args.task_schema, args.response_schema)
    except TaskSetError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Web GPT task/rehearsal contract: PASS tasks={counts['tasks']} responses={counts['responses']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
