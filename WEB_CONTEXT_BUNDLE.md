# Web Research Context Bundle

This file is generated from repository truth and bounded by `governance/control-plane/web-context-profile.v1.json`. It is navigation context, not a Result, EvidenceLink, verifier receipt, or permission grant.

## Mandatory order

1. Read `AGENTS.md`, `governance/harness/PROJECT_AGENTS.md`, and `WEB_BOOTSTRAP.md`.
2. Read the execution-context profile and confirm its digest-bound limits.
3. Check the exact ProblemContract and its SHA-256 below.
4. Check `context_selection.status`. Only `ready` permits mathematical work; `no_active_execution_context` is maintenance/pre-admission only; ambiguous, inconsistent, missing, or invalid states are fail-closed.
5. When `ready`, use only the selected Attempt/Route/ObligationGraph/Obligation and its bounded dependency closure. The catalogs are navigation indexes, not permission grants.
6. Read the selected top-level Skill's `INTERNAL-PACKAGES.json`; route to the smallest applicable internal source package before inventing a method. Complete package bodies are bundled at repository-relative paths; rights remain HOLD and bundling does not grant publication or execution authority.
7. Search registered mathematical knowledge sources before inventing a new theorem.
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
  "context_bundle_version": "2.0.0",
  "context_payload_sha256": "c633eabc51b8a94fefde1c540334dea118d70426049b7769a3d6244050aa236b",
  "context_policy": {
    "budgets": {
      "max_attempt_catalog": 32,
      "max_dependency_closure": 64,
      "max_failed_route_catalog": 24,
      "max_graph_catalog": 32,
      "max_list_items": 32,
      "max_obligation_catalog": 96,
      "max_operator_catalog": 64,
      "max_package_catalog": 64,
      "max_source_catalog": 64,
      "max_text_chars": 768
    },
    "max_chars": 90000,
    "profile_id": "web-execution-context:bounded-v2",
    "schema_version": "1.0.0",
    "selection": {
      "active_lifecycle_priority": [
        "running",
        "planned"
      ],
      "ambiguous_policy": "catalog_only_fail_closed",
      "default_obligation": "root_obligation",
      "explicit_selector_fields": [
        "attempt_id",
        "route_id",
        "graph_id",
        "obligation_id"
      ]
    }
  },
  "context_selection": {
    "reason": "no running or planned Attempt is available",
    "research_ready": false,
    "selected_attempt_id": null,
    "selectors": {
      "attempt_id": null,
      "graph_id": null,
      "obligation_id": null,
      "route_id": null
    },
    "status": "no_active_execution_context"
  },
  "execution_catalog": {
    "attempts": {
      "items": [],
      "omitted_count": 0,
      "total": 0
    },
    "failed_routes": {
      "items": [],
      "omitted_count": 0,
      "total": 0
    },
    "obligation_graphs": {
      "items": [],
      "omitted_count": 0,
      "total": 0
    }
  },
  "internal_package_routing": {
    "package_catalog": {
      "items": [
        {
          "capabilities": [
            "problem-to-method fit",
            "verification-first experimentation",
            "informative failure"
          ],
          "cross_referenced_by": [
            "ai4math-bounded-computation",
            "ai4math-proof-refutation"
          ],
          "entry_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/ai-for-mathematics/SKILL.md",
          "package_id": "ai-for-mathematics",
          "primary_owner": "ai4math-source-discovery",
          "repository_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/ai-for-mathematics",
          "rights_state": "HOLD",
          "source_bytes": 96401,
          "source_files": 11
        },
        {
          "capabilities": [
            "artifact and modality routing",
            "evaluation design",
            "research-system comparison"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/ai4math-research-navigator/ai4math-research-navigator/SKILL.md",
          "package_id": "ai4math-research-navigator",
          "primary_owner": "ai4math-source-discovery",
          "repository_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/ai4math-research-navigator",
          "rights_state": "HOLD",
          "source_bytes": 152236,
          "source_files": 36
        },
        {
          "capabilities": [
            "dependency-aware formalization",
            "plan/prove/review separation",
            "stalled-run diagnosis"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/archon-formalization/SKILL.md",
          "package_id": "archon-formalization",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/archon-formalization",
          "rights_state": "HOLD",
          "source_bytes": 85673,
          "source_files": 22
        },
        {
          "capabilities": [
            "model/property separation",
            "abstraction soundness",
            "state-space control"
          ],
          "cross_referenced_by": [
            "ai4math-modeling-derivation",
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-bounded-computation/internal-packages/baier-katoen-model-checking/SKILL.md",
          "package_id": "baier-katoen-model-checking",
          "primary_owner": "ai4math-bounded-computation",
          "repository_relative_path": ".pi/skills/ai4math-bounded-computation/internal-packages/baier-katoen-model-checking",
          "rights_state": "HOLD",
          "source_bytes": 187243,
          "source_files": 20
        },
        {
          "capabilities": [
            "assumption exposure",
            "definition variation",
            "counterexample-guided boundary discovery"
          ],
          "cross_referenced_by": [
            "ai4math-proof-refutation"
          ],
          "entry_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/cheng-math-logic/SKILL.md",
          "package_id": "cheng-math-logic",
          "primary_owner": "ai4math-modeling-derivation",
          "repository_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/cheng-math-logic",
          "rights_state": "HOLD",
          "source_bytes": 46588,
          "source_files": 13
        },
        {
          "capabilities": [
            "type-directed search",
            "dependency-preserving Skolemization",
            "higher-order unification limits"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/classical-type-theory/SKILL.md",
          "package_id": "classical-type-theory",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/classical-type-theory",
          "rights_state": "HOLD",
          "source_bytes": 95276,
          "source_files": 20
        },
        {
          "capabilities": [
            "producer/verifier separation",
            "fact-graph memory",
            "falsification before persistence"
          ],
          "cross_referenced_by": [
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/danus-proof-orchestration/SKILL.md",
          "package_id": "danus-proof-orchestration",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/danus-proof-orchestration",
          "rights_state": "HOLD",
          "source_bytes": 71790,
          "source_files": 17
        },
        {
          "capabilities": [
            "capability diagnosis",
            "specialist-versus-general tool choice",
            "verifier feedback"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/dong-ai4m-research-guide/dong-ai4m-research-guide/SKILL.md",
          "package_id": "dong-ai4m-research-guide",
          "primary_owner": "ai4math-source-discovery",
          "repository_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/dong-ai4m-research-guide",
          "rights_state": "HOLD",
          "source_bytes": 26115,
          "source_files": 8
        },
        {
          "capabilities": [
            "capability diagnosis",
            "formalization stack",
            "understanding-over-ritual objective"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/dongbin-ai4m/SKILL.md",
          "package_id": "dongbin-ai4m",
          "primary_owner": "ai4math-source-discovery",
          "repository_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/dongbin-ai4m",
          "rights_state": "HOLD",
          "source_bytes": 43210,
          "source_files": 8
        },
        {
          "capabilities": [
            "logic-fragment routing",
            "rewriting and decision-procedure scope",
            "LCF trust boundary"
          ],
          "cross_referenced_by": [
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/harrison-automated-reasoning/SKILL.md",
          "package_id": "harrison-automated-reasoning",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/harrison-automated-reasoning",
          "rights_state": "HOLD",
          "source_bytes": 136952,
          "source_files": 16
        },
        {
          "capabilities": [
            "universal constructions",
            "functorial translation",
            "naturality and adjunction routing"
          ],
          "cross_referenced_by": [
            "mathematics-in-lean"
          ],
          "entry_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/hewei-category-theory/hewei-category-theory/SKILL.md",
          "package_id": "hewei-category-theory",
          "primary_owner": "ai4math-modeling-derivation",
          "repository_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/hewei-category-theory",
          "rights_state": "HOLD",
          "source_bytes": 67818,
          "source_files": 32
        },
        {
          "capabilities": [
            "statement parsing",
            "proof-language discipline",
            "example and counterexample use"
          ],
          "cross_referenced_by": [
            "ai4math-proof-refutation"
          ],
          "entry_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/houston-mathematical-thinking/SKILL.md",
          "package_id": "houston-mathematical-thinking",
          "primary_owner": "ai4math-modeling-derivation",
          "repository_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/houston-mathematical-thinking",
          "rights_state": "HOLD",
          "source_bytes": 98588,
          "source_files": 43
        },
        {
          "capabilities": [
            "toolchain matching",
            "InfoTree and declaration products",
            "static-analysis diagnostics"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/jixia-lean-analyzer/jixia-lean-analyzer/SKILL.md",
          "package_id": "jixia-lean-analyzer",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/jixia-lean-analyzer",
          "rights_state": "HOLD",
          "source_bytes": 65561,
          "source_files": 14
        },
        {
          "capabilities": [
            "counterexample triage",
            "lemma incorporation",
            "conjecture and definition repair"
          ],
          "cross_referenced_by": [
            "ai4math-modeling-derivation"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/lakatos-proofs-and-refutations/SKILL.md",
          "package_id": "lakatos-proofs-and-refutations",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/lakatos-proofs-and-refutations",
          "rights_state": "HOLD",
          "source_bytes": 133520,
          "source_files": 19
        },
        {
          "capabilities": [
            "pristine-versus-edited comparison",
            "isolated elaboration",
            "pin and security audit"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-assurance-admission/internal-packages/lean-eval-comparator/SKILL.md",
          "package_id": "lean-eval-comparator",
          "primary_owner": "ai4math-assurance-admission",
          "repository_relative_path": ".pi/skills/ai4math-assurance-admission/internal-packages/lean-eval-comparator",
          "rights_state": "HOLD",
          "source_bytes": 68671,
          "source_files": 15
        },
        {
          "capabilities": [
            "query routing by known information",
            "syntax-sensitive search",
            "local validation of suggestions"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/lean-search-client/SKILL.md",
          "package_id": "lean-search-client",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/lean-search-client",
          "rights_state": "HOLD",
          "source_bytes": 53353,
          "source_files": 12
        },
        {
          "capabilities": [
            "statement translation",
            "proof-state reading",
            "abstraction-ladder control"
          ],
          "cross_referenced_by": [
            "mathematics-in-lean"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/lean4-math-formalization-2025/lean4-math-formalization-2025/SKILL.md",
          "package_id": "lean4-math-formalization-2025",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/lean4-math-formalization-2025",
          "rights_state": "HOLD",
          "source_bytes": 90032,
          "source_files": 14
        },
        {
          "capabilities": [
            "syntax/elaboration/kernel staging",
            "metavariable state and rollback",
            "generated-term validation"
          ],
          "cross_referenced_by": [
            "ai4math-toolchain-reproducibility"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/lean4-metaprogramming/lean4-metaprogramming/SKILL.md",
          "package_id": "lean4-metaprogramming",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/lean4-metaprogramming",
          "rights_state": "HOLD",
          "source_bytes": 97929,
          "source_files": 19
        },
        {
          "capabilities": [
            "goal-based resource routing",
            "learning progression",
            "resource-fit recovery"
          ],
          "cross_referenced_by": [
            "mathematics-in-lean"
          ],
          "entry_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/lean4-self-study-resources/lean4-self-study-resources/SKILL.md",
          "package_id": "lean4-self-study-resources",
          "primary_owner": "ai4math-source-discovery",
          "repository_relative_path": ".pi/skills/ai4math-source-discovery/internal-packages/lean4-self-study-resources",
          "rights_state": "HOLD",
          "source_bytes": 27378,
          "source_files": 8
        },
        {
          "capabilities": [
            "parse/index/embed/search pipeline",
            "schema and revision pinning",
            "service diagnostics"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/ai4math-toolchain-reproducibility/internal-packages/leansearch-operator/SKILL.md",
          "package_id": "leansearch-operator",
          "primary_owner": "ai4math-toolchain-reproducibility",
          "repository_relative_path": ".pi/skills/ai4math-toolchain-reproducibility/internal-packages/leansearch-operator",
          "rights_state": "HOLD",
          "source_bytes": 66182,
          "source_files": 17
        },
        {
          "capabilities": [
            "expression normalization",
            "theorem precondition routing",
            "convergence-mode distinctions"
          ],
          "cross_referenced_by": [
            "mathematics-in-lean"
          ],
          "entry_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/math-analysis-thinking-methods/math-analysis-thinking-methods/SKILL.md",
          "package_id": "math-analysis-thinking-methods",
          "primary_owner": "ai4math-modeling-derivation",
          "repository_relative_path": ".pi/skills/ai4math-modeling-derivation/internal-packages/math-analysis-thinking-methods",
          "rights_state": "HOLD",
          "source_bytes": 219444,
          "source_files": 65
        },
        {
          "capabilities": [
            "goal-shape routing",
            "library interface preference",
            "formal analysis patterns"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/mathematics-in-lean-external-snapshot/mathematics-in-lean/SKILL.md",
          "package_id": "mathematics-in-lean-external-snapshot",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/mathematics-in-lean-external-snapshot",
          "rights_state": "HOLD",
          "source_bytes": 119810,
          "source_files": 18
        },
        {
          "capabilities": [
            "proof state as API",
            "weakest sufficient abstraction",
            "typeclasses filters and induction"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/mathematics-in-lean-project-record/SKILL.md",
          "package_id": "mathematics-in-lean-project-record",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/mathematics-in-lean-project-record",
          "rights_state": "HOLD",
          "source_bytes": 160516,
          "source_files": 21
        },
        {
          "capabilities": [
            "constructor and recursor alignment",
            "rewrite-to-recursion",
            "witness-based order"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/natural-number-game-lean4/natural-number-game-lean4/SKILL.md",
          "package_id": "natural-number-game-lean4",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/natural-number-game-lean4",
          "rights_state": "HOLD",
          "source_bytes": 101871,
          "source_files": 26
        },
        {
          "capabilities": [
            "understand-plan-execute-review",
            "backward reasoning",
            "heuristic-versus-proof separation"
          ],
          "cross_referenced_by": [
            "ai4math-modeling-derivation"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/polya-problem-solving/SKILL.md",
          "package_id": "polya-problem-solving",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/polya-problem-solving",
          "rights_state": "HOLD",
          "source_bytes": 57908,
          "source_files": 18
        },
        {
          "capabilities": [
            "persistent proof state",
            "retrieval applicability checks",
            "strict verification and degraded-mode honesty"
          ],
          "cross_referenced_by": [
            "ai4math-source-discovery",
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/rethlas-math-reasoning/SKILL.md",
          "package_id": "rethlas-math-reasoning",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/rethlas-math-reasoning",
          "rights_state": "HOLD",
          "source_bytes": 77575,
          "source_files": 16
        },
        {
          "capabilities": [
            "concise proof exposition",
            "explicit logical relations",
            "editing-versus-validation separation"
          ],
          "cross_referenced_by": [
            "ai4math-source-discovery"
          ],
          "entry_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/strunk-elements-of-style/SKILL.md",
          "package_id": "strunk-elements-of-style",
          "primary_owner": "ai4math-proof-refutation",
          "repository_relative_path": ".pi/skills/ai4math-proof-refutation/internal-packages/strunk-elements-of-style",
          "rights_state": "HOLD",
          "source_bytes": 94239,
          "source_files": 15
        },
        {
          "capabilities": [
            "API phase alignment",
            "epsilon-filter translation",
            "totalization and type-boundary guards"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/tao-analysis-lean/tao-analysis-lean/SKILL.md",
          "package_id": "tao-analysis-lean",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/tao-analysis-lean",
          "rights_state": "HOLD",
          "source_bytes": 104196,
          "source_files": 19
        },
        {
          "capabilities": [
            "propositions as types",
            "constructor and recursor interfaces",
            "termination and typeclass inference"
          ],
          "cross_referenced_by": [
            "ai4math-lean-formalization"
          ],
          "entry_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/theorem-proving-in-lean-4/SKILL.md",
          "package_id": "theorem-proving-in-lean-4",
          "primary_owner": "mathematics-in-lean",
          "repository_relative_path": ".pi/skills/mathematics-in-lean/internal-packages/theorem-proving-in-lean-4",
          "rights_state": "HOLD",
          "source_bytes": 112153,
          "source_files": 17
        },
        {
          "capabilities": [
            "verifier hard boundary",
            "retrieval before brute force",
            "reasoning-proving interleaving"
          ],
          "cross_referenced_by": [
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/welleck-informal-formal-reasoning/welleck-informal-formal-reasoning/SKILL.md",
          "package_id": "welleck-informal-formal-reasoning",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/welleck-informal-formal-reasoning",
          "rights_state": "HOLD",
          "source_bytes": 62773,
          "source_files": 13
        },
        {
          "capabilities": [
            "statement freezing",
            "API engineering",
            "normalize-before-automation and counterexample checks"
          ],
          "cross_referenced_by": [
            "mathematics-in-lean",
            "ai4math-assurance-admission"
          ],
          "entry_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/xena-formalization-method/SKILL.md",
          "package_id": "xena-formalization-method",
          "primary_owner": "ai4math-lean-formalization",
          "repository_relative_path": ".pi/skills/ai4math-lean-formalization/internal-packages/xena-formalization-method",
          "rights_state": "HOLD",
          "source_bytes": 236007,
          "source_files": 33
        }
      ],
      "omitted_count": 0,
      "total": 31
    },
    "policy": {
      "complete_package_bodies_bundled": true,
      "internal_packages_are_not_pi_entries": true,
      "one_physical_repository_copy_per_package": true,
      "public_redistribution_requires_separate_rights_admission": true,
      "top_level_skills_own_routing_not_mathematical_strategy": true
    }
  },
  "knowledge_operators": [
    {
      "evidence_ceiling": "discovery_only",
      "external_effect": "none",
      "input_kinds": [
        "problem_contract",
        "obligation_statement"
      ],
      "operator_id": "op:identify-mathematical-object",
      "output_kind": "object_identity_candidates",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_local",
      "input_kinds": [
        "obligation_statement",
        "object_identity_candidates",
        "source_profile"
      ],
      "operator_id": "op:search-formal-theorem",
      "output_kind": "formal_theorem_hits",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_network",
      "input_kinds": [
        "object_fingerprint",
        "source_profile"
      ],
      "operator_id": "op:search-mathematical-database",
      "output_kind": "database_object_hits",
      "owner_skill": "ai4math-source-discovery"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "read_local",
      "input_kinds": [
        "formal_theorem_hit",
        "package_candidate",
        "source_profile"
      ],
      "operator_id": "op:resolve-formal-package",
      "output_kind": "environment_closure_candidate",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "input_kinds": [
        "obligation_statement",
        "external_statement",
        "environment_closure_candidate"
      ],
      "operator_id": "op:compare-statements",
      "output_kind": "statement_relation_candidate",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "input_kinds": [
        "statement_relation_candidate",
        "obligation_graph",
        "failed_routes"
      ],
      "operator_id": "op:compose-reuse-plan",
      "output_kind": "reuse_plan_candidate",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "none",
      "input_kinds": [
        "reuse_plan_candidate",
        "active_obligation"
      ],
      "operator_id": "op:prove-reuse-gap",
      "output_kind": "candidate_artifact",
      "owner_skill": "ai4math-proof-refutation"
    },
    {
      "evidence_ceiling": "candidate_only",
      "external_effect": "bounded_candidate_build",
      "input_kinds": [
        "candidate_artifact",
        "environment_closure_candidate"
      ],
      "operator_id": "op:build-formal-candidate",
      "output_kind": "formal_build_receipt",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "verifier_receipt",
      "external_effect": "bounded_candidate_build",
      "input_kinds": [
        "formal_build_receipt",
        "candidate_artifact",
        "obligation_statement"
      ],
      "operator_id": "op:verify-formal-candidate",
      "output_kind": "machine_verifier_receipts",
      "owner_skill": "ai4math-lean-formalization"
    },
    {
      "evidence_ceiling": "verifier_receipt",
      "external_effect": "none",
      "input_kinds": [
        "candidate_artifact",
        "statement_relation_candidate",
        "problem_contract"
      ],
      "operator_id": "op:review-reuse-semantics",
      "output_kind": "semantic_review_receipt",
      "owner_skill": "ai4math-proof-refutation"
    }
  ],
  "knowledge_sources": [
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "installed",
      "operational_status": "quarantined",
      "source_class": "formal_library_index",
      "source_id": "lean-mathlib-local",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-proof-refutation",
        "ai4math-lean-formalization"
      ]
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_package_registry",
      "source_id": "lean-reservoir",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-lean-formalization"
      ]
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_library_index",
      "source_id": "mathlib-docs-search",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-proof-refutation",
        "ai4math-lean-formalization"
      ]
    },
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "proof_archive",
      "source_id": "isabelle-afp",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-proof-refutation",
        "ai4math-lean-formalization"
      ]
    },
    {
      "evidence_ceiling": "verifier_input",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "formal_package_registry",
      "source_id": "rocq-mathcomp",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-proof-refutation",
        "ai4math-lean-formalization"
      ]
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "mathematical_object_database",
      "source_id": "oeis",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-bounded-computation"
      ]
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "mathematical_object_database",
      "source_id": "lmfdb",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-bounded-computation"
      ]
    },
    {
      "evidence_ceiling": "candidate_only",
      "maturity": "surveyed",
      "operational_status": "available",
      "source_class": "formula_reference",
      "source_id": "nist-dlmf",
      "used_by": [
        "ai4math-source-discovery",
        "ai4math-modeling-derivation",
        "ai4math-bounded-computation"
      ]
    },
    {
      "evidence_ceiling": "computation_evidence",
      "maturity": "surveyed",
      "operational_status": "design_only",
      "source_class": "algorithm_distribution",
      "source_id": "sagemath",
      "used_by": [
        "ai4math-bounded-computation"
      ]
    }
  ],
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
  "problem_contract_sha256": "e64cd03254e03dd661eade23243c3c21793fc2d8bffa2d33c172cf8ed2e7f940",
  "selected_execution_context": null
}
```
