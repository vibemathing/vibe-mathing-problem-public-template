#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from audit_release_checklist import audit, git_clean_receipt

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
        snapshot = json.loads((ROOT / "HARNESS_SNAPSHOT.json").read_text(encoding="utf-8"))
        if snapshot.get("problem", {}).get("problem_id") == "problem:template-placeholder":
            # 通用模板不适用 live Web；仅这个精确身份可豁免。
            self.assertEqual(by_id["C08"]["status"], "PASS")
        elif snapshot.get("problem", {}).get("admission") == "preview_unadmitted":
            # 生成仓 preview 必须真实 BLOCK，不允许测试把 C08 翻绿。
            self.assertEqual(by_id["C08"]["status"], "BLOCK")
            self.assertTrue(by_id["C08"]["blockers"])
        else:
            # 具体仓须有 live Web 回执，不能由 fixture 身份猜 PASS。
            admission = json.loads((ROOT / "WEB_REPOSITORY_ADMISSION.json").read_text(encoding="utf-8"))
            profile = json.loads((ROOT / "WEB_CHANNEL_PROFILE.json").read_text(encoding="utf-8"))
            live = (profile.get("operational_admission") == "admitted_problem_repository_namespace"
                    and admission.get("decision") == "ADMITTED" and len(admission.get("receipts", [])) >= 4)
            expected = "PASS" if live else "BLOCK"
            self.assertEqual(by_id["C08"]["status"], expected)
        self.assertEqual(by_id["C10"]["status"], "BLOCK")

    def test_clean_but_stale_checkout_cannot_pass_c07(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            independent = Path(directory)
            (independent / ".git").mkdir()
            (independent / "HARNESS_SNAPSHOT.json").write_text("{}\n", encoding="utf-8")
            with patch("audit_release_checklist.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                valid, _, blockers = git_clean_receipt(ROOT, independent)
            self.assertFalse(valid)
            self.assertTrue(any("snapshot" in error for error in blockers))

    def test_independent_receipt_requires_distinct_matching_clean_checkout(self) -> None:
        with patch("audit_release_checklist.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "", "")):
            valid, _, blockers = git_clean_receipt(ROOT, ROOT)
        self.assertFalse(valid)
        self.assertTrue(any("must not" in error for error in blockers))
        with tempfile.TemporaryDirectory() as directory:
            independent = Path(directory)
            (independent / ".git").mkdir()
            (independent / "HARNESS_SNAPSHOT.json").write_bytes((ROOT / "HARNESS_SNAPSHOT.json").read_bytes())
            with patch("audit_release_checklist.subprocess.run", return_value=subprocess.CompletedProcess([], 0, "", "")):
                valid, _, blockers = git_clean_receipt(ROOT, independent)
            self.assertTrue(valid, blockers)


if __name__ == "__main__":
    unittest.main()
