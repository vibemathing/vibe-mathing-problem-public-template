# Evaluation Plan

`cases.json` covers positive/negative triggering, method selection, failure recovery, and fresh-agent simulations. `scripts/validate.py` performs structural checks, frontmatter checks, link checks, token-budget approximations, source coverage, placeholder checks, and eval-shape checks.

Manual review additionally asks:

1. Does every core method have source provenance or a structural/implementation label?
2. Does the main skill route details on demand instead of duplicating every chapter?
3. Can a fresh agent distinguish statement semantics from proof checking?
4. Are historical Lean names presented as version-sensitive?
5. Does failure recovery include stopping when meaning cannot be established?
