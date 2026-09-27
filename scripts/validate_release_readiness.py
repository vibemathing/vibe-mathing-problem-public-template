#!/usr/bin/env python3
"""Fail-closed release, rights, privacy, and publication-boundary audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from validate_web_problem_harness import validate_pi_goal_npm_cache

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".txt", ".yml", ".yaml", ".cff", ".toml", ".in", ".sh"}
REQUIRED_RELEASE_FILES = {"LICENSE", "NOTICE", "CODEOWNERS", "SECURITY.md", "RELEASE-CHECKLIST.md"}
FORBIDDEN_TEXT = (
    "\\\\wsl.localhost", ".private/", "BEGIN OPENSSH",
    "https://github.com/tradecatlabs/vibe-mathing-cn",
)
FORBIDDEN_REGEX = (
    r"(?<![A-Za-z0-9])/(?:home|mnt)/(?:lenovo|13208|Users)/",
    r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}",
    r"(?<![A-Za-z0-9])github_pat_[A-Za-z0-9_]{20,}",
    r"(?<![A-Za-z0-9])sk-[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_files(root: Path, verified_npm_cache: bool = False):
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if verified_npm_cache and relative.parts[:2] == (".pi", "npm"):
            continue  # 受审且未跟踪的 Pi 本地包缓存不是发布成员。
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix == ".pyc":
            continue
        yield path


def rights_audit(root: Path, errors: list[str]) -> None:
    matrix_path = root / ".pi/skills/INTERNAL-PACKAGE-RIGHTS-MATRIX.json"
    schema_path = root / ".pi/skills/internal-package-rights-matrix.schema.json"
    classification_path = root / ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json"
    if not matrix_path.is_file() or not schema_path.is_file() or not classification_path.is_file():
        errors.append("missing package rights matrix, schema, or classification")
        return
    matrix = load(matrix_path)
    schema = load(schema_path)
    errors.extend(
        f"rights matrix schema: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(matrix)
    )
    classification = load(classification_path)
    expected = {item.get("package_id") for item in classification.get("packages", [])}
    actual = {item.get("package_id") for item in matrix.get("packages", [])}
    if expected != actual:
        errors.append(f"rights matrix package set mismatch: expected={sorted(expected)} actual={sorted(actual)}")
    for item in matrix.get("packages", []):
        if item.get("public_redistribution_admitted") is not True or item.get("rights_state") != "ADMITTED":
            errors.append(f"package {item.get('package_id')}: public redistribution is not admitted")
        for field in ("source_url", "source_revision", "license_ref", "attribution", "rights_holder", "evidence_ref"):
            if not item.get(field):
                errors.append(f"package {item.get('package_id')}: missing {field}")


def privacy_audit(root: Path, errors: list[str], verified_npm_cache: bool = False) -> None:
    for path in iter_files(root, verified_npm_cache):
        if path.name == "validate_release_readiness.py":
            continue
        if path.stat().st_size > 8 * 1024 * 1024:
            errors.append(f"oversized release member: {path.relative_to(root)}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"binary release member: {path.relative_to(root)}")
            continue
        except OSError:
            continue
        for marker in FORBIDDEN_TEXT:
            if marker in text:
                errors.append(f"privacy/secret marker {marker!r}: {path.relative_to(root)}")
        for pattern in FORBIDDEN_REGEX:
            if re.search(pattern, text):
                errors.append(f"privacy/secret pattern {pattern!r}: {path.relative_to(root)}")
        if re.search(r"(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}", text, re.I):
            errors.append(f"possible credential assignment: {path.relative_to(root)}")


def filesystem_audit(root: Path, errors: list[str], verified_npm_cache: bool = False) -> None:
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if verified_npm_cache and relative.parts[:2] == (".pi", "npm"):
            continue
        if ".git" in path.parts:
            continue
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {path.relative_to(root)}")
            continue
        try:
            mode = stat.S_IMODE(path.stat().st_mode)
        except OSError:
            continue
        if mode & 0o022:
            errors.append(f"group/world writable member: {path.relative_to(root)} mode={mode:04o}")


def dependency_audit(root: Path, errors: list[str]) -> None:
    for relative in ("requirements.txt", "requirements-math-tools.txt"):
        path = root / relative
        if not path.is_file():
            continue
        active: dict[str, Any] | None = None
        for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("--hash="):
                if active is None:
                    errors.append(f"orphan dependency hash: {relative}:{number}")
                else:
                    active["has_hash"] = True
                continue
            if "==" in line and not line.startswith("-"):
                if active is not None and not active["has_hash"]:
                    errors.append(f"unhashed pinned dependency: {relative}:{active['line']}")
                active = {"line": number, "has_hash": "--hash=" in line}
                continue
            if line.startswith("-"):
                continue
            if active is not None and not active["has_hash"]:
                errors.append(f"unhashed pinned dependency: {relative}:{active['line']}")
            active = None
        if active is not None and not active["has_hash"]:
            errors.append(f"unhashed pinned dependency: {relative}:{active['line']}")


def is_generic_template(root: Path) -> bool:
    snapshot_path = root / "HARNESS_SNAPSHOT.json"
    if not snapshot_path.is_file():
        return False
    try:
        snapshot = load(snapshot_path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    return (
        snapshot.get("repository") == "vibemathing/vibe-mathing-problem-public-template"
        and snapshot.get("problem", {}).get("problem_id") == "problem:template-placeholder"
    )


def profile_audit(root: Path, errors: list[str], generic_template: bool = False) -> None:
    path = root / "WEB_CHANNEL_PROFILE.json"
    if not path.is_file():
        errors.append("missing WEB_CHANNEL_PROFILE.json")
        return
    profile = load(path)
    admission_path = root / "WEB_REPOSITORY_ADMISSION.json"
    admission_schema_path = root / "governance/control-plane/repository-admission-receipt.schema.json"
    if not admission_path.is_file() or not admission_schema_path.is_file():
        errors.append("missing live repository admission receipt/schema")
    else:
        admission = load(admission_path)
        errors.extend(
            f"repository admission receipt: {error.message}"
            for error in Draft202012Validator(load(admission_schema_path), format_checker=FormatChecker()).iter_errors(admission)
        )
        expected = "ADMITTED" if profile.get("operational_admission") == "admitted_problem_repository_namespace" else "BLOCK"
        if admission.get("decision") != expected:
            errors.append("repository admission receipt/profile mismatch")
    pending_words = ("pending", "self_report_only", "planned", "unverified")
    encoded = json.dumps(profile, ensure_ascii=False).lower()
    if generic_template:
        if profile.get("operational_admission") != "synthetic_only_pending_permission_and_ruleset_smoke":
            errors.append("generic template must retain synthetic Web operational admission")
        if admission_path.is_file() and load(admission_path).get("decision") != "BLOCK":
            errors.append("generic template must not claim live Web repository admission")
    else:
        if any(word in encoded for word in pending_words):
            errors.append("WEB_CHANNEL_PROFILE contains pending/self-reported/unverified admission state")
        if profile.get("operational_admission") != "admitted_problem_repository_namespace":
            errors.append("WEB_CHANNEL_PROFILE operational_admission is not the admitted namespace")


def run(args: argparse.Namespace) -> dict[str, Any]:
    root = args.project_root.resolve()
    errors: list[str] = []
    missing = sorted(relative for relative in REQUIRED_RELEASE_FILES if not (root / relative).is_file())
    errors.extend(f"missing release file: {relative}" for relative in missing)
    generic_template = is_generic_template(root)
    verified_npm_cache, cache_errors = validate_pi_goal_npm_cache(root)
    errors.extend(cache_errors)
    rights_audit(root, errors)
    privacy_audit(root, errors, verified_npm_cache)
    filesystem_audit(root, errors, verified_npm_cache)
    dependency_audit(root, errors)
    profile_audit(root, errors, generic_template=generic_template)
    if args.mode == "public":
        classification = root / ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json"
        if classification.is_file():
            packages = load(classification).get("packages", [])
            held = [item.get("package_id") for item in packages if item.get("public_redistribution_admitted") is not True]
            if held:
                errors.append(f"public release contains non-admitted package bodies: {len(held)}")
    return {"decision": "PASS" if not errors else "BLOCK", "mode": args.mode, "errors": errors, "files_scanned": sum(1 for _ in iter_files(root, verified_npm_cache))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--mode", choices=("public", "private"), default="public")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = run(args)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    elif report["decision"] == "PASS":
        print(f"release readiness: PASS files={report['files_scanned']}")
    else:
        for error in report["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"release readiness: BLOCK errors={len(report['errors'])}", file=sys.stderr)
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
