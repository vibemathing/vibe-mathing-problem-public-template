#!/usr/bin/env python3
"""Research OS owner adapter、WAL exactly-once 与 projection 回归测试。"""

from __future__ import annotations

import copy
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_research_os_events import event_digest
from vibe_mathing.research_os import (
    ResearchOsError,
    ResearchOsEventWriter,
    ResearchOsOwnerLedgerAdapter,
    ResearchOsProjector,
    ResearchOsWriterError,
    canonical_json_sha256,
    problem_scope_sha256,
    problem_statement_sha256,
    validate_projection,
)


FIXTURE_PROBLEM_ID = "problem:sympy-counterexample-fixture"


def _read_problem() -> dict[str, Any]:
    # 从随母版复制的 test-only fixture 读取，不依赖具体问题仓的冻结合同。
    value = json.loads((ROOT / "fixtures/sympy-counterexample/problem.json").read_text(encoding="utf-8"))
    if value.get("problem_id") != FIXTURE_PROBLEM_ID or value.get("lifecycle") != "active":
        raise AssertionError("Research OS test fixture identity or lifecycle mismatch")
    schema = json.loads((ROOT / "problem-library/schema/canonical-problem.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(value)
    return value


def _copy_schema(source_relative: str, target_root: Path) -> None:
    target = target_root / source_relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / source_relative, target)


def _rehash(events: list[dict[str, Any]]) -> None:
    previous = None
    for sequence, event in enumerate(events, 1):
        event["sequence"] = sequence
        event["previous_event_sha256"] = previous
        event["event_sha256"] = event_digest(event)
        previous = event["event_sha256"]


class ResearchOsRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="research-os-runtime-")
        self.root = Path(self.tempdir.name)
        for relative in (
            "research/schema/research-os-event.v1.schema.json",
            "research/schema/research-os-event-projection.v1.schema.json",
            "problem-library/schema/canonical-problem.schema.json",
        ):
            _copy_schema(relative, self.root)
        problem_path = self.root / "problem-library/records/canonical-problems.jsonl"
        problem_path.parent.mkdir(parents=True, exist_ok=True)
        problem_path.write_text(json.dumps(_read_problem(), ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        self.problem = _read_problem()
        self.binding = {
            "problem_id": FIXTURE_PROBLEM_ID,
            "problem_contract_sha256": canonical_json_sha256(self.problem),
            "statement_sha256": problem_statement_sha256(self.problem),
            "scope_sha256": problem_scope_sha256(self.problem),
        }
        self.adapter = ResearchOsOwnerLedgerAdapter(self.root)
        self.ledger = self.root / "research/records/research-os-events.jsonl"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _event(
        self,
        *,
        event_id: str,
        event_kind: str,
        object_kind: str,
        object_id: str,
        action: str,
        refs: list[str],
        recorded_at: str,
        note: str = "candidate-only metadata",
    ) -> dict[str, Any]:
        return {
            "schema_version": "research-os-event.v1",
            "ledger_id": "research-os-cognitive-events",
            "event_id": event_id,
            "event_kind": event_kind,
            "recorded_at": recorded_at,
            "problem_contract": copy.deepcopy(self.binding),
            "object_kind": object_kind,
            "object_id": object_id,
            "payload": {
                "action": action,
                "claims_ceiling": "candidate_only",
                "refs": refs,
                "statement_sha256": None,
                "scope_sha256": None,
                "artifact_sha256": None,
                "coverage": "unknown",
                "note": note,
            },
            "producer": "research-os-cognitive-projection",
            "non_authoritative": True,
        }

    def _base_events(self) -> list[dict[str, Any]]:
        events = [
            self._event(
                event_id="research-os-event:fixture-working-set",
                event_kind="working_set_created",
                object_kind="working_set",
                object_id="research-os:fixture-open",
                action="recorded",
                refs=[self.problem["problem_id"]],
                recorded_at="2026-09-21T00:00:00Z",
            ),
            self._event(
                event_id="research-os-event:fixture-example",
                event_kind="example_recorded",
                object_kind="example",
                object_id="example:fixture-one",
                action="recorded",
                refs=["research-os:fixture-open", "source:fixture-source"],
                recorded_at="2026-09-21T00:00:01Z",
            ),
        ]
        _rehash(events)
        return events

    def test_owner_adapter_accepts_explicit_problem_binding_without_writing_owner_ledger(self) -> None:
        before = (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes()
        events = self._base_events()
        self.adapter.ensure_valid(events)
        after = (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes()
        self.assertEqual(before, after)

    def test_owner_adapter_resolves_synthetic_attempt_and_obligation(self) -> None:
        # The public template has intentionally empty owner ledgers.  Build a
        # generic in-memory-style fixture in the temporary project instead of
        # importing a concrete problem ID or internal research record.
        for relative in (
            "research/schema/attempt.schema.json",
            "research/schema/obligation-graph.schema.json",
        ):
            _copy_schema(relative, self.root)
        statement = {
            "text": "A synthetic runtime obligation remains candidate-only.",
            "language": "en",
            "formal_declaration": None,
        }
        obligation_id = "obligation:template-runtime-root"
        graph_id = "graph:template-runtime"
        attempt_id = "attempt:template-runtime"
        obligation = {
            "obligation_id": obligation_id,
            "kind": "root_claim",
            "statement": statement,
            "statement_sha256": canonical_json_sha256(statement),
            "dependencies": [],
            "acceptance": {
                "required_capabilities": ["statement_faithfulness"],
                "allowed_candidate_kinds": ["proof"],
            },
            "source_refs": [self.problem["problem_id"]],
        }
        graph = {
            "schema_version": "1.0.0",
            "graph_id": graph_id,
            "problem_id": self.problem["problem_id"],
            "attempt_id": attempt_id,
            "route_id": "route:template-runtime",
            "problem_contract_sha256": self.binding["problem_contract_sha256"],
            "root_obligation_id": obligation_id,
            "obligations": [obligation],
            "created_at": "2026-09-21T00:00:00Z",
            "supersedes": None,
        }
        attempt = {
            "attempt_id": attempt_id,
            "problem_id": self.problem["problem_id"],
            "route_id": graph["route_id"],
            "obligation_graph_id": graph_id,
            "problem_contract_sha256": self.binding["problem_contract_sha256"],
            "generator": "public-template-runtime-test",
            "objective": "Exercise generic owner-ledger resolution.",
            "method": "discovery",
            "lifecycle": "planned",
            "started_at": "2026-09-21T00:00:00Z",
            "completed_at": None,
            "inputs": ["synthetic fixture"],
            "claims": ["candidate-only"],
            "artifacts": [],
        }
        for relative, value in (
            ("research/records/attempts.jsonl", attempt),
            ("research/records/obligation-graphs.jsonl", graph),
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        event = self._base_events()[0]
        dependency = self._event(
            event_id="research-os-event:fixture-obligation",
            event_kind="proof_dependency_linked",
            object_kind="proof_dependency",
            object_id=obligation_id,
            action="linked",
            refs=[obligation_id, "research-os:fixture-open"],
            recorded_at="2026-09-21T00:00:01Z",
        )
        dependency["payload"]["statement_sha256"] = obligation["statement_sha256"]
        events = [event, dependency]
        _rehash(events)
        ResearchOsOwnerLedgerAdapter(self.root).ensure_valid(events)

    def test_owner_adapter_fails_closed_on_scope_or_missing_managed_ref(self) -> None:
        events = self._base_events()
        for event in events:
            event["problem_contract"]["scope_sha256"] = "f" * 64
        _rehash(events)
        errors = self.adapter.validate_events(events)
        self.assertTrue(any("scope digest mismatch" in error for error in errors), errors)

        events = self._base_events()
        events[1]["payload"]["refs"].append("candidate:missing")
        _rehash(events)
        errors = self.adapter.validate_events(events)
        self.assertTrue(any("unknown Candidate" in error for error in errors), errors)

    def test_writer_rejects_unbound_append(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        with self.assertRaises(ResearchOsWriterError):
            writer.append(self._base_events()[0])
        self.assertFalse(self.ledger.exists())

    def test_writer_is_exactly_once_and_keeps_chain(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        first = writer.append(self._base_events()[0], owner_adapter=self.adapter)
        duplicate = writer.append(self._base_events()[0], owner_adapter=self.adapter)
        self.assertEqual(first, duplicate)
        second = writer.append(self._base_events()[1], owner_adapter=self.adapter)
        self.assertEqual(second["sequence"], 2)
        self.assertEqual(len(writer.read_events()), 2)
        self.assertFalse(writer.wal_path.exists())
        self.assertEqual(stat.S_IMODE(writer.lock_path.stat().st_mode), 0o600)
        conflict = copy.deepcopy(self._base_events()[0])
        conflict["payload"]["note"] = "different immutable event content"
        with self.assertRaises(ResearchOsWriterError):
            writer.append(conflict, owner_adapter=self.adapter)
        self.assertEqual(len(writer.read_events()), 2)

    def test_wal_recovers_after_before_and_after_replace_crashes(self) -> None:
        first = self._base_events()[0]
        for fail_point in ("after_wal", "after_replace"):
            with self.subTest(fail_point=fail_point):
                crash_root = self.root / fail_point
                crash_root.mkdir()
                for relative in (
                    "research/schema/research-os-event.v1.schema.json",
                    "problem-library/schema/canonical-problem.schema.json",
                ):
                    _copy_schema(relative, crash_root)
                problem_path = crash_root / "problem-library/records/canonical-problems.jsonl"
                problem_path.parent.mkdir(parents=True, exist_ok=True)
                problem_path.write_bytes((self.root / "problem-library/records/canonical-problems.jsonl").read_bytes())
                adapter = ResearchOsOwnerLedgerAdapter(crash_root)
                writer = ResearchOsEventWriter(crash_root)
                with self.assertRaises(ResearchOsWriterError):
                    writer.append(first, owner_adapter=adapter, fail_point=fail_point)
                self.assertTrue(writer.wal_path.exists())
                recovered = writer.read_events()
                self.assertEqual(len(recovered), 1)
                self.assertEqual(recovered[0]["event_id"], first["event_id"])
                self.assertFalse(writer.wal_path.exists())
                self.assertEqual(writer.append(first, owner_adapter=adapter)["sequence"], 1)

    def test_projection_missing_ledger_has_no_runtime_side_effect(self) -> None:
        projector = ResearchOsProjector(self.root, self.adapter)
        with self.assertRaises(ResearchOsError):
            projector.project_file(self.ledger)
        self.assertFalse((self.root / "research/records/.research-os-events.jsonl.lock").exists())

    def test_projection_refuses_unresolved_wal_without_recovery_side_effect(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        with self.assertRaises(ResearchOsWriterError):
            writer.append(self._base_events()[0], owner_adapter=self.adapter, fail_point="after_wal")
        wal_before = writer.wal_path.read_bytes()
        with self.assertRaises(ResearchOsError) as failure:
            ResearchOsProjector(self.root, self.adapter).project_file(self.ledger)
        self.assertIn("unresolved WAL", str(failure.exception))
        self.assertEqual(wal_before, writer.wal_path.read_bytes())

    def test_tampered_wal_fails_closed(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        with self.assertRaises(ResearchOsWriterError):
            writer.append(self._base_events()[0], owner_adapter=self.adapter, fail_point="after_wal")
        wal = json.loads(writer.wal_path.read_text(encoding="utf-8"))
        wal["target_sha256"] = "0" * 64
        writer.wal_path.write_text(json.dumps(wal, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaises(ResearchOsWriterError):
            writer.read_events()

    def test_batch_is_atomic_when_late_owner_binding_fails(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        valid, invalid = self._base_events()
        invalid["problem_contract"]["problem_contract_sha256"] = "0" * 64
        invalid.pop("sequence")
        invalid.pop("previous_event_sha256")
        invalid.pop("event_sha256")
        with self.assertRaises(ResearchOsError):
            writer.append_many([valid, invalid], owner_adapter=self.adapter)
        self.assertFalse(self.ledger.exists())
        self.assertFalse(writer.wal_path.exists())

    def test_projection_is_deterministic_read_only_and_candidate_only(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        writer.append_many(self._base_events(), owner_adapter=self.adapter)
        owner_before = (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes()
        projection = ResearchOsProjector(self.root, self.adapter).project_file(self.ledger)
        projection_again = ResearchOsProjector(self.root, self.adapter).project_file(self.ledger)
        self.assertEqual(projection, projection_again)
        self.assertEqual(projection["claims_ceiling"], "candidate_only")
        self.assertTrue(projection["non_authoritative"])
        self.assertTrue(projection["non_mathematical_truth"])
        self.assertEqual(projection["event_count"], 2)
        self.assertEqual(projection["opaque_ref_ids"], ["source:fixture-source"])
        self.assertEqual(
            projection["owner_snapshot_sha256"],
            canonical_json_sha256(projection["owner_ledgers"]),
        )
        self.assertEqual(len(projection["owner_ledgers"]), 5)
        self.assertEqual(
            validate_projection(
                projection,
                projection_again,
                json.loads((self.root / "research/schema/research-os-event-projection.v1.schema.json").read_text()),
            ),
            [],
        )
        self.assertEqual(owner_before, (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes())

    def test_owner_snapshot_drift_fails_closed(self) -> None:
        events = self._base_events()
        problem_path = self.root / "problem-library/records/canonical-problems.jsonl"
        original = problem_path.read_bytes()
        problem_path.write_bytes(original[:-1] + b" \n")
        errors = self.adapter.validate_events(events)
        self.assertTrue(any("owner snapshot" in error for error in errors), errors)

    def test_projection_cli_is_read_only_and_revalidates_stored_projection(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        writer.append_many(self._base_events(), owner_adapter=self.adapter)
        command = [
            sys.executable,
            str(ROOT / "scripts/project_research_os.py"),
            "--project-root",
            str(self.root),
            "--ledger",
            str(self.ledger),
        ]
        owner_before = (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes()
        generated = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(generated.returncode, 0, generated.stderr)
        projection = json.loads(generated.stdout)
        stored_path = self.root / "projection.json"
        stored_path.write_text(json.dumps(projection, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        checked = subprocess.run(
            [*command, "--stored", str(stored_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn('"status": "PASS"', checked.stdout)
        self.assertEqual(owner_before, (self.root / "problem-library/records/canonical-problems.jsonl").read_bytes())

    def test_projection_rejects_tampered_self_digest(self) -> None:
        writer = ResearchOsEventWriter(self.root, self.ledger)
        writer.append_many(self._base_events(), owner_adapter=self.adapter)
        projection = ResearchOsProjector(self.root, self.adapter).project_file(self.ledger)
        tampered = copy.deepcopy(projection)
        tampered["event_count"] = 99
        errors = validate_projection(tampered, projection, json.loads((self.root / "research/schema/research-os-event-projection.v1.schema.json").read_text()))
        self.assertTrue(any("self-digest" in error for error in errors), errors)
        self.assertTrue(any("stale" in error for error in errors), errors)

    def test_broken_owner_ledger_symlink_is_rejected(self) -> None:
        problem_path = self.root / "problem-library/records/canonical-problems.jsonl"
        backup = self.root / "problem-library/records/canonical-problems.backup.jsonl"
        problem_path.rename(backup)
        try:
            problem_path.symlink_to(self.root / "missing-problem-ledger.jsonl")
            with self.assertRaises(ResearchOsError):
                ResearchOsOwnerLedgerAdapter(self.root)
        finally:
            problem_path.unlink(missing_ok=True)
            backup.rename(problem_path)

    def test_symlink_event_path_is_rejected_before_write(self) -> None:
        outside = self.root / "outside.jsonl"
        outside.write_bytes(b"")
        link = self.root / "research/records/link.jsonl"
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(outside)
        with self.assertRaises(ResearchOsWriterError):
            ResearchOsEventWriter(self.root, link)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ResearchOsRuntimeTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
