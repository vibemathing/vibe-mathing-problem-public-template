# Web Research Context Bundle

This file is generated from repository truth and bounded for the web channel. It is navigation context, not a Result, EvidenceLink, verifier receipt, or permission grant.

## Mandatory order

1. Read `AGENTS.md`, `governance/harness/PROJECT_AGENTS.md`, and `WEB_BOOTSTRAP.md`.
2. Check the exact ProblemContract and its SHA-256 below.
3. Select exactly one pre-admitted Attempt/Route/ObligationGraph/Obligation.
4. Search registered mathematical knowledge sources before inventing a new theorem.
5. After repository admission, autonomously complete Issue, candidate branch/file edits, commit, PR review, checks/rerun, merge, and checkpoint within the profile.
6. Write only candidate files under the profile allowlist and one `WEB_ATTEMPT_PACKET`; do not wait for project-added routine human approvals.
7. Never claim that Issue, PR, AI review, merge, Actions status, package build, search hit, test success, or this context closes mathematics.

## Compiled repository truth

```json
{
  "active_skills": [
    {
      "entry": ".pi/skills/ai4math-assurance-admission/SKILL.md",
      "entry_sha256": "c1fee24e444faeab4f22c7c4ed0b2d1611f9bf58d85e8631aab6d01da72503cc",
      "skill_id": "ai4math-assurance-admission",
      "version": "1.1.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-bounded-computation/SKILL.md",
      "entry_sha256": "58720c5d7c73519108938a289cd2cd46ed3388325fff4dd7290510c695441d4b",
      "skill_id": "ai4math-bounded-computation",
      "version": "1.1.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-lean-formalization/SKILL.md",
      "entry_sha256": "4975006512820c130e041bcec460dc6667c5c8550f84420d7a514366b3a821e8",
      "skill_id": "ai4math-lean-formalization",
      "version": "1.1.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-modeling-derivation/SKILL.md",
      "entry_sha256": "e20bd3b51be54739471e6bbe92fc3de8e8d75bef7f90f4bee76e21bcc8c3d70d",
      "skill_id": "ai4math-modeling-derivation",
      "version": "1.1.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-proof-refutation/SKILL.md",
      "entry_sha256": "33bd1bbd7d09d979529fe49025061ae50b8b6d8a0a34e43c5338080e3826a61b",
      "skill_id": "ai4math-proof-refutation",
      "version": "1.1.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-source-discovery/SKILL.md",
      "entry_sha256": "0f2776c32224c313c943164e77b206c12472cb030c0f0d6a82c20e2dc161520d",
      "skill_id": "ai4math-source-discovery",
      "version": "1.1.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-toolchain-reproducibility/SKILL.md",
      "entry_sha256": "c436ffc08a36b6be58aef825790789db8b840049948720d7a846ef5d7766ff14",
      "skill_id": "ai4math-toolchain-reproducibility",
      "version": "1.1.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/mathematics-in-lean/SKILL.md",
      "entry_sha256": "58a1647bb4e6bf8934a31655be6f0ca623093d46145298ed7ccec5de0dffd00d",
      "skill_id": "mathematics-in-lean",
      "version": "1.1.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/prove2me/SKILL.md",
      "entry_sha256": "535dfa98839d78543d9c00259ccb3a1a3647933a0f7c0bad6062ae079bb1b190",
      "skill_id": "prove2me",
      "version": "1.1.0",
      "web_status": "constrained"
    }
  ],
  "attempts": [],
  "failed_routes": [],
  "knowledge_operators": [
    {
      "evidence_ceiling": "discovery_only",
      "external_effect": "none",
      "operator_id": "op:identify-mathematical-object",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_local",
      "operator_id": "op:search-formal-theorem",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_network",
      "operator_id": "op:search-mathematical-database",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_local",
      "operator_id": "op:resolve-formal-package",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "operator_id": "op:compare-statements",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "operator_id": "op:compose-reuse-plan",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "operator_id": "op:prove-reuse-gap",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "bounded_candidate_build",
      "operator_id": "op:build-formal-candidate",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "verifier_receipt",
      "external_effect": "bounded_candidate_build",
      "operator_id": "op:verify-formal-candidate",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "verifier_receipt",
      "external_effect": "none",
      "operator_id": "op:review-reuse-semantics",
      "owner_skill": "ai4math-proof-refutation"
    }
  ],
  "knowledge_sources": [
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "installed",
      "operational_status": "quarantined",
      "source_class": "formal_library_index",
      "source_id": "lean-mathlib-local"
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_package_registry",
      "source_id": "lean-reservoir"
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_library_index",
      "source_id": "mathlib-docs-search"
    },
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "proof_archive",
      "source_id": "isabelle-afp"
    },
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_package_registry",
      "source_id": "rocq-mathcomp"
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "mathematical_object_database",
      "source_id": "oeis"
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "mathematical_object_database",
      "source_id": "lmfdb"
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "available",
      "source_class": "formula_reference",
      "source_id": "nist-dlmf"
    },
    {
      "evidence_ceiling": "computation_evidence",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "algorithm_distribution",
      "source_id": "sagemath"
    }
  ],
  "obligation_graphs": [],
  "problem_contract": {
    "acceptance": {
      "policy": "solution-admission-v1"
    },
    "aliases": [],
    "allowed_axioms": [
      "none"
    ],
    "assumptions": [
      "This record must never be treated as an active research problem."
    ],
    "constraints": {
      "allowed_adapters": [
        "template-validation-v1"
      ],
      "allowed_methods": [
        "discovery"
      ],
      "max_attempts": 1,
      "runtime": {
        "max_output_bytes": 65536,
        "max_retries": 1,
        "max_transitions": 10,
        "timeout_seconds": 60
      }
    },
    "created_at": "2026-09-06T00:00:00Z",
    "definitions": [
      {
        "definition": "A non-admitted draft record used only to validate the physical public repository template.",
        "term": "template placeholder"
      }
    ],
    "domain": {
      "description": "Template-only placeholder domain; not a mathematical research question.",
      "objects": [
        "template-placeholder"
      ]
    },
    "lifecycle": "draft",
    "msc": [
      "00A00"
    ],
    "problem_id": "problem:template-placeholder",
    "quantifiers": [
      {
        "domain": "a reviewed public canonical ProblemContract supplied by the repository builder",
        "kind": "find",
        "variables": [
          "replacement_problem"
        ]
      }
    ],
    "schema_version": "1.0.0",
    "sources": [
      {
        "retrieved_at": "2026-09-06T00:00:00Z",
        "source": "Vibe Mathing public Web Harness",
        "source_record_id": "public-template-placeholder-v1",
        "url": "https://github.com/vibemathing/vibe-mathing-problem-public-template"
      }
    ],
    "statement": {
      "language": "en",
      "text": "This is a non-research placeholder. Replace it with exactly one reviewed public ProblemContract before creating a public problem repository.",
      "version": 1
    },
    "title": "Vibe Mathing public problem repository template placeholder",
    "updated_at": "2026-09-06T00:00:00Z"
  },
  "problem_contract_sha256": "e64cd03254e03dd661eade23243c3c21793fc2d8bffa2d33c172cf8ed2e7f940"
}
```
