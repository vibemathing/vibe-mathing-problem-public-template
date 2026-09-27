# Chapter 3: Blueprint and DAG Discipline

## Core Idea
The blueprint is executable planning infrastructure: it must state the mathematics, declare dependencies, map to Lean names, and form a coherent cone toward the project goals. A vague blueprint produces noisy objectives and wasted prover budget.

## Completeness Gate
Before treating a cone as ready, check:
1. no infinite/unknown-effort placeholders remain in the relevant blueprint route;
2. `\uses{}` references resolve;
3. blueprint declarations map to Lean names or intentional placeholders;
4. the goal ancestor cone is connected and meaningful;
5. Lean↔blueprint unmatched queries are empty for covered work;
6. `content.tex` includes the intended chapters.

Use `leandag build`, stats/focus/query commands, `archon dag-query`, and `archon blueprint-doctor` as mechanical evidence. The doctor catches orphan chapters, broken references, malformed annotations, stray axioms, and coverage annotation problems.

## One-to-One Rule
Every significant Lean declaration should have blueprint representation, including helpers introduced during proving. A helper that lacks a blueprint block is dependency debt: report it so planner/reviewer can add the corresponding label, Lean mapping, and uses edges.

## Blueprint Purity
Blueprint prose should carry mathematics and source grounding. Keep Lean tactic mechanics out of mathematical explanations. Use source citations where the argument depends on external material.

## Repair Routes
- **High-effort node** → split into smaller `\uses`-linked lemmas; repeat until each has a finite, intelligible proof route.
- **Incomplete dependency cone** → walk upward and fill statements/proofs/dependencies before dispatching provers.
- **Lean/blueprint drift** → use bidirectional audit; correct either implementation or blueprint according to the intended math.
- **Structural lint failure** → fix doctor findings before calling the graph ready.

## Validation
A DAG can parse and still be mathematically poor. Combine structural checks with fresh-context blueprint/strategy critique when the route is load-bearing.

## Source Provenance
Primary: `src/archon/.archon-src/prompts/dag.md`, blueprint subagents, DAG commands, `tests/test_blueprint_doctor.py`, `tests/test_chapter_covers.py`.

## Frameworks Introduced
- **Blueprint completeness gate**: a proving route is ready only when its statements, informal proofs, Lean mappings, dependencies, and chapter inclusion are coherent.
- **One-to-one correspondence**: every meaningful Lean declaration should be represented in the blueprint; every blueprint target should have a Lean mapping or explicit placeholder.
- **Cone-first planning**: reason from goal ancestors and dependency closure instead of scanning files linearly.

## Key Concepts
- **`\\uses{}`**: dependency edges between blueprint declarations.
- **Unmatched declaration**: Lean or blueprint item lacking its corresponding representation.
- **Effort estimate**: a signal used to distinguish actionable nodes from unresolved/infinite-complexity placeholders.
- **Coverage annotation**: mechanism for mapping consolidated blueprint chapters to Lean files.
- **Blueprint doctor**: deterministic structural lint separate from mathematical review.

## Mental Models
- Treat the DAG as a **compiler IR for the mathematical plan**: ambiguous dependencies here become wasted work downstream.
- Treat disconnected or isolated nodes as a **wiring smell** until proven intentional.

## Anti-patterns
- **Pretty prose, missing edges**: an informal proof can read well while giving the prover no dependency-ready route.
- **Helper invisibility**: adding Lean helpers without blueprint entries silently corrupts frontier analysis.
- **Structural success = mathematical success**: a graph may parse with zero broken refs and still encode a false or incomplete argument.

## Worked Example
A target `main_theorem` depends informally on `compact_reduction`, which itself uses a local finiteness lemma. The blueprint only lists `main_theorem -> compact_reduction`. `leandag` shows the finiteness helper absent, and provers repeatedly discover it ad hoc. Add a dedicated blueprint block for the helper, give it an informal proof and source citation, add `\\uses{}` from `compact_reduction`, map the helper to Lean, rebuild, and verify unmatched/doctor output. The next prover round can target the helper first rather than re-discovering the same dependency.

## Reference Table
| Gate failure | Repair |
|---|---|
| broken `\\uses` | correct label/edge before proving |
| infinite/high effort | decompose or strengthen informal proof |
| unmatched Lean helper | add blueprint block + mapping |
| isolated goal ancestor | repair dependency wiring |
| orphan chapter | include or remove intentionally |
| malformed annotation | fix syntax, then rebuild doctor report |

## Key Takeaways
1. Spend prover budget only on a trustworthy cone.
2. Preserve 1:1 Lean↔blueprint coverage as helpers evolve.
3. Combine deterministic structure checks with mathematical critique.
4. Rebuild the graph after structural edits.

## Connects To
- **Ch 04**: the plan phase consumes DAG readiness.
- **Ch 05**: fine-grained mode operationalizes detailed blueprint proofs.
- **Ch 11**: blueprint claims need source provenance.
