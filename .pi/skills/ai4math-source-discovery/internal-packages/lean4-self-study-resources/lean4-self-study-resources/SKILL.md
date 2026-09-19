---
name: lean4-self-study-resources
description: "Operational guide from the archived Lean4 自学资源 Tencent Docs snapshot. Use when choosing a Lean4 learning path or resource, locating theorem/API search tools, running Lean online, selecting formal-math or metaprogramming materials, or recovering when a listed study resource does not fit."
---

<!-- argument-hint: [goal, resource type, tool need, or chapter number] -->

# Lean4 自学资源（腾讯文档存档）

**Author**: 未标注 | **Content sections**: 2 | **Snapshot**: 2026-09-12

## How to Use This Skill

Use this skill as a **resource router**. The source is a curated Lean4 self-study index, so the skill helps choose the right listed resource and a sensible next action.

- **No argument** — identify the learner's current goal and route to the most relevant resource family.
- **Learning goal** — ask about setup, functional programming, theorem proving, formal mathematics, metaprogramming, game-based practice, lecture-style study, or quick reference.
- **During-work need** — ask about running Lean online, finding a theorem/API, automated formalization, or community help.
- **Chapter** — use `ch01` for learning resources or `ch02` for tools used while learning.

If a request needs detail that the archive does not contain, state the coverage limit. Do not invent capabilities for a resource from its name alone.

## Core Decision Logic

### 1. Route by learning goal

| Goal | First listed resource | Why this fits the archive |
|---|---|---|
| Install Lean locally | [安装教程](http://faculty.bicmr.pku.edu.cn/~wenzw/formal/docs/#/install) | The archive explicitly labels it as installation guidance. |
| Learn Lean as a functional language | [leanprover.cn](https://www.leanprover.cn) → *Functional Programming in Lean* | The Chinese hub lists this track. |
| Learn theorem proving | [leanprover.cn](https://www.leanprover.cn) → *Theorem Proving in Lean* | The Chinese hub lists this track. |
| Practice beginner proofs through a game | [Natural Number Game](https://adam.math.hhu.de/#/g/leanprover-community/nng4) | The archive describes it as an introductory game about natural-number theorems. |
| Learn formal mathematics | [Mathematics in Lean](https://github.com/leanprover-community/mathematics_in_lean) | The archive calls it the main class material and strongly recommends it. |
| Learn Lean metaprogramming | [leanprover.cn](https://www.leanprover.cn) → *Metaprogramming in Lean* | The Chinese hub lists this track. |
| Follow lecture/minicourse material | [NUS Lean minicourse](https://github.com/NUS-Math-Formalization/minicourse/tree/main) | Listed as Lean lecture material. |
| Get a compact reference | [Terence Tao's Lean cheatsheet](https://docs.google.com/spreadsheets/d/1Gsn5al4hlpNc_xKoXdU6XGmMyLiX4q-LFesFVsMlANo/edit?gid=1045418473#gid=1045418473) | Listed as a Lean cheatsheet. |
| Explore the general resource entry | [ReasLab](https://beta.reaslab.io) | Listed as a learning resource; the archive gives no narrower feature description. |

### 2. Build a beginner path

Use this operational sequence when the user wants an end-to-end starting route:

1. **Setup if needed** — use the archived installation tutorial.
2. **Choose foundations** — functional programming, theorem proving, or both through the Chinese hub.
3. **Add practice** — Natural Number Game when game-based proof practice is useful.
4. **Move into formal mathematics** — prioritize *Mathematics in Lean* because the source explicitly recommends it.
5. **Branch by need** — metaprogramming, NUS minicourse, or cheatsheet for specialization/reference.

This ordering is a structural synthesis from the resource categories. Treat it as a practical route, not as an author-stated curriculum.

### 3. Route during active Lean work

| Need | Route |
|---|---|
| Run a quick Lean experiment online | [Lean official online compiler](https://live.lean-lang.org/) |
| Look up Mathlib declarations/API | [Mathlib4 documentation](https://leanprover-community.github.io/mathlib4_docs/) |
| Search for a theorem | Mathlib docs, then LeanSearch or [Moogle](https://www.moogle.ai/) |
| Ask humans when still blocked | Zulip, referenced by the archive via the Lean community homepage/sidebar |
| Try automated formalization | [Quokka](https://quokka-beta.reaslab.io/) |

For theorem/API problems, a useful synthesized escalation is: **documentation → theorem search → test in Lean → community help**.

### 4. Failure Recovery

- **Resource is unavailable** — switch to another resource serving the same archived function when one exists. For theorem search, try another search surface before escalating.
- **Resource is too broad or too advanced for the user** — reclassify the goal and move one stage earlier in the beginner path.
- **Cheatsheet does not answer a declaration-level question** — move to Mathlib documentation or theorem search.
- **Automated formalization output fails** — validate in a Lean environment, then fall back to theorem search and community help. Never treat generated Lean as correct merely because a tool produced it.
- **ReasLab or Quokka appears to have a platform bug** — first separate a Lean/code error from a service defect. The archive explicitly says bug feedback is welcome for both entries, but records no feedback channel; use only a feedback mechanism the current service itself exposes.
- **The archive does not cover the requested goal** — say so explicitly and stop attributing extra guidance to this source.

## SELF_CHECK

Before answering with this skill:

1. What is the user's actual goal: learn, run, search, automate, or get help?
2. Does the chosen resource's archived label support the claimed use?
3. Does the user need setup or prerequisite material first?
4. Is the recommendation source-derived, structurally synthesized, or an implementation safety rule?
5. Is there a listed fallback if the first route fails?
6. Have you avoided claiming unrecorded features, uptime, completeness, or correctness?
7. If citing a Chinese version of *Mathematics in Lean*, have you noted that the snapshot references “4.a” but does not contain that section or its link?

## Chapter Index

| # | Title | Key content |
|---|---|---|
| [ch01](chapters/ch01-learning-resources.md) | 学习资源 | Chinese learning tracks, Mathematics in Lean, Natural Number Game, setup, cheatsheet, minicourse, ReasLab |
| [ch02](chapters/ch02-working-resources.md) | 学习时需要的常用资源 | Zulip, Mathlib/API lookup, online compiler, Quokka, theorem search |

## Topic Index

- **API / Mathlib lookup** → ch02
- **Automated formalization / Quokka** → ch02
- **Cheatsheet** → ch01
- **Functional programming** → ch01
- **Installation** → ch01
- **LeanSearch** → ch02
- **Mathematics in Lean** → ch01
- **Metaprogramming** → ch01
- **Moogle** → ch02
- **Natural Number Game** → ch01
- **Online compiler** → ch02
- **ReasLab** → ch01
- **Theorem proving** → ch01
- **Theorem search** → ch02
- **Zulip** → ch02

## Supporting Files

- [glossary.md](glossary.md) — resource and tool terms from the archive
- [patterns.md](patterns.md) — operational routing and recovery patterns
- [cheatsheet.md](cheatsheet.md) — fast goal-to-resource decisions
- [provenance.md](provenance.md) — source traceability and synthesis labels

## Scope & Limits

The source archive is a compact resource list, not a Lean4 textbook. It records resource names, links, and short role labels; it does not contain the full tutorials, theorem content, APIs, or platform documentation behind those links. External sites can change after the 2026-09-12 snapshot. Use this skill to route and decide within the archived knowledge, then verify current external behavior when needed.
