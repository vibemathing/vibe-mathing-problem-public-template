#!/usr/bin/env python3
"""Compile the bounded, deterministic entry context for Web GPT research."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from vibe_mathing.web_channel import canonical_json_sha256, load_json, load_jsonl, load_problem

VERSION = "1.1.0"


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)


def render_context(root: Path, max_chars: int = 120_000) -> str:
    root = root.resolve()
    problem = load_problem(root)
    attempts = [item for item in load_jsonl(root / "research/records/attempts.jsonl") if item.get("problem_id") == problem.get("problem_id")]
    graphs = [item for item in load_jsonl(root / "research/records/obligation-graphs.jsonl") if item.get("problem_id") == problem.get("problem_id")]
    failed = [item for item in load_jsonl(root / "research/records/failed-routes.jsonl") if item.get("problem_id") == problem.get("problem_id")]
    source_registry = load_json(root / "governance/control-plane/math-knowledge-source.v1.json")
    operator_registry = load_json(root / "governance/control-plane/math-knowledge-operators.v1.json")
    active_skills = load_json(root / "WEB_ACTIVE_SKILLS.json")
    internal_package_classification = load_json(root / ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json")

    graph_summary = []
    for graph in graphs:
        graph_summary.append({
            "graph_id": graph.get("graph_id"),
            "attempt_id": graph.get("attempt_id"),
            "route_id": graph.get("route_id"),
            "root_obligation_id": graph.get("root_obligation_id"),
            "obligations": [
                {
                    "obligation_id": item.get("obligation_id"),
                    "kind": item.get("kind"),
                    "statement": item.get("statement"),
                    "statement_sha256": item.get("statement_sha256"),
                    "dependencies": item.get("dependencies", []),
                }
                for item in graph.get("obligations", [])
                if isinstance(item, dict)
            ],
        })

    payload = {
        "problem_contract": problem,
        "problem_contract_sha256": canonical_json_sha256(problem),
        "attempts": attempts,
        "obligation_graphs": graph_summary,
        "failed_routes": failed,
        "active_skills": active_skills.get("skills", []),
        "internal_package_routing": {
            "policy": internal_package_classification.get("policy", {}),
            "top_level_skills": {
                skill_id: {
                    "owned_packages": [
                        item.get("package_id")
                        for item in internal_package_classification.get("packages", [])
                        if isinstance(item, dict) and item.get("primary_owner") == skill_id
                    ],
                    "cross_referenced_packages": [
                        item.get("package_id")
                        for item in internal_package_classification.get("packages", [])
                        if isinstance(item, dict) and skill_id in item.get("cross_referenced_by", [])
                    ],
                }
                for skill_id in sorted({
                    item.get("primary_owner")
                    for item in internal_package_classification.get("packages", [])
                    if isinstance(item, dict) and item.get("primary_owner")
                })
            },
        },
        "knowledge_sources": [
            {
                "source_id": item.get("source_id"),
                "source_class": item.get("source_class"),
                "maturity": item.get("maturity"),
                "evidence_ceiling": item.get("evidence_ceiling"),
                "operational_status": item.get("operational_status"),
            }
            for item in source_registry.get("sources", [])
        ],
        "knowledge_operators": [
            {
                "operator_id": item.get("operator_id"),
                "owner_skill": item.get("owner_skill"),
                "external_effect": item.get("external_effect"),
                "evidence_ceiling": item.get("evidence_ceiling"),
            }
            for item in operator_registry.get("operators", [])
        ],
    }
    body = compact_json(payload)
    prefix = """# Web Research Context Bundle

This file is generated from repository truth and bounded for the web channel. It is navigation context, not a Result, EvidenceLink, verifier receipt, or permission grant.

## Mandatory order

1. Read `AGENTS.md`, `governance/harness/PROJECT_AGENTS.md`, and `WEB_BOOTSTRAP.md`.
2. Check the exact ProblemContract and its SHA-256 below.
3. Select exactly one pre-admitted Attempt/Route/ObligationGraph/Obligation.
4. Read the selected top-level Skill's `INTERNAL-PACKAGES.json`; route to the smallest applicable internal source package before inventing a method. HOLD package bodies remain private-local and are not publication content.
5. Search registered mathematical knowledge sources before inventing a new theorem.
6. After repository admission, autonomously complete Issue, candidate branch/file edits, commit, PR review, checks/rerun, merge, and checkpoint within the profile.
7. Write only candidate files under the profile allowlist and one `WEB_ATTEMPT_PACKET`; do not wait for project-added routine human approvals.
8. Never claim that Issue, PR, AI review, merge, Actions status, package build, search hit, test success, or this context closes mathematics.

## Compiled repository truth

```json
"""
    suffix = "\n```\n"
    rendered = prefix + body + suffix
    if len(rendered) > max_chars:
        raise RuntimeError(f"compiled web context exceeds {max_chars} characters")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a bounded Web GPT context bundle.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("WEB_CONTEXT_BUNDLE.md"))
    parser.add_argument("--max-chars", type=int, default=120_000)
    args = parser.parse_args()
    root = args.project_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        text = render_context(root, args.max_chars)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1
    print(f"web context bundle: PASS chars={len(text)} output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
