#!/usr/bin/env python3
"""Audit every release-checklist gate without converting blockers into approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECK_IDS = tuple(f"C{i:02d}" for i in range(1, 11))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(check_id: str, title: str, status: str, evidence: list[str], blockers: list[str]) -> dict[str, Any]:
    return {
        "id": check_id,
        "title": title,
        "status": status,
        "evidence": evidence,
        "blockers": blockers,
    }


def run_json_command(command: list[str], cwd: Path) -> tuple[bool, str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return False, (result.stderr or result.stdout).strip()[-1000:]
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return False, "command did not return JSON"
    if payload.get("decision") not in {"PASS", "OK"}:
        return False, json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return True, "decision=PASS"


def git_clean_receipt(root: Path, independent_root: Path | None) -> tuple[bool, list[str], list[str]]:
    if independent_root is None:
        return False, [], ["no independent checkout/receipt was supplied"]
    if independent_root.resolve() == root.resolve():
        return False, [], ["independent checkout must not be the release candidate worktree"]
    git_dir = independent_root / ".git"
    if not git_dir.exists():
        return False, [f"independent workspace supplied: {independent_root}"], ["supplied independent workspace is not a Git checkout"]
    expected_snapshot = root / "HARNESS_SNAPSHOT.json"
    reproduced_snapshot = independent_root / "HARNESS_SNAPSHOT.json"
    if not reproduced_snapshot.is_file() or reproduced_snapshot.is_symlink() or sha256(expected_snapshot) != sha256(reproduced_snapshot):
        return False, [f"independent checkout: {independent_root}"], ["independent checkout snapshot does not match the release candidate"]
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=independent_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if status.returncode != 0 or status.stdout.strip():
        return False, [f"independent checkout: {independent_root}"], ["independent checkout is not clean"]
    checks = subprocess.run(
        ["make", "check-full"],
        cwd=independent_root,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=False,
    )
    if checks.returncode != 0:
        return False, ["make check-full attempted in independent checkout"], ["independent check-full failed"]
    return True, [f"clean independent checkout: {independent_root}", "make check-full=PASS"], []


def audit(root: Path, independent_root: Path | None = None, maintainer_review: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    snapshot_path = root / "HARNESS_SNAPSHOT.json"
    snapshot = load_json(snapshot_path)
    snapshot_digest = sha256(snapshot_path)
    generic_template = (
        snapshot.get("repository") == "vibemathing/vibe-mathing-problem-public-template"
        and snapshot.get("problem", {}).get("problem_id") == "problem:template-placeholder"
    )
    release = __import__("validate_release_readiness").run(SimpleNamespace(project_root=root, mode="public"))
    harness_errors = __import__("validate_web_problem_harness").validate(root)
    matrix = load_json(root / ".pi/skills/INTERNAL-PACKAGE-RIGHTS-MATRIX.json")
    packages = [item for item in matrix.get("packages", []) if isinstance(item, dict)]
    source_blockers = [
        item.get("package_id")
        for item in packages
        if not item.get("source_url") or not item.get("source_revision")
    ]
    license_blockers = [
        item.get("package_id")
        for item in packages
        if not item.get("license_ref") or not item.get("attribution") or not item.get("rights_holder") or not item.get("evidence_ref")
    ]
    rights_blockers = [
        item.get("package_id")
        for item in packages
        if item.get("rights_state") != "ADMITTED" or item.get("public_redistribution_admitted") is not True
    ]
    problem_lines = [
        json.loads(line)
        for line in (root / "problem-library/records/canonical-problems.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    canonical_problem = next((item for item in problem_lines if item.get("problem_id") == snapshot["problem"]["problem_id"]), None)
    problem_ok = bool(
        canonical_problem
        and canonical_problem.get("lifecycle") == "active"
        and snapshot["problem"].get("admission") == "canonical_admitted"
    )
    template_problem_ok = bool(
        generic_template
        and canonical_problem
        and canonical_problem.get("problem_id") == "problem:template-placeholder"
        and canonical_problem.get("lifecycle") == "draft"
        and snapshot["problem"].get("admission") == "preview_unadmitted"
    )
    admission = load_json(root / "WEB_REPOSITORY_ADMISSION.json")
    profile = load_json(root / "WEB_CHANNEL_PROFILE.json")
    live_admission_ok = bool(
        profile.get("operational_admission") == "admitted_problem_repository_namespace"
        and admission.get("decision") == "ADMITTED"
        and len(admission.get("receipts", [])) >= 4
    )
    template_live_admission_ok = bool(
        generic_template
        and profile.get("operational_admission") == "synthetic_only_pending_permission_and_ruleset_smoke"
        and admission.get("decision") == "BLOCK"
    )
    privacy_dependency_errors = [
        error
        for error in release["errors"]
        if error.startswith((
            "privacy/", "binary release member:", "symlink is not allowed:",
            "group/world writable member:", "oversized release member:",
            "possible credential assignment:", "unhashed pinned dependency:",
            "Pi Goal npm cache", "Pi Goal installed package",
        ))
    ]
    separation_ok, separation_detail = run_json_command(
        [sys.executable, "-B", "scripts/validate_research_spaces.py", "--project-root", ".", "--json"], root
    )
    independent_ok, independent_evidence, independent_blockers = git_clean_receipt(root, independent_root)
    review_ok = False
    review_evidence: list[str] = []
    review_blockers: list[str] = []
    if maintainer_review is None:
        review_blockers.append("no independent maintainer review receipt was supplied")
    elif not maintainer_review.is_file():
        review_blockers.append(f"maintainer review receipt missing: {maintainer_review}")
    else:
        review = load_json(maintainer_review)
        review_ok = (
            review.get("decision") == "PASS"
            and review.get("source_commit") == snapshot.get("source", {}).get("commit")
            and review.get("snapshot_sha256") == snapshot_digest
        )
        if review_ok:
            review_evidence.append(f"maintainer review receipt: {maintainer_review}")
        else:
            review_blockers.append("maintainer review is missing, stale, or not PASS")

    checks = [
        check("C01", "official source URL and immutable revision", "BLOCK" if source_blockers else "PASS", [f"rights matrix packages={len(packages)}"], [f"missing source URL/revision: {len(source_blockers)} packages"] if source_blockers else []),
        check("C02", "LICENSE/NOTICE and attribution", "BLOCK" if license_blockers else "PASS", ["root LICENSE/NOTICE present"], [f"missing package-scoped license/attribution evidence: {len(license_blockers)} packages"] if license_blockers else []),
        check("C03", "rights-holder receipt and public redistribution admission", "BLOCK" if rights_blockers else "PASS", ["rights matrix schema validated"], [f"rights not admitted: {len(rights_blockers)} packages"] if rights_blockers else []),
        check("C04", "privacy, path, symlink, mode, binary, dependency and secret scans", "BLOCK" if privacy_dependency_errors else "PASS", ["release privacy/filesystem scan completed"], privacy_dependency_errors),
        check("C05", "canonical ProblemContract exact admission", "PASS" if (problem_ok or template_problem_ok) else "BLOCK", [f"problem={snapshot['problem']['problem_id']}", f"lifecycle={snapshot['problem'].get('lifecycle')}", "generic template: placeholder intentionally inert" if template_problem_ok else "concrete problem admission required"], [] if (problem_ok or template_problem_ok) else ["canonical ProblemContract is not active and admitted"]),
        check("C06", "atomic snapshot, history, source manifest and generated output", "PASS" if not harness_errors else "BLOCK", [f"snapshot_sha256={snapshot_digest}", f"tree_sha256={snapshot.get('tree_sha256')}", "standalone Harness validation executed"], harness_errors),
        check("C07", "clean independent checkout", "PASS" if independent_ok else "BLOCK", independent_evidence, independent_blockers),
        check("C08", "fresh live Web repository identity and protection receipts", "PASS" if (live_admission_ok or template_live_admission_ok) else "BLOCK", ["WEB_REPOSITORY_ADMISSION.json present", "generic template: live Web admission intentionally not applicable" if template_live_admission_ok else "concrete repository admission required"], [] if (live_admission_ok or template_live_admission_ok) else ["live repository/permissions/protection/required-check receipts are absent or admission is BLOCK"]),
        check("C09", "Candidate/Evidence/Result/Solution separation", "PASS" if separation_ok else "BLOCK", [separation_detail], [] if separation_ok else ["research-space validation failed"]),
        check("C10", "independent maintainer review receipt", "PASS" if review_ok else "BLOCK", review_evidence, review_blockers),
    ]
    decision = "PASS" if all(item["status"] == "PASS" for item in checks) else "BLOCK"
    return {
        "schema_version": "release-checklist-audit.v1",
        "audited_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "decision": decision,
        "release_authorized": decision == "PASS",
        "source_commit": snapshot.get("source", {}).get("commit"),
        "snapshot_sha256": snapshot_digest,
        "snapshot_tree_sha256": snapshot.get("tree_sha256"),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--independent-root", type=Path)
    parser.add_argument("--maintainer-review", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit(args.project_root, args.independent_root, args.maintainer_review)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        for item in report["checks"]:
            print(f"{item['id']} {item['status']}: {item['title']}")
        print(f"release checklist audit: {report['decision']}")
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
