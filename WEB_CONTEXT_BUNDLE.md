# Web Research Context Bundle

This file is generated from repository truth and bounded for the web channel. It is navigation context, not a Result, EvidenceLink, verifier receipt, or permission grant.

## Mandatory order

1. Read `AGENTS.md`, `governance/harness/PROJECT_AGENTS.md`, and `WEB_BOOTSTRAP.md`.
2. Check the exact ProblemContract and its SHA-256 below.
3. Select exactly one pre-admitted Attempt/Route/ObligationGraph/Obligation.
4. Read the selected top-level Skill's `INTERNAL-PACKAGES.json`; route to the smallest applicable internal source package before inventing a method. Complete package bodies are bundled at repository-relative paths; rights remain HOLD and bundling does not grant publication or execution authority.
5. Search registered mathematical knowledge sources before inventing a new theorem.
6. After repository admission, autonomously complete Issue, candidate branch/file edits, commit, PR review, checks/rerun, merge, and checkpoint within the profile.
7. Write only candidate files under the profile allowlist and one `WEB_ATTEMPT_PACKET`; do not wait for project-added routine human approvals.
8. Never claim that Issue, PR, AI review, merge, Actions status, package build, search hit, test success, or this context closes mathematics.

## Compiled repository truth

```json
{
  "active_skills": [
    {
      "entry": ".pi/skills/solve/SKILL.md",
      "entry_sha256": "ff557dc3fc2fa10df4b21e8bef251a37928f5572ccf0092c79f0d9ab90a00ec0",
      "skill_id": "solve",
      "version": "0.3.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/mathematics-in-lean/SKILL.md",
      "entry_sha256": "ddefbff20ddae7fa3cb2d644217b967db88bf6347db77256c03df46bdb4fd69e",
      "skill_id": "mathematics-in-lean",
      "version": "1.3.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/prove2me/SKILL.md",
      "entry_sha256": "535dfa98839d78543d9c00259ccb3a1a3647933a0f7c0bad6062ae079bb1b190",
      "skill_id": "prove2me",
      "version": "1.1.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-source-discovery/SKILL.md",
      "entry_sha256": "c831f416f09193c3354f615b776da9693eda002da643cd14246294a7aabd2fd6",
      "skill_id": "ai4math-source-discovery",
      "version": "1.3.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-modeling-derivation/SKILL.md",
      "entry_sha256": "cfcd1e46903cf8a5b5dd504a3e39d3a1e0d5fe5a5b1b532f50ced6580667de1b",
      "skill_id": "ai4math-modeling-derivation",
      "version": "1.3.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-proof-refutation/SKILL.md",
      "entry_sha256": "2ae3f923089576c9bc7c9ee7e0f16595ed9d49374d0fd5df6a1742feec4290d3",
      "skill_id": "ai4math-proof-refutation",
      "version": "1.3.0",
      "web_status": "active"
    },
    {
      "entry": ".pi/skills/ai4math-bounded-computation/SKILL.md",
      "entry_sha256": "0eba4c14b7069b9aaf55d3184e048fddeb8d86d27b5ddaca460a2a184509b38c",
      "skill_id": "ai4math-bounded-computation",
      "version": "1.3.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-lean-formalization/SKILL.md",
      "entry_sha256": "0c5a5a2813666f2512ccbc521655ef162152d2e203c52067649e4829fa0b1917",
      "skill_id": "ai4math-lean-formalization",
      "version": "1.3.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-assurance-admission/SKILL.md",
      "entry_sha256": "7262ba1d79702ddd3907c2206bf4faa6743f4982dc8802b0eb9fa4ae9859b1bd",
      "skill_id": "ai4math-assurance-admission",
      "version": "1.3.0",
      "web_status": "constrained"
    },
    {
      "entry": ".pi/skills/ai4math-toolchain-reproducibility/SKILL.md",
      "entry_sha256": "d36b1c8f6c7cd6ea17ac3cc10bf12875d91aa4277f4e48f198c499b3082551de",
      "skill_id": "ai4math-toolchain-reproducibility",
      "version": "1.3.0",
      "web_status": "constrained"
    }
  ],
  "attempts": [],
  "failed_routes": [],
  "internal_package_routing": {
    "policy": {
      "complete_package_bodies_bundled": true,
      "internal_packages_are_not_pi_entries": true,
      "one_physical_repository_copy_per_package": true,
      "public_redistribution_requires_separate_rights_admission": true,
      "top_level_skills_own_routing_not_mathematical_strategy": true
    },
    "top_level_skills": {
      "ai4math-assurance-admission": {
        "cross_referenced_packages": [
          "baier-katoen-model-checking",
          "danus-proof-orchestration",
          "harrison-automated-reasoning",
          "rethlas-math-reasoning",
          "welleck-informal-formal-reasoning",
          "xena-formalization-method"
        ],
        "owned_packages": [
          "lean-eval-comparator"
        ]
      },
      "ai4math-bounded-computation": {
        "cross_referenced_packages": [
          "ai-for-mathematics"
        ],
        "owned_packages": [
          "baier-katoen-model-checking"
        ]
      },
      "ai4math-lean-formalization": {
        "cross_referenced_packages": [
          "classical-type-theory",
          "lean-search-client",
          "leansearch-operator",
          "mathematics-in-lean-project-record",
          "mathematics-in-lean-external-snapshot",
          "natural-number-game-lean4",
          "tao-analysis-lean",
          "theorem-proving-in-lean-4"
        ],
        "owned_packages": [
          "archon-formalization",
          "jixia-lean-analyzer",
          "lean4-math-formalization-2025",
          "lean4-metaprogramming",
          "welleck-informal-formal-reasoning",
          "xena-formalization-method"
        ]
      },
      "ai4math-modeling-derivation": {
        "cross_referenced_packages": [
          "baier-katoen-model-checking",
          "lakatos-proofs-and-refutations",
          "polya-problem-solving"
        ],
        "owned_packages": [
          "cheng-math-logic",
          "hewei-category-theory",
          "houston-mathematical-thinking",
          "math-analysis-thinking-methods"
        ]
      },
      "ai4math-proof-refutation": {
        "cross_referenced_packages": [
          "ai-for-mathematics",
          "cheng-math-logic",
          "houston-mathematical-thinking"
        ],
        "owned_packages": [
          "classical-type-theory",
          "danus-proof-orchestration",
          "harrison-automated-reasoning",
          "lakatos-proofs-and-refutations",
          "polya-problem-solving",
          "rethlas-math-reasoning",
          "strunk-elements-of-style"
        ]
      },
      "ai4math-source-discovery": {
        "cross_referenced_packages": [
          "rethlas-math-reasoning",
          "strunk-elements-of-style"
        ],
        "owned_packages": [
          "ai-for-mathematics",
          "ai4math-research-navigator",
          "dong-ai4m-research-guide",
          "dongbin-ai4m",
          "lean4-self-study-resources"
        ]
      },
      "ai4math-toolchain-reproducibility": {
        "cross_referenced_packages": [
          "ai4math-research-navigator",
          "archon-formalization",
          "dong-ai4m-research-guide",
          "dongbin-ai4m",
          "jixia-lean-analyzer",
          "lean-eval-comparator",
          "lean4-metaprogramming"
        ],
        "owned_packages": [
          "leansearch-operator"
        ]
      },
      "mathematics-in-lean": {
        "cross_referenced_packages": [
          "hewei-category-theory",
          "lean4-math-formalization-2025",
          "lean4-self-study-resources",
          "math-analysis-thinking-methods",
          "xena-formalization-method"
        ],
        "owned_packages": [
          "lean-search-client",
          "mathematics-in-lean-project-record",
          "mathematics-in-lean-external-snapshot",
          "natural-number-game-lean4",
          "tao-analysis-lean",
          "theorem-proving-in-lean-4"
        ]
      }
    }
  },
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
