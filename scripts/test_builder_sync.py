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

from build_problem_repository import BUILDER_VERSION, enforce_public_rights, read_suite_version

ROOT = Path(__file__).resolve().parents[1]


class BuilderSyncTests(unittest.TestCase):
    def test_version_file_is_the_single_suite_version_source(self) -> None:
        declared = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads((ROOT / "governance/control-plane/harness-source-manifest.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(read_suite_version(ROOT), declared)
        self.assertEqual(BUILDER_VERSION, declared)
        self.assertEqual(manifest["harness_version"], declared)
        with tempfile.TemporaryDirectory(prefix="vibe-invalid-version-") as directory:
            invalid_root = Path(directory)
            (invalid_root / "VERSION").write_text("latest\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "semantic version"):
                read_suite_version(invalid_root)

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

    def test_live_candidate_is_not_harness_but_unrelated_or_unsafe_members_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-candidate-boundary-") as directory:
            output = Path(directory) / "out"
            built = subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                    "--project-root", str(ROOT),
                    "--problem-file", str(ROOT / "problem-library/records/canonical-problems.jsonl"),
                    "--repository", "vibemathing/vibe-mathing-problem-public-template",
                    "--output", str(output),
                    "--allow-dirty-source", "--allow-draft-problem", "--allow-unadmitted-problem",
                    "--allow-planned-repository-identity", "--json",
                ],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            candidate = output / "research/artifacts/candidates"
            (candidate / "synthetic-observation.txt").write_text("candidate-only; no Result\n", encoding="utf-8")
            command = [sys.executable, str(output / "scripts/validate_web_problem_harness.py"),
                       "--project-root", str(output)]
            valid = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertEqual(valid.returncode, 0, valid.stderr)

            (output / "scripts/foreign.txt").write_text("unlisted Harness mutation\n", encoding="utf-8")
            (candidate / "escape").symlink_to(ROOT / "VERSION")
            (candidate / "binary.bin").write_bytes(b"\xff\x00")
            invalid = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("unlisted snapshot members: scripts/foreign.txt", invalid.stderr)
            self.assertIn("symlink forbidden in problem repository: research/artifacts/candidates/escape", invalid.stderr)
            self.assertIn("binary web artifact forbidden: research/artifacts/candidates/binary.bin", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
