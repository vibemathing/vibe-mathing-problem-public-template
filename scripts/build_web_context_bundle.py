#!/usr/bin/env python3
"""Compile a bounded, deterministic execution context for Web GPT research."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

from vibe_mathing.web_channel import (
    canonical_json_sha256,
    load_json,
    load_jsonl,
    load_problem,
    validate_schema,
)

VERSION = "2.0.0"
PROFILE_RELATIVE = "governance/control-plane/web-context-profile.v1.json"
PROFILE_SCHEMA_RELATIVE = "governance/control-plane/web-context-profile.v1.schema.json"


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)


def clip_text(value: Any, limit: int) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 20)] + "…[clipped]"


def record_time(record: dict[str, Any]) -> str:
    for key in ("started_at", "recorded_at", "created_at", "completed_at"):
        value = record.get(key)
        if isinstance(value, str):
            return value
    return ""


def record_id(record: dict[str, Any]) -> str:
    for key in ("attempt_id", "graph_id", "route_id", "obligation_id"):
        value = record.get(key)
        if isinstance(value, str):
            return value
    return ""


def recent(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(records, key=lambda item: (record_time(item), record_id(item)), reverse=True)


def bounded_items(
    records: list[dict[str, Any]],
    limit: int,
    projector: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    ordered = recent(records)
    return {
        "total": len(ordered),
        "omitted_count": max(0, len(ordered) - limit),
        "items": [projector(item) for item in ordered[:limit]],
    }


def load_profile(root: Path) -> dict[str, Any]:
    profile_path = root / PROFILE_RELATIVE
    schema_path = root / PROFILE_SCHEMA_RELATIVE
    profile = load_json(profile_path)
    errors = validate_schema(profile, schema_path)
    if errors:
        raise RuntimeError(f"execution-context profile invalid: {errors[0]}")
    return profile


def records_for_problem(root: Path, relative: str, problem_id: str) -> list[dict[str, Any]]:
    return [
        record
        for record in load_jsonl(root / relative)
        if record.get("problem_id") == problem_id
    ]


def attempt_summary(record: dict[str, Any], text_limit: int) -> dict[str, Any]:
    return {
        "attempt_id": record.get("attempt_id"),
        "route_id": record.get("route_id"),
        "obligation_graph_id": record.get("obligation_graph_id"),
        "lifecycle": record.get("lifecycle"),
        "method": record.get("method"),
        "objective": clip_text(record.get("objective", ""), text_limit),
        "started_at": record.get("started_at"),
        "completed_at": record.get("completed_at"),
        "input_count": len(record.get("inputs", [])) if isinstance(record.get("inputs"), list) else 0,
        "claim_count": len(record.get("claims", [])) if isinstance(record.get("claims"), list) else 0,
        "artifact_count": len(record.get("artifacts", [])) if isinstance(record.get("artifacts"), list) else 0,
        "record_sha256": canonical_json_sha256(record),
    }


def graph_summary(record: dict[str, Any], text_limit: int) -> dict[str, Any]:
    obligations = record.get("obligations", [])
    return {
        "graph_id": record.get("graph_id"),
        "attempt_id": record.get("attempt_id"),
        "route_id": record.get("route_id"),
        "root_obligation_id": record.get("root_obligation_id"),
        "created_at": record.get("created_at"),
        "obligation_count": len(obligations) if isinstance(obligations, list) else 0,
        "root_statement": clip_text(
            next(
                (
                    item.get("statement", {}).get("text", "")
                    for item in obligations
                    if isinstance(item, dict) and item.get("obligation_id") == record.get("root_obligation_id")
                ),
                "",
            ),
            text_limit,
        ),
        "graph_sha256": canonical_json_sha256(record),
    }


def failed_route_summary(record: dict[str, Any], text_limit: int) -> dict[str, Any]:
    evidence = record.get("evidence", [])
    return {
        "route_id": record.get("route_id"),
        "route": clip_text(record.get("route", ""), text_limit),
        "blocker": clip_text(record.get("blocker", ""), text_limit),
        "conclusion": record.get("conclusion"),
        "evidence_count": len(evidence) if isinstance(evidence, list) else 0,
        "recorded_at": record.get("recorded_at"),
        "recorded_by": record.get("recorded_by"),
        "record_sha256": canonical_json_sha256(record),
    }


def attempt_projection(record: dict[str, Any], max_items: int) -> dict[str, Any]:
    projection: dict[str, Any] = {
        key: record.get(key)
        for key in (
            "attempt_id",
            "problem_id",
            "route_id",
            "obligation_graph_id",
            "generator",
            "objective",
            "method",
            "lifecycle",
            "started_at",
            "completed_at",
        )
        if key in record
    }
    omitted: dict[str, int] = {}
    for key in ("inputs", "claims", "artifacts"):
        values = record.get(key, [])
        if not isinstance(values, list):
            projection[key] = values
            continue
        projection[key] = values[:max_items]
        if len(values) > max_items:
            omitted[key] = len(values) - max_items
    projection["omitted_list_items"] = omitted
    projection["record_sha256"] = canonical_json_sha256(record)
    return projection


def graph_projection(
    graph: dict[str, Any],
    obligation_id: str,
    max_catalog: int,
    max_closure: int,
    text_limit: int,
) -> dict[str, Any]:
    raw_obligations = [item for item in graph.get("obligations", []) if isinstance(item, dict)]
    by_id = {item.get("obligation_id"): item for item in raw_obligations}
    target = by_id.get(obligation_id)
    if target is None:
        raise RuntimeError(f"selected obligation is absent from graph: {obligation_id}")

    closure_ids: list[str] = []
    pending = [obligation_id]
    seen: set[str] = set()
    while pending and len(closure_ids) < max_closure:
        current = pending.pop(0)
        if current in seen:
            continue
        seen.add(current)
        closure_ids.append(current)
        dependency_ids = by_id.get(current, {}).get("dependencies", [])
        if isinstance(dependency_ids, list):
            pending.extend(str(item) for item in dependency_ids if str(item) not in seen)

    dependency_objects = [by_id[item] for item in closure_ids[1:] if item in by_id]
    catalog = sorted(
        (
            {
                "obligation_id": item.get("obligation_id"),
                "kind": item.get("kind"),
                "statement": clip_text(item.get("statement", {}).get("text", ""), text_limit),
                "dependencies": item.get("dependencies", []),
                "statement_sha256": item.get("statement_sha256"),
            }
            for item in raw_obligations
        ),
        key=lambda item: str(item.get("obligation_id", "")),
    )
    return {
        "graph_id": graph.get("graph_id"),
        "attempt_id": graph.get("attempt_id"),
        "route_id": graph.get("route_id"),
        "root_obligation_id": graph.get("root_obligation_id"),
        "created_at": graph.get("created_at"),
        "graph_sha256": canonical_json_sha256(graph),
        "selected_obligation_id": obligation_id,
        "selected_obligation": target,
        "dependency_obligations": dependency_objects,
        "dependency_closure_ids": closure_ids,
        "dependency_closure_omitted_count": len(pending),
        "obligation_catalog": {
            "total": len(catalog),
            "omitted_count": max(0, len(catalog) - max_catalog),
            "items": catalog[:max_catalog],
        },
    }


def select_execution_context(
    problem_id: str,
    attempts: list[dict[str, Any]],
    graphs: list[dict[str, Any]],
    *,
    profile: dict[str, Any],
    attempt_id: str | None,
    route_id: str | None,
    graph_id: str | None,
    obligation_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    selectors = {
        "attempt_id": attempt_id,
        "route_id": route_id,
        "graph_id": graph_id,
        "obligation_id": obligation_id,
    }
    selected_attempt: dict[str, Any] | None = None
    selected_graph: dict[str, Any] | None = None
    status = "no_active_execution_context"
    reason = "no running or planned Attempt is available"

    attempts_by_id = {item.get("attempt_id"): item for item in attempts}
    graphs_by_id = {item.get("graph_id"): item for item in graphs}

    if attempt_id is not None:
        selected_attempt = attempts_by_id.get(attempt_id)
        if selected_attempt is None:
            status = "invalid_selector"
            reason = f"attempt_id is not present for this ProblemContract: {attempt_id}"
    else:
        for lifecycle in profile["selection"]["active_lifecycle_priority"]:
            candidates = [item for item in attempts if item.get("lifecycle") == lifecycle]
            if len(candidates) == 1:
                selected_attempt = candidates[0]
                break
            if len(candidates) > 1:
                status = "ambiguous_attempt"
                reason = f"{len(candidates)} {lifecycle} Attempts require an explicit attempt_id"
                return (
                    {
                        "status": status,
                        "research_ready": False,
                        "reason": reason,
                        "selectors": selectors,
                    },
                    None,
                )

    if selected_attempt is not None:
        active_lifecycles = set(profile["selection"]["active_lifecycle_priority"])
        if selected_attempt.get("lifecycle") not in active_lifecycles:
            return (
                {
                    "status": "inactive_attempt",
                    "research_ready": False,
                    "reason": "selected Attempt is historical/inactive; create or select a running or planned Attempt",
                    "selectors": selectors,
                },
                None,
            )
        attempt_route = selected_attempt.get("route_id")
        if route_id is not None and attempt_route not in {None, route_id}:
            return (
                {
                    "status": "inconsistent_selector",
                    "research_ready": False,
                    "reason": "route_id does not match selected Attempt",
                    "selectors": selectors,
                },
                None,
            )
        route_id = route_id or attempt_route
        bound_graph_id = selected_attempt.get("obligation_graph_id")
        if graph_id is not None and bound_graph_id not in {None, graph_id}:
            return (
                {
                    "status": "inconsistent_selector",
                    "research_ready": False,
                    "reason": "graph_id does not match selected Attempt",
                    "selectors": selectors,
                },
                None,
            )
        graph_id = graph_id or bound_graph_id

    if graph_id is not None:
        selected_graph = graphs_by_id.get(graph_id)
        if selected_graph is None:
            return (
                {
                    "status": "invalid_selector",
                    "research_ready": False,
                    "reason": f"graph_id is not present for this ProblemContract: {graph_id}",
                    "selectors": selectors,
                },
                None,
            )
    else:
        candidates = graphs
        if route_id is not None:
            candidates = [item for item in candidates if item.get("route_id") == route_id]
        if selected_attempt is not None:
            candidates = [
                item
                for item in candidates
                if item.get("attempt_id") == selected_attempt.get("attempt_id")
            ]
        if len(candidates) == 1:
            selected_graph = candidates[0]
        elif len(candidates) > 1:
            return (
                {
                    "status": "ambiguous_graph",
                    "research_ready": False,
                    "reason": f"{len(candidates)} ObligationGraphs match; provide graph_id",
                    "selectors": selectors,
                },
                None,
            )

    if selected_graph is None:
        if selected_attempt is not None or any(value is not None for value in selectors.values()):
            status = "missing_graph"
            reason = "selected execution identity has no matching ObligationGraph"
        return (
            {
                "status": status,
                "research_ready": False,
                "reason": reason,
                "selectors": selectors,
                "selected_attempt_id": selected_attempt.get("attempt_id") if selected_attempt else None,
            },
            None,
        )

    if selected_graph.get("problem_id") != problem_id:
        return (
            {
                "status": "cross_problem_reference",
                "research_ready": False,
                "reason": "selected ObligationGraph belongs to another ProblemContract",
                "selectors": selectors,
            },
            None,
        )
    if selected_attempt is None:
        selected_attempt = attempts_by_id.get(selected_graph.get("attempt_id"))
    if selected_attempt is None:
        return (
            {
                "status": "missing_attempt",
                "research_ready": False,
                "reason": "selected ObligationGraph has no matching Attempt",
                "selectors": selectors,
            },
            None,
        )
    if selected_attempt.get("attempt_id") != selected_graph.get("attempt_id"):
        return (
            {
                "status": "inconsistent_execution_identity",
                "research_ready": False,
                "reason": "Attempt and ObligationGraph identities do not agree",
                "selectors": selectors,
            },
            None,
        )
    if route_id is not None and selected_graph.get("route_id") not in {None, route_id}:
        return (
            {
                "status": "inconsistent_selector",
                "research_ready": False,
                "reason": "route_id does not match selected ObligationGraph",
                "selectors": selectors,
            },
            None,
        )

    target_id = obligation_id or selected_graph.get("root_obligation_id")
    obligations = {
        item.get("obligation_id"): item
        for item in selected_graph.get("obligations", [])
        if isinstance(item, dict)
    }
    if target_id not in obligations:
        return (
            {
                "status": "invalid_selector" if obligation_id else "missing_root_obligation",
                "research_ready": False,
                "reason": f"obligation is absent from selected graph: {target_id}",
                "selectors": selectors,
            },
            None,
        )

    selection = {
        "status": "ready",
        "research_ready": True,
        "reason": "one bounded Attempt/Route/Graph/Obligation context selected",
        "selectors": selectors,
        "selected_attempt_id": selected_attempt.get("attempt_id") if selected_attempt else None,
        "selected_route_id": selected_graph.get("route_id"),
        "selected_graph_id": selected_graph.get("graph_id"),
        "selected_obligation_id": target_id,
    }
    return selection, {
        "attempt": selected_attempt,
        "graph": selected_graph,
        "obligation_id": target_id,
    }


def render_context(
    root: Path,
    max_chars: int | None = None,
    *,
    attempt_id: str | None = None,
    route_id: str | None = None,
    graph_id: str | None = None,
    obligation_id: str | None = None,
) -> str:
    root = root.resolve()
    profile = load_profile(root)
    effective_max_chars = profile["max_chars"] if max_chars is None else min(max_chars, profile["max_chars"])
    if effective_max_chars < 1:
        raise ValueError("max_chars must be positive")

    problem = load_problem(root)
    problem_id = problem.get("problem_id")
    attempts = records_for_problem(root, "research/records/attempts.jsonl", problem_id)
    graphs = records_for_problem(root, "research/records/obligation-graphs.jsonl", problem_id)
    failed = records_for_problem(root, "research/records/failed-routes.jsonl", problem_id)
    source_registry = load_json(root / "governance/control-plane/math-knowledge-source.v1.json")
    operator_registry = load_json(root / "governance/control-plane/math-knowledge-operators.v1.json")
    active_skills = load_json(root / "WEB_ACTIVE_SKILLS.json")
    classification = load_json(root / ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json")
    budgets = profile["budgets"]
    text_limit = budgets["max_text_chars"]

    selection, selected = select_execution_context(
        problem_id,
        attempts,
        graphs,
        profile=profile,
        attempt_id=attempt_id,
        route_id=route_id,
        graph_id=graph_id,
        obligation_id=obligation_id,
    )

    attempt_catalog = bounded_items(
        attempts,
        budgets["max_attempt_catalog"],
        lambda item: attempt_summary(item, text_limit),
    )
    graph_catalog = bounded_items(
        graphs,
        budgets["max_graph_catalog"],
        lambda item: graph_summary(item, text_limit),
    )
    failed_catalog = bounded_items(
        failed,
        budgets["max_failed_route_catalog"],
        lambda item: failed_route_summary(item, text_limit),
    )

    selected_context: dict[str, Any] | None = None
    if selected is not None:
        selected_attempt = selected["attempt"]
        selected_graph = selected["graph"]
        selected_context = {
            "attempt": (
                attempt_projection(selected_attempt, budgets["max_list_items"])
                if selected_attempt is not None
                else None
            ),
            "graph": graph_projection(
                selected_graph,
                selected["obligation_id"],
                budgets["max_obligation_catalog"],
                budgets["max_dependency_closure"],
                text_limit,
            ),
        }

    packages = []
    for item in sorted(classification.get("packages", []), key=lambda value: str(value.get("package_id", ""))):
        packages.append({
            "package_id": item.get("package_id"),
            "primary_owner": item.get("primary_owner"),
            "cross_referenced_by": item.get("cross_referenced_by", []),
            "capabilities": item.get("extracted_capabilities", []),
            "source_files": item.get("source_files"),
            "source_bytes": item.get("source_bytes"),
            "entry_relative_path": item.get("entry_relative_path"),
            "repository_relative_path": item.get("repository_relative_path"),
            "rights_state": "ADMITTED" if item.get("public_redistribution_admitted") is True else "HOLD",
        })
    package_catalog = {
        "total": len(packages),
        "omitted_count": max(0, len(packages) - budgets["max_package_catalog"]),
        "items": packages[: budgets["max_package_catalog"]],
    }

    payload: dict[str, Any] = {
        "context_bundle_version": VERSION,
        "context_policy": profile,
        "problem_contract": problem,
        "problem_contract_sha256": canonical_json_sha256(problem),
        "context_selection": selection,
        "selected_execution_context": selected_context,
        "freshness": {
            "bundle_role": "bounded_navigation_cache",
            "authoritative_state": "fresh_repository_ledgers_and_live_github_objects",
            "recompute_when_input_digest_changes": True,
            "input_ledgers": {
                "research/records/attempts.jsonl": {
                    "record_count": len(attempts),
                    "records_sha256": canonical_json_sha256(attempts),
                },
                "research/records/obligation-graphs.jsonl": {
                    "record_count": len(graphs),
                    "records_sha256": canonical_json_sha256(graphs),
                },
                "research/records/failed-routes.jsonl": {
                    "record_count": len(failed),
                    "records_sha256": canonical_json_sha256(failed),
                },
            },
        },
        "execution_catalog": {
            "attempts": attempt_catalog,
            "obligation_graphs": graph_catalog,
            "failed_routes": failed_catalog,
        },
        "active_skills": active_skills.get("skills", []),
        "internal_package_routing": {
            "policy": classification.get("policy", {}),
            "package_catalog": package_catalog,
        },
        "knowledge_sources": [
            {
                "source_id": item.get("source_id"),
                "source_class": item.get("source_class"),
                "maturity": item.get("maturity"),
                "evidence_ceiling": item.get("evidence_ceiling"),
                "operational_status": item.get("operational_status"),
                "used_by": item.get("used_by", []),
            }
            for item in source_registry.get("sources", [])[: budgets["max_source_catalog"]]
        ],
        "knowledge_operators": [
            {
                "operator_id": item.get("operator_id"),
                "owner_skill": item.get("owner_skill"),
                "external_effect": item.get("external_effect"),
                "evidence_ceiling": item.get("evidence_ceiling"),
                "input_kinds": item.get("input_kinds", []),
                "output_kind": item.get("output_kind"),
            }
            for item in operator_registry.get("operators", [])[: budgets["max_operator_catalog"]]
        ],
    }
    payload["context_payload_sha256"] = canonical_json_sha256(payload)
    body = compact_json(payload)
    prefix = """# Web Research Context Bundle

This file is generated from repository truth and bounded by `governance/control-plane/web-context-profile.v1.json`. It is navigation context, not a Result, EvidenceLink, verifier receipt, or permission grant.

## Mandatory order

1. Read `AGENTS.md`, `governance/harness/PROJECT_AGENTS.md`, and `WEB_BOOTSTRAP.md`.
2. Read the execution-context profile and confirm its digest-bound limits.
3. Check the exact ProblemContract and its SHA-256 below.
4. Check `context_selection.status`. Only `ready` permits mathematical work; `no_active_execution_context` is maintenance/pre-admission only; ambiguous, inconsistent, missing, or invalid states are fail-closed.
5. Treat the bundle as a bounded navigation cache. Fresh repository ledgers and live GitHub state outrank it; compare the input-ledger digests before relying on a selected context.
6. When `ready`, use only the selected Attempt/Route/ObligationGraph/Obligation and its bounded dependency closure. The catalogs are navigation indexes, not permission grants.
7. Read the selected top-level Skill's `INTERNAL-PACKAGES.json`; route to the smallest applicable internal package before inventing a method. Complete project-authored package bodies are bundled at repository-relative paths and are MIT-licensed; package admission does not grant execution, mathematical-evidence, or Result authority.
8. Search registered mathematical knowledge sources before inventing a new theorem.
9. Never claim that Issue, PR, AI review, merge, Actions status, package build, search hit, test success, or this context closes mathematics.

## Compiled repository truth

```json
"""
    suffix = "\n```\n"
    rendered = prefix + body + suffix
    if len(rendered) > effective_max_chars:
        raise RuntimeError(
            f"compiled web context exceeds {effective_max_chars} characters "
            f"(rendered={len(rendered)}, status={selection['status']})"
        )
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a bounded Web GPT execution-context bundle.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("WEB_CONTEXT_BUNDLE.md"))
    parser.add_argument("--max-chars", type=int)
    parser.add_argument("--attempt-id")
    parser.add_argument("--route-id")
    parser.add_argument("--graph-id")
    parser.add_argument("--obligation-id")
    args = parser.parse_args()
    root = args.project_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        text = render_context(
            root,
            args.max_chars,
            attempt_id=args.attempt_id,
            route_id=args.route_id,
            graph_id=args.graph_id,
            obligation_id=args.obligation_id,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    print(f"web context bundle: PASS version={VERSION} chars={len(text)} output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
