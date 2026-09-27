export PYTHONDONTWRITEBYTECODE := 1

.PHONY: check check-research-os check-research check-full check-release audit-release

check:
	python3 scripts/validate_agent_identity.py --project-root .
	python3 scripts/validate_mathematical_reasoning_discipline.py --project-root .
	python3 scripts/validate_web_problem_harness.py --project-root .
	python3 scripts/validate_web_attempt.py --project-root . --all-inbox
	python3 scripts/validate_math_knowledge_registry.py --project-root .
	python3 scripts/validate_obligation_graphs.py --project-root .
	python3 scripts/validate_research_spaces.py --project-root .

check-research-os:
	python3 scripts/validate_research_os_production_readiness.py --strict
	python3 scripts/test_validate_research_os_production_readiness.py
	python3 scripts/validate_research_os_metadata.py --strict
	python3 scripts/test_validate_research_os_metadata.py
	python3 scripts/validate_research_os_working_set.py
	python3 scripts/test_validate_research_os_working_set.py
	python3 scripts/validate_research_os_events.py
	python3 scripts/test_validate_research_os_events.py
	python3 scripts/test_research_os_runtime.py

check-research: check check-research-os
	python3 scripts/test_research_spaces.py
	python3 scripts/test_obligation_harness.py

check-full: check-research
	python3 scripts/test_template_release_pr_diff.py
	python3 scripts/test_agent_identity.py
	python3 scripts/test_web_context_bundle.py
	python3 scripts/test_builder_sync.py
	python3 scripts/test_release_audit.py

check-release:
	python3 scripts/validate_release_readiness.py --project-root . --mode public

audit-release:
	python3 scripts/audit_release_checklist.py --project-root . --json
