# Provenance

Source archive: `05_Lean4_自学资源_腾讯文档.zip`  
Snapshot date recorded by source: 2026-09-12  
Primary readable knowledge source: `Lean4自学资源_存档.md`

## Source condition

- `README.md` identifies the Tencent Docs origin and says the Markdown file is the page-content snapshot.
- `tencent_doc_raw.html` is a Tencent Docs application shell. Under the current book-to-skill HTML extraction rule (remove `script`, `style`, and `head`, then extract visible text), it yields interface text and no substantive Lean resource list. Its embedded metadata confirms the document title.
- `tencent_api.json` is empty (0 bytes).
- No substantive source image or table was present in the archive. Image URLs found in the raw HTML belong to Tencent Docs application resources, not to the archived Lean resource list.
- The *Mathematics in Lean* bullet points to a Chinese version in “4.a”, but the archived snapshot contains no section 4.a and no link for that referenced version. This is an unresolved source cross-reference.

## Rule traceability

| Skill behavior | Location | Classification |
|---|---|---|
| Chinese hub and its four listed tracks | Snapshot §1 | SOURCE_DERIVED |
| *Mathematics in Lean* is strongly recommended / main class content | Snapshot §1 | SOURCE_DERIVED |
| Natural Number Game, installation tutorial, Tao cheatsheet, NUS minicourse, ReasLab | Snapshot §1 | SOURCE_DERIVED |
| ReasLab and Quokka explicitly welcome bug feedback; no feedback channel is recorded | Snapshot §1 / §2 | SOURCE_DERIVED |
| Zulip, Mathlib/API lookup, official online compiler, Quokka | Snapshot §2 | SOURCE_DERIVED |
| Mathlib docs, LeanSearch, Moogle as theorem-search resources | Snapshot §2 | SOURCE_DERIVED |
| setup → foundations → formal mathematics route | Cross-section organization | STRUCTURAL_SYNTHESIS |
| docs/search → Lean validation → Zulip escalation | Cross-section organization | STRUCTURAL_SYNTHESIS |
| validate automated formalization before acceptance | Skill safety/quality design | IMPLEMENTATION_DECISION |
| do not invent unrecorded resource capabilities | Source-fidelity design | IMPLEMENTATION_DECISION |

## Fidelity rule

When the archive supplies only a resource name and link, preserve that narrow claim. Any richer description requires separate verification outside this skill and must not be attributed to the archived source.
