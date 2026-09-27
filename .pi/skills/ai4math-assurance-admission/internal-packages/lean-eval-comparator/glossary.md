# Glossary

**Attempted** — a problem whose selected workspace differs from the freshly rendered expected workspace (ch04).

**Challenge** — trusted generated module containing the benchmark statement/holes (ch01).

**Comparator** — verifier that builds/exports Challenge and Solution, checks reachable constants/axioms, and replays the exported result (ch01, ch07).

**`COMPARATOR_BIN`** — environment override selecting the comparator executable used by `WorkspaceTest` (ch03).

**`definition_names`** — comparator targets whose implementation bodies may differ while required type structure is checked; used for def/instance holes (ch10).

**Dual-kernel defense** — requirement that evaluation pass Lean kernel replay and nanoda independent-kernel checking (ch07).

**Enforced config** — temporary config produced by `WorkspaceTest` after forcing `enable_nanoda` to true (ch03).

**Environment allowlist** — expected Submission-visible variable set bounded to PATH/HOME/Lean runtime paths; checked by `env_dump_probe` (ch07, ch08).

**Generated workspace** — deterministic Lake project under `generated/<id>/` derived from trusted source, manifest, and templates (ch05).

**Hole** — solver-owned tagged declaration listed in a problem manifest; may be theorem, def, or named instance (ch05, ch10).

**Immutable pin** — exact commit/toolchain selector used to prevent silent upstream drift (ch09).

**Landrun** — Linux landlock sandbox used by comparator's safe build/export operations (ch02, ch07).

**`lake env`** — Lake environment wrapper; source probes assert it does not elaborate project Submission code in the pinned toolchain (ch07, ch08).

**Lean4export** — tool that exports compiled Lean environments for comparator processing; its olean format must match the active Lean toolchain (ch02).

**Mismatch** — workspace difference from expected rendered files; basis for `attempted` (ch04).

**Nanoda** — independent kernel required by LeanEval; forced on by `WorkspaceTest` (ch03, ch07).

**Olean** — compiled Lean artifact whose binary format is Lean-version sensitive (ch02).

**Permitted axioms** — `{propext, Quot.sound, Classical.choice}` in generated configs; disallows `sorryAx`/`Lean.ofReduceBool` (ch01, ch07).

**Pin drift** — disagreement among authoritative/runtime setup sources about dependency revisions (ch09).

**Pristine workspace** — generated source-of-truth workspace before solver edits (ch03, ch04).

**Sandbox-engaged probe** — synthetic workspace test asserting forbidden writes fail and allowed `.lake` write succeeds (ch08).

**Solution** — trusted generated bridge that connects Challenge names to Submission declarations (ch01).

**Submission** — solver-controlled proof/definition code, normally limited to `Submission.lean` and `Submission/` modules (ch01, ch03).

**Succeeded** — attempted problem whose `lake test` exits zero (ch04).

**`theorem_names`** — comparator theorem targets subject to graph/axiom verification (ch01, ch10).

**WorkspaceTest** — trusted harness that forces nanoda on and invokes comparator through `lake env` (ch03).

**Writable-`.lake` limitation** — documented process-lifetime/artifact-race concern around build outputs; no working false-credit exploit is claimed in the snapshot (ch07).
