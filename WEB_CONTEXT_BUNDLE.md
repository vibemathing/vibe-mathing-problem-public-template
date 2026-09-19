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
      "entry_sha256": "c20468c5fab97118ba574c766c474ad7ed14d6a1aa6a2458e1cf59275cf1d30d",
      "skill_id": "ai4math-assurance-admission",
      "version": "1.0.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-bounded-computation/SKILL.md",
      "entry_sha256": "eadbd8b93d7927c85247378fe17eebebe89bfaf3d23b0e0c5499ad0a66f5f605",
      "skill_id": "ai4math-bounded-computation",
      "version": "1.0.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-lean-formalization/SKILL.md",
      "entry_sha256": "d7200af5ed58b7bafefb531dee309e4085eada329be618dee67c3f2f61dbbc08",
      "skill_id": "ai4math-lean-formalization",
      "version": "1.0.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-modeling-derivation/SKILL.md",
      "entry_sha256": "b98bd8c1f3a9640a080143ebd5deae4d43fff00318063bf9b5e86db40f2da088",
      "skill_id": "ai4math-modeling-derivation",
      "version": "1.0.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-proof-refutation/SKILL.md",
      "entry_sha256": "10342bc2b6c3e0f8cdf747afeb7e3aae7dd3ef2f5af9faaac470cdd3e3d6701d",
      "skill_id": "ai4math-proof-refutation",
      "version": "1.0.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-source-discovery/SKILL.md",
      "entry_sha256": "de0c419b8c4e4e185bb5e299cb5b759a4c328dddcb7a2eea9198600e9fc9526f",
      "skill_id": "ai4math-source-discovery",
      "version": "1.0.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-toolchain-reproducibility/SKILL.md",
      "entry_sha256": "c7dab252042407c3a8c0c4fe7f8fb5f1d9336e379b37647094b88d953c5319c2",
      "skill_id": "ai4math-toolchain-reproducibility",
      "version": "1.0.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/mathematics-in-lean/SKILL.md",
      "entry_sha256": "111d841454e8dd110ca7c9daa8132c0a84a2dfdda6c0ee7aa1e917a9eb85493b",
      "skill_id": "mathematics-in-lean",
      "version": "1.0.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/prove2me/SKILL.md",
      "entry_sha256": "8140d0e64c643c52cfdb6db06267b28c35c29f3985bdd284b7f3779fca231737",
      "skill_id": "prove2me",
      "version": "1.0.0",
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
