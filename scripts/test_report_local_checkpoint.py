#!/usr/bin/env python3
"""读写仅发生在临时 fixture；正式报告器只读、无数学准入权。"""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from report_local_checkpoint import MAX_READ_BYTES, read_bound, report

PROBLEM = "problem:fixture"
CONTRACT = "a" * 64


class CheckpointReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def fixture(self, name: str, sequence: int, *, status="open", event=211):
        path = self.root / name
        value = {
            "problem_id": PROBLEM, "problem_contract_sha256": CONTRACT,
            "sequence": sequence, "state_vector": {
                "mathematical_state": {"root_status": status, "candidate_frontier": sequence},
                "claim_boundary": "candidate_only",
                "evidence_state": {"independent_admission": False},
                "admission_state": {"closure_receipt": False},
            },
            "infrastructure_update": {"recorded_at_sequence": event, "kind": "infrastructure_only",
                                       "new_mathematical_delta": False},
        }
        path.write_text(json.dumps(value), encoding="utf-8")
        os.utime(path, ns=(sequence * 1_000_000_000, sequence * 1_000_000_000))
        return path

    def test_historical_event_is_not_current_delta_or_admission(self):
        self.fixture("a.json", 774)
        self.fixture("b.json", 775)
        result = report(self.root, PROBLEM, CONTRACT)
        self.assertEqual(result["latest_sequence_by_mtime"], 775)
        self.assertEqual(result["historical_infrastructure_event"], {
            "recorded_at_sequence": 211, "belongs_to_latest_checkpoint": False,
        })
        self.assertIs(result["mathematical_state_differs_from_adjacent_checkpoint"], True)
        self.assertEqual(result["root_status_reported"], "open")
        self.assertEqual(result["claim_boundary_reported"], "candidate_only")
        self.assertIs(result["independent_admission_reported_not_verified"], False)
        self.assertIs(result["closure_receipt_reported_not_verified"], False)
        self.assertEqual(result["storage"], {"json_files": 2, "json_bytes": sum(p.stat().st_size for p in self.root.iterdir()), "retention_action": "none"})
        self.assertNotIn("candidate_frontier", json.dumps(result))

    def test_no_predecessor_or_nonadjacent_is_unknown_not_false(self):
        self.fixture("first.json", 10, event=5)
        self.assertIsNone(report(self.root, PROBLEM, CONTRACT)["mathematical_state_differs_from_adjacent_checkpoint"])
        self.fixture("gap.json", 12, event=5)
        self.assertIsNone(report(self.root, PROBLEM, CONTRACT)["mathematical_state_differs_from_adjacent_checkpoint"])

    def test_identity_mismatch_and_future_event_fail_closed(self):
        p = self.fixture("a.json", 775)
        with self.assertRaisesRegex(ValueError, "identity"):
            report(self.root, PROBLEM, "b" * 64)
        data = json.loads(p.read_text())
        data["infrastructure_update"]["recorded_at_sequence"] = 776
        p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "future"):
            report(self.root, PROBLEM, CONTRACT)

    def test_symlink_and_oversize_fail_closed(self):
        source = self.fixture("a.json", 775)
        (self.root / "alias.json").symlink_to(source)
        with self.assertRaisesRegex(ValueError, "regular"):
            report(self.root, PROBLEM, CONTRACT)
        with tempfile.TemporaryDirectory() as other:
            large = Path(other) / "oversize.json"
            large.write_bytes(b" " * (MAX_READ_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "bound"):
                report(Path(other), PROBLEM, CONTRACT)

    def test_regular_file_replaced_by_fifo_does_not_block(self):
        source = self.fixture("a.json", 775)
        before = source.stat()
        source.rename(self.root / "retained-original")  # 仅在临时 fixture 中移动，保留原内容。
        os.mkfifo(source)
        with self.assertRaisesRegex(ValueError, "changed"):
            read_bound(source, before)

    def test_invalid_sequence_mtime_pair_fails_closed(self):
        self.fixture("old.json", 12)
        newer = self.fixture("new.json", 11)
        os.utime(newer, ns=(13_000_000_000, 13_000_000_000))
        with self.assertRaisesRegex(ValueError, "order"):
            report(self.root, PROBLEM, CONTRACT)


if __name__ == "__main__":
    unittest.main()
