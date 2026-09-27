#!/usr/bin/env python3
"""整版模板迁移的有界正例/安全负例；不修改 Git 或真实研究数据。"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_web_pr_diff as validator


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class TemplateReleaseDiffTests(unittest.TestCase):
    def setUp(self):
        self.contract = {"problem_id": "problem:template-placeholder", "lifecycle": "draft",
                         "acceptance": {"policy": "solution-admission-v1"}}
        identity = {"full_name": "vibemathing/template", "default_branch": "main", "visibility": "public",
                    "binding_state": "planned", "database_id": None, "node_id": None}
        problem = {"problem_id": self.contract["problem_id"], "lifecycle": "draft",
                   "admission": "preview_unadmitted", "contract_sha256": digest(self.contract)}
        self.old = {"harness_version": "1.0.0", "repository": "vibemathing/template",
                    "repository_identity": dict(identity), "problem": dict(problem), "tree_sha256": "a" * 64,
                    "source": {"worktree_dirty": False, "source_manifest_sha256": "f" * 64}, "files": []}
        self.truncate_history = False
        self.tamper_history_tail = False
        raw = b"print('fixture')\n"
        self.raw = raw
        entry = {"owner": "harness", "path": "scripts/new.py", "mode": "0644",
                 "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        self.new = {**self.old, "harness_version": "1.1.0", "tree_sha256": "c" * 64,
                    "files": [entry]}
        self.entries = [("A", ["scripts/new.py"]), ("M", ["HARNESS_SNAPSHOT.json"]),
                        ("M", ["HARNESS_SNAPSHOT_HISTORY.json"])]
        self.solutions = {"generated_at": "1970-01-01T00:00:00Z", "schema_version": "2.0.0", "result_ids": []}
        self.inert = b""

    def run_gate(self, branch="maintenance/template-release-1.1.0", actor="vibemathing", mode_override=None):
        def encoded(value):
            return json.dumps(value, ensure_ascii=False, sort_keys=True).encode()

        previous = {"harness_snapshot_sha256": hashlib.sha256(encoded(self.old)).hexdigest(),
                    "harness_version": self.old["harness_version"], "tree_sha256": "a" * 64,
                    "source_manifest_sha256": "f" * 64, "importer_policy_sha256": "b" * 64}
        latest = {"harness_snapshot_sha256": hashlib.sha256(encoded(self.new)).hexdigest(),
                  "harness_version": self.new["harness_version"], "tree_sha256": "c" * 64,
                  "source_manifest_sha256": "f" * 64,
                  "importer_policy_sha256": hashlib.sha256(b"importer fixture").hexdigest()}

        def json_at(root, rev, path):
            if path == "HARNESS_SNAPSHOT.json":
                return self.old if rev == "BASE" else self.new
            if path == "HARNESS_SNAPSHOT_HISTORY.json":
                head_tail = {**latest, "tree_sha256": "0" * 64} if self.tamper_history_tail else latest
                return {"repository": "vibemathing/template", "repository_identity":
                        {key: self.old["repository_identity"][key]
                         for key in ("database_id", "node_id", "default_branch", "visibility")},
                        "entries": [previous] if rev == "BASE" or self.truncate_history else [previous, head_tail]}
            if path == "problem-library/records/canonical-problems.jsonl":
                return self.contract
            if path == "result-library/indexes/solutions.json":
                return self.solutions
            raise AssertionError(path)

        def git(root, *args, binary=False):
            if args == ("show", "HEAD:problem-library/records/problems.jsonl"):
                return self.inert
            if args == ("show", "HEAD:scripts/new.py"):
                return self.raw
            if args in (("show", "HEAD:HARNESS_SNAPSHOT.json"), ("show", "BASE:HARNESS_SNAPSHOT.json")):
                return encoded(self.new if args[1].startswith("HEAD:") else self.old)
            if args == ("show", "HEAD:scripts/import_web_attempt.py"):
                return b"importer fixture"
            raise AssertionError(args)

        def mode(root, rev, path):
            if path == "scripts/new.py":
                return mode_override or "100644", len(self.raw)
            return "100644", 3

        with patch.object(validator, "changed_paths", return_value=self.entries), \
             patch.object(validator, "json_at_revision", side_effect=json_at), \
             patch.object(validator, "git", side_effect=git), \
             patch.object(validator, "tree_mode_and_size", side_effect=mode):
            return validator.validate(Path("/unused"), "BASE", "HEAD", branch, actor)

    def test_valid_bounded_template_upgrade(self):
        self.assertEqual(self.run_gate(), [])

    def test_untrusted_actor_and_invalid_branch(self):
        self.assertTrue(any("not trusted" in e for e in self.run_gate(actor="someone-else")))
        self.assertTrue(any("invalid" in e for e in self.run_gate(branch="maintenance/template-release-")))
        self.assertTrue(any("must match" in e for e in self.run_gate(branch="maintenance/template-release-9.9.9")))

    def test_candidate_path_never_selects_template_route(self):
        # 不要把候选 PR 错送宽于候选 allowlist 的模板分支。
        with patch.object(validator, "validate_template_release", side_effect=AssertionError("route escaped")), \
             patch.object(validator, "changed_paths", return_value=[]), \
             patch.object(validator, "load_json", return_value={}), \
             patch.object(validator, "git", return_value=""):
            errors = validator.validate(Path("/unused"), "BASE", "HEAD", "web/attempt-unsafe", "vibemathing")
        self.assertTrue(errors)

    def test_changed_truth_or_untracked_path_rejected(self):
        self.entries.append(("A", ["research/records/evidence-links.jsonl"]))
        self.assertTrue(any("research truth" in e for e in self.run_gate()))
        self.entries[-1] = ("A", ["scripts/not-in-snapshot.py"])
        self.assertTrue(any("not snapshot-owned" in e for e in self.run_gate()))

    def test_rename_membership_is_checked_on_both_sides(self):
        self.old["files"] = [{**self.new["files"][0], "path": "scripts/legacy.py"}]
        self.entries[0] = ("R100", ["scripts/legacy.py", "scripts/new.py"])
        self.assertEqual(self.run_gate(), [])
        self.entries[0] = ("R100", ["research/records/evidence-links.jsonl", "scripts/new.py"])
        self.assertTrue(any("research truth" in e for e in self.run_gate()))

    def test_missing_snapshot_member_and_digest_drift_rejected(self):
        self.entries.pop(0)
        self.assertTrue(any("missing paths" in e for e in self.run_gate()))
        self.entries.insert(0, ("A", ["scripts/new.py"]))
        self.new["files"][0]["sha256"] = "0" * 64
        self.assertTrue(any("member drift" in e for e in self.run_gate()))

    def test_template_never_admits_problem_or_results(self):
        self.contract["lifecycle"] = "active"
        self.assertTrue(any("draft placeholder" in e for e in self.run_gate()))
        self.contract["lifecycle"] = "draft"
        self.solutions["result_ids"] = ["fake"]
        self.assertTrue(any("solution index" in e for e in self.run_gate()))
        self.solutions["result_ids"] = []
        self.inert = b"{}\n"
        self.assertTrue(any("ledger must remain empty" in e for e in self.run_gate()))

    def test_base_contract_drift_rejected(self):
        self.old["problem"]["contract_sha256"] = "0" * 64
        self.assertTrue(any("base contract digest mismatch" in e for e in self.run_gate()))

    def test_history_truncation_rejected(self):
        self.truncate_history = True
        self.assertTrue(any("append exactly one" in e for e in self.run_gate()))

    def test_history_tail_drift_rejected(self):
        self.tamper_history_tail = True
        self.assertTrue(any("append exactly one" in e for e in self.run_gate()))

    def test_symlink_and_nonincreasing_version_rejected(self):
        self.new["harness_version"] = "1.0.0"
        self.assertTrue(any("increase" in e for e in self.run_gate()))
        self.new["harness_version"] = "1.1.0"
        self.assertTrue(any("requires regular file" in e for e in self.run_gate(mode_override="120000")))


if __name__ == "__main__":
    unittest.main()
