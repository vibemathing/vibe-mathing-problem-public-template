#!/usr/bin/env python3
# 做什么：测试公开模板 Research OS profile 的边界、digest 和 Makefile 接线。
# 怎么运行：python3 scripts/test_validate_research_os_production_readiness.py
# 需要什么：公开 profile/schema、项目源码和 Python jsonschema。
"""Regression tests for the public-template Research OS capability profile."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_os_production_readiness import (  # noqa: E402
    DEFAULT_CONTRACT,
    DEFAULT_SCHEMA,
    RESEARCH_OS_CHECK_COMMANDS,
    load_json,
    validate_document,
)


class PublicResearchOsProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_json(DEFAULT_SCHEMA, "profile schema")
        self.profile = load_json(DEFAULT_CONTRACT, "profile")

    def test_current_profile_is_strictly_valid_and_pilot(self) -> None:
        self.assertEqual(validate_document(self.profile, self.schema, ROOT, strict=True), [])
        self.assertEqual(self.profile["status"], "pilot")
        self.assertEqual(self.profile["claim_boundary"], "candidate_only_no_mathematical_truth")

    def test_source_digest_drift_is_blocked(self) -> None:
        value = copy.deepcopy(self.profile)
        value["capabilities"][0]["source_sha256"] = "0" * 64
        errors = validate_document(value, self.schema, ROOT, strict=True)
        self.assertTrue(any("source digest drift" in error for error in errors), errors)

    def test_self_promotion_is_rejected_by_schema(self) -> None:
        value = copy.deepcopy(self.profile)
        value["status"] = "ready"
        errors = validate_document(value, self.schema, ROOT, strict=False)
        self.assertTrue(any("status" in error for error in errors), errors)

    def test_duplicate_capability_is_blocked(self) -> None:
        value = copy.deepcopy(self.profile)
        value["capabilities"].append(copy.deepcopy(value["capabilities"][0]))
        errors = validate_document(value, self.schema, ROOT, strict=False)
        self.assertTrue(any("duplicate capability_id" in error for error in errors), errors)

    def test_math_truth_boundary_gate_cannot_be_removed(self) -> None:
        value = copy.deepcopy(self.profile)
        value["gates"] = [gate for gate in value["gates"] if gate["gate_id"] != "gate.math-truth-boundary"]
        errors = validate_document(value, self.schema, ROOT, strict=False)
        self.assertTrue(any("truth boundary gate is missing" in error for error in errors), errors)

    def test_check_contract_is_explicit_and_ordered(self) -> None:
        check = (ROOT / "Makefile").read_text(encoding="utf-8")
        positions = []
        for command in RESEARCH_OS_CHECK_COMMANDS:
            position = check.find(command)
            self.assertGreaterEqual(position, 0, command)
            positions.append(position)
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(self.profile["validation_commands"], list(RESEARCH_OS_CHECK_COMMANDS))

    def test_validator_does_not_mutate_profile(self) -> None:
        before = json.dumps(self.profile, ensure_ascii=False, sort_keys=True)
        validate_document(self.profile, self.schema, ROOT, strict=True)
        after = json.dumps(self.profile, ensure_ascii=False, sort_keys=True)
        self.assertEqual(before, after)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublicResearchOsProfileTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
