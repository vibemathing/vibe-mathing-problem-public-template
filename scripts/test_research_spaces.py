#!/usr/bin/env python3
"""Regression tests for research-space CLI, derived index and fail-closed identity."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_research_spaces.py"


class ResearchSpaceTests(unittest.TestCase):
    def run_validator(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--project-root", str(root), *args],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_project_root_and_json_report(self) -> None:
        result = self.run_validator(ROOT, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["decision"], "PASS")
        self.assertEqual(report["solution_count"], 0)

    def test_stale_solution_index_blocks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-research-space-") as directory:
            copy = Path(directory) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            index = copy / "result-library/indexes/solutions.json"
            value = json.loads(index.read_text(encoding="utf-8"))
            value["result_ids"] = ["result:unexpected"]
            index.write_text(json.dumps(value) + "\n", encoding="utf-8")
            result = self.run_validator(copy, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["decision"], "BLOCK")
            self.assertTrue(any("派生结果不一致" in item for item in json.loads(result.stdout)["errors"]))


if __name__ == "__main__":
    unittest.main()
