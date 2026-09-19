#!/usr/bin/env python3
"""Focused tests for bounded execution-context selection and rendering."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from build_web_context_bundle import render_context
from vibe_mathing.web_channel import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]


def parse_payload(text: str) -> dict:
    return json.loads(text.split("```json\n", 1)[1].rsplit("\n```", 1)[0])


def copy_context_inputs(destination: Path) -> None:
    paths = [
        "problem-library/records/canonical-problems.jsonl",
        "WEB_ACTIVE_SKILLS.json",
        ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json",
        "governance/control-plane/math-knowledge-source.v1.json",
        "governance/control-plane/math-knowledge-operators.v1.json",
        "governance/control-plane/web-context-profile.v1.json",
        "governance/control-plane/web-context-profile.v1.schema.json",
    ]
    for relative in paths:
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for relative in (
        "research/records/attempts.jsonl",
        "research/records/obligation-graphs.jsonl",
        "research/records/failed-routes.jsonl",
    ):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("", encoding="utf-8")


def problem_id() -> str:
    line = next(line for line in (ROOT / "problem-library/records/canonical-problems.jsonl").read_text().splitlines() if line.strip())
    return json.loads(line)["problem_id"]


def attempt(attempt_id: str, lifecycle: str = "running") -> dict:
    return {
        "attempt_id": attempt_id,
        "problem_id": problem_id(),
        "route_id": "route:test",
        "obligation_graph_id": "graph:test",
        "generator": "test",
        "objective": "bounded selector test",
        "method": "proof",
        "lifecycle": lifecycle,
        "started_at": "2026-01-01T00:00:00Z",
        "completed_at": None,
        "inputs": ["frozen problem"],
        "claims": ["candidate"],
        "artifacts": ["research/artifacts/candidates/test.md"],
    }


def graph() -> dict:
    statement = {
        "text": "A bounded test obligation.",
        "language": "en",
        "formal_declaration": None,
    }
    return {
        "schema_version": "1.0.0",
        "graph_id": "graph:test",
        "problem_id": problem_id(),
        "attempt_id": "attempt:test",
        "route_id": "route:test",
        "problem_contract_sha256": "0" * 64,
        "root_obligation_id": "obligation:test",
        "obligations": [{
            "obligation_id": "obligation:test",
            "kind": "root_claim",
            "statement": statement,
            "statement_sha256": canonical_json_sha256(statement),
            "dependencies": [],
            "acceptance": {
                "required_capabilities": ["proof"],
                "allowed_candidate_kinds": ["proof"],
            },
            "source_refs": ["test"],
        }],
        "created_at": "2026-01-01T00:00:00Z",
        "supersedes": None,
    }


class ContextBundleTests(unittest.TestCase):
    def test_template_without_attempt_is_maintenance_only(self) -> None:
        payload = parse_payload(render_context(ROOT))
        self.assertEqual(payload["context_selection"]["status"], "no_active_execution_context")
        self.assertFalse(payload["context_selection"]["research_ready"])
        self.assertIsNone(payload["selected_execution_context"])

    def test_multiple_active_attempts_fail_closed_to_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            copy_context_inputs(root)
            (root / "research/records/attempts.jsonl").write_text(
                json.dumps(attempt("attempt:one")) + "\n" + json.dumps(attempt("attempt:two")) + "\n",
                encoding="utf-8",
            )
            payload = parse_payload(render_context(root))
            self.assertEqual(payload["context_selection"]["status"], "ambiguous_attempt")
            self.assertFalse(payload["context_selection"]["research_ready"])

    def test_explicit_identity_selects_one_bounded_context(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            copy_context_inputs(root)
            (root / "research/records/attempts.jsonl").write_text(json.dumps(attempt("attempt:test")) + "\n", encoding="utf-8")
            (root / "research/records/obligation-graphs.jsonl").write_text(json.dumps(graph()) + "\n", encoding="utf-8")
            payload = parse_payload(render_context(root, attempt_id="attempt:test"))
            self.assertEqual(payload["context_selection"]["status"], "ready")
            self.assertTrue(payload["context_selection"]["research_ready"])
            selected = payload["selected_execution_context"]
            self.assertEqual(selected["graph"]["selected_obligation_id"], "obligation:test")
            self.assertEqual(selected["attempt"]["attempt_id"], "attempt:test")

    def test_budget_is_hard(self) -> None:
        with self.assertRaises(RuntimeError):
            render_context(ROOT, max_chars=1000)


if __name__ == "__main__":
    unittest.main()
