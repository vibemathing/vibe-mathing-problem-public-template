#!/usr/bin/env python3
"""Fail-closed Git diff gate for candidates, Harness maintenance and template releases."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from vibe_mathing.web_channel import (
    load_json,
    matches_any,
    scan_private_text,
    scan_prohibited_keys,
    validate_packet,
)

MAINTENANCE_BRANCH_PREFIX = "maintenance/harness-"
TEMPLATE_RELEASE_BRANCH_PREFIX = "maintenance/template-release-"
# 模板迁移例外只允许三个不可执行、未准入的占位账本；其余研究真相仍禁止修改。
TEMPLATE_RELEASE_INERT_FILES = {
    "problem-library/records/canonical-problems.jsonl",
    "problem-library/records/problems.jsonl",
    "result-library/indexes/solutions.json",
}
TRUSTED_HARNESS_MAINTAINERS = {"vibemathing"}
GENERATED_HARNESS_FILES = {
    "HARNESS_SNAPSHOT.json",
    "HARNESS_SNAPSHOT_HISTORY.json",
    "WEB_BOOTSTRAP.md",
    "WEB_COORDINATOR.md",
    "WEB_CONTEXT_BUNDLE.md",
    "WEB_CHANNEL_PROFILE.json",
    "WEB_ACTIVE_SKILLS.json",
    "WEB_OUTPUT_CONTRACT.json",
}
MUTABLE_TRUTH_FILES = {
    "problem-library/records/canonical-problems.jsonl",
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
    "result-library/indexes/solutions.json",
}


def git(root: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or "git command failed")
    return result.stdout if binary else result.stdout.decode("utf-8", "strict").strip()


def changed_paths(root: Path, base: str, head: str) -> list[tuple[str, list[str]]]:
    raw = git(root, "diff", "--name-status", "-z", "--find-renames", f"{base}..{head}", binary=True)
    assert isinstance(raw, bytes)
    tokens = raw.decode("utf-8", "strict").split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    changes: list[tuple[str, list[str]]] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        count = 2 if status.startswith(("R", "C")) else 1
        if index + count > len(tokens):
            raise RuntimeError("malformed git name-status output")
        paths = tokens[index:index + count]
        index += count
        changes.append((status, paths))
    return changes


def tree_mode_and_size(root: Path, revision: str, path: str) -> tuple[str | None, int | None]:
    raw = git(root, "ls-tree", "-z", revision, "--", path, binary=True)
    assert isinstance(raw, bytes)
    if not raw:
        return None, None
    line = raw.split(b"\0", 1)[0]
    meta, listed_path = line.split(b"\t", 1)
    mode, object_type, object_id = meta.decode("ascii").split(" ")
    if listed_path.decode("utf-8") != path or object_type != "blob":
        return mode, None
    size = int(git(root, "cat-file", "-s", object_id))
    return mode, size


def json_at_revision(root: Path, revision: str, path: str) -> dict[str, Any]:
    raw = git(root, "show", f"{revision}:{path}", binary=True)
    assert isinstance(raw, bytes)
    value = json.loads(raw.decode("utf-8", "strict"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} at {revision} must be a JSON object")
    return value


def semantic_version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value):
        return None
    major, minor, patch = value.split(".")
    return int(major), int(minor), int(patch)


def harness_owned(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["path"]: item
        for item in snapshot.get("files", [])
        if isinstance(item, dict) and item.get("owner") == "harness" and isinstance(item.get("path"), str)
    }


def validate_harness_maintenance(root: Path, base: str, head: str, branch: str, actor: str) -> list[str]:
    errors: list[str] = []
    if actor not in TRUSTED_HARNESS_MAINTAINERS:
        errors.append(f"Harness maintenance actor is not trusted: {actor or '<missing>'}")
    suffix = branch[len(MAINTENANCE_BRANCH_PREFIX):]
    if not suffix or not re.fullmatch(r"[A-Za-z0-9._-]+", suffix):
        errors.append(f"invalid Harness maintenance branch: {branch}")
    try:
        changes = changed_paths(root, base, head)
        old_snapshot = json_at_revision(root, base, "HARNESS_SNAPSHOT.json")
        new_snapshot = json_at_revision(root, head, "HARNESS_SNAPSHOT.json")
    except (RuntimeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return errors + [str(exc)]
    if not changes:
        return errors + ["Harness maintenance PR has no changed files"]

    old_version = semantic_version(old_snapshot.get("harness_version"))
    new_version = semantic_version(new_snapshot.get("harness_version"))
    if old_version is None or new_version is None or new_version <= old_version:
        errors.append("Harness maintenance must strictly increase semantic harness_version")
    for field in ("repository", "repository_identity", "problem"):
        if old_snapshot.get(field) != new_snapshot.get(field):
            errors.append(f"Harness maintenance cannot change snapshot {field}")
    if new_snapshot.get("source", {}).get("worktree_dirty") is not False:
        errors.append("Harness maintenance source must be a clean committed worktree")

    old_files = harness_owned(old_snapshot)
    new_files = harness_owned(new_snapshot)
    expected = {
        path
        for path in set(old_files) | set(new_files)
        if old_files.get(path) != new_files.get(path)
    }
    actual: set[str] = set()
    for status, paths in changes:
        operation = status[:1]
        if operation not in {"A", "M", "D"} or len(paths) != 1:
            errors.append(f"Harness maintenance allows only non-rename add/modify/delete: {status} {paths}")
        for path in paths:
            if path in actual:
                errors.append(f"duplicate changed path: {path}")
            actual.add(path)
            if path in MUTABLE_TRUTH_FILES or path.startswith("research/artifacts/"):
                errors.append(f"Harness maintenance cannot change mathematical truth/candidate state: {path}")
            if operation == "D":
                continue
            mode, size = tree_mode_and_size(root, head, path)
            if mode not in {"100644", "100755"}:
                errors.append(f"Harness maintenance path must be a regular file: {path}")
            if size is None:
                errors.append(f"Harness maintenance path is not a blob: {path}")
                continue
            if size > 1_048_576:
                errors.append(f"Harness maintenance file exceeds 1048576 bytes: {path}")
            # Harness files contain policy vocabulary (for example prohibited
            # packet keys and privacy-regex fixtures), so candidate-content
            # scanners would create false positives here. The exact snapshot
            # delta, trusted actor, full Harness validator, JSON schemas and
            # coordinator privacy scan are the maintenance controls.
    expected.update(path for path in actual if path in GENERATED_HARNESS_FILES)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"Harness snapshot delta is missing changed paths: {missing}")
    if extra:
        errors.append(f"Harness maintenance changed paths outside regenerated snapshot delta: {extra}")
    if "HARNESS_SNAPSHOT.json" not in actual:
        errors.append("Harness maintenance must regenerate HARNESS_SNAPSHOT.json")
    return errors


def validate_template_release(root: Path, base: str, head: str, branch: str, actor: str) -> list[str]:
    """单独验证整版模板迁移；不改变候选 PR 与日常 Harness 维护路径。"""
    errors: list[str] = []
    suffix = branch[len(TEMPLATE_RELEASE_BRANCH_PREFIX):]
    if not suffix or not re.fullmatch(r"[A-Za-z0-9._-]+", suffix):
        errors.append("invalid template release branch")
    if actor not in TRUSTED_HARNESS_MAINTAINERS:
        errors.append("template release actor is not trusted")
    if errors:
        return errors  # 不可信调用方无需为千文件迁移消耗 Git blob 扫描预算。
    try:
        changes = changed_paths(root, base, head)
        before = json_at_revision(root, base, "HARNESS_SNAPSHOT.json")
        after = json_at_revision(root, head, "HARNESS_SNAPSHOT.json")
        before_history = json_at_revision(root, base, "HARNESS_SNAPSHOT_HISTORY.json")
        after_history = json_at_revision(root, head, "HARNESS_SNAPSHOT_HISTORY.json")
        before_snapshot_bytes = git(root, "show", f"{base}:HARNESS_SNAPSHOT.json", binary=True)
        after_snapshot_bytes = git(root, "show", f"{head}:HARNESS_SNAPSHOT.json", binary=True)
        importer_bytes = git(root, "show", f"{head}:scripts/import_web_attempt.py", binary=True)
        contract = json_at_revision(root, head, "problem-library/records/canonical-problems.jsonl")
        base_contract = json_at_revision(root, base, "problem-library/records/canonical-problems.jsonl")
        inert = git(root, "show", f"{head}:problem-library/records/problems.jsonl", binary=True)
        solutions = json_at_revision(root, head, "result-library/indexes/solutions.json")
    except (RuntimeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return errors + [str(exc)]
    if not changes:
        errors.append("template release has no changed files")
    if len(changes) > 1200:
        errors.append("template release exceeds 1200 changed entries")
    old_version = semantic_version(before.get("harness_version"))
    new_version = semantic_version(after.get("harness_version"))
    if old_version is None or new_version is None or new_version <= old_version:
        errors.append("template release must strictly increase semantic harness_version")
    old_entries = before_history.get("entries")
    new_entries = after_history.get("entries")
    if not isinstance(old_entries, list) or not old_entries or not isinstance(new_entries, list):
        errors.append("template release snapshot history is missing")
    else:
        old_tail = old_entries[-1]
        if not isinstance(old_tail, dict) or old_tail.get("harness_snapshot_sha256") != hashlib.sha256(before_snapshot_bytes).hexdigest():
            errors.append("template release base snapshot history binding mismatch")
        next_entry = {
            "harness_snapshot_sha256": hashlib.sha256(after_snapshot_bytes).hexdigest(),
            "harness_version": after.get("harness_version"),
            "tree_sha256": after.get("tree_sha256"),
            "source_manifest_sha256": after.get("source", {}).get("source_manifest_sha256"),
            "importer_policy_sha256": hashlib.sha256(importer_bytes).hexdigest(),
        }
        if (new_entries != old_entries + [next_entry]
                or before_history.get("repository") != after_history.get("repository")
                or after_history.get("repository") != after.get("repository")
                or before_history.get("repository_identity") != after_history.get("repository_identity")):
            errors.append("template release must append exactly one bound snapshot history entry")
    if suffix != after.get("harness_version"):
        errors.append("template release branch must match new harness_version")
    if before.get("repository") != after.get("repository"):
        errors.append("template release cannot change repository identity")
    old_identity, new_identity = before.get("repository_identity"), after.get("repository_identity")
    if not isinstance(old_identity, dict) or not isinstance(new_identity, dict):
        errors.append("template repository identity missing")
    else:
        for field in ("full_name", "default_branch", "visibility"):
            if old_identity.get(field) != new_identity.get(field):
                errors.append(f"template repository identity drift: {field}")
        if new_identity.get("binding_state") != "planned" or any(new_identity.get(k) is not None for k in ("database_id", "node_id")):
            errors.append("template release identity must be unbound planned")
    source = after.get("source")
    if not isinstance(source, dict) or source.get("worktree_dirty") is not False:
        errors.append("template release source must be a clean committed worktree")
    acceptance = contract.get("acceptance")
    if not isinstance(contract, dict) or contract.get("problem_id") != "problem:template-placeholder" or contract.get("lifecycle") != "draft" or not isinstance(acceptance, dict) or acceptance.get("policy") != "solution-admission-v1":
        errors.append("template release must retain the draft placeholder contract")
    else:
        digest = hashlib.sha256(json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        problem = after.get("problem")
        if not isinstance(problem, dict) or problem.get("problem_id") != contract["problem_id"] or problem.get("lifecycle") != "draft" or problem.get("admission") != "preview_unadmitted" or problem.get("contract_sha256") != digest:
            errors.append("template release snapshot contract digest/identity mismatch")
    if not isinstance(base_contract, dict) or before.get("problem", {}).get("contract_sha256") != hashlib.sha256(json.dumps(base_contract, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest():
        errors.append("template release base contract digest mismatch")
    if inert != b"":
        errors.append("template problem observation ledger must remain empty")
    if solutions.get("result_ids") != [] or set(solutions) != {"generated_at", "schema_version", "result_ids"}:
        errors.append("template solution index must remain empty and inert")
    for snapshot in (before, after):
        problem = snapshot.get("problem", {})
        if not isinstance(problem, dict) or problem.get("problem_id") != "problem:template-placeholder" or problem.get("lifecycle") != "draft" or problem.get("admission") != "preview_unadmitted":
            errors.append("template release base/head must both be unadmitted drafts")
    old_files, new_files = harness_owned(before), harness_owned(after)
    expected = {path for path in old_files.keys() | new_files.keys() if old_files.get(path) != new_files.get(path)}
    actual: set[str] = set()
    changed_bytes = 0
    for status, paths in changes:
        op = status[:1]
        if op not in {"A", "M", "D", "R"} or len(paths) != (2 if op == "R" else 1):
            errors.append(f"template release allows only add/modify/delete/rename: {status} {paths}")
        for path in paths:
            if path in actual:
                errors.append(f"duplicate template release path: {path}")
            actual.add(path)
            if path.startswith("research/artifacts/") or (path in MUTABLE_TRUTH_FILES and path not in TEMPLATE_RELEASE_INERT_FILES):
                errors.append(f"template release cannot change research truth/candidate state: {path}")
            if path not in old_files and path not in new_files and path not in GENERATED_HARNESS_FILES and path not in TEMPLATE_RELEASE_INERT_FILES:
                errors.append(f"template release path is not snapshot-owned or explicitly inert: {path}")
            # 重命名只检查新路径的模式/摘要；旧路径在下方的 expected/actual 集合中核对。
            if op == "D" or (op == "R" and path == paths[0]):
                continue
            mode, size = tree_mode_and_size(root, head, path)
            if mode not in {"100644", "100755"} or size is None:
                errors.append(f"template release requires regular file: {path}")
                continue
            changed_bytes += size
            if size > 1_048_576:
                errors.append(f"template release file exceeds 1048576 bytes: {path}")
            entry = new_files.get(path)
            if entry is not None:
                raw = git(root, "show", f"{head}:{path}", binary=True)
                assert isinstance(raw, bytes)
                if entry.get("sha256") != hashlib.sha256(raw).hexdigest() or entry.get("bytes") != size or entry.get("mode") != ("0" + mode[-3:]):
                    errors.append(f"template release snapshot member drift: {path}")
    if changed_bytes > 8_388_608:
        errors.append("template release total changed bytes exceeds 8388608")
    expected.update(path for path in actual if path in GENERATED_HARNESS_FILES or path in TEMPLATE_RELEASE_INERT_FILES)
    if "HARNESS_SNAPSHOT.json" not in actual or "HARNESS_SNAPSHOT_HISTORY.json" not in actual:
        errors.append("template release must regenerate snapshot and history")
    if expected - actual:
        errors.append(f"template release snapshot delta missing paths: {sorted(expected - actual)[:5]}")
    if actual - expected:
        errors.append(f"template release extra paths: {sorted(actual - expected)[:5]}")
    return errors


def validate(root: Path, base: str, head: str, branch: str, actor: str | None = None) -> list[str]:
    errors: list[str] = []
    if branch.startswith(MAINTENANCE_BRANCH_PREFIX):
        return validate_harness_maintenance(root, base, head, branch, actor or "")
    if branch.startswith(TEMPLATE_RELEASE_BRANCH_PREFIX):
        return validate_template_release(root, base, head, branch, actor or "")
    try:
        profile = load_json(root / "WEB_CHANNEL_PROFILE.json")
        output_contract = load_json(root / "WEB_OUTPUT_CONTRACT.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot load web control files: {exc}"]
    branch_policy = profile.get("branch_policy", {})
    if not branch.startswith(str(branch_policy.get("prefix", "web/attempt-"))):
        errors.append(f"candidate branch must match web/attempt-*: {branch}")
    if branch in branch_policy.get("protected", []):
        errors.append(f"protected branch is forbidden: {branch}")

    try:
        changes = changed_paths(root, base, head)
    except (RuntimeError, UnicodeDecodeError) as exc:
        return errors + [str(exc)]
    if not changes:
        errors.append("candidate PR has no changed files")
        return errors

    max_files = int(output_contract.get("limits", {}).get("max_files_per_pull_request", 64))
    max_file_bytes = int(output_contract.get("limits", {}).get("max_file_bytes", 1_048_576))
    max_total = int(output_contract.get("limits", {}).get("max_total_changed_bytes", 8_388_608))
    if len(changes) > max_files:
        errors.append(f"changed-file count exceeds {max_files}")

    allowed = profile.get("allowed_repository_write_paths", [])
    prohibited = profile.get("prohibited_repository_write_paths", [])
    total = 0
    packet_paths: list[str] = []
    seen: set[str] = set()
    for status, paths in changes:
        operation = status[:1]
        if operation not in {"A", "M", "D"}:
            errors.append(f"web PR allows only add/modify/delete inside candidate paths; status {status} is forbidden for {paths}")
        for path in paths:
            if path in seen:
                errors.append(f"duplicate changed path: {path}")
            seen.add(path)
            if not matches_any(path, allowed):
                errors.append(f"changed path outside allowlist: {path}")
            if matches_any(path, prohibited):
                errors.append(f"changed path is prohibited: {path}")
            if operation != "D" and path.startswith("research/artifacts/web-inbox/") and path.endswith(".json"):
                packet_paths.append(path)
            if operation == "D":
                continue
            mode, size = tree_mode_and_size(root, head, path)
            if mode != "100644":
                errors.append(f"changed path must be a regular non-executable file, got mode {mode}: {path}")
            if size is None:
                errors.append(f"changed path is not a blob: {path}")
                continue
            total += size
            if size > max_file_bytes:
                errors.append(f"changed file exceeds {max_file_bytes} bytes: {path}")
            raw = git(root, "show", f"{head}:{path}", binary=True)
            assert isinstance(raw, bytes)
            try:
                text = raw.decode("utf-8", "strict")
            except UnicodeDecodeError:
                errors.append(f"binary web artifact forbidden: {path}")
                continue
            for label in scan_private_text(text):
                errors.append(f"privacy finding {label}: {path}")
            if path.endswith(".json"):
                try:
                    value: Any = json.loads(text)
                except json.JSONDecodeError as exc:
                    errors.append(f"invalid JSON {path}: {exc}")
                else:
                    errors.extend(f"{path}: {message}" for message in scan_prohibited_keys(value))
    if total > max_total:
        errors.append(f"total changed bytes exceeds {max_total}")
    if len(packet_paths) != 1:
        errors.append(f"candidate PR must add exactly one web attempt packet, found {len(packet_paths)}")
    elif head == "HEAD":
        packet, packet_errors = validate_packet(root, root / packet_paths[0])
        errors.extend(f"{packet_paths[0]}: {message}" for message in packet_errors)
        if packet and packet.get("transport", {}).get("branch") != branch:
            errors.append("packet transport branch does not match PR branch")
        if packet:
            actual_base = str(git(root, "rev-parse", base))
            if packet.get("base_revision") != actual_base:
                errors.append("packet base_revision does not match PR base")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a role-specific pull request diff.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--branch", default=os.environ.get("GITHUB_HEAD_REF", ""))
    parser.add_argument("--actor", default=os.environ.get("GITHUB_ACTOR", ""))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    branch = args.branch
    if not branch:
        try:
            branch = str(git(root, "branch", "--show-current"))
        except RuntimeError:
            branch = ""
    errors = validate(root, args.base, args.head, branch, args.actor)
    report = {"decision": "PASS" if not errors else "BLOCK", "base": args.base, "head": args.head, "branch": branch, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"web PR diff validation: {report['decision']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
