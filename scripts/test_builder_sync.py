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

from build_problem_repository import BUILDER_VERSION, enforce_public_rights, history_to_continue, read_suite_version
from validate_web_problem_harness import validate_pi_goal_npm_cache

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

    def test_same_repository_history_continuation_preserves_old_entries_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-history-continuation-") as directory:
            source = Path(directory)
            snapshot_path = source / "HARNESS_SNAPSHOT.json"
            history_path = source / "HARNESS_SNAPSHOT_HISTORY.json"
            shutil.copy2(ROOT / snapshot_path.name, snapshot_path)
            shutil.copy2(ROOT / history_path.name, history_path)
            prior = json.loads(history_path.read_text(encoding="utf-8"))
            incoming = json.loads(snapshot_path.read_text(encoding="utf-8"))
            incoming["harness_version"] = "999.0.0"
            expected = history_to_continue(source, incoming, "0" * 64)
            self.assertEqual(expected, prior["entries"])
            self.assertGreater(len(expected), 1, "existing release history must not reset to one entry")
            incoming["problem"]["problem_id"] = "problem:other"
            with self.assertRaisesRegex(RuntimeError, "same repository/problem"):
                history_to_continue(source, incoming, "0" * 64)
            incoming["problem"]["problem_id"] = "problem:template-placeholder"
            prior["entries"][-1]["harness_snapshot_sha256"] = "0" * 64
            history_path.write_text(json.dumps(prior), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not bound"):
                history_to_continue(source, incoming, "0" * 64)

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
            # 新问题仓默认从一条历史开始；仅显式同仓升级才续接已有历史。
            history = json.loads((output / "HARNESS_SNAPSHOT_HISTORY.json").read_text(encoding="utf-8"))
            self.assertEqual(len(history["entries"]), 1)
            pi_settings = json.loads((output / ".pi/settings.json").read_text(encoding="utf-8"))
            self.assertEqual(pi_settings["packages"], ["npm:pi-goal-x@0.31.9"])
            self.assertEqual(len(pi_settings["skills"]), 10)
            self.assertNotIn("hook", json.dumps(pi_settings).lower())
            self.assertNotIn("pi-goal-operator", json.dumps(pi_settings))
            operator = output / ".pi/opt-in-skills/pi-goal-operator/SKILL.md"
            self.assertTrue(operator.is_file())
            self.assertIn("disable-model-invocation: true", operator.read_text(encoding="utf-8"))
            defaults_path = output / ".pi/pi-goal-x-settings.json"
            defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
            self.assertTrue(defaults["disableTasks"])
            self.assertFalse(defaults["autoSelectSingleGoal"])
            self.assertEqual(defaults["networkRecovery"]["maxAttempts"], 3)
            self.assertIn(".pi/goals/", (output / ".gitignore").read_text(encoding="utf-8"))
            command = [sys.executable, str(output / "scripts/validate_web_problem_harness.py"),
                       "--project-root", str(output)]
            defaults["disableTasks"] = False
            defaults_path.write_text(json.dumps(defaults), encoding="utf-8")
            drift = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertNotEqual(drift.returncode, 0)
            self.assertIn("Pi Goal project defaults drift", drift.stderr)
            defaults_path.write_bytes((ROOT / ".pi/pi-goal-x-settings.json").read_bytes())
            pi_settings["packages"] = ["npm:pi-goal-x"]
            (output / ".pi/settings.json").write_text(json.dumps(pi_settings), encoding="utf-8")
            invalid = subprocess.run(
                command, cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("Pi Goal package must be pinned", invalid.stderr)

    def test_goal_runtime_cannot_enter_public_snapshot(self) -> None:
        ignored = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "--quiet", "--", ".pi/goals/active_goal_test.md"],
            capture_output=True, check=False,
        )
        self.assertEqual(ignored.returncode, 0, "local Goal records must not be staged by default")
        with tempfile.TemporaryDirectory(prefix="vibe-goal-runtime-") as directory:
            output = Path(directory) / "out"
            built = subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                 "--project-root", str(ROOT),
                 "--problem-file", str(ROOT / "problem-library/records/canonical-problems.jsonl"),
                 "--repository", "vibemathing/vibe-mathing-problem-public-template",
                 "--visibility", "public", "--output", str(output),
                 "--allow-dirty-source", "--allow-draft-problem", "--allow-unadmitted-problem",
                 "--allow-planned-repository-identity", "--json"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            goal_root = output / ".pi/goals"
            goal_root.mkdir()
            (goal_root / "active_goal_test.md").write_text("test-only runtime goal\n", encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, str(output / "scripts/validate_web_problem_harness.py"),
                 "--project-root", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("Goal runtime state must live outside", rejected.stderr)

    def test_builder_rejects_directory_symlink_in_template(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-template-symlink-") as directory:
            working = Path(directory)
            source = working / "template"
            flags = [
                "--project-root", str(ROOT),
                "--problem-file", str(ROOT / "problem-library/records/canonical-problems.jsonl"),
                "--repository", "vibemathing/vibe-mathing-problem-public-template",
                "--visibility", "public", "--allow-dirty-source", "--allow-draft-problem",
                "--allow-unadmitted-problem", "--allow-planned-repository-identity", "--json",
            ]
            first = subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                 *flags, "--output", str(source)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            (source / "review-symlink-dir").symlink_to("research", target_is_directory=True)
            rejected = subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                 *flags, "--template", str(source), "--output", str(working / "blocked")],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("unsafe problem repository template member", rejected.stderr)

    def test_installed_goal_cache_needs_git_ignore_and_reviewed_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="vibe-goal-cache-") as directory:
            root = Path(directory)
            (root / ".gitignore").write_text(".pi/npm/\n", encoding="utf-8")
            package = root / ".pi/npm/node_modules/pi-goal-x"
            reviewed = Path.home() / ".pi/agent/npm/node_modules/pi-goal-x"
            if reviewed.is_dir():
                shutil.copytree(reviewed, package)
            else:
                (package / "extensions").mkdir(parents=True)
                (package / "package.json").write_text(json.dumps({
                    "name": "pi-goal-x", "version": "0.31.9",
                    "pi": {"extensions": ["extensions/goal.ts"]},
                }), encoding="utf-8")
                (package / "extensions/goal.ts").write_text("// fixture only\n", encoding="utf-8")
            allowed, errors = validate_pi_goal_npm_cache(root)
            self.assertFalse(allowed)
            self.assertIn("requires a Git index", " ".join(errors))
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            ignored = subprocess.run(
                ["git", "-C", str(root), "check-ignore", "--quiet", "--", ".pi/npm/.gitignore"],
                check=False, capture_output=True,
            )
            self.assertEqual(ignored.returncode, 0)
            allowed, errors = validate_pi_goal_npm_cache(root)
            if reviewed.is_dir():
                self.assertTrue(allowed, errors)
                (package / "LICENSE").chmod(0o666)
                allowed, errors = validate_pi_goal_npm_cache(root)
                self.assertFalse(allowed)
                self.assertIn("group/world writable", " ".join(errors))
                (package / "LICENSE").chmod(0o644)
            else:
                self.assertFalse(allowed)
                self.assertIn("unexpected members", " ".join(errors))
            with (package / "LICENSE").open("a", encoding="utf-8") as sink:
                sink.write("fixture-drift\n")
            allowed, errors = validate_pi_goal_npm_cache(root)
            self.assertFalse(allowed)
            self.assertIn("content digest differs" if reviewed.is_dir() else "unexpected members", " ".join(errors))
            subprocess.run(
                ["git", "-C", str(root), "add", "-f", "--", ".pi/npm/node_modules/pi-goal-x/LICENSE"],
                check=True, capture_output=True,
            )
            allowed, errors = validate_pi_goal_npm_cache(root)
            self.assertFalse(allowed)
            self.assertIn("no tracked files", " ".join(errors))
            (package / ".vibemathing-package-manifest.json").write_text("{}\n", encoding="utf-8")
            allowed, errors = validate_pi_goal_npm_cache(root)
            self.assertFalse(allowed)
            self.assertIn("unexpected members", " ".join(errors))
            (package.parent / "unreviewed-package").mkdir()
            allowed, errors = validate_pi_goal_npm_cache(root)
            self.assertFalse(allowed)
            self.assertIn("unreviewed sibling package", " ".join(errors))

    def test_builder_does_not_copy_verified_local_goal_install(self) -> None:
        reviewed = Path.home() / ".pi/agent/npm/node_modules/pi-goal-x"
        if not reviewed.is_dir():
            self.skipTest("Pi Goal package unavailable; independent cache-boundary test still runs")
        with tempfile.TemporaryDirectory(prefix="vibe-goal-build-") as directory:
            working = Path(directory)
            source = working / "source"
            flags = ["--repository", "vibemathing/vibe-mathing-problem-public-template",
                     "--visibility", "public", "--allow-dirty-source", "--allow-draft-problem",
                     "--allow-unadmitted-problem", "--allow-planned-repository-identity", "--json"]
            first = subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_problem_repository.py"),
                 "--project-root", str(ROOT),
                 "--problem-file", str(ROOT / "problem-library/records/canonical-problems.jsonl"),
                 "--output", str(source), *flags],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            subprocess.run(["git", "init", "-q", str(source)], check=True, capture_output=True)
            npm_root = source / ".pi/npm"
            (npm_root / "node_modules").mkdir(parents=True)
            (npm_root / ".gitignore").write_text("*\n!.gitignore\n", encoding="utf-8")
            shutil.copytree(reviewed, npm_root / "node_modules/pi-goal-x")
            def rebuild(destination: Path) -> subprocess.CompletedProcess[str]:
                return subprocess.run(
                    [sys.executable, str(source / "scripts/build_problem_repository.py"),
                     "--project-root", str(source), "--template", str(source),
                     "--source-manifest", str(source / "governance/control-plane/harness-source-manifest.v1.json"),
                     "--problem-file", str(source / "problem-library/records/canonical-problems.jsonl"),
                     "--output", str(destination), *flags],
                    cwd=ROOT, text=True, capture_output=True, check=False,
                )
            exported = working / "export"
            second = rebuild(exported)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse((exported / ".pi/npm").exists())
            with (npm_root / "node_modules/pi-goal-x/LICENSE").open("a", encoding="utf-8") as sink:
                sink.write("canary-drift\n")
            blocked = working / "blocked"
            rejected = rebuild(blocked)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("unsafe Pi Goal install cache in template", rejected.stderr)
            self.assertFalse(blocked.exists(), "package drift must fail before creating output")

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
