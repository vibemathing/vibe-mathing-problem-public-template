# Consolidated core: source discovery and research navigation

## Purpose

Turn an informal research need into a bounded, provenance-aware source question. Discovery supplies candidate inputs; it never certifies a theorem or chooses the canonical actor's mathematical route.

## Intake model

Record before searching:

- exact claim or unresolved concept;
- domain, quantifiers, definitions, assumptions and notation;
- desired source function: statement identity, prior result, method, counterexample, dataset, theorem-library declaration, or tool capability;
- date/freshness requirement;
- acceptable source classes and language;
- output needed and evidence ceiling.

If the request mixes several functions, split the **questions**, not the mathematical mission. A literature source, a Lean declaration and a software release are different evidence objects.

## Source-question types

1. **Identity** — What is the canonical statement, title, author, identifier and version?
2. **Status** — Is the problem stated open, solved, conditional, retracted, or merely answered on one site?
3. **Dependency** — Which theorem, definition or API provides a needed interface?
4. **Method** — Which ideas have been tried, under which hypotheses, and what failed?
5. **Falsifier** — Are counterexamples, edge cases or negative results known?
6. **Capability** — Does a tool actually accept the required input and emit the required checkable output?
7. **Reproducibility** — Is there an immutable revision, environment and executable procedure?

Do not answer one type with evidence for another. A survey may identify a method but not establish current package behavior; a repository README may describe behavior but not establish mathematical truth.

## Discovery loop

### Normalize

Write a search identity with aliases, notation variants and excluded homonyms. Preserve the original wording alongside normalized terms.

### Retrieve

Prefer the narrowest authoritative layer:

- original paper, official problem list or standards text for statements;
- publisher or author page for bibliographic identity;
- repository, registry or release API for software facts;
- formal library source for declaration types;
- later surveys for navigation, not replacement of primary evidence.

### Qualify

For every candidate record:

- source URL or stable locator;
- source class and authority;
- publication/revision date;
- exact relevant passage or declaration;
- claim supported and claim not supported;
- assumptions and applicability conditions;
- immutable digest/revision when available;
- license/redistribution status when content may enter the repository.

### Compare

Build a claim-level matrix. Distinguish:

- same statement with different notation;
- strict strengthening or weakening;
- different domain or quantifier order;
- conditional versus unconditional result;
- formal theorem versus prose paraphrase;
- current upstream behavior versus historical snapshot.

### Hand off

Return a source capsule containing only what the next capability needs. Preserve contradictions and uncertainty. Never collapse several conflicting sources into an unsupported consensus sentence.

## Research-method routing

Use source discovery to expose options, not prescribe a route:

- informal proof research: definitions, nearby theorems, known constructions, obstructions;
- formalization: exact theorem types, imports, namespace, toolchain revision and examples of API use;
- computation: benchmark definitions, instance formats, algorithms, complexity and independent implementations;
- AI4Math systems: task modality, verifier, dataset leakage risk, evaluation unit and failure modes;
- mathematical exposition: terminology, historical attribution and established conventions.

## Applicability check

Before importing a theorem or method, ask:

1. Do domains and quantifiers match?
2. Are all preconditions established, not merely plausible?
3. Is the source result exact, asymptotic, probabilistic, numerical, or conditional?
4. Does notation hide a changed object or equivalence relation?
5. Is the claimed version the version actually inspected?
6. Would using it create a new unresolved obligation?

A useful but inapplicable result is recorded as a candidate route, not silently used.

## Failure recovery

- **Too many results:** tighten by statement fragments, identifiers, authors, domain restrictions and date.
- **No results:** expand aliases, search cited/citing works, inspect formal-library synonyms, then record the negative search boundary.
- **Conflicting sources:** privilege fresh primary evidence and preserve the disagreement.
- **Paywalled or unavailable:** record metadata and locate a lawful author manuscript or independent reference; do not invent passages.
- **Unknown license:** use facts and independently written abstractions only; do not copy body text.
- **Stale tool documentation:** inspect pinned source and executable behavior before claiming capability.

## Anti-loop rule

A repeated search is justified only by a substantive change: new alias, source class, time window, database, citation edge, theorem type, or contradiction. Rephrasing the same query without a new discriminator is not progress.

## Output checklist

- normalized question and original claim both present;
- each fact tied to a source;
- primary/secondary distinction explicit;
- applicability and mismatch recorded;
- licenses and immutable identities tracked where needed;
- unresolved contradictions retained;
- no claim of proof, installation or admission.
