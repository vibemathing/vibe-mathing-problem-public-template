#!/usr/bin/env python3
"""Regression and adversarial tests for the Mathematical Research OS projection."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_os_working_set import (  # noqa: E402
    DEFAULT_SCHEMA,
    load_json,
    validate,
)

FIXTURE_DIR = ROOT / "fixtures/research-os"
FIXTURE = FIXTURE_DIR / "valid-working-set.json"
INVALID_ADMITTED = FIXTURE_DIR / "invalid-admitted-working-set.json"
INVALID_LINKED = FIXTURE_DIR / "invalid-linked-without-evidence.json"
INVALID_DUPLICATE = FIXTURE_DIR / "invalid-duplicate-working-set.json"


def _load(path: Path = FIXTURE) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ResearchOsWorkingSetTests(unittest.TestCase):
    def test_schema_and_fixture_are_valid(self) -> None:
        schema = load_json(DEFAULT_SCHEMA, "schema")
        Draft202012Validator.check_schema(schema)
        self.assertEqual(validate(_load(), schema), [])

    def test_candidate_only_ceiling_is_required(self) -> None:
        errors = validate(_load(INVALID_ADMITTED))
        self.assertTrue(any("claims_ceiling" in error for error in errors), errors)

    def test_linked_verification_requires_evidence(self) -> None:
        errors = validate(_load(INVALID_LINKED))
        self.assertTrue(any("linked verification requires" in error for error in errors), errors)

    def test_duplicate_working_set_identity_is_blocked(self) -> None:
        errors = validate(_load(INVALID_DUPLICATE))
        self.assertTrue(any("duplicate example_id" in error for error in errors), errors)
        self.assertTrue(any("duplicate working-set identity" in error for error in errors), errors)

    def test_admitted_conjecture_status_is_blocked(self) -> None:
        working_set = _load()
        working_set["conjectures"][0]["status"] = "admitted"
        errors = validate(working_set)
        self.assertTrue(any("schema at conjectures/0/status" in error for error in errors), errors)

    def test_unknown_local_obligation_is_blocked(self) -> None:
        working_set = _load()
        working_set["frame"]["obligation_refs"].append("obligation:not-in-working-set")
        errors = validate(working_set)
        self.assertTrue(any("unknown local ID" in error for error in errors), errors)

    def test_supersession_requires_reason_and_new_version(self) -> None:
        working_set = _load()
        working_set["supersedes"] = "research-os:fixture-open-v1"
        errors = validate(working_set)
        self.assertTrue(any("record_version > 1" in error for error in errors), errors)
        self.assertTrue(any("supersession_reason is required" in error for error in errors), errors)

    def test_working_set_does_not_accept_result_reference_shape(self) -> None:
        working_set = _load()
        working_set["result_refs"] = ["result:forbidden"]
        errors = validate(working_set)
        self.assertTrue(any("Additional properties" in error for error in errors), errors)

    def test_validator_does_not_mutate_input(self) -> None:
        working_set = _load()
        before = copy.deepcopy(working_set)
        validate(working_set)
        self.assertEqual(working_set, before)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ResearchOsWorkingSetTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
