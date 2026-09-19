# Chapter 2: 学习时需要的常用资源

## Core Idea

When Lean4 work is already in progress, route by the immediate action: run code, look up an API/declaration, search for a theorem, try automated formalization, or ask the community.

## Frameworks Introduced

The source supplies a tool list rather than a named workflow. The following routes operationalize that list.

- **Search escalation** *(STRUCTURAL_SYNTHESIS)*
  - **When to use**: a proof is blocked because the needed theorem or declaration is unknown.
  - **How**: Mathlib/API documentation → LeanSearch or Moogle → test the candidate in Lean → Zulip if still unresolved.
  - **Failure mode**: assuming a search result is applicable without checking its type, namespace, imports, or actual compilation.
- **Automation-with-validation** *(IMPLEMENTATION_DECISION)*
  - **When to use**: the user wants automated formalization through Quokka.
  - **How**: use Quokka as the archived automation option → run/check the resulting Lean → fall back to manual search/help on failure.
  - **Why it works**: generated or suggested formalization still has to satisfy Lean's checker.

## Key Concepts

- **Zulip** — the archive points learners to the Lean community's Zulip chat for support.
- **Mathlib API Documentation** — the archive lists Mathlib theorem/API lookup as a routine learning resource; direct documentation URL: https://leanprover-community.github.io/mathlib4_docs/
- **Official online compiler** — https://live.lean-lang.org/ for running Lean online.
- **Quokka** — automated formalization platform: https://quokka-beta.reaslab.io/
- **LeanSearch** — theorem-search engine named by the archive: leansearch.net
- **Moogle** — theorem-search engine: https://www.moogle.ai/

## Mental Models

- **Execution answers “does this Lean code check?”** Use the official online compiler for quick experiments.
- **Documentation answers “what is this declaration/API?”** Prefer Mathlib docs when the neighborhood of the declaration is already known.
- **Search answers “what theorem might solve this?”** Use theorem-search engines when the name is unknown.
- **Community answers “what am I missing?”** Escalate when search and local experimentation do not resolve the problem.
- **Automation proposes work; Lean validates work.** Treat automated formalization as a route to candidates, not a correctness certificate.

## Anti-patterns

- **Inventing a bug-report channel**: the archive says Quokka welcomes bug feedback but does not record a submission channel; rely only on what the live service exposes.

- **Searching only one surface**: the archive lists multiple theorem-search resources; switch surfaces when the first one fails.
- **Confusing theorem search with compilation**: finding a candidate theorem and checking a Lean term are separate steps.
- **Treating automation output as final**: validate the result in Lean before relying on it.
- **Overstating Zulip details**: the archive references Zulip as a support resource but does not document channel structure or policies.

## Worked Example

A learner knows the mathematical fact needed for a proof but cannot remember its Mathlib name.

1. If they know the likely namespace or library area, inspect **Mathlib documentation** first.
2. If the declaration name is unknown, try **LeanSearch** or **Moogle**.
3. Put the candidate theorem into a small example in the **official online compiler** (or the user's local environment) to confirm imports, arguments, and elaboration.
4. If the search still fails or the theorem does not apply, ask **Zulip** with the smallest reproducible Lean context.
5. If the task is suitable for automated formalization, **Quokka** is another archived option, followed by the same Lean validation step.

## Key Takeaways

1. Match the tool to the action: run, document, search, automate, or ask.
2. A practical recovery loop is docs/search → Lean validation → community help.
3. Use alternate theorem-search engines when one surface misses the target.
4. Validate automated formalization in Lean.
5. Keep claims about external tools within the archived descriptions unless separately verified.

## Connects To

- **Ch 1**: use the learning resources to build the conceptual skills needed to interpret search results and errors.
- **Cheatsheet**: `../cheatsheet.md` gives the fastest routing table.
