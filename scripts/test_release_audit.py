#!/usr/bin/env python3
import unittest
from pathlib import Path

from audit_release_checklist import audit

ROOT = Path(__file__).resolve().parents[1]


class ReleaseChecklistAuditTest(unittest.TestCase):
    def test_all_checklist_items_are_explicit_and_fail_closed(self) -> None:
        report = audit(ROOT)
        self.assertEqual([item["id"] for item in report["checks"]], [f"C{i:02d}" for i in range(1, 11)])
        self.assertEqual(report["decision"], "BLOCK")
        self.assertFalse(report["release_authorized"])
        by_id = {item["id"]: item for item in report["checks"]}
        self.assertEqual(by_id["C04"]["status"], "PASS")
        self.assertEqual(by_id["C06"]["status"], "PASS")
        self.assertEqual(by_id["C09"]["status"], "PASS")
        self.assertEqual(by_id["C03"]["status"], "PASS")
        self.assertEqual(by_id["C05"]["status"], "PASS")
        self.assertEqual(by_id["C08"]["status"], "PASS")
        self.assertEqual(by_id["C10"]["status"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
