#!/usr/bin/env python3
"""来源登记消费前的摘要、许可与运行成熟度负例。"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_math_knowledge_registry import preflight_source_use


class SourcePreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry_bytes = (ROOT / "governance/control-plane/math-knowledge-source.v1.json").read_bytes()
        cls.registry = json.loads(cls.registry_bytes)
        cls.digest = hashlib.sha256(cls.registry_bytes).hexdigest()

    def check(self, source_id: str, use: str, *, registry=None, digest=None):
        raw = self.registry_bytes if registry is None else json.dumps(registry, sort_keys=True).encode()
        return preflight_source_use(raw, source_id, use, expected_registry_sha256=digest or self.digest)

    def test_discovery_is_metadata_only_even_for_surveyed_source(self) -> None:
        result = self.check("mathlib-docs-search", "discovery")
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["authorization_scope"], "catalog_metadata_only")
        self.assertEqual(result["claims_ceiling"], "candidate_only")
        self.assertEqual(result["operational_status"], "design_only")
        self.assertEqual(result["registry_sha256"], self.digest)

    def test_design_only_query_and_quarantined_build_are_blocked(self) -> None:
        for source_id, use in (("mathlib-docs-search", "query"), ("lean-mathlib-local", "build")):
            with self.subTest(source_id=source_id, use=use):
                self.assertEqual(self.check(source_id, use)["decision"], "BLOCK")

    def test_restricted_license_and_unknown_source_are_blocked(self) -> None:
        for source_id, use in (("nist-dlmf", "local_reference"), ("not-registered", "discovery")):
            with self.subTest(source_id=source_id):
                self.assertEqual(self.check(source_id, use)["decision"], "BLOCK")

    def test_missing_or_stale_digest_fails_closed(self) -> None:
        self.assertEqual(self.check("mathlib-docs-search", "discovery", digest="0" * 64)["decision"], "BLOCK")
        changed = copy.deepcopy(self.registry)
        changed["sources"][0]["notes"] = "synthetic drift"
        self.assertEqual(self.check("mathlib-docs-search", "discovery", registry=changed)["decision"], "BLOCK")

    def test_duplicate_id_and_unknown_use_fail_closed(self) -> None:
        changed = copy.deepcopy(self.registry)
        changed["sources"].append(copy.deepcopy(changed["sources"][2]))
        raw = json.dumps(changed, sort_keys=True).encode()
        self.assertEqual(preflight_source_use(raw, "mathlib-docs-search", "discovery",
            expected_registry_sha256=hashlib.sha256(raw).hexdigest())["decision"], "BLOCK")
        self.assertEqual(self.check("mathlib-docs-search", "admission")["decision"], "BLOCK")

    def test_staged_available_source_still_cannot_claim_execution_or_proof(self) -> None:
        staged = copy.deepcopy(self.registry)
        item = next(source for source in staged["sources"] if source["source_id"] == "mathlib-docs-search")
        item["maturity"] = "source_locked"
        item["operational_status"] = "available"
        raw = json.dumps(staged, sort_keys=True).encode()
        result = preflight_source_use(raw, item["source_id"], "query",
            expected_registry_sha256=hashlib.sha256(raw).hexdigest())
        self.assertEqual(result["decision"], "PASS")
        self.assertEqual(result["authorization_scope"], "catalog_metadata_only")
        self.assertEqual(result["claims_ceiling"], "candidate_only")

    def test_cli_uses_real_bytes_and_returns_nonzero_on_block(self) -> None:
        script = ROOT / "scripts/validate_math_knowledge_registry.py"
        args = [sys.executable, str(script), "--project-root", str(ROOT),
                "--source-id", "mathlib-docs-search", "--use", "discovery",
                "--expected-registry-sha256", self.digest, "--json"]
        good = subprocess.run(args, text=True, capture_output=True, check=False)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)["authorization_scope"], "catalog_metadata_only")
        blocked = subprocess.run(args[:-2] + ["0" * 64, "--json"], text=True, capture_output=True, check=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(json.loads(blocked.stdout)["decision"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
