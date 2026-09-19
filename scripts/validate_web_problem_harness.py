#!/usr/bin/env python3
"""Validate a self-contained Web GPT problem-repository Harness snapshot."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from validate_mathematical_reasoning_discipline import validate as validate_reasoning_discipline
from vibe_mathing.reasoning import strip_reasoning_agent_overlay
from vibe_mathing.web_channel import (
    canonical_json_sha256,
    load_json,
    load_jsonl,
    load_problem,
    scan_private_text,
    sha256_file,
    snapshot_file_sha256,
    validate_schema,
)

REQUIRED_CONTROL_FILES = {
    ".gitignore",
    "README.md",
    "Makefile",
    "requirements.txt",
    "requirements-web-harness.txt",
    "AGENTS.md",
    ".github/AGENTS.md",
    ".github/workflows/web-candidate-gate.yml",
    "governance/harness/PROJECT_AGENTS.md",
    "WEB_BOOTSTRAP.md",
    "WEB_COORDINATOR.md",
    "WEB_CONTEXT_BUNDLE.md",
    "WEB_CHANNEL_PROFILE.json",
    "WEB_ACTIVE_SKILLS.json",
    "WEB_OUTPUT_CONTRACT.json",
    "HARNESS_SNAPSHOT.json",
    "HARNESS_SNAPSHOT_HISTORY.json",
    ".pi/AGENTS.md",
    ".pi/settings.json",
    ".pi/skills/README.md",
    ".pi/skills/CONSOLIDATION-MAP.md",
    ".pi/skills/SOURCE-ABSTRACTION-MAP.json",
    ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json",
    ".pi/skills/INTERNAL-PACKAGE-ARCHITECTURE.md",
    "problem-library/records/canonical-problems.jsonl",
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
    "governance/control-plane/mathematical-reasoning-discipline.schema.json",
    "governance/control-plane/mathematical-reasoning-discipline.v1.json",
    "governance/control-plane/math-knowledge-source.v1.json",
    "governance/control-plane/math-knowledge-operators.v1.json",
    "governance/control-plane/harness-source-manifest.v1.json",
    "governance/control-plane/harness-source-manifest.v1.schema.json",
    "governance/control-plane/container-skill-source-lock.v1.json",
    "governance/control-plane/container-skill-source-lock.v1.schema.json",
    "governance/control-plane/harness-snapshot-manifest.v1.schema.json",
    "governance/control-plane/harness-snapshot-history.v1.schema.json",
    "governance/control-plane/web-context-profile.v1.schema.json",
    "governance/control-plane/web-context-profile.v1.json",
    "scripts/build_problem_repository.py",
    "scripts/build_web_context_bundle.py",
    "scripts/sync_problem_repository_harness.py",
    "scripts/validate_mathematical_reasoning_discipline.py",
    "scripts/validate_math_knowledge_registry.py",
    "scripts/validate_web_problem_harness.py",
    "scripts/validate_web_attempt.py",
    "scripts/validate_web_pr_diff.py",
    "scripts/import_web_attempt.py",
    "scripts/test_web_context_bundle.py",
}
FORBIDDEN_PARTS = {".private", ".lake", "sessions", "vendor"}
FORBIDDEN_LOCAL_RUNTIME_FILES = {
    "persistent-worker-checkpoint.schema.json",
    "research-execution-scope.v1.schema.json",
    "resume-session-receipt.schema.json",
}
REQUIRED_EXCLUDED_CONTAINER_SKILLS = {"auto-goal", "auto-tmux", "nvidia-private-compute"}
PRIVATE_REPOSITORY_LOCATOR = re.compile(
    r"\b(?:vibemathing|tradecatlabs)/[A-Za-z0-9_.-]*internal[A-Za-z0-9_.-]*\b"
)
PI_SKILL_STATUS = {
    "solve": "active",
    "mathematics-in-lean": "active",
    "prove2me": "constrained",
    "ai4math-source-discovery": "active",
    "ai4math-modeling-derivation": "active",
    "ai4math-proof-refutation": "active",
    "ai4math-bounded-computation": "constrained",
    "ai4math-lean-formalization": "constrained",
    "ai4math-assurance-admission": "constrained",
    "ai4math-toolchain-reproducibility": "constrained",
}
INTERNAL_PACKAGE_TOP_SKILLS = {
    "mathematics-in-lean",
    "ai4math-source-discovery",
    "ai4math-modeling-derivation",
    "ai4math-proof-refutation",
    "ai4math-bounded-computation",
    "ai4math-lean-formalization",
    "ai4math-assurance-admission",
    "ai4math-toolchain-reproducibility",
}
MUTABLE_RECORDS = {
    "research/records/attempts.jsonl",
    "research/records/failed-routes.jsonl",
    "research/records/obligation-graphs.jsonl",
    "research/records/candidate-artifacts.jsonl",
    "research/records/evidence-links.jsonl",
    "result-library/records/results.jsonl",
}


def tree_digest(files: list[dict[str, Any]]) -> str:
    payload = [
        {key: item[key] for key in ("path", "bytes", "mode", "sha256", "layer", "owner")}
        for item in sorted(files, key=lambda item: item["path"])
    ]
    return canonical_json_sha256(payload)


def content_snapshot(root: Path) -> dict[str, Any]:
    files = [path for path in sorted(root.rglob("*")) if path.is_file() and not path.is_symlink()]
    rows = []
    for path in files:
        relative = path.relative_to(root).as_posix()
        source_bytes = strip_reasoning_agent_overlay(relative, path.read_bytes())
        rows.append({
            "path": relative,
            "bytes": len(source_bytes),
            "sha256": hashlib.sha256(source_bytes).hexdigest(),
        })
    return {
        "files": len(rows),
        "bytes": sum(item["bytes"] for item in rows),
        "tree_sha256": canonical_json_sha256(rows),
    }


def internal_package_snapshot(root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink in internal package: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"non-regular internal package member: {path}")
        if path.parent == root and path.name == ".vibemathing-package-manifest.json":
            continue
        data = path.read_bytes()
        rows.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    digest = hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "files": len(rows),
        "bytes": sum(item["bytes"] for item in rows),
        "tree_sha256": digest,
        "rows": rows,
    }


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative in sorted(REQUIRED_CONTROL_FILES):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"required regular file missing: {relative}")
    errors.extend(f"reasoning discipline: {message}" for message in validate_reasoning_discipline(root))

    try:
        snapshot = load_json(root / "HARNESS_SNAPSHOT.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load Harness snapshot: {exc}"]
    schema_path = root / "governance/control-plane/harness-snapshot-manifest.v1.schema.json"
    if not schema_path.is_file():
        errors.append("missing Harness snapshot schema")
    else:
        errors.extend(f"snapshot schema: {message}" for message in validate_schema(snapshot, schema_path))

    listed = snapshot.get("files", [])
    if not isinstance(listed, list):
        return errors + ["snapshot files must be an array"]
    paths = [item.get("path") for item in listed if isinstance(item, dict)]
    if paths != sorted(paths):
        errors.append("snapshot file list is not sorted")
    if len(paths) != len(set(paths)):
        errors.append("snapshot file list contains duplicates")
    if set(paths) & MUTABLE_RECORDS:
        errors.append("mutable record ledger must not be owned by Harness snapshot")

    for item in listed:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        relative = item["path"]
        path = root / relative
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            errors.append(f"snapshot path missing or escapes root: {relative}")
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"snapshot path is not a regular file: {relative}")
            continue
        actual_mode = "0755" if path.stat().st_mode & 0o111 else "0644"
        if item.get("mode") != actual_mode:
            errors.append(f"mode mismatch: {relative}")
        if item.get("bytes") != path.stat().st_size:
            errors.append(f"size mismatch: {relative}")
        if item.get("sha256") != sha256_file(path):
            errors.append(f"digest mismatch: {relative}")
    if listed and snapshot.get("tree_sha256") != tree_digest(listed):
        errors.append("Harness tree digest mismatch")
    repository_identity = snapshot.get("repository_identity", {})
    if repository_identity.get("full_name") != snapshot.get("repository"):
        errors.append("snapshot repository identity/full name mismatch")
    if repository_identity.get("binding_state") == "verified":
        if not isinstance(repository_identity.get("database_id"), int) or not repository_identity.get("node_id"):
            errors.append("verified repository identity lacks database/node ID")

    try:
        history = load_json(root / "HARNESS_SNAPSHOT_HISTORY.json")
        history_schema = root / "governance/control-plane/harness-snapshot-history.v1.schema.json"
        errors.extend(f"snapshot history schema: {message}" for message in validate_schema(history, history_schema))
        expected_history_identity = {
            key: repository_identity.get(key)
            for key in ("database_id", "node_id", "default_branch", "visibility")
        }
        if history.get("repository") != snapshot.get("repository"):
            errors.append("Harness snapshot history repository mismatch")
        if history.get("repository_identity") != expected_history_identity:
            errors.append("Harness snapshot history repository identity mismatch")
        entries = history.get("entries", [])
        digests = [item.get("harness_snapshot_sha256") for item in entries if isinstance(item, dict)]
        if len(digests) != len(set(digests)):
            errors.append("Harness snapshot history contains duplicate digests")
        current_entry = {
            "harness_snapshot_sha256": sha256_file(root / "HARNESS_SNAPSHOT.json"),
            "harness_version": snapshot.get("harness_version"),
            "tree_sha256": snapshot.get("tree_sha256"),
            "source_manifest_sha256": snapshot.get("source", {}).get("source_manifest_sha256"),
            "importer_policy_sha256": sha256_file(root / "scripts/import_web_attempt.py"),
        }
        if current_entry not in entries:
            errors.append("Harness snapshot history lacks the current snapshot/importer binding")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"Harness snapshot history invalid: {exc}")

    try:
        problem = load_problem(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        problem = None
    if problem is not None:
        problem_schema = root / "problem-library/schema/canonical-problem.schema.json"
        if problem_schema.is_file():
            errors.extend(f"ProblemContract schema: {message}" for message in validate_schema(problem, problem_schema))
        contract_digest = canonical_json_sha256(problem)
        if snapshot.get("problem", {}).get("problem_id") != problem.get("problem_id"):
            errors.append("snapshot Problem ID mismatch")
        if snapshot.get("problem", {}).get("contract_sha256") != contract_digest:
            errors.append("snapshot ProblemContract digest mismatch")
        if snapshot.get("problem", {}).get("lifecycle") != problem.get("lifecycle"):
            errors.append("snapshot Problem lifecycle mismatch")

    try:
        profile = load_json(root / "WEB_CHANNEL_PROFILE.json")
        profile_schema = root / "governance/control-plane/web-research-channel.schema.json"
        errors.extend(f"web profile schema: {message}" for message in validate_schema(profile, profile_schema))
        output_contract = load_json(root / "WEB_OUTPUT_CONTRACT.json")
        if output_contract.get("channel") != profile.get("channel_id"):
            errors.append("WEB_OUTPUT_CONTRACT channel mismatch")
        if output_contract.get("allowed_write_paths") != profile.get("allowed_repository_write_paths"):
            errors.append("WEB_OUTPUT_CONTRACT allowed paths drift")
        if output_contract.get("prohibited_write_paths") != profile.get("prohibited_repository_write_paths"):
            errors.append("WEB_OUTPUT_CONTRACT prohibited paths drift")
        if output_contract.get("autonomy_policy") != profile.get("autonomy_policy"):
            errors.append("WEB_OUTPUT_CONTRACT autonomy policy drift")
        if output_contract.get("repository_scope_policy") != profile.get("repository_scope_policy"):
            errors.append("WEB_OUTPUT_CONTRACT repository scope policy drift")
        expected_maintenance = {
            "branch_prefix": "maintenance/harness-",
            "trusted_actors": ["vibemathing"],
            "exact_regenerated_snapshot_delta_required": True,
            "mathematical_state_changes_allowed": False,
        }
        if output_contract.get("harness_maintenance_policy") != expected_maintenance:
            errors.append("WEB_OUTPUT_CONTRACT Harness maintenance policy drift")
        freshness = output_contract.get("state_freshness_policy", {})
        expected_freshness = {
            "authoritative_state": "fresh_default_branch_and_live_github_objects",
            "historical_chat_is_authoritative": False,
            "design_time_revisions_may_advance": True,
            "audit_maturity_is_repository_admission": False,
            "round_end_is_permission_failure": False,
            "issue_identity_fields": ["problem_id", "attempt_id", "route_id", "obligation_id"],
            "issue_creation": "search_twice_then_create_or_reuse_unique",
        }
        if freshness != expected_freshness:
            errors.append("WEB_OUTPUT_CONTRACT state freshness policy drift")
        if profile.get("operational_admission") != "admitted_problem_repository_namespace":
            errors.append("Web candidate namespace is not operationally admitted")
        required_operations = {
            "issue_create", "candidate_branch_create", "candidate_file_create", "candidate_file_update",
            "candidate_file_delete", "commit_create", "pull_request_create", "pull_request_review",
            "actions_read", "actions_rerun_existing_candidate_run", "pull_request_merge", "checkpoint",
        }
        if set(output_contract.get("allowed_github_operations", [])) != required_operations:
            errors.append("WEB_OUTPUT_CONTRACT lacks AI-native candidate operations")
        if profile.get("github_permissions", {}).get("actions") != "write":
            errors.append("AI-native candidate workflow requires Actions write for rerun")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"web control JSON invalid: {exc}")
        profile = {}

    try:
        context_profile = load_json(root / "governance/control-plane/web-context-profile.v1.json")
        context_profile_schema = root / "governance/control-plane/web-context-profile.v1.schema.json"
        errors.extend(f"execution-context profile: {message}" for message in validate_schema(context_profile, context_profile_schema))
        bundle_path = root / "WEB_CONTEXT_BUNDLE.md"
        bundle_text = bundle_path.read_text(encoding="utf-8")
        for label in scan_private_text(bundle_text):
            errors.append(f"WEB_CONTEXT_BUNDLE privacy finding {label}")
        if len(bundle_text) > context_profile.get("max_chars", 0):
            errors.append("WEB_CONTEXT_BUNDLE exceeds the configured execution-context budget")
        marker = "```json\n"
        if marker not in bundle_text or "\n```" not in bundle_text.rsplit(marker, 1)[-1]:
            errors.append("WEB_CONTEXT_BUNDLE lacks its generated JSON payload")
        else:
            payload_text = bundle_text.split(marker, 1)[1].rsplit("\n```", 1)[0]
            payload = json.loads(payload_text)
            if payload.get("context_bundle_version") != "2.0.0":
                errors.append("WEB_CONTEXT_BUNDLE version is not 2.0.0")
            if payload.get("context_policy") != context_profile:
                errors.append("WEB_CONTEXT_BUNDLE execution-context profile drift")
            if payload.get("problem_contract_sha256") != canonical_json_sha256(problem):
                errors.append("WEB_CONTEXT_BUNDLE ProblemContract digest mismatch")
            freshness = payload.get("freshness", {})
            if freshness.get("bundle_role") != "bounded_navigation_cache":
                errors.append("WEB_CONTEXT_BUNDLE freshness role mismatch")
            if freshness.get("authoritative_state") != "fresh_repository_ledgers_and_live_github_objects":
                errors.append("WEB_CONTEXT_BUNDLE freshness authority mismatch")
            if freshness.get("recompute_when_input_digest_changes") is not True:
                errors.append("WEB_CONTEXT_BUNDLE lacks input-digest refresh rule")
            expected_ledgers = {
                "research/records/attempts.jsonl": root / "research/records/attempts.jsonl",
                "research/records/obligation-graphs.jsonl": root / "research/records/obligation-graphs.jsonl",
                "research/records/failed-routes.jsonl": root / "research/records/failed-routes.jsonl",
            }
            for relative, ledger_path in expected_ledgers.items():
                ledger = load_jsonl(ledger_path)
                observed = freshness.get("input_ledgers", {}).get(relative, {})
                if observed.get("record_count") != len(ledger):
                    errors.append(f"WEB_CONTEXT_BUNDLE ledger count mismatch: {relative}")
                if observed.get("records_sha256") != canonical_json_sha256(ledger):
                    errors.append(f"WEB_CONTEXT_BUNDLE ledger digest mismatch: {relative}")
            digest_input = dict(payload)
            digest_input.pop("context_payload_sha256", None)
            if payload.get("context_payload_sha256") != canonical_json_sha256(digest_input):
                errors.append("WEB_CONTEXT_BUNDLE payload digest mismatch")
            selection = payload.get("context_selection", {})
            valid_statuses = {
                "ready", "no_active_execution_context", "ambiguous_attempt", "ambiguous_graph",
                "missing_graph", "missing_attempt", "inactive_attempt", "missing_root_obligation", "invalid_selector",
                "inconsistent_selector", "inconsistent_execution_identity", "cross_problem_reference",
            }
            if selection.get("status") not in valid_statuses:
                errors.append("WEB_CONTEXT_BUNDLE has an unknown context-selection status")
            if selection.get("status") == "ready" and not selection.get("research_ready"):
                errors.append("ready execution context is not marked research_ready")
            if selection.get("status") != "ready" and selection.get("research_ready"):
                errors.append("non-ready execution context is marked research_ready")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"execution-context bundle invalid: {exc}")
        context_profile = {}

    try:
        source_manifest = load_json(root / "governance/control-plane/harness-source-manifest.v1.json")
        source_manifest_schema = root / "governance/control-plane/harness-source-manifest.v1.schema.json"
        errors.extend(f"source manifest: {message}" for message in validate_schema(source_manifest, source_manifest_schema))
        excluded_container_skills = set(source_manifest.get("excluded_container_skill_ids", []))
        if not REQUIRED_EXCLUDED_CONTAINER_SKILLS.issubset(excluded_container_skills):
            errors.append("source manifest must exclude auto-goal, auto-tmux and nvidia-private-compute")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"source manifest invalid: {exc}")
        excluded_container_skills = set(REQUIRED_EXCLUDED_CONTAINER_SKILLS)

    try:
        container_lock = load_json(root / "governance/control-plane/container-skill-source-lock.v1.json")
        lock_schema = root / "governance/control-plane/container-skill-source-lock.v1.schema.json"
        errors.extend(f"container Skill lock: {message}" for message in validate_schema(container_lock, lock_schema))
        if not REQUIRED_EXCLUDED_CONTAINER_SKILLS.issubset(set(container_lock.get("excluded_skill_ids", []))):
            errors.append("container Skill lock lacks required Web exclusions")
        locked_skills = {item.get("skill_id"): item for item in container_lock.get("skills", []) if isinstance(item, dict)}
        expected_locked = {"solve", "math-toolchain"}
        if set(locked_skills) != expected_locked:
            errors.append("container Skill lock must preserve exactly the two source identities")
        expected_lock_status = {"solve": "active", "math-toolchain": "historical_source_only"}
        for skill_id, expected_status in expected_lock_status.items():
            locked = locked_skills.get(skill_id, {})
            if locked.get("web_status") != expected_status:
                errors.append(f"container Skill status mismatch: {skill_id}")
            if locked.get("evidence_ceiling") != "candidate_only":
                errors.append(f"container Skill evidence ceiling must be candidate_only: {skill_id}")
        if not (root / ".pi/skills/solve/SKILL.md").is_file():
            errors.append("solve operator library must be present and active")
        if (root / ".pi/skills/math-toolchain").exists():
            errors.append("legacy math-toolchain Skill must not be active in the designated Pi suite")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"container Skill lock invalid: {exc}")

    for stem in ("math-knowledge-source", "math-knowledge-operators"):
        config_path = root / f"governance/control-plane/{stem}.v1.json"
        registry_schema = root / f"governance/control-plane/{stem}.schema.json"
        try:
            config = load_json(config_path)
            errors.extend(f"{stem}: {message}" for message in validate_schema(config, registry_schema))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{stem} invalid: {exc}")

    try:
        active = load_json(root / "WEB_ACTIVE_SKILLS.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"WEB_ACTIVE_SKILLS invalid: {exc}")
        active = {"skills": []}
    snapshot_skills = {item.get("skill_id"): item for item in snapshot.get("active_skills", []) if isinstance(item, dict)}
    expected_skill_status = PI_SKILL_STATUS
    expected_skill_ids = set(expected_skill_status)
    actual_skill_ids = {item.get("skill_id") for item in active.get("skills", []) if isinstance(item, dict)}
    if actual_skill_ids != expected_skill_ids:
        errors.append(f"WEB_ACTIVE_SKILLS must contain exactly the 10 bundled Web research Skills: {sorted(actual_skill_ids)}")
    for item in active.get("skills", []):
        if isinstance(item, dict) and item.get("skill_id") in expected_skill_status:
            if item.get("web_status") != expected_skill_status[item["skill_id"]]:
                errors.append(f"WEB Skill status mismatch: {item.get('skill_id')}")
    if (root / ".codex").exists():
        errors.append("legacy .codex runtime tree must not enter a Pi-native problem repository")
    if (root / ".pi/skills/nvidia-private-compute").exists():
        errors.append("nvidia-private-compute is host-only and must not enter Web problem repositories")
    try:
        pi_settings = load_json(root / ".pi/settings.json")
        expected_paths = [f"skills/{skill_id}/SKILL.md" for skill_id in PI_SKILL_STATUS]
        if pi_settings.get("skills") != expected_paths:
            errors.append(".pi/settings.json must list exactly the admitted project Skill entries in canonical order")
        if pi_settings.get("enableSkillCommands") is not True:
            errors.append(".pi/settings.json must enable Skill commands")
        if set(pi_settings) != {"skills", "enableSkillCommands"}:
            errors.append(".pi/settings.json contains undeclared project runtime settings")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"Pi settings invalid: {exc}")
    for item in active.get("skills", []):
        if not isinstance(item, dict):
            errors.append("WEB_ACTIVE_SKILLS contains non-object")
            continue
        skill_id = item.get("skill_id")
        entry = root / str(item.get("entry", ""))
        if not entry.is_file() or entry.is_symlink():
            errors.append(f"active Skill entry missing: {skill_id}")
            continue
        if item.get("entry_sha256") != sha256_file(entry):
            errors.append(f"active Skill digest mismatch: {skill_id}")
        if entry.parent.name != skill_id or entry.parent.parent != root / ".pi/skills":
            errors.append(f"active Skill entry is outside the canonical Pi Skill directory: {skill_id}")
        else:
            head = entry.read_text(encoding="utf-8")[:4096]
            if not re.search(rf"(?m)^name:\s*{re.escape(str(skill_id))}\s*$", head):
                errors.append(f"Pi Skill frontmatter name mismatch: {skill_id}")
            if not re.search(r"(?m)^description:\s*\S", head):
                errors.append(f"Pi Skill frontmatter description missing: {skill_id}")
        if snapshot_skills.get(skill_id) != item:
            errors.append(f"active Skill does not match snapshot: {skill_id}")

    consolidation_map = root / ".pi/skills/CONSOLIDATION-MAP.md"
    if consolidation_map.is_file():
        consolidation_text = consolidation_map.read_text(encoding="utf-8")
        if "31 packages from 29 source families" not in consolidation_text:
            errors.append("Skill consolidation map lacks the audited 31-package/29-family boundary")
        if consolidation_map.stat().st_size < 7000:
            errors.append("Skill consolidation map is unexpectedly thin")
    abstraction_map_path = root / ".pi/skills/SOURCE-ABSTRACTION-MAP.json"
    if abstraction_map_path.is_file():
        try:
            abstraction_map = load_json(abstraction_map_path)
            packages = abstraction_map.get("packages", [])
            package_ids = [item.get("package_id") for item in packages if isinstance(item, dict)]
            source_families = {item.get("source_family") for item in packages if isinstance(item, dict)}
            if len(packages) != 31 or len(package_ids) != len(set(package_ids)):
                errors.append("Skill source abstraction map must contain 31 unique packages")
            if len(source_families) != 29 or None in source_families:
                errors.append("Skill source abstraction map must contain exactly 29 source families")
            for item in packages:
                if not isinstance(item, dict):
                    errors.append("Skill source abstraction map contains a non-object package")
                    continue
                if item.get("source_body_redistributed") is not False:
                    errors.append(f"held source body redistribution is forbidden: {item.get('package_id')}")
                targets = item.get("primary_skills", [])
                if not targets or not set(targets).issubset(expected_skill_ids):
                    errors.append(f"invalid Skill abstraction targets: {item.get('package_id')}")
                if not item.get("extracted_capabilities"):
                    errors.append(f"empty Skill abstraction: {item.get('package_id')}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"Skill source abstraction map invalid: {exc}")

    classification_path = root / ".pi/skills/INTERNAL-PACKAGE-CLASSIFICATION.json"
    classified_packages: list[dict[str, Any]] = []
    if classification_path.is_file():
        try:
            classification = load_json(classification_path)
            classified_packages = classification.get("packages", [])
            ids = [item.get("package_id") for item in classified_packages if isinstance(item, dict)]
            families = {item.get("source_family") for item in classified_packages if isinstance(item, dict)}
            owners = [item.get("primary_owner") for item in classified_packages if isinstance(item, dict)]
            if len(classified_packages) != 31 or len(ids) != len(set(ids)):
                errors.append("internal-package classification must contain 31 unique packages")
            if len(families) != 29 or None in families:
                errors.append("internal-package classification must contain exactly 29 source families")
            if not set(owners).issubset(INTERNAL_PACKAGE_TOP_SKILLS) or set(owners) != INTERNAL_PACKAGE_TOP_SKILLS:
                errors.append("internal-package classification owner set mismatch")
            for item in classified_packages:
                if not isinstance(item, dict):
                    errors.append("internal-package classification contains a non-object")
                    continue
                package_id = item.get("package_id")
                owner = item.get("primary_owner")
                if item.get("body_policy") != "bundled_complete_self_contained":
                    errors.append(f"internal-package body policy mismatch: {package_id}")
                if item.get("repository_body_included") is not True:
                    errors.append(f"complete internal-package body missing: {package_id}")
                if item.get("public_redistribution_admitted") is not False:
                    errors.append(f"HOLD package incorrectly marked redistribution-admitted: {package_id}")
                if not set(item.get("cross_referenced_by", [])).issubset(INTERNAL_PACKAGE_TOP_SKILLS - {owner}):
                    errors.append(f"invalid internal-package cross-reference: {package_id}")
                expected_relative = f".pi/skills/{owner}/internal-packages/{package_id}"
                if item.get("repository_relative_path") != expected_relative:
                    errors.append(f"internal-package repository path mismatch: {package_id}")
                    continue
                package_root = root / expected_relative
                try:
                    resolved = package_root.resolve(strict=True)
                    resolved.relative_to(root / ".pi/skills")
                except (OSError, ValueError):
                    errors.append(f"internal-package path missing or escapes repository: {package_id}")
                    continue
                manifest_path = package_root / ".vibemathing-package-manifest.json"
                try:
                    manifest = load_json(manifest_path)
                    observed = internal_package_snapshot(package_root)
                    if manifest.get("package_id") != package_id or manifest.get("primary_owner") != owner:
                        errors.append(f"internal-package manifest identity mismatch: {package_id}")
                    if manifest.get("source_files") != observed["files"] or item.get("source_files") != observed["files"]:
                        errors.append(f"internal-package file-count mismatch: {package_id}")
                    if manifest.get("source_bytes") != observed["bytes"] or item.get("source_bytes") != observed["bytes"]:
                        errors.append(f"internal-package byte-count mismatch: {package_id}")
                    if manifest.get("source_tree_sha256") != observed["tree_sha256"] or item.get("source_tree_sha256") != observed["tree_sha256"]:
                        errors.append(f"internal-package tree digest mismatch: {package_id}")
                    if manifest.get("source_rows") != observed["rows"]:
                        errors.append(f"internal-package per-file manifest mismatch: {package_id}")
                    if manifest.get("rights_state") != "HOLD" or manifest.get("public_redistribution_admitted") is not False:
                        errors.append(f"internal-package rights boundary mismatch: {package_id}")
                    entry_relative = item.get("entry_relative_path")
                    if not isinstance(entry_relative, str) or not (root / entry_relative).is_file():
                        errors.append(f"internal-package entry missing: {package_id}")
                    elif not entry_relative.startswith(expected_relative + "/") or not entry_relative.endswith("/SKILL.md"):
                        errors.append(f"internal-package entry path mismatch: {package_id}")
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    errors.append(f"internal-package manifest invalid {package_id}: {exc}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"internal-package classification invalid: {exc}")

    classified_by_owner = {
        skill_id: {item.get("package_id") for item in classified_packages if isinstance(item, dict) and item.get("primary_owner") == skill_id}
        for skill_id in INTERNAL_PACKAGE_TOP_SKILLS
    }
    physical_packages: set[str] = set()
    for skill_id in INTERNAL_PACKAGE_TOP_SKILLS:
        skill_dir = root / ".pi/skills" / skill_id
        registry_path = skill_dir / "INTERNAL-PACKAGES.json"
        routing_path = skill_dir / "references/internal-package-routing.md"
        package_dir = skill_dir / "internal-packages"
        if not registry_path.is_file() or registry_path.is_symlink():
            errors.append(f"internal-package registry missing: {skill_id}")
            continue
        if not routing_path.is_file() or routing_path.is_symlink():
            errors.append(f"internal-package routing guide missing: {skill_id}")
        if not package_dir.is_dir() or package_dir.is_symlink():
            errors.append(f"internal-package body directory missing: {skill_id}")
            actual_owned: set[str] = set()
        else:
            actual_owned = {path.name for path in package_dir.iterdir() if path.is_dir() and not path.is_symlink()}
            physical_packages.update(actual_owned)
        try:
            registry = load_json(registry_path)
            if registry.get("top_level_skill") != skill_id:
                errors.append(f"internal-package registry owner mismatch: {skill_id}")
            if registry.get("body_availability") != "bundled_complete_self_contained":
                errors.append(f"internal-package availability mismatch: {skill_id}")
            owned_items = [item for item in registry.get("owned_packages", []) if isinstance(item, dict)]
            owned = {item.get("package_id") for item in owned_items}
            if owned != classified_by_owner[skill_id] or actual_owned != classified_by_owner[skill_id]:
                errors.append(f"internal-package owned set mismatch: {skill_id}")
            for owned_item in owned_items:
                if owned_item.get("public_redistribution_admitted") is not False:
                    errors.append(f"internal-package rights flag mismatch: {owned_item.get('package_id')}")
                for key in ("body_relative_path", "entry_relative_path"):
                    value = owned_item.get(key)
                    if not isinstance(value, str) or value.startswith("/") or ".." in Path(value).parts:
                        errors.append(f"unsafe internal-package registry path {key}: {owned_item.get('package_id')}")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"internal-package registry invalid {skill_id}: {exc}")
        entry = skill_dir / "SKILL.md"
        if entry.is_file():
            entry_text = entry.read_text(encoding="utf-8")
            if "INTERNAL-PACKAGES.json" not in entry_text or "references/internal-package-routing.md" not in entry_text:
                errors.append(f"top-level Skill does not route internal packages: {skill_id}")
    if physical_packages != {item.get("package_id") for item in classified_packages if isinstance(item, dict)}:
        errors.append("physical internal-package set does not match the 31-package classification")

    skill_suite_bytes = 0
    consolidated_skill_ids = expected_skill_ids - {"solve"}
    for skill_id in expected_skill_ids:
        skill_dir = root / ".pi/skills" / str(skill_id)
        skill_suite_bytes += sum(
            path.stat().st_size
            for path in skill_dir.rglob("*")
            if path.is_file() and not path.is_symlink()
        )
        if skill_id not in consolidated_skill_ids:
            continue
        core = skill_dir / "references/consolidated-core.md"
        if not core.is_file() or core.is_symlink():
            errors.append(f"consolidated Skill core missing: {skill_id}")
            continue
        if core.stat().st_size < 3500:
            errors.append(f"consolidated Skill core is unexpectedly thin: {skill_id}")
        entry = skill_dir / "SKILL.md"
        if entry.is_file() and "references/consolidated-core.md" not in entry.read_text(encoding="utf-8"):
            errors.append(f"Skill entry does not route to its consolidated core: {skill_id}")
    if skill_suite_bytes < 100000:
        errors.append("designated Pi Skill suite is unexpectedly thin")

    bootstrap = root / "WEB_BOOTSTRAP.md"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        try:
            expected_snapshot_sha = snapshot_file_sha256(root)
            if expected_snapshot_sha not in text:
                errors.append("WEB_BOOTSTRAP does not bind Harness snapshot digest")
        except ValueError as exc:
            errors.append(str(exc))
        if snapshot.get("repository") not in text:
            errors.append("WEB_BOOTSTRAP repository mismatch")
        if f"Repository binding: `{repository_identity.get('binding_state')}`" not in text:
            errors.append("WEB_BOOTSTRAP repository binding mismatch")
        expected_database_id = repository_identity.get("database_id") if repository_identity.get("database_id") is not None else "pending"
        expected_node_id = repository_identity.get("node_id") or "pending"
        if f"Repository database ID: `{expected_database_id}`" not in text:
            errors.append("WEB_BOOTSTRAP repository database ID mismatch")
        if f"Repository node ID: `{expected_node_id}`" not in text:
            errors.append("WEB_BOOTSTRAP repository node ID mismatch")
        if f"Default branch: `{repository_identity.get('default_branch')}`" not in text:
            errors.append("WEB_BOOTSTRAP default branch mismatch")
        if f"Visibility: `{repository_identity.get('visibility')}`" not in text:
            errors.append("WEB_BOOTSTRAP visibility mismatch")
        if snapshot.get("problem", {}).get("problem_id") not in text:
            errors.append("WEB_BOOTSTRAP Problem mismatch")
        if f"Problem lifecycle: `{snapshot.get('problem', {}).get('lifecycle')}`" not in text:
            errors.append("WEB_BOOTSTRAP Problem lifecycle mismatch")
        if f"Problem admission: `{snapshot.get('problem', {}).get('admission')}`" not in text:
            errors.append("WEB_BOOTSTRAP Problem admission mismatch")

    for path in sorted(root.rglob("*")):
        if path == root / ".git" or ".git" in path.relative_to(root).parts:
            continue
        relative = path.relative_to(root)
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            errors.append(f"forbidden Harness path: {relative.as_posix()}")
            continue
        if relative.name in FORBIDDEN_LOCAL_RUNTIME_FILES:
            errors.append(f"local runtime contract forbidden in Web problem repository: {relative.as_posix()}")
            continue
        if excluded_container_skills.intersection(relative.parts):
            errors.append(f"excluded container Skill path: {relative.as_posix()}")
            continue
        if path.is_symlink():
            errors.append(f"symlink forbidden in problem repository: {relative.as_posix()}")
        elif path.exists() and not path.is_dir() and not path.is_file():
            errors.append(f"non-regular repository member: {relative.as_posix()}")
        elif repository_identity.get("visibility") == "public" and path.is_file():
            try:
                public_text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
            else:
                if PRIVATE_REPOSITORY_LOCATOR.search(public_text):
                    errors.append(f"public repository exposes a private repository locator: {relative.as_posix()}")

    scan_roots = [
        root / "research/artifacts/web-inbox",
        root / "research/artifacts/candidates",
        root / "research/artifacts/source-notes",
    ]
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"binary web artifact forbidden: {path.relative_to(root).as_posix()}")
                continue
            for label in scan_private_text(text):
                errors.append(f"privacy finding {label}: {path.relative_to(root).as_posix()}")

    workflow = root / ".github/workflows/web-candidate-gate.yml"
    if workflow.is_file():
        workflow_text = workflow.read_text(encoding="utf-8")
        if "pull_request_target" in workflow_text:
            errors.append("candidate workflow must not use pull_request_target")
        if "contents: read" not in workflow_text or "persist-credentials: false" not in workflow_text:
            errors.append("candidate workflow lacks read-only checkout controls")
        if "pip install --require-hashes -r requirements-web-harness.txt" not in workflow_text:
            errors.append("candidate workflow dependencies are not hash-pinned")
        if "cache-dependency-path: requirements-web-harness.txt" not in workflow_text:
            errors.append("candidate workflow lacks an explicit pip cache dependency path")
        required_check_jobs = set(profile.get("branch_policy", {}).get("required_checks", []))
        for check_name in sorted(required_check_jobs):
            job_pattern = rf"(?m)^  {re.escape(check_name)}:\s*$"
            name_pattern = rf"(?m)^    name:\s*{re.escape(check_name)}\s*$"
            if not re.search(job_pattern, workflow_text) or not re.search(name_pattern, workflow_text):
                errors.append(f"candidate workflow lacks required status-check job: {check_name}")
        if "${{ secrets." in workflow_text:
            errors.append("candidate workflow must not receive secrets")
        for action_ref in re.findall(r"uses:\s*[^@\s]+@([^\s#]+)", workflow_text):
            if not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                errors.append(f"candidate workflow action is not commit-pinned: {action_ref}")

    makefile = root / "Makefile"
    if makefile.is_file():
        for script in re.findall(r"python3\s+(scripts/[A-Za-z0-9_./-]+\.py)", makefile.read_text(encoding="utf-8")):
            if not (root / script).is_file():
                errors.append(f"Makefile references missing script: {script}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Web GPT problem repository Harness.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate(args.project_root)
    report = {"decision": "PASS" if not errors else "BLOCK", "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(f"web problem Harness validation: {report['decision']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
