#!/usr/bin/env python3
"""Regression tests for builder/sync fail-closed publication controls."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_problem_repository import enforce_public_rights

ROOT = Path(__file__).resolve().parents[1]


class BuilderSyncTests(unittest.TestCase):
    def test_builder_has_public_rights_gate_and_runtime_cleanup(self) -> None:
        text = (ROOT / "scripts/build_problem_repository.py").read_text(encoding="utf-8")
        self.assertIn("enforce_public_rights", text)
        self.assertIn("remove_runtime_noise", text)
        self.assertIn('args.visibility == "public"', text)

    def test_sync_binds_target_ledger_and_rejects_apply_bypasses(self) -> None:
        text = (ROOT / "scripts/sync_problem_repository_harness.py").read_text(encoding="utf-8")
        self.assertIn('"--canonical-ledger", str(target / "problem-library/records/canonical-problems.jsonl")', text)
        self.assertIn("development bypass flags are forbidden for --apply", text)
        self.assertIn("merged_history", text)

    def test_public_body_build_rejects_held_rights_matrix(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-public-rights-") as directory:
            root = Path(directory)
            skills = root / ".pi/skills"
            skills.mkdir(parents=True)
            for name in (
                "INTERNAL-PACKAGE-CLASSIFICATION.json",
                "INTERNAL-PACKAGE-RIGHTS-MATRIX.json",
                "internal-package-rights-matrix.schema.json",
            ):
                shutil.copy2(ROOT / ".pi/skills" / name, skills / name)
            matrix_path = skills / "INTERNAL-PACKAGE-RIGHTS-MATRIX.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["packages"][0]["rights_state"] = "HOLD"
            matrix["packages"][0]["public_redistribution_admitted"] = False
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "public build blocked"):
                enforce_public_rights(root)

    def test_public_body_build_uses_admitted_rights_matrix(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-public-build-") as directory:
            output = Path(directory) / "out"
            result = subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                    "--project-root", str(ROOT),
                    "--problem-file", str(ROOT / "problem-library/records/canonical-problems.jsonl"),
                    "--repository", "vibemathing/vibe-mathing-problem-public-template",
                    "--visibility", "public",
                    "--output", str(output),
                    "--allow-dirty-source", "--allow-draft-problem", "--allow-unadmitted-problem",
                    "--allow-planned-repository-identity", "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["decision"], "PASS")
            self.assertTrue((output / "HARNESS_SNAPSHOT.json").is_file())


if __name__ == "__main__":
    unittest.main()
