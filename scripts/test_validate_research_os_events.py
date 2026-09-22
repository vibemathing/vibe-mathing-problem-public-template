#!/usr/bin/env python3
"""Regression and adversarial tests for the Research OS cognitive event ledger."""

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

from validate_research_os_events import (  # noqa: E402
    DEFAULT_SCHEMA,
    event_digest,
    load_json,
    read_jsonl,
    validate_events,
)

FIXTURE_DIR = ROOT / "fixtures/research-os"
VALID = FIXTURE_DIR / "valid-events.jsonl"
INVALID = FIXTURE_DIR / "invalid-events.jsonl"


def _events(path: Path = VALID) -> list[dict[str, Any]]:
    events, errors = read_jsonl(path)
    if errors:
        raise AssertionError(errors)
    return events


def _rehash(events: list[dict[str, Any]]) -> None:
    previous = None
    for index, event in enumerate(events, 1):
        event["sequence"] = index
        event["previous_event_sha256"] = previous
        event["event_sha256"] = event_digest(event)
        previous = event["event_sha256"]


class ResearchOsEventTests(unittest.TestCase):
    def test_schema_and_fixture_are_valid(self) -> None:
        schema = load_json(DEFAULT_SCHEMA, "schema")
        Draft202012Validator.check_schema(schema)
        self.assertEqual(validate_events(_events(), schema), [])

    def test_invalid_chain_and_link_are_blocked(self) -> None:
        invalid_events, parse_errors = read_jsonl(INVALID)
        errors = list(parse_errors)
        errors.extend(validate_events(invalid_events, load_json(DEFAULT_SCHEMA, "schema")))
        self.assertTrue(any("chain mismatch" in error for error in errors), errors)
        self.assertTrue(any("linked verification" in error for error in errors), errors)

    def test_event_digest_tampering_is_blocked(self) -> None:
        events = _events()
        events[2]["payload"]["note"] = "tampered"
        errors = validate_events(events)
        self.assertTrue(any("event_sha256 mismatch" in error for error in errors), errors)

    def test_problem_binding_drift_is_blocked(self) -> None:
        events = _events()
        events[3]["problem_contract"]["scope_sha256"] = "9" * 64
        _rehash(events)
        errors = validate_events(events)
        self.assertTrue(any("ProblemContract binding drifts" in error for error in errors), errors)

    def test_non_authoritative_ceiling_cannot_be_raised(self) -> None:
        events = _events()
        events[1]["payload"]["claims_ceiling"] = "admitted"
        _rehash(events)
        errors = validate_events(events)
        self.assertTrue(any("candidate_only" in error for error in errors), errors)

    def test_forbidden_payload_keys_are_blocked(self) -> None:
        events = _events()
        events[1]["payload"]["reasoning"] = "must not be stored"
        _rehash(events)
        errors = validate_events(events)
        self.assertTrue(any("forbidden content/secret keys" in error for error in errors), errors)

    def test_validator_does_not_mutate_input(self) -> None:
        events = _events()
        before = copy.deepcopy(events)
        validate_events(events)
        self.assertEqual(events, before)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ResearchOsEventTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
