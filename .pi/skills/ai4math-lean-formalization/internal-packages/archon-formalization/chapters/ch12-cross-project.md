# Chapter 12: Extract, Merge, Peers, and Scope

## Core Idea
When projects share mathematical declarations, reuse should be DAG-driven. Archon provides dependency-cone extraction, declaration-aware merging, and a deterministic cross-project roadmap.

## Extract
Use `archon extract` to carve a dependency-cone subproject. Compute the keep/mixed/imported/drop plan from the DAG, preserve necessary Lean import riders, update blueprint `content.tex`, prune references/state to the kept scope, and verify the extracted cone with DAG checks (and build when requested).

## Merge
A merge operates in a sandbox duplicate of the target with the source read-only. Shared declarations with identical signatures can be compared by proof strength; a differing statement is a conflict requiring an explicit decision. Import whole declarations, preserve stable Lean names/blueprint labels, include source-only helper riders, rebuild DAG after batches, and use `lake build` as the real consistency gate.

## Scope Roadmap
Across peers, deterministic analysis computes:
- **unblock matrix**: which project already satisfies names another still needs;
- **duplication**: declarations open in multiple projects;
- **leverage**: projects ranked by how much peer work they can unlock;
- **stalled**: projects whose open names are already satisfied elsewhere.

Use these numbers to decide where to work, what to extract into a shared base, or which proof to import. Agentic `scope discuss` can add judgment after the reproducible graph facts.

## Safety Rules
Source projects remain read-only during merge/extract sessions. Keep inner-git commits through surgery. Never auto-resolve statement conflicts. Verify final seeds/closure and broken dependency counts before accepting a transformed project.

## Source Provenance
Primary: extract/merge prompts and commands, scope merge-DAG/roadmap code, peer/scope/extract tests.

## Frameworks Introduced
- **DAG carve**: compute a dependency closure and preserve only the material needed for a subproject.
- **Proof-strength overlap merge**: when signatures match, choose between proof states using explicit quality ordering and user preference.
- **Deterministic scope roadmap**: derive reuse decisions from available/needed Lean names before adding agent judgment.

## Key Concepts
- **Seed**: declaration(s) whose dependency cone defines an extraction/merge scope.
- **Rider**: source-only auxiliary/import dependency needed by a selected proof even if not obvious in blueprint edges.
- **Statement conflict**: same logical identifier/label but differing Lean signature; cannot be silently merged.
- **Unblock edge**: provider project already satisfies a declaration needed by a consumer.
- **Leverage**: count of cross-project needs a project can satisfy now.

## Mental Models
- Treat extract/merge like **program slicing and link-time integration**: compute closure, preserve required riders, then rebuild.
- Treat cross-project naming as an **interface contract**; stable names/signatures make reuse mechanical.

## Anti-patterns
- **Freehand project surgery**: bypasses computed closure and can leave broken hidden dependencies.
- **Auto-merge statement conflicts**: changes mathematics under the guise of proof reuse.
- **Copy whole source project for one proof**: loses the value of declaration-level dependency analysis.

## Worked Example
Projects P1 and P2 both contain `Foo.main`; P1 proves it, P2 still has a sorry, and signatures match. Scope roadmap shows P1 unblocks P2 and another project. Merge can select P1's whole declaration proof for the shared name, import any P1-only helper rider, rebuild LeanDag, and run `lake build`. If P2's `Foo.main` signature differs, stop and require a mathematical decision. If the same open helper is duplicated in three projects, extract its cone into a shared base candidate instead of proving it three times.

## Key Takeaways
1. Compute closures before copying files.
2. Stable signatures enable safe proof reuse.
3. Statement conflicts require explicit human choice.
4. Rank work by leverage when coordinating many peers.

## Connects To
- **Ch 03**: all reuse depends on reliable DAGs.
- **Ch 09**: sandbox/inner-git make surgery reversible.
- **Ch 14**: transformed projects must pass full verify gates.
